---
title: "Actividad 5. Triage de defectos, causa raíz, plan de mejora y quality gates"
subtitle: "Sistema bajo prueba: Restful-Booker"
author:
  - Camilo Rivera Quintero
  - Karen Torres
date: "Calidad en Software II · Universidad de La Salle · 30 de octubre de 2026"
lang: es
---

# Introducción

Desde la Actividad 2 trabajamos con Restful-Booker, una API de reservas hecha en Node.js y Express que guarda los datos en memoria. En esa actividad ejecutamos el plan de pruebas y encontramos varios defectos reales. En la 3 medimos su rendimiento con k6 y en la 4 armamos un dashboard con esos resultados. Para esta actividad retomamos esos defectos y los pasamos por el flujo que vimos en clase:

```
Defectos con evidencia → Triage → Causa raíz → Plan de mejora → Quality gates en CI/CD
```

Para no perder el hilo entre una etapa y otra, guardamos todo el triage en un solo archivo, `triage/defects.json`. De ahí salen las tablas de este informe y también el primer gate del pipeline. Lo hicimos así porque, cuando el acta y el pipeline se mantienen por separado, tarde o temprano dejan de coincidir.

El profesor comentó que un piloto automatizado sumaba, así que además de proponer los gates los montamos en GitHub Actions. Primero corrimos el pipeline con el código que tenía los defectos y quedó en rojo. Después hicimos un pull request con las correcciones y quedó en verde. Las dos ejecuciones están enlazadas en la sección del piloto.

**Objetivo.** Hacer el acta de triage de cinco defectos de Restful-Booker, encontrar sus causas raíz con los 5 porqués y el diagrama de Ishikawa, priorizar un plan de mejora por impacto y esfuerzo, y demostrar en un pipeline los quality gates que evitan que esos defectos vuelvan.

**Supuestos.** La app es un fork académico de un proyecto open source. Las correcciones las hicimos sobre una copia (`app/`) para no tocar el repositorio de las actividades anteriores. El despliegue del pipeline es simulado: solo construye la imagen Docker, porque no tenemos un ambiente productivo.
