"""Coloca piezas de un piezas*.json en DEF-anim respetando la pista de cada pieza (V2 o V3).

Uso: python place3.py piezas3.json [solo_id ...]
     python place3.py --swap m1-salto m1-salto-v2   # reemplaza un clip de V2 por otro render en el mismo record
Reglas: endFrame = frames (EXCLUSIVO) · mediaType 1 · timeline por nombre · readback · pm.SaveProject().
"""
import sys, json
from pathlib import Path
import DaVinciResolveScript as dvr

ROOT = Path(__file__).parent
G = str(Path(__file__).parent / "renders")   # carpeta de renders, idealmente en un SSD externo
TL_NAME = "DEF-anim"

r = dvr.scriptapp("Resolve"); pm = r.GetProjectManager(); proj = pm.GetCurrentProject()
mp = proj.GetMediaPool()
tl = None
for i in range(1, int(proj.GetTimelineCount()) + 1):
    t = proj.GetTimelineByIndex(i)
    if t.GetName() == TL_NAME: tl = t
assert tl, f"no existe {TL_NAME}"
proj.SetCurrentTimeline(tl)
fps = float(tl.GetSetting("timelineFrameRate")); st = tl.GetStartFrame()
rootf = mp.GetRootFolder()
gbin = next((f for f in rootf.GetSubFolderList() if f.GetName() == "graficas"), None) or mp.AddSubFolder(rootf, "graficas")
mp.SetCurrentFolder(gbin)
existing = {c.GetName(): c for c in gbin.GetClipList()}

def clip_for(name):
    clip = existing.get(name)
    if not clip:
        res = mp.ImportMedia([f"{G}/{name}"]); clip = res[0] if res else None
        if clip: existing[name] = clip
    return clip

def put(name, track, record, frames):
    while tl.GetTrackCount("video") < track:
        tl.AddTrack("video"); print("pista agregada")
    placed = {it.GetName(): it for it in (tl.GetItemListInTrack("video", track) or [])}
    if name in placed: print("ya colocada:", name, "en f", placed[name].GetStart() - st); return
    clip = clip_for(name)
    if not clip: print("NO importó", name); return
    nf = int(clip.GetClipProperty("Frames") or 0)
    if nf != frames: print(f"  aviso {name}: clip tiene {nf} frames, plan {frames}; uso el plan")
    ok = mp.AppendToTimeline([{ "mediaPoolItem": clip, "startFrame": 0, "endFrame": frames,
                                 "trackIndex": track, "recordFrame": st + record, "mediaType": 1 }])
    it = next((x for x in (tl.GetItemListInTrack("video", track) or []) if x.GetName() == name), None)
    if it: print(f"OK {name}: V{track} f{it.GetStart()-st}-{it.GetEnd()-st} ({it.GetEnd()-it.GetStart()} fr, plan {frames}) | alpha {clip.GetClipProperty('Alpha mode')}")
    else: print(f"FALLÓ {name}: AppendToTimeline devolvió {ok}")

if sys.argv[1] == "--swap":
    old, new = sys.argv[2] + ".mov", sys.argv[3] + ".mov"
    it = next((x for x in (tl.GetItemListInTrack("video", 2) or []) if x.GetName() == old), None)
    assert it, f"no está {old} en V2"
    rec, frames = it.GetStart() - st, it.GetEnd() - it.GetStart()
    print("reemplazo", old, "f", rec, "+", frames, "->", tl.DeleteClips([it], False))
    put(new, 2, rec, frames)
else:
    piezas = json.load(open(ROOT / sys.argv[1])); only = set(sys.argv[2:])
    for p in piezas:
        if only and p["id"] not in only: continue
        name = p["id"] + ".mov"
        if not Path(f"{G}/{name}").exists(): print("FALTA render:", name); continue
        put(name, p.get("track", 2), p["record"], p["frames"])
pm.SaveProject(); r.OpenPage("edit")
for tr in (2, 3):
    print(f"V{tr} ahora:", [(x.GetName(), x.GetStart() - st, x.GetEnd() - st) for x in (tl.GetItemListInTrack("video", tr) or [])])
print("guardado")
