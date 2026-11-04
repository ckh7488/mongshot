"""Current cabinet target: one 12V SMPS, 5V buck, two real common distribution blocks.
All DC returns are electrically common; branch routing is not galvanic isolation.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import draw_cabinet as d
ROOT=Path(__file__).resolve().parents[1]
NS={'s':'http://www.w3.org/2000/svg'}
ET.register_namespace('','http://www.w3.org/2000/svg')
orig=ET.parse(ROOT/'hardware/cabinet-layout.svg').getroot()
devices={g.attrib['data-part']:g for g in orig.findall('s:g',NS) if 'data-part' in g.attrib}
d.out=[]
a=d.add;t=d.text;r=d.rect;c=d.circle;line=d.line;screw=d.screw
a('<svg xmlns="http://www.w3.org/2000/svg" id="redesign-svg" width="1480" height="1230" viewBox="0 0 1480 1230" role="img" aria-label="새 배전함: 12V SMPS 하나, 5V DC-DC, 실제 공통 분배블록, RFID 회색함, 릴레이 두 장, 외부 LED와 진행 버튼">')
a(ET.tostring(orig.find('s:defs',NS),encoding='unicode'))
a('<style>text{font-family:"Malgun Gothic",Arial,sans-serif}.device{cursor:pointer;outline:none}.device:focus,.selected-device{filter:drop-shadow(0 0 4px #20a297)}.net{stroke-linecap:round;stroke-linejoin:round}.net-hit{stroke:transparent;stroke-width:15;fill:none;cursor:pointer}.power-net{display:none}.show-power .power-net{display:initial}.selected-net{stroke-width:5!important;opacity:1!important}.dim-net{opacity:.14!important}</style>')
r(173,25,1091,1130,'#d1dade',14,'#aab7be');r(187,39,1063,1102,'#f8fbfc',8,'#b4c1c8');r(210,80,1016,1030,'url(#backplate)',3,'#c3ced3')
for x in [198,1240]:
 for y in [51,1127]:screw(x,y,5)
t(231,64,'MONG SHOT / SINGLE-SMPS CABINET',17,'#526571')
t(1210,64,'RFID 함체 + 릴레이 2장 보존',13,'#718892',500,'end')

# One actual-shaped SMPS, with a guarded AC terminal area.
d.begin('smps','12V 메인 SMPS 1대')
r(248,111,664,144,'#b6c0c6',5,'#8c9aa3',extra='filter="url(#boardshadow)"');r(255,118,650,115,'#dce3e7',3)
for yy in range(128,225,16):
 for xx in range(270,675,19):c(xx,yy,3.3,'#a5b4bd')
r(702,132,182,71,'#edf2f5',3,'#bac6cd');t(794,160,'12V SMPS ×1',21,'#536d7a',500,'middle');t(794,184,'전류 용량은 동시 부하로 선정',12,'#8398a3',500,'middle')
for i,label in enumerate(['L','N','PE','V−','V−','V+','V+']):
 x=466+i*57;r(x,235,47,29,'#515b62',2);screw(x+23,247,5);t(x+23,282,label,12,'#5c7481',500,'middle')
r(458,230,172,38,'#e5c993',3,'#bfa25f',extra='fill-opacity=".7"');t(545,302,'AC 단자 보호커버 / PE 별도',11,'#967f56',500,'middle')
d.end()

def block(part,x,y,w,color,title,ports):
 d.begin(part,title)
 r(x,y,w,84,color,5,'#7f99a7',extra='filter="url(#boardshadow)"')
 r(x+8,y+8,48,67,'#d5e1e8',3,'#a6bac5');c(x+32,y+32,10,'#506e7e');r(x+20,y+53,24,9,'#e9ac55',2)
 step=(w-73)/6
 for i in range(12):
  xx=x+68+(i%6)*step;yy=y+17+(i//6)*34
  c(xx,yy,6,'#405e70');r(xx-6,yy+11,12,5,'#f1ad4f',1)
 t(x,y-14,title,15,'#426c7f')
 t(x+w/2,y+105,'내부 도체로 13개 단자 모두 공통',11,'#8396a0',500,'middle')
 d.end()
block('gnd',249,369,359,'#78a8c0','0V-L  로직 공통 분배블록',None)
block('power-ground',881,369,306,'#849cac','0V-PWR  고전류 귀환 분배블록',None)

# DC/DC: independent 5V rail, with common in/out negative.
d.begin('buck','12V → 5V DC-DC · 비절연형 기본안')
r(972,125,209,135,'#37887d',5,'#28685f',extra='filter="url(#boardshadow)"')
r(1032,145,77,59,'#85844c',5,'#696f47');c(1071,175,22,'#bca668','#756f4b');c(1071,175,12,'#4e6d68')
for x in [996,1156]:c(x,172,13,'#2d404b','#b5c5cd');c(x,172,8,'#bdcbd1')
d.terminal(980,222,2,['IN+','IN−'],'#7fa7b8');d.terminal(1132,222,2,['5V+','0V'],'#7fa7b8')
t(1075,282,'5V 로직 분기 / Arduino LDO로 코일 급전 금지',11,'#6c8793',500,'middle')
d.end()

d.begin('mag-power','12V 부하별 퓨즈 분기')
t(643,344,'+12V 개별 퓨즈 분기',14,'#9e7950')
for i in range(6):
 x=641+(i%3)*68;y=365+(i//3)*43;r(x,y,56,32,'#b4a68f',2,'#9e8f76');r(x+9,y+5,38,21,'#eee4d3',2);t(x+28,y+20,'F'+str(i+1),11,'#9f8d6e',500,'middle')
t(736,472,'자석 ×3 / 모터 / 오디오 / DC-DC',11,'#8d9496',500,'middle')
d.end()

for y in [313,682,900]:r(223,y,990,23,'url(#duct-slots)',2)
for y in [599,855,1071]:d.rail(232,y,973)
def place(part,dx,dy,scale=1):a(f'<g transform="translate({dx} {dy}) scale({scale})">'+ET.tostring(devices[part],encoding='unicode')+'</g>')
place('uno',-86,-3) # actual board x246 / y498
place('relayA',357,193) # 615 / 500
place('relayB',331,193) # 940 / 500
t(754,480,'A · 네 출력의 조건부 재배치안',12,'#708894',500,'middle')
t(1078,480,'B · 기존 채널/배선 보존',12,'#708894',500,'middle')
place('amp',289,664) # 551 / 769
place('mp3',236,667) # 905 / 785
place('l298',300,398) # 1009 / 930

# The large user-confirmed gray RFID assembly is kept as a whole.
d.begin('rfidbox','RFID 회색 제어함 · 함체/기존 회로 전체 유지')
r(252,770,254,290,'#b7c3ca',7,'#8b9ba5',extra='filter="url(#boardshadow)"');r(261,779,236,272,'#d5dee4',5,'#a7b7c1')
for x in [272,487]:
 for y in [790,1039]:screw(x,y,5)
r(305,829,159,70,'#edf2f5',3,'#b8c8d1');t(384,857,'RFID CONTROL',16,'#526e7c',500,'middle');t(384,882,'기존 회색 제어함',13,'#7b929f',500,'middle')
for y in range(824,940,14):line(278,y,290,y,'#a1b4bf',2)
t(381,955,'감지 출력 → A5',13,'#6f8d99',500,'middle');t(381,979,'급전·출력 방식은 기존 정격 적용',12,'#8298a4',500,'middle')
r(495,1002,17,18,'#718690',4);r(495,1030,17,18,'#718690',4)
d.end()

# Front door: actual six indicators and manual next button.
d.begin('frontpanel','함체 외부 LED 6개와 2초 진행 버튼')
r(1293,41,169,299,'#d7e0e5',9,'#a2b5c0');r(1301,49,153,283,'#f2f6f8',6)
t(1378,74,'외부 조작부',14,'#4f7282',500,'middle')
for i,label in enumerate(['액자','조명','열쇠','RFID','책','완료']):
 y=102+i*28;c(1323,y,8,'#8a9ca6','#657d89',extra=f'id="panel-led-{i}"');t(1343,y+5,label,13,'#65818f')
c(1378,296,19,'#455c6a','#253f4d',extra='data-action="manual-next"');c(1378,296,12,'#a9bbc5',extra='data-action="manual-next"');t(1378,327,'진행 · 2초 누름',12,'#678491',500,'middle')
d.end()
t(1378,364,'J7: 5V / 0V / DATA',10,'#8a9da7',500,'middle');t(1378,381,'CLK / LATCH / BTN',10,'#8a9da7',500,'middle')

inputs=[('frame','액자 리드','D8',514),('light','조명','A0',604),('key','열쇠','A1',694),('rfid','RFID 함내 출력','A5',784),('book','책 리드','D6 · 100Ω',874)]
for i,(name,label,pin,y) in enumerate(inputs):
 d.begin(name,label)
 r(10,y-21,148,53,'#fff',6,'#d1dde3');t(23,y, label,13,'#597a89');t(23,y+20,pin,11,'#91a3ac');d.end()
 d.terminal(216,y-10,3,['S','V*','0'],'#739c84');t(270,y+6,'X1.'+str(i+1),10,'#87a0ad')
 line(158,y,216,y,'#2b9d97',2.4)
 if name!='rfid':line(158,y+13,216,y+13,'#8fa6b1',1.5)

for i,(part,label,pin,y) in enumerate([('mold','몰딩 전자석',12,443),('slide','슬라이드 전자석',10,536),('bookload','책 전자석',9,629),('window','창문 독립 접점',18,722),('motor','리니어 액추에이터',16,1008)]):
 d.begin(part,label);r(1292,y-23,171,67,'#fff',6,'#cfdae1');t(1305,y,label,13,'#587988');t(1305,y+23,'A4 / D18' if pin==18 else 'L298N 구동' if pin==16 else '12V / D'+str(pin),11,'#8da1ad');c(1283,y+9,4,'#8b9ca5',extra=f'id="new-load-led-{pin}"');d.end()

def net(key,points,color='#2b9d97',layer='signal',dash=None):
 path='M'+'L'.join(f'{x} {y}' for x,y in points);cls='net '+('power-net' if layer=='power' else '')
 a(f'<path d="{path}" fill="none" stroke="#f1f5f6" stroke-width="5.5" class="{cls}" data-net="{key}"/>')
 a(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.6" class="{cls}" data-net="{key}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 a(f'<path d="{path}" class="net-hit '+('power-net' if layer=='power' else '')+f'" data-net="{key}"/>')

# Common potential, separately routed returns. IN−/OUT− are connected by the buck.
net('power-ground',[(660,264),(660,290),(1194,290),(1194,400),(914,400)],'#987a5d')
net('buck-reference',[(1002,246),(1002,340),(922,340),(922,398)],'#987a5d')
net('gnd',[(1154,246),(1213,246),(1213,348),(235,348),(235,400),(281,400)],'#278d86')
for i,(_,_,_,y) in enumerate(inputs):
 if i==3:continue # RFID reference/output type must follow actual interface.
 net('gnd',[(253,y+13),(292+i*7,y+13),(292+i*7,458),(330+i*25,458),(330+i*25,419)],'#278d86')
net('gnd',[(386,712),(386,742),(579,742),(579,425)],'#278d86')
net('gnd',[(630,640),(630,661),(599,661),(599,435)],'#278d86')
net('gnd',[(955,640),(955,664),(606,664),(606,435)],'#278d86')
net('gnd',[(935,873),(935,928),(607,928),(607,438)],'#278d86')
net('logic-power',[(1139,246),(1230,246),(1230,345),(607,345),(607,495),(247,495),(247,558)],'#bd6f66','power')

ux,uy,sc=246,498,1.12
pins={8:(173,9),6:(198.5,9),12:(134.5,9),10:(153.5,9),9:(163,9),18:(246,191.5),'A0':(208,191.5),'A1':(217.5,191.5),'A5':(255.5,191.5),4:(217.5,9),5:(208,9),16:(227,191.5),2:(236.5,9),3:(227,9),11:(144,9),13:(125,9),7:(189,9),17:(236.5,191.5)}
def pp(pin):x,y=pins[pin];return ux+x*sc,uy+y*sc
for i,(name,pin,y) in enumerate([('frame',8,514),('light','A0',604),('key','A1',694),('rfid','A5',784),('book',6,874)]):
 x,z=pp(pin)
 net(name,[(216,y),(195-i*4,y),(195-i*4,479-i*6 if pin in [8,6] else 751+i*5),(x,479-i*6 if pin in [8,6] else 751+i*5),(x,z)])
net('rfidbox-output',[(512,1012),(539,1012),(539,798),(210,798),(210,784),(216,784)],'#2b9d97',dash='6 4')
for i,pin in enumerate([12,10,9,18]):
 x,z=pp(pin);end=630+i*19
 route=474-i*7 if pin!=18 else 734
 net('out'+str(pin),[(x,z),(x,route),(end,route),(end,640)],'#597ac5')
for i,pin in enumerate([4,5,16]):
 x,z=pp(pin);net('motor'+str(pin),[(x,z),(x,945+i*8),(1088+i*11,945+i*8),(1088+i*11,1078)],'#8f72b8')
for i,pin in enumerate([2,3]):
 x,z=pp(pin);net('uart'+str(pin),[(x,z),(x,467-i*8),(895-i*6,467-i*8),(895-i*6,890),(968+i*20,890),(968+i*20,876)],'#b99445')
net('audio',[(1078,833),(1101,833),(1101,923),(705,923),(705,875)],'#9a80ae')
for i,pin in enumerate([12,10,9]):
 y=443+i*93;net('load'+str(pin),[(651+i*64,496),(651+i*64,480-i*6),(1264+i*5,480-i*6),(1264+i*5,y+9),(1291,y+9)],'#ab7558','power')
 net('power-ground',[(1291,y+29),(1240-i*8,y+29),(1240-i*8,432),(1137-i*22,432),(1137-i*22,400)],'#987a5d')
net('power-ground',[(1038,1078),(1038,1100),(1218,1100),(1218,448),(1115,448),(1115,419)],'#987a5d')
net('power-ground',[(800,875),(800,941),(1208,941),(1208,455),(1093,455),(1093,419)],'#987a5d')
net('window',[(846,496),(1254,496),(1254,731),(1291,731)],'#859ca7',dash='5 4')
net('actuator',[(1176,983),(1272,983),(1272,1017),(1291,1017)],'#ab7558','power')
for i,pin in enumerate([11,13,7,17]):
 x,z=pp(pin);net('panel',[(x,z),(x,459-i*6 if pin!=17 else 745),(1220-i*6,459-i*6 if pin!=17 else 745),(1220-i*6,210+i*10),(1292,210+i*10)],'#6492a4','signal',dash='5 4')
t(232,1134,'0V-L과 0V-PWR은 비절연 DC-DC를 통해 전기적으로 공통입니다. 전자석은 릴레이 접점으로 스위칭합니다.',14,'#688795')
t(231,1185,'기본안: 12V SMPS 1대 + 5V DC-DC / 대안: 5V SMPS 추가 / 외함 크기는 RFID 함체 실측 후 선정',14,'#5d7d8b')
t(231,1211,'분배블록은 내부 공통 도체가 있는 제품 사용 · 일반 독립 단자대라면 정격 공통 점퍼 필요 · PE는 별도',12,'#91a3ad')
a('</svg>')
svg='\n'.join(d.out)
for name in ['metal','backplate','ampbody','boardshadow','duct-slots','led-body','ledFilter','pin-female','pin-male','mcu-leads']:
 svg=svg.replace('id="'+name+'"','id="s-'+name+'"').replace('url(#'+name+')','url(#s-'+name+')').replace('href="#'+name+'"','href="#s-'+name+'"')
(ROOT/'hardware/cabinet-redesign.svg').write_text(svg,encoding='utf-8')
print('Single-SMPS cabinet with RFID, two relays and door panel ready')
