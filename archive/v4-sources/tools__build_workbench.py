from pathlib import Path
import base64,re

ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'simulation/source'
page=(src/'page.html').read_text(encoding='utf-8')
page=page.replace('{{FIT_VIEW}}',(src/'fit-view.html').read_text(encoding='utf-8'))
page=page.replace('{{FRONTPANEL_SVG}}',(ROOT/'hardware/frontpanel-circuit.svg').read_text(encoding='utf-8'))
page=page.replace('{{GROUND_TABLE}}',(src/'ground-table.html').read_text(encoding='utf-8'))
page=page.replace('{{BOM_VIEW}}',(src/'bom-view.html').read_text(encoding='utf-8'))
page=page.replace('<button type="button" data-view="cabinet">기능·배선 보기</button>','<button type="button" data-view="gnd">GND 구조</button><button type="button" data-view="labels">핀·라벨</button><button type="button" data-view="cabinet">기능 배선</button>')
labels=[
('IN-D8','X1.1-S','Arduino D8','액자 리드 S','frame'),('0VL-FRAME','X1.1-0','0V-L 공통 버스','액자 리드 0V','gnd'),
('IN-A0','X1.2-S','Arduino A0','조명 출력 S','light'),('0VL-LIGHT','X1.2-0','0V-L 공통 버스','조명 0V','gnd'),
('IN-A1','X1.3-S','Arduino A1','열쇠 출력 S','key'),('0VL-KEY','X1.3-0','0V-L 공통 버스','열쇠 0V','gnd'),
('IN-A5','X1.4-S','Arduino A5','RFID 출력 S','rfid'),('0VL-RFID','X1.4-0','0V-L 공통 버스','RFID 0V','gnd'),
('IN-D6','X1.5-S','Arduino D6 / 100Ω','책 리드 S','book'),('0VL-BOOK','X1.5-0','0V-L 공통 버스','책 리드 0V','gnd'),
('OUT-D12','X2.1','Arduino D12','RY-A IN1 / 몰딩','out12'),('OUT-D10','X2.2','Arduino D10','RY-A IN2 / 슬라이드','out10'),('OUT-D9','X2.3','Arduino D9','RY-A IN3 / 책','out9'),('OUT-A4','X2.4','Arduino A4(18)','RY-A IN4 / 창문','out18'),
('MOT-D4','X4.1','Arduino D4','L298N IN1','motor4'),('MOT-D5','X4.2','Arduino D5','L298N IN2','motor5'),('MOT-A2','X4.3','Arduino A2(16)','L298N ENA','motor16'),('MP3-RX','X5.1','Arduino D2 RX','KT403A TX','uart2'),('MP3-TX','X5.2','Arduino D3 TX','KT403A RX','uart3'),
('MAG1+','X3-M1+','RY-A CH1 접점','몰딩 전자석 +','load12'),('MAG1-','X3-M1-','0V-MAG 버스','몰딩 전자석 −','mag-ground'),('MAG2+','X3-M2+','RY-A CH2 접점','슬라이드 전자석 +','load10'),('MAG2-','X3-M2-','0V-MAG 버스','슬라이드 전자석 −','mag-ground'),('MAG3+','X3-M3+','RY-A CH3 접점','책 전자석 +','load9'),('MAG3-','X3-M3-','0V-MAG 버스','책 전자석 −','mag-ground'),('WIN-C','X3-WIN.C','RY-A CH4 COM','창문 회로 자체 전원','window'),('WIN-SW','X3-WIN.SW','RY-A CH4 선택 접점','창문 부하','window')]

labels.extend([
('PANEL-5V','J7.1','5V 로직 분기','외부 LED 보드 VCC','panel'),
('PANEL-0V','J7.2','0V-L 분배블록','외부 LED/버튼 GND','gnd'),
('PANEL-DATA','J7.3','Arduino D11','74HC595 SER / pin14','panel'),
('PANEL-CLK','J7.4','Arduino D13','74HC595 SRCLK / pin11','panel'),
('PANEL-LATCH','J7.5','Arduino D7','74HC595 RCLK / pin12','panel'),
('BTN-NEXT','J7.6','Arduino A3','진행 버튼 / 2초 누름','panel')
])
# Historical label text is retained only in the archived functional drawing.
labels=[tuple(v.replace('0V-MAG 공통','0V-PWR 상부 분배블록').replace('mag-ground','power-ground') if isinstance(v,str) else v for v in row) for row in labels]
import csv
with (ROOT/'hardware/pin-and-wire-labels.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['양쪽 선 라벨','새 단자','제어반 쪽','현장/모듈 쪽','연결 ID']);w.writerows(labels)
table='<div id="labels-drawing" hidden style="padding:20px"><div style="margin-bottom:16px;font-size:12px;color:#738a96">양 끝에 같은 라벨을 붙입니다. 새 단자번호는 이번 재결선 설계 기준입니다.</div><table style="width:100%;border-collapse:collapse;font-size:12px"><thead><tr>'+''.join('<th style="text-align:left;padding:10px 6px;border-bottom:2px solid #dce6ea">'+s+'</th>' for s in ['선 라벨','새 단자','제어반','현장 / 모듈'])+'</tr></thead><tbody>'
for label,terminal,start,end,net in labels:table+='<tr tabindex="0" role="button" data-select-net="'+net+'">'+''.join('<td style="padding:10px 6px;border-bottom:1px solid #e5ecef">'+v+'</td>' for v in [label,terminal,start,end])+'</tr>'
table+='</tbody></table></div>'
with (ROOT/'hardware/wire-segments.csv').open(encoding='utf-8-sig') as f:fullrows=list(csv.reader(f))
import html
fulltable='<section class="fit-sheet"><h2>전체 설치 결선표 · 실제 선 구간</h2><p>기존 회로 ID를 먼저 붙인 뒤, 새 단자대에서 나뉘는 선에는 -C(함체)/-F(현장)를 붙입니다. 각 새 선 양 끝에 같은 구간 라벨을 사용합니다. T1은 신호12자리, T2는 부하12자리이며 조건부 회로는 적용 확인 후 연결합니다. X2/X5는 모듈 핀 별칭입니다.</p><div class="table-scroll"><table><thead><tr>'+''.join('<th>'+html.escape(v)+'</th>' for v in fullrows[0])+'</tr></thead><tbody>'
for rr in fullrows[1:]:fulltable+='<tr>'+''.join('<td>'+html.escape(v)+'</td>' for v in rr)+'</tr>'
fulltable+='</tbody></table></div></section>'
table=table[:-6]+fulltable+'</div>'
page=page.replace('<img class="photograph"',table+'<img class="photograph"')
steps=''.join(f'<div class="step"><span class="step-num">{i}</span><span class="step-name">{n}</span></div>' for i,n in enumerate(['액자','조명 ×3','열쇠','RFID','책','종료']))
vals={'CSS':(src/'app.css').read_text(encoding='utf-8'),'CABINET_SVG':(ROOT/'hardware/cabinet-layout.svg').read_text(encoding='utf-8'),'DESIGN_SVG':(ROOT/'hardware/cabinet-redesign.svg').read_text(encoding='utf-8'),'PHOTO':'data:image/jpeg;base64,'+base64.b64encode((ROOT/'evidence/cabinet-original.jpg').read_bytes()).decode(),'AVR_LIB':(ROOT/'simulation/vendor/avr8js-0.21.1.min.js').read_text(encoding='utf-8'),'RUNNER':(src/'runner.js').read_text(encoding='utf-8'),'FIRMWARE_DATA':(src/'firmware-data.js').read_text(encoding='utf-8'),'APP':(src/'app.js').read_text(encoding='utf-8'),'STEPS':steps}
# User file opens offline: no server, network imports, API, or account needed.
vals['GROUND_SVG']=(ROOT/'hardware/ground-topology.svg').read_text(encoding='utf-8')
vals['APP']+='\n'+(src/'fit.js').read_text(encoding='utf-8')
for key,value in vals.items():page=page.replace('{{'+key+'}}',value)
assert '{{' not in page
(ROOT/'simulation/index.html').write_text(page,encoding='utf-8')
print('Offline workbench',len(page.encode('utf-8')),'bytes')
