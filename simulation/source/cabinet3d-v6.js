/* Original dimension-driven Three.js cabinet model; no network assets. */
import * as T from '../vendor/three/three.module.js';
import {OrbitControls} from '../vendor/three/OrbitControls.js';

export function mount(host,data,options={}){
  const model=data.model,items=model.parts;
  const colors={P0:0xb87a3d,G0:0x148c83,A0:0x9673ad,PE:0x749849,BOUNDARY:0x526c94};
  const scene=new T.Scene();scene.background=new T.Color(0xecf1f5);
  const renderer=new T.WebGLRenderer({antialias:true,alpha:false,preserveDrawingBuffer:true,powerPreference:'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.0;
  renderer.domElement.setAttribute('aria-label','3D 배전함: 휠 확대, 왼쪽 드래그 회전, 오른쪽 드래그 이동');renderer.domElement.setAttribute('role','img');host.appendChild(renderer.domElement);
  const leader=document.createElementNS('http://www.w3.org/2000/svg','svg');leader.setAttribute('class','three-leader');leader.innerHTML='<path fill="none" stroke="#ba9141" stroke-width="1.4" stroke-dasharray="4 3"/><circle r="4" fill="#ba9141"/>';host.appendChild(leader);
  const camera=new T.OrthographicCamera(-600,600,500,-500,1,10000);
  camera.position.set(650,260,2200);
  const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.1;controls.zoomToCursor=true;controls.minZoom=.25;controls.maxZoom=15;controls.maxPolarAngle=Math.PI*.93;
  controls.target.set(0,0,40);controls.update();
  scene.add(new T.HemisphereLight(0xffffff,0xa8b7c6,1.8));
  for(const [x,y,z,intensity]of [[-550,1000,1300,2],[700,100,1000,1]]){const l=new T.DirectionalLight(0xffffff,intensity);l.position.set(x,y,z);scene.add(l);}
  const cabinet=new T.Group();scene.add(cabinet);const picks=[],partGroups=new Map(),partAnchors=new Map(),labels=[],wireGroup=new T.Group();cabinet.add(wireGroup);wireGroup.visible=false;
  const metal=new T.MeshStandardMaterial({color:0xadb9c3,metalness:.65,roughness:.45});
  const paint=new T.MeshStandardMaterial({color:0xdce4ea,metalness:.25,roughness:.6});
  const mat=(color,metalness=.12,roughness=.5)=>new T.MeshStandardMaterial({color,metalness,roughness});
  function box(parent,x,y,z,w,h,d,material,r=0){const mesh=new T.Mesh(new T.BoxGeometry(w,h,d),typeof material==='number'?mat(material):material);mesh.position.set(x,y,z);parent.add(mesh);return mesh;}
  function cyl(parent,x,y,z,rad,len,material,axis='z',segments=18){const a=new T.Mesh(new T.CylinderGeometry(rad,rad,len,segments),typeof material==='number'?mat(material):material);if(axis==='z')a.rotation.x=Math.PI/2;if(axis==='x')a.rotation.z=Math.PI/2;a.position.set(x,y,z);parent.add(a);return a;}
  const textCache=new Map();
  function textTexture(text,w=512,h=128,color='#233f50',bg='#edf2f5',size=38){const key=[text,w,h,color,bg,size].join('|');if(textCache.has(key))return textCache.get(key);const c=document.createElement('canvas');c.width=w;c.height=h;const ctx=c.getContext('2d');ctx.fillStyle=bg;ctx.fillRect(0,0,w,h);ctx.font=`600 ${size}px "Malgun Gothic",Arial`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=color;ctx.fillText(text,w/2,h/2,w-20);const tex=new T.CanvasTexture(c);tex.colorSpace=T.SRGBColorSpace;textCache.set(key,tex);return tex;}
  function plateText(parent,text,x,y,z,w,h,color='#233f50',bg='#edf2f5'){
    const p=new T.Mesh(new T.PlaneGeometry(w,h),new T.MeshBasicMaterial({map:textTexture(text,512,128,color,bg),side:T.DoubleSide,transparent:false}));p.position.set(x,y,z);parent.add(p);return p;
  }
  function tube(points,color,r=1,parent=wireGroup){const curve=new T.CurvePath();for(let i=1;i<points.length;i++){const a=new T.Vector3(...points[i-1]),b=new T.Vector3(...points[i]);if(a.distanceTo(b)>.01)curve.add(new T.LineCurve3(a,b));}const mesh=new T.Mesh(new T.TubeGeometry(curve,Math.max(16,points.length*8),r,5,false),mat(color,.1,.65));parent.add(mesh);return mesh;}
  function frame(top,height){const center=top-height/2;
    box(cabinet,0,center,-4,400,height,8,metal);
    box(cabinet,-211,center,58,18,height+30,136,paint);box(cabinet,211,center,58,18,height+30,136,paint);
    box(cabinet,0,top+10,58,440,18,136,paint);box(cabinet,0,top-height-10,58,440,18,136,paint);
    // Visible fastening hardware and a fine coordinate grid on the actual backplate.
    for(const x of [-186,186])for(const y of [top-15,top-height+15])cyl(cabinet,x,y,3,3,2,0x7d8d98);
    const lines=[];for(let x=-200;x<=200;x+=50)lines.push(x,top,1,x,top-height,1);for(let y=top;y>=top-height;y-=50)lines.push(-200,y,1,200,y,1);
    const geo=new T.BufferGeometry();geo.setAttribute('position',new T.Float32BufferAttribute(lines,3));cabinet.add(new T.LineSegments(geo,new T.LineBasicMaterial({color:0xc1cdd6,transparent:true,opacity:.55})));
  }
  const top=445,lowerTop=115;frame(top,260);frame(lowerTop,560);
  // The passage is a representation of the existing opening, not a proposed new hole.
  box(cabinet,0,150,16,265,25,20,0x34495a);plateText(cabinet,'기존 상하 관통구',0,150,27,150,17,'#eff5f7','#34495a');
  plateText(cabinet,'상부 · 전원',0,472,55,180,19);plateText(cabinet,'하부 · 직결 / 전력·신호 분리',0,-475,55,210,19);
  function world(bay,x,y,z=10){return new T.Vector3(-200+x,(bay==='upper'?top:lowerTop)-y,z);}
  // Lids removed for the assembly view; U-channel bases show routed wires.
  for(const [bay,ducts]of [['upper',model.ducts.upperVertical],['lower',[...model.ducts.lowerVertical,...model.ducts.lowerHorizontal]]])for(const [x,y,w,h]of ducts){
    const p=world(bay,x+w/2,y+h/2),horizontal=w>h;
    const dg=(model.ducts.groups||[]).find(d=>d.bay===bay&&d.rect.every((v,i)=>v===[x,y,w,h][i]));
    const floor=dg?.group==='power'?0xe0b795:dg?0x92cdc4:0xc6d3dc;
    const ww=horizontal?w:model.ducts.actualWidthMm,hh=horizontal?model.ducts.actualWidthMm:h;box(cabinet,p.x,p.y,3,ww,hh,4,floor);
    if(horizontal){for(const s of [-1,1])box(cabinet,p.x,p.y+s*(hh/2-.8),13,ww,1.6,22,0xb6c5ce);}
    else{for(const s of [-1,1])box(cabinet,p.x+s*(ww/2-.8),p.y,13,1.6,hh,22,0xb6c5ce);}
  }
  function term(parent,x,y,z,count=2,color=0x6ea0b8){box(parent,x,y,z,Math.max(9,count*5.5),11,9,color);for(let i=0;i<count;i++){const xx=x-(count-1)*2.75+i*5.5;cyl(parent,xx,y,z+5,1.5,1,0x455e6d);box(parent,xx,y-3,z+5,2,2,1,0xe7aa54);}}
  function pcb(parent,w,h){box(parent,0,0,1.2,w,h,2.4,0x24786c);for(const x of [-w/2+4,w/2-4])for(const y of [-h/2+4,h/2-4])cyl(parent,x,y,3,1.8,1,0xbcbca1);}
  function pinrow(parent,x,y,z,num,vertical=false){for(let i=0;i<num;i++){const xx=vertical?x:x+i*2.54,yy=vertical?y-i*2.54:y;box(parent,xx,yy,z,2,2,5,0x303c44);cyl(parent,xx,yy,z+3,.35,2,0xc7ae65,undefined,8);}}
  for(const p of items){
    const group=new T.Group(),w=p.bodyW,h=p.bodyH,d=p.bodyD;
    const center=world(p.bay,p.x+p.reserveW/2,p.y+(p.bodyOffsetY??4)+h/2,12);group.position.copy(center);cabinet.add(group);partGroups.set(p.id,group);partAnchors.set(p.id,center.clone().add(new T.Vector3(0,0,d+8)));
    const id=p.id;
    if(id==='smps'){
      box(group,0,0,d/2,w,h,d,metal);box(group,0,5,d+.5,w-5,h-26,1,0xc2ccd4);
      const holes=new T.InstancedMesh(new T.CylinderGeometry(1.8,1.8,.8,10),mat(0x506472),16*7);const dummy=new T.Object3D();let idx=0;
      for(let row=0;row<7;row++)for(let col=0;col<16;col++){dummy.position.set(-w/2+9+col*9,-h/2+28+row*12,d+1.2);dummy.rotation.x=Math.PI/2;dummy.updateMatrix();holes.setMatrixAt(idx++,dummy.matrix);}group.add(holes);
      plateText(group,'LRS-200-12',w/2-39,20,d+2,66,35);term(group,0,-h/2+7,d+4,7,0x455967);plateText(group,'L N PE  V− V− V+ V+',0,-h/2-1,d+10,185,9);
    }else if(id==='uno'){
      pcb(group,w,h);box(group,-w/2+7,h/2-12,9,15,12,14,metal);box(group,-w/2+7,-h/2+9,7,13,10,11,0x2f3d47);
      box(group,4,-5,5,30,10,5,0x283840);box(group,-5,12,4,9,8,3,0x52616d);
      pinrow(group,-w/2+24,h/2-4,5,14);pinrow(group,-w/2+24,-h/2+4,5,12);
      for(let j=0;j<6;j++)box(group,-12+j*5,-h/2+14,3,3,1.5,1,0xe1c37b);
      plateText(group,'UNO',6,10,7,23,10,'#f2f6f6','#24786c');
    }else if(id==='relayA'||id==='relayB'){
      pcb(group,w,h);for(let i=0;i<4;i++){const x=-w/2+12+i*18;box(group,x,3,11,16,22,20,0x2e77af);plateText(group,'SRD 5V',x,3,21.5,14,8,'#eff5fa','#2e77af');term(group,x,h/2-7,6,3,0x69a78d);box(group,x,-h/2+10,3,5,6,3,0xf0e9d2);cyl(group,x+4,-h/2+17,4,1.3,1,0xd77146);}
      pinrow(group,-8,-h/2+3,4,6);
    }else if(id==='rfidbox'){
      box(group,0,0,d/2,w,h,d,0xc7cfd6);box(group,0,0,d+1,w-7,h-7,2,0xdce3e8);
      for(const x of [-w/2+8,w/2-8])for(const y of [-h/2+8,h/2-8])cyl(group,x,y,d+3,2,1,0x8397a4);
      plateText(group,'RFID CONTROL',0,8,d+3,w*.7,24);for(let i=0;i<4;i++)box(group,-45+i*30,-h/2+2,d/2,18,8,12,0x455d6e);
    }else if(id==='amp'){
      box(group,0,0,d/2,w,h,d,0x414b77);for(let x=-w/2+5;x<w/2;x+=8)box(group,x,0,d+1,2,h-4,3,0x242e58);
      plateText(group,'HONGXING',0,4,d+3,w*.72,22,'#f3f1ed','#414b77');
      for(const x of [-w/2+20,w/2-20])cyl(group,x,-h/2,d/2,5,8,0x253b4c,'x');
    }else if(id==='l298'){
      pcb(group,w,h);box(group,0,3,15,w-15,h-20,28,0x344654);for(let x=-w/2+12;x<w/2-8;x+=6)box(group,x,3,35,3,h-20,30,0x3e505c);
      term(group,-w/2+12,-h/2+6,8,3,0x6a99ae);term(group,w/2-10,-h/2+6,8,2,0x6a99ae);pinrow(group,-7,h/2-4,5,6);
    }else if(id==='magdiodes'){
      for(const y of [-15,0,15]){const body=new T.Mesh(new T.CylinderGeometry(2.5,2.5,9.5,14),mat(0x283942));body.position.set(0,y,3);group.add(body);const band=new T.Mesh(new T.CylinderGeometry(2.56,2.56,1.4,14),mat(0xdeddd1));band.position.set(0,y+3,3);group.add(band);tube([[0,y-7,3],[0,y-4.75,3]],0xaebbc1,.55,group);tube([[0,y+4.75,3],[0,y+7,3]],0xaebbc1,.55,group);}
    }else if(id==='isolated5'){
      box(group,0,0,d/2,w,h,d,0xe2dfd7);box(group,0,0,d+1,w-2,h-28,1,0xf0ede5);
      for(const y of [-h/2+10,h/2-10])for(const x of [-4,4])cyl(group,x,y,d+2,2,1,0x637681);
      plateText(group,'DDR',0,10,d+3,w-2,12);plateText(group,'5V',0,-10,d+3,w-2,12);
    }else if(['power-ground','mag-power','gnd','logic-positive'].includes(id)){
      const two=false;for(let a=0;a<1;a++){const yy=0,c=['power-ground','gnd'].includes(id)?0x679bb4:0xb56d6c;box(group,0,yy,15,58.1,28.6,30,c);
        for(let i=0;i<12;i++){const x=-14+(i%6)*7,y=yy+7-Math.floor(i/6)*14;cyl(group,x,y,31,1.8,1,0x294957);box(group,x,y-4,31,2.6,2,1,0xe3ad64);}cyl(group,-23,yy,31,3,1,0x294957);
        plateText(group,{'power-ground':'P0','mag-power':'P12','gnd':'G','logic-positive':'5V'}[id],0,yy,32,17,8,'#fff',c===0x679bb4?'#679bb4':'#b56d6c');
      }
    }else if(id==='ac'){
      box(group,0,0,d/2,w,h,d,0xe7e5df);box(group,0,4,d+4,12,26,8,0x35495b);plateText(group,'AC',0,-23,d+1,25,12);
    }else if(id==='pe'){
      box(group,0,0,6,w,h,12,0x88a264);for(let i=0;i<4;i++)cyl(group,0,-h/2+10+i*20,14,3,4,0xbda865);
    }else if(id==='amp-adapter'){
      box(group,0,0,d/2,w,h,d,0x354655);plateText(group,'기존 DC 어댑터',0,0,d+1,w*.8,18);tube([[-w/2,0,8],[-w/2-8,0,8],[-w/2-8,-18,8]],0x293d4d,1.4,group);
    }else{
      pcb(group,w,h);
      if(id==='mp3'){
        box(group,0,0,6,w-8,h-8,7,metal);plateText(group,'micro SD',0,0,10,w-13,10);pinrow(group,-w/2+4,-h/2+3,3,8);
      }else if(id==='buck')box(group,0,0,5,12,12,8,0xb6a575);
    }
    group.traverse(obj=>{if(obj.isMesh){obj.userData.partId=id;picks.push(obj);}});
    const label=document.createElement('button');label.className='three-part-label';label.type='button';label.dataset.partId=id;label.setAttribute('aria-label',p.name+' 3D 부품 선택');
    label.innerHTML=`<i style="background:#${colors[p.domain].toString(16).padStart(6,'0')}"></i><span>${p.name}<small>${p.bodyW} × ${p.bodyH} × ${p.bodyD} mm${['rfidbox','amp','amp-adapter'].includes(id)?' *':''}</small></span>`;
    label.addEventListener('click',()=>select(id));host.appendChild(label);labels.push({el:label,p,anchor:partAnchors.get(id),side:p.x<210?'left':'right'});
  }
  // Full conductors remain selectable; shared duct sections are mechanically bundled.
  wireGroup.visible=true;
  const wireMeshes=[],leadMeshes=[],trunkMeshes=[],wireLabels=[];
  let highlightedRoute=null,showWireLabels=true,wireMode='bundle',showAlternatives=false;
  const rmap=new Map(data.routes.map(r=>[r.id,r]));
  const terminalHeight={smps:47,ac:65,pe:26,'amp-adapter':30,rfidbox:45,amp:35,mp3:20,relayA:24,relayB:24,l298:26,buck:20,gnd:45,'logic-positive':45,'power-ground':45,'mag-power':45,uno:23};
  function terminalZ(pt){const p=items.find(p=>{const y=p.bodyY+(p.bay==='lower'?330:0);return pt[0]>=p.bodyX-.2&&pt[0]<=p.bodyX+p.bodyW+.2&&pt[1]>=y-.2&&pt[1]<=y+p.bodyH+.2;});return p?terminalHeight[p.id]||25:20;}
  function wp(p,z=18){return [p[0]-200,445-p[1],z];}
  function visibleRoute(r){return showAlternatives||!r.alternative;}
  for(const r of data.routes){
    const m=r.labels.length;
    for(let index=0;index<m;index++){
      const lane=(r.returnWire?-2.6:r.kind==='CTL'?0:2.6)+(index-(m-1)/2)*.62;
      const pts=r.points.map((p,i)=>{const endpoint=i===0||i===r.points.length-1;const q=wp(p,endpoint?terminalZ(p):18+Math.abs(lane)*.35);if(!endpoint){const a=r.points[i-1],b=r.points[i+1],dx=b[0]-a[0],dy=b[1]-a[1],len=Math.hypot(dx,dy)||1;q[0]+=-dy/len*lane;q[1]+=-dx/len*lane;}return q;});
      const mesh=tube(pts,r.color,.65);mesh.userData.routeId=r.id;mesh.userData.label=r.labels[index];wireMeshes.push(mesh);picks.push(mesh);
    }
    if(r.mainPath.length){
      for(const [a,b]of [r.startLead,r.endLead]){
        if(a[0]===b[0]&&a[1]===b[1])continue;
        const aEnd=a===r.startLead[0],za=(a[0]===r.points[0][0]&&a[1]===r.points[0][1])?terminalZ(a):18;
        const zb=(b[0]===r.points.at(-1)[0]&&b[1]===r.points.at(-1)[1])?terminalZ(b):18;
        const mesh=tube([wp(a,za),wp(b,zb)],r.labels.length>1?0x475d6b:r.color,Math.min(1.65,.66+Math.sqrt(m)*.36));mesh.userData.routeId=r.id;leadMeshes.push(mesh);picks.push(mesh);
      }
    }
  }
  for(const trunk of data.harness.trunks){
    const count=trunk.labels.length,rad=Math.min(3.0,1.1+Math.sqrt(count)*.30);
    const mesh=tube([wp(trunk.a),wp(trunk.b)],0x435d69,rad);mesh.userData.trunkId=trunk.id;trunkMeshes.push(mesh);picks.push(mesh);
  }
  const hints=[['H1 · 접점 전력',[100,540],'H1'],['H2 · 제어 묶음',[255,657.5],'H2'],['H3 · DC 분배',[245,777.5],'H3'],['현장 센서 묶음',[390,612],'FIELD'],['MP3 · UART/전원',[390,510],'MP3']];
  for(const [name,p,zone]of hints){
    const trunk=data.harness.zones.find(t=>t.id==='ZONE-'+zone);
    if(!trunk)continue;const el=document.createElement('button');el.className='three-wire-label';el.type='button';el.dataset.trunk=trunk.id;el.style.borderLeftColor=p[1]===540?'#dc743d':'#4c8c96';el.textContent=name;el.addEventListener('click',()=>options.onTrunkSelect?.(trunk.id));host.appendChild(el);wireLabels.push({el,anchor:new T.Vector3(...wp(p,38))});
  }
  function emphasis(on){
    const picked=rmap.get(highlightedRoute),cables=new Set(picked?picked.cables:[]);
    function match(r){return !picked||r.cables.some(c=>cables.has(c));}
    for(const mesh of wireMeshes){const r=rmap.get(mesh.userData.routeId);mesh.visible=visibleRoute(r)&&(wireMode==='cores'||!r.mainPath.length||!!picked||on);mesh.material.transparent=true;mesh.material.opacity=match(r)&&(!on||r.returnWire)?1:.055;mesh.material.depthTest=!(picked||on);mesh.material.depthWrite=false;mesh.renderOrder=picked||on?20:0;}
    for(const mesh of leadMeshes){const r=rmap.get(mesh.userData.routeId);mesh.visible=visibleRoute(r)&&wireMode==='bundle'&&!picked&&!on;mesh.material.transparent=true;mesh.material.opacity=r.conditional?.75:1;}
    for(const mesh of trunkMeshes){const t=data.harness.trunks.find(t=>t.id===mesh.userData.trunkId);mesh.visible=wireMode==='bundle'&&t.routeIds.some(id=>visibleRoute(rmap.get(id)));mesh.material.transparent=true;mesh.material.opacity=picked||on?.13:1;}
    host.dataset.wireMode=wireMode;host.dataset.alternatives=String(showAlternatives);dirty=true;
  }
  function highlightRoute(id){highlightedRoute=id;host.dataset.route=id||'';emphasis(document.getElementById('power-layer').classList.contains('active'));}
  function setWireMode(mode){wireMode=mode;host.querySelector('[data-3d="bundle"]').setAttribute('aria-pressed',String(mode==='bundle'));host.querySelector('[data-3d="cores"]').setAttribute('aria-pressed',String(mode==='cores'));emphasis(document.getElementById('power-layer').classList.contains('active'));}
  function wireLabelLayout(){const W=host.clientWidth,H=host.clientHeight;let placed=[];
    for(const l of wireLabels){const q=l.anchor.clone().project(camera),x=(q.x+1)*W/2,y=(1-q.y)*H/2;l.el.hidden=!showWireLabels||y<35||y>H-65||q.z>1;if(l.el.hidden)continue;let yy=y;for(const p of placed)if(Math.abs(p.x-x)<170&&Math.abs(p.y-yy)<25)yy=p.y+27;placed.push({x,y:yy});l.el.style.left=Math.max(190,Math.min(W-320,x+12))+'px';l.el.style.top=Math.min(H-95,yy)+'px';}
  }
  host.querySelector('[data-3d="wirelabels"]').addEventListener('click',e=>{showWireLabels=!showWireLabels;e.currentTarget.setAttribute('aria-pressed',String(showWireLabels));dirty=true;});
  host.querySelector('[data-3d="bundle"]').addEventListener('click',()=>setWireMode('bundle'));
  host.querySelector('[data-3d="cores"]').addEventListener('click',()=>setWireMode('cores'));
  host.querySelector('[data-3d="alternatives"]').addEventListener('click',e=>{showAlternatives=!showAlternatives;e.currentTarget.setAttribute('aria-pressed',String(showAlternatives));emphasis(document.getElementById('power-layer').classList.contains('active'));});
  const door=new T.Group();door.position.set(220,-165,128);door.rotation.y=1.75;door.visible=false;cabinet.add(door);
  box(door,-200,0,0,400,560,4,paint);const panel=new T.Group();panel.position.set(-400+model.doorPanel.x+model.doorPanel.width/2,280-model.doorPanel.y-model.doorPanel.height/2,6);door.add(panel);box(panel,0,0,0,180,75,4,0x4e6576);
  const ledMeshes=[];for(let i=0;i<6;i++){const x=-65+Math.floor(i/3)*65,y=22-(i%3)*22;const lm=mat(0x42675e);lm.emissive=new T.Color(0x19ad79);lm.emissiveIntensity=0;ledMeshes.push(cyl(panel,x,y,4,3.5,3,lm));plateText(panel,['액자','조명','열쇠','RFID','책','완료'][i],x+21,y,4,29,12,'#eef5f8','#4e6576');}
  cyl(panel,65,0,7,9,10,0x318a8f);plateText(panel,'2초 진행',62,-24,4,45,11,'#eef5f8','#4e6576');
  const selection=new T.BoxHelper(new T.Object3D(),0xd6a23e);selection.visible=false;scene.add(selection);
  const hud=host.querySelector('.three-selection');let selectedId=null,showLabels=true,lastWidth=0,lastHeight=0;
  function select(id){const p=items.find(x=>x.id===id);if(!p)return;selectedId=id;host.dataset.selected=id;dirty=true;selection.setFromObject(partGroups.get(id));selection.visible=true;labels.forEach(l=>l.el.classList.toggle('selected',l.p.id===id));
    hud.innerHTML=`<strong>${p.name}</strong><span>${p.domain} · ${p.bay==='upper'?'상부':'하부'} (${p.x}, ${p.y}) mm</span><small>${p.basis}</small>`;hud.hidden=false;options.onSelect?.(id);}
  function resize(){const w=host.clientWidth,h=host.clientHeight;if(w===lastWidth&&h===lastHeight)return;lastWidth=w;lastHeight=h;renderer.setSize(w,h,false);const span=1040;camera.left=-span*w/h/2;camera.right=span*w/h/2;camera.top=span/2;camera.bottom=-span/2;camera.updateProjectionMatrix();}
  function fit(which='all',angle='front'){
    const yy=which==='upper'?315:which==='lower'?-165:-5,span=which==='upper'?385:which==='lower'?680:1040;
    controls.target.set(0,yy,35);camera.position.set(angle==='iso'?650:0,yy+(angle==='iso'?200:0),2200);camera.zoom=1040/span;camera.updateProjectionMatrix();controls.update();host.dataset.focus=which;host.dataset.angle=angle;dirty=true;}
  function zoom(factor){camera.zoom=T.MathUtils.clamp(camera.zoom*factor,.25,15);camera.updateProjectionMatrix();dirty=true;}
  function labelLayout(){
    const W=host.clientWidth,H=host.clientHeight;if(!showLabels||W<720){labels.forEach(l=>l.el.hidden=true);leader.style.display='none';return;}
    const focus=host.dataset.focus||'all';labels.forEach(l=>{l.el.hidden=focus!=='all'&&l.p.bay!==focus;});
    for(const side of ['left','right']){const group=labels.filter(x=>x.side===side&&!x.el.hidden).map(l=>{const v=l.anchor.clone().project(camera);return {...l,sy:(1-v.y)*H/2};}).sort((a,b)=>a.sy-b.sy);let pos=62;
      const gap=Math.min(44,(H-130)/Math.max(1,group.length));
      for(let i=0;i<group.length;i++){const l=group[i],y=Math.max(pos,Math.min(H-70-(group.length-1-i)*gap,l.sy));pos=y+gap;l.el.hidden=false;l.el.style.top=y+'px';l.el.style.left=side==='left'?'14px':'auto';l.el.style.right=side==='right'?'14px':'auto';}
    }
    const l=labels.find(a=>a.p.id===selectedId&&!a.el.hidden);leader.style.display=l?'block':'none';if(l){const v=l.anchor.clone().project(camera),x=(v.x+1)*W/2,y=(1-v.y)*H/2,sx=l.side==='left'?l.el.offsetLeft+l.el.offsetWidth:l.el.offsetLeft,sy=l.el.offsetTop+l.el.offsetHeight/2;leader.setAttribute('viewBox',`0 0 ${W} ${H}`);leader.querySelector('path').setAttribute('d',`M${sx},${sy} L${sx+(l.side==='left'?18:-18)},${sy} L${x},${y}`);leader.querySelector('circle').setAttribute('cx',x);leader.querySelector('circle').setAttribute('cy',y);}
  }
  const pointer=new T.Vector2(),ray=new T.Raycaster();let down=null;
  renderer.domElement.addEventListener('pointerdown',e=>{down=[e.clientX,e.clientY];});renderer.domElement.addEventListener('pointerup',e=>{if(!down||Math.hypot(e.clientX-down[0],e.clientY-down[1])>5)return;const r=renderer.domElement.getBoundingClientRect();pointer.set((e.clientX-r.left)/r.width*2-1,-(e.clientY-r.top)/r.height*2+1);ray.setFromCamera(pointer,camera);const hit=ray.intersectObjects(picks,false)[0];if(hit){if(hit.object.userData.trunkId)options.onTrunkSelect?.(hit.object.userData.trunkId);else if(hit.object.userData.routeId)options.onRouteSelect?.(hit.object.userData.routeId);else select(hit.object.userData.partId);}});
  host.querySelector('[data-3d="front"]').addEventListener('click',()=>fit('all','front'));host.querySelector('[data-3d="iso"]').addEventListener('click',()=>fit('all','iso'));host.querySelector('[data-3d="fit"]').addEventListener('click',()=>fit());
  host.querySelector('[data-3d="zoomin"]').addEventListener('click',()=>zoom(1.3));host.querySelector('[data-3d="zoomout"]').addEventListener('click',()=>zoom(1/1.3));
  host.querySelector('[data-3d="wires"]').addEventListener('click',()=>document.getElementById('power-layer').click());
  host.querySelector('[data-3d="labels"]').addEventListener('click',e=>{showLabels=!showLabels;dirty=true;e.currentTarget.setAttribute('aria-pressed',String(showLabels));});
  host.querySelector('[data-3d="door"]').addEventListener('click',e=>{door.visible=!door.visible;dirty=true;e.currentTarget.setAttribute('aria-pressed',String(door.visible));});
  function expand(){const on=host.classList.toggle('expanded');document.body.classList.toggle('three-expanded',on);host.querySelector('[data-3d="expand"]').textContent=on?'설계 탭으로 복귀':'화면 채우기';resize();dirty=true;}
  host.querySelector('[data-3d="expand"]').addEventListener('click',expand);document.addEventListener('keydown',e=>{if(e.key==='Escape'&&host.classList.contains('expanded'))expand();});
  for(const el of document.querySelectorAll('[data-bay]'))el.addEventListener('click',()=>fit(el.dataset.bay));
  document.getElementById('zoom-in').addEventListener('click',()=>zoom(1.3));document.getElementById('zoom-out').addEventListener('click',()=>zoom(1/1.3));document.getElementById('zoom-fit').addEventListener('click',()=>fit());
  document.getElementById('power-layer').addEventListener('click',e=>{emphasis(e.currentTarget.classList.contains('active'));host.dataset.wires=String(e.currentTarget.classList.contains('active'));dirty=true;});
  let dirty=true;controls.addEventListener('change',()=>{dirty=true;});new ResizeObserver(()=>{resize();dirty=true;}).observe(host);
  let lastLED=-1,lastFrame=0;
  function animate(now=0){requestAnimationFrame(animate);if(host.getClientRects().length===0||now-lastFrame<30)return;lastFrame=now;resize();controls.update();const shown=document.getElementById('power-layer').classList.contains('active');if(host.dataset.wires!==String(shown))emphasis(shown);wireGroup.visible=true;host.dataset.wires=String(shown);host.querySelector('[data-3d="wires"]').setAttribute('aria-pressed',String(shown));const mask=options.ledMask?.()||0;if(mask!==lastLED){lastLED=mask;dirty=true;ledMeshes.forEach((led,i)=>{led.material.emissiveIntensity=(mask&(1<<i))?2:0;});}if(dirty){labelLayout();wireLabelLayout();if(selection.visible)selection.update();host.dataset.zoom=camera.zoom.toFixed(3);host.querySelector('.three-badge').textContent='Three.js r'+T.REVISION+' · '+Math.round(camera.zoom*100)+'%';dirty=false;}renderer.render(scene,camera);}
  resize();fit('all','iso');animate();host.dataset.ready='true';
  return {fit,zoom,select,highlightRoute,setWireMode,renderer,controls,camera,scene,get selected(){return selectedId;},get wireVisible(){return wireGroup.visible;}};
}
