"""Open-duct harness renderer derived from the preserved v5 model."""
def build_source(src):
    start=src.index('  // Separate power-return branches');end=src.index('  const door=new T.Group()',start)
    wiring=r'''  wireGroup.visible=true;
  const wireMeshes=[],wireLabels=[];let highlightedRoute=null,showWireLabels=true;
  const terminalHeight={smps:47,ac:65,pe:26,'amp-adapter':30,rfidbox:45,amp:35,mp3:20,relayA:24,relayB:24,l298:26,buck:20,gnd:45,'logic-positive':45,'power-ground':45,'mag-power':45,uno:23};
  function terminalZ(pt){const p=items.find(p=>{const y=p.bodyY+(p.bay==='lower'?330:0);return pt[0]>=p.bodyX-.2&&pt[0]<=p.bodyX+p.bodyW+.2&&pt[1]>=y-.2&&pt[1]<=y+p.bodyH+.2;});return p?terminalHeight[p.id]||25:20;}
  const labelIds=new Set(['TRK-P','CAB-MOT','CAB-RLY','CAB-MP3-SIG','MAG1-FEED','AUD-SIG','PANEL-SIG']);
  for(const r of data.routes){
    const pts=r.points.map(([x,y],i)=>[x-200,445-y,i===0||i===r.points.length-1?terminalZ([x,y]):20]);
    const mesh=tube(pts,r.color,r.kind==='CTL'?1.7:r.returnWire?1.05:.85);
    mesh.userData.routeId=r.id;mesh.userData.returnWire=r.returnWire;wireMeshes.push(mesh);picks.push(mesh);
    if(labelIds.has(r.id)){
      const p=r.points[Math.max(1,Math.floor(r.points.length/2))];
      const el=document.createElement('button');el.className='three-wire-label';el.type='button';el.dataset.route=r.id;el.style.borderLeftColor=r.color;
      el.textContent={'TRK-P':'TRK · 12V ±','CAB-MOT':'모터 제어 · 3선','CAB-RLY':'릴레이 제어 · 6선','CAB-MP3-SIG':'MP3 · UART + 전원','MAG1-FEED':'자석3 · 전원/귀환','AUD-SIG':'오디오 L/R/G','PANEL-SIG':'도어 · J7'}[r.id];
      el.addEventListener('click',()=>options.onRouteSelect?.(r.id));host.appendChild(el);wireLabels.push({el,r,anchor:new T.Vector3(p[0]-200,445-p[1],40)});
    }
  }
  function emphasis(on){
    const picked=data.routes.find(r=>r.id===highlightedRoute),cables=new Set(picked?data.wires.filter(w=>picked.labels.includes(w.label)).map(w=>w.cable):[]);
    for(const m of wireMeshes){const r=data.routes.find(r=>r.id===m.userData.routeId),match=!picked||data.wires.some(w=>r.labels.includes(w.label)&&cables.has(w.cable));m.material.transparent=true;m.material.opacity=match&&(!on||m.userData.returnWire)?1:.09;}
    dirty=true;
  }
  function highlightRoute(id){highlightedRoute=id;host.dataset.route=id||'';emphasis(document.getElementById('power-layer').classList.contains('active'));}
  function wireLabelLayout(){const W=host.clientWidth,H=host.clientHeight;let placed=[];
    for(const l of wireLabels){const q=l.anchor.clone().project(camera),x=(q.x+1)*W/2,y=(1-q.y)*H/2;l.el.hidden=!showWireLabels||y<35||y>H-90||q.z>1;if(l.el.hidden)continue;let yy=y;for(const p of placed)if(Math.abs(p.x-x)<150&&Math.abs(p.y-yy)<25)yy=p.y+26;placed.push({x,y:yy});l.el.style.left=Math.max(190,Math.min(W-320,x+12))+'px';l.el.style.top=Math.min(H-110,yy)+'px';}
  }
  host.querySelector('[data-3d="wirelabels"]').addEventListener('click',e=>{showWireLabels=!showWireLabels;e.currentTarget.setAttribute('aria-pressed',String(showWireLabels));dirty=true;});
'''
    src=src[:start]+wiring+src[end:]
    start=src.index('  // DIN ducts:');end=src.index('  function term(',start)
    ducts=r'''  // Lids removed for the assembly view; U-channel bases show routed wires.
  for(const [bay,ducts]of [['upper',model.ducts.upperVertical],['lower',[...model.ducts.lowerVertical,...model.ducts.lowerHorizontal]]])for(const [x,y,w,h]of ducts){
    const p=world(bay,x+w/2,y+h/2),horizontal=w>h;
    const dg=(model.ducts.groups||[]).find(d=>d.bay===bay&&d.rect.every((v,i)=>v===[x,y,w,h][i]));
    const floor=dg?.group==='power'?0xe0b795:dg?0x92cdc4:0xc6d3dc;
    box(cabinet,p.x,p.y,3,w,h,4,floor);
    if(horizontal){for(const s of [-1,1])box(cabinet,p.x,p.y+s*(h/2-.8),13,w,1.6,22,0xb6c5ce);}
    else{for(const s of [-1,1])box(cabinet,p.x+s*(w/2-.8),p.y,13,1.6,h,22,0xb6c5ce);}
  }
'''
    src=src[:start]+ducts+src[end:]
    src=src.replace("const curve=new T.CatmullRomCurve3(points.map(v=>new T.Vector3(...v)),false,'centripetal');","const curve=new T.CurvePath();for(let i=1;i<points.length;i++){const a=new T.Vector3(...points[i-1]),b=new T.Vector3(...points[i]);if(a.distanceTo(b)>.01)curve.add(new T.LineCurve3(a,b));}")
    src=src.replace("plateText(cabinet,'하부 · 절연 제어'","plateText(cabinet,'하부 · 직결 / 전력·신호 분리'")
    src=src.replace("'gnd':'G0','logic-positive':'5L'","'gnd':'G','logic-positive':'5V'")
    src=src.replace("if(hit)select(hit.object.userData.partId);","if(hit){if(hit.object.userData.routeId)options.onRouteSelect?.(hit.object.userData.routeId);else select(hit.object.userData.partId);}")
    src=src.replace("wireGroup.visible=e.currentTarget.classList.contains('active');host.dataset.wires=String(wireGroup.visible);dirty=true;","emphasis(e.currentTarget.classList.contains('active'));host.dataset.wires=String(e.currentTarget.classList.contains('active'));dirty=true;")
    src=src.replace("if(wireGroup.visible!==shown){wireGroup.visible=shown;dirty=true;}","if(host.dataset.wires!==String(shown))emphasis(shown);wireGroup.visible=true;")
    src=src.replace("labelLayout();if(selection.visible)","labelLayout();wireLabelLayout();if(selection.visible)")
    src=src.replace("select('isogpio')","select('power-ground')")
    src=src.replace('return {fit,zoom,select,renderer,controls,camera,scene,','return {fit,zoom,select,highlightRoute,renderer,controls,camera,scene,')
    return src
