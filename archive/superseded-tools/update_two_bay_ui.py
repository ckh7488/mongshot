"""One-time source migration; subsequent builds use the edited source files."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'simulation/source/page.html'
s=p.read_text(encoding='utf-8')
s=s.replace('<button type="button" data-view="cabinet">','<button type="button" data-view="fit">실장·치수</button><button type="button" data-view="panel">LED·버튼 회로</button><button type="button" data-view="cabinet">',1)
s=s.replace('확정 HW 반영 · 2026.11.03','상하 함체 실장안 · 2026.11.03')
s=s.replace('이 화면의 배치·배선 길이는 축척 도면이 아닙니다.','최신 배치의 점선 영역·좌표는 mm 기준 계획값입니다. 몸체 그림과 배선 경로는 설명용이며, 사진 추정치를 실제 실측치로 간주하지 않습니다.')
intro='''<article class="design-card"><h3>상하 공간을 함께 쓰는 실제 배치</h3><p><strong>상부:</strong> 차단기·12V SMPS·PE 바·0V-PWR·부하별 퓨즈. <strong>하부:</strong> 큰 RFID 회색함, 릴레이 A/B, Arduino, L298N, DC-DC, 0V-L, 앰프/MP3.</p><p>검토 유효 공간은 <strong>폭 400 / 상부 260 / 하부 650 / 깊이 120mm</strong>. 사진의 확정 치수가 아닙니다. <strong>실장·치수</strong> 보기에서 실측값과 RFID 크기를 넣으면 확보 영역 조건을 비교합니다.</p><p>상하 기존 관통구에는 DC 12선 + RFID 조건부 2선을 분리 묶음으로 통과시킵니다. AC는 상부에서 끝내며, 모서리 부싱과 양쪽 고정 클립을 적용합니다.</p></article>'''
s=s.replace('<section class="design-doc active" id="design-doc"><div class="design-grid">','<section class="design-doc active" id="design-doc"><div class="design-grid">'+intro)
p.write_text(s,encoding='utf-8')
p=ROOT/'simulation/source/app.js';s=p.read_text(encoding='utf-8')
s=s.replace("const views={new:['새 배전함 · SMPS와 외부 조작부','12V 메인 + 5V DC-DC · RFID 회색함·릴레이 2장 · LED 6개·진행 버튼'],", "const views={new:['사진 기준 상하 배전함 · 실장 계획','상부 전원 / 하부 RFID·제어 · mm 좌표·확보 영역·기존 관통구'],fit:['실장·치수 · 부품이 들어가는 조건','유효 폭·상하 높이·깊이·RFID 외곽을 입력해 계획 영역과 비교'],panel:['외부 LED·진행 버튼 · 실제 핀 회로','SN74HC595N / 1kΩ ×6 / A3 버튼 · 기존 Gun/Hint 선 제거 후 재사용'],")
start=s.index('function setView(v)');end=s.index("\nall('[data-view]').forEach",start)+1
s=s[:start]+'''function setView(v){
 currentView=v;all('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===v));
 $('view-title').textContent=views[v][0];$('view-subtitle').textContent=views[v][1];
 $('drawing-stage').classList.toggle('photo',v==='photo');
 for(const [id,view] of [['design-drawing','new'],['ground-drawing','gnd'],['panel-drawing','panel'],['fit-drawing','fit'],['functional-drawing','cabinet'],['labels-drawing','labels']])$(id).hidden=v!==view;
 $('bay-controls').hidden=v!=='new';$('domain-notice').hidden=!['new','gnd'].includes(v);
 $('design-doc').classList.toggle('active',['new','gnd','labels','panel','fit'].includes(v));
 if(v==='gnd'){hasPower=true;all('svg').forEach(s=>s.classList.add('show-power'));select('gnd');}
 else if(v==='new')select('smps');else if(v==='cabinet')select('uno');else if(v==='panel')select('frontpanel');
 updatePowerButton();applyZoom();
}
let bayFocus='all';
all('[data-bay]').forEach(b=>b.addEventListener('click',()=>{bayFocus=b.dataset.bay;all('[data-bay]').forEach(x=>x.classList.toggle('active',x===b));$('redesign-svg').setAttribute('viewBox',({all:'0 0 1420 2200',upper:'40 100 1370 700',lower:'45 730 970 1440'})[bayFocus]);zoom=100;applyZoom();}));
$('wide-drawing').addEventListener('click',()=>{const on=document.body.classList.toggle('wide-drawing');$('wide-drawing').setAttribute('aria-pressed',String(on));$('wide-drawing').textContent=on?'입력창 표시':'도면 크게';applyZoom();});
''' +s[end:]
s=s.replace("#design-drawing>svg,#ground-drawing>svg,#functional-drawing>svg","#design-drawing>svg,#ground-drawing>svg,#panel-drawing>svg,#functional-drawing>svg")
s=s.replace("'기존 12V 전자석입니다. 새 배선에서는 전용 전원·0V-MAG와 릴레이 접점으로 제어부에서 분리합니다.'", "'기존 12V 전자석입니다. 상부 개별 퓨즈에서 내려온 양극을 하부 릴레이 접점으로 스위칭하며, 음극은 상부 0V-PWR로 직접 귀환합니다.'")
s=s.replace("'창문 부하 자체 전원':'0V-MAG'", "'창문 부하 자체 전원':'상부 0V-PWR 개별 포트'")
s=s.replace("x.replace('接点','접점')", "x.replace('接点','접점').replace('0V-MAG BUS','상부 0V-PWR')")
s=s.replace("['기구 크기','실물 치수로 외함 선정']", "['기구 공간','하부 (40,10) / 280×220 확보']")
s=s.replace("details.power=details.smps;", """details.power=details.smps;
details.pe={title:'PE 보호접지 바',desc:'상부 금속 외함과 문 등 접지 대상의 보호접지용입니다. 센서 신호 귀환을 이 바나 외함으로 대신하지 않습니다.',rows:[['장소','상부 (325,15)'],['연결','인입 PE / SMPS PE / 외함'],['DC 0V','임의 결합 금지']],note:'기존 접지 경로와 제조사 요구를 확인해 적용합니다. DC 음극-PE의 의도적 결합 여부는 전원/시스템 사양에 따라 별도 기록합니다.',nets:[]};
details.ac={title:'상부 AC 전용 구역',desc:'기존 인입 회로를 추적한 뒤 차단기·SMPS AC·PE를 상부 안에 고정합니다. 아래 제어함으로 AC를 통과시키지 않는 배치입니다.',rows:[['장소','상부 (10,10)'],['상하 관통구','DC 전원선만'],['보호','단자 커버 / 고정 배선']],note:'이 사진에 보이는 기존 두 SMPS가 모두 이 장치용이라고 단정하지 않습니다. 다른 장치의 회로는 철거 전에 구별합니다.',nets:[]};
details.motor={...details.motor,rows:[['드라이버','L298N E6'],['방향','D4 / D5'],['ENABLE','A2(16) HIGH'],['귀환','L298N 전력 0V → 상부 0V-PWR']]};""")
p.write_text(s,encoding='utf-8')
print('Two-bay source UI installed')
