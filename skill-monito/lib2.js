/* LIB2: actuación del monito sobre la mesa. Se inlinea después de LIB (gen.py). */
const pop=(t,t0,d,o)=>{d=d||0.3;o=o==null?1.6:o;if(t<t0)return 0;return t-t0<d?backOut(o,(t-t0)/d):1;};
const fade=(t,t1,d)=>{d=d||0.10;if(t1==null||t<t1)return 1;const k=clamp01((t-t1)/d);return 1-k*k;};
const lerp=(a,b,k)=>a+(b-a)*k;
const smooth=k=>{k=clamp01(k);return k*k*(3-2*k);};
const ease=(t,t0,t1)=>smooth((t-t0)/(t1-t0));
function xf(el,cx,cy,sx,sy,rot){ el.setAttribute("transform","translate("+cx.toFixed(2)+" "+cy.toFixed(2)+") rotate("+(rot||0).toFixed(2)+") scale("+sx.toFixed(4)+" "+(sy==null?sx:sy).toFixed(4)+") translate("+(-cx).toFixed(2)+" "+(-cy).toFixed(2)+")"); }
function show(el,on){ el.setAttribute("opacity",on?"1":"0"); }
/* pop + muerte de un grupo alrededor de (cx,cy); devuelve la escala aplicada */
function popDie(el,t,t0,t1,cx,cy,o){ o=o||{}; const s=pop(t,t0,o.d,o.o)*fade(t,t1,o.fd); show(el,s>0); if(s>0) xf(el,cx,cy,s*(o.sx||1),s*(o.sy||1),o.rot||0); return s; }
/* monito con rotación alrededor de los pies */
function placeEx(m,cx,cy,sx,sy,rot){ m.g.setAttribute("transform","translate("+cx.toFixed(2)+" "+cy.toFixed(2)+") rotate("+(rot||0).toFixed(2)+") scale("+sx.toFixed(4)+" "+(sy==null?sx:sy).toFixed(4)+") translate(-1627 -907)"); }
/* sombra de contacto */
function shadow(parent){ const e=mk("ellipse",{fill:"#000",opacity:0}); parent.appendChild(e); return e; }
function shadowPose(sh,cx,cy,s,air,on){ if(!on){sh.setAttribute("opacity","0");return;} const k=clamp01(1-air/140); sh.setAttribute("cx",cx.toFixed(1)); sh.setAttribute("cy",(cy+3).toFixed(1)); sh.setAttribute("rx",(150*s*(0.7+0.3*k)).toFixed(1)); sh.setAttribute("ry",(14*s*(0.6+0.4*k)).toFixed(1)); sh.setAttribute("opacity",(0.24*k).toFixed(3)); }
function eyes(m,mode){ const h=mode==="closed"?6:mode==="squint"?22:48, y=mode==="closed"?736:mode==="squint"?728:715; for(const e of [m.ojoI,m.ojoD]){e.setAttribute("height",h);e.setAttribute("y",y);} }
/* brazos: type | down | up | flail | pointL | push | catch */
function arms(m,mode,t,rate){ rate=rate||7; let yl=763,yr=763,xl=1439,xr=1771,hl=48,hr=48;
  if(mode==="type"){ yl=763-Math.round(6*Math.max(0,Math.sin(TAU*rate*t))); yr=763-Math.round(6*Math.max(0,Math.sin(TAU*rate*t+Math.PI))); }
  else if(mode==="up"){ yl=yr=636; }
  else if(mode==="catch"){ yl=yr=690; xl=1455; xr=1755; }
  else if(mode==="flail"){ yl=700+Math.round(44*Math.sin(TAU*5*t)); yr=700+Math.round(44*Math.sin(TAU*5*t+2)); }
  else if(mode==="pointL"){ yl=640; hl=120; xl=1425; }
  else if(mode==="push"){ xr=1800; yr=792; xl=1455; yl=770; }
  m.brI.setAttribute("y",yl); m.brD.setAttribute("y",yr); m.brI.setAttribute("x",xl); m.brD.setAttribute("x",xr); m.brI.setAttribute("height",hl); m.brD.setAttribute("height",hr); }
function grey(m){ for(const r of [...m.patas,m.body.childNodes[4],m.brI,m.brD]) if(r&&r.setAttribute) r.setAttribute("class","f-gris"); }
/* pista de movimiento: segmentos {type:'hop'|'jump'|'at', t0,t1, from,to | at, s:[s0,s1]|s, h, n} */
function motion(segs,t,def){
  const st={x:def.x,y:def.y,s:def.s,air:0,sx:1,sy:1,moving:false};
  for(const sg of segs){
    if(t<sg.t0) break;
    const q=sg.t1>sg.t0?clamp01((t-sg.t0)/(sg.t1-sg.t0)):1;
    if(sg.type==="hop"){ const n=sg.n||Math.max(1,Math.round(Math.hypot(sg.to[0]-sg.from[0],sg.to[1]-sg.from[1])/140));
      st.x=lerp(sg.from[0],sg.to[0],q); st.y=lerp(sg.from[1],sg.to[1],q); if(sg.s!=null) st.s=lerp(sg.s[0],sg.s[1],q);
      const ph=frac(q*n-1e-6), H=sg.h||28;
      if(q<1){ st.air=H*Math.sin(Math.PI*ph); st.moving=true; if(ph<0.12||ph>0.88){st.sx=1.10;st.sy=0.88;} else {st.sx=0.96;st.sy=1.06;} }
      else { st.air=0; st.moving=false; const dt=t-sg.t1; if(dt<0.12){st.sx=1.12;st.sy=0.86;} }
    } else if(sg.type==="jump"){ const H=sg.h||120; st.x=lerp(sg.from[0],sg.to[0],q); st.y=lerp(sg.from[1],sg.to[1],q); if(sg.s!=null) st.s=lerp(sg.s[0],sg.s[1],q);
      if(q<1){ st.air=H*4*q*(1-q); st.moving=true; st.sx=0.92; st.sy=1.12; } else { st.air=0; st.moving=false; const dt=t-sg.t1; if(dt<0.16){const k=dt/0.16; st.sx=1+0.24*(1-k); st.sy=1-0.28*(1-k);} }
    } else if(sg.type==="at"){ st.x=sg.at[0]; st.y=sg.at[1]; if(sg.s!=null) st.s=sg.s; st.air=0; st.moving=false; }
  }
  return st;
}
function actor(parent,withMask){ const m=makeMonito(parent,withMask); m.sh=shadow(parent); parent.insertBefore(m.sh,m.g); m.P=m.P||[]; return m; }
/* o: {on, scale, arms, eyes, sx, sy, rot, shadow, rate, nobob} */
function actorPose(m,t,st,o){ o=o||{}; const on=o.on!==false&&(o.scale==null||o.scale>0.001)&&(o.sx==null||o.sx>0.001);
  if(!on){ m.g.setAttribute("opacity","0"); m.sh.setAttribute("opacity","0"); return; }
  m.g.setAttribute("opacity","1");
  const s=st.s*(o.scale==null?1:o.scale);
  const bobv=(st.moving||o.nobob)?0:Math.round(2*Math.sin(TAU*2*t));
  m.bob.setAttribute("transform","translate(0 "+bobv+")");
  arms(m,o.arms||(st.moving?"down":"type"),t+(o.tph||0),o.rate); eyes(m,o.eyes||"open");
  placeEx(m,st.x,st.y-st.air,s*st.sx*(o.sx==null?1:o.sx),s*st.sy*(o.sy==null?1:o.sy),o.rot||0);
  shadowPose(m.sh,st.x,st.y,s,st.air,o.shadow!==false);
}
/* partículas globales: GP flota (G<0), GS salpica y cae (G>0) */
const GP=[], GS=[]; const gparts=mk("g",{});
function burst(arr,x,y,n,seed,tb,o){ o=o||{}; for(let i=0;i<n;i++){ const ang=o.arc?(-Math.PI*(0.15+0.7*prand(seed+i*5))):((i/n)*TAU+prand(seed+i)*0.5); const sp=(o.sp||90)*(0.6+prand(seed+i*3)*0.8);
  const el=mk("rect",{width:o.sz||5,height:o.sz||5,opacity:0,class:o.cls||(i%2?"f-clay":"f-clay-deep")}); gparts.appendChild(el);
  arr.push({el,ox:x,oy:y,b:tb,life:(o.life||0.25)+prand(seed+i*7)*0.15,vx:Math.cos(ang)*sp,vy:Math.sin(ang)*sp-(o.up==null?40:o.up)}); } }
/* partículas que CONVERGEN hacia el cuerpo del monito (nacer desde partículas) */
function seedGatherParts(m,t0,t1,seed){
  for(let n=0;n<44;n++){ const ox=1483+prand(seed+n*13)*288, oy=667+prand(seed+n*7+1)*192; const life=0.3+prand(seed+n*11)*0.12;
    const birth=t0+((oy-667)/192)*(t1-t0)-life; const vx=(prand(seed+n*5)-0.5)*120, vy=(60+prand(seed+n*3)*80);
    const el=mk("rect",{width:5,height:5,opacity:0,class:n%2?"f-clay":"f-clay-deep"}); m.parts.appendChild(el);
    m.P.push({el,ox:ox-vx*life,oy:oy-vy*life,b:birth,life,vx,vy}); } }
/* máscara de ola: borra de izquierda a derecha hasta front */
function waveMask(parent,id,x0,y0,w,h){ const defs=mk("defs",{}); parent.appendChild(defs);
  defs.innerHTML='<linearGradient id="wg'+id+'" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient><mask id="wm'+id+'" maskUnits="userSpaceOnUse" x="'+(x0-100)+'" y="'+y0+'" width="'+(w+200)+'" height="'+h+'"><rect id="wmr'+id+'" x="'+x0+'" y="'+y0+'" width="'+w+'" height="'+h+'" fill="white"/><rect id="wmg'+id+'" x="'+(x0-80)+'" y="'+y0+'" width="80" height="'+h+'" fill="url(#wg'+id+')"/></mask>';
  return {url:"url(#wm"+id+")",set:(front)=>{ const r=$("wmr"+id), g=$("wmg"+id); if(!r)return; r.setAttribute("x",front.toFixed(1)); r.setAttribute("width",Math.max(0,x0+w-front).toFixed(1)); g.setAttribute("x",(front-80).toFixed(1)); }}; }
/* utilería pixel */
function pixelRect(parent,cls,x,y,w,h,rx){ const r=mk("rect",{class:cls,x,y,width:w,height:h}); if(rx) r.setAttribute("rx",rx); parent.appendChild(r); return r; }
function docIcon(parent,x,y,w,h){ const g=mk("g",{opacity:0}); parent.appendChild(g); pixelRect(g,"f-paper",x,y,w,h,4);
  for(let i=0;i<5;i++) pixelRect(g,"f-ink",x+w*0.16,y+h*0.42+i*h*0.1,w*0.68*(i===4?0.5:1),h*0.045);
  pixelRect(g,"f-clay",x+w*0.16,y+h*0.12,w*0.26,h*0.2); return {g,cx:x+w/2,cy:y+h/2,x,y,w,h}; }
function folderIcon(parent,x,y,w,h){ const g=mk("g",{opacity:0}); parent.appendChild(g); pixelRect(g,"f-clay-deep",x,y-h*0.18,w*0.42,h*0.3,4); pixelRect(g,"f-clay",x,y,w,h,5); pixelRect(g,"f-paper",x+w*0.1,y+h*0.3,w*0.8,h*0.55,3);
  return {g,cx:x+w/2,cy:y+h/2,x,y,w,h}; }
function checkIcon(parent,cx,cy,r){ const g=mk("g",{opacity:0}); parent.appendChild(g); g.appendChild(mk("circle",{class:"f-green",cx,cy,r}));
  g.appendChild(mk("path",{d:"M"+(cx-r*0.52)+" "+(cy+r*0.02)+" L"+(cx-r*0.12)+" "+(cy+r*0.44)+" L"+(cx+r*0.56)+" "+(cy-r*0.46),stroke:"#faf9f5","stroke-width":(r*0.24).toFixed(1),fill:"none","stroke-linecap":"square"})); return {g,cx,cy,r}; }
function digitBox(parent,n,bx,by,B){ const g=mk("g",{opacity:0}); parent.appendChild(g); pixelRect(g,"f-clay",bx,by,B,B,Math.round(B*0.14));
  const c=B*0.105; buildPixelText(g,String(n),{x:bx+(B-pixelTextWidth(String(n),c))/2,y:by+(B-7*c)/2,cell:c,cls:"f-paper"}); return {g,cx:bx+B/2,cy:by+B/2}; }
/* tira de timeline: paper con ranuras; slots[i] = {x,w,fill} */
function strip(parent,x,y,w,h,xs,sw){ const g=mk("g",{opacity:0}); parent.appendChild(g); pixelRect(g,"f-paper",x,y,w,h,8);
  const slots=xs.map(cx=>{ const f=pixelRect(g,"f-clay",cx-sw/2,y+6,sw,h-12,3); f.setAttribute("opacity","0"); pixelRect(g,"f-mute",cx-sw/2-3,y+6,3,h-12); return {cx,fill:f}; });
  return {g,cx:x+w/2,cy:y+h/2,slots,x,y,w,h}; }
/* zZZ sobre un punto (hx,hy), ciclo 1.4 s */
function zzz(parent){ const Ls=[4,5.5,7].map(c=>{ const g=mk("g",{opacity:0}); parent.appendChild(g); buildPixelText(g,"z",{x:0,y:0,cell:c,cls:"f-ink"}); return g; }); return Ls; }
function zzzPose(Ls,t,t0,hx,hy,on){ Ls.forEach((g,i)=>{ if(!on||t<t0){show(g,false);return;} const p=frac((t-t0)/1.4-i*0.33); const o=p<0.15?p/0.15:p>0.8?(1-p)/0.2:1; show(g,o>0.02); g.setAttribute("opacity",o.toFixed(2)); g.setAttribute("transform","translate("+(hx+20+i*22+p*18).toFixed(1)+" "+(hy-30-i*26-p*40).toFixed(1)+")"); }); }
