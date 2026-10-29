---
title: "Actividad 5 — Triage de defectos, análisis causa raíz, plan de mejora y quality gates"
subtitle: "Sistema bajo prueba: Restful-Booker"
author:
  - Camilo Rivera Quintero
  - Karen Torres
date: "Calidad en Software II · Universidad de La Salle · 30 de octubre de 2026"
lang: es
---

# Introducción

Este informe documenta un ciclo completo de gestión de defectos sobre **Restful-Booker**, la API REST de reservas (Node.js/Express con LokiJS en memoria) que el equipo ha usado como sistema bajo prueba desde la Actividad 2. Allí se ejecutó el Master Test Plan y se confirmaron defectos reales, con evidencia curl y pruebas automatizadas. La Actividad 3 midió su rendimiento con k6 y la Actividad 4 consolidó esos KPI en un dashboard. Esta actividad toma esos hallazgos como **entrada** y los lleva por el flujo de calidad visto en clase:

```
Entradas (defectos + evidencia) → Triage → Causa raíz (5 porqués + Ishikawa) → Plan de mejora → Quality gates en CI/CD
```

Los defectos no son simulados: cada uno conserva el código con el que se registró en la Actividad 2 (DEF-0X, R-X) y recibe un código nuevo (**D-001 a D-005**) que se mantiene igual en el acta, el análisis causal, las acciones, los KPI, las pruebas de regresión y los gates del pipeline. Para asegurar esa trazabilidad, toda la información del triage vive en un único archivo de datos (`triage/defects.json`). Las tablas de este informe y el gate de triage del pipeline se generan a partir de él con la herramienta `triage/triage.py`.

Como valor agregado, además de proponer los quality gates se **implementó un piloto automatizado**: un pipeline de GitHub Actions (más un script equivalente para ejecución local) que se ejecutó primero en **rojo** sobre el código con los defectos y luego en **verde** después de corregir los cuatro defectos de mayor prioridad. Ambas ejecuciones quedaron registradas como evidencia.

# Objetivo

Elaborar un acta de triage para cinco defectos reales de Restful-Booker, analizar sus causas raíz con los 5 porqués y el diagrama de Ishikawa, construir un plan de mejora priorizado por impacto/esfuerzo con responsables, esfuerzo y KPI de verificación, y proponer, implementar y evidenciar en un pipeline CI/CD los quality gates que previenen la recurrencia de esos defectos.

**Alcance y supuestos**

- Equipo: Camilo Rivera Quintero y Karen Torres. Los roles del comité de triage se describen en el acta.
- La aplicación es un fork académico de un proyecto de código abierto. Las correcciones se hicieron sobre una copia en el repositorio de esta actividad (`app/`), sin modificar el de actividades anteriores.
- El despliegue del pipeline es **simulado** (construcción de la imagen candidata). No existe un ambiente productivo real.
