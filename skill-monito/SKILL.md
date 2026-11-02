---
name: monito
description: Sistema de animación del monito pixel de Claude Code para overlays de video del canal. Produce piezas HyperFrames (ProRes 4444 con alfa, 4K/60) sincronizadas palabra a palabra a la voz de Nicolás y las coloca por script en el timeline de DaVinci Resolve. Usar SIEMPRE que Nicolás pida animaciones, overlays, gráficas o intros para un video, mencione al monito o "la imagen de Claude Code", pida "como lo del video de CI", o esté editando un video y quiera que las gráficas actúen lo que él dice. También cuando pida agregar un gesto nuevo del personaje (dormir, cargar algo, parpadear, multiplicarse).
---

# Monito — overlays animados del personaje del canal

El monito pixel de Claude Code es la firma visual del canal: actúa lo que Nicolás
dice en cámara, sincronizado a su voz real. Este sistema produce piezas de overlay
transparentes y las inserta en el timeline de Resolve sin edición manual.

## La gramática visual (no negociable)

**Ninguna gráfica aparece ni desaparece "normal": todo nace con pop y muere en
partículas pixel**, igual que un agente efímero. Esa es la tesis del canal hecha
lenguaje visual. Entrada = pop `backOut` desde su punto de apoyo (+ squash si
aterriza); salida = disolución de abajo hacia arriba con partículas, o colapso
instantáneo (morir es rápido, nacer cuesta).

Regla de retención aprendida (30-ago-2026): **no repetir el mismo gesto visual
más de dos veces seguidas en un video** — la tercera aparición necesita un
comportamiento NUEVO (pattern interrupt). Ejemplo real: la tercera vez que el
monito iba a disolverse se rehizo como "parpadeo de existencia".

## Proceso

1. **Leer contexto**: qué video, qué timeline de Resolve, qué frases quiere
   animadas. Si ya existe transcript del rodaje, reutilizarlo.
2. **Transcript sincronizado**: seguir `references/pipeline.md` § Audio y WhisperX.
   El resultado son timestamps por palabra EN TIEMPO DE TIMELINE.
3. **Proponer el plan de piezas en el chat ANTES de construir** (regla dura del
   canal): qué gesto, en qué frase, en qué hueco del timeline. Esperar el "dale".
4. **Componer**: una composición HyperFrames por pieza en el proyecto
   `editor/projects/monito-intro-ci/compositions/` (o el proyecto del video).
   Leer `references/personaje.md` (geometría y paleta exactas) y
   `references/patron-composicion.md` (el patrón determinista y sus trampas).
   Reutilizar gestos existentes: catálogo en `references/gestos.md`.
5. **Render + verificación**: render con alfa, extraer frames clave con ffmpeg y
   MIRARLOS antes de tocar el timeline (detalles y trampas en pipeline.md).
6. **Colocar en Resolve por script**: AppendToTimeline a V2 con el transform del
   usuario copiado, readback, SaveProject. Nunca pisar una versión anterior:
   los renders se nombran con sufijo nuevo y los clips viejos quedan en el bin.

## Reglas duras heredadas del canal

- El bloque de EVIDENCIA de un guion queda limpio, sin monito: la prueba debe
  leerse 100% real ("mira que no es maqueta").
- Sin cifras inventadas en pantalla (un medidor que se llena sí; "$2.40" no).
- Cortes de cámara del timeline (V1) mandan: las piezas terminan antes del corte
  o exactamente en él; verificar huecos de V2 antes de asignar record frames.
- El video SE EDITA: si un beat de voz no calza con la animación, se ajusta la
  pieza al audio real, jamás al guion teórico.

## Referencias

| Archivo | Cuándo leerlo |
|---|---|
| `references/personaje.md` | Antes de dibujar el monito o texto pixel |
| `references/patron-composicion.md` | Antes de escribir cualquier composición |
| `references/pipeline.md` | Para transcript, render, verificación y Resolve |
| `references/gestos.md` | Para reutilizar piezas/gestos ya construidos |

El proyecto vivo con todas las composiciones de ejemplo es
`editor/projects/monito-intro-ci/` — ante cualquier duda, leer una pieza real
equivalente antes de improvisar.
