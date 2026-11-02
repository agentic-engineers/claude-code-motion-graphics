# Patrón de composición determinista

Cada pieza es un HTML HyperFrames independiente en `compositions/`, renderizado
con `-c`. Envelope 4K nativo con SVG vectorial:

```html
<meta name="viewport" content="width=3840, height=2160" />
html,body,#stage { width:3840px; height:2160px; background:transparent }
<div id="stage" data-composition-id="ID" data-start="0" data-duration="D"
     data-fps="60" data-width="3840" data-height="2160">
  <div id="shot" class="clip" data-start="0" data-duration="D" data-track-index="1">
    <svg id="scene" viewBox="0 0 1920 1080">…</svg>
```

El viewBox 1920×1080 escala vectorial al stage 4K → nítido sin upscale.
(`--resolution 4k` del render NO combina con alfa; por eso el envelope va en 4K.)

## El driver maestro — todo función pura de t

UN tween GSAP `ease:"none"` que llama `pose()`; todo estado visual se calcula
desde t, sin estado acumulado. Así cada seek del render produce el frame exacto.

```js
const D = { p: 0 };
function pose() {
  const t = D.p * DURACION;
  // ...setAttribute de transforms/opacity como función de t...
}
tl.to(D, { p: 1, duration: DURACION, ease: "none", onUpdate: pose }, 0);
pose(); // hornear frame 0
window.__timelines["ID"] = tl;
tl.seek(0);
```

## TRAMPA CRÍTICA: svgOrigin de GSAP está roto en el capture

`svgOrigin` en tweens de scale sobre `<g>` SVG se ignora (escala desde la
esquina del bbox → el elemento aparece flotando). NUNCA usar GSAP para
transforms de grupos SVG. Escribir el transform a mano dentro de pose():

```js
el.setAttribute("transform",
  "translate(cx cy) scale(" + s + ") translate(-cx -cy)");
```

Eases a mano: `backOut(s,p){const q=p-1; return 1+(s+1)*q*q*q+s*q*q}` (pops,
s=1.8), `p*p` (power2.in, colapsos), squash de aterrizaje = press (sy 0.9,
sx 1.08, 0.08s) + release backOut(1.5) 0.18s.

GSAP SÍ sirve para: `autoAlpha`, `tl.set` de scaleX en rects individuales
(barras, con transformOrigin "left center"), y el pop del check (transformOrigin
"50% 50%" funciona en ese elemento).

## TRAMPA: dos sistemas de coordenadas, y es fácil mezclarlos

El personaje se dibuja SIEMPRE en coordenadas locales (asiento 1627,907) y se
coloca con `translate(cx cy) scale(s) translate(-1627 -907)`. Todo lo que
acompañe al personaje cae en uno de dos casos, y confundirlos cuesta un render:

1. **Cuelga del wrapper del monito** (`makeDoc(m.wrap)`): usa coordenadas
   LOCALES (1627/907 y alrededores), hereda escala y colapso. Sus propios
   desplazamientos se dividen por la escala.
2. **Cuelga de un grupo suelto** (utilería que vive por su cuenta): usa
   coordenadas ABSOLUTAS del viewBox. Ahí 1627 es el borde derecho, no el centro
   del personaje. Hay que calcular la posición real: un monito en `cx=960` con
   escala 0.55 tiene la cabeza en `y = cy + (667-907)*0.55`.

Pasó tres veces antes de quedar escrito: dos por poner utilería fuera del
wrapper (los tres minis la dibujaban encima uno del otro) y una por usar 1627
en un grupo absoluto (los objetos quedaron fuera de cuadro).

## TRAMPA: la utilería va DENTRO del wrapper escalado

Un documento, una hoja o cualquier objeto que acompañe a un mini debe colgar del
MISMO wrapper que el monito (`makeDoc(m.wrap)`), no del grupo padre. Si cuelga
del padre queda en coordenadas absolutas: los tres minis lo dibujan encima uno
del otro, no se escala con ellos y puede irse fuera del viewBox. Pasó dos veces
(b3-tareas y b6-callarse) antes de quedar anotado acá. Dentro del wrapper, las
coordenadas son LOCALES del personaje (asiento 1627,907) y los desplazamientos
propios del objeto se dividen por la escala.

## Disolución (la muerte canónica)

Máscara `userSpaceOnUse` con frente blanco + banda de degradado de 50px
(`fadeGrad` blanco→negro vertical); el frente se traslada hacia arriba en
pose(). Un frente para el cuerpo y otro RETRASADO para los bracitos (sobreviven
~0.2s). Dentro de un wrapper escalado, la máscara se define en coordenadas
LOCALES del wrapper (se puede reutilizar la geometría del monito grande).

## Partículas

Pool sembrado una vez con `prand(n) = frac(sin(n*127.1+311.7)*43758.5453)` —
la única "aleatoriedad" permitida. Cuadrados de 4-8px (pixel debris, no
círculos), clases alternadas f-clay/f-clay-deep. Movimiento balístico puro:
`x = ox+vx·ti`, `y = oy+vy·ti+0.5·G·ti²` con G=-25 (siguen subiendo), attack
0.05-0.08s, decay del 55-65% de la vida. En disoluciones, el nacimiento de cada
partícula se mapea a la altura de su fila (las de abajo nacen primero, igual
que el frente). Vidas recortadas para que todas mueran antes del fin de pieza.

## Ritmo

- Pop de entrada: 0.25-0.35s. Colapso de salida: 0.08-0.12s (morir es rápido).
- Cascadas (fila de elementos): stagger 0.02-0.1s por elemento.
- Los beats se anclan al INICIO de la palabra hablada; si el gesto necesita
  aviso (un número que "trae"), restar el tiempo del pop al record frame.

Ejemplos reales de cada patrón: ver `references/gestos.md`.
