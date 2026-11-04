/* v5 design data + unchanged tested AVR workbench behavior. */
(()=>{'use strict';
const $=id=>document.getElementById(id),all=(s,r=document)=>[...r.querySelectorAll(s)];
const details={"ac": {"title": "기존 차단기", "desc": "기존 회로 보존; 정격/실물 대조", "rows": [["영역", "PE"], ["좌표", "upper (10,10) mm"], ["확보", "45×110 mm"], ["몸체 검토", "36×80×70 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["PE"]}, "smps": {"title": "12V 메인 SMPS", "desc": "LRS-200-12 후보; 17A 필요 확정 아님. 부하/가는 선에 맞춰 용량 재선정", "rows": [["영역", "P0"], ["좌표", "upper (70,10) mm"], ["확보", "240×145 mm"], ["몸체 검토", "215×115×30 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["P0"]}, "pe": {"title": "기존 PE 접지부", "desc": "금속 함체/도어/SMPS FG; DC 귀환에 사용하지 않음", "rows": [["영역", "PE"], ["좌표", "upper (325,15) mm"], ["확보", "55×100 mm"], ["몸체 검토", "30×80×35 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["PE"]}, "power-ground": {"title": "부하 12V − (P0)", "desc": "SMPS V− 1가닥을 여러 부하 귀환으로 분배. 내부13접속점 공통. 변환/절연 기능 없음", "rows": [["영역", "P0"], ["좌표", "upper (15,175) mm"], ["확보", "75×65 mm"], ["몸체 검토", "58.1×28.6×32.4 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["P0"]}, "mag-power": {"title": "부하 12V + (P12)", "desc": "SMPS V+를 여러 회로로 분기. 전압변환기가 아닌 수동 분배블록", "rows": [["영역", "P0"], ["좌표", "upper (105,175) mm"], ["확보", "75×65 mm"], ["몸체 검토", "58.1×28.6×32.4 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["P0"]}, "amp-adapter": {"title": "홍싱 기존 어댑터", "desc": "기존 DC 어댑터 재사용; 90×45×35는 배치 가정", "rows": [["영역", "G0"], ["좌표", "upper (200,175) mm"], ["확보", "110×65 mm"], ["몸체 검토", "90×45×35 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["G0"]}, "rfidbox": {"title": "RFID 제어함", "desc": "기존 제어함을 보존하되 160×100×65mm 가정으로 줄였습니다. 정격12V일 때 전원은 P0. 무전압 접점은G0 입력으로,12V 비절연 스위칭 출력만 옵토로 전달합니다. 실제 출력형식 대조.", "rows": [["영역", "P0"], ["좌표", "lower (25,10) mm"], ["확보", "170×130 mm"], ["몸체 검토", "160×100×65 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["P0"]}, "amp": {"title": "HONGXING", "desc": "몸체140×90×45 배치가정. MP3를 바로 아래로 이동. 기존 라인출력/GND 직결", "rows": [["영역", "G0"], ["좌표", "lower (215,10) mm"], ["확보", "170×110 mm"], ["몸체 검토", "140×90×45 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["G0"]}, "mp3": {"title": "KT403A MP3", "desc": "홍싱 바로 아래. UART/라인 출력은G0, SPK±는 앰프 입력으로 쓰지 않음", "rows": [["영역", "G0"], ["좌표", "lower (235,125) mm"], ["확보", "70×40 mm"], ["몸체 검토", "45×30×20 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["G0"]}, "relayA": {"title": "4CH 릴레이 A", "desc": "기존 보드; 3자석+창문을 조건부 재배치", "rows": [["영역", "P0"], ["좌표", "lower (25,200) mm"], ["확보", "90×75 mm"], ["몸체 검토", "80×60×30 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["P0"]}, "relayB": {"title": "4CH 릴레이 B", "desc": "8채널 추적 전 철거/예비 단정 금지", "rows": [["영역", "P0"], ["좌표", "lower (125,200) mm"], ["확보", "90×75 mm"], ["몸체 검토", "80×60×30 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["P0"]}, "magdiodes": {"title": "자석 다이오드 ×3 · 릴레이 옆", "desc": "별도 PCB 없음. 3개와 절연 리드 고정공간6×50mm는 배치값. 자석선 +/−에 병렬, 접점 COM/NO 사이 아님", "rows": [["영역", "P0"], ["좌표", "lower (115,200) mm"], ["확보", "10×65 mm"], ["몸체 검토", "6×50×6 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["P0"]}, "l298": {"title": "L298N E6", "desc": "D4/D5/A2를 기존처럼 직결합니다. G0.4에서 L298 GND로 기준선을 연결하므로 P0/G0는 공통입니다. 모터 전력 귀환은 별도 P0-MOTOR로 유지합니다.", "rows": [["영역", "P0"], ["좌표", "lower (25,315) mm"], ["확보", "90×75 mm"], ["몸체 검토", "60×60×55 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["P0"]}, "buck": {"title": "부하측 5V 변환기 (5D)", "desc": "P12/P0에서5D/P0를 만듦. 릴레이 코일/L298 제어전원용. 12V→5V 강압, 입력/출력−는 P0 공통. 실물 기판25.4×25.4mm", "rows": [["영역", "P0"], ["좌표", "lower (25,430) mm"], ["확보", "60×65 mm"], ["몸체 검토", "25.4×25.4×9.5 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["P0"]}, "isolated5": {"title": "로직용 5V 변환기 · 현재 GND 공통", "desc": "DDR-15G-5 전원분기 후보 유지. G0↔P0가 공통이므로 전체 시스템 절연용으로 보지 않음. 몸체 위40/아래20/좌우5mm 이상 비움. 낮은 입력전압에서는2.7A 제한", "rows": [["영역", "BOUNDARY"], ["좌표", "lower (100,405) mm"], ["확보", "45×150 mm"], ["몸체 검토", "17.5×90×54.5 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["BOUNDARY"]}, "gnd": {"title": "로직 5V − (G0)", "desc": "G0는 전압변환기가 아니라 DDR의 출력−를 나누는 분배블록입니다. 짝은5L(+5V)입니다. P0와 제품/크기가 같고 제어 기준선으로 공통입니다. 귀환 분기이며 절연이 아닙니다.", "rows": [["영역", "G0"], ["좌표", "lower (160,430) mm"], ["확보", "75×40 mm"], ["몸체 검토", "58.1×28.6×32.4 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["G0"]}, "logic-positive": {"title": "로직 5V + (5L)", "desc": "DDR의 출력+를 나누는 로직5V 분배블록입니다. G0와 한 쌍입니다. 부하측5V인5D와 연결하지 않습니다.", "rows": [["영역", "G0"], ["좌표", "lower (160,480) mm"], ["확보", "75×40 mm"], ["몸체 검토", "58.1×28.6×32.4 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["G0"]}, "uno": {"title": "Arduino Uno", "desc": "USB/핀 삽입 여유 포함; 로직 G0", "rows": [["영역", "G0"], ["좌표", "lower (265,430) mm"], ["확보", "95×80 mm"], ["몸체 검토", "68.6×53.4×25 mm"]], "note": "실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.", "nets": ["G0"]}, "frontpanel": {"title": "외부 진행 LED·버튼", "desc": "6개 LED + 2초 진행 버튼. 기존 AVR 동작과 595 래치를 유지합니다.", "rows": [["DATA / CLK / LATCH", "D11 / D13 / D7"], ["진행 버튼", "A3 / J7.6"], ["귀환", "G0 / J7.2"]], "note": "Gun/Hint 배선을 제거한 뒤 재사용. 실물 하드웨어 업로드 전 MP3 라이브러리 호환 문제 해결.", "nets": ["G0"]}};
const mode=$('firmware-mode');let runner,playing=false,lastWall=0,simDebt=0,currentView='new',selection='gnd',zoom=100,demoStart=null,demoEvents=[],prevStage=-1,hasPower=false,pendingManualReleaseAt=null;
const outputs=[[12,'몰딩 / D12'],[10,'슬라이드 / D10'],[9,'책 / D9'],[18,'창문 / A4'],[4,'모터 방향 / D4'],[5,'모터 방향 / D5'],[16,'ENABLE / A2']];
$('outputs').innerHTML=outputs.map(([p,name])=>`<div class="output-row"><span><i id="dot-${p}"></i>${name}</span><span class="level" id="out-${p}">Hi-Z</span></div>`).join('');
const row=(k,v)=>`<div class="info-row"><span>${k}</span><span class="v">${v}</span></div>`;
function select(id){
 selection=id;
 const idFallback=id.startsWith('out')?({out12:'mold',out10:'slide',out9:'bookload',out18:'window'})[id]:id.startsWith('motor')?'l298':id.startsWith('uart')?'mp3':id.startsWith('load')?({load12:'mold',load10:'slide',load9:'bookload',load18:'window'})[id]:id==='actuator'?'motor':id.startsWith('gnd-')?'gnd':id;
 const d=details[id]||details[idFallback]||details.gnd;
 $('detail-title').textContent=d.title;$('detail-desc').textContent=d.desc;$('detail-rows').innerHTML=d.rows.map(([k,v])=>row(k,v)).join('')+`<div class="inspector-note">${d.note}</div>`;
 const targets=d.nets||[id];
 all('.net').forEach(el=>{const yes=targets.includes(el.dataset.net);el.classList.toggle('selected-net',yes);el.classList.toggle('dim-net',targets.length>0&&!yes);});
 all('.device').forEach(el=>el.classList.toggle('selected-device',el.dataset.part===id||el.dataset.part===idFallback));
 all('[data-select-net]').forEach(el=>el.classList.toggle('selected-label',el.dataset.selectNet===id));
}
all('.device').forEach(el=>{const handler=()=>select(el.dataset.part);el.addEventListener('click',handler);el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();handler();}});});
all('.net-hit').forEach(el=>el.addEventListener('click',()=>select(el.dataset.net)));
all('[data-select-net]').forEach(el=>{const handler=()=>select(el.dataset.selectNet);el.addEventListener('click',handler);el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();handler();}});});
function clearHighlight(){all('.net').forEach(el=>el.classList.remove('selected-net','dim-net'));all('.device').forEach(el=>el.classList.remove('selected-device'));}
function reset(){runner=new MongshotAVR.Runner(MONGSHOT_FIRMWARE[mode.value]);playing=false;demoStart=null;demoEvents=[];pendingManualReleaseAt=null;lastWall=0;simDebt=0;prevStage=-1;update();$('run').textContent='▶ 실행';$('toast').classList.remove('visible');}
function requestManual(){if(!runner.firmware.frontpanel||runner.inputs.manual||runner.word('phase')===9)return;demoStart=null;demoEvents=[];if(runner.ms<1100)runner.runMs(1100-runner.ms);runner.setInputs({manual:true});pendingManualReleaseAt=runner.ms+2100;playing=true;lastWall=performance.now();$('run').textContent='Ⅱ 일시정지';$('toast').textContent='부팅을 마친 뒤 진행 버튼 입력 2초를 시뮬레이션합니다. 입력 단계는 1회 완료하고, 프로그램 대기 중 입력은 다음 단계로 예약하지 않습니다.';$('toast').classList.add('visible');select('frontpanel');}
$('manual-next').addEventListener('click',requestManual);
all('[data-action="manual-next"]').forEach(el=>el.addEventListener('click',e=>{e.stopPropagation();requestManual();}));
function setInput(values){runner.setInputs(values);update();}
for(const key of ['frame','book'])$('input-'+key).addEventListener('click',()=>setInput({[key]:!runner.inputs[key]}));
for(const key of ['light','key','rfid'])$('input-'+key).addEventListener('input',e=>setInput({[key]:Number(e.target.value)}));
$('pulse-light').addEventListener('click',()=>setInput({light:runner.inputs.light<500?900:100}));
for(const key of ['key','rfid'])$('toggle-'+key).addEventListener('click',()=>setInput({[key]:runner.inputs[key]<400?900:0}));
$('run').addEventListener('click',()=>{playing=!playing;lastWall=performance.now();$('run').textContent=playing?'Ⅱ 일시정지':'▶ 실행';update();});
$('reset').addEventListener('click',reset);mode.addEventListener('change',reset);
$('demo').addEventListener('click',()=>{
 reset();demoStart=0;demoEvents=[
 [1200,{frame:true}],[1500,{light:100}],[1750,{light:900}],[2000,{light:100}],[2250,{light:900}],[2500,{light:100}],
 [22900,{key:0}],[23400,{rfid:0}],[24800,{book:true}]
 ];playing=true;lastWall=performance.now();$('run').textContent='Ⅱ 일시정지';$('toast').textContent='자동 시연: 센서 입력만 순서대로 주입합니다. 코드의 20초·1초·10초 지연은 그대로 실행됩니다.';$('toast').classList.add('visible');
});
const views={"new": ["v5.3 · 기존 제어선 직결", "400mm 폭 / 상부260 / 하부560 · 부품을 누르면 좌표·영역 표시"], "gnd": ["P0/G0 · 공통 기준과 별도 전력 귀환", "공통 기준선 G0.4→L298 GND · 자석−도 공통 · PE는 별도 보호접지"], "interfaces": ["직결·다이오드 · 실제 핀 회로", "L2983신호 / 릴레이4입력 / 기존 센서 / 자석 양단 다이오드"], "cable": ["가는 이더넷 심선 · 전원 검토", "실제 길이·전류·단심저항 입력 · 전압강하와 페어 병렬 비교"], "bom": ["제품 BOM · 제거/추가/제작 구분", "일반 큰 단자열을 제거하고 필요한 접속부만 남긴 품번·수량"], "fit": ["실장·치수 · 작은 확보 영역 대조", "사진 기반 계획과 실물 치수를 비교 · 자동 설치승인 아님"], "panel": ["외부 LED·버튼 · 기존 회로 유지", "LED1.5kΩ×6 / 버튼4.7kΩ풀업 / A3 2초 진행"], "labels": ["핀·라벨 · 실제 선 구간", "가상의 T1/T2 단자열 없이 PCB 접속부와 모듈 핀에 직접 종단"], "photo": ["기존 현장", "철거 전 기록과 실제 배선 추적 기준"], "cabinet": ["과거 기능 참고", "v5 설치 결선도로 사용하지 않음"], "review": ["왜 이 구성이 필요한가", "분배블록/전원변환/MP3 위치/조건부 센서절연을 구별해 설명"]};
function setView(v){
 currentView=v;all('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===v));
 $('view-title').textContent=views[v][0];$('view-subtitle').textContent=views[v][1];
 $('drawing-stage').classList.toggle('photo',v==='photo');
 for(const [id,view] of [['design-drawing','new'],['ground-drawing','gnd'],['panel-drawing','panel'],['fit-drawing','fit'],['bom-drawing','bom'],['functional-drawing','cabinet'],['labels-drawing','labels'],['interfaces-drawing','interfaces'],['cable-drawing','cable'],['review-drawing','review']])$(id).hidden=v!==view;
 $('bay-controls').hidden=v!=='new';$('domain-notice').hidden=!['new','gnd'].includes(v);
 $('design-doc').classList.toggle('active',['new','gnd','labels','panel','fit','bom','interfaces','cable'].includes(v));
 if(v==='gnd'){hasPower=true;all('svg').forEach(s=>s.classList.add('show-power'));select('gnd');}
 else if(v==='new')select('smps');else if(v==='cabinet')select('uno');else if(v==='panel')select('frontpanel');
 updatePowerButton();applyZoom();
}
let bayFocus='all';
all('[data-bay]').forEach(b=>b.addEventListener('click',()=>{bayFocus=b.dataset.bay;all('[data-bay]').forEach(x=>x.classList.toggle('active',x===b));$('redesign-svg').setAttribute('viewBox',({all:'0 0 1320 2020',upper:'45 95 1250 680',lower:'45 750 900 1200'})[bayFocus]);zoom=100;applyZoom();}));
$('wide-drawing').addEventListener('click',()=>{const on=document.body.classList.toggle('wide-drawing');$('wide-drawing').setAttribute('aria-pressed',String(on));$('wide-drawing').textContent=on?'입력창 표시':'도면 크게';applyZoom();});
all('[data-view]').forEach(b=>b.addEventListener('click',()=>setView(b.dataset.view)));
function updatePowerButton(){$('power-layer').classList.toggle('active',hasPower);$('power-layer').textContent=hasPower?'전원선 켜짐':'전원선';}
$('power-layer').addEventListener('click',()=>{hasPower=!hasPower;all('svg').forEach(s=>s.classList.toggle('show-power',hasPower));updatePowerButton();});
function applyZoom(){const host=$('drawing-stage'),mobile=window.innerWidth<=760;all('#design-drawing>svg,#ground-drawing>svg,#panel-drawing>svg,#functional-drawing>svg,#interfaces-drawing>svg').forEach(s=>{const box=s.viewBox.baseVal;const base=mobile?Math.max(680,host.clientWidth):Math.min(host.clientWidth,host.clientHeight*box.width/box.height);s.style.width=base*zoom/100+'px';s.style.height='auto';s.style.maxWidth='none';});}
new ResizeObserver(()=>applyZoom()).observe($('drawing-stage'));
$('zoom-in').addEventListener('click',()=>{zoom=Math.min(200,zoom+20);applyZoom();});$('zoom-out').addEventListener('click',()=>{zoom=Math.max(60,zoom-20);applyZoom();});$('zoom-fit').addEventListener('click',()=>{zoom=100;applyZoom();clearHighlight();});
function update(){
 const s=runner.snapshot();$('sim-time').textContent=(s.ms/1000).toFixed(2)+' s';$('light-count').textContent=Math.min(3,s.lightCount)+' / 3';$('filter-info').textContent=MONGSHOT_FIRMWARE[mode.value].sampleMs+'ms × 5회';
 for(const key of ['frame','book']){const active=s.inputs[key];$('value-'+key).textContent=active?'LOW':'HIGH';$('input-'+key).textContent=active?'감지 중 · 해제하기':'자석 감지시키기';$('input-'+key).classList.toggle('on',active);$('input-'+key).setAttribute('aria-pressed',String(active));}
 for(const key of ['light','key','rfid']){$('value-'+key).textContent=s.inputs[key];$('input-'+key).value=s.inputs[key];}
 for(const [p]of outputs){const val=s.pins[p],txt=val===null?'Hi-Z':val?'HIGH':'LOW';$('out-'+p).textContent=txt;$('out-'+p).classList.toggle('high',val===1);$('dot-'+p).classList.toggle('high',val===1);all(`[id="relay-led-${p}"],[id="load-led-${p}"],[id="new-load-led-${p}"]`).forEach(el=>el.setAttribute('fill',val===1?'#4dbb88':'#899ca5'));}
 all('.step').forEach((el,i)=>{el.classList.toggle('current',i===s.stage);el.classList.toggle('done',i<s.stage);});
 const title=['액자 감지 대기','조명 3회 판정','열쇠 감지 대기','RFID 감지 대기','책 감지 대기','종료 · 리셋 대기'];let note='';
 if(s.ms<1050)note='부팅·MP3 초기화 대기';else if(s.stage===2&&s.pins[10]===0)note='슬라이드 해제 전 20초 대기';else if(s.stage===4)note='창문 출력 HIGH · 1초 지연 후 책 입력';else if(s.stage===5)note=s.pins[9]===0?'책 전자석 출력 전 200ms 대기':'책 출력 HIGH · 10초 후 종료 루프';else if(s.stage===0)note='모터 GPIO: D4 LOW / D5 HIGH / EN HIGH';else note='현재 단계의 입력만 판정합니다.';
 if(runner.firmware.frontpanel){const phases={1:'부팅 준비',2:'MP3 초기화 대기',3:'슬라이드 해제 전 20초 대기',4:'슬라이드 해제 후 10ms 대기',5:'창문 출력 후 1초 대기',6:'책 출력 전 100ms',7:'음성 후 100ms',8:'최종 10초 대기',9:'완료 · LED 유지'};note=phases[s.phase]||'현재 LED 단계의 입력 대기 · 2초 버튼으로 1회 완료';}
 for(let i=0;i<6;i++){const on=runner.firmware.frontpanel&&!!(s.ledMask&(1<<i));$('front-led-'+i).classList.toggle('on',on);all(`[id="panel-led-${i}"]`).forEach(el=>el.setAttribute('fill',on?'#4cb58c':'#8a9ca6'));}
 $('manual-next').disabled=!runner.firmware.frontpanel||s.phase===9;$('manual-state').textContent=runner.firmware.frontpanel?`수동 진행 ${s.manualCount}회 · ${s.inputs.manual?'버튼 누름 중':'2초 누름 / 유지 반복 없음'}`:'원본/최소변경안은 외부 조작부 미지원';
 $('stage-title').textContent=title[s.stage]||'실행 중';$('stage-note').textContent=note;$('stage-progress').style.width=Math.min(100,s.stage/5*100)+'%';$('serial-log').textContent=runner.serial.slice(-6).map(x=>(x.ms/1000).toFixed(2)+'  '+x.text).join('\n');
 const runStatus=playing?(demoStart!==null?'자동 시연 실행 중':'실행 중'):'일시정지';if($('run-status').textContent!==runStatus)$('run-status').textContent=runStatus;
 if(s.stage!==prevStage){prevStage=s.stage;}
}
let lastPaint=0;
function frame(now){
 if(playing){
  const dt=Math.min(80,Math.max(0,now-lastWall||0));lastWall=now;simDebt=Math.min(500,simDebt+dt*Number($('speed').value));const wallLimit=performance.now()+16;
  while(simDebt>0&&performance.now()<wallLimit){
   let chunk=Math.min(5,simDebt);
   if(demoStart!==null&&demoEvents.length&&runner.ms+chunk>=demoEvents[0][0]){chunk=Math.max(.01,demoEvents[0][0]-runner.ms);}
   runner.runMs(chunk);simDebt-=chunk;
   if(pendingManualReleaseAt!==null&&runner.ms>=pendingManualReleaseAt){runner.setInputs({manual:false});pendingManualReleaseAt=null;}
   while(demoEvents.length&&runner.ms>=demoEvents[0][0]-.05){runner.setInputs(demoEvents.shift()[1]);}
   if(demoStart!==null&&runner.ms>=35500){playing=false;$('run').textContent='▶ 실행';$('toast').textContent='자동 시연 완료: 5단계 종료. 원본 지연시간과 최종 GPIO 상태를 유지했습니다.';break;}
  }
 }
 if(now-lastPaint>80){update();lastPaint=now;}requestAnimationFrame(frame);
}
reset();setView('new');select('gnd');requestAnimationFrame(frame);
window.mongshotWorkbench={get runner(){return runner;},select,setView,reset,setInput,get playing(){return playing;},details};
})();
