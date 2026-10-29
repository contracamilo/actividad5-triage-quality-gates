# Propuesta técnica de automatización en CI/CD

## Diseño del pipeline

Los quality gates convierten los criterios de cierre del acta y los KPI del plan de mejora en reglas automáticas. El pipeline aplica una política **fail-fast**: las etapas van de la más barata a la más costosa y cada una depende de la anterior (`needs:` en GitHub Actions). Si un gate falla, el resto del flujo y el despliegue no se ejecutan.

```
push / pull request
   │
   ├─ Etapa 1 · Estático (≈ 20 s) ── G1 gate de triage · G2 gitleaks + npm audit
   │        ✗ → se detiene
   ├─ Etapa 2 · Pruebas (≈ 30 s) ─── G3 regresión D-00X + unitarias · G4 cobertura ≥ 80 %
   │        ✗ → se detiene
   ├─ Etapa 3 · Rendimiento (≈ 1 min) ─ G5 docker build + k6 smoke (error < 1 %, p95 < 300 ms)
   │        ✗ → se detiene
   └─ Etapa 4 · Despliegue ────────── G6 solo en main y con G1–G5 aprobados
```

- **Workflow:** `.github/workflows/quality-gate.yml` (se ejecuta en cada push y pull request a `main`).
- **Ejecución local equivalente:** `bash ci/run_gates.sh` ejecuta los mismos gates en el mismo orden. Con `FAIL_FAST=0` funciona en modo diagnóstico: ejecuta todos los gates y reporta cada resultado.
- **Artefactos:** reporte de cobertura (lcov) y resumen de k6 (`k6-summary.json`) publicados en cada ejecución.

## Herramientas seleccionadas y justificación

| Herramienta | Gate | Por qué se eligió | Alternativas consideradas |
|---|---|---|---|
| GitHub Actions | Orquestación (G1–G6) | El repositorio ya vive en GitHub y las actividades 2–4 usaron Actions. Es gratis para repositorios públicos y `needs:` implementa fail-fast de forma nativa. | GitLab CI, Jenkins (requiere servidor propio) |
| `triage.py` (Python stdlib) | G1 | Conecta el acta con el pipeline: lee `defects.json` y bloquea si hay defectos P1 abiertos o defectos cerrados sin prueba de regresión. No tiene dependencias. | Integración con la API de Jira (requiere credenciales) |
| gitleaks | G2 | Escáner de secretos open source y rápido (≈ 40 ms sobre la app). Permite reglas propias: se añadió `hardcoded-basic-auth`, dirigida a la causa raíz de D-001. | TruffleHog, GitHub secret scanning (no admite reglas propias en el plan gratuito) |
| npm audit | G2 | Viene incluido con npm y no requiere configuración. Bloquea vulnerabilidades high/critical en dependencias de producción. | Dependabot (avisa pero no bloquea), Snyk (requiere cuenta) |
| mocha + supertest | G3 | Es el framework que ya usa el proyecto. Cada prueba de regresión lleva el código del defecto en su nombre, lo que da trazabilidad directa con el acta. | Jest (implicaría migrar la suite) |
| c8 | G4 | Usa la cobertura nativa de V8, sin instrumentar el código, y con `--check-coverage --lines 80` falla el build por debajo del umbral. | nyc/istanbul |
| k6 | G5 | Es la herramienta de la Actividad 3, así que los umbrales salen de una línea base medida. Sus thresholds devuelven un exit code ≠ 0, lo que implementa el fail-fast de forma natural. | JMeter (más pesado para CI), Artillery |
| SonarQube / SonarCloud | G7 (recomendado) | Es el estándar para gates estáticos: cobertura de código nuevo, duplicación < 3 %, issues bloqueantes y hotspots de seguridad. Se recomienda como siguiente paso. No se implementó porque requiere cuenta, token y configurar el servidor. | — |

## Umbrales de seguridad del pipeline

| Indicador | Umbral | Origen del umbral |
|---|---|---|
| Defectos P1 abiertos | 0 | Regla de clase: no desplegar con defectos críticos o urgentes abiertos |
| Defectos cerrados sin prueba de regresión | 0 | Criterio de cierre del acta |
| Secretos en el código | 0 | Causa raíz de D-001 |
| Vulnerabilidades high/critical en dependencias | 0 | Buenas prácticas OWASP. Las moderadas sin parche se registran como riesgo aceptado. |
| Pruebas fallidas | 0 (100 % de éxito) | Criterio de cierre de D-001, D-002, D-003 y D-005 |
| Cobertura de líneas (helpers, routes, models) | ≥ 80 % | Umbral visto en clase y por defecto en "Sonar way" para código nuevo. La línea base medida fue 91 %. |
| Tasa de error HTTP (k6) | < 1 % | SLO de la Actividad 3 |
| Latencia P95 (k6) | < 300 ms | Umbral de clase. La Actividad 3 midió 6–10 ms con un SLO de 800 ms, así que el margen detecta regresiones grandes sin falsos positivos. |
| Checks funcionales del smoke | > 99 % | Los flujos críticos (crear, consultar, actualizar con token) deben funcionar bajo carga |

## Configuración recomendada para el gate de SonarQube (G7)

```yaml
# Paso adicional sugerido para el job "estatico"
- uses: SonarSource/sonarqube-scan-action@v5
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
  with:
    args: >
      -Dsonar.projectKey=restful-booker-a5
      -Dsonar.sources=app/routes,app/helpers,app/models
      -Dsonar.javascript.lcov.reportPaths=app/coverage/lcov.info
      -Dsonar.qualitygate.wait=true
```

Condiciones del quality gate en el servidor: cobertura de código nuevo ≥ 80 %, líneas duplicadas en código nuevo < 3 %, 0 issues blocker/critical y rating de seguridad A. Con `sonar.qualitygate.wait=true`, el job falla si el gate no se aprueba.

# Piloto automatizado: evidencia rojo → verde

El piloto se ejecutó sobre el historial de commits del repositorio de la actividad:

| Commit | Contenido | Resultado del pipeline |
|---|---|---|
| `02c4ced` | App original + pruebas de regresión D-00X + gates | **ROJO** (`triage/evidencia/pipeline_01_rojo.log`) |
| `2389430` | Corrección de D-001, D-002, D-003 y D-005 + actualización de dependencias | **VERDE** (`triage/evidencia/pipeline_02_verde.log`) |
| `aca97e1` | Workflow de GitHub Actions con los mismos gates | — |

**Resultado por gate**

| Gate | Ejecución en rojo (código original) | Ejecución en verde (después de las correcciones) |
|---|---|---|
| G1 triage | ✗ BLOQUEADO: D-001, D-002 y D-003 son P1 y están abiertos | ✓ 0 P1 abiertos. Los 4 defectos resueltos tienen prueba de regresión. D-004 (P2) sigue abierto sin bloquear. |
| G2 secretos | ✗ 19 hallazgos de la credencial Basic en el código y en la apidoc | ✓ 0 hallazgos. npm audit: 0 high/critical (quedó 1 moderada sin parche, como riesgo aceptado) |
| G3 pruebas | ✗ 36 pasan / **10 fallan** (todas las pruebas D-00X de defectos abiertos) | ✓ 46 pasan / 0 fallan / 1 pendiente (D-004) |
| G4 cobertura | 91,2 % de líneas | ✓ 89,8 % de líneas (≥ 80 %) |
| G5 k6 smoke | ✓ p95 = 7,51 ms; error 0,00 % | ✓ p95 = 8,48 ms; error 0,00 %; checks 100 % |
| G6 despliegue | ✗ Bloqueado | ✓ Habilitado |

**Fragmento del log en rojo (G1):**

```
D-001    Crítica  P1     open       no
D-002    Alta     P1     open       no
D-003    Alta     P1     open       no
D-004    Crítica  P2     open       no
D-005    Media    P3     open       no
RESULTADO: BLOQUEADO
  ✗ D-001 es P1 y está 'open' (debe estar resuelto antes de desplegar)
```

**Verificación de cierre con los casos originales.** Se repitieron los curl de la evidencia de la Actividad 2 contra la versión corregida (`triage/evidencia/verificacion_post_correccion.txt`). El PUT y el DELETE con el header Basic ahora responden **403**, como esperaba el criterio de cierre (antes 200/201). Las fechas invertidas y `totalprice` −50 o `"abc"` ahora se **rechazan** (antes 200 con datos corruptos). El DELETE de un id inexistente responde **404** (antes 405). Los flujos válidos con token siguen respondiendo 200.

**Lecciones del piloto**

1. Tres pruebas heredadas **afirmaban el comportamiento defectuoso**: aceptar el Basic y responder 405. La suite estaba en verde precisamente porque protegía los defectos. El gate G1 cierra esa brecha, porque un defecto solo puede cerrarse si existe una prueba con su código.
2. Las pruebas de regresión necesitan **aserciones precisas**. Al principio, dos casos de D-002 pasaban por la razón equivocada: sin header `Accept`, la API respondía 418 antes de validar. Se corrigió fijando `Accept: application/json` y verificando además que la reserva no se persistiera.
3. El gate G2 encontró **un problema que no estaba en el acta**: 7 vulnerabilidades en dependencias (1 crítica, 2 altas). Esto muestra el valor preventivo de los gates más allá de los defectos conocidos.
4. **Severidad ≠ prioridad.** D-004 es Crítico pero P2: el pipeline lo deja pasar de forma explícita y justificada, mientras el plan de mejora define su investigación y su workaround.

**Cómo reproducir**

```bash
cd app && npm ci && cd ..
FAIL_FAST=0 bash ci/run_gates.sh            # diagnóstico de todos los gates
python3 triage/triage.py gate               # solo el gate de triage
git checkout 02c4ced && bash ci/run_gates.sh  # reproducir el estado en rojo
```

# Conclusiones

- El triage separó con criterios explícitos la gravedad (severidad) de la urgencia (prioridad). Dos defectos se reclasificaron durante la sesión (D-002 subió a P1 y D-003 pasó a Alta por pérdida silenciosa de datos financieros), y D-004 quedó como Crítico pero P2 porque su corrección requiere una decisión de diseño.
- El análisis causal mostró que las causas raíz son de **proceso** más que de código: no hay requisitos de seguridad ni de reglas de negocio, no hay estándar de API y la suite caracterizaba los defectos en lugar de especificar el comportamiento esperado. Por eso el plan combina correcciones con acciones preventivas de proceso y de herramientas.
- Los quality gates cierran el ciclo de mejora continua: cada criterio de cierre y cada KPI del plan tiene una regla automática que impide que el defecto vuelva a llegar a producción. El piloto demostró el ciclo completo, del rojo al verde, con evidencia reproducible.

# Referencias

- ISTQB. (2024). *Certified Tester Advanced Level — Test Management (CTAL-TM) Syllabus v3.0*, sección Defect Management. International Software Testing Qualifications Board. https://www.istqb.org/
- Beyer, B., Jones, C., Petoff, J., & Murphy, N. R. (2016). Postmortem culture: Learning from failure. En *Site Reliability Engineering*. O'Reilly / Google. https://sre.google/sre-book/postmortem-culture/
- American Society for Quality. (s. f.). *Five Whys and Five Hows*. https://asq.org/quality-resources/five-whys
- NHS Improvement Cymru. (s. f.). *Cause and effect (fishbone) diagram*. Guía de herramientas de mejora de la calidad.
- SonarSource. (s. f.). *Quality gates*. Documentación de SonarQube. https://docs.sonarsource.com/
- Grafana Labs. (s. f.). *Thresholds*. Documentación de k6. https://grafana.com/docs/k6/latest/using-k6/thresholds/
- Gitleaks. (s. f.). *Gitleaks*. https://github.com/gitleaks/gitleaks

# Anexos

- **A. Fuente de datos del triage:** `triage/defects.json`
- **B. Herramienta de triage:** `triage/triage.py` (`validate`, `gate`, `report`, `diagrams`)
- **C. Evidencia original (Actividad 2):** `triage/evidencia/T01…T05*.txt`
- **D. Logs del pipeline:** `triage/evidencia/pipeline_01_rojo.log`, `triage/evidencia/pipeline_02_verde.log`
- **E. Verificación posterior a la corrección:** `triage/evidencia/verificacion_post_correccion.txt`
- **F. Pruebas de regresión:** `app/tests/regression.spec.js`
- **G. Pipeline:** `.github/workflows/quality-gate.yml`, `ci/run_gates.sh`, `ci/k6_smoke.js`, `.gitleaks.toml`
