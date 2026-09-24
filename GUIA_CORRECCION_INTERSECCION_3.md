# Guía paso a paso: corrección de la unión en la Intersección 3

Proyecto: `ANDY RODRIGO BAYONA ANTÓN_Autodesk Civil 3D.dwg` (Civil 3D 2027).
Intersección 3 = confluencia del Eje_Via_de_evitamiento (VE) en la carretera 1NK_I1.

Datos que vas a necesitar (sacados del LandXML del proyecto):

| Dato | Valor |
|---|---|
| Fin de la VE | 4+275.61, sobre la 1NK_I1 en 0+185.00 |
| Ángulo entre ejes | 19.7° |
| Fin de la superficie Rasante | 4+210.28 |
| Regiones del eje VE dentro del corredor "Interseccion 3" | 4+210.28 a 4+237.58 (sección completa VE) y 4+237.58 a 4+240.28 (media sección izquierda VE) |
| Regiones de la 1NK_I1 | 0+119.66 a 0+149.66, 0+149.66 a 0+223.04, 0+223.04 a 0+233.04 |
| Acuerdo NO | R 200 m, tangencias 1NK 0+149.66 y VE 4+240.28 |
| Acuerdo SO (nariz) | R 3.00 m, giro 160.3°, tangencias VE 4+237.58 y 1NK 0+223.04. Regiones 0+010.00 a 0+014.20 y 0+014.20 a 0+018.39 |
| Nariz teórica (cruce de bordes) | VE 4+254.90 |
| Cruce del eje VE con el borde NO de la 1NK | VE 4+264.90 |
| Alineaciones y perfiles objetivo | `1NK_I1-Derecha-3.600` y su perfil `1NK_I1 - -2.000% (35)` |

Orden de las fases: 0, 1, 2, 3, 4. La 5 y la 6 son opcionales. No cambies el orden de la 2 y la 3.

---

## Fase 0. Antes de empezar (5 min)

1. Guarda una copia del DWG con otro nombre, por ejemplo `..._antes_int3.dwg`.
2. En el Prospector, en `Corredores`, clic derecho sobre `Interseccion 3` y desactiva `Reconstruir - Automático`. Haz lo mismo con `Vía de evitamiento`. Así cada cambio no dispara una reconstrucción de minutos. Reconstruirás a mano al final de cada fase.
3. Identifica tus ensamblajes actuales: Prospector, `Corredores`, `Vía de evitamiento`, clic derecho, `Propiedades`, pestaña `Parámetros`. En la columna `Ensamblaje` verás el nombre de tu sección completa de la VE. Haz lo mismo en `Interseccion 3` para ver el nombre de tu media sección izquierda. Apúntalos.

---

## Fase 1. Ensamblajes (30 a 40 min)

Regla general: todo se hace copiando tus ensamblajes de la VE, para que los códigos (Crown, ETW, EPS, Hinge, Daylight, Top, Datum) y las capas sean idénticos.

Cómo copiar y renombrar un ensamblaje:
- Selecciona el ensamblaje completo (clic en la línea vertical del eje del ensamblaje), `Ctrl+C`, `Ctrl+V` y colócalo a un lado.
- Selecciona la copia, clic derecho, `Propiedades de ensamblaje`, pestaña `Información`, cambia `Nombre`.

Cómo borrar un subensamblaje: clic sobre él y `Supr`. Después comprueba que el resto sigue "colgado" del punto correcto. Si algo queda suelto, selecciónalo, clic derecho, `Mover a` y pincha el marcador circular del punto al que debe unirse.

### 1.1 `1NK - Sección completa`
Copia tu sección completa de la VE. Borra el subensamblaje `Bordillo` de cada lado. Queda: carril 3.60 + berma 3.00 + talud, a ambos lados. Comprueba que el talud sigue unido al punto exterior de la berma.

### 1.2 `1NK - Media sección - Talud izquierda`
Copia `1NK - Sección completa`. Borra la berma y el talud del lado DERECHO. No borres el carril derecho: las medias secciones llevan los dos carriles.

### 1.3 `1NK - Media sección - Talud derecha`
Copia `1NK - Sección completa` y borra la berma y el talud del lado IZQUIERDO. En esta intersección no se usa, pero el asistente pide asignarla y la necesitarás en las intersecciones 1 y 2.

### 1.4 `Acuerdo`
Ensamblaje nuevo: cinta `Inicio`, panel `Crear diseño`, `Ensamblaje`, `Crear ensamblaje`. Nombre `Acuerdo`. Pincha un punto libre en pantalla.
Abre las paletas (`Ctrl+3`) y añade en este orden:
1. El mismo carril que usas en la VE (`CarrilPeralteAOR`, en inglés LaneSuperelevationAOR). En la ventana `Propiedades` antes de colocarlo: `Lado = Izquierda`, `Anchura = 3.60`, pendiente `-2.00 %`, mismos espesores de capas que tu carril de la VE. Pincha el marcador del eje del ensamblaje.
2. La misma berma que usas en la VE. `Lado = Derecha`, `Anchura = 3.00`. Pincha OTRA VEZ el marcador del eje del ensamblaje, no el del carril. En el acuerdo la berma nace en el propio eje, porque ese eje es el borde de calzada.
3. El mismo talud que usas en la VE. `Lado = Derecha`. Pincha el marcador exterior de la berma, el mismo punto donde cuelga el talud en tu sección de la VE.

Resultado: carril a la izquierda del eje, berma y talud a la derecha. Si quieres que el bordillo de la VE continúe por el acuerdo NO hasta la 1NK, añade también el `Bordillo` sobre el punto exterior de la berma, igual que en la VE.

### 1.5 `Acuerdo - solo exterior`
Copia `Acuerdo` y borra el carril. Queda solo berma + talud a la derecha. Es para la nariz SO.

### 1.6 `VE - Carril derecho a la 1NK`
Ensamblaje nuevo con un único `CarrilPeralteAOR`, `Lado = Derecha`, `Anchura = 3.60`, mismos espesores. Nada más.

### 1.7 Corregir tu media sección izquierda de la VE
Abre tu ensamblaje de media sección izquierda (el que va de 4+237.58 a 4+240.28). Añádele un `CarrilPeralteAOR` con `Lado = Derecha`, `Anchura = 3.60`, sobre el marcador del eje. Ahora mismo no lo tiene y por eso el carril derecho de ese tramo lo estaba dibujando la nariz.

### Comprobación de la fase 1
Para cada ensamblaje: clic derecho, `Propiedades de ensamblaje`, pestaña `Construcción`. Debe aparecer el árbol con los subensamblajes y, en cada uno, `Lado` correcto y anchuras 3.60 y 3.00. En `Acuerdo` el carril tiene que estar a la izquierda.

---

## Fase 2. Asignar los ensamblajes a la intersección (10 min)

1. Selecciona el marcador de la intersección (el círculo con la etiqueta `Interseccion 3 (1)`). En la cinta contextual `Intersección` pulsa `Propiedades de intersección`.
2. Pestaña `Regiones de corredor`. Es una tabla con `Tipo de sección de corredor` y `Ensamblaje`. Asigna:

| Tipo de sección | Ensamblaje |
|---|---|
| Sección completa de carretera principal | `1NK - Sección completa` |
| Media sección de carretera principal - Talud izquierda | `1NK - Media sección - Talud izquierda` |
| Media sección de carretera principal - Talud derecha | `1NK - Media sección - Talud derecha` |
| Sección completa de carretera secundaria | tu sección completa de la VE (ya está) |
| Media sección de carretera secundaria - Talud izquierda | tu media sección izquierda de la VE (ya está, ahora con carril derecho) |
| Media sección de carretera secundaria - Talud derecha | tu media sección derecha de la VE si la tienes; si no, la izquierda. Aquí no se usa |
| Acuerdos de bordillo | `Acuerdo` |

   Los nombres de los tipos pueden variar un poco según la traducción, pero son esos siete.
3. Pulsa `Guardar como conjunto` y guarda un XML, por ejemplo `Conjunto VE-1NK.xml`. Te servirá para las intersecciones 1 y 2 con `Importar conjunto`.
4. Opcional pero recomendado (parte vertical, ver fase 5): en la pestaña de parámetros de desfase, en `Carretera secundaria`, `Desfase derecho`, pon `Pendiente transversal = +2.00 %`. Deja `-2.00 %` en el resto. Con esto el borde derecho de la VE sube 0.144 m dentro de la intersección y la nariz queda a la cota del borde de la 1NK. Si lo haces, tienes que completar la fase 5; si no, no lo toques.
5. `Aceptar`. Si Civil 3D pregunta si quieres volver a crear las regiones, di que sí. Si no pregunta, con la intersección seleccionada pulsa en la cinta `Volver a crear regiones de corredor` y elige el corredor `Interseccion 3`.
6. Prospector, `Corredores`, `Interseccion 3`, clic derecho, `Reconstruir`.

### Comprobación de la fase 2
La 1NK y el arco NO deben mostrar berma de 3 m y talud, sin las líneas rojas de la cuneta triangular. El borde exterior ya no salta en 4+240.28. La nariz SO seguirá con el bulbo: es normal, se arregla en la fase 3.

Si en la tabla no aparece `Acuerdos de bordillo` o los tipos están en gris, la intersección se creó sin la opción `Crear corredores en el área de intersección`. En ese caso, con la intersección seleccionada, pulsa `Crear corredores en el área de intersección`, marca `Añadir a un corredor existente: Interseccion 3` y usa el conjunto XML que guardaste.

---

## Fase 3. Nariz y confluencia, en el corredor (15 min)

Hazla siempre DESPUÉS de la fase 2. `Volver a crear regiones de corredor` borra estos cambios manuales; si algún día lo vuelves a ejecutar, repite esta fase.

1. Prospector, `Corredores`, `Interseccion 3`, clic derecho, `Propiedades`, pestaña `Parámetros`. Despliega las líneas base.

2. Línea base `Interseccion 3 (1) - SO - Quadrant`. Tiene dos regiones, 0+010.00 a 0+014.20 y 0+014.20 a 0+018.39.
   - Columna `Ensamblaje`: en las dos elige `Acuerdo - solo exterior`.
   - Columna `Frecuencia`, botón `...`: `A lo largo de curvas = 0.500`, `En puntos de geometría horizontal = Sí`.

3. Línea base `Eje_Via_de_evitamiento`, región 4+237.58 a 4+240.28 (tu media sección izquierda).
   - Columna `Objetivo`, botón `...`. Se abre `Asignación de objetivos`.
   - En `Objetivos de anchura o desfase`, fila del carril DERECHO (`CarrilPeralteAOR - (Derecha)` o el nombre que tenga): pulsa en `<Ninguno>`, `Tipo de objeto = Alineaciones`, selecciona `1NK_I1-Derecha-3.600`, `Aceptar`.
   - En `Objetivos de talud o elevación`, misma fila: `Tipo de objeto = Perfiles`, alineación `1NK_I1-Derecha-3.600`, perfil `1NK_I1 - -2.000% (35)`, `Aceptar`.
   - El carril izquierdo se deja como está.

4. Nueva región en la misma línea base. Clic derecho sobre `Eje_Via_de_evitamiento`, `Añadir región`. Nombre `Carril derecho confluencia`, ensamblaje `VE - Carril derecho a la 1NK`. En la tabla pon `Estación inicial = 4+240.28` y `Estación final = 4+264.90`. Frecuencia 2.000 en tangentes, 1.000 en curvas, `En puntos de geometría horizontal = Sí`. Objetivos: los mismos del punto 3 (alineación `1NK_I1-Derecha-3.600`, perfil `(35)`).
   - Si el asistente hubiera dejado alguna región de la VE más allá de 4+240.28, bórrala o acórtala para que no se solape.
   - Del 4+264.90 al 4+275.61 no debe haber ninguna región en este eje. Ese tramo ya lo pavimentan el carril NO de la 1NK y el acuerdo NO.

5. Botón `Establecer todos los objetivos` (arriba de la pestaña): en `Objetivos de superficie` todos los taludes apuntan a `Topografia`. Las bermas no llevan objetivo de anchura.

6. `Aceptar` y `Reconstruir` el corredor `Interseccion 3`.

### Comprobación de la fase 3
El bulbo desaparece. Entre 4+237.58 y 4+254.90 el carril derecho de la VE se abre hasta el borde de la 1NK y después se estrecha hasta cero en 4+264.90. Alrededor del arco de 3 m solo hay berma y talud. Pasa el cursor por las secciones: la ayuda emergente debe decir `Carril derecho confluencia` en 4+250.

---

## Fase 4. Superficies (10 min)

1. Propiedades del corredor `Interseccion 3`, pestaña `Superficies`. La superficie `Interseccion_3` debe tener como único código de vínculo `Top`. Si aparece otro, quítalo.
2. Pestaña `Contornos`: clic derecho sobre `Interseccion_3`, `Contorno de corredor`, `Añadir automáticamente`, `Daylight`. Tipo `Exterior`. Si no te deja el automático, usa `Añadir de contornos del corredor` y elige `Exterior`.
3. `Aceptar`. Prospector, `Superficies`, `Interseccion_3`, clic derecho, `Reconstruir`. Después `Rasante`, `Reconstruir`.
4. Opcional, una única superficie para el final: crea `Terreno final` (`Crear superficie`), y en `Definición`, `Editar`, `Pegar superficie`, pega en este orden: `Topografia`, después `Rasante`, después `Interseccion_3`. La última pegada manda.
5. Comprobación: `Ver`, `Visor de objetos`, mira la zona en 3D. Y `Cortar sección rápida` en 4+238 y en 4+250: la calzada debe verse continua, sin escalones en los bordes.

Vuelve a activar `Reconstruir - Automático` en los dos corredores si lo prefieres.

---

## Fase 5 (opcional). Vertical: un solo plano en la confluencia (20 min)

Solo si activaste el +2.00 % en la fase 2, punto 4. Objetivo: que el carril derecho de la VE pase de -2 % a +2 % entre 4+183.00 y 4+210.28, dentro del corredor `Vía de evitamiento`, para que en 4+210.28 empalme con el perfil de desfase derecho de la intersección.

Cotas de la rasante de la VE en ese tramo (calculadas de tu perfil, que ahí va en curva vertical):

| Estación | Rasante en el eje | Borde derecho buscado |
|---|---|---|
| 4+183.00 | 18.071 | 17.999 (rasante - 0.072) |
| 4+196.64 | 18.036 | 18.036 (rasante + 0.000) |
| 4+210.28 | 17.975 | 18.047 (rasante + 0.072) |

1. Dibuja una línea característica de tres vértices sobre el borde derecho de la VE (desfase +3.60 del eje) en esas tres estaciones, con esas tres cotas. La forma más cómoda: `Inicio`, `Línea característica`, `Crear línea característica`, dando los puntos con `Estación y desfase` sobre el eje `Eje_Via_de_evitamiento` y escribiendo la cota de cada vértice. Ponle nombre `VE borde derecho transición`.
2. Propiedades del corredor `Vía de evitamiento`, `Parámetros`. Divide la última región en dos: la nueva va de 4+183.00 a 4+210.28 con el mismo ensamblaje de sección completa (clic derecho sobre la región, `Dividir región`, estación 4+183.00).
3. En la región 4+183.00 a 4+210.28, `Objetivo`, `Objetivos de talud o elevación`, fila del carril derecho: `Tipo de objeto = Líneas características, líneas de rotura de topografía y polilíneas 3D`, selecciona `VE borde derecho transición`.
4. `Aceptar`, `Reconstruir` los dos corredores y las superficies.

Si tu versión permite crear el perfil de desfase con tabla de pendientes transversales por estación (`Crear perfil de desfase` sobre `Límite de calzada - Derecha`, tabla -2 % en 4+183 y +2 % en 4+210.28), puedes usar ese perfil como objetivo de elevación en vez de la línea característica.

Resultado: toda la zona entre el eje de la 1NK y el arco NO es un plano al 2 %, sin la "V" en la línea de unión.

---

## Fase 6 (opcional). Limpieza (5 min)

En el Prospector, `Alineaciones`:
- `Alineaciones de acuerdo de bordillo`: borra `Interseccion 3 - SO - Quadrant` (sin el "(1)") y su perfil. Es el resto del primer intento.
- `Alineaciones de desfase`: borra `Eje Via de evitamiento-Derecha-3.300`, `Eje Via de evitamiento-Izquierda-3.300` y sus perfiles `(20)` y `(21)`.
- Decide entre `1NK_I1_ Calzada derecha / Izquierda` y `1NK_I1-Derecha / Izquierda-3.600`. El corredor debe apuntar a las de 3.600.
- La 1NK fuera del tramo 0+119.66 a 0+233.04 no tiene corredor. Si lo necesitas, amplía las regiones de la línea base `1NK_I1` con `1NK - Sección completa`.

Después de todo, vuelve a lanzar la comprobación de visibilidad: las violaciones de 4+120 y 4+140 venían de un punto en 4+231 sobre el propio eje, 0.67 m por encima de la rasante, que ya no debería existir.
