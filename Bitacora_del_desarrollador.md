# Bitácora del desarrollador

### De una planilla heredada a una herramienta para todo Chile

*El relato de cómo se construyó ProgramAPS: qué encontramos, qué decidimos y por qué.*

---

## Por qué empezamos

Hay una planilla que circula por los CESFAM de este país. Cambia de nombre, de comuna, de manos, pero es siempre la misma criatura: un Excel de programación con hojas ocultas, fórmulas encadenadas y, en alguna celda que nadie mira, la respuesta a la única pregunta que importa cuando se planifica un año de salud primaria: **¿cuántas horas de cada profesional necesitamos, y nos alcanzan?**

La planilla que originó este trabajo la construyó Carlos Guerra en el DESAM de Coquimbo, para el CESFAM Tongoy. Y hay que decirlo de entrada, porque es el punto de partida de todo lo demás: **es un buen trabajo técnico**. La lógica que encierra —traducir población en demanda, demanda en horas, horas en brechas— es sólida y está bien alineada con cómo el MINSAL espera que se programe en la red.

El problema nunca fue el cálculo. El problema era otro, y es un problema que se repite en miles de establecimientos: **el conocimiento vivía en una sola cabeza.** Las reglas críticas estaban en hojas ocultas, en fórmulas de 130 caracteres, en decisiones que el autor tomó con buen criterio pero que nunca quedaron escritas en ninguna parte legible. El día que esa persona se va —a otro cargo, a otra comuna, a su jubilación— la planilla sigue funcionando, pero ya nadie sabe *por qué* funciona. Y una herramienta que nadie entiende es una herramienta que, tarde o temprano, se usa mal o se abandona.

Esta bitácora cuenta cómo convertimos esa planilla en algo distinto: no en un cálculo mejor —el cálculo era correcto— sino en un cálculo **auditable**. Algo que cualquier equipo pueda abrir, entender, cuestionar y corregir, sin depender de la memoria de quien lo construyó.

Ese es el hilo conductor de todo lo que sigue: **hacer visible lo que estaba tácito.** Porque cuando el cálculo es transparente, deja de ser una caja negra que hay que obedecer y se convierte en lo que siempre debió ser: una conversación honesta sobre a cuánta gente alcanzamos a cuidar con las horas que realmente tenemos.

---

## Capítulo 1 · Escuchar la planilla antes de tocarla

La tentación, frente a un Excel viejo, es reescribirlo de inmediato. Resistimos esa tentación. Antes de proponer nada, había que entender —de verdad, celda por celda— qué hacía la planilla y por qué.

Abrimos los dos archivos con una librería que permite leer tanto las fórmulas como sus resultados (`openpyxl`, cargando cada libro dos veces: una para ver las fórmulas, otra para ver los valores calculados). Y empezamos a reconstruir la maquinaria.

Lo que encontramos fue una cadena de ocho reglas, repartidas en catorce hojas, tres de ellas ocultas:

- Una hoja oculta (`0-DAYPRO`) calculaba **cuántos días hábiles quedaban realmente** para programar, restando vacaciones, capacitaciones y permisos. En 2023: 217 días, 44 semanas. Este número, que nadie veía, era la base temporal de todo el ejercicio.
- Otra hoja oculta (`Índices`) guardaba los catálogos maestros: estamentos, jornadas, programas, tipos de atención.
- La hoja de recurso humano tomaba a cada persona, le descontaba la colación, las horas de administración y las de actividades indirectas, y así calculaba su **oferta asistencial real**: las horas que de verdad le quedaban para atender público.
- La hoja de programación —el corazón— cruzaba población, cobertura y concentración para estimar cuántas atenciones había que hacer al año, las repartía entre estamentos y las valorizaba en horas usando una matriz de rendimientos.
- Y una hoja de balance final contrastaba, por estamento, las horas que se necesitaban contra las que había.

Documentamos cada una de esas reglas con un nombre (R1 a R8) y su origen exacto en el Excel. No para lucirlas, sino porque **ese fue precisamente el activo que se estaba perdiendo**: el conocimiento de por qué la planilla hacía lo que hacía.

### El primer hallazgo que nos detuvo

Mientras reconstruíamos la regla del "total a trabajar", encontramos algo que no estaba documentado en ninguna parte y que solo se veía leyendo una fórmula concreta, la de la celda M6:

> En las actividades **grupales**, la planilla divide por el número de asistentes a la sesión —pero **solo cuando la población viene del per cápita**. Si viene de un valor observado, no divide.

Al principio pareció un error. No lo era. Era una decisión fina y correcta: el per cápita entrega *personas*, que hay que convertir a *sesiones*; pero un valor observado del registro REM ya viene expresado en sesiones realizadas. Dividirlo sería contarlo dos veces.

Nos detuvimos en este detalle porque es la prueba viviente de por qué valía la pena todo el proyecto. **Ningún funcionario que heredara esa planilla lo habría deducido jamás.** Estaba en la cabeza de quien la construyó, y en ningún otro lugar. En la app, ahora es la regla R6, escrita, comentada y verificada. Ese es, en miniatura, el problema que vinimos a resolver.

---

## Capítulo 2 · Las decisiones de diseño, y sus porqués

Con la maquinaria entendida, había que decidir qué conservar, qué rediseñar y qué construir desde cero. Cada decisión tuvo una razón, y conviene dejarlas por escrito.

### Por qué una sola página web, sin instalar nada

Elegimos construir la herramienta como un único archivo HTML que se abre con doble clic en cualquier navegador. Sin servidor, sin instalación, sin cuenta. La razón es práctica y humana a la vez: un CESFAM no tiene un departamento de sistemas esperando para instalar software, y un funcionario no debería necesitar permisos de administrador para programar su año. Un archivo que se abre como una página web elimina toda esa fricción. Se puede copiar en un pendrive, mandar por correo, guardar en una carpeta compartida.

### Por qué los datos se guardan en un archivo, y no solos

La herramienta no guarda nada automáticamente. Al terminar, uno aprieta "Guardar proyecto" y se descarga un archivo. Esto fue deliberado y va contra la costumbre. La razón: en salud pública, la **trazabilidad** no es un lujo, es un requisito. Que cada ejercicio quede en un archivo con nombre y fecha permite versionar, auditar y adjuntar a un oficio. Un dato escondido en la memoria del navegador no se puede auditar; un archivo, sí.

### Por qué anonimizamos al equipo

El archivo original contenía los RUN y los nombres completos de 78 funcionarios. Para programar, eso no hace falta: se necesita saber *qué estamento, qué jornada, qué horas*, no *quién*. Así que la app trae la dotación real —persona por persona, para que las sumas cuadren— pero sin RUN ni nombres, con etiquetas editables. Cada centro pone las glosas que quiera. Fue una decisión de respeto por los datos de personas que no tienen por qué circular en un archivo que se comparte.

### Por qué agregamos cosas que la planilla no tenía

La planilla no registraba los box clínicos, no consideraba el ausentismo, no permitía sectorizar ni comparar escenarios. Agregamos las cuatro cosas, pero con una regla de honestidad estricta: **todo lo que inventamos aparece marcado como supuesto a validar.** El ausentismo viene en 8 % con un cartel que lo dice. Los box vienen con cantidades tentativas y una advertencia de que hay que reemplazarlas por las reales. Preferimos un supuesto visible y discutible a un silencio cómodo. La planilla, por ejemplo, asumía cero ausentismo sin decirlo nunca: un supuesto oculto que todos heredaban. El nuestro está a la vista, y por eso se puede corregir.

---

## Capítulo 3 · La lección más dura: cuando la validación miente

Aquí la bitácora tiene que ser incómoda, porque la honestidad técnica lo exige.

En una primera versión, anunciamos con orgullo que el motor reproducía el Excel a la perfección: 359,54 horas semanales en la planilla, 359,54 en la app. Catorce de catorce estamentos, diferencia cero. Parecía la prueba definitiva.

Era falsa.

Cuando pusimos la herramienta a prueba con datos de otros establecimientos —una posta pequeña, un CESFAM urbano grande— apareció algo raro. Y al investigar, descubrimos el error: **nuestra extracción de datos había leído solo hasta la fila 300 del Excel, y la planilla llegaba a la 341.** Nos habíamos saltado 56 prestaciones, entre ellas el ciclo vital del Adulto Mayor completo: los controles cardiovasculares, el EMPAM, el pie diabético, la podología.

Pero lo verdaderamente aleccionador fue *por qué* la validación no lo detectó. El script que comparaba la app contra el Excel **leía el mismo rango truncado**. Ambos lados ignoraban las mismas 56 filas. Coincidían a la perfección porque compartían exactamente el mismo error.

De ahí salió el principio que quedó grabado en el manual técnico:

> Una validación solo prueba algo si el verificador no comparte los supuestos del verificado. Coincidir no es lo mismo que estar bien.

Rehicimos la extracción leyendo la hoja completa. La demanda real no era 359,54: era **480,84 horas semanales**. Habíamos estado omitiendo un cuarto de la carga del establecimiento —justamente la de los adultos mayores, que en muchos centros son la población que más consulta.

Y esta vez buscamos un testigo independiente. La propia planilla tiene una hoja de resumen (`Resumen_clinico`) que no participa del cálculo principal. Nuestro motor arrojó 49,54 horas de enfermería; esa hoja mostraba `2 days 1:32:30`, que son exactamente 49,54 horas. Coincidir con un testigo que no estuvo en el crimen sí prueba algo.

La lección no fue solo técnica. Fue sobre la humildad que exige trabajar con datos que afectan a personas: **hay que desconfiar de la propia buena noticia**, y probar contra algo que no pueda estar cometiendo el mismo error.

---

## Capítulo 4 · Probarla en cinco Chiles distintos

Para que sirviera en todo el país, no bastaba con que funcionara en Tongoy. Así que la ejecutamos —de verdad, no en el papel— contra cinco perfiles de establecimiento: Tongoy tal cual, un CESFAM urbano grande y sectorizado, una posta rural mínima, un centro envejecido y uno joven de alta natalidad.

El resultado fue revelador e incómodo. La demanda proveniente de los valores observados era **idéntica en los cinco casos**, aunque las poblaciones iban de 3.000 a 36.000 personas. La razón: 137 de las 236 prestaciones usaban cifras absolutas del REM de Tongoy, que no se ajustan solas al cambiar de población. Al triplicar la población, la demanda crecía apenas un 63 % en vez de un 200 %. **Un CESFAM grande que heredara la cartera habría subestimado casi la mitad de su demanda, y el balance se habría visto tranquilizador.** El peor tipo de error: el que no avisa.

Así nació el panel de **adaptación de cartera**, con su alerta automática y su ajuste por estructura de población —que reescala cada prestación según su propio grupo etario, no según el total del centro. Tras adaptarla, los tres establecimientos de tamaños tan distintos convergieron en la misma demanda por cada mil inscritos. Y donde la pirámide cambiaba, la demanda cambiaba como debía: más horas por persona en el centro envejecido, menos en el joven. Eso es medicina, y por fin el modelo lo reflejaba.

De ese mismo ejercicio salió una pregunta que ninguna planilla de horas responde y que agregamos como gráfico: **¿a quién le estamos programando?** Contrastar el peso de cada tramo etario en la población con su peso en las horas programadas convierte un cálculo de recursos en una pregunta de equidad.

---

## Capítulo 5 · Endurecer la herramienta

Una vez que el cálculo era correcto y portable, tocó pensar como quien quiere romperla.

La app deja escribir nombres libres —de prestaciones, de personas, de sectores— y esos nombres se muestran en pantalla. Si alguien escribía instrucciones maliciosas disfrazadas de nombre y compartía el archivo de proyecto, esas instrucciones podían ejecutarse al abrirlo en otro computador. Es una vulnerabilidad clásica, y estaba presente en unos treinta puntos de la app. La cerramos: ahora todo texto escrito por una persona se neutraliza antes de mostrarse, de modo que un nombre es siempre solo un nombre, nunca una instrucción. Lo probamos inyectando ataques reales en el navegador: ninguno se disparó.

Añadimos también una validación estricta al cargar proyectos —para que un archivo dañado o manipulado no rompa el motor ni meta datos extraños— y una política de seguridad que impide que la app haga conexiones a servidores externos. Porque ese es otro compromiso de fondo: **los datos nunca salen del computador de quien la usa.** No hay servidor, no hay telemetría, no hay nube.

Hubo aquí una decisión que vale la pena contar, porque muestra que la seguridad no es una lista de casillas que marcar. Intentamos añadir una verificación criptográfica a las librerías externas que la app carga. En el papel, más seguro. En la práctica, descubrimos que esa verificación —al abrir la app con doble clic desde una carpeta local— hacía que el navegador **bloqueara las librerías y dejara la app sin funcionar.** Habría sido "más seguro" y completamente inútil. Lo revertimos y documentamos por qué. La seguridad que rompe la herramienta no es seguridad: es un obstáculo con buena prensa.

---

## Lo que quedó, y lo que falta

Al final de este camino, la herramienta reproduce fielmente el modelo de programación comunal —verificado contra la planilla original y contra su propia hoja de resumen—, se adapta a establecimientos de cualquier tamaño y perfil demográfico, resiste archivos maliciosos y no deja escapar ningún dato del computador. Tiene la cartera completa, los cinco ciclos vitales, cobertura desde el nacimiento hasta los cien años.

Y tiene pendientes honestos, que decimos nosotros antes de que los descubra otro: los box hay que levantarlos con el dato real de cada centro; el ausentismo conviene calcularlo con las licencias propias; las coberturas vienen del ejercicio 2023 y deben contrastarse con las orientaciones vigentes; y lo definitivo, más allá de adaptar la cartera heredada, es que cada establecimiento cargue su propio REM, prestación por prestación. Ninguno de esos pendientes afecta el cálculo, que está verificado. Son datos de entrada, todos a la vista y todos editables. Que estén declarados es, precisamente, lo que diferencia esta herramienta de la planilla que reemplaza.

---

## Coda · Para quién es todo esto

Se puede leer esta bitácora como una crónica técnica: extraer, reconstruir, validar, endurecer. Pero sería quedarse en la superficie.

Lo que de verdad se hizo aquí fue tomar un conocimiento que vivía encerrado en la cabeza de una persona y en las hojas ocultas de un archivo, y ponerlo sobre la mesa para que un equipo entero pudiera verlo, entenderlo y discutirlo. Programar bien un CESFAM no es llenar una planilla: es decidir, con horas contadas y población real, a quién se alcanza a cuidar y a quién no. Esa decisión es demasiado importante para que ocurra a ciegas, o para que dependa de que una sola persona recuerde por qué una celda dice lo que dice.

Cada brecha que esta herramienta hace visible es una conversación que antes ocurría sin números. Cada supuesto que obliga a declarar es un acuerdo que antes se heredaba en silencio. Y esa transparencia, al final del día, no es una virtud técnica: es un asunto de equidad. Porque las horas que un equipo de salud no ve, son horas de cuidado que alguien, en algún rincón de su población a cargo, no va a recibir.

Por eso se construyó esta herramienta. No para calcular mejor —el cálculo ya estaba bien—, sino para que nadie más tenga que programar a ciegas.

---

*Bitácora del desarrollo de ProgramAPS · Departamento de Salud Coquimbo · CESFAM Tongoy y Posta Guanaqueros*
