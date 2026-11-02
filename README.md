# Monito: motion graphics con Claude Code, sincronizados a tu voz

La skill de Claude Code que animó 433 piezas del [curso de Claude Code](https://youtu.be/ZxVEmG172Xg) y el
video [Claude Code Motion Graphics](https://www.youtube.com/@NicolasNeiraGarcia). Convierte lo que dices
en cámara en animaciones de un personaje pixel, con cada gesto clavado a la palabra exacta, y las monta
solas en DaVinci Resolve por su API.

## Qué hay aquí

```
skill-monito/
├── SKILL.md                     la skill tal cual la usa Claude Code
├── references/
│   ├── personaje.md             el personaje es un archivo: geometría medida, paleta, tipografía pixel
│   ├── gestos.md                catálogo de gestos ya construidos y notas de dirección
│   ├── patron-composicion.md    cómo se escribe una composición HyperFrames seek-safe
│   └── pipeline.md              Resolve → ffmpeg → WhisperX → plan → HyperFrames → verificar → Resolve API
├── lib2.js                      actuación: saltos, caminata, sombra, ojos, brazos, pliegue, ola
├── pixel-font.js                fuente pixel 5×7
├── place3.py                    colocación en Resolve por API (endFrame exclusivo, readback, save)
├── render-todo.sh               render en tanda a ProRes 4444 con alfa, 4K, 60 fps
└── ejemplos/
    ├── gen-hook.py              el generador del hook del video (seis piezas, el monito en la mesa)
    ├── m1-salto.html            una composición terminada: nace en el hombro y salta a la mesa
    └── b3-gestos.html           el catálogo de gestos, actuado
```

## Las seis etapas

1. **Cortes.** Claude Code lee la pista V1 del timeline de Resolve y reconstruye el audio exacto desde el crudo (ffmpeg). Nada sale del render.
2. **Palabras.** WhisperX (large-v3, CPU) devuelve cada palabra con su tiempo. Ese tiempo manda: todo lo que se anima en una frase nace en ese frame.
3. **Plan.** Claude decide qué piezas, en qué frase, en qué frame y con qué gesto. El plan se muestra antes de construir y espera un "dale".
4. **Componer.** Cada pieza es un HTML con HyperFrames. Un solo driver de tiempo, todo es función de `t`, sin estado.
5. **Verificar.** Se extraen frames del render y se componen sobre el cuadro real de la cámara. Se miran antes de tocar el timeline.
6. **Montar.** `AppendToTimeline` por la API de Resolve, en la pista de arriba, en el frame exacto del plan. Readback y guardar.

Claude decide en dos lugares (3 y 4). ffmpeg corta, el navegador renderiza y la API coloca: ninguno opina. Por eso es reproducible.

## Requisitos

- DaVinci Resolve Studio (la API de scripting externa es solo de Studio).
- [HyperFrames](https://github.com/heygen-com/hyperframes) (`npx hyperframes@0.8.20`), ffmpeg, Chrome.
- WhisperX en un venv propio (large-v3, `--compute_type int8` en Mac).
- Claude Code con la carpeta `skill-monito` copiada a `.claude/skills/monito/`.

## El personaje es un parámetro

`references/personaje.md` describe al personaje como coordenadas y colores medidos sobre el dibujo original.
Cámbialo por tu mascota, tu logo o solo texto y las seis etapas corren igual.

## Trampas que ya pagué

Están en `references/pipeline.md` y en `references/gestos.md`: medir en el navegador no ve el error, el GOP largo deja
tramos offline, el último frame no entra (`endFrame` es exclusivo), los stills se esconden en el disco interno,
WhisperX se equivoca con los nombres, y el origen de giro se rompe al renderizar.

Licencia MIT. HyperFrames es Apache 2.0.
