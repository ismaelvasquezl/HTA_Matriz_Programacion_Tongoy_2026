# ProgramAPS — Índice del proyecto

Programación de oferta y cupos para la Atención Primaria de Salud en Chile.
Todo lo desarrollado, en un solo lugar.

---

## La herramienta

**`ProgramAPS_Tongoy.html`**
La aplicación. Se abre con doble clic en cualquier navegador; no necesita instalación ni internet (salvo la primera vez, para dibujar los gráficos). Trae 236 prestaciones, la dotación real anonimizada y el per cápita 2026 de Tongoy. Reproduce el modelo de la planilla original verificado celda a celda (480,84 h/sem), se adapta a cualquier establecimiento del país y está endurecida contra archivos maliciosos. Los datos nunca salen del computador.

---

## Para presentarla al equipo

**`ProgramAPS_Presentacion.html`**
Presentación de 17 láminas que se abre en el navegador. Se navega con las flechas, la tecla **N** muestra las notas del orador, **F** activa pantalla completa. Diseño moderno con la barra de balance como firma visual.

**`presentacion_contenido.json`**
El contenido de la presentación (textos y notas), separado del diseño. Se edita aquí, sin tocar código.

**`presentacion_generar.py`**
El generador. Lee el JSON y produce el HTML. Tras editar el contenido, ejecutar `python3 presentacion_generar.py` para regenerar la presentación.

**`ProgramAPS_Presentacion.pptx`**
La misma presentación en formato PowerPoint, por si se prefiere editarla o proyectarla desde Office.

---

## Para aprender a usarla y explicarla

**`Guia_de_uso_ProgramAPS.md`**
Guía llana, paso a paso, para cualquier equipo CESFAM. Diez pasos, lenguaje sencillo, sin tecnicismos. Pensada para que cualquier persona la siga sin ayuda.

**`Manual_tecnico_ProgramAPS.md`**
Material para el responsable técnico: las reglas del modelo con su origen en el Excel, el encuadre normativo (per cápita FONASA, orientaciones MINSAL, Ley 19.378, IAAPS, MAIS), un guion de capacitación de 45 minutos y las respuestas a las objeciones que van a aparecer.

---

## Para entender cómo se hizo

**`Bitacora_del_desarrollador.md`**
El relato completo del viaje desde el Excel hasta la app: qué encontramos en la planilla, qué decidimos y por qué, los errores que cometimos y corregimos, y la motivación de fondo. Escrita para leerse de corrido.

**`Informe_pruebas_ProgramAPS.md`**
El registro técnico de las pruebas en cinco perfiles de establecimiento: los cuatro defectos encontrados —uno grave— y cómo se corrigieron. La evidencia detrás de las afirmaciones de la bitácora.

---

## Orden sugerido de lectura

1. Si vas a **usar** la herramienta → empieza por la *Guía de uso* y abre la app.
2. Si vas a **presentarla** → abre la *Presentación* y lee sus notas del orador; apóyate en el *Manual técnico*.
3. Si quieres **entender el desarrollo** → la *Bitácora*, y luego el *Informe de pruebas* para el detalle.

---

*Departamento de Salud Coquimbo · CESFAM Tongoy y Posta Guanaqueros*
