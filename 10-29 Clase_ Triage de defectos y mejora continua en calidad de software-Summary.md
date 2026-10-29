# 10-29 Clase: Triage de defectos y mejora continua en calidad de software

# Unidad 3: análisis de resultados, triage de defectos y mejora continua en calidad de software
La Unidad 3 del curso introduce una etapa del trabajo en calidad de software orientada principalmente al **análisis de resultados** y a la **mejora continua**. A diferencia de fases anteriores, en las que el énfasis estaba más concentrado en componentes técnicos como la planificación de pruebas, la ejecución de pruebas de rendimiento o la recolección de métricas, esta unidad desplaza el foco hacia actividades de proceso: interpretar hallazgos, clasificar defectos, tomar decisiones, identificar causas raíz y formular acciones correctivas y preventivas.
Esto no significa que la dimensión técnica desaparezca. En un entorno de calidad de software siempre hay elementos técnicos: pruebas, logs, métricas, herramientas de monitoreo, despliegues, automatización y validaciones. Sin embargo, en esta unidad el interés principal está en comprender cómo se gestionan los resultados obtenidos. La calidad no se reduce a encontrar errores; implica documentarlos, analizarlos, priorizarlos, asignar responsables, definir fechas, establecer criterios de cierre y proponer mejoras sostenibles.
Desde esta perspectiva, la unidad exige una mirada más gerencial y de gestión de calidad. Se busca que el estudiante pase de una visión centrada únicamente en la ejecución técnica a una comprensión más integral del proceso de calidad, entendido como un ciclo continuo de control, aprendizaje y mejora.
La clase se organiza alrededor de tres grandes componentes:
1. **La sesión de triage**, en la que se revisan, clasifican y priorizan defectos.
2. **El análisis de causa raíz**, mediante herramientas como los **cinco porqués** y el **diagrama de Ishikawa** o **espina de pescado**.
3. **El plan de mejora**, que traduce los hallazgos en acciones concretas, indicadores, responsables, umbrales y posibles **Quality Gates**.
Más adelante, en la actividad 6, se abordará también la **auditoría cruzada**, entendida como una revisión entre frentes o equipos para validar auditorías realizadas por otros. No obstante, el núcleo de esta parte de la unidad corresponde al laboratorio de triage, al análisis causal y a la construcción de un plan de mejora asociado a los defectos encontrados.
---
# El laboratorio de triage como flujo de trabajo de calidad
El laboratorio de triage tiene como propósito orientar el análisis de defectos dentro de un proceso formal de calidad de software. La actividad no consiste simplemente en listar errores, sino en demostrar que se sabe **gestionar un defecto de software**: documentarlo, clasificarlo, analizarlo, priorizarlo, asignar responsables, definir tiempos de atención y establecer mecanismos para evitar su recurrencia.
En calidad de software, aquello que no se mide, no se registra o no queda establecido dentro de un proceso formal tiende a perderse. Por eso, los **reportes**, los **hallazgos**, las **fechas**, las **evidencias** y las decisiones tomadas son elementos fundamentales. Esta lógica se relaciona directamente con las auditorías, porque una auditoría valida si las actividades se están ejecutando de forma correcta, trazable y conforme a lo definido.
El laboratorio puede entenderse como un flujo progresivo:
```text
Entradas del laboratorio
        ↓
Triage de defectos
        ↓
Análisis de causa raíz
        ↓
Plan de mejora y Quality Gates
```
La primera etapa reúne los defectos y sus evidencias mínimas. La segunda permite discutirlos y clasificarlos en una sesión de triage. La tercera busca comprender por qué ocurrieron realmente. Finalmente, el plan de mejora convierte las conclusiones en acciones concretas, medibles y orientadas a prevenir que los problemas se repitan.
Aunque algunos defectos puedan construirse con datos sintéticos o escenarios simulados, el objetivo central no es probar que el defecto existe en un sistema real, sino evidenciar que el estudiante comprende cómo se reporta, clasifica, analiza y gestiona un hallazgo dentro de un proceso de calidad de software.
---
# Capa de entrada: defectos reportados y evidencia mínima
La primera fase del laboratorio corresponde a la **capa de entrada**. En ella se recopilan los defectos identificados durante un proceso de auditoría, pruebas de software o análisis de resultados. Esta fase es el punto de partida del trabajo, porque proporciona los insumos necesarios para la discusión posterior.
Cada defecto reportado debe contar con una evidencia mínima. Esta evidencia puede incluir pasos para reproducir el problema, logs, stack traces, capturas de pantalla, videos, métricas, resultados de pruebas, errores HTTP, trazas de navegador o cualquier otro elemento que permita comprender qué ocurrió. También puede proponerse inicialmente una severidad, aunque dicha severidad podrá discutirse y ajustarse durante la sesión de triage.
La capa de entrada se conecta con actividades previas del curso. Si ya se ejecutaron pruebas de rendimiento o carga con herramientas como Grafana, K6 u otras tecnologías de monitoreo, los resultados obtenidos pueden transformarse en evidencia para el laboratorio. Por ejemplo, una métrica de latencia, un error HTTP 500, un timeout, una saturación de conexiones o una degradación del servicio pueden constituir insumos válidos para analizar un defecto.
En la práctica profesional, muchas organizaciones registran estos hallazgos en sistemas de seguimiento de bugs. Allí se adjuntan evidencias, se describen los pasos de reproducción, se indica el resultado esperado y el resultado obtenido, y se asigna el defecto a un responsable. Para el laboratorio, los estudiantes pueden usar evidencias reales o sintéticas, siempre que sean coherentes y plausibles.
---
# Codificación, descripción e impacto de los defectos
Para trabajar los defectos de forma ordenada, lo primero es **codificarlos**. Cada defecto debe tener un identificador único que permita hacer seguimiento, buscarlo, referenciarlo y relacionarlo con evidencias, decisiones, causas y acciones de mejora.
La codificación puede ser sencilla, por ejemplo: D-001, D-002, D-003. También puede construirse un esquema más elaborado, en el que ciertas letras indiquen el proyecto, el módulo o el tipo de defecto. Si se trabaja con un único software, basta con un consecutivo claro. Lo importante es que exista trazabilidad.
Además del código, el defecto debe tener una descripción breve y precisa. Una buena descripción permite entender el problema sin ambigüedad. Algunos ejemplos trabajados o sugeridos durante la clase son:
- “Pago aprobado sin resultado visible”.
- “Descuento calculado incorrectamente”.
- “Login intermitente en horas pico”.
- “Botón de enviar fuera de la pantalla”.
- “PDF tarda más de 35 segundos en descargar”.
Estas descripciones son cortas, pero identifican con claridad el comportamiento defectuoso. Luego, cada defecto debe ampliarse con evidencia, impacto, reproducibilidad, alcance, severidad, prioridad y decisión de triage.
El **impacto principal** explica por qué el defecto es relevante. Puede involucrar afectación funcional, pérdida de confianza del usuario, errores de negocio, cobros incorrectos, indisponibilidad parcial, degradación del servicio, pérdida económica, corrupción de datos o incumplimientos legales.
Por ejemplo, un pago aprobado sin resultado visible puede afectar una operación crítica y deteriorar la confianza del usuario. Un descuento mal calculado puede generar cobros equivocados. Un login intermitente en horas pico puede hacer que los usuarios perciban que la aplicación está caída. Un botón fuera de pantalla puede bloquear una operación en dispositivos móviles. Un PDF que tarda más de 35 segundos en descargarse puede indicar una degradación importante del servicio.
El impacto también ayuda a construir indicadores o KPIs. Si se sabe qué tipo de consecuencia produce cada defecto, es posible definir métricas para reducir la recurrencia, disminuir tiempos de solución o priorizar correcciones que afectan operaciones críticas.
---
# La sesión de triage: clasificación, decisión y trazabilidad
La **sesión de triage** es un espacio de análisis y decisión en el que se revisan defectos, hallazgos o problemas identificados durante un proceso de calidad. Su propósito no es simplemente enumerar errores, sino clasificarlos, priorizarlos, asignar responsables y definir qué se hará con ellos.
En la práctica, un triage es una reunión en la que participan distintos actores involucrados en el producto de software. Normalmente intervienen:
- el equipo de calidad, que realizó pruebas y encontró hallazgos;
- los ingenieros de desarrollo, que conocen la implementación técnica y suelen encargarse de corregir defectos;
- los dueños del producto o de la aplicación;
- usuarios funcionales, líderes funcionales o representantes del negocio.
De manera general, pueden distinguirse tres grupos: quienes encontraron los defectos, quienes deben analizarlos y corregirlos, y quienes representan el uso o el valor funcional del sistema.
Durante la sesión se acuerdan aspectos como la **severidad**, la **prioridad**, los **responsables**, los **tiempos de atención** y las decisiones de gestión. Estas decisiones pueden consistir en crear un hotfix, incluir el defecto en un release, pasarlo al backlog, investigarlo con mayor profundidad o planificar una actualización futura.
El triage es, por tanto, un mecanismo de coordinación. Permite que los hallazgos no queden como simples errores reportados, sino que se conviertan en compromisos claros y auditables. En el contexto de la actividad, se espera que los estudiantes elaboren un **acta de triage** que simule una situación real en la que un equipo revisa defectos, discute su impacto y establece responsables y fechas.
El producto mínimo solicitado incluye un acta con **tres defectos** identificados. Para cada defecto debe registrarse, como mínimo:
- severidad;
- prioridad;
- responsables;
- fechas asociadas a su tratamiento.
Aunque el mínimo puede ser de tres defectos, el docente sugiere que trabajar con cinco puede permitir un ejercicio más completo, porque facilita comparar severidades, prioridades, impactos y acciones de mejora.
---
# Severidad, prioridad, impacto y urgencia
Uno de los objetivos fundamentales del triage es diferenciar adecuadamente entre **severidad** y **prioridad**. Aunque estos términos suelen confundirse, cumplen funciones distintas dentro de la gestión de defectos.
La **severidad** se refiere a la gravedad del defecto en términos de impacto técnico, funcional o de negocio. Evalúa qué tan serio es el daño producido: si el sistema se cae, si una funcionalidad crítica no funciona, si se corrompen datos, si se afecta gravemente al usuario o si se genera pérdida económica.
La **prioridad**, en cambio, indica la rapidez con que debe atenderse el defecto. Responde a la pregunta: ¿qué tan pronto necesitamos corregirlo? La prioridad depende del riesgo de negocio, del release, de los usuarios afectados, de fechas críticas y del contexto operativo.
Por eso, un defecto puede ser severo, pero no necesariamente ser el primero en resolverse si existen restricciones de contexto, dependencias técnicas o un impacto inmediato distinto. También puede ocurrir lo contrario: un defecto de severidad media puede tener prioridad alta si bloquea una actividad importante que debe ejecutarse pronto.
El docente ilustra esta diferencia con el caso de un botón mal alineado. En principio, un botón desalineado podría parecer un defecto visual de severidad media o baja. Sin embargo, si ese botón impide finalizar una inscripción masiva, entonces la prioridad se vuelve alta, porque bloquea un proceso relevante.
También se menciona el caso de un defecto poco frecuente, pero con consecuencias críticas. Si ocurre pocas veces, pero cuando ocurre destruye datos, interrumpe una operación fundamental o produce pérdida económica, debe tratarse con gran atención. En un comercio electrónico, si muchos usuarios no pueden comprar durante una fecha clave como Black Friday, la empresa puede perder ventas significativas. Todo aquello que implique pérdida económica explícita puede considerarse crítico en determinados contextos.
La severidad mira la gravedad del defecto. La prioridad mira la urgencia de actuar.
---
## Escalas posibles de severidad y prioridad
Las escalas pueden variar según la organización. Una clasificación posible de severidad es la siguiente:
| Severidad | Descripción general |
| --- | --- |
| Baja | Defecto menor, de bajo impacto, que afecta casos específicos o no bloquea procesos relevantes. |
| Media | Defecto con impacto funcional moderado, que afecta la experiencia o alguna funcionalidad sin comprometer gravemente el negocio. |
| Alta | Defecto que afecta de forma importante una funcionalidad, usuarios o procesos del negocio. |
| Crítica | Caída total, corrupción de datos, pérdida económica significativa, incumplimiento legal o riesgo institucional grave. |
| El docente aclara que esta escala es orientativa. Algunas organizaciones trabajan solo con tres niveles: alta, media y baja. Otras, por su naturaleza, manejan prácticamente solo alta y media. También existe una línea delgada entre severidad alta y crítica. En algunas empresas, lo crítico se reserva para eventos con consecuencias legales, demandas potenciales, pérdidas económicas graves o situaciones que requieren acción inmediata. |  |
Para la prioridad puede emplearse una codificación como P1, P2, P3 y P4:
| Prioridad | Acción esperada |
| --- | --- |
| P1 | Se atiende de inmediato. |
| P2 | Se trabaja en el ciclo actual. |
| P3 | Se programa para el próximo sprint. |
| P4 | Se deja en backlog para atenderlo cuando haya disponibilidad. |
| **Nota:** En la transcripción aparece la palabra “baglio”, pero por el contexto de gestión ágil de software la corrección altamente probable es **backlog**. |  |
---
# Alcance, reproducibilidad y evidencia
Para clasificar un defecto no basta con saber qué falla. Es necesario hacer “zoom” sobre el problema y responder preguntas más específicas: cuándo ocurre, a quién afecta, bajo qué condiciones se reproduce, cuál es su impacto real y qué evidencia lo sustenta.
El **alcance** permite determinar si el defecto afecta a un usuario, a varios usuarios o a todos. También puede estimarse en porcentaje cuando existen datos de uso. Por ejemplo, si un defecto solo ocurre en Android y el 70 % de los usuarios accede desde Android, entonces el defecto podría afectar potencialmente al 70 % de los usuarios.
La **reproducibilidad** indica si el defecto ocurre siempre, ocasionalmente o solo bajo ciertas condiciones. Por ejemplo, un botón fuera de pantalla puede ocurrir únicamente en celulares Android, pero no en iPhone. Un login intermitente puede fallar solo en horas pico. Un PDF puede tardar demasiado solo cuando el archivo es grande o cuando el sistema se encuentra bajo carga.
Esta información es esencial porque evita clasificaciones arbitrarias. La severidad y la prioridad deben sustentarse en criterios observables: evidencia, impacto, alcance, reproducibilidad y riesgo.
El docente insiste en que las decisiones de triage deben basarse en **evidencia**, no en intuiciones. Expresiones como “creo que solo me pasa a mí”, “siempre me ocurre”, “el software no me quiere” o “tengo mala suerte” no son evidencia técnica. Pueden ser un punto de partida para investigar, pero no son fundamento suficiente para clasificar un defecto.
La evidencia puede incluir logs, capturas, trazas, métricas, horarios de ocurrencia, pasos de reproducción, errores HTTP, reportes de monitoreo, impacto económico o datos de usuarios afectados. Un proceso riguroso de calidad requiere información concreta para evitar decisiones subjetivas y facilitar la comunicación entre áreas técnicas, negocio, soporte, desarrollo y gestión.
---
# Urgencia, matrices de clasificación y workaround
Además de impacto y severidad, debe analizarse la **urgencia**. La urgencia indica qué tan pronto debe atenderse un defecto. Para organizar mejor esta evaluación, el docente recomienda utilizar matrices o tablas que crucen variables, como impacto y urgencia.
Una lógica sencilla de priorización es la siguiente:
| Situación | Decisión orientativa |
| --- | --- |
| Importante y urgente | Hacerlo primero. |
| Importante, pero no urgente | Programarlo para más adelante. |
| Urgente, pero no importante | Delegarlo. |
| No urgente y no importante | Puede no requerir acción inmediata. |
| Esta lógica ayuda a evitar que todo sea tratado como crítico. No todos los defectos tienen el mismo valor ni la misma urgencia. Incluso puede ocurrir que solicitudes antiguas hayan perdido relevancia. El docente menciona el caso de un equipo de soporte que revisaba casos antiguos y encontró uno con seis meses sin solución. Si durante seis meses nadie reclamó por ese caso, probablemente la necesidad desapareció o el contexto cambió. En situaciones así, puede ser razonable cerrar el caso, porque aquello que se solicitó puede haber dejado de tener valor. |  |
Otro concepto importante es el **workaround**, entendido como una alternativa temporal o plan de contingencia que permite operar mientras se corrige la causa del problema. La existencia de un workaround puede modificar la urgencia de un defecto, aunque no necesariamente elimina su importancia.
Por ejemplo, si un sistema no genera recibos automáticamente, podría definirse una alternativa temporal: cada noche se descargan los pagos, se ejecuta manualmente un proceso y se envían los recibos por correo. Esta solución no corrige la causa raíz, pero reduce el impacto mientras se implementa la corrección definitiva.
Por eso, durante el triage no solo debe preguntarse “¿cuándo se corrige?”, sino también “¿qué hacemos mientras tanto para disminuir el impacto?”.
---
# Decisión de triage, acta y criterio de cierre
Después de revisar la evidencia, discutir el impacto, evaluar la urgencia y acordar la clasificación, el proceso debe quedar documentado en un **acta de triage**. Esta acta registra los acuerdos derivados de la revisión de defectos y permite que el proceso sea trazable y auditable.
Un acta de triage puede incluir campos como:
| Campo | Propósito |
| --- | --- |
| Código del defecto | Identificación única del hallazgo. |
| Descripción | Explicación breve del problema. |
| Evidencia | Datos que sustentan el defecto. |
| Impacto | Consecuencias técnicas, funcionales o de negocio. |
| Severidad acordada | Gravedad del defecto. |
| Prioridad acordada | Urgencia de atención. |
| Responsable | Persona, rol o equipo encargado. |
| Decisión | Acción acordada: hotfix, release, backlog, investigación, cierre. |
| Fecha o plazo | Momento de registro, compromiso o seguimiento. |
| Criterio de cierre | Forma de validar que el defecto quedó resuelto. |
| El **criterio de cierre** es especialmente importante. No basta con corregir el defecto; se debe validar que la corrección funcionó. Esto suele hacerse mediante pruebas posteriores a la corrección, pruebas de regresión, pruebas funcionales o pruebas de humo, dependiendo del contexto. |  |
El docente menciona las **pruebas de humo**, aclarando que suelen asociarse con validaciones posteriores a una salida a producción o con pruebas ejecutadas después de un despliegue, normalmente con datos sintéticos o controlados. En cualquier caso, el punto central es que una corrección debe verificarse antes de dar el defecto por cerrado.
---
# Análisis de causa raíz: del síntoma al origen del problema
Una vez realizado el triage, se avanza hacia el **análisis de causa raíz**. Esta etapa busca responder por qué está fallando realmente el software. En calidad de software, limitarse a aplicar soluciones superficiales puede generar problemas mayores a futuro. El docente utiliza la idea de “pañitos de agua tibia” para referirse a soluciones que ocultan temporalmente el síntoma, pero no eliminan la causa que lo produce.
La causa raíz es la razón profunda que origina un defecto o problema. Si solo se corrige el síntoma, el defecto puede reaparecer en otro módulo, bajo otras condiciones o en una versión posterior. En cambio, cuando se comprende la causa raíz, es posible proponer acciones de mejora más eficaces y sostenibles.
Para este análisis se proponen dos herramientas principales:
- la técnica de los **cinco porqués**;
- el **diagrama de Ishikawa**, también llamado **espina de pescado** o diagrama de causa-efecto.
Estas herramientas pueden usarse de manera alternativa o complementaria. El docente aclara que no es obligatorio aplicar ambas técnicas de la misma manera a todos los defectos. Si se analizan cinco defectos, por ejemplo, se pueden aplicar los cinco porqués a tres de ellos y la espina de pescado a los otros dos. Lo importante es evidenciar la capacidad de seleccionar y aplicar herramientas de análisis causal.
---
# La técnica de los cinco porqués
La estrategia de los **cinco porqués** consiste en preguntar repetidamente “¿por qué?” frente a un problema identificado, con el objetivo de profundizar progresivamente hasta encontrar una causa raíz plausible y verificable.
El número cinco no debe entenderse de manera rígida. Funciona como una guía metodológica para no quedarse en explicaciones superficiales. Lo importante es construir una cadena lógica en la que cada respuesta esté conectada con la anterior y esté respaldada por evidencia o, si no lo está, quede señalada como supuesto pendiente por validar.
Cada respuesta debe ser:
- concreta;
- basada en evidencia;
- conectada lógicamente con la respuesta anterior.
Por ejemplo, decir “el sistema falla” es demasiado general. Se debe preguntar por qué falla. Tal vez la respuesta sea que las conexiones hacia la base de datos no funcionan. Luego se pregunta por qué ocurre eso. Quizá se descubre que se genera un timeout. Después se sigue profundizando hasta llegar a una causa más estructural del proceso.
Una regla clave es diferenciar entre **causas validadas** y **supuestos**. Una causa validada tiene respaldo en evidencias, métricas, logs o revisión técnica. Un supuesto puede orientar la investigación, pero debe quedar identificado como pendiente de confirmación.
---
## Ejemplo: error HTTP 500 en el login durante horas pico
El docente presenta un ejemplo aplicado a un sistema universitario, como el acceso a Moodle. El síntoma inicial es que el login falla con error **HTTP 500** en ciertas horas, especialmente hacia las 6:00 p. m., cuando comienzan clases nocturnas y muchos usuarios intentan ingresar al mismo tiempo.
El análisis mediante cinco porqués puede organizarse así:
| Nivel | Pregunta y respuesta |
| --- | --- |
| Síntoma | El login falla con HTTP 500 en horas pico. |
| ¿Por qué? | Porque se agota el pool de conexiones a la base de datos. |
| ¿Por qué? | Porque los intentos que terminan en timeout no liberan su conexión. |
| ¿Por qué? | Porque el manejo de errores no cierra la conexión en la ruta de excepción. |
| ¿Por qué? | Porque en las pruebas de carga no se simulan fallos de este tipo. |
| Causa raíz | El proceso no exige una prueba de carga antes de cada release. |
| Este análisis muestra que el problema no era simplemente que “el login fallaba”. Tampoco era únicamente un problema de conexiones a la base de datos. La causa raíz estaba en el proceso de calidad: no se exigía una prueba de carga antes de cada release que simulara condiciones de alta concurrencia y posibles fallos. |  |
Esta conclusión conduce a una acción concreta de mejora: incorporar en el pipeline una prueba de carga que permita verificar cuántos usuarios puede soportar el sistema antes de llegar a producción.
**Nota:** En la transcripción aparece “BUC”, pero por contexto corresponde probablemente a **bug**. Se corrige el término por ser una interpretación altamente fiable dentro del tema tratado.
---
# El diagrama de Ishikawa o espina de pescado
Otra herramienta propuesta para el análisis causal es el **diagrama de Ishikawa**, conocido también como **espina de pescado** o **diagrama de causa-efecto**. Esta herramienta permite representar visualmente las posibles causas de un problema, agrupándolas por categorías.
El defecto o problema principal se ubica en la “cabeza” del pescado, mientras que las causas posibles se organizan en las “espinas”. Esta representación ayuda a ordenar el análisis y evita que el equipo se limite a una única explicación.
La herramienta nació en contextos industriales, de producción y procesos manuales. Por ejemplo, en un proceso de fabricación podría analizarse un problema como “sellos defectuosos en una bolsa de 1 kg”. Las causas se agrupan en categorías tradicionales como:
- mano de obra;
- métodos;
- maquinaria;
- medición;
- materia prima;
- medio ambiente.
A partir de cada categoría se exploran causas más específicas. En mano de obra, por ejemplo, podría aparecer falta de capacitación o falta de sensibilización del personal. En medio ambiente, podrían considerarse factores como temperatura o condiciones del entorno. La lógica consiste en ir de lo macro a lo micro: desde grandes familias de causas hacia causas particulares.
**Nota:** En la transcripción aparecen expresiones como “Ichihuaca”, “Chicagua”, “vaina de Chicagua” o “esquina de pescado”. Por el contexto de calidad y análisis de causa raíz, la corrección altamente probable es **Ishikawa** y **espina de pescado**.
---
## Adaptación del Ishikawa al software
Aunque el diagrama de Ishikawa proviene de entornos industriales, puede adaptarse al análisis de defectos de software. La lógica se mantiene, pero cambian las categorías.
En software, en lugar de hablar de mano de obra, maquinaria o materia prima, pueden utilizarse categorías como:
- personas;
- procesos;
- herramientas;
- entornos;
- datos;
- código;
- diseño.
Por ejemplo, ante un defecto en una aplicación, el equipo puede preguntarse si el problema proviene de la forma en que está definido el proceso, de las herramientas usadas, del entorno donde se ejecuta el sistema, de la calidad del código, de los datos de prueba, de decisiones de diseño o de la capacitación de las personas involucradas.
El propósito no es llenar un diagrama de manera mecánica, sino ordenar hipótesis y visualizar que un defecto puede tener múltiples causas concurrentes. Un problema rara vez se explica por un único factor. El Ishikawa ayuda a considerar varias aristas antes de concluir cuál es la causa raíz o cuáles son las causas más probables.
---
# El plan de mejora: convertir el análisis en acción
Después de identificar defectos y analizar sus causas, el siguiente paso es construir un **plan de mejora**. Este plan no debe ser una lista de buenas intenciones, sino una estructura de acciones concretas, priorizadas, asignadas y medibles.
El plan de mejora debe responder preguntas fundamentales:
- ¿Qué se va a corregir o prevenir?
- ¿Quién será responsable?
- ¿Cuándo se realizará?
- ¿Qué esfuerzo implica?
- ¿Qué indicador permitirá verificar si la acción funcionó?
- ¿Cómo se evitará que el defecto vuelva a presentarse?
Como mínimo, el plan debe incluir:
| Elemento | Descripción |
| --- | --- |
| Acción | Qué se va a corregir, prevenir o ejecutar. |
| Responsable | Persona, rol o área encargada. |
| Momento o plazo | Cuándo se realizará la acción. |
| Esfuerzo | Estimación del esfuerzo requerido: bajo, medio o alto. |
| KPI esperado | Indicador que permitirá verificar la efectividad. |
| Por ejemplo, si se identifica que el problema está asociado a falta de pruebas de carga, una acción de mejora podría ser ejecutar una prueba de carga en el piloto. El responsable podría ser el líder de QA. El esfuerzo podría clasificarse como medio, porque implica configurar escenarios, preparar herramientas y ejecutar mediciones. El KPI esperado podría ser que la latencia alcance un **percentil 95 menor a 300 milisegundos**. |  |
Este ejemplo muestra cómo los elementos se conectan: se parte de un defecto, se analiza su causa, se define una acción, se asigna un responsable, se estima el esfuerzo y se establece un indicador medible.
---
# Priorización de acciones por impacto y esfuerzo
Además de clasificar defectos, también es necesario priorizar las acciones de mejora. Para ello, el docente menciona la matriz de **impacto y esfuerzo**, que permite ordenar las acciones según el valor que generan y los recursos que requieren.
La lógica general es la siguiente:
|  | Esfuerzo bajo | Esfuerzo alto |
| --- | --- | --- |
| Impacto alto | Acciones prioritarias: alto valor con poco esfuerzo. | Acciones importantes, pero requieren planificación. |
| Impacto bajo | Acciones de mejora rápida, si hay disponibilidad. | Acciones de baja prioridad. |
| Una acción de alto impacto y bajo esfuerzo resulta especialmente atractiva, porque permite obtener beneficios importantes sin requerir demasiados recursos. En cambio, una acción de bajo impacto y alto esfuerzo probablemente no debería ser prioritaria. |  |  |
Esta herramienta ayuda a decidir qué mejoras abordar primero cuando existen varias alternativas derivadas del análisis causal. No todas las acciones deben ejecutarse al mismo tiempo ni con la misma urgencia.
---
# KPIs para medir la mejora
Los **KPIs** son indicadores que permiten medir el avance, el cumplimiento o la efectividad de una acción de mejora. En un proceso de calidad, no basta con decir que se corregirá un problema; es necesario definir cómo se comprobará que la corrección fue efectiva.
El docente señala que muchos indicadores utilizados en pruebas pueden convertirse en KPIs del plan de mejora. Algunos ejemplos son:
| KPI | Ejemplo de umbral |
| --- | --- |
| Error rate | Menor al 1 % de solicitudes fallidas. |
| Latencia | Percentil 95 menor a 300 ms. |
| Cobertura de smoke testing | Todos los flujos críticos protegidos. |
| Automatización | Más del 80 % de pantallas o flujos automatizados. |
| Cobertura de nuevo código | Al menos 80 % de nuevas líneas cubiertas por pruebas unitarias. |
| Issues críticos o bloqueantes | Cero issues críticos o bloqueantes. |
| Duplicidad de código nuevo | Menor al 3 %. |
| El **error rate** mide el porcentaje de solicitudes fallidas. Por ejemplo, un umbral menor al 1 % significa que las fallas deben mantenerse por debajo de ese porcentaje respecto al total de transacciones. |  |
La **latencia** puede medirse mediante percentiles. El ejemplo más claro dado por el docente fue un percentil 95 menor a 300 milisegundos. Esto significa que el 95 % de las solicitudes debería responder por debajo de ese tiempo.
La **cobertura de smoke testing** busca asegurar que los flujos críticos estén protegidos por pruebas rápidas y esenciales. La **automatización** puede medirse, por ejemplo, como porcentaje de pantallas o flujos automatizados. La cobertura de nuevo código, los issues críticos y la duplicidad son métricas útiles para controlar la calidad técnica del desarrollo.
**Nota:** En la transcripción aparece una referencia a “percentivo 25”, pero el ejemplo más claro y coherente con pruebas de rendimiento fue **percentil 95 menor a 300 milisegundos**. También aparece repetidamente “campage”, probablemente como error de transcripción asociado a **KPIs** o indicadores.
---
# Quality Gates: puntos de control para prevenir defectos
Los **Quality Gates** son puntos de control dentro del proceso de desarrollo, pruebas o despliegue. Funcionan como criterios que deben cumplirse antes de avanzar a la siguiente etapa. Si los criterios se cumplen, el proceso continúa. Si no se cumplen, el flujo se detiene.
Un Quality Gate puede aplicarse antes de liberar una versión, antes de cerrar un sprint, antes de pasar de pruebas a producción o después de ejecutar pruebas de rendimiento. Su valor está en prevenir que errores conocidos o riesgos importantes avancen hacia fases posteriores.
Algunos ejemplos de criterios de Quality Gate son:
- no permitir despliegues si existen defectos críticos abiertos;
- exigir que el error rate esté por debajo de un umbral definido;
- exigir que la latencia esté dentro de límites aceptables;
- verificar que los flujos críticos estén aprobados;
- exigir cobertura mínima de pruebas;
- impedir el avance si hay issues críticos o bloqueantes;
- controlar que la duplicidad de código nuevo esté por debajo del 3 %;
- exigir que el nuevo código tenga al menos 80 % de cobertura con pruebas unitarias.
Los Quality Gates transforman criterios de calidad en reglas concretas de decisión. No son simples formalidades; son mecanismos de prevención y control. Su objetivo es asegurar que el producto o proceso cumple condiciones mínimas antes de avanzar.
En la actividad, se espera que los estudiantes investiguen y definan reglas asociadas a estos puntos de control, establezcan umbrales claros y justifiquen su pertinencia. No basta con decir que habrá un Quality Gate; debe indicarse qué mide, cuál es el umbral, por qué se eligió y qué ocurre si no se cumple.
---
# Automatización, pipelines y despliegue
La actividad también contempla una propuesta técnica relacionada con **automatización**, especialmente en relación con despliegues y controles de calidad. En un flujo moderno de desarrollo, las pruebas, los Quality Gates y el despliegue pueden integrarse dentro de un **pipeline**.
La lógica general es la siguiente:
```text
Desarrollo
   ↓
Pruebas automatizadas
   ↓
Quality Gates
   ↓
¿Cumple los criterios?
   ├── Sí → Despliegue
   └── No → Se detiene el despliegue
```
En este flujo, las pruebas automatizadas generan resultados medibles. Luego, los Quality Gates verifican si se cumplen los umbrales definidos: error rate, latencia, cobertura, seguridad, ausencia de defectos bloqueantes, duplicidad de código, flujos críticos aprobados, entre otros. Si el sistema cumple los criterios, puede avanzar hacia el despliegue. Si no cumple, el despliegue se bloquea.
El docente aclara que para el trabajo no se exige necesariamente una automatización completa. Lo esperado es que los estudiantes validen propuestas, definan umbrales y justifiquen cómo podría automatizarse un piloto. Si algún grupo logra implementar un piloto funcionando, esto sería un valor agregado. Podría evidenciarse mediante capturas de pantalla o ejecución del pipeline, incluso si se automatiza sobre un solo defecto.
La propuesta técnica debe justificar las herramientas seleccionadas para automatización. No se trata solo de nombrar herramientas, sino de explicar por qué son pertinentes para el proceso de calidad, qué necesidad cubren y cómo contribuyen a controlar el despliegue o prevenir defectos.
---
# Producto esperado del laboratorio
El docente recomienda presentar el laboratorio en un único informe organizado, con una línea argumental clara. Aunque también podrían entregarse carpetas separadas para entradas, análisis y plan de mejora, esta modalidad puede dificultar la lectura si no existen conectores entre los documentos. Por eso, resulta preferible construir un solo documento que integre todos los elementos y utilice anexos cuando sea necesario.
Una estructura sugerida es:
```text
1. Introducción
2. Objetivo del trabajo
3. Entradas: defectos y evidencias
4. Acta de triage
5. Análisis de causa raíz
6. Plan de mejora
7. Quality Gates propuestos
8. Propuesta técnica de automatización
9. Anexos
```
El objetivo del trabajo puede formularse indicando que se busca elaborar un acta de triage, analizar las causas de los defectos identificados y generar un plan de mejora con una propuesta técnica.
El informe debe mostrar continuidad: se identifican defectos, se documentan evidencias, se realiza el triage, se analizan causas, se definen acciones de mejora, se establecen KPIs y se proponen Quality Gates. Esa línea clara es preferible a documentos aislados sin conexión explícita.
---
# Ejemplo de tabla para registrar defectos
Una forma útil de organizar los defectos es mediante una tabla que permita comparar información básica antes del triage:
| Código | Descripción del defecto | Impacto principal | Evidencia inicial | Reproducibilidad | Alcance | Severidad propuesta | Prioridad |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D-001 | Pago aprobado sin resultado visible | Afecta operación crítica y confianza del usuario | Captura de pantalla, log de transacción | Ocurre bajo ciertas condiciones | Usuarios que realizan pagos | Alta | Alta |
| D-002 | Descuento calculado incorrectamente | Error de negocio y cobro equivocado | Datos de prueba vs. resultado esperado | Reproducible con ciertos productos | Clientes con descuentos activos | Alta | Alta |
| D-003 | Login intermitente en horas pico | Indisponibilidad parcial del sistema | HTTP 500, timeout, métricas de carga | Ocurre en horas pico | Usuarios concurrentes | Alta | Alta |
| D-004 | Botón de enviar fuera de pantalla | Problema funcional en móvil | Captura en dispositivo móvil | Solo en Android | Usuarios Android | Media | Alta |
| D-005 | PDF tarda más de 35 segundos en descargar | Degradación del servicio | Video, métrica de tiempo de descarga | Reproducible con archivos grandes | Usuarios que descargan PDF | Media | Media |
| Esta tabla no reemplaza el análisis escrito, pero facilita la trazabilidad y la comparación entre defectos. |  |  |  |  |  |  |  |
---
# Ejemplo de acta de triage
El acta de triage debe recoger los acuerdos derivados de la revisión de defectos. Un formato posible es:
| Código del defecto | Severidad acordada | Prioridad acordada | Responsable | Decisión | Fecha o plazo | Observaciones |
| --- | --- | --- | --- | --- | --- | --- |
| D-001 | Alta | Alta | Equipo de desarrollo | Hotfix | Por definir | Validar flujo completo de pagos. |
| D-002 | Alta | Alta | Equipo funcional y desarrollo | Corrección en próximo release | Por definir | Revisar reglas de negocio. |
| D-003 | Alta | Alta | Desarrollo / infraestructura | Análisis inmediato | Por definir | Revisar métricas de carga. |
| D-004 | Media | Alta | Frontend | Corrección UI móvil | Por definir | Afecta Android. |
| D-005 | Media | Media | Backend | Optimización planificada | Por definir | Revisar generación de PDF. |
| Este formato permite evidenciar que el triage se realizó y que los defectos no quedaron sin gestión. |  |  |  |  |  |  |
---
# Auditoría cruzada en la actividad 6
Más adelante, en la actividad 6, se trabajará el concepto de **auditoría cruzada**. Esta actividad consiste en tomar auditorías realizadas por otros frentes o equipos y validarlas desde una mirada externa.
La auditoría cruzada permite contrastar criterios, detectar inconsistencias y fortalecer la objetividad del proceso. Al revisar el trabajo de otros, los equipos pueden identificar aspectos que quizá el grupo original no observó. Al mismo tiempo, quienes reciben la revisión obtienen retroalimentación útil para mejorar sus propios procesos.
En términos generales, la auditoría cruzada contribuye a la mejora continua porque promueve una revisión colaborativa y comparativa. No se limita a comprobar si algo está bien o mal, sino que ayuda a fortalecer los criterios de calidad entre diferentes participantes.
---
# Fechas, material de clase y observaciones administrativas
El docente menciona que la actividad está programada para el **1 de noviembre**. También revisa fechas dentro de la plataforma y menciona una actividad que aparece con un rango del **26 al 8**, aunque señala que podría existir un error de configuración, porque primero debería cerrarse una actividad y después abrirse la siguiente.
Después de estas actividades, los estudiantes presentarían una evaluación tipo quiz, disponible para ser presentada en cualquier momento dentro del periodo correspondiente. Con ello se cerraría esta parte del curso.
**Nota:** La transcripción no permite establecer con certeza a qué meses corresponden las fechas “26 al 8”. Además, el docente indica que la configuración parece estar mal, por lo que conviene verificar directamente en la plataforma académica las fechas definitivas.
Hacia el final de la sesión, el docente se enfoca en compartir las diapositivas utilizadas durante la clase. Indica que las dejará disponibles en el chat del grupo o en la sección correspondiente del entorno virtual, para que los estudiantes puedan consultarlas como guía. Se presentan algunas dificultades técnicas para acceder al contenido desde la plataforma o desde la aplicación web. Se revisan opciones como los tres puntos de la interfaz, la sección de contenido, avisos y foro. Finalmente, el docente decide publicar el material en el foro o en avisos para facilitar el acceso.
Se menciona que el material corresponde a la **clase del 15 de octubre** y a la **actividad 5**. También aparece una inconsistencia entre “encuentro 6” y “encuentro 5”, aunque luego parece corregirse a **encuentro 5**.
**Nota:** Existe una inconsistencia en la transcripción entre “encuentro 6” y “encuentro 5”. El propio intercambio posterior parece corregirlo a **encuentro 5**, pero se deja señalada la duda por tratarse de una referencia administrativa.
La grabación proporcionada indica como hora de inicio el **29 de octubre de 2026 a las 14:45:23**, hora local.
---
# Síntesis final para estudio
La Unidad 3 se centra en la gestión de defectos y la mejora continua. El estudiante debe comprender que un proceso de calidad no termina cuando se encuentra un error. El valor real aparece cuando el defecto se documenta, se clasifica, se analiza, se corrige, se valida y se convierte en aprendizaje para prevenir recurrencias.
## Conceptos clave
| Concepto | Idea principal |
| --- | --- |
| **Triage** | Sesión de análisis y decisión sobre defectos encontrados. |
| **Acta de triage** | Documento que registra defectos, evidencia, severidad, prioridad, responsables, fechas, decisiones y criterios de cierre. |
| **Severidad** | Gravedad técnica, funcional o de negocio del defecto. |
| **Prioridad** | Urgencia con la que debe corregirse el defecto. |
| **Impacto** | Consecuencias del defecto sobre usuarios, negocio, operación o sistema. |
| **Urgencia** | Qué tan pronto debe atenderse el defecto. |
| **Workaround** | Alternativa temporal para operar mientras se corrige la causa raíz. |
| **Evidencia** | Datos verificables que sustentan el defecto y su clasificación. |
| **Causa raíz** | Origen profundo del problema, más allá del síntoma visible. |
| **Cinco porqués** | Técnica que profundiza mediante preguntas sucesivas de “¿por qué?”. |
| **Ishikawa / espina de pescado** | Herramienta visual para organizar posibles causas por categorías. |
| **Plan de mejora** | Conjunto de acciones priorizadas con responsables, esfuerzo, KPI y fechas. |
| **KPI** | Indicador que mide avance, cumplimiento o efectividad. |
| **Quality Gate** | Punto de control que permite o bloquea el avance según criterios de calidad. |
| **Pipeline** | Flujo automatizado que integra desarrollo, pruebas, Quality Gates y despliegue. |
| **Auditoría cruzada** | Validación de auditorías entre diferentes frentes o equipos. |
## Flujo general del trabajo
```text
Defectos identificados
        ↓
Evidencia mínima y codificación
        ↓
Sesión de triage
        ↓
Clasificación de severidad, prioridad, impacto y urgencia
        ↓
Asignación de responsables, fechas y decisiones
        ↓
Análisis de causa raíz
(cinco porqués / Ishikawa)
        ↓
Plan de mejora
(acciones, responsables, esfuerzo, KPIs)
        ↓
Definición de Quality Gates
(umbrales y criterios)
        ↓
Propuesta o piloto de automatización
        ↓
Validación, cierre y mejora continua
```
## Idea central de la unidad
La calidad de software no consiste únicamente en ejecutar pruebas o encontrar errores. Un proceso maduro de calidad exige **gestionar los hallazgos con evidencia**, distinguir severidad y prioridad, analizar causas raíz, definir acciones de mejora, medir resultados mediante KPIs y establecer Quality Gates que impidan que defectos conocidos avancen hacia etapas posteriores o producción. Esta es la base de una mejora continua real, trazable y sostenible.