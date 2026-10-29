# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this folder is

This is not a software project: there is no code, build, lint or test tooling, and it is not a git repository. It is the workspace for **Actividad 5** of the university course *Calidad en Software* (Universidad de La Salle, UnisalleVirtual/Moodle). It is a team assignment (max 3 people), due **Sunday 2026-11-01, 23:59**. All deliverables are written in **Spanish**.

Source material:
- `actividad_5.pdf`: the official assignment statement and grading rubric (the source of truth for requirements).
- `10-29 Clase_ ... -Summary.md`: structured summary of the 2026-10-29 class, where the teacher explained what is expected. It holds the recommended table formats, severity/priority scales and KPI examples.
- `10-29 Clase_ ... -transcript.txt`: raw transcript of that class (auto-transcribed, contains errors such as "baglio" → backlog, "campage" → KPIs). Use the Summary first; check the transcript only to confirm a detail.

## Required deliverables

1. **Acta de triage**: ≥ 3 critical/high-impact defects, with agreed severity/priority, owner and dates.
2. **Análisis causa-raíz** per defect: **5 Whys + Ishikawa**, with linked evidence, separating verifiable causes from assumptions still to validate.
3. **Plan de mejora**: table of actions prioritized by impact/effort, with owner, effort (bajo/medio/alto) and a verification KPI/threshold.
4. **Propuesta técnica de Quality Gates / CI-CD**: rules and thresholds (e.g. error rate ≤ X %, latency P95 ≤ Y ms, minimum smoke coverage), fail-fast policy, recommended tools and why they were chosen.

Rubric weights (5 points total): triage 1, root-cause analysis **2** (the heaviest: rigor, evidence, verifiability), improvement plan 1, CI/CD integration 1 (graded on "evidence (pipeline/MR) and traceability").

## Expectations the teacher stated in class

- Prefer **one integrated report** with a clear narrative thread rather than separate disconnected files. Suggested outline: Introducción → Objetivo → Entradas (defectos y evidencias) → Acta de triage → Análisis causa-raíz → Plan de mejora → Quality Gates propuestos → Propuesta técnica de automatización → Anexos.
- Defects may be synthetic/simulated, but must be coherent and plausible; evidence can be steps, logs, stack traces, screenshots, HTTP errors, k6/Grafana metrics (ties to earlier course activities on performance testing).
- **Traceability is the core idea**: every defect gets a code (`D-001`, `D-002`, …) that is reused in the acta, the root-cause analysis, each improvement action, each KPI and each Quality Gate.
- Keep severity (how bad) and priority (how soon) distinct, and justify both. Scales used in class: severity Baja/Media/Alta/Crítica; priority P1 (immediately), P2 (current cycle), P3 (next sprint), P4 (backlog). Consider urgency, reproducibility, scope and any **workaround**.
- The acta should also record the triage **decision** (hotfix, release, backlog, investigation, close) and a **criterio de cierre** (how the fix is verified: regression, smoke, functional tests).
- Ishikawa categories adapted to software: personas, procesos, herramientas, entornos, datos, código, diseño.
- Example KPI thresholds from class: error rate < 1 %, latency P95 < 300 ms, all critical flows covered by smoke tests, ≥ 80 % new-code coverage, 0 critical/blocker issues, new-code duplication < 3 % (SonarQube-style quality gate conditions).
- Each Quality Gate must state what it measures, the threshold, why that threshold, and what happens when it fails (pipeline blocks). A fully working pipeline is not required, but a working pilot (even for a single defect, shown with screenshots or a pipeline run) is extra credit.

Readings referenced by the assignment: ISTQB Advanced Test Manager v3.0 (defect management), Google SRE blameless postmortems, ASQ 5 Whys, NHS Ishikawa guide, SonarQube Quality Gates.
