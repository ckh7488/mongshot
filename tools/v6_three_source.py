"""Open-duct harness renderer derived from the preserved v5 model."""
def build_source(src):
    start=src.index('  // Separate power-return branches');end=src.index('  const door=new T.Group()',start)
    from pathlib import Path
    wiring=Path(__file__).with_name('v61_wire_renderer.jsfrag').read_text(encoding='utf-8')
    src=src[:start]+wiring+src[end:]
    start=src.index('  // DIN ducts:');end=src.index('  function term(',start)
    ducts=r'''  // Lids removed for the assembly view; U-channel bases show routed wires.
  for(const [bay,ducts]of [['upper',model.ducts.upperVertical],['lower',[...model.ducts.lowerVertical,...model.ducts.lowerHorizontal]]])for(const [x,y,w,h]of ducts){
    const p=world(bay,x+w/2,y+h/2),horizontal=w>h;
    const dg=(model.ducts.groups||[]).find(d=>d.bay===bay&&d.rect.every((v,i)=>v===[x,y,w,h][i]));
    const floor=dg?.group==='power'?0xe0b795:dg?0x92cdc4:0xc6d3dc;
    const ww=horizontal?w:model.ducts.actualWidthMm,hh=horizontal?model.ducts.actualWidthMm:h;box(cabinet,p.x,p.y,3,ww,hh,4,floor);
    if(horizontal){for(const s of [-1,1])box(cabinet,p.x,p.y+s*(hh/2-.8),13,ww,1.6,22,0xb6c5ce);}
    else{for(const s of [-1,1])box(cabinet,p.x+s*(ww/2-.8),p.y,13,1.6,hh,22,0xb6c5ce);}
  }
'''
    src=src[:start]+ducts+src[end:]
    src=src.replace("const curve=new T.CatmullRomCurve3(points.map(v=>new T.Vector3(...v)),false,'centripetal');","const curve=new T.CurvePath();for(let i=1;i<points.length;i++){const a=new T.Vector3(...points[i-1]),b=new T.Vector3(...points[i]);if(a.distanceTo(b)>.01)curve.add(new T.LineCurve3(a,b));}")
    src=src.replace("plateText(cabinet,'하부 · 절연 제어'","plateText(cabinet,'하부 · 직결 / 전력·신호 분리'")
    src=src.replace("'gnd':'G0','logic-positive':'5L'","'gnd':'G','logic-positive':'5V'")
    src=src.replace("if(hit)select(hit.object.userData.partId);","if(hit){if(hit.object.userData.trunkId)options.onTrunkSelect?.(hit.object.userData.trunkId);else if(hit.object.userData.routeId)options.onRouteSelect?.(hit.object.userData.routeId);else select(hit.object.userData.partId);}")
    src=src.replace("wireGroup.visible=e.currentTarget.classList.contains('active');host.dataset.wires=String(wireGroup.visible);dirty=true;","emphasis(e.currentTarget.classList.contains('active'));host.dataset.wires=String(e.currentTarget.classList.contains('active'));dirty=true;")
    src=src.replace("if(wireGroup.visible!==shown){wireGroup.visible=shown;dirty=true;}","if(host.dataset.wires!==String(shown))emphasis(shown);wireGroup.visible=true;")
    src=src.replace("labelLayout();if(selection.visible)","labelLayout();wireLabelLayout();if(selection.visible)")
    src=src.replace("select('isogpio');","")
    src=src.replace('return {fit,zoom,select,renderer,controls,camera,scene,','return {fit,zoom,select,highlightRoute,setWireMode,renderer,controls,camera,scene,')
    src=src.replace("pinrow(group,-w/2+4,h/2-3,3,8)","pinrow(group,-w/2+4,-h/2+3,3,8)")
    return src
