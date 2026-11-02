# El personaje canónico

Medido píxel a píxel del PNG de referencia de Nicolás (grilla de celdas de 26px
en el original). NO improvisar proporciones: cuando se dibujó "a ojo" fue
rechazado. Si aparece una referencia visual nueva, medirla con un script antes
de dibujar (regla del canal: referencia antes de generar).

## Geometría (escala estándar: celda U=48 en viewBox 1920×1080)

Asiento (baseline de patas): y=907. Centro del personaje: x=1627.

```
cuerpo   x=1483 y=667 w=288 h=192   (6U×4U, esquinas RECTAS, sin cortes)
ojo izq  x=1527 y=715 w=22  h=48    (½U×1U, fila 2, al 19% del ancho)
ojo der  x=1705 y=715 w=22  h=48    (al 81%)
patas    x=1527/1572/1660/1705  y=859 w=22 h=48   (2 pares metidos hacia adentro)
brazo izq x=1439 y=763 w=44 h=48    (fila 3, pegado al costado)
brazo der x=1771 y=763 w=44 h=48
```

Para minis: envolver las MISMAS coordenadas en un wrapper
`translate(cx cy) scale(s) translate(-1627 -907)` — el asiento local queda en
(cx, cy). Escalas usadas: 0.42 (bajo palabras), 0.32 (fila de fondo).

## Paleta

```
--clay:        #d07e78   (salmón del personaje, muestreado del PNG — NO #d97757)
--clay-deep:   #ad615c   (partículas alternas)
--clay-shadow: #6e3b36   (sombra de contacto, opacidad 0.2)
--paper:       #faf9f5   (laptop, doc)
--ink:         #191919   (ojos, pantallas)
--green:       #2e9e5b   (check verde)
--gris:        #55524e   (servidores, monitos apagados, celdas de horas)
```

## Laptop compañero

```
base     x=1150 y=874 w=370 h=34 rx=12 (paper)
pantalla grupo rotate(-6 1165 874): shell x=1150 y=608 w=210 h=274 rx=16,
         cara ink x=1164 y=622 w=182 h=222 rx=10
barras   3 rects paper x=1182 y=656/692/728 w=146 h=18 rx=9 (scaleX animado
         en grilla de 0.25s, transformOrigin "left center")
check    circle green cx=1255 cy=733 r=48 + path paper "M1231 735 L1249 755
         L1281 713" stroke 11
```

## Tipografía pixel

`compositions/pixel-font.js` — fuente 5×7 propia (`buildPixelText(grupo, texto,
{x, y, cell, cls, shadow})`). Glifos: minúsculas comunes + í + dígitos + $ . :
IMPORTANTE: mantener una copia en la RAÍZ del proyecto HyperFrames (el file
server de `render -c` sirve desde ahí). Celdas usadas: 18 (rótulos), 15
(palabras b2), 12-14 (dígitos, $), 6-10 (zZZ). Sombra: pasada f-ink 0.35 con
offset 0.35·cell (dos pasadas: sombras primero, bloques después).

## Bob y tecleo (cuantizados a píxel entero — feel chunky)

- Bob de reposo: `Math.round(2 * sin(TAU*2*t))` en translate Y del grupo bob.
- Tecleo de brazos: `-Math.round(6 * max(0, sin(TAU*7*t)))` alternando fase π
  entre brazo izq y der.
- En una pieza que hace loop, usar frecuencias con ciclos enteros en la duración
  para que pose(final) == pose(0).
