# Prompt para el agente local (Civil 3D) – corrección de la Intersección 3

Copia todo lo que sigue (desde "ROL" hasta el final) y pégalo como instrucción a tu agente local.
Los valores están calculados a partir del modelo actual; si el agente reporta algo distinto en un CHECKPOINT,
no sigas hasta revisarlo.

---

## ROL Y REGLAS

Eres mis manos dentro de Autodesk Civil 3D. No diseñas ni decides: ejecutas exactamente los pasos de este documento,
en orden, y me reportas lo que ves. Reglas obligatorias:

1. Trabaja siempre sobre la copia del dibujo que se crea en la FASE 0, nunca sobre el original.
2. Haz un paso a la vez. Cuando llegues a una línea que empieza por **CHECKPOINT**, detente, reporta exactamente los datos
   que se piden (copiando los valores tal cual aparecen en pantalla) y espera mi confirmación antes de continuar.
3. Si un nombre, un valor, un botón o un mensaje no coincide con lo que dice este documento, o aparece un error, detente y
   repórtalo textualmente. No improvises, no "arregles", no busques alternativas.
4. Nunca borres nada que no esté en la lista de la FASE 1. Nunca cambies valores que no estén escritos aquí.
5. Los nombres de menús se dan en español y entre paréntesis en inglés; usa el que corresponda a la interfaz.
6. Unidades: metros. Las estaciones se escriben como 4+142.60 (= 4142.60 m). Coordenadas en UTM 17S (Este, Norte).
   Offset positivo = lado derecho de la alineación mirando en el sentido de avance de las estaciones.
7. Comando transparente `'SO` (Estación/desfase, Station Offset): cuando Civil 3D pide un punto, escribe `'SO` y Enter,
   selecciona la alineación que se indica, escribe la estación, Enter, escribe el desfase, Enter. Si el comando pide
   "estación" en otro formato, escribe el número sin el signo "+" (por ejemplo 4100).
8. Al terminar cada fase, guarda el dibujo (Ctrl+S).

## CONTEXTO (solo para que entiendas el objetivo)

El eje "Eje Via de evitamiento" termina hoy sobre la vía "1NK_I1" en su estación 0+184.99 formando una "Y" de 19.7°, y la
intersección creada con el asistente quedó mal (cuadrantes con radios de 3 m y 200 m, taludes cruzados). La corrección es:

* La vía de evitamiento se prolonga con una curva (R = 550 m, espirales de 75 m) y continúa por el tramo norte de 1NK_I1.
* La antigua 1NK_I1 del lado sur se conecta a la vía de evitamiento con un ramal nuevo en "T" a 90°, en la estación 4+100.
* Se rehace la intersección con el asistente, ahora en T, con radios de 20 m y ensamblajes rurales iguales en ambas vías.

## DATOS DE CONTROL (para verificar, no para modificar)

| Punto | Este | Norte |
|---|---|---|
| Fin actual del eje (vértice, 4+275.61) | 528814.319 | 9404994.645 |
| Inicio de 1NK_I1 (0+000) | 528900.293 | 9405158.448 |
| Fin de 1NK_I1 (0+487.37) | 528711.823 | 9404711.806 |
| 1NK_I1 estación 0+330 | 528752.763 | 9404863.775 |
| Punto J = eje 4+100.00, desfase 0 (inicio del ramal) | 528685.094 | 9404875.731 |
| Eje 4+100.00, desfase +100 | 528752.794 | 9404802.132 |
| TS esperado de la nueva curva (4+142.60) | 528716.447 | 9404904.571 |
| ST esperado de la nueva curva (= 1NK_I1 0+051.98) | 528876.139 | 9405112.420 |
| PI de la curva del ramal | 528739.89 | 9404816.15 |
| Fin de la curva del ramal (= 1NK_I1 0+412.4) | 528731.33 | 9404784.22 |

## FASE 0 – Preparación e inventario

0.1 Abre el DWG del proyecto. Menú Archivo → Guardar como (Save As) con el nombre `<nombre original>_v2_interseccion3.dwg`.
    A partir de aquí trabaja solo en este archivo.
0.2 En el Espacio de herramientas (Toolspace), pestaña Prospector, despliega y anota:
    * Alineaciones (Alignments) → Alineaciones de eje (Centerline), Alineaciones de desfase (Offset), Alineaciones de retorno
      de bordillo (Curb Return). Anota el nombre exacto de todas.
    * Corredores (Corridors): nombres.
    * Superficies (Surfaces): nombres.
    * Intersecciones (Intersections): nombres.
    * Ensamblajes (Assemblies): nombres y, para el ensamblaje que usa el corredor "Vía de evitamiento", la lista de
      subensamblajes de cada lado (clic derecho en el ensamblaje → Propiedades → pestaña Construcción).

**CHECKPOINT 0**: pega las listas completas de 0.2. Debe existir: alineación "Eje Via de evitamiento", alineación "1NK_I1",
corredor "Vía de evitamiento", corredor "Interseccion 3", superficies "Rasante", "Subrasante", "Topografia",
"Interseccion_3", y una o dos intersecciones cuyo nombre empieza por "Interseccion 3". Si los nombres difieren, repórtalo.

## FASE 1 – Eliminar la intersección 3 actual y los objetos sobrantes

1.1 Prospector → Intersecciones → clic derecho en cada intersección cuyo nombre empiece por "Interseccion 3" (por ejemplo
    "Interseccion 3" e "Interseccion 3 (1)") → Eliminar (Delete). Si pregunta si borra los objetos dependientes
    (alineaciones de desfase, retornos de bordillo, perfiles), responde Sí.
1.2 Prospector → Corredores → clic derecho en "Interseccion 3" → Eliminar.
1.3 Prospector → Superficies → clic derecho en "Interseccion_3" → Eliminar.
1.4 Prospector → Alineaciones: borra SOLO las que sigan existiendo de esta lista (clic derecho → Eliminar):
    * "Interseccion 3 - SO - Quadrant", "Interseccion 3 (1) - NO - Quadrant", "Interseccion 3 (1) - SO - Quadrant"
    * "Eje Via de evitamiento-Derecha-3.300", "Eje Via de evitamiento-Izquierda-3.300"
    * "Eje Via de evitamiento-Derecha-3.600 (24)", "Eje Via de evitamiento-Izquierda-3.600 (23)"
    * "1NK_I1-Derecha-3.600", "1NK_I1-Izquierda-3.600", "1NK_I1_ Calzada derecha", "1NK_I1_ Calzada Izquierda"
    No borres ninguna otra alineación. En particular NO borres "1NK_I1", "Eje Via de evitamiento",
    "Límite de calzada - Derecha", "Límite de calzada - Izquierda" ni las que empiezan por "Analisis".
1.5 Guarda.

**CHECKPOINT 1**: pega de nuevo la lista de alineaciones, corredores, superficies e intersecciones.

## FASE 2 – Prolongar el eje "Eje Via de evitamiento" con la nueva curva

2.1 Selecciona la alineación "Eje Via de evitamiento" en el dibujo (o en Prospector → clic derecho → Seleccionar).
    En la cinta contextual Alineación → Modificar → Editor de geometría (Geometry Editor). Se abre la barra
    "Herramientas de composición de alineación" (Alignment Layout Tools).
2.2 En esa barra, botón "Línea fija (dos puntos)" (Fixed Line – Two points).
    * Primer punto: escribe `'SO`, selecciona "Eje Via de evitamiento", estación 4275.613, desfase 0.
    * Segundo punto: escribe `'SO`, selecciona "1NK_I1", estación 0, desfase 0.
    * Enter para terminar. Debe aparecer una línea nueva desde el fin del eje hasta el inicio de 1NK_I1, superpuesta a 1NK_I1.
2.3 En la misma barra, botón "Espiral-curva-espiral libre (entre dos entidades)" (Free Spiral-Curve-Spiral – Between two entities).
    * Primera entidad: haz clic sobre la última tangente del eje (por ejemplo cerca de la estación 4+200).
    * Segunda entidad: haz clic sobre la línea creada en 2.2 (cerca de su punto medio).
    * Si pregunta "ángulo de solución de la curva" (curve solution angle): elige "Menor que 180" (Lessthan180).
    * Longitud de espiral de entrada: 75. Radio: 550. Longitud de espiral de salida: 75. (Si pide tipo de espiral: Clotoide.)
    * Enter/Esc para terminar. Cierra la barra de herramientas.
2.4 Selecciona la alineación → cinta Alineación → Propiedades de alineación (Alignment Properties) → pestaña Información:
    anota la longitud. Luego cinta Alineación → Editor de geometría → botón "Vista de entidades de alineación"
    (Alignment Entities / Grid View) y anota las tres últimas entidades y la última línea.

**CHECKPOINT 2**: reporta (a) longitud total de la alineación: esperado 4458.58 m (±0.10); (b) entidades finales esperadas:
Espiral L=75.000, Curva R=550.000 L=114.00 con Δ=19.6889°, Espiral L=75.000, Línea L=51.98; (c) estaciones esperadas:
TS 4+142.60, SC 4+217.60, CS 4+331.60, ST 4+406.60, fin 4+458.58; (d) las estaciones de inicio/fin de las alineaciones
"Límite de calzada - Derecha" e "Izquierda" (Propiedades → Información) y si se actualizaron solas hasta 4+458.58.
Si la longitud no es 4458.58 ±0.10, detente.

## FASE 3 – Crear el ramal "Ramal_1NK_I1"

3.1 Cinta Inicio → Crear diseño → Alineación → Herramientas de creación de alineaciones (Create Alignment – Layout).
    Nombre: `Ramal_1NK_I1`. Tipo: Eje (Centerline). Estación inicial: 0. Estilo y conjunto de etiquetas: los mismos que
    "Eje Via de evitamiento". Criterios de diseño: sin marcar por ahora. Aceptar.
3.2 Barra de composición → "Línea fija (dos puntos)":
    * Primer punto: `'SO` → "Eje Via de evitamiento" → estación 4100 → desfase 0.
    * Segundo punto: `'SO` → "Eje Via de evitamiento" → estación 4100 → desfase 100.
    * Enter. (Línea perpendicular al eje, hacia el lado derecho/sureste.)
3.3 "Línea fija (dos puntos)" de nuevo:
    * Primer punto: `'SO` → "1NK_I1" → estación 330 → desfase 0.
    * Segundo punto: `'SO` → "1NK_I1" → estación 487.374 → desfase 0.
    * Enter. (Línea sobre la última tangente de la antigua 1NK_I1.)
3.4 "Curva libre – acuerdo entre dos entidades, por radio" (Free Curve Fillet – Between two entities, radius):
    * Primera entidad: la línea de 3.2. Segunda entidad: la línea de 3.3.
    * Si pregunta el ángulo de solución: "Menor que 180". Radio: 60.
    * Enter/Esc. Civil 3D recorta las dos líneas en los puntos de tangencia. Cierra la barra.
3.5 Propiedades de la alineación → Información: anota la longitud. Editor de geometría → Vista de entidades: anota entidades.

**CHECKPOINT 3**: esperado: Línea L≈47.9, Curva R=60.000 L≈60.43 Δ≈57.70°, Línea L≈75.0; longitud total ≈183.3 m (±0.3);
inicio del ramal en E 528685.094 / N 9404875.731 (coincide con el punto J). Reporta también las coordenadas del fin de
la curva (esperado E 528731.33 / N 9404784.22).

## FASE 4 – Perfiles

4.1 Perfil de la vía principal. Selecciona la alineación "Eje Via de evitamiento" → abre su visualización de perfil
    (si no existe una vista de perfil, cinta Alineación → Vista de perfil → Crear vista de perfil, con la superficie
    "Topografia" y el perfil "Rasante"). Selecciona el perfil "Rasante" → cinta Perfil → Modificar → Editor de geometría
    (Profile Layout Tools) → botón "Vista de cuadrícula de perfil" (Profile Grid View).
4.2 En la cuadrícula, localiza los PVI de estación 4264.93 y 4275.61 y elimínalos (botón "Eliminar PVI" de la barra y clic
    sobre cada uno, o clic derecho en la fila → eliminar). No toques el PVI de 4141.81 ni ninguno anterior.
4.3 Barra → "Insertar PVI – tabular" (Insert PVIs – Tabular). Añade:
    * Estación 4380.00, elevación 20.373
    * Estación 4458.58, elevación 21.037
    Aceptar. Si la última estación no se acepta porque supera el final de la alineación, usa 4458.57.
4.4 En la cuadrícula comprueba que el PVI 4141.81 conserva la curva vertical de longitud 172.39 m.
4.5 Perfil del ramal. Selecciona "Ramal_1NK_I1" → Crear vista de perfil (superficie "Topografia") → en la vista, cinta
    Vista de perfil → Crear perfil por composición (Profile Creation Tools). Nombre: `Rasante ramal`.
    Barra → "Insertar PVI – tabular":
    * Estación 0.00, elevación: la elevación del perfil "Rasante" del eje en la estación 4+100 DESPUÉS de la FASE 4.3.
      Para leerla: en la vista de perfil del eje usa Perfil → Propiedades → pestaña "Datos de perfil" o el comando
      de etiqueta de estación; esperado ≈ 17.80.
    * Estación 108.30, elevación 20.01
    * Estación 183.30, elevación 19.16
    Después, en la cuadrícula, al PVI de 108.30 asígnale una curva vertical (parabólica) de longitud 30.
4.6 Guarda.

**CHECKPOINT 4**: pega la tabla de PVI (estación, elevación, longitud de curva) de "Rasante" desde 3985 hasta el final, y la
tabla completa de "Rasante ramal". Reporta además la elevación del perfil "Perfil 1NK_I1" en las estaciones 0+000, 0+031,
0+052 y 0+078 (para revisar el empalme con la vía existente).

## FASE 5 – Ensamblajes para la intersección (juego rural)

Objetivo: que las dos vías usen la misma sección. Se parte del ensamblaje del corredor "Vía de evitamiento"
(lo llamo `VE`; usa el nombre real que anotaste en la FASE 0).

5.1 Prospector → Ensamblajes → clic derecho en `VE` → Copiar (o selecciónalo en el dibujo y usa Copiar/Pegar en un sitio
    libre del dibujo). Repite hasta tener 5 copias. Renómbralas (clic derecho → Propiedades → Información → Nombre):
    `VE_Cuadrante`, `VE_TaludIzq`, `VE_TaludDer`, `VE_MitadIzq`, `VE_MitadDer`.
5.2 Edita cada copia seleccionando el subensamblaje en el dibujo y pulsando Supr (o desde Propiedades del ensamblaje →
    Construcción → clic derecho → Eliminar):
    * `VE_TaludIzq`: en el lado DERECHO elimina el talud (Daylight), el bordillo y la berma. Deja solo el carril derecho.
      El lado izquierdo queda completo.
    * `VE_TaludDer`: lo simétrico: lado IZQUIERDO solo carril; lado derecho completo.
    * `VE_MitadIzq`: elimina todo el lado derecho (carril, berma, bordillo, talud). Queda solo el lado izquierdo completo.
    * `VE_MitadDer`: elimina todo el lado izquierdo. Queda solo el lado derecho completo.
    * `VE_Cuadrante`: lado IZQUIERDO solo el carril; lado DERECHO berma + bordillo + talud (elimina el carril derecho).
5.3 Comprueba el tipo del subensamblaje de carril: selecciónalo → Propiedades → pestaña Parámetros → arriba aparece el
    nombre del subensamblaje (por ejemplo "LaneSuperelevationAOR", "LaneOutsideSuper", "BasicLane").

**CHECKPOINT 5**: reporta el nombre del subensamblaje de carril y de talud, y la lista de subensamblajes de cada uno de los
6 ensamblajes (`VE` y las 5 copias). Si el carril NO es "LaneSuperelevationAOR", detente: te indicaré cómo reemplazarlo
(ese subensamblaje es el que admite destinos de anchura y elevación, que la intersección necesita).

## FASE 6 – Crear la nueva intersección en T

6.1 Cinta Inicio → Crear diseño → Intersecciones → Crear intersección (Create Intersection). Cuando pida el punto de
    intersección, escribe `'SO` → "Eje Via de evitamiento" → estación 4100 → desfase 0 (o haz clic exactamente donde el
    ramal toca el eje). Si pide seleccionar la vía principal, elige "Eje Via de evitamiento".
6.2 Página General: nombre `Interseccion 3 T`; tipo de corredor de intersección: "Bombeo de vía principal mantenido"
    (Primary Road Crown Maintained). Siguiente.
6.3 Página Detalles de geometría:
    * Prioridad: vía principal = "Eje Via de evitamiento", secundaria = "Ramal_1NK_I1".
    * Botón Parámetros de desfase (Offset parameters): anchura de carril izquierda y derecha = 3.60 en ambas vías.
      Marca "Crear nuevos desfases desde el inicio hasta el fin de los ejes" SOLO para el ramal (no para el eje).
    * Botón Parámetros de retorno de bordillo (Curb return parameters): en los dos cuadrantes, tipo "Acuerdo circular"
      (Circular fillet), radio 20.00. "Ensanchar carril de giro" (Widen turn lane) desactivado en ambos.
    * Botón Parámetros de pendiente de carril (Lane slope): −2.00 % en todos.
    * Parámetros de perfil de retorno de bordillo: deja los valores por defecto.
    Siguiente.
6.4 Página Regiones de corredor:
    * Marca "Crear corredores en la zona de intersección".
    * Elige "Añadir a un corredor existente" (Add to an existing corridor) → "Vía de evitamiento".
    * Superficie para taludes (daylight): "Topografia".
    * Conjunto de ensamblajes: asigna
      - Retornos de bordillo / Curb Return Fillets → `VE_Cuadrante`
      - Sección completa de vía principal / Primary Road Full Section → `VE`
      - Sección parcial de vía principal, talud izquierdo / Primary Road Part Section – Daylight Left → `VE_TaludIzq`
      - Sección parcial de vía principal, talud derecho / Primary Road Part Section – Daylight Right → `VE_TaludDer`
      - Sección completa de vía secundaria / Secondary Road Full Section → `VE`
      - Media sección de vía secundaria, talud izquierdo / Secondary Road Half Section – Daylight Left → `VE_MitadIzq`
      - Media sección de vía secundaria, talud derecho / Secondary Road Half Section – Daylight Right → `VE_MitadDer`
    * Botón "Guardar como conjunto" (Save as a set) con nombre `Rural_VE` (para reutilizar).
    * Crear intersección.
6.5 Si aparece un aviso de regiones superpuestas o de destinos sin asignar, no cierres nada: copia el mensaje completo.

**CHECKPOINT 6**: pega los mensajes de 6.5 (si los hubo) y, en Prospector, la lista de alineaciones nuevas (desfases y
retornos de bordillo) con sus longitudes. Reporta el ángulo de la intersección que muestra la etiqueta (esperado 90.00°).

## FASE 7 – Corredor, superficies y comprobaciones

7.1 Prospector → Corredores → "Vía de evitamiento" → clic derecho → Propiedades → pestaña Parámetros. Copia la tabla
    completa: líneas base, regiones, ensamblaje, estación inicial y final de cada región.

**CHECKPOINT 7a**: pega esa tabla. Con ella te diré a qué estación debe terminar la región original del eje (para que no se
superponga con las regiones de la intersección) y qué región nueva hay que añadir desde el final de la intersección hasta
4+458.58 con el ensamblaje `VE`. Espera instrucciones.

7.2 (Tras mis instrucciones) ajusta las estaciones indicadas y, en la misma pestaña, botón "Definir todos los destinos"
    (Set all targets): superficie de destino = "Topografia" para todos los taludes. En las regiones de retorno de bordillo
    (`VE_Cuadrante`) comprueba en "Destinos" (Targets) que el carril tenga destino de anchura = alineación
    "Eje Via de evitamiento" y destino de elevación = perfil "Rasante". Copia lo que aparece antes de cambiar nada.
7.3 Aceptar → reconstruir el corredor (clic derecho → Reconstruir / Rebuild).
7.4 Propiedades del corredor → pestaña Contornos (Boundaries): clic derecho en la superficie "Rasante" → Añadir
    automáticamente → Extensión del corredor como contorno exterior (Corridor extents as outer boundary). Igual para
    "Subrasante". Aceptar y reconstruir.
7.5 Cinta Analizar → Comprobar distancia de visibilidad (Check Sight Distance): alineación "Eje Via de evitamiento",
    perfil "Rasante", superficie "Rasante", altura de ojo 1.07, altura de objeto 0.15, distancia mínima 128.156,
    exportar el informe HTML con el nombre `visibilidad_v2.html` en la carpeta del dibujo.
7.6 Guarda el dibujo. Exporta LandXML: Salida → Exportar → Exportar a LandXML, todos los objetos, nombre
    `<nombre original>_v2.xml`.

**CHECKPOINT 7b**: reporta si el corredor reconstruyó sin avisos, el área de las superficies "Rasante" y "Subrasante"
(Propiedades de superficie → Estadísticas), y cuántas filas del informe de visibilidad dicen "Yes" entre 4+000 y el final.
Adjunta `visibilidad_v2.html` y el LandXML exportado.

FIN. No hagas nada más después del CHECKPOINT 7b.
