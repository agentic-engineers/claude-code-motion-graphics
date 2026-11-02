# Pipeline: Resolve → WhisperX → HyperFrames → Resolve

> **EL CANAL ES 60 fps. SIEMPRE.** Composición `data-fps="60"` y render `--fps 60`.
> Un render a 24 puesto en timeline de 60 NO sirve: 60/24 = 2,5 no es entero, así que
> Resolve alterna 2 y 3 frames y produce judder visible en los movimientos lentos
> (pops, punch-ins, derivas, partículas). El frame rate NO se deduce del proyecto
> abierto: se pregunta. Ver [[reference_canal_60fps]].

Requisitos: Resolve Studio ABIERTO con el proyecto del video. Venv del MCP:
`editor/vendor/davinci-resolve-mcp/venv/bin/python`. Env vars:

```bash
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$RESOLVE_SCRIPT_API/Modules"
```

## 1. Audio del timeline (para sincronizar a la voz real)

NO usar el render de Resolve para exportar wav
(`SetCurrentRenderFormatAndCodec('wav','lpcm')` devuelve False y el job no
corre). En su lugar, reconstruir el audio desde el clip crudo con la cut list:

- Por cada item de V1: `it.GetSourceStartTime()` / `GetSourceEndTime()`
  (SEGUNDOS de fuente — sin ambigüedad; `GetLeftOffset()` está en frames de
  TIMELINE, no del clip: 60fps vs 24fps muerde aquí) y `GetStart()/GetEnd()`
  (frames de timeline).
- Extraer cada segmento: `ffmpeg -ss <src_s> -t <(rec_out-rec_in)/fps> -i crudo
  -vn -ar 16000 -ac 1 seg.wav` y concatenar en orden de record. La duración del
  concat debe calzar con el timeline al milisegundo (verificarlo).

## 2. WhisperX

Venv persistente `~/.cache/video-editor/whisperx-venv`. large-v3, CPU int8,
batch 4, idioma es, con align → words.json con `{word, start, end}` por palabra
ya en tiempo de timeline. Correr en background (minutos en M1). Ojo con el ASR:
"Anthropic"→"Antropi", "el agente"→"la gente" — buscar anclas con tolerancia.

## 3. Anclar beats y planificar huecos

- record_frame = round(timeline_s × 60).
- Leer V1 para conocer los CORTES de cámara (las piezas terminan en o antes de
  un corte) y V2 para conocer los huecos libres (nada puede traslapar).
- Mostrar el plan (pieza → frase → frame → duración) en el chat y esperar dale.

## 4. Render

```bash
cd <proyecto-hyperframes>   # SIEMPRE cd primero: cwd equivocado = render perdido
npm run check               # antes de cada tanda
npx hyperframes@<pin> render -c compositions/PIEZA.html \
  --format mov --quality high --fps 60 -o renders/PIEZA.mov
```

ProRes 4444 con alfa (`yuva444p12le`). Verificar `nb_frames` con ffprobe =
duración×60. El pin de versión del proyecto se respeta (no flotar a latest).

## 5. Verificación visual ANTES de colocar (obligatoria)

Extraer frames clave directo del MOV (SIN el filtro overlay de ffmpeg para
verificar — con `-ss` a veces compone el frame 0 vacío y da falsos negativos):

```bash
ffmpeg -ss T -i pieza.mov -frames:v 1 -vf "format=rgba,crop=W:H:X:Y" f.png
```

Si un frame parece vacío pero debería tener contenido, medir el alfa
(`alphaextract,signalstats`) o leer píxeles crudos antes de concluir nada.
Mirar las imágenes con Read; montar grillas con xstack para comparar momentos.

## 6. Colocar en Resolve

```python
mp.AppendToTimeline([{'mediaPoolItem': clip, 'startFrame': 0,
    'endFrame': nframes-1, 'trackIndex': 2, 'recordFrame': rec,
    'mediaType': 1}])   # mediaType 1 = solo video
```

- Importar al bin `graphics` (idempotente: buscar por nombre antes de importar).
- Autoridad de propiedades: `clip.GetClipProperty('FPS'/'Frames'/'Alpha mode')`
  — Resolve detecta el alfa solo ("Straight").
- **Copiar el transform del usuario** a las piezas de escena: leer
  `GetProperty('ZoomX'/'ZoomY'/'Pan'/'Tilt'/'AnchorPointX'/'AnchorPointY')` de
  un clip del monito ya ajustado por Nicolás y aplicarlo con SetProperty a las
  nuevas. Las piezas a pantalla completa (palabras, barra) van SIN transform.
- Targetear timeline POR NOMBRE, readback de V2 tras cada write, `SaveProject()`.
- Reemplazos: `tl.DeleteClips([item], False)` del clip viejo y append del nuevo
  (el clip viejo queda en el bin; renders con nombre nuevo, jamás pisar).
- Para que Nicolás lo vea: `resolve.OpenPage('edit')` +
  `tl.SetCurrentTimecode(...)` sobre la pieza nueva.

## Trampas aprendidas en el short vertical (23-oct-2026)

- El renderer sirve la RAÍZ del proyecto: un `<script src="lib.js">` relativo
  dentro de `compositions/` falla (`sub_timeline_script_failure`, render
  bloqueado). Helpers compartidos → inlinear antes de renderizar
  (ver `ia-invisible/short-senior/inline.py`).
- Duraciones no enteras en frames (4.3667 s) rinden 1 frame de más:
  pasar `endFrame` = frames planificados al AppendToTimeline, no `Frames`.
- Envelope vertical: viewport y stage 1080×1920, viewBox `0 0 1080 1920`;
  dejar libres los ~300 px de abajo y ~120 px de la derecha (UI de Shorts).
- `check` recibe un DIRECTORIO (no `-c`); el render sí acepta `-c`.
