# Análisis de la Intersección 3 (Vía de evitamiento × 1NK_I1)

Análisis hecho a partir del LandXML del proyecto (`ANDY RODRIGO BAYONA ANTÓN_Autodesk Civil 3D.xml`,
exportado el 2026-09-23 22:04 desde Civil 3D 2027) y del reporte HTML de comprobación de visibilidad
(`…_Autodesk Civil 3D.html`, 2026-09-23 10:36). El DWG no se puede leer fuera de Civil 3D, pero el LandXML
contiene alineamientos, perfiles, peraltes, corredores, secciones transversales (links y códigos de cada
subensamblaje) y superficies, que es todo lo que hace falta para reconstruir la intersección.

## 1. Conclusión

**La intersección se ve mal porque no es una intersección: es un empalme en "Y" con un ángulo de cruce de 19.7°.**
El eje de la vía de evitamiento llega a 1NK_I1 casi tangente a ella. El asistente de intersecciones de Civil 3D
(*Create Intersection*) está pensado para cruces en T o en cruz con ángulos razonables; con 19.7° genera:

| Elemento generado por el asistente | Valor en el modelo | Consecuencia visible |
|---|---|---|
| Cuadrante SO (ángulo agudo) | fillet **R = 3.00 m**, Δ = 160.3°, L = 8.39 m, T = 17.29 m | el "bucle" rojo: las secciones del corredor giran 160° sobre un radio de 3 m y se cruzan entre sí |
| Cuadrante NO (ángulo obtuso) | fillet **R = 200 m**, Δ = 19.7°, L = 68.7 m + 2 × 30 m de extensión (128.7 m) | franja larga de sardinel + cuneta + talud casi paralela a ambas vías |
| Puntos de tangencia | Eje 4+237.58 y 4+240.28; 1NK_I1 0+223.03 y 0+149.66 | la "boca" de la intersección mide 73 m sobre 1NK_I1 y 38 m sobre el eje |
| Región del corredor principal | llega hasta 4+240.28 con su sección rural completa | su **talud de corte derecho (hasta 15.8 m de ancho) entra en la calzada de 1NK_I1** entre 4+224 y 4+238 y cruza el eje de 1NK_I1 en 4+232 |
| Región de 1NK_I1 (0+119.66 a 0+233.03) | talud oeste completo | su talud entre 0+224 y 0+233 cae dentro de la calzada/berma del eje |
| Superficie `Interseccion_3` | 1 367 puntos, 2 655 caras, **todas invisibles, área = 0** | la superficie del corredor de intersección está vacía (por eso no se ve nada consistente en la zona) |

Las secciones transversales sí contribuyen, pero son la segunda causa, no la primera:

* Eje (corredor "Vía de evitamiento"): **sección rural**: calzada 2 × 3.60 m al 2 %, bermas de 3.00 m (código EPS en ±6.60),
  bordillo de 0.20 × 0.15 m en el borde exterior de la berma, taludes de corte 2H:1V y relleno 1.5H:1V.
* 1NK_I1 dentro de la intersección y ambos cuadrantes: **sección urbana**: calzada 2 × 3.60 m, sardinel con cuneta de 0.60 m
  (Flange 3.60 → Back_Curb 4.20, sardinel de 0.15 m), y hacia afuera cuneta de corte (Ditch_In/Ditch_Out) o talud de relleno.
* 1NK_I1 no tiene corredor fuera de 0+119.66 a 0+233.03, es decir, su sección real no está modelada; la sección urbana es
  una suposición del asistente. Al llegar a 4+240 la berma de 3.00 m y el bordillo del eje mueren de golpe contra un sardinel.

Lo vertical no es el problema: la rasante del eje y el perfil de 1NK_I1 coinciden en el vértice (17.475 m), el eje llega con
−0.80 % y 1NK_I1 pasa con +1.56 %, y la transición de peralte de la última curva termina en 4+007.98, lejos de la intersección.

## 2. Por qué "cumple" y aun así está mal

Los elementos aislados (radios de 550 m con clotoides de 65/75 m para 80 km/h, curvas verticales, peraltes) pueden cumplir
el DG-2018, pero el diseño de intersecciones tiene sus propios criterios (DG-2018, Capítulo V, Sección 502):

* **Perpendicularidad de las trayectorias cuando se cortan**: se busca ~90° y se aconseja no bajar de 60°
  (AASHTO recomienda ≥ 75°, mínimo 60°). Aquí hay 19.7°.
* **Paralelismo cuando convergen o divergen (10° a 15°)** se aplica a convergencias/divergencias canalizadas con isla y carriles
  de cambio de velocidad, no a una intersección con bordes redondeados. Con 19.7° la solución no es ni una cosa ni la otra.
* **Radios de borde según vehículo de diseño**: en vías rurales los bordes de intersección se diseñan con radios del orden de
  15 a 25 m (el radio mínimo de giro de un auto es ~7.3 m). Un fillet de 3.00 m no lo puede recorrer ningún vehículo, y uno
  de 200 m no es un borde de intersección sino un carril paralelo de 69 m.
* Las intersecciones en "Y" de ángulo agudo se corrigen realineando el ramal menor para formar una T (figuras de intersecciones
  de tres ramales del DG-2018 y del AASHTO).

## 3. Evidencia numérica

### 3.1 Geometría horizontal en la zona

| Alineamiento | Dato |
|---|---|
| Eje Vía de evitamiento | L = 4 275.61 m; última tangente desde 4+030.53 (245.08 m), azimut 47.38°; termina sobre 1NK_I1 en 0+184.99 |
| 1NK_I1 | recta 0+000–0+279.15 azimut 207.69°, curva R = 200 m (44.0 m), recta hasta 0+487.37 azimut 195.08° |
| Ángulo entre ejes en el vértice | **19.69°** (Δ del fillet NO = 19.689°, Δ del fillet SO = 160.311°) |
| Cuadrante SO (`Interseccion_3_(1)_-_SO_-_Quadrant`) | 10 m + arco R 3 (8.39 m) + 10 m = 28.39 m; tangencias en borde derecho del eje 4+237.58 y borde oeste de 1NK_I1 0+223.03 |
| Cuadrante NO (`Interseccion_3_(1)_-_NO_-_Quadrant`) | 30 m + arco R 200 (68.73 m) + 30 m = 128.73 m; tangencias en borde izquierdo del eje 4+240.28 y borde oeste de 1NK_I1 0+149.66 |
| Offsets de la intersección sobre el eje | `…-Derecha/Izquierda-3.600 (23)/(24)`: 65.40 m (4+210.22 → fin); además quedan `…-3.300` de 66.24 m de un intento anterior |

### 3.2 Regiones del corredor y secciones (según `CrossSects` del LandXML)

| Región | Estaciones con sección | Sección (códigos de links) |
|---|---|---|
| Corredor "Vía de evitamiento", eje | 0+000 → **4+240.28** (entre 4+238 y 4+240.28 sólo mitad izquierda) | Crown, ETW ±3.60, EPS ±6.60, bordillo 6.60–6.80, Daylight_Sub 7.57, Hinge_Cut/Hinge_Fill, Daylight |
| Corredor "Interseccion 3", 1NK_I1 | 0+119.66 → 0+233.03; entre 0+149.66 y 0+223.03 sólo mitad este | Crown, ETW ±3.60, Flange, Flowline_Gutter, Top_Curb, Back_Curb 4.20, Hinge, Ditch_In/Out, Hinge_Cut, Daylight |
| Corredor "Interseccion 3", cuadrante NO | 0+030 → 0+098.73 (solo el arco) | carril interior + sardinel/cuneta 0.60 + talud exterior (de 3.6 a 8.2 m fuera del sardinel) |
| Corredor "Interseccion 3", cuadrante SO | 0+010 → 0+018.39 (solo el arco) | igual; talud exterior de hasta 9.55 m con corte de 3.1 m |
| Eje entre 4+240.28 y 4+275.61 | **sin secciones** | el área la cubren únicamente las regiones de los cuadrantes |

Superficie `Rasante` (corredor principal) termina en 4+210.28. Superficie `Interseccion_3`: 0 caras visibles.

### 3.3 Solapes entre corredores (distancia del pie de talud al eje de la otra vía)

| Sección | Pie de talud derecho | Distancia al eje de 1NK_I1 | Situación |
|---|---|---|---|
| Eje 4+210.28 | 15.63 m | 7.29 m | en zona de sardinel/talud de 1NK_I1 |
| Eje 4+222 | 15.31 m | 3.65 m | borde de calzada de 1NK_I1 |
| Eje 4+224 → 4+237.58 | 15.4 – 15.8 m | 2.92 → 0.02 → 2.07 m | **dentro de la calzada de 1NK_I1**, cruza su eje en 4+232 |
| 1NK_I1 0+224 | 10.27 m (oeste) | 3.47 m al eje del Eje | dentro de la calzada del eje |
| 1NK_I1 0+226 → 0+233 | 10.3 – 10.5 m | 4.1 → 6.3 m | dentro de berma/bordillo del eje |

### 3.4 Terreno vs rasante (para ubicar cualquier rediseño)

| Eje | 4+040 | 4+060 | 4+080 | 4+100 | 4+120 | 4+140 | 4+160 | 4+200 | 4+240 | 4+275.6 |
|---|---|---|---|---|---|---|---|---|---|---|
| rasante − terreno (m) | +3.2 | +4.8 | +5.5 | +5.4 | +3.6 | +1.3 | +0.1 | −1.0 | −1.4 | +0.2 |

| 1NK_I1 | 0+060 | 0+100 | 0+140 | 0+180 | 0+220 | 0+260 | 0+280 | 0+320 | 0+360 | 0+400 | 0+440 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| perfil − terreno (m) | +1.4 | +1.5 | +0.8 | +0.7 | −2.2 | −4.3 | −4.8 | −3.2 | +0.2 | +0.4 | −1.3 |

Entre los dos ejes, al sur del vértice, hay una loma (terreno 21 a 24 m con rasantes de 17.5 a 19 m). Eso explica los
taludes de corte de 15 m de ancho a la derecha del eje y de 10 m al oeste de 1NK_I1 que se cruzan en la cuña aguda.

### 3.5 Reporte de visibilidad (HTML)

El HTML no contiene la geometría; es la *comprobación de visibilidad* de Civil 3D a lo largo del eje (ojo 1.07 m, objeto 0.15 m,
distancia mínima 128.156 m, superficie `Rasante`). En la zona de la intersección marca violaciones en 4+120 y 4+140 con puntos
de obstrucción **sobre el propio eje** en 4+230.75 (z = 18.50) y 4+237.75 (z = 18.37), es decir 0.66 y 0.59 m por encima de la
rasante (17.84 y 17.78). En el LandXML la superficie `Rasante` ya no llega a esa zona y `Interseccion_3` no tiene caras, así que
esas obstrucciones corresponden a un estado anterior de la superficie en la zona de la intersección: hay que repetir la
comprobación cuando el corredor y la superficie estén reconstruidos. Las demás violaciones (0+560, 1+280, 1+440, 1+940, 2+800,
2+960, 3+300–3+620, 3+840) también reportan obstrucciones sobre el eje a 0.1–0.7 m sobre la rasante, casi todas en curvas
horizontales; conviene revisar con qué superficie se corrió (parece haber puntos por encima de la rasante en los TS/ST y en
las curvas) antes de tocar el perfil.

## 4. Qué hacer

### 4.1 Corregir la geometría del empalme (causa raíz, obligatorio)

Opción recomendada (esquema en `fig_int3_propuesta.png`, es conceptual, no un diseño definitivo):

1. **Vía principal continua**: la vía de evitamiento sigue por 1NK_I1 hacia el NNE con una curva R = 550 m, Le = 75 m
   (misma familia que el resto del eje, V = 80 km/h). Con Δ = 19.69°: T = 133.0 m, L = 264 m, TS en 4+142.6 del eje y
   ST en 0+052 de 1NK_I1. Quedan 112 m de tangente entre el ST de la curva anterior (4+030.53) y el nuevo TS.
2. **Ramal menor en T**: la antigua 1NK_I1 (lado SSO) se realinea para llegar a la vía principal a 90°. Por ejemplo, T en
   4+100: 48 m de recta de aproximación + curva R = 60 m (Δ = 57.7°) empalmando con la última tangente de 1NK_I1 en 0+412.
   Variante más cerca de la rasante natural: T en 4+120 con R = 50 m (41 m de recta, empalme en 0+383).
   Entre 0+052 y 0+412 (≈ 360 m) la 1NK_I1 actual quedaría fuera de servicio.
3. Con la T a 90° el asistente de Civil 3D vuelve a funcionar: ángulo correcto, dos cuadrantes normales, radios de borde
   de 15 a 25 m según vehículo de diseño.

Condicionantes a resolver en el diseño definitivo: entre 4+040 y 4+120 el eje va en relleno de 3 a 5.5 m, por lo que la T
debe ubicarse/perfilarse con cuidado (o desplazar la curva principal con un radio algo menor, por ejemplo R = 400 m da
TS ≈ 4+168, para poder poner la T más cerca de 4+140 donde el relleno es de 1.3 m); el ramal menor atraviesa la loma
(terreno 19 a 24 m) y necesitará cortes; hay que verificar el triángulo de visibilidad de la T.

Alternativas: (a) doblar el final del eje hacia la derecha para cortar 1NK_I1 a ≥ 75° manteniendo 1NK_I1 intacta,
pero entonces el tráfico de paso del evitamiento tendría que girar 90° y la T caería donde 1NK_I1 va en corte de 2 a 5 m;
(b) mantener la "Y" y diseñarla como convergencia/divergencia canalizada (isla triangular, carriles de cambio de velocidad),
que no se puede hacer con *Create Intersection*, sólo con corredor manual, líneas características y explanación.

### 4.2 Parámetros del asistente (una vez que sea una T)

* Radios de los cuadrantes: 15–25 m (vehículo de diseño), nunca 3 m ni 200 m.
* Anchos de carril iguales en ambas vías (3.60 m); eliminar los offsets de 3.30 m del intento anterior.
* Ensanches (*widening*) desactivados salvo que se necesiten carriles de giro.

### 4.3 Ensamblajes (segunda causa)

* Usar la **misma familia de sección** en las dos vías dentro de la intersección. Si las vías son rurales con berma, los
  ensamblajes de "vía principal", "vía secundaria" y "cuadrantes" deben ser carril + berma + talud, no carril + sardinel/cuneta +
  cuneta de corte. Dentro del área pavimentada de la intersección el ensamblaje de cuadrante no debe tener talud ni cuneta,
  sólo el carril con destino (*target*) al eje de la vía principal y la berma hacia afuera.
* Modelar la sección real de 1NK_I1 con un corredor propio fuera de la intersección (hoy no existe), de modo que las
  secciones de ambas vías coincidan en los puntos de tangencia.
* Revisar el bordillo de 0.15 m en el borde exterior de la berma de 3.00 m del eje: en una vía de 80 km/h sin sección urbana
  es inusual y es lo que produce el "escalón" visible donde termina el corredor principal.

### 4.4 Limpieza del modelo y reconstrucción

* Borrar los objetos duplicados del primer intento: `Interseccion 3 - SO - Quadrant`, `Eje Via de evitamiento-Derecha/Izquierda-3.300`
  y sus perfiles; conservar sólo una intersección.
* Hacer que la región del corredor principal termine exactamente donde empiezan las regiones de la intersección (o meter la
  intersección en el mismo corredor) para que no se superpongan taludes; poner la superficie `Topografia` como destino de
  todos los taludes y reconstruir.
* Añadir la extensión del corredor como contorno exterior de la superficie de intersección (hoy tiene 0 caras) y volver a
  correr la comprobación de visibilidad.

### 4.5 Compatibilidad de la nueva curva con el trazo existente

* Todo lo anterior al ST de la última curva actual (4+030.53) queda intacto: las cuatro curvas con espirales, sus peraltes
  (la última transición termina en 4+007.98) y el perfil hasta 4+055.6.
* La nueva curva gira a la izquierda y la anterior a la derecha, así que forman una "S". El DG-2018 (Tabla 302.01) pide una
  tangente mínima entre curvas en S de 1.39·V = 111.2 m a 80 km/h. Con R = 550 m y Le = 75 m la tangente es de 112.1 m
  (4+030.53 a 4+142.60): cumple, con poco margen. Entre el fin del peralte anterior (4+007.98) y el inicio de la nueva
  transición (≈ 4+165) quedan 157 m de bombeo normal.
* Si se quiere más margen o mover la T más al norte, basta con bajar el radio de la nueva curva (todos cumplen R mín = 229 m
  para 80 km/h):

| R (m) | T (m) | TS en el eje | tangente desde 4+030.53 | ST sobre 1NK_I1 | longitud total de curva |
|---|---|---|---|---|---|
| 550 | 133.0 | 4+142.60 | 112.1 m | 0+051.98 | 264.0 m |
| 500 | 124.3 | 4+151.27 | 120.7 m | 0+060.65 | 246.8 m |
| 450 | 115.7 | 4+159.94 | 129.4 m | 0+069.32 | 229.6 m |
| 400 | 107.0 | 4+168.61 | 138.1 m | 0+077.99 | 212.5 m |

* En perfil, el PVI de 4+141.81 (18.545 m, L = 172.39 m) se conserva; solo cambia su pendiente de salida. Propuesta inicial:
  PVI 4+380.00 a 20.373 m (+0.767 %) y fin en 4+458.58 a 21.037 m (+0.845 %, la pendiente con la que 1NK_I1 llega a su
  0+000). En 4+141.81 el cambio de pendiente pasa a 0.90 % y con L = 172.39 m resulta K = 192, muy por encima del mínimo.
  Ojo: entre 1NK_I1 0+031 y 0+078 la vía existente baja al −6.25 %; la nueva rasante queda ≈ 1 m por encima de la vía
  existente en 0+052, así que ese tramo de 1NK_I1 se reconstruye y el empalme definitivo debe verificarse con el
  levantamiento de la vía más allá de 0+000.
* Ramal: perfil 0+000 = rasante del eje en 4+100 (≈ 17.80 m con la rasante modificada), 0+108.3 a 20.01 m (cresta, L = 30 m)
  y 0+183.3 a 19.16 m; pendientes +2.0 % y −1.1 %.

### 4.6 Por qué los ensamblajes propios "empeoraban" la intersección

El asistente no mira las características de la sección (anchos, espesores) sino el tipo de subensamblaje y sus destinos:
los carriles de sus ensamblajes por defecto son `LaneSuperelevationAOR` con destino de anchura hacia las alineaciones de
desfase y, en los cuadrantes, hacia el eje de la vía principal; además usa un juego de siete ensamblajes (completo, parcial
con talud a un lado, media sección, cuadrante) para que cada región tenga talud solo hacia afuera. Al poner un ensamblaje
"completo" propio en todas las regiones, los carriles no se estiran hasta la vía principal, los taludes y el bordillo
aparecen dentro del área de la intersección y las regiones se cruzan. Y con 19.7° ningún ensamblaje iba a verse bien.
El archivo `prompt-agente-local.md` incluye cómo derivar el juego rural a partir del ensamblaje propio.

## 5. Prompt para el agente local

`prompt-agente-local.md` contiene, fase por fase y con puntos de control, los pasos para ejecutar esta corrección en
Civil 3D (limpieza, prolongación del eje, ramal, perfiles, ensamblajes, intersección en T, corredor y comprobaciones).

## 6. Figuras

* `fig_int3_planta.png`: planta reconstruida desde el LandXML (links de sección de cada región, alineamientos, TIN de la
  superficie `Rasante`, puntos de `Interseccion_3`, curvas de nivel) con los problemas anotados.
* `fig_int3_general.png`: vista general de los últimos 300 m del eje y de 1NK_I1.
* `fig_int3_propuesta.png`: esquema conceptual "Y → vía continua + T a 90°".

## 7. Cómo se hizo (reproducible)

Scripts en `scripts/` (Python 3 con `lxml`, `numpy`, `matplotlib`). El LandXML está en Git LFS; hay que descargarlo primero.

```
python3 scripts/summary.py  via.xml          # censo de alineamientos, perfiles, secciones y superficies
python3 scripts/extract.py  via.xml          # extrae alineamientos, corredores, secciones y superficies a archivos pequeños
python3 scripts/secsum.py                    # resumen por estación de los ensamblajes (códigos y links Top)
python3 scripts/plot_plan.py --plot          # planta reconstruida + tabla de solapes entre corredores
python3 scripts/concept.py                   # geometría del esquema conceptual y figura de propuesta
python3 scripts/terreno.py                   # terreno natural vs rasante a lo largo de ambos ejes
```
