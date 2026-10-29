#!/usr/bin/env bash
# Ejecuta localmente los mismos quality gates que .github/workflows/quality-gate.yml,
# en el mismo orden fail-fast (de lo más barato a lo más caro). Se detiene en el primer gate que falle.
#   bash ci/run_gates.sh [archivo_log]
#   FAIL_FAST=0 bash ci/run_gates.sh   # modo diagnóstico: ejecuta todos los gates y reporta cada resultado
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="${1:-}"
if [[ -n "$LOG" ]]; then exec > >(tee "$LOG") 2>&1; fi

APP_PID=""
FAILED=0
cleanup() { [[ -n "$APP_PID" ]] && kill "$APP_PID" 2>/dev/null; }
trap cleanup EXIT

gate() {
  local id="$1" name="$2"; shift 2
  echo
  echo "=================================================================="
  echo "$id — $name"
  echo "=================================================================="
  if "$@"; then
    echo ">> $id APROBADO"
  else
    FAILED=1
    if [[ "${FAIL_FAST:-1}" == "1" ]]; then
      echo ">> $id FALLÓ — pipeline detenido (fail-fast), no se despliega"
      echo "RESULTADO FINAL: ROJO ($(date '+%Y-%m-%d %H:%M:%S'))"
      exit 1
    fi
    echo ">> $id FALLÓ (modo diagnóstico: se continúa para reportar los demás gates)"
  fi
}

smoke() {
  (cd "$ROOT/app" && PORT=3001 node ./bin/www >/dev/null 2>&1) &
  APP_PID=$!
  for _ in $(seq 1 30); do curl -sf http://localhost:3001/ping >/dev/null && break; sleep 1; done
  k6 run --quiet "$ROOT/ci/k6_smoke.js"
}

echo "Quality gates — Restful-Booker (Actividad 5) — $(date '+%Y-%m-%d %H:%M:%S')"
echo "Commit: $(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo 'sin git')"

gate G1 "Gate de triage (defects.json)" bash -c "python3 '$ROOT/triage/triage.py' validate && python3 '$ROOT/triage/triage.py' gate"
gate G2 "Escaneo de secretos (gitleaks) y dependencias (npm audit)" bash -c \
  "gitleaks dir '$ROOT/app' --config '$ROOT/.gitleaks.toml' --no-banner --redact && (cd '$ROOT/app' && npm audit --omit=dev --audit-level=high)"
gate G3+G4 "Pruebas unitarias + regresión de defectos y cobertura ≥ 80 %" bash -c "cd '$ROOT/app' && npm run --silent coverage"
gate G5 "Smoke de rendimiento k6 (error < 1 %, p95 < 300 ms, checks > 99 %)" smoke
if [[ "$FAILED" == "1" ]]; then
  echo
  echo "G6 — Despliegue condicionado: BLOQUEADO (hay gates en rojo)"
  echo "RESULTADO FINAL: ROJO ($(date '+%Y-%m-%d %H:%M:%S'))"
  exit 1
fi
gate G6 "Despliegue condicionado" bash -c "echo 'Todos los gates en verde: se habilita el despliegue (simulado: docker build en CI).'"

echo
echo "RESULTADO FINAL: VERDE ($(date '+%Y-%m-%d %H:%M:%S'))"
