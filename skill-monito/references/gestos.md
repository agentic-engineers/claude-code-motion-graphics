# Catálogo de gestos construidos

Todas las piezas viven en `editor/projects/monito-intro-ci/compositions/` y sus
renders en `renders/`. Antes de inventar un gesto nuevo, revisar si uno de estos
se adapta — y al crear uno nuevo, agregarlo a esta lista.

| Gesto | Pieza de referencia | Qué hace |
|---|---|---|
| Ciclo de vida completo | `index.html` (+ raíz `../index.html`) | Tipea en el laptop, check verde, se disuelve de abajo hacia arriba (bracitos sobreviven 0.2s), puf de partículas, renace con pop + squash |
| Ciclo sincronizado a frase | `b1b-ciclo.html` | El mismo ciclo pero con cada beat clavado a palabras habladas ("un minuto"→check, "se muere"→disolución, "trabajo de nuevo"→barras vuelven, "vuelve a nacer"→pop) |
| Parpadeo de existencia | `b1c-parpadeo.html` | Existe/no-existe en 3 ventanas (pattern interrupt); las barras de código SOLO avanzan mientras existe; check con la silla vacía. Nació porque repetir la disolución por 3ª vez era fuga |
| Fantasma (medio disuelto) | `b1c-fantasma.html` | Tecleando con la mitad inferior deshaciéndose en equilibrio (frente de máscara oscilando + goteo de partículas). La imagen de la miniatura, animada |
| Rótulo pixel con palabras | `b1c-efimero.html`, `b2-palabras.html` | Texto pixel-font palabra a palabra al golpe de voz, estelas de partículas como flechas, disolución + cursor de terminal parpadeando |
| Mini-monitos actuando | `b2-palabras.html` (v2) | Wrappers escalados 0.42 bajo cada palabra: uno nace, uno teclea, uno se disuelve |
| Servidor que se desintegra | `b1d-servidor.html` | Rack pixel gris con lucecitas parpadeantes + $ flotando; el rack se disuelve y el $ hace puf en las palabras correspondientes; saltito final |
| Documento con check | `b1e-documentada.html` fase A | Página paper con líneas de texto ink; check verde pop en la esquina |
| Fila apagados/encendido | `b1e-documentada.html` fase B | 8 minis grises en cascada; solo UNO se enciende salmón (capa duplicada con opacity) y teclea — "muy pocas personas lo conocen" |
| Dormido sobre la barra | `b4-barra24.html` | Mini monito con ojos cerrados (rects de 5px) + zZZ pixel-font cíclico, parado sobre la barra de 24 horas |
| Barra de 24 horas | `b4-barra24.html` | 24 celdas-hora en cascada, celda de trabajo iluminada, medidor $ llenándose parejo (sin cifras), tachado, desintegración total, sobrevive la celda con check |
| Trae un número | `b5-n1/n2/n3.html` | Mini monito pop con dígito pixel sobre la cabeza; se disuelve y deja el número; el número se disuelve después |
| Dígitos 1-2-3 anticipo | `b1f-tres.html` | Monito con los tres dígitos haciendo pop escalonado arriba |
| Panel de evidencia lateral | `ev1-actions.html`, `ev2-commits.html`, `ev3-post.html` | Captura real en panel a la derecha (x 1080-1830 del viewBox), Nicolás sigue en cámara al lado. Pop de entrada, punch-in DENTRO del marco, muerte en partículas. NADA dibujado encima de la imagen |
| Interrogante de lo indefinido | `b3-tareas.html` fase A | Monito con un "?" pixel dibujado a mano (grilla 5×7, la pixel-font no trae el glifo); el "?" colapsa cuando lo indefinido se vuelve concreto |
| Enumeración en tres tareas | `b3-tareas.html` fase B | Tres minis nacen uno por cada cosa que él enumera; cada uno con su documento. El segundo ESCRIBE (líneas que se llenan), el tercero PUBLICA (su doc sale volando y se disuelve) |
| Cafecito (pattern interrupt) | `b3-tareas.html` fase C | Taza pixel con vapor cíclico; los monitos DEJAN de teclear mientras ella está. Rompe la monotonía de la enumeración |
| Entrega de objeto entre piezas | `b3-tareas.html` → `b4-barra24-v2.html` | Una pieza termina dejando un elemento en coordenadas exactas y la siguiente nace con ese mismo elemento ya en pantalla: match cut invisible en el corte. Acá la celda de trabajo en x=762 y=790 |
| Quedarse quieto (el que calla) | `b6-callarse.html` | Deja de teclear pero PARPADEA: callado no es apagado. Su hoja se congela a media línea, no en una línea completa |
| Sepultado por su producción | `b6-callarse.html` | El que produce sin parar teclea cada vez más rápido (7→13 Hz) mientras una pila de hojas se apila encima hasta taparlo; la pila colapsa y el que calló queda intacto |
| Hilo que engancha nodos | `b5-hilo.html` | Una curva de cuadraditos pixel llega suelta, se interpola hasta enganchar tres nodos, se apaga a 0.28 de opacidad ("yo no se lo vi") y se enciende con un pulso que sale del centro |
| Bloque fijo contra torre | `b5-suscripcion.html` | Izquierda: un bloque que nunca cambia de tamaño. Derecha: una torre que se apila cada vez más rápido y se sale del marco, se tacha y colapsa. Compara costos SIN cifras inventadas |
| Rótulo que nace entre las manos | `b1c-efimero-v2.html` | Cuando Nicolás abre las manos en cámara, el rótulo pixel nace entre ellas y se despliega desde el centro hacia afuera, como si el gesto lo abriera. Hace lo que nombra: se evapora mientras todavía lo está diciendo. Reemplazó al monito grande, que ahí iba por tercera vez igual |
| Torre improvisada que colapsa | `b1g-sin-truco.html` | Bloques apilados torcidos, con el desalineo creciendo hacia arriba; se tambalea con una oscilación que crece y colapsa en escombros. Niega "lo armé yo" sin una sola palabra |
| Feed que frena | `b5-lectura.html` | Titulares grises corriendo hacia arriba dentro de una ventana recortada; el monito lee con los ojos achicados y, en la palabra clave, el flujo FRENA y el titular que queda centrado se enciende salmón |
| Sello que cae y aplasta | `b5-evidencia.html` | Las líneas del documento se van marcando mientras habla y el check verde CAE de golpe (no hace pop) con squash del papel y salpicadura de partículas. Nació para que el tercer check verde del video no repitiera el mismo gesto |
| El sistema que se ensambla | `b7-patron.html` | Seis módulos, uno por cada cosa que el espectador ya vio en la intro, vuelan desde fuera de cuadro y encajan en fila con un golpe seco; cuando entra el último, un marco los cierra. La única pieza que muestra SISTEMA y no gesto |
| Distintivo por rol (cascos) | `b3-tareas-cascos.html` (prueba) | Casco de minero con lámpara, gorra con visera y casco con alitas, en gris con detalles paper. Regla aprendida: el casco va SOBRE la cabeza (el cuerpo empieza en y=667), NUNCA encima de los ojos — la primera versión tapaba la mirada y el personaje perdía la vida. Usar solo donde el guion nombra un rol |
| Nacer desde partículas | `b1a-dos-semanas.html` | La disolución canónica corrida al revés: el frente de máscara BAJA revelando el cuerpo, y las partículas caen HACIA él en vez de salir. A mitad de camino el personaje es la imagen de la miniatura (cuerpo sí, patas no), así que el primer segundo del video engancha con ella sin gastar el ciclo de vida |
| Acumulado en casillas | `b1a-dos-semanas.html` | Dos filas de siete casillas = dos semanas, literal, una fila por semana; se llenan día a día al ritmo de la voz. Muestra volumen de trabajo sin escribir una cifra, y usa el mismo vocabulario que la barra de 24 horas |
| Probar automatizaciones | `b3-tareas-v2.html` fase A | El monito teclea y sobre su cabeza se turnan seis objetos, uno por palabra (documento, sobre, barras, reloj, check, interrogante), cada uno con pop y colapso. Reemplazó a un monito quieto con un solo "?" que daba dos eventos en 4.9 segundos |
| Saltar del hombro a la mesa | `claude-code-motion-graphics/compositions/m1-salto.html` (lib2 `motion` jump) | Nace en el hombro 3 s y SALTA a la mesa con estirón en el aire y squash al aterrizar, salpicadura de partículas. La mesa pasa a ser el escenario |
| Multiplicarse | `m1-salto.html` | Una cascada de minis (escala 0.22) nace hacia afuera desde el protagonista hasta llenar el borde de la mesa; después saltan uno a uno a las ranuras de una tira de timeline |
| Ola que borra | `m1-salto.html` (lib2 `waveMask`) | Máscara de frente vertical que avanza de izquierda a derecha borrando tira y multitud, con partículas en el frente; el protagonista salta cuando la ola pasa por debajo |
| Cargar y cruzar la mesa | `m2-carga.html` | Levanta la tarjeta sobre la cabeza (brazos `up`) y cruza la mesa a saltitos (hop con n saltos); la carga sigue la cabeza |
| Dormir junto a la taza | `m2-carga.html` (lib2 `zzz`) | Ojos cerrados (rect de 6 px), cuerpo a 0.8 respirando, zZZ cíclico de tres tamaños; despierta con susto (salto corto) |
| Arrugar y patear | `m2-carga.html` | La tarjeta "prompt" rota 560° y se encoge a bolita + puf; la "plantilla" sale pateada con gravedad y rotación hasta salir del cuadro por abajo |
| Onda de voz | `m3-sistema.html` | Barras pixel a lo largo de la mesa con un pulso que viaja; al llegar se vuelve un mini que hace pop |
| Caer sobre la palabra | `m3-sistema.html` | Agacharse (anticipación), salto alto y aterrizaje exacto sobre un rótulo que se aplasta (sy 0.55) con salpicadura |
| Frenar en el borde del cuadro | `m3-sistema.html` | Camina hasta que el cuerpo toca x=1915 y se tambalea (rotación alrededor de los pies con amplitud en campana, brazos `flail`, ojos achicados), recupera con squash |
| Entrar y salir de verdad | `m3-sistema.html` (lib2 `seedGatherParts`) | Disolución canónica y nacimiento desde partículas que convergen, uno tras otro, en las palabras "entra" / "se va" |
| Editor en su laptop | `m4-editor.html` | Laptop pixel al lado del real: ventanas que se abren, rombo arrastrado por una guía, barra de exportar que llena, ida y vuelta a la tira, bloque empujado de a 14 px hasta calzar en la ranura (flash) |
| Sepultados por hojas | `m4-editor.html` | Multitud gris tecleando a 11 Hz; pilas de hojas (rects paper) suben con pop hasta taparlos; todo colapsa en ola con partículas que caen |
| Tubería que se ensambla | `m5-tuberia.html` | Seis módulos vuelan desde fuera con backOut y encajan con squash; LEDs que recorren la tubería; minis grises entran por una boca y salen salmón por la otra, cada uno con una acción distinta |
| Plegarse en archivo | `m5-tuberia.html` | scaleX 1→0 del personaje y 0→1 de un documento en el mismo punto (y vuelta). "El personaje es un archivo", literal |
| Objetos sobre la cabeza por turno | `m6-cierre.html` | Reloj con manecillas, disco, bucle que gira; uno por palabra, con pop y colapso |
| Pisar el botón | `m6-cierre.html` | Salta sobre un botón paper que se hunde a la mitad y cambia a salmón; salpicadura al pisar |
| Polvo de transición | `polvo-transicion.html` | 0.7s de partículas cruzando el corte entre bloques (se coloca centrado en el corte, mismo render reutilizado N veces) |

## Notas de dirección

- **Si hay mesa en cuadro, la mesa es el escenario (1-nov-2026)**: el personaje en el hombro
  repitiendo la misma puesta cuatro veces fue rechazado ("no siempre el mismo... más wow").
  Cada beat de voz una mecánica distinta; interactuar con lo real (taza, laptop, borde del
  cuadro); actuar lo que había que leer. Librería: `claude-code-motion-graphics/lib2.js`.

- **Los cascos diferencian pero no explican**: a escala 0.42 se lee "estos son
  distintos oficios", no "este lee y este publica". Si hace falta comunicar el
  rol exacto, el objeto que el monito manipula (su documento) lo dice mejor.
- **El b-roll de pantalla nunca va a pantalla completa**: panel lateral y Nicolás
  en cámara al lado (regla dada por él el 31-ago-2026). Y el bloque de evidencia
  no lleva monito encima: la prueba se lee 100% real.
- **Si un tramo "se ve vacío", revisar el transform del clip antes de dar por
  hecho que falta contenido**: `b2-palabras-v2` estaba colocada y habilitada pero
  con un Tilt que la empujaba entera fuera de cuadro. Ojo con los dos getters de
  Resolve: `GetProperty()` (dict) y `GetProperty("Tilt")` devuelven valores en
  escalas distintas para la misma propiedad; el que manda es lo que se ve.
- **AppendToTimeline deja 1 frame descubierto**: pasando `endFrame = frames-1`,
  Resolve reporta el clip como `start -> end` con `end` EXCLUSIVO, así que el
  frame `end` queda sin cubrir. Da igual entre piezas que mueren y nacen (un
  frame vacío entre una muerte y un pop no se ve), pero produce un parpadeo
  visible cuando una pieza CONTINÚA en la siguiente con el mismo objeto en
  pantalla. Mordió tres veces: el empalme b1a→b1b a 24 fps, el mismo a 60, y
  las diez repeticiones del marco del split (ocho parpadeos de un frame).
  **Regla: nunca encadenar calculando `pos += duracion`. Colocar el clip, leer
  su `GetEnd()` real y usar ESE valor como inicio del siguiente.**
- Un polvo de transición solo tiene sentido pegado a una pieza (entrando o
  saliendo). Suelto en medio de un hueco no transiciona nada y no se percibe.

- El laptop nunca se disuelve con el monito: la pega sobrevive al agente (el
  check verde aparece idealmente cuando él YA no está).
- Los gestos de "compañía" (dormir, cargar, mirar) van en mini escala; los de
  tesis (ciclo, parpadeo, barra) a escala completa.
- Elementos nuevos de utilería siguen la misma lógica pixel: rects sin rx para
  lo pixel-art (monito, rack, doc… bueno, el doc usa esquinas rectas), rx solo
  en la utilería "suave" heredada (laptop, barras de código, check).

## Paneles de captura para el formato split (tramo-union, 31-ago-2026)

Cuando el video usa el formato split (pantalla izquierda / camara derecha) y la
grabacion de pantalla repite la misma vista, se reemplaza el clip por un PANEL:
un MOV con alfa que trae la captura ya encuadrada en la ventana del marco, con
punch-in propio. No toca la camara, no toca el marco.

Receta (ffmpeg, sin HyperFrames — es una imagen, no una animacion de personaje):

```
ventana izquierda del marco, en canvas UHD:  x 92  y 92  w 2106  h 1976
base a 2x para que el punch no pixele:       4212 x 3952, pad color #faf9f5
zoompan  z de 1.0 a Z,  s=2106x1976,  d=1,  fps=60
x = max(0, min(iw-iw/z, iw*cx - iw/(2*z)))     y analogo para y
overlay sobre color=black@0.0:s=3840x2160  ->  prores_ks 4444, yuva444p10le, qscale 11
```

TRAMPA DE PROPORCION (la vio Nicolas, no yo): **el asset debe venir recortado
al ratio de la ventana ANTES de generar el panel**. La ventana es 2106x1976 =
ratio 1.0658. Si el asset es mas ancho (una captura de GitHub suele ser 1.3-1.5),
el `force_original_aspect_ratio=decrease` lo mete entero y deja bandas del color
de fondo arriba y abajo: la imagen se ve chica y no llena el borde redondeado.
Recortar primero — normalmente sobra una columna (la de fechas, el sidebar) o la
barra inferior de la app.

TRAMPA (costo dos renders): **cx/cy son fracciones de la imagen YA CON PADDING**,
no del asset. Si el asset tiene otra proporcion que la ventana, hay bandas y la
fraccion se corre. Conversion: `cy_pad = (padTop + cy_asset*hEscalada)/BH`.

TRAMPA 0, LA QUE MAS CARO SALE: **`overlay` de ffmpeg APLANA el alfa**. Componer
el panel con `[color=black@0.0][panel]overlay` produce un MOV cuyo canal alfa es
OPACO EN TODO EL FRAME: en Resolve el panel tapa la pista de abajo entera y la
camara desaparece en negro. Nicolas lo vio antes que yo, y mi propio composite
de prueba ya lo mostraba (lo atribui a un seek fallido, mal).
Lo correcto es NO usar overlay: terminar la cadena con un pad transparente.

```
format=rgba, scale/pad a la base, zoompan, format=rgba,
pad=3840:2160:92:92:color=black@0
```

VERIFICACION OBLIGATORIA de cualquier pieza con alfa, antes de colocarla:

```
ffmpeg -ss T -i pieza.mov -frames:v 1 -vf "format=rgba,alphaextract" alfa.png
```

y MIRAR la imagen: blanco = opaco, negro = transparente. Debe ser negro en todo
lo que tiene que dejar pasar. HyperFrames genera el alfa bien; el que hay que
vigilar es el ffmpeg escrito a mano.

TRAMPA 2: si `cx` pide un centro que la region no alcanza, el `min()` lo CLAMPEA
y el punch termina descentrado sin avisar. Condicion para centrar en cx sin
clamp: `z >= 1/(2*(1-cx))`. Cuando no se cumple, o se baja el objetivo o se
sube el zoom.

Peso: yuva444p12le sin qscale daba 1.16 GB por 8s de captura oscura; con
10 bits + qscale 11 baja a 350 MB sin diferencia visible en texto.

## Que se ve REALMENTE en la ventana del marco

Antes de juzgar una captura de pantalla hay que recortar lo que de verdad entra
en la ventana, no mirar la grabacion completa: el crop del clip MAS el recorte
de la ventana dejan fuera una franja. En este video el area util del source es
`crop=2190:1715:0:457` (source 4096x2648, CropRight 1504 / CropTop 210 /
CropBottom 143, Zoom 1.1524). Mirar la grabacion entera me hizo reportar dos
veces mal que el guion de rodaje salia al aire.

## jornada — el ciclo completo SIN repetir el gesto

`compositions/jornada.html` (14.1s, 60fps). Va sobre camara a PANTALLA COMPLETA
(no en panel): el monito se para en la mesa, a la derecha del vaso, zona libre
del encuadre. Verificado componiendo el MOV sobre un frame real de la camara
antes de colocarlo — ese composite es el unico modo de saber si tapa a Nicolas.

Tercera aparicion del ciclo en el mismo video, asi que el gesto tuvo que cambiar:
- "morir" = COLAPSO instantaneo (0.10s, s = 1-k^2), no la disolucion canonica.
- "nace con el reloj" = el reloj entra primero y la aguja da UNA vuelta; el
  monito se forma recien cuando la aguja llega a las 12.
- remate: el monito se disuelve y LOS DOS DOCUMENTOS QUEDAN en cuadro. Es la
  tesis del video hecha imagen ("el estado no vive en el agente").

Truco util: para correr toda la escena sin recalcular decenas de coordenadas,
envolver todo en `<g id="todo" transform="translate(dx dy)">`.

## Paneles conceptuales para tramos largos sin demo (EL MARCO, 1-sep-2026)

Cuando el video entra en un bloque conceptual largo (aqui 2:45) el formato split
se queda sin material: no hay pantalla que mostrar porque no se esta haciendo
nada. Dejar la camara sola ahi es donde se cae la retencion. La solucion es
llenar la ventana izquierda con paneles que ACTUAN el argumento.

Reglas que salieron de esta tanda:

- **Fondo obligatorio.** La pieza debe pintar `<rect x=46 y=46 w=1053 h=988
  rx=44 fill="#faf9f5">`. Sin eso se ve la camara por detras de la ventana.
- **Claro, no negro.** El marco del canal es #faf9f5 y los paneles vecinos son
  capturas claras; una ventana negra pesa demasiado y rompe la paleta.
- **El panel no puede estar lleno los N segundos ni vacio los primeros.** En M4
  los tres marcos numerados entran en el segundo 2 aunque las preguntas lleguen
  en el 16: se ve de entrada que vienen tres, y el hueco intermedio lo ocupa una
  frase que se va sola.
- **No ridiculizar la alternativa que el guion respeta.** Nicolas dice del
  gateway "no porque este malo": la pieza lo dibuja entero y lo termina VALIDANDO
  con un check verde y sus tres condiciones. El contraste llega despues.
- **Un gesto por bloque, no el mismo tres veces.** La barra de 24h ya se uso dos
  veces en la intro, asi que la espera de M3 es un CONTADOR de digitos.

## Medir el layout ANTES de renderizar (ahorra ~10 min por error)

Un render de 4K a 60fps son 3-9 minutos. Verificar por render es carisimo.
Servir el proyecto y medir en el navegador cuesta segundos:

```
python3 -m http.server 8777           # desde la carpeta del proyecto
# navegar a /compositions/PIEZA.html y en la consola:
tl.progress(t/DUR, false)             # OJO: el 2do arg false; seek() por
                                      # defecto suprime los callbacks y pose()
                                      # no corre, se ve el panel vacio
el.getBoundingClientRect()            # bbox CON transforms; getBBox() los ignora
```

Comparar cada bbox contra los limites de la ventana (46..1099 x 46..1034). Asi
se cazaron cuatro desbordes en una pasada: el titulo de M1, las etiquetas de M2
y M4, y una burbuja de M3.
