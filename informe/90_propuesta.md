# Propuesta técnica y piloto automatizado

## Cómo armamos el pipeline

El workflow está en `.github/workflows/quality-gate.yml` y corre en cada push y en cada pull request a `main`. Cada etapa depende de la anterior (`needs:`), así que si un gate falla el resto no se ejecuta y no se gasta tiempo construyendo algo que ya sabemos que no sirve.

```
push / pull request
   ├─ Etapa 1, estático (~20 s) ...... G1 triage, G2 gitleaks + npm audit
   ├─ Etapa 2, pruebas (~30 s) ....... G3 regresión D-00X, G4 cobertura ≥ 80 %
   ├─ Etapa 3, rendimiento (~1 min) .. G5 docker + k6 smoke
   └─ Etapa 4, despliegue ............ G6 solo en main y con todo en verde
```

Casi todas las herramientas ya las conocíamos de actividades anteriores. Mocha y supertest son las pruebas que ya traía el proyecto, y k6 lo usamos en la Actividad 3. Las nuevas fueron gitleaks, que elegimos porque permite reglas propias y le agregamos una para detectar credenciales Basic como la de D-001, y c8 para la cobertura. El gate G1 es un script nuestro en Python que lee el acta y bloquea si queda algún P1 abierto o si se marcó como resuelto un defecto que no tiene prueba.

Los umbrales no los sacamos de la nada. El 80 % de cobertura es el que vimos en clase, y la línea base medida fue de 91 %. Para k6 pusimos p95 < 300 ms: en la Actividad 3 medimos entre 6 y 10 ms, así que el margen detecta una regresión grande sin dar falsas alarmas. SonarCloud (G7) lo dejamos como recomendación porque necesita cuenta y token. La configuración que proponemos es cobertura de código nuevo ≥ 80 %, duplicación < 3 % y cero issues bloqueantes.

## Resultado: de rojo a verde

El repositorio es <https://github.com/contracamilo/actividad5-triage-quality-gates>. Seguimos el flujo normal de un cambio: `main` quedó con los defectos y las correcciones entraron por un pull request.

| Qué se ejecutó | Resultado |
|---|---|
| `main` con el código original ([ejecución 41017376828](https://github.com/contracamilo/actividad5-triage-quality-gates/actions/runs/41017376828)) | **Rojo.** G1 bloqueó por D-001, D-002 y D-003 abiertos, y los demás gates ni siquiera arrancaron. |
| [PR #1](https://github.com/contracamilo/actividad5-triage-quality-gates/pull/1) con las correcciones ([ejecución 41017467045](https://github.com/contracamilo/actividad5-triage-quality-gates/actions/runs/41017467045)) | **Verde.** G1 a G5 aprobados. 46 pruebas pasan y 1 queda pendiente (D-004), con cobertura de 89,8 %, p95 de 6,37 ms y 0 % de errores en 901 peticiones. |

Como en GitHub el rojo se detiene en el primer gate, también corrimos `ci/run_gates.sh` en local con `FAIL_FAST=0` para ver qué decía cada gate sobre el código original. Con los defectos abiertos fallaban 10 pruebas, gitleaks encontraba la credencial Basic 19 veces y npm audit reportaba vulnerabilidades altas. Los logs están en `triage/evidencia/`. También repetimos los curl de la Actividad 2 contra la versión corregida. El Basic ahora responde 403, las fechas invertidas y los precios negativos se rechazan y el DELETE de un id que no existe responde 404.

## Lo que aprendimos

- **Las pruebas estaban protegiendo los defectos.** Tres pruebas que ya traía el proyecto comprobaban justo el comportamiento malo (aceptar el Basic, responder 405). La suite pasaba en verde y por eso nadie lo había notado.
- **Una prueba puede pasar por la razón equivocada.** Al principio dos de nuestras pruebas de D-002 pasaban porque la API respondía 418 al no recibir el header `Accept`, no porque validara las fechas. Lo notamos porque fallaban menos pruebas de las que esperábamos, y lo corregimos.
- **Los gates encontraron cosas que no estaban en el acta.** npm audit detectó 7 vulnerabilidades en dependencias, entre ellas una crítica. Las arreglamos actualizando versiones. Queda una moderada sin parche, que dejamos como riesgo aceptado.
- **Severidad y prioridad no son lo mismo.** D-004 es crítico, pero lo dejamos en P2 porque arreglarlo exige definir qué es una habitación. El pipeline no lo bloquea, y esa decisión quedó justificada en el acta.

# Conclusiones

Lo más útil de la actividad fue ver que la mayoría de las causas raíz no estaban en el código, sino en el proceso: no había requisitos de seguridad, ni reglas de negocio escritas, ni un estándar para los códigos de respuesta. Por eso el plan de mejora mezcla correcciones puntuales con cambios de proceso.

También nos quedó claro para qué sirve un quality gate. Un criterio de cierre que vive solo en un documento se olvida, mientras que uno que está en el pipeline se revisa en cada cambio. Con el piloto pudimos ver el ciclo completo funcionando: el pipeline bloqueó el código con defectos y dejó pasar el que tenía las correcciones.

# Referencias

- ISTQB. (2024). *Certified Tester Advanced Level, Test Management (CTAL-TM) Syllabus v3.0*. https://www.istqb.org/
- Beyer, B., Jones, C., Petoff, J. y Murphy, N. R. (2016). Postmortem culture: Learning from failure. En *Site Reliability Engineering*. O'Reilly. https://sre.google/sre-book/postmortem-culture/
- American Society for Quality. (s. f.). *Five Whys and Five Hows*. https://asq.org/quality-resources/five-whys
- SonarSource. (s. f.). *Quality gates*. https://docs.sonarsource.com/
- Grafana Labs. (s. f.). *Thresholds*. Documentación de k6. https://grafana.com/docs/k6/latest/using-k6/thresholds/

# Anexos

El acta (`triage/defects.json`), la evidencia, las pruebas y el pipeline están en el repositorio de GitHub citado arriba.
