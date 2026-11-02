"""Hook v2: el monito actúa sobre la MESA (1-nov-2026, tras el feedback "no siempre el mismo").

Seis piezas contiguas (m1..m6) que cubren 2.4 s → 161.4 s. Reutiliza HEAD/LIB/pixel-font de gen.py
y agrega lib2.js (saltos, caminata, sombra, ojos, brazos, pliegue, ola). Las anclas se resuelven
contra audio-hook.json. Salida: compositions/m*.html + piezas2.json.

Geometría del encuadre (viewBox 1920x1080 sobre el cuadro ya transformado, fondo-cam.png):
borde trasero de la mesa y≈895 · banda delante del laptop y 985-1080 · laptop x 566-1061 (base 946-984)
· taza x 326-422, y 821-936 · hombro derecho (1205,620) · pared libre izquierda x 70-670, y 100-560.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).parent
src = (ROOT / "gen.py").read_text()
LIB = src.split('LIB = r"""')[1].split('"""')[0]
HEAD = src.split('HEAD = """')[1].split('"""')[0]
PIXEL_FONT = (ROOT / "pixel-font.js").read_text()
LIB2 = (ROOT / "lib2.js").read_text()

A_ = str(ROOT / "analisis")   # audio-hook.json: salida de WhisperX sobre el audio reconstruido
T = json.load(open(f"{A_}/audio-hook.json"))
import unicodedata
W = [(w["start"], w["end"], w["word"]) for w in T["word_segments"] if "start" in w]
norm = lambda s: unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower().strip(".,;:!?¿¡")
def a(txt, desde=0.0):
    for s, e, w in W:
        if s >= desde and norm(w).startswith(norm(txt)):
            return s
    raise SystemExit(f"ancla no encontrada: '{txt}' desde {desde}s")

FPS = 60
PIEZAS = []
def emit(pid, rec_s, end_s, nota, anchors, body, track=2):
    rec = round(rec_s * FPS); fin = round(end_s * FPS); dur = round((fin - rec) / FPS, 4)
    A = {k: round(v - rec_s, 3) for k, v in anchors.items()}
    full = "const A=" + json.dumps(A) + ";\n" + body
    html = (HEAD.replace("__ID__", pid).replace("__DUR__", str(dur)).replace("__NOTA__", nota)
            .replace("__PIXELFONT__", PIXEL_FONT).replace("__GSAP__", (ROOT / "gsap.min.js").read_text()).replace("__LIB__", LIB + "\n" + LIB2).replace("__BODY__", full))
    (ROOT / "compositions" / f"{pid}.html").write_text(html)
    PIEZAS.append(dict(id=pid, record=rec, frames=fin - rec, track=track, start_s=rec_s, end_s=end_s))
    print(f"{pid:10s} rec f{rec} ({rec_s:7.2f}s)  {fin-rec} frames = {dur}s   anclas: " + " ".join(f"{k}={v}" for k, v in A.items()))

# fronteras contiguas (segundos del timeline)
B1, B2, B3, B4, B5, B6, B7 = 2.4, 20.1, 29.3, 66.1, 92.3, 129.5, 161.4

COMMON = r"""
      svg.appendChild(gparts);
"""

# ======================= m1: hombro → salto → multitud → timeline → ola =======================
an1 = dict(nunca=a("nunca"), anime=a("animé"), creo=a("creó"), n400=a("400", 4), anim2=a("animaciones", 7), curso=a("curso"),
           tres=a("3", 12), puso=a("puso"), exacto=a("exacto"), timeline=a("timeline", 16), sin=a("sin", 18), after=a("after", 18))
body1 = r"""
      const PX=1500, PY=1040, PS=0.55, SH=[1205,620], SHS=0.45;
      /* grupo de la ola: tira + multitud (el protagonista queda fuera) */
      const WG=mk("g",{}); svg.appendChild(WG);
      const WM=waveMask(svg,"a",60,900,1860,180);
      const XS=[]; for(let x=100;x<=1880;x+=85) if(Math.abs(x-PX)>=120) XS.push(x);
      const CY=992, CS=0.22;
      const S=strip(WG,70,1012,1820,50,XS,40);
      const crowd=XS.map((x,i)=>{ const c=actor(WG,false); c.born=A.n400+0.08+Math.abs(x-PX)/1400*2.0; c.x=x; c.i=i; c.hop=A.puso+0.1+i*0.085; return c; });
      /* palabras de la primera frase en la pared izquierda ("con las palabras ahí apareciendo"); colapsan al saltar */
      const WP=wordsPanel(svg,__WORDS__,110,150,8,560); const words=WP.words;
      const m=actor(svg,false);
      const segs=[
        {type:'at',t0:0,t1:0,at:SH,s:SHS},
        {type:'jump',t0:A.anime,t1:A.anime+0.55,from:SH,to:[PX,PY],s:[SHS,PS],h:70},
        {type:'jump',t0:A.n400,t1:A.n400+0.3,from:[PX,PY],to:[PX,PY],s:[PS,PS],h:40},
        {type:'jump',t0:A.sin+0.72,t1:A.sin+1.02,from:[PX,PY],to:[PX,PY],s:[PS,PS],h:36},
      ];
      burst(GS,PX,PY,12,11,A.anime+0.55,{sp:150,up:60});
      for(let j=0;j<25;j++){ const xj=60+j*76; burst(GP,xj,1030,3,100+j,A.sin+0.03+(xj-60)/1840,{sp:60,up:70,sz:4}); }
      /* contador en una tarjeta sobre la mesa, atrás a la derecha */
      const CC=[1620,886,250,72]; const cc=mk("g",{opacity:0}); svg.appendChild(cc); pixelRect(cc,"f-paper",CC[0],CC[1],CC[2],CC[3],14);
      const digitsG=mk("g",{}); cc.appendChild(digitsG); let lastN=-1;
      function pose(t){
        const st=motion(segs,t,{x:SH[0],y:SH[1],s:SHS});
        const onSh=t<A.anime;
        actorPose(m,t,st,{scale:pop(t,A.nunca),arms:onSh?"down":(t>A.n400-0.35&&t<A.n400?"up":(t>=A.sin&&t<A.sin+1.1?"up":undefined)),eyes:(t>A.sin&&t<A.sin+1.1)?"squint":"open",shadow:!onSh});
        { let ps=t<0.3?backOut(1.6,t/0.3):1; const tw=A.anime+0.1; if(t>=tw){ const k=clamp01((t-tw)/0.10); ps=1-k*k; }
          show(WP.paper.g,ps>0); xf(WP.paper.g,WP.paper.cx,WP.paper.cy,Math.max(ps,0.001),Math.max(ps,0.001)); }
        for(const L of words) labelPose(L,t,L.t,A.anime+0.1);
        crowd.forEach(c=>{ const k=pop(t,c.born);
          const cs=motion([{type:'hop',t0:c.hop,t1:c.hop+0.3,from:[c.x,CY],to:[c.x,1058],s:[CS,0.17],h:34,n:1}],t,{x:c.x,y:CY,s:CS});
          actorPose(c,t,cs,{scale:k,tph:c.i*0.137}); show(S.slots[c.i].fill,t>=c.hop+0.3); });
        popDie(S.g,t,A.puso,null,S.cx,S.cy,{sy:1});
        const wv=t>=A.sin+0.03; if(wv){ WG.setAttribute("mask",WM.url); WM.set(lerp(60,1900,clamp01((t-(A.sin+0.03))/1.0))); } else WG.removeAttribute("mask");
        /* contador */
        const cs=pop(t,A.n400-0.1); show(cc,cs>0); if(cs>0) xf(cc,CC[0]+CC[2]/2,CC[1]+CC[3],cs,cs);
        const n=t>=A.n400?Math.round(433*outCubic((t-A.n400)/1.4)):-1;
        if(n!==lastN){ while(digitsG.firstChild) digitsG.removeChild(digitsG.firstChild); if(n>=0){ const s=String(n); buildPixelText(digitsG,s,{x:CC[0]+(CC[2]-pixelTextWidth(s,6.4))/2,y:CC[1]+(CC[3]-7*6.4)/2,cell:6.4,cls:"f-clay"}); } lastN=n; }
        renderParts(GP,t); renderParts(GS,t,320);
      }
""" + COMMON
frase1=[(w, max(0.0, s_-B1)) for s_, e_, w in W if s_ < 4.0]
body1=body1.replace("__WORDS__", json.dumps([dict(w=norm(w), t=round(t_,3)) for w, t_ in frase1]))
emit("m1-salto", B1, B2, "M1: nace en el hombro, salta a la mesa, se multiplica en '400', los minis saltan a la tira del timeline, la ola de 'After Effects' los borra y queda uno.", an1, body1)

# ======================= m2: carga, duerme, prompt arrugado, plantilla pateada =======================
an2 = dict(cuando=a("cuando", 20), carga1=a("carga", 21), carga2=a("carga", 22), duerme1=a("duerme", 23), duerme2=a("duerme", 24.5),
           no=a("no", 25.5), prompt=a("prompt"), bonito=a("bonito"), plantilla=a("plantilla"), construi=a("construí"))
body2 = r"""
      const P0=[1500,1040], PS=0.55, CC=[1620,886,250,72], PZ=[480,958], ZS=0.45;
      const m=actor(svg,false);
      const segs=[
        {type:'hop',t0:A.carga1-0.4,t1:A.carga1-0.08,from:P0,to:[1700,1000],s:[PS,0.5],n:1,h:30},
        {type:'hop',t0:A.carga1+0.25,t1:A.duerme1-0.3,from:[1700,1000],to:[540,1040],s:[0.5,PS],n:8,h:30},
        {type:'hop',t0:A.duerme1-0.28,t1:A.duerme1,from:[540,1040],to:PZ,s:[PS,ZS],n:1,h:44},
        {type:'jump',t0:A.no,t1:A.no+0.22,from:PZ,to:PZ,s:[ZS,ZS],h:26},
        {type:'jump',t0:A.plantilla+0.12,t1:A.plantilla+0.3,from:PZ,to:PZ,s:[ZS,ZS],h:16},
      ];
      /* tarjeta 433 (misma que m1) */
      const cc=mk("g",{}); svg.appendChild(cc); pixelRect(cc,"f-paper",CC[0],CC[1],CC[2],CC[3],14);
      buildPixelText(cc,"433",{x:CC[0]+(CC[2]-pixelTextWidth("433",6.4))/2,y:CC[1]+(CC[3]-7*6.4)/2,cell:6.4,cls:"f-clay"});
      burst(GP,0,0,0,0,0); const CCc=[CC[0]+CC[2]/2,CC[1]+CC[3]/2];
      const Z=zzz(svg);
      const Lp=card(svg,"prompt",98,770,8,"f-ink",18);
      const TP=mk("g",{opacity:0}); svg.appendChild(TP); pixelRect(TP,"f-paper",570,850,140,100,6);
      for(let i=1;i<4;i++){ pixelRect(TP,"f-mute",570+i*35,850,2,100); } for(let i=1;i<3;i++){ pixelRect(TP,"f-mute",570,850+i*33,140,2); }
      const TK=A.plantilla+0.2;
      burst(GS,640,900,10,21,TK,{sp:120,up:40});
      function pose(t){
        const st=motion(segs,t,{x:P0[0],y:P0[1],s:PS});
        const carrying=t>=A.carga1&&t<A.duerme1+0.04;
        const asleep=t>=A.duerme1+0.1&&t<A.no;
        let o={};
        if(carrying) o={arms:"up"};
        if(asleep){ const br=0.80+0.02*Math.sin(TAU*0.6*t); o={arms:"down",eyes:"closed",sy:br,nobob:true}; }
        if(t>=A.no&&t<A.no+0.25) o={arms:"up",eyes:"open"};
        if(t>=A.plantilla+0.1&&t<A.plantilla+0.45) o={arms:"push"};
        actorPose(m,t,st,o);
        /* tarjeta: estática, luego al hombro/cabeza, luego puf */
        const headY=st.y-st.air-240*st.s*(o.sy||1)*st.sy;
        let cx=CCc[0], cy=CCc[1];
        if(t>=A.carga1){ const k=ease(t,A.carga1,A.carga1+0.18); cx=lerp(CCc[0],st.x,k); cy=lerp(CCc[1],headY-40-st.air*0.15,k); }
        const dead=t>=A.duerme1+0.04; const ds=fade(t,A.duerme1+0.04,0.12);
        show(cc,ds>0); if(ds>0) cc.setAttribute("transform","translate("+(cx-CCc[0]).toFixed(1)+" "+(cy-CCc[1]).toFixed(1)+") translate("+CCc[0]+" "+CCc[1]+") scale("+ds.toFixed(3)+") translate("+(-CCc[0])+" "+(-CCc[1])+")");
        if(!cc.puffed&&dead){ cc.puffed=true; }
        /* zZZ */
        zzzPose(Z,t,A.duerme1+0.5,st.x+40*0.45/0.45,headY,asleep);
        /* prompt: pop en 'prompt', se arruga en 'bonito' */
        { const ccx=Lp.ax+Lp.w/2, ccy=Lp.cy; let s=pop(t,A.prompt,0.3,1.6), rot=0; const tk=A.bonito+0.1;
          if(t>=tk){ const k=ease(t,tk,tk+0.32); s*=1-0.88*k; rot=560*k; if(t>=tk+0.34) s=0; }
          show(Lp.g,s>0); if(s>0) xf(Lp.g,ccx,ccy,s,s,rot); }
        /* plantilla: pop, patada, cae fuera de cuadro */
        { let s=pop(t,A.plantilla-0.2,0.3,1.6), x=640, y=900, rot=0;
          if(t>=TK){ const q=(t-TK)/0.6; x=640+340*q; y=900+40*q+1000*q*q; rot=170*q; if(q>1) s=0; }
          show(TP,s>0); if(s>0) TP.setAttribute("transform","translate("+(x-640).toFixed(1)+" "+(y-900).toFixed(1)+") rotate("+rot.toFixed(1)+" 640 900) translate(640 900) scale("+s.toFixed(3)+") translate(-640 -900)"); }
        renderParts(GP,t); renderParts(GS,t,320);
      }
""" + COMMON
# puf de la tarjeta y del prompt (sembrados con tiempos conocidos)
body2 = body2.replace("burst(GP,0,0,0,0,0);", "burst(GP,480,760,10,31,%.3f,{sp:90,up:50}); burst(GP,%d,%d,10,41,%.3f,{sp:80,up:50});" % (
    a("duerme", 23) - B2 + 0.04, 98 + 150, 770 + 28, a("bonito") - B2 + 0.44))
emit("m2-carga", B2, B3, "M2: carga la tarjeta 433 y cruza la mesa, duerme junto a la taza con zZZ, despierta en 'No', arruga el 'prompt', patea la 'plantilla' fuera de cuadro.", an2, body2)

# ======================= m3: voz → mini, check, monta, 1-2-3, entra/se va, palabra, borde =======================
an3 = dict(construi=a("construí"), sistema=a("sistema", 29), convierte=a("convierte", 30), voz=a("voz", 31), anim=a("animaciones", 32),
           comprueba=a("comprueba", 34), monta=a("monta", 36), hoy=a("hoy", 37), delante=a("delante", 38), ti=a("ti", 40), fijate=a("fíjate", 40),
           tres=a("tres", 41), primero=a("primero", 47), mira=a("mira", 48), entra=a("entra", 48), se=a("se", 50.4), va=a("va", 50.6),
           despues=a("después", 51), el2=a("2", 53.5), gesto=a("gesto", 54), cae=a("cae", 55), palabra=a("palabra", 56), frase=a("frase", 58),
           la3=a("3", 59), pieza=a("pieza", 59.5), corte=a("corte", 62), camara=a("cámara", 63), nunca=a("nunca", 64), pisa=a("pisa", 65))
body3 = r"""
      const P0=[480,958], S0=0.45, P1=[330,1045], S1=0.6, PW=[683,1050], PE=[1802,1050];
      const m=actor(svg,true);
      const segs=[
        {type:'at',t0:0,t1:0,at:P0,s:S0},
        {type:'hop',t0:A.delante-0.45,t1:A.delante,from:P0,to:P1,s:[S0,S1],n:2,h:34},
        {type:'jump',t0:A.tres,t1:A.tres+0.25,from:P1,to:P1,s:[S1,S1],h:24},
        {type:'jump',t0:A.palabra-0.5,t1:A.palabra,from:P1,to:PW,s:[S1,S1],h:190},
        {type:'hop',t0:A.pieza,t1:A.camara,from:PW,to:PE,s:[S1,S1],n:11,h:30},
      ];
      seedDissolveParts(m,A.mira+0.05,A.mira+0.6,7); seedGatherParts(m,A.entra-0.35,A.entra+0.05,17); seedDissolveParts(m,A.se+0.05,A.se+0.6,27);
      burst(GS,PW[0],PW[1],14,77,A.palabra,{sp:170,up:80});
      /* onda de voz: barras a lo largo de la mesa, viajan de derecha a izquierda */
      const bars=[]; for(let x=560;x<=1262;x+=18){ const r=mk("rect",{class:"f-clay",x:x-5,y:1000,width:10,height:0,opacity:0}); svg.appendChild(r); bars.push({r,x}); }
      /* mini nacido de la voz, check que cae, tira de 3 ranuras */
      const ms=actor(svg,false); const MS=0.28, MP=[600,1040];
      const chk=checkIcon(svg,0,0,30);
      const S3=strip(svg,700,1020,240,40,[740,820,900],40);
      burst(GP,MP[0],MP[1]-40,10,51,A.anim,{sp:80,up:60});
      burst(GS,MP[0],MP[1]-60,8,61,A.comprueba,{sp:110,up:30});
      burst(GP,820,1030,10,71,A.hoy+0.1,{sp:80,up:50});
      /* dígitos sobre la cabeza (locales) */
      const digs=[1,2,3].map((n,i)=>digitBox(m.extra,n,1497+i*100,520,86));
      const d2=digitBox(m.extra,2,1584,520,86), d3=digitBox(m.extra,3,1584,520,86);
      /* palabras sobre la mesa */
      const Wp=card(svg,"palabra",584,1016,6,"f-ink",10), Wf=card(svg,"frase",930,1016,6,"f-mute",10);
      function pose(t){
        const st=motion(segs,t,{x:P0[0],y:P0[1],s:S0});
        let dk=0, on=true, sc=1, o={};
        if(t>=A.mira+0.05&&t<A.entra-0.35){ dk=clamp01((t-(A.mira+0.05))/0.55); if(t>=A.mira+1.0) on=false; }
        else if(t>=A.entra-0.35&&t<A.entra+0.3){ dk=1-clamp01((t-(A.entra-0.1))/0.4); }
        else if(t>=A.se+0.05&&t<A.despues+0.1){ dk=clamp01((t-(A.se+0.05))/0.55); if(t>=A.se+1.0) on=false; }
        else if(t>=A.despues+0.1&&t<A.despues+0.5){ sc=pop(t,A.despues+0.1); }
        dissolve(m,dk);
        if(t>=A.voz&&t<A.anim+0.3) o.arms="catch";
        if(t>=A.gesto&&t<A.palabra-0.5){ const k=ease(t,A.gesto,A.palabra-0.5); o.sy=1-0.16*k; o.sx=1+0.12*k; o.eyes="squint"; o.arms="down"; }
        if(t>=A.palabra-0.5&&t<A.palabra) o.arms="up";
        let rot=0;
        if(t>=A.nunca-0.3&&t<A.pisa){ const q=(t-(A.nunca-0.3))/(A.pisa-(A.nunca-0.3)); rot=16*Math.sin(Math.PI*q)*Math.sin(TAU*1.7*(t-(A.nunca-0.3))); o.arms="flail"; o.eyes="squint"; }
        if(t>=A.pisa&&t<A.pisa+0.2){ const k=(t-A.pisa)/0.2; o.sx=1+0.18*(1-k); o.sy=1-0.2*(1-k); }
        o.rot=rot; o.scale=sc; o.on=on;
        actorPose(m,t,st,o);
        /* onda */
        const act=t>=A.voz&&t<A.voz+1.25, front=lerp(1262,560,clamp01((t-A.voz)/1.1));
        bars.forEach(b=>{ const d=b.x-front, vis=act&&d>-20&&d<170; if(!vis){show(b.r,false);return;} const h=8+50*Math.abs(Math.sin((d+20)/190*Math.PI*2.5))*(1-d/170); b.r.setAttribute("height",h.toFixed(1)); b.r.setAttribute("y",(1000-h/2).toFixed(1)); show(b.r,true); });
        /* mini */
        const mst=motion([{type:'hop',t0:A.monta,t1:A.monta+0.3,from:MP,to:[820,1058],s:[MS,0.2],n:1,h:40}],t,{x:MP[0],y:MP[1],s:MS});
        const msc=pop(t,A.anim)*fade(t,A.hoy+0.1); let mo={scale:msc,tph:0.4};
        if(t>=A.comprueba&&t<A.comprueba+0.16){ const k=(t-A.comprueba)/0.16; mo.sy=0.68+0.32*k; mo.sx=1.2-0.2*k; }
        actorPose(ms,t,mst,mo);
        { let cs=0, cx=MP[0], cy=0; if(t>=A.comprueba-0.24){ cs=fade(t,A.hoy+0.1); const q=clamp01((t-(A.comprueba-0.24))/0.24); const hy=mst.y-mst.air-240*mst.s*(mo.sy||1)-30; cy=lerp(700,hy,q*q); cx=mst.x; }
          show(chk.g,cs>0); if(cs>0) chk.g.setAttribute("transform","translate("+cx.toFixed(1)+" "+cy.toFixed(1)+") scale("+cs.toFixed(3)+")"); }
        popDie(S3.g,t,A.monta-0.2,A.hoy+0.1,S3.cx,S3.cy,{}); show(S3.slots[1].fill,t>=A.monta+0.3&&t<A.hoy+0.1);
        /* dígitos */
        digs.forEach((d,i)=>popDie(d.g,t,A.tres+i*0.2,A.primero,d.cx,d.cy,{o:1.8}));
        popDie(d2.g,t,A.el2,A.palabra-0.05,d2.cx,d2.cy,{o:1.8}); popDie(d3.g,t,A.la3,A.pisa+0.05,d3.cx,d3.cy,{o:1.8});
        /* palabra: pop antes del aterrizaje, se aplasta al caerle encima */
        { let s=pop(t,A.cae+0.1)*fade(t,A.pieza), sy=1; if(t>=A.palabra&&t<A.palabra+0.18){ const k=(t-A.palabra)/0.18; sy=0.55+0.45*k; }
          show(Wp.g,s>0); if(s>0) xf(Wp.g,Wp.ax+Wp.w/2,Wp.cy+Wp.h/2,s,s*sy); }
        { let s=pop(t,A.frase), rot=0, op=1; const tf=A.frase+0.4; if(t>=tf){ const k=ease(t,tf,tf+0.4); rot=84*k; op=1-k; if(k>=1) s=0; }
          show(Wf.g,s>0); if(s>0){ Wf.g.setAttribute("opacity",op.toFixed(2)); Wf.g.setAttribute("transform","rotate("+rot.toFixed(1)+" "+Wf.ax+" "+(Wf.cy+Wf.h/2)+") translate("+(Wf.ax+Wf.w/2)+" "+(Wf.cy+Wf.h/2)+") scale("+s.toFixed(3)+") translate("+(-(Wf.ax+Wf.w/2))+" "+(-(Wf.cy+Wf.h/2))+")"); } }
        renderParts(m.P,t); renderParts(GP,t); renderParts(GS,t,320);
      }
""" + COMMON
emit("m3-sistema", B3, B4, "M3: la voz corre por la mesa y se vuelve un mini, el check le cae encima, lo monta en la tira; 1-2-3; entra y se va de verdad; cae sobre 'palabra'; camina al borde del cuadro y no lo pisa.", an3, body3)

# ======================= m4: el editor a mano, la multitud gris sepultada, 'semanas' =======================
an4 = dict(si=a("si", 66), editas=a("editas"), sabes=a("sabes"), graficas=a("gráficas", 69), abrir=a("abrir"), after=a("after", 70), premiere=a("premiere"),
           animar=a("animar"), mano=a("mano"), exportar=a("exportar"), volver=a("volver"), timeline=a("timeline", 76), mover=a("mover"), frame1=a("frame", 78),
           frame2=a("frame", 79), calce=a("calce"), multiplica=a("multiplica"), n400=a("400", 84), ya=a("ya", 85), ratito=a("ratito"), hasta=a("hasta", 88),
           semanas=a("semanas", 88), ese=a("ese", 90), trabajo=a("trabajo", 90), pipeline=a("pipeline", 92))
body4 = r"""
      const P0=[1802,1050], S0=0.6, PE=[1560,1040], SE=0.55, PB=[1620,1040];
      const m=actor(svg,false);
      const segs=[
        {type:'at',t0:0,t1:0,at:P0,s:S0},
        {type:'hop',t0:A.editas,t1:A.editas+0.6,from:P0,to:PE,s:[S0,SE],n:2,h:30},
        {type:'hop',t0:A.volver,t1:A.volver+0.4,from:PE,to:[1760,1040],s:[SE,SE],n:1,h:30},
        {type:'hop',t0:A.timeline-0.05,t1:A.timeline+0.3,from:[1760,1040],to:PB,s:[SE,SE],n:1,h:30},
      ];
      const NP=8, PUSH=[]; for(let i=0;i<NP;i++){ const t0=A.mover+0.15+i*0.36; PUSH.push(t0); segs.push({type:'hop',t0:t0,t1:t0+0.16,from:[PB[0]+i*14,1040],to:[PB[0]+(i+1)*14,1040],s:[SE,SE],n:1,h:8}); }
      const PBX=PB[0]+NP*14;
      segs.push({type:'jump',t0:A.calce,t1:A.calce+0.25,from:[PBX,1040],to:[PBX,1040],s:[SE,SE],h:30});
      segs.push({type:'hop',t0:A.multiplica-0.35,t1:A.multiplica,from:[PBX,1040],to:PE,s:[SE,SE],n:1,h:30});
      segs.push({type:'jump',t0:A.n400,t1:A.n400+0.3,from:PE,to:PE,s:[SE,SE],h:40});
      segs.push({type:'jump',t0:A.ese+0.2,t1:A.ese+0.5,from:PE,to:PE,s:[SE,SE],h:36});
      /* laptop pixel a la izquierda del monito (coordenadas del personaje, escala del puesto) */
      const LO=mk("g",{opacity:0}); svg.insertBefore(LO,m.sh);
      const LG=mk("g",{transform:"translate("+PE[0]+" "+PE[1]+") scale("+SE+") translate(-1627 -907)"}); LO.appendChild(LG);
      pixelRect(LG,"f-paper",1150,874,370,34,12);
      const SCR=mk("g",{transform:"rotate(-6 1165 874)"}); LG.appendChild(SCR);
      pixelRect(SCR,"f-paper",1150,608,210,274,16); pixelRect(SCR,"f-ink",1164,622,182,222,10);
      const W1=mk("g",{opacity:0}); SCR.appendChild(W1); pixelRect(W1,"f-paper",1176,650,120,90,4); pixelRect(W1,"f-clay",1176,650,120,12,2);
      const W2=mk("g",{opacity:0}); SCR.appendChild(W2); pixelRect(W2,"f-paper",1206,690,130,100,4); pixelRect(W2,"f-clay-deep",1206,690,130,12,2);
      const PGt=mk("g",{opacity:0}); SCR.appendChild(PGt); pixelRect(PGt,"f-paper",1180,760,150,16,4); const PGf=pixelRect(PGt,"f-clay",1180,760,0,16,4);
      /* rombo (keyframe) y su guía */
      const KG=mk("g",{opacity:0}); svg.appendChild(KG); pixelRect(KG,"f-mute",1300,848,180,2); const KD=mk("rect",{class:"f-clay",x:-12,y:-12,width:24,height:24}); KG.appendChild(KD);
      /* tira (volver al timeline), bloque y ranura (frame a frame) */
      const S4=strip(svg,1660,1012,230,48,[1700,1775,1850],44);
      const SL=mk("rect",{x:PBX+70,y:996,width:44,height:44,fill:"none",stroke:"#faf9f5","stroke-width":3,opacity:0}); svg.appendChild(SL);
      const FL=pixelRect(svg,"f-paper",PBX+70,996,44,44,4); FL.setAttribute("opacity","0");
      const BK=pixelRect(svg,"f-clay",0,0,44,44,4); BK.setAttribute("opacity","0");
      burst(GS,PBX+92,1018,10,81,A.calce,{sp:120,up:50});
      /* multitud gris + pilas de hojas */
      const XS=[]; for(let x=80;x<=1880;x+=78) if(Math.abs(x-PE[0])>=110) XS.push(x);
      const CG=mk("g",{}); svg.appendChild(CG);
      const crowd=XS.map((x,i)=>{ const c=actor(CG,false); grey(c); c.x=x; c.i=i; c.born=A.n400+0.05+Math.abs(x-PE[0])/1500*1.4;
        c.pile=[]; for(let j=0;j<10;j++){ const r=pixelRect(CG,"f-paper",x-33+(prand(i*31+j)-0.5)*12,992-(j+1)*8,66,7,1); r.setAttribute("opacity","0"); c.pile.push({r,t0:A.ratito-0.4+prand(i*7+j*3)*0.5+j*0.2,cx:x,cy:992-(j+1)*8+3.5}); }
        return c; });
      const myPile=[]; for(let j=0;j<13;j++){ const r=pixelRect(CG,"f-paper",PE[0]-85+(prand(j*5)-0.5)*16,1040-(j+1)*12,170,11,2); r.setAttribute("opacity","0"); myPile.push({r,t0:A.ratito-0.2+prand(j*9)*0.4+j*0.19,cx:PE[0],cy:1040-(j+1)*12+5.5}); }
      for(let j=0;j<22;j++){ const xj=90+j*84; burst(GS,xj,1000,4,200+j,A.semanas+0.08+(xj/1920)*0.4,{sp:90,up:60,sz:4,cls:j%2?"f-paper":"f-gris"}); }
      burst(GP,PE[0],PE[1]-70,12,91,A.ese+0.2,{sp:110,up:60});
      function pose(t){
        const st=motion(segs,t,{x:P0[0],y:P0[1],s:S0});
        let o={}; const typing=t>=A.graficas&&t<A.exportar;
        if(t>=A.exportar+0.05&&t<A.volver){ o.arms="down"; o.eyes="squint"; }
        if(t>=A.animar+0.2&&t<A.mano+0.1) o.arms="catch";
        for(const p0 of PUSH) if(t>=p0-0.1&&t<p0+0.2) o.arms="push";
        if(t>=A.ratito&&t<A.hasta+0.3) o.arms="flail";
        if(t>=A.semanas+0.25&&t<A.ese+0.2) o.on=false;
        if(t>=A.ese+0.2) o.scale=pop(t,A.ese+0.2);
        if(t>=A.multiplica&&t<A.n400) o.arms="up";
        actorPose(m,t,st,o);
        /* laptop */
        const ls=pop(t,A.graficas)*fade(t,A.multiplica+0.1); show(LO,ls>0); if(ls>0) xf(LO,1400,1000,ls,ls);
        popDie(W1,t,A.abrir,A.volver,1236,695,{}); popDie(W2,t,A.premiere,A.volver,1271,740,{});
        popDie(PGt,t,A.exportar,A.volver,1255,768,{sy:1}); PGf.setAttribute("width",(150*clamp01((t-A.exportar)/(A.volver-0.05-A.exportar))).toFixed(1));
        /* rombo */
        { const s=pop(t,A.animar)*fade(t,A.exportar); show(KG,s>0); if(s>0){ const q=ease(t,A.animar+0.2,A.mano+0.05); const x=lerp(1300,1480,q)+3*Math.sin(60*t)*(1-q); KD.setAttribute("transform","translate("+x.toFixed(1)+" 849) rotate(45)"); xf(KG,1390,849,s,s); } }
        /* tira, bloque, ranura */
        popDie(S4.g,t,A.volver-0.12,A.mover-0.1,S4.cx,S4.cy,{});
        { const s=pop(t,A.mover)*fade(t,A.multiplica); show(SL,s>0); show(BK,s>0);
          let bx=PBX-48; for(const p0 of PUSH) if(t>=p0+0.1) bx+=14; if(t>=A.calce) bx=PBX+70;
          let bsy=1; for(const p0 of PUSH) if(t>=p0+0.1&&t<p0+0.22) bsy=0.85;
          BK.setAttribute("transform","translate("+bx.toFixed(1)+" 996) translate(22 44) scale("+s.toFixed(3)+" "+(s*bsy).toFixed(3)+") translate(-22 -44)");
          xf(SL,PBX+92,1018,s,s); const fl=t>=A.calce&&t<A.calce+0.25?(1-(t-A.calce)/0.25):0; FL.setAttribute("opacity",fl.toFixed(2)); }
        /* multitud gris */
        crowd.forEach(c=>{ const k=pop(t,c.born)*fade(t,A.semanas+0.05+(c.x/1920)*0.4,0.15); actorPose(c,t,{x:c.x,y:992,s:0.22,air:0,sx:1,sy:1,moving:false},{scale:k,rate:11,tph:c.i*0.19});
          c.pile.forEach(p=>{ const s=pop(t,p.t0,0.2,1.5)*fade(t,A.semanas+0.05+(c.x/1920)*0.4,0.15); show(p.r,s>0); if(s>0) xf(p.r,p.cx,p.cy,s,s); }); });
        myPile.forEach(p=>{ const s=pop(t,p.t0,0.2,1.5)*fade(t,A.semanas+0.05+(PE[0]/1920)*0.4,0.15); show(p.r,s>0); if(s>0) xf(p.r,p.cx,p.cy,s,s); });
        renderParts(GP,t); renderParts(GS,t,320);
      }
""" + COMMON
emit("m4-editor", B4, B5, "M4: el mini editor en su laptop pixel (ventanas, rombo arrastrado, barra de exportar, ida y vuelta, bloque empujado de a un píxel), la multitud gris sepultada por hojas en '400', colapso en 'semanas'.", an4, body4)

# ======================= m5: tubería, crudos entran y salen animados, el sistema por dentro, archivo =======================
an5 = dict(pipeline=a("pipeline", 92), tres=a("tres", 95), cosas=a("cosas", 96), primero=a("primero", 99), corro=a("corro"), vivo=a("vivo"), viendo=a("viendo"),
           entran=a("entran"), crudos=a("crudos"), lado=a("lado"), salen=a("salen"), animados=a("animados"), montados=a("montados"), davinci=a("davinci"),
           resolve=a("resolve", 115), segunda=a("segunda"), abro=a("abro"), dentro=a("dentro"), seis=a("seis"), etapas=a("etapas"), decide=a("decide"),
           claude=a("cloud", 122), no=a("no", 124), personaje=a("personaje", 124), archivo1=a("archivo", 126.5), si=a("sí", 127.5), archivo2=a("archivo", 128.5),
           finalmente=a("finalmente"), promesas=a("promesas"), sigamos=a("sigamos"))
SCENE56 = r"""
      /* --- escena compartida m5/m6: tubería de 6 módulos, tarjetas de etapas (detrás), HUD izquierda, 5 minis + marco --- */
      const TX0=260, TW=200, TY=990, TH=56, NM=6, MXC=[]; for(let i=0;i<NM;i++) MXC.push(TX0+i*TW+TW/2);
      const STG=["cortes","audio","palabras","plan","componer","montar"];
      const stageCards=STG.map((tx,i)=>{ const g=mk("g",{opacity:0}); svg.appendChild(g); const cx=MXC[i], w=168, h=46, x=cx-w/2, y=920;
        const rp=pixelRect(g,"f-paper",x,y,w,h,8), rc=pixelRect(g,"f-clay",x,y,w,h,8); rc.setAttribute("opacity","0");
        const c=3.6, tw=pixelTextWidth(tx,c); const ti=mk("g",{}); g.appendChild(ti); buildPixelText(ti,tx,{x:cx-tw/2,y:y+(h-7*c)/2,cell:c,cls:"f-ink"});
        const tp=mk("g",{opacity:0}); g.appendChild(tp); buildPixelText(tp,tx,{x:cx-tw/2,y:y+(h-7*c)/2,cell:c,cls:"f-paper"});
        return {g,cx,cy:y+h/2,rp,rc,ti,tp}; });
      const TG=mk("g",{}); svg.appendChild(TG);
      const mods=[]; for(let i=0;i<NM;i++){ const g=mk("g",{opacity:0}); TG.appendChild(g); const x=TX0+i*TW;
        pixelRect(g,"f-gris",x+2,TY,TW-4,TH,6); pixelRect(g,"f-paper",x+10,TY+8,TW-20,8,3); const led=mk("circle",{class:"f-clay",cx:x+TW/2,cy:TY+36,r:6,opacity:0.35}); g.appendChild(led);
        mods.push({g,x,cx:x+TW/2,cy:TY+TH/2,led}); }
      const HUD=["1  en vivo, ahora","2  el sistema por dentro","3  lo que cuesta de verdad"].map((tx,i)=>card(svg,tx,74,150+i*86,4.6,"f-ink",16));
      const outs=[0,1,2,3,4].map(i=>{ const c=actor(svg,false); c.i=i; c.lx=1525+i*86; return c; });
      const Zo=zzz(svg);
      const blk2=pixelRect(outs[2].extra,"f-clay-deep",1577,560,100,60,0); const chk3=checkIcon(outs[3].extra,1627,560,46); chk3.g.setAttribute("opacity","1");
      const MARCO=mk("rect",{x:1476,y:950,width:440,height:122,rx:10,fill:"none",stroke:"#faf9f5","stroke-width":4,opacity:0}); svg.appendChild(MARCO);
      /* pose de la escena compartida. T = tiempos absolutos relativos a la pieza */
      function sceneOuts(t,T){ outs.forEach((c,i)=>{ const t0=T.salen+0.05+i*0.28; const segsO=[{type:'jump',t0:t0,t1:t0+0.35,from:[1470,1018],to:[c.lx,1040],s:[0.2,0.25],h:70}];
          if(i===4) for(let k=0;k<70;k++){ const tk=t0+0.9+k*0.7; segsO.push({type:'jump',t0:tk,t1:tk+0.3,from:[c.lx,1040],to:[c.lx,1040],s:[0.25,0.25],h:30}); }
          const cs=motion(segsO,t,{x:1470,y:1018,s:0.2}); const landed=t>=t0+0.35;
          const o={scale:(t>=t0?1:0)*fade(t,T.promesas+0.05+i*0.08),tph:i*0.21};
          if(i===1&&landed){ o.eyes="closed"; o.arms="down"; o.nobob=true; o.sy=0.84; }
          if(i===2&&landed) o.arms="up";
          actorPose(c,t,cs,o);
          if(i===1) zzzPose(Zo,t,t0+0.6,cs.x+16,cs.y-240*0.25*0.84,landed&&t<T.promesas); });
        { const s=pop(t,T.resolve,0.2,1.4)*fade(t,T.promesas); show(MARCO,s>0); if(s>0) xf(MARCO,1696,1011,s,s); } }
"""
body5 = SCENE56 + r"""
      const P0=[1560,1040], PS=0.55, PT=[1380,990], PL=[180,1040];
      const m=actor(svg,false);
      const segs=[
        {type:'at',t0:0,t1:0,at:P0,s:PS},
        {type:'hop',t0:A.pipeline+0.9,t1:A.pipeline+1.25,from:P0,to:PT,s:[PS,0.5],n:1,h:60},
        {type:'jump',t0:A.tres,t1:A.tres+0.25,from:PT,to:PT,s:[0.5,0.5],h:24},
        {type:'hop',t0:A.abro-0.1,t1:A.dentro,from:PT,to:PL,s:[0.5,PS],n:7,h:34},
        {type:'jump',t0:A.personaje,t1:A.personaje+0.28,from:PL,to:PL,s:[PS,PS],h:40},
      ];
      /* minis grises que entran por la boca izquierda */
      const ins=[0,1,2,3,4].map(i=>{ const c=actor(svg,false); grey(c); c.t0=A.entran-0.15+i*0.3; burst(GP,266,1018,6,120+i,c.t0+0.5,{sp:60,up:30,sz:4,cls:"f-gris"}); return c; });
      const DOC=docIcon(svg,135,922,90,118);
      burst(GP,180,960,10,131,A.archivo2+0.26,{sp:90,up:50});
      function pose(t){
        const st=motion(segs,t,{x:P0[0],y:P0[1],s:PS});
        let o={};
        if(t>=A.pipeline&&t<A.pipeline+0.9) o.arms="up";
        if(t>=A.personaje+0.3&&t<A.archivo1) o.arms="pointL";
        let fx=1; if(t>=A.archivo1-0.07&&t<A.archivo2+0.26){ fx=1-clamp01((t-(A.archivo1-0.07))/0.14); } else if(t>=A.archivo2+0.26){ fx=clamp01((t-(A.archivo2+0.26))/0.14); }
        o.sx=fx; actorPose(m,t,st,o);
        /* documento en su lugar */
        { let s=0, dy=0; if(t>=A.archivo1+0.07){ s=clamp01((t-(A.archivo1+0.07))/0.14); } if(t>=A.archivo2+0.12){ s=1-clamp01((t-(A.archivo2+0.12))/0.14); }
          if(t>=A.si&&t<A.si+0.3){ const q=(t-A.si)/0.3; dy=-22*Math.sin(Math.PI*q); }
          show(DOC.g,s>0); if(s>0) DOC.g.setAttribute("transform","translate(0 "+dy.toFixed(1)+") translate("+DOC.cx+" "+(DOC.y+DOC.h)+") scale("+s.toFixed(3)+" 1) translate("+(-DOC.cx)+" "+(-(DOC.y+DOC.h))+")"); }
        /* módulos vuelan y encajan */
        mods.forEach((md,i)=>{ const ti=A.pipeline+0.05+i*0.12; if(t<ti){show(md.g,false);return;} show(md.g,true);
          const q=clamp01((t-ti)/0.35), e=backOut(1.2,q); const dx=(i%2?520:-520)*(1-e), dy=(-300-i*40)*(1-e); let sy=1; if(t>=ti+0.35&&t<ti+0.47) sy=0.85;
          md.g.setAttribute("transform","translate("+dx.toFixed(1)+" "+dy.toFixed(1)+") translate("+md.cx+" "+(TY+TH)+") scale(1 "+sy.toFixed(3)+") translate("+(-md.cx)+" "+(-(TY+TH))+")");
          const bl=t>=A.lado+0.7+i*0.16&&t<A.lado+0.7+i*0.16+0.3; md.led.setAttribute("opacity",bl?"1":"0.35"); });
        /* HUD izquierda: 1 y 2 */
        cardPose(HUD[0],t,A.primero,null); cardPose(HUD[1],t,A.segunda,null); show(HUD[2].g,false);
        /* crudos entran */
        ins.forEach((c,i)=>{ const cs=motion([{type:'hop',t0:c.t0,t1:c.t0+0.5,from:[-60,1040],to:[250,1018],s:[0.25,0.2],n:3,h:30}],t,{x:-60,y:1040,s:0.25});
          actorPose(c,t,cs,{scale:(t>=c.t0?1:0)*fade(t,c.t0+0.5,0.12),tph:i*0.3,arms:"down"}); });
        sceneOuts(t,A);
        /* etapas suben desde la tubería; plan y componer se encienden; el resto se apaga */
        stageCards.forEach((sc,i)=>{ const t0=A.seis-0.3+i*0.1; const q=pop(t,t0,0.35,1.3); show(sc.g,q>0); if(q>0){ sc.g.setAttribute("transform","translate(0 "+(70*(1-q)).toFixed(1)+")"); }
          const lit=(i===3||i===4)&&t>=A.decide+0.05+(i-3)*0.35; sc.rc.setAttribute("opacity",lit?"1":"0"); sc.tp.setAttribute("opacity",lit?"1":"0"); sc.ti.setAttribute("opacity",lit?"0":"1");
          const dim=!(i===3||i===4)&&t>=A.no+0.05; sc.rp.setAttribute("opacity",dim?"0.4":"1"); });
        renderParts(GP,t); renderParts(GS,t,320);
      }
""" + COMMON
emit("m5-tuberia", B5, B6, "M5: la tubería se ensambla en 'pipeline' y él se sube; los crudos grises entran por un lado y salen salmón por el otro, cada uno haciendo algo distinto; el marco de Resolve; las seis etapas suben de la tubería; se pliega en un archivo.", an5, body5)

# ======================= m6: lo que cuesta, repositorio, suscríbete, sigamos =======================
an6 = dict(salen=a("salen"), resolve=a("resolve", 115), finalmente=a("finalmente"), cuesta=a("cuesta", 131), tiempo=a("tiempo", 133), disco=a("disco"),
           iteraciones=a("iteraciones"), sigue=a("sigue"), trabajo=a("trabajo", 137), mio=a("mío"), numeros=a("números"), promesas=a("promesas"),
           queda=a("queda"), repositorio=a("repositorio"), publico=a("público"), gratis=a("gratis"), canal=a("canal", 152), suscribete=a("suscríbete"),
           uno=a("uno", 157), asi=a("así", 159), sigamos=a("sigamos"))
body6 = SCENE56 + r"""
      const P0=[180,1040], PS=0.55, PB=[710,930], PR=[920,990], PF=[1560,1040];
      const m=actor(svg,true);
      const segs=[
        {type:'at',t0:0,t1:0,at:P0,s:PS},
        {type:'jump',t0:A.mio,t1:A.mio+0.25,from:P0,to:P0,s:[PS,PS],h:26},
        {type:'hop',t0:A.suscribete-0.62,t1:A.suscribete,from:P0,to:PB,s:[PS,0.5],n:2,h:60},
        {type:'hop',t0:A.suscribete+0.45,t1:A.suscribete+0.75,from:PB,to:PR,s:[0.5,0.5],n:1,h:40},
        {type:'jump',t0:A.uno,t1:A.uno+0.25,from:PR,to:PR,s:[0.5,0.5],h:26},
        {type:'hop',t0:A.asi,t1:A.asi+0.6,from:PR,to:PF,s:[0.5,PS],n:3,h:34},
        {type:'hop',t0:A.sigamos,t1:A.sigamos+0.9,from:PF,to:[1990,1040],s:[PS,PS],n:3,h:30},
      ];
      seedDissolveParts(m,A.sigamos+0.35,A.sigamos+0.85,37);
      /* objetos sobre la cabeza */
      const RJ=mk("g",{opacity:0}); m.extra.appendChild(RJ); RJ.appendChild(mk("circle",{class:"f-paper",cx:1627,cy:540,r:70})); const RH=pixelRect(RJ,"f-ink",1623,484,8,60); const RH2=pixelRect(RJ,"f-ink",1623,500,8,44);
      const DK=mk("g",{opacity:0}); m.extra.appendChild(DK); pixelRect(DK,"f-gris",1547,490,160,100,8); pixelRect(DK,"f-paper",1547,506,160,16); DK.appendChild(mk("circle",{class:"f-clay",cx:1672,cy:562,r:12}));
      const LP=mk("g",{opacity:0}); m.extra.appendChild(LP); const LPr=mk("g",{}); LP.appendChild(LPr);
      LPr.appendChild(mk("path",{d:"M1567 540 A60 60 0 0 1 1687 540",stroke:"#d07e78","stroke-width":16,fill:"none"})); LPr.appendChild(mk("path",{d:"M1687 540 A60 60 0 0 1 1567 540",stroke:"#ad615c","stroke-width":16,fill:"none"}));
      pixelRect(LPr,"f-clay",1675,522,26,26); pixelRect(LPr,"f-clay-deep",1553,532,26,26);
      /* documento que vuela al repositorio, carpeta, gratis, botón */
      const DOC=docIcon(svg,-30,-39,60,78);
      const FD=folderIcon(svg,1640,940,150,100);
      const GR=card(svg,"gratis",1660,860,6,"f-clay",10);
      const BT=mk("g",{opacity:0}); svg.appendChild(BT); const BTa=mk("g",{}); BT.appendChild(BTa); pixelRect(BTa,"f-paper",560,930,300,70,14);
      { const c=4.4, tw=pixelTextWidth("suscríbete",c); buildPixelText(BTa,"suscríbete",{x:710-tw/2,y:965-3.5*c,cell:c,cls:"f-clay"}); }
      const BTb=mk("g",{opacity:0}); BT.appendChild(BTb); pixelRect(BTb,"f-clay",560,930,300,70,14);
      { const c=4.4, tw=pixelTextWidth("suscríbete",c); buildPixelText(BTb,"suscríbete",{x:710-tw/2,y:965-3.5*c,cell:c,cls:"f-paper"}); }
      burst(GS,710,1000,12,141,A.suscribete,{sp:150,up:60}); burst(GP,1715,960,10,151,A.publico-0.1,{sp:90,up:50});
      for(let j=0;j<18;j++){ const xj=270+j*72; burst(GP,xj,1020,3,300+j,A.sigamos+0.1+(xj-260)/1200*0.7,{sp:60,up:70,sz:4,cls:"f-gris"}); }
      outs.forEach((c,i)=>burst(GP,c.lx,1010,6,160+i,A.promesas+0.05+i*0.08,{sp:70,up:50,sz:4}));
      const WM=waveMask(svg,"t",240,980,1240,80);
      function pose(t){
        const st=motion(segs,t,{x:P0[0],y:P0[1],s:PS});
        let o={}; let dk=0;
        if(t>=A.trabajo&&t<A.mio+0.5) o.arms="pointL";
        if(t>=A.uno&&t<A.uno+0.6) o.arms="up";
        const carrying=t>=A.asi+0.75;
        if(carrying) o.arms="up";
        let dy=0; if(t>=A.suscribete&&t<A.suscribete+0.45){ dy=35*clamp01((t-A.suscribete)/0.12); }
        if(t>=A.sigamos+0.35){ dk=clamp01((t-(A.sigamos+0.35))/0.5); if(dk>=1) o.on=false; }
        dissolve(m,dk);
        const st2={x:st.x,y:st.y+dy,s:st.s,air:st.air,sx:st.sx,sy:st.sy,moving:st.moving};
        actorPose(m,t,st2,o);
        const headY=st2.y-st2.air-240*st2.s;
        /* escena compartida */
        mods.forEach((md,i)=>{ show(md.g,true); md.g.removeAttribute("transform"); md.led.setAttribute("opacity","0.35"); });
        const wv=t>=A.sigamos+0.1; if(wv){ TG.setAttribute("mask",WM.url); WM.set(lerp(240,1480,clamp01((t-(A.sigamos+0.1))/0.7))); }
        cardPose(HUD[0],t,-1,A.sigamos); cardPose(HUD[1],t,-1,A.sigamos); cardPose(HUD[2],t,A.finalmente,A.sigamos);
        sceneOuts(t,A);
        stageCards.forEach((sc,i)=>{ const s=fade(t,A.finalmente+0.05+i*0.06); show(sc.g,s>0); if(s>0) xf(sc.g,sc.cx,sc.cy,s,s);
          const lit=(i===3||i===4); sc.rc.setAttribute("opacity",lit?"1":"0"); sc.tp.setAttribute("opacity",lit?"1":"0"); sc.ti.setAttribute("opacity",lit?"0":"1"); sc.rp.setAttribute("opacity",lit?"1":"0.4"); });
        /* objetos sobre la cabeza */
        popDie(RJ,t,A.tiempo,A.disco,1627,540,{o:1.8}); RH.setAttribute("transform","rotate("+((t-A.tiempo)*450).toFixed(1)+" 1627 540)"); RH2.setAttribute("transform","rotate("+((t-A.tiempo)*37).toFixed(1)+" 1627 540)");
        popDie(DK,t,A.disco,A.iteraciones,1627,540,{o:1.8});
        popDie(LP,t,A.iteraciones,A.sigue,1627,540,{o:1.8}); LPr.setAttribute("transform","rotate("+((t-A.iteraciones)*300).toFixed(1)+" 1627 540)");
        /* documento: nace sobre la cabeza en 'queda', vuela a la carpeta */
        { let s=pop(t,A.queda), x=st2.x, y=headY-70, rot=0; const t0=A.repositorio+0.05, t1=A.publico-0.1;
          if(t>=t0){ const q=ease(t,t0,t1); x=lerp(st2.x,1715,q); y=lerp(headY-70,985,q)-260*Math.sin(Math.PI*q); rot=360*q; if(t>=t1) s=0; }
          show(DOC.g,s>0); if(s>0) DOC.g.setAttribute("transform","translate("+x.toFixed(1)+" "+y.toFixed(1)+") rotate("+rot.toFixed(1)+") scale("+s.toFixed(3)+")"); }
        /* carpeta: pop, rebote al recibir, se va con él */
        { let s=pop(t,A.repositorio-0.1), sy=1, x=FD.cx, y=FD.y+FD.h; const tb=A.publico-0.1; if(t>=tb&&t<tb+0.22){ const k=(t-tb)/0.22; sy=0.72+0.28*k; }
          if(carrying){ const k=ease(t,A.asi+0.75,A.asi+0.95); x=lerp(FD.cx,st2.x,k); y=lerp(FD.y+FD.h,headY-20,k); if(t>=A.sigamos+0.5) s*=1-clamp01((t-(A.sigamos+0.5))/0.3); }
          show(FD.g,s>0); if(s>0) FD.g.setAttribute("transform","translate("+(x-FD.cx).toFixed(1)+" "+(y-(FD.y+FD.h)).toFixed(1)+") translate("+FD.cx+" "+(FD.y+FD.h)+") scale("+s.toFixed(3)+" "+(s*sy).toFixed(3)+") translate("+(-FD.cx)+" "+(-(FD.y+FD.h))+")"); }
        cardPose(GR,t,A.gratis,A.gratis+1.3);
        /* botón: pop antes de 'suscríbete', se hunde al pisarlo, muere con la tubería */
        { const s=pop(t,A.suscribete-0.75)*fade(t,A.sigamos+0.15); show(BT,s>0); const pressed=t>=A.suscribete; const k=pressed?clamp01((t-A.suscribete)/0.12):0;
          if(s>0) BT.setAttribute("transform","translate(710 1000) scale("+s.toFixed(3)+" "+(s*(1-0.5*k)).toFixed(3)+") translate(-710 -1000)"); BTb.setAttribute("opacity",pressed?"1":"0"); BTa.setAttribute("opacity",pressed?"0":"1"); }
        renderParts(m.P,t); renderParts(GP,t); renderParts(GS,t,320);
      }
""" + COMMON
emit("m6-cierre", B6, B7, "M6: reloj, disco y bucle sobre la cabeza; apunta a Nicolás en 'trabajo mío'; el documento vuela al repositorio; pisa el botón de suscribirse; se lleva la carpeta y se disuelve con la tubería en 'sigamos'.", an6, body6)

json.dump(PIEZAS, open(ROOT / "piezas2.json", "w"), indent=1)
print("piezas2.json:", len(PIEZAS), "piezas,", sum(p["frames"] for p in PIEZAS), "frames")
