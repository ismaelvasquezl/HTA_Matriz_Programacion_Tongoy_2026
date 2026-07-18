# ProgramAPS — Manual técnico y guion de capacitación

**Documento de referencia para el responsable técnico.**
Para explicar, defender y auditar la herramienta ante equipos, dirección y DESAM.

---

## 0. Qué es esto, en una frase que puedas usar

> «Es la misma lógica de programación que ya usamos, con las mismas fórmulas y los mismos resultados, pero auditable: cada número muestra de dónde viene, cualquiera puede modificar los supuestos sin romper nada, y agrega lo que la planilla no tenía — box, ausentismo, sectorización y escenarios.»

La frase clave cuando alguien desconfíe: **no es un modelo nuevo**. Es el modelo de programación comunal existente, verificado línea por línea, con la opacidad removida.

---

## 1. El argumento más fuerte que tienes: la validación

Antes de discutir cualquier funcionalidad, este es el dato que ordena la conversación:

> El motor reproduce el balance del Excel original **celda a celda**: **480,84 h/semana** de demanda clínica en el Excel, **480,84 h/semana** en ProgramAPS. **14 de 14 estamentos** coinciden con diferencia cero. Las **236 filas** de «Total a trabajar» coinciden una a una.

**Confirmación independiente que conviene tener a mano:** el motor arroja 49,54 h/sem para enfermería, exactamente el `2 days 1:32:30` que muestra la hoja `Resumen_clinico` del propio Excel. Ese resumen es un testigo que no participó del cálculo: si coincide, la cifra es correcta.

**Por qué importa:** cualquier objeción del tipo *"¿y cómo sé que este programa calcula bien?"* se responde con evidencia reproducible: se corrió el ejercicio 2023 con la misma población (10.830), el mismo calendario (248 hábiles → 44 semanas) y los mismos parámetros, y el resultado es idéntico.

**Cómo lo demuestras en vivo:** módulo 02, cambia la población al corte anterior; módulo 01, pon 248 días hábiles. El total de demanda vuelve a 480,8 h/sem. Es el mismo modelo.

> **Honestidad metodológica que debes conocer.** Una primera versión de esta validación daba 359,54 en ambos lados y era falsa: el verificador leía el mismo rango truncado de filas que la extracción, y ambos omitían las mismas 56 prestaciones. Coincidían por compartir el error. Se detectó al ejecutar la herramienta contra establecimientos de otro tamaño. **Una validación solo prueba algo si el verificador no comparte los supuestos del verificado.** Si alguien te pregunta cómo sabes que ahora está bien, esta es la respuesta: porque la cifra coincide además con una hoja del Excel que no intervino en el cálculo.

### Un hallazgo de la auditoría que conviene contar

Durante la validación apareció una regla que **no está documentada en ninguna parte** de la planilla y que solo se ve leyendo la fórmula `M6`:

```
IF(N="Grupal", IF(J="Percapita", (H*K*L)/O , (I*K*L) ), IF(J="Percapita", H*K*L, I*K*L))
```

En actividades **grupales**, el Excel divide por asistentes/sesión **solo si la población viene del per cápita**. Si viene de un valor observado, **no divide**.

La razón es correcta y es fina: el per cápita entrega **personas**, que hay que convertir a sesiones; el valor observado del consolidado REM ya viene expresado en **sesiones realizadas**. Dividirlo sería contarlo dos veces.

**Qué significa esto para tu argumento:** es exactamente el tipo de conocimiento que vivía solo en la cabeza de quien construyó la planilla. Un funcionario nuevo que la heredara jamás lo habría deducido. En ProgramAPS está escrito como regla R6, documentado en el código y verificado. **Ese es el problema que esta herramienta resuelve: la dependencia del conocimiento tácito.**

---

## 2. Las ocho reglas del modelo (memorízalas: son todo el sistema)

| # | Regla | Origen |
|---|---|---|
| **R1** | Días a programar = hábiles − vacaciones − PAC − permisos | hoja `0-DAYPRO` (oculta) |
| **R2** | Semanas = ⌈días ÷ 5⌉ | `0-DAYPRO`, `ROUNDUP` |
| **R3** | Jornada líquida = jornada − colación (solo 44 y 33 h) | `1-RRHH`, col. F |
| **R4** | Oferta asistencial = líquida − admin − indirectas | `1-RRHH`, col. I |
| **R5** | Población objetivo = Σ per cápita (tramo etario × sexo), o valor observado | `2-CREA`, `SUMIFS` |
| **R6** | Total a trabajar = ⌈pob × cobertura × concentración⌉ ÷ asistentes *(solo grupal + per cápita)* | `3-PROGRA`, col. M |
| **R9** | Los valores observados son cifras absolutas del REM local: no escalan solos con la población | hallazgo de las pruebas |
| **R7** | Por estamento: actividades = ⌈total × %⌉; horas/sem = act × min ÷ 60 ÷ semanas | `3-PROGRA`, cols. T–W |
| **R8** | Balance = oferta − demanda; jornadas equivalentes = horas ÷ 39 | `5-BALANCE` |

Todo lo demás es interfaz. Si dominas estas ocho reglas, dominas la herramienta completa.

**Detalle técnico que te van a preguntar:** los tres redondeos hacia arriba (`⌈⌉` en R2, R6 y R7) son deliberados y se conservaron. Programar en salud redondea al alza: no existe media atención. Esto genera una diferencia mínima frente a un cálculo lineal, y es correcto que exista.

---

## 3. Encuadre técnico: por qué el modelo es defendible

La lógica **demanda → horas → brecha** es la estructura estándar de la programación en red del MINSAL. Conviene amarrarla a los instrumentos que tu auditorio reconoce:

| Elemento del modelo | Instrumento que lo respalda |
|---|---|
| Población validada por edad y sexo | Per cápita FONASA (corte anual de inscritos validados) |
| Cobertura y concentración por prestación | Orientaciones para la Planificación y Programación en Red, MINSAL |
| Rendimientos (min/atención) por tipo de atención | Orientaciones vigentes + estandarización local de agenda |
| Valores observados (población bajo control) | Consolidado REM (DEIS) del año anterior |
| Jornada de 44 h y su composición | Ley 19.378, Estatuto de Atención Primaria Municipal |
| Prestaciones trazadoras y metas | IAAPS y Metas Sanitarias (Ley 19.813) |
| Enfoque por ciclo vital y sector | Modelo de Atención Integral de Salud Familiar y Comunitaria (MAIS) |

> **Advertencia que debes hacer siempre:** las coberturas, concentraciones y rendimientos precargados vienen del ejercicio 2023 de Tongoy. **No son norma vigente.** Antes de usar la herramienta para el año en curso, contrástalos con las Orientaciones del año que se programa. La app no valida eso por ti: es una decisión técnica que sigue siendo tuya.

---

## 4. Lo que la herramienta agrega al Excel (y cómo justificar cada cosa)

### 4.1 Lo que se conservó porque estaba bien

La cadena de cálculo completa, la estructura demanda–oferta–brecha, el catálogo de prestaciones, la matriz de rendimientos por tipo de atención × estamento, y el reparto multi-estamento de una misma prestación. **Nada de esto se tocó.** Es el activo técnico del modelo original y hay que decirlo con todas sus letras: es un buen modelo.

### 4.2 Lo que se rediseñó, con su razón

| Problema del Excel | Consecuencia real | Solución |
|---|---|---|
| Hojas ocultas (`0-DAYPRO`, `Índices`) | Parámetros críticos invisibles para quien usa | Módulo 01, todo a la vista y editable |
| `VLOOKUP` con **RUN como clave** | Un error de dígito rompe el cálculo en silencio | Identificadores internos; el RUN no cumple ninguna función de cálculo |
| Tiempos como fracción de día | Celdas que muestran `-1 day, 23:25:54` | Horas decimales en toda la app |
| Tope de 10 estamentos por prestación | Límite estructural arbitrario | Sin límite |
| ~150 nombres definidos | Ilegible y frágil de mantener | Modelo de datos explícito |
| Datos personales embebidos | 78 RUN y nombres circulando en un archivo | **Anonimizado**: estamento, jornada y horas. Sin RUN, sin nombres |

**La anonimización es una decisión que debes poder defender.** El archivo original contenía RUN y nombres completos de 78 funcionarios. Para programar no se necesita saber *quién* es: se necesita saber *qué estamento, qué jornada, qué horas*. La app conserva el detalle persona a persona (para que la suma sea exacta) con glosas editables. Cada centro pone las etiquetas que quiera.

### 4.3 Lo que no existía y hubo que crear

Estos cuatro módulos **no tienen respaldo en el archivo fuente**. Son propuestas fundamentadas, y en la propia app aparecen marcados como hipótesis a validar. Preséntalos así, nunca como dato:

1. **Box clínicos.** El Excel no registra infraestructura: programa horas profesionales como si el espacio fuera infinito. Se asigna a cada prestación un tipo de box mediante una heurística por tipo de atención y se contrasta contra la capacidad. **Los valores precargados son un supuesto y hay que reemplazarlos.**

2. **Ausentismo (8 % por defecto).** El Excel asume que toda hora contratada se trabaja. Ninguna programación honesta puede asumir eso. Es un parámetro global editable, y también persona a persona.

3. **Sectorización.** Tongoy no sectoriza, y por eso el modelo no lo contemplaba. Como capa opcional: la demanda se fracciona por población y la oferta por adscripción del RRHH; el personal transversal se prorratea. Esto es lo que permite que la herramienta sirva a un CESFAM urbano grande.

4. **Escenarios.** El Excel permitía un solo ejercicio a la vez. La comparación de alternativas es, en la práctica, el único insumo real para una conversación sobre dotación.

---

## 4.4 Portabilidad: lo que hace que sirva fuera de Tongoy

**El punto que más importa si esto va a usarse en otros centros.**

137 de las 236 prestaciones usan **valores observados**: cifras absolutas del consolidado REM ("3.879 consultas de morbilidad al año"). A diferencia del per cápita, **no se ajustan solas** al cambiar la población. Un CESFAM que cargue su per cápita y no adapte la cartera arrastra las cifras de Tongoy: en las pruebas, al triplicar la población la demanda crecía solo ×1,63 — **una subestimación del 45,8 %**.

Por eso el módulo 02 tiene el panel **Adaptar la cartera**, con dos métodos:

- **Por estructura de población** (recomendado): ajusta cada prestación según **su propio grupo etario**. El control cardiovascular escala según cómo creció el grupo de 55–64 años, no según el total del centro.
- **Proporcional simple**: un mismo factor de tamaño para todas. Más rápido, ciego a la pirámide.

Y una **alerta crítica automática** si la población difiere más de 10 % de aquella con que se midieron los observados.

**El indicador que debes enseñar a leer: horas por 1.000 inscritos.** Permite comparar centros de distinto tamaño. Tras adaptar, tres establecimientos de 3.046, 11.273 y 36.072 inscritos con la misma pirámide convergen en 44,5 / 44,3 / 44,3. Un valor muy alejado del de un centro comparable delata una cartera sin adaptar.

**Lo que hay que decir siempre:** el reescalamiento es una **aproximación transitoria**. Lo correcto es cargar el REM propio, prestación por prestación. La app lo declara en el informe, y esa declaración debe quedar.

---

## 5. Vista por estamento: el módulo que más te va a servir

Es la vista de la que depende que la programación se valide de verdad, porque responde la pregunta con que cada referente llega: **«¿qué me toca a mí y me alcanzan las horas?»**

Qué entrega, por estamento y con filtro de sector:

- Dotación real y oferta asistencial de cada persona.
- Todas sus prestaciones con % asignado, rendimiento, actividades/año, actividades/semana y horas/semana.
- Distribución de su carga por programa.
- **Curva de concentración de carga** (Pareto): prestaciones ordenadas por horas, con acumulado.
- Exportación CSV de su programación completa.

**Nota de arquitectura que vale la pena defender:** esta vista **no recalcula nada**. Consume el mismo `Engine.compute()` que el balance global. Es imposible que el detalle por estamento contradiga al consolidado, porque son el mismo cálculo leído de dos maneras. En una planilla, en cambio, cada resumen es una fórmula distinta que puede desincronizarse — y suele hacerlo.

**Uso práctico de la curva de concentración:** típicamente 3 o 4 prestaciones concentran la mitad de la carga de un estamento. Ahí es donde una discusión sobre cobertura o rendimiento mueve la aguja. Discutir las de la cola es gastar reunión.

---

## 6. Guion de capacitación (45 minutos)

**Minutos 0–5 · El problema.**
No partas por la app. Parte por la pregunta: *¿cuántas horas de médico necesitamos el próximo año y por qué?* Deja que intenten responder. La incomodidad instala la necesidad.

**Minutos 5–10 · La validación.**
Muestra que reproduce el Excel exactamente. Compra credibilidad antes de pedir confianza. *«No les traigo un invento: les traigo lo mismo que ya usamos, pero que se puede revisar.»*

**Minutos 10–25 · El recorrido 01 → 07.**
Sigue el orden del menú. No expliques botones: cuenta la historia. *La población que tenemos → el equipo que tenemos → lo que nos comprometemos a hacer → si alcanza o no.*

**Minutos 25–35 · El momento que convence.**
Abre una prestación de alta carga. Cambia la cobertura de 1.0 a 0.8. Que vean el balance moverse en vivo. Luego vuelve atrás. **Ese es el instante en que se entiende que programar es decidir, y que las decisiones tienen aritmética.**

**Minutos 35–45 · El módulo 08 y el cierre.**
Que cada referente vea lo suyo. Cierra con el informe generado. Y con la frase que importa: *«Esto no reemplaza el criterio técnico. Lo hace visible, y por eso discutible.»*

---

## 7. Objeciones que van a aparecer, y qué responder

**«Los números no coinciden con lo que yo tenía.»**
Casi siempre es la población: el Excel usaba el corte 2023 (10.830) y la app trae el 2026 (11.273), un 4,1 % más. Más población es más demanda. Iguala el corte y comparen de nuevo.

**«¿Esto sirve para mi CESFAM, que es cinco veces más grande?»**
Sí, pero **no basta con cargar tu población**: hay que adaptar la cartera en el módulo 02, porque 137 prestaciones traen cifras absolutas del REM de Tongoy. La app te avisa con una alerta crítica si no lo hiciste. Sin ese paso, subestimarías cerca de la mitad de tu demanda.

**«¿Y si me equivoco y rompo el archivo?»**
No se puede. No hay fórmulas que romper: los datos y el cálculo están separados. Se cierra sin guardar y listo. Este es, además, el argumento más fuerte frente al Excel, donde un `Supr` mal puesto destruye una fórmula sin avisar.

**«El ausentismo del 8 % es inventado.»**
Correcto, y hay que concederlo de inmediato. Es un supuesto explícito y editable. **La alternativa del Excel era peor: asumir 0 % sin decirlo.** Un supuesto visible se discute; uno oculto se hereda.

**«Los box no son esos.»**
También correcto: son un supuesto, la app lo declara en pantalla. Hay que levantar el dato real. Es, de hecho, la primera tarea pendiente del establecimiento.

**«Esto lo hace un sistema, ya no decidimos nosotros.»**
Al revés. La app no decide nada: calcula consecuencias. Cobertura, concentración y rendimiento los define el equipo. Lo único que hace es impedir que se prometa lo que no cabe en las horas disponibles.

---

## 8. Detalles técnicos, por si te preguntan

- **Arquitectura:** archivo HTML único, sin servidor ni instalación. Cuatro capas separadas: datos, estado, motor de cálculo y presentación. Chart.js (gráficos) y SheetJS (lectura de Excel) desde CDN.
- **Persistencia:** archivo de proyecto `.json`. **Deliberadamente no usa almacenamiento del navegador.** El archivo es la fuente de verdad: se versiona, se adjunta a un oficio y deja trazabilidad. Un dato en la caché del navegador no se puede auditar.
- **Privacidad:** ningún dato sale del computador. No hay backend, ni telemetría, ni envío a servidores.
- **Verificación aplicada:** reproducción del Excel al 100 % (236/236 filas, 14/14 estamentos) con confirmación independiente contra `Resumen_clinico`; coherencia entre balance global y vista por estamento (0 descuadres); consolidación de oferta por sectores exacta; portabilidad verificada entre 3.046 y 36.072 inscritos y en pirámides opuestas; 5 de 5 regresiones en verde. El detalle está en el *Informe de pruebas*.

---

## 9. Pendientes honestos

Lo que hay que decir antes de que lo descubra otro:

1. **Días hábiles 2026 = 250** es un supuesto. Corregir con el calendario oficial.
2. **Dotación de box:** levantar el dato real de Tongoy. Hoy son supuestos.
3. **Coberturas y concentraciones:** son del ejercicio 2023. Contrastar con las Orientaciones vigentes del año a programar.
4. **Ausentismo:** calcularlo con los datos reales de licencias del establecimiento en vez del 8 % genérico.
5. **La heurística de asignación de box** clasifica por palabras del tipo de atención. Es razonable, pero conviene revisar prestación por prestación en el primer uso serio.
6. **Adaptación de la cartera:** el reescalamiento automático es transitorio. La tarea de fondo es cargar el REM local prestación por prestación.
7. **Consolidación por sector:** sumar sectores da ~1 % más que el establecimiento completo, por los redondeos al alza. Para cifras oficiales, usar la vista consolidada.

Ninguno de estos pendientes afecta el núcleo validado del cálculo: son parámetros de entrada, y todos están a la vista y son editables. Que estén declarados es justamente lo que diferencia esta herramienta de la planilla que reemplaza.
