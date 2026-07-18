# Guía de uso — ProgramAPS

**Programar el año de tu CESFAM en 10 pasos.**
No necesitas saber de computación. Solo conocer tu centro.

---

## Antes de empezar (1 minuto)

Abre el archivo `ProgramAPS_Tongoy.html` haciendo doble clic. Se abre en tu navegador, como una página web. No hay que instalar nada.

**Tres cosas que conviene saber desde ya:**

1. **No puedes romperla.** Si algo queda mal, cierras sin guardar y vuelves a abrir. Todo vuelve al inicio.
2. **Los números se recalculan solos.** Cambias un dato y todo el resto se ajusta al instante. No hay que apretar "calcular".
3. **Guarda al terminar.** Botón *Guardar proyecto* (menú izquierdo). Se descarga un archivo; ese archivo es tu trabajo. Para seguir otro día, usa *Cargar proyecto*.

El menú de la izquierda está numerado del **00 al 10**. Ese es el orden. Ve de arriba hacia abajo.

---

## Paso 1 · Parámetros (menú 01)

Dile a la app quién eres y cuántos días vas a trabajar.

- Escribe el **nombre de tu establecimiento** y el **año** a programar.
- Revisa los **días hábiles** del año, y cuántos días se van en vacaciones, capacitación y permisos.

La app te muestra abajo los **días y semanas a programar**. Ese número es la base de todo lo demás: es el tiempo real que tiene tu equipo.

> **Ojo con esto:** el *ausentismo* es el porcentaje de horas que se pierden por licencias e imprevistos. Viene en 8 %. Si en tu centro es distinto, cámbialo. Si lo dejas en 0, la app te dirá que tienes más horas de las que realmente tendrás.

---

## Paso 2 · Población (menú 02)

Aquí va tu gente: cuántas personas tienes inscritas, por edad y sexo.

- Ya viene cargado el per cápita de Tongoy 2026 (11.273 personas).
- **Para usar el tuyo:** botón *Importar desde Excel/CSV* y eliges tu archivo. Solo necesita tener tres columnas: edad, mujeres, hombres.
- También puedes corregir cualquier celda a mano.

Esta tabla es el punto de partida de todo. Si tu población está mal, todo lo demás estará mal.

### Si no eres de Tongoy, este paso es obligatorio

Más abajo verás un recuadro que dice **Adaptar la cartera a este establecimiento**.

Muchas prestaciones traen cifras fijas tomadas del REM de Tongoy (por ejemplo, "3.879 consultas al año"). Esas cifras **no se ajustan solas** cuando cambias la población. Si no las adaptas, tu programación puede quedar a la mitad de lo que necesitas.

- Si el recuadro dice **«al día»** en verde, sigue tranquilo.
- Si dice **«requiere acción»** en rojo, elige *Por estructura de población* y aprieta el botón. Listo.

Lo ideal, con tiempo, es reemplazar esas cifras por las de tu propio REM en el módulo 06. Mientras tanto, adaptar es mucho mejor que no hacerlo.

---

## Paso 3 · Sectores (menú 03)

¿Tu centro trabaja por sectores (Azul, Verde…)?

- **Si no sectorizas:** no toques nada. Sigue de largo.
- **Si sectorizas:** agrega cada sector y pon qué porcentaje de la población le corresponde. Deben sumar 100 % — la app te avisa con un cartel rojo si no cuadra.

---

## Paso 4 · Recurso humano (menú 04)

Tu equipo, persona por persona. Ya vienen cargados los 78 funcionarios, sin nombres.

Para cada uno revisa cuatro cosas:

| Columna | Qué poner |
|---|---|
| **Glosa** | El nombre o etiqueta con que lo reconoces |
| **Jornada** | Sus horas de contrato (44, 33, 22, 11) |
| **Admin** | Horas semanales de tareas administrativas |
| **Indirectas** | Horas de reuniones, registro, coordinación |

La última columna, **Oferta asistencial**, la calcula la app: es lo que realmente le queda para atender público.

> **Si aparece un cartel rojo que dice "sobreasignado":** esa persona tiene más horas de reuniones y papeleo que horas de contrato. No es un error del programa — es un problema real que hay que arreglar en el centro.

---

## Paso 5 · Box (menú 05)

Cuántas salas tienes y cuántas horas a la semana está abierta cada una.

**Importante:** estos números son un supuesto, porque la planilla original no los registraba. Ajústalos a lo que realmente tienes antes de tomar decisiones con esto.

---

## Paso 6 · Cartera (menú 06)

El corazón del asunto: qué prestaciones vas a entregar.

Vienen 236 cargadas, de todos los ciclos vitales. **Haz clic en cualquier fila** y se abre un panel a la derecha donde defines:

- **Cobertura**: a qué parte de la población vas a llegar. Se escribe en decimales: `0.8` significa 80 %.
- **Concentración**: cuántas veces al año atiendes a cada persona.
- **Quién la hace**: el estamento, qué porcentaje le toca y cuántos minutos dura la atención.

Abajo del panel, un recuadro te muestra **el cálculo completo, en palabras**: de dónde salió la población, cuántas atenciones son al año y cuántas horas por semana significan. Nada queda escondido.

Usa los filtros de arriba para no perderte entre 236 filas.

---

## Paso 7 · Resultados (menú 07)

La respuesta a la pregunta de fondo: **¿alcanzamos o no?**

Verás una barra por cada estamento:

- **Barra verde a la derecha** → te sobran horas.
- **Barra roja a la izquierda** → te faltan horas. Ahí hay un problema.

El número al final es cuántas horas semanales sobran o faltan.

**Haz clic en cualquier barra** y te lleva al detalle de ese estamento.

Más abajo, el gráfico de *cuello de botella* te dice qué recurso es el que aprieta primero: si un estamento o una sala. Sobre 100 % significa que ese recurso ya no da más.

---

## Paso 8 · Vista por estamento (menú 08)

Para que cada referente revise **lo suyo**.

Eliges un estamento arriba y ves todo lo que le toca: cuántas personas tiene, qué prestaciones le asignaron, cuántas horas exige cada una y si le alcanza.

El último gráfico ordena sus prestaciones de mayor a menor carga. Sirve para lo más práctico: **las primeras tres o cuatro suelen concentrar la mitad del trabajo**. Ahí es donde vale la pena discutir, no en las de abajo.

Puedes hacer clic en cualquier prestación para corregirla al vuelo, y bajar la tabla con *Exportar programación (CSV)*.

---

## Paso 9 · Escenarios (menú 09)

Para probar sin miedo: *¿y si contratamos otro médico?*, *¿y si subimos la cobertura?*

1. Botón **Duplicar escenario activo**.
2. Ponle nombre ("Con 2 médicos más").
3. Ve a los módulos y haz los cambios que quieras.
4. Vuelve aquí: la tabla y el gráfico te muestran los escenarios lado a lado.

Tu escenario original queda intacto. Puedes tener todos los que quieras.

---

## Paso 10 · Informe (menú 10)

Botón **Generar informe** y listo: un documento con los insumos, los supuestos, los resultados, las brechas y las recomendaciones, escrito en lenguaje profesional.

Con **Imprimir o guardar como PDF** lo llevas a una reunión o lo adjuntas a un oficio.

---

## Cuando termines

**Guardar proyecto** (menú izquierdo). Se descarga un archivo. Guárdalo como guardarías cualquier documento importante.

Ese archivo tiene todo: tus datos, tus escenarios, tus decisiones.

---

## Preguntas que todos hacen

**¿Necesito internet?**
Solo la primera vez que la abres, para cargar los gráficos. Después funciona igual.

**¿Se guarda sola?**
No, y es a propósito. Tú decides qué versión conservar y con qué nombre. Así queda constancia de cada ejercicio.

**¿Los datos se van a algún servidor?**
No. Todo ocurre en tu computador. El archivo que descargas es el único lugar donde queda tu información.

**Cambié algo y quedó peor. ¿Cómo vuelvo atrás?**
Cierra sin guardar y carga tu último archivo guardado. Por eso conviene guardar cada cierto rato.

**¿Sirve para otro CESFAM que no sea Tongoy?**
Sí. Cambia la población, el equipo, los box y el nombre. La lógica de cálculo es la misma para cualquier centro del país.

**Me sale un número raro.**
Abre la prestación en el módulo 06: el recuadro del cálculo te muestra paso a paso de dónde salió cada cifra.

**¿Qué es eso de "horas por 1.000 inscritos"?**
Sirve para compararte con otros centros, sin importar el tamaño. Si tu centro marca un número muy distinto al de un CESFAM parecido, lo más probable es que falte adaptar la cartera (módulo 02).

**Los sectores suman un poco más que el total del centro.**
Es normal, alrededor de 1 %. Cada sector redondea sus atenciones hacia arriba, porque no existen medias atenciones. Para cifras oficiales usa la vista consolidada.
