# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Deliverable for **Actividad 5** of *Calidad en Software II* (Universidad de La Salle; team Camilo Rivera Quintero + Karen Torres; due 2026-11-01). The assignment asks for a defect triage record, root-cause analysis (5 Whys + Ishikawa), an improvement plan and CI/CD quality gates. The rubric is in `actividad_5.pdf` and the class guidance is in the `10-29 Clase_…` summary/transcript. Everything user-facing is written in **Spanish**.

The system under test is **Restful-Booker** (Node/Express + in-memory LokiJS). `app/` is a copy of `../restful-booker`, the repo used for activities 2–4. The defects are real ones found in activity 2 (DEF-01..04, R1) and are renumbered here as **D-001..D-005**.

## Architecture: one data source drives everything

`triage/defects.json` is the single source of truth: the triage session, the defects with their evidence, the agreed severity/priority, the 5 Whys, the Ishikawa causes (marked `verificada` or `suposición`), the actions with KPIs, and the gates G1–G7. Everything else is derived from it:

- `triage/triage.py validate`: checks rubric completeness (exit 1 if anything is missing).
- `triage/triage.py gate`: **quality gate G1**. Fails if any P1 defect isn't `resolved`, or if a resolved defect has no `it('D-00X …')` in `app/tests/regression.spec.js`.
- `triage/triage.py report` / `diagrams`: write `informe/generado.md` and `informe/img/*.png` (diagrams need matplotlib).
- `informe/build.sh`: generated sections + hand-written `00_intro.md` / `90_propuesta.md` → DOCX (Homebrew pandoc at `/opt/homebrew/bin/pandoc`; the Anaconda pandoc is an x86 binary and fails) and PDF (Chrome headless, `estilo.css`).

When a defect changes, edit `defects.json` and rebuild. Don't hand-edit `informe/generado.md`.

## Commands

```bash
cd app && npm ci                         # first time
cd app && npm test                       # mocha: tests/spec.js + tests/regression.spec.js
cd app && npx mocha tests/regression.spec.js -g "D-002"   # one defect's regression tests
cd app && npm run coverage               # c8, fails under 80 % lines (gate G4)
bash ci/run_gates.sh [log]               # all gates locally, fail-fast
FAIL_FAST=0 bash ci/run_gates.sh         # diagnostic: run every gate, report each
bash informe/build.sh                    # regenerate the report (DOCX + PDF)
```

Local gates require `gitleaks`, `k6`, Python 3 and Node 22. `.github/workflows/quality-gate.yml` runs the same gates in the same order: estático (G1, G2) → pruebas (G3, G4) → rendimiento (G5, docker + k6) → despliegue (G6, simulated, only on main).

## Gotchas

- Regression tests must send `Accept: application/json` (use `createBooking`). Without it the API returns 418 before validation, and a "should reject" test passes for the wrong reason.
- Rejected bookings return **500** on POST (pre-existing behavior, logged as a P4 observation in the acta). That's why tests assert `status >= 400` instead of 400. PUT returns 400.
- D-004 (overlapping bookings) is deliberately open as Crítica/P2. Its test is `it.skip`, so G1 doesn't block on it.
- `.gitleaks.toml` has a custom `hardcoded-basic-auth` rule. `tests/` is allowlisted because the regression tests use that credential on purpose.
- Git history is part of the evidence: commit `02c4ced` is the red state and `68e8805` the green fix (published history: workflow `6c87c84`, PR #1 on github.com/contracamilo/actividad5-triage-quality-gates; the pre-publication hashes survive in local tag `historial-local-original`). Logs are in `triage/evidencia/pipeline_0{1,2}_*.log`. The report cites these hashes, so don't rewrite history.
