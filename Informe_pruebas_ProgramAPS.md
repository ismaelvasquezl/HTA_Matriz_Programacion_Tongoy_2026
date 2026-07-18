# Informe de pruebas — ProgramAPS en 5 escenarios de la red chilena

**Objetivo:** verificar si la herramienta sirve para cualquier CESFAM de Chile, no solo para Tongoy.
**Método:** ejecución real del motor contra cinco perfiles de establecimiento, más pruebas de regresión.
**Resultado:** se encontraron **cuatro defectos, uno de ellos grave**. Los cuatro están corregidos y verificados.

---

## Los cinco casos

Se construyeron escalando la estructura demográfica base con factores de forma distintos, para cubrir el rango real de la red:

| # | Perfil | Inscritos | Rasgo |
|---|---|---|---|
| 1 | Tongoy (datos reales) | 11.273 | Rural costero, referencia |
| 2 | Urbano grande sectorizado | 36.072 | 4 sectores, dotación ×3 |
| 3 | Posta rural pequeña | 3.046 | Dotación mínima |
| 4 | CESFAM envejecido | 18.017 | 35,9 % de 65+ |
| 5 | CESFAM joven | 25.511 | 28,9 % de menores de 15 |

---

## Hallazgo 1 — GRAVE · La cartera estaba incompleta (corregido)

**Este es un error mío, y es el más importante del informe.**

La extracción de datos del Excel recorría las filas 6 a 300. Pero `3-PROGRA_ACTIVIDADES` llega hasta la fila 341. **Se perdieron 56 de 236 prestaciones**, entre ellas **el ciclo vital Adulto Mayor completo** (38 prestaciones) y 18 del ciclo "Todos":

- EMPAM y control de seguimiento EMPAM
- Control cardiovascular RCV alto — **2.149 atenciones al año**
- Control cardiovascular RCV moderado-bajo — 1.377 al año
- Consulta de morbilidad del adulto mayor — 1.428 al año
- Evaluación de pie diabético (4 niveles de riesgo), podología, visita domiciliaria PADDS

**Impacto:** la versión anterior omitía **121,3 h/sem, el 25,2 % de la demanda real** del establecimiento.

### Y algo peor: la validación anterior era falsa

El informe previo afirmaba que el motor reproducía el Excel exactamente, con 359,54 h/sem en ambos lados. Era cierto y era inútil: **el script de verificación leía el mismo rango truncado que la extracción**. Ambos lados ignoraban las mismas 56 filas, así que coincidían perfectamente mientras compartían el mismo error.

> **Lección que vale para toda la herramienta:** una validación solo prueba algo si el verificador no comparte los supuestos del verificado. Coincidir no es lo mismo que estar bien.

### La validación corregida

Releyendo el Excel hasta el final real de la hoja:

| | Excel | ProgramAPS |
|---|---|---|
| Demanda clínica total | 480,84 h/sem | **480,84 h/sem** |
| Estamentos coincidentes | — | **14 de 14** |
| Filas «Total a trabajar» | — | **236 de 236** |

**Confirmación independiente:** el motor arroja **49,54 h/sem** para enfermería, que es exactamente el `2 days 1:32:30` que muestra la hoja `Resumen_clinico` del propio Excel. La versión anterior daba 34,8 y no podía explicar la diferencia. Ese resumen es un testigo que no participó del error: si coincide, la cifra es correcta.

---

## Hallazgo 2 — CRÍTICO · La cartera no se adaptaba a otro establecimiento (corregido)

**137 de 236 prestaciones usan valores observados**: cifras absolutas del consolidado REM de Tongoy ("3.879 consultas de morbilidad al año"). A diferencia del per cápita, **no se ajustan solas** al cambiar la población.

La prueba lo dejó en evidencia. La demanda proveniente de observados era **idéntica (245,5 h/sem) en los cinco casos**, con poblaciones de 3.046 a 36.072:

| Caso | Inscritos | h/sem por 1.000 |
|---|---|---|
| Posta rural | 3.046 | **90,60** |
| Tongoy | 11.273 | **31,74** |
| Urbano grande | 36.072 | **16,76** |

Un mismo modelo no puede exigir 90 horas por mil personas en un lugar y 17 en otro con idéntica pirámide. Al triplicar la población, la demanda crecía solo ×1,63 en vez de ×3: **una subestimación del 45,8 %, y sin ninguna advertencia en pantalla.**

Un CESFAM de Maipú habría cargado su población, obtenido un balance tranquilizador y programado con la mitad de las horas que necesita.

### Corrección aplicada

1. **Panel «Adaptar la cartera»** en el módulo 02, con dos métodos:
   - *Por estructura de población* (recomendado): ajusta cada prestación según **su propio grupo etario**. El control cardiovascular escala según cómo creció el grupo de 55–64, no según el total del centro.
   - *Proporcional simple*: un mismo factor para todas.
2. **Alerta crítica automática** cuando la población difiere más de 10 % de aquella con que se midieron los observados. Es imposible programar mal en silencio.
3. **Nuevo indicador: horas por 1.000 inscritos**, visible en el panel, en resultados y en el informe.

### Verificación

| Caso | Antes | Después |
|---|---|---|
| Posta rural (3.046) | 90,60 | **44,5** |
| Tongoy (11.273) | 31,74 | **44,3** |
| Urbano grande (36.072) | 16,76 | **44,3** |

Tres tamaños distintos con la misma pirámide convergen en el mismo valor. **El modelo es portable.**

Y donde la pirámide cambia, el resultado cambia como debe: **CESFAM envejecido 50,3** h/mil frente a **CESFAM joven 42,6**. Un centro con más adultos mayores necesita más horas por persona inscrita. Eso es medicina, y ahora el modelo lo refleja.

---

## Hallazgo 3 — La consolidación por sectores no era exacta (documentado)

Programar 4 sectores por separado y sumarlos daba **+0,9 %** frente a programar el establecimiento completo.

**No es un error.** Cada prestación redondea hacia arriba (no existen medias atenciones), y cuatro sectores generan cuatro redondeos donde antes había uno. Es propiedad del modelo original, que se conservó deliberadamente.

**Corrección:** se documentó en pantalla, en el módulo 03, con la regla práctica: para cifras oficiales, usar la vista consolidada; la vista por sector sirve para distribuir el trabajo.

---

## Hallazgo 4 — Rigideces que impedían el uso nacional (corregidas)

| Problema | Corrección |
|---|---|
| La colación se descontaba solo a jornadas de exactamente 44 y 33 h. Un centro con jornadas de 40 h no la descontaba y sobrestimaba su oferta | Umbral parametrizable (módulo 01). Verificado: jornada 40 h → 35 h líquidas |
| La utilización global mostraba `∞` sin dotación cargada | Muestra "—" y la etiqueta explica por qué |

---

## Mejora adicional — El gráfico de equidad etaria

Las pruebas dejaron a la vista una pregunta que ninguna planilla de horas responde: **¿a quién le estamos programando?**

Se agregó al módulo 07 un gráfico que contrasta el peso de cada tramo etario en la población con su peso en las horas programadas, más una **alerta automática de vacío de cartera** cuando un grupo con más del 12 % de la población recibe menos de un tercio de las horas que le corresponderían.

Con la cartera completa, Tongoy queda razonable (65–79 años: 12,3 % de la población, 20,7 % de las horas — coherente, los mayores consultan más). Pero la alerta seguirá siendo útil para cualquier centro que herede esta cartera sin revisarla.

**Detalle técnico:** las horas de cada prestación se reparten entre las edades de su tramo **ponderadas por la población de cada edad**, no en partes iguales. Una prestación de 65 a 100 años recae sobre todo en los 65–79, que es donde está la gente. Repartir por año calendario inflaba artificialmente al grupo 80+ (mostraba 15 % de las horas para el 3,7 % de la población, un artefacto que se corrigió).

---

## Pruebas de regresión — todas pasan

| # | Verificación | Resultado |
|---|---|---|
| 1 | Reproduce el Excel original | 480,84 = 480,84 ✓ |
| 2 | La vista por estamento cuadra con el balance global | 0 descuadres en 14 estamentos ✓ |
| 3 | La oferta por sectores consolida exacto | 2.039,94 = 2.039,94 ✓ |
| 4 | Sin dotación cargada no rompe | Sin división por cero ✓ |
| 5 | Colación con jornada de 40 h y umbral 33 | 35 h líquidas ✓ |

---

## Qué significa esto para el uso nacional

**Lo que la herramienta ya resuelve.** Cualquier CESFAM puede cargar su per cápita, su dotación y sus box, adaptar la cartera heredada por estructura demográfica y obtener un balance verificado contra un modelo que reproduce fielmente la lógica de programación comunal. El indicador de horas por 1.000 inscritos permite, por primera vez, **comparar establecimientos de distinto tamaño** y detectar carteras mal adaptadas de un vistazo.

**Lo que sigue exigiendo criterio profesional.** La adaptación automática es una aproximación transitoria: **lo correcto es cargar el REM del propio establecimiento**, prestación por prestación. La app lo dice en pantalla y lo declara en el informe. Ninguna herramienta puede inventar la cartera que falta ni el dato que no se midió.

**La advertencia que hay que repetir.** Los defectos encontrados no aparecieron leyendo el código: aparecieron **ejecutándolo con datos distintos a los de origen**. Antes de que un segundo establecimiento la use en decisiones reales, conviene repetir este ejercicio con sus datos reales. Es barato, y encuentra cosas.

---

## Estado tras las correcciones

- **236 prestaciones** (antes 180), los 5 ciclos vitales, cobertura etaria completa de 0 a 100 años.
- **480,84 h/sem** de demanda validada contra el Excel, con confirmación independiente de su propia hoja de resumen.
- Portabilidad verificada en un rango de **3.046 a 36.072 inscritos** y en pirámides opuestas.
- 5 de 5 regresiones en verde.
