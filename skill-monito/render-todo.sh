#!/bin/zsh
# Render de las piezas del hook directo al SSD (ProRes 4444 con alfa, 4K, 60 fps)
cd "$(dirname "$0")"
G="${RENDERS:-$(dirname "$0")/renders}"   # carpeta de renders, idealmente en un SSD externo
for p in $(python3 -c "import json;print(' '.join(x['id'] for x in json.load(open('${PZ:-piezas.json}'))))"); do
  if [[ -f "$G/$p.mov" ]]; then echo "=== $p (ya estaba)"; continue; fi
  echo "=== $p $(date +%H:%M:%S)"
  npx --yes hyperframes@0.8.20 render -c "compositions/$p.html" --format mov --quality high --fps 60 -o "$G/$p.mov" 2>&1 | grep -E "MB ·|rror|fail|Rendered|frames" || true
  echo "--- fin $p $(date +%H:%M:%S)"
done
echo "=== FIN $(date +%H:%M:%S)"
