"""New cabinet system design: isolated magnet supply, common logic return.
Coordinates are illustrative, not manufacturing dimensions.
"""
from pathlib import Path
import re,xml.etree.ElementTree as ET
import draw_cabinet as d

ROOT=Path(__file__).resolve().parents[1]
NS={'s':'http://www.w3.org/2000/svg'}
ET.register_namespace('','http://www.w3.org/2000/svg')
original=ET.parse(ROOT/'hardware/cabinet-layout.svg').getroot()
devices={g.attrib['data-part']:g for g in original.findall('s:g',NS) if 'data-part' in g.attrib}
d.out=[]
a=d.add;t=d.text;r=d.rect;c=d.circle;line=d.line;screw=d.screw
a('<svg xmlns="http://www.w3.org/2000/svg" id="redesign-svg" width="1180" height="1230" viewBox="0 0 1180 1230" role="img" aria-label="새 몽샷 배전함: RFID 회색 제어함과 릴레이 2장, 공통 로직 GND, 절연 전자석 0V">')
a(ET.tostring(original.find('s:defs',NS),encoding='unicode'))
a('<style>text{font-family:"Malgun Gothic","Noto Sans KR",Arial,sans-serif}.device{cursor:pointer;outline:none}.device:focus{filter:drop-shadow(0 0 3px #13a6a0)}.selected-device{filter:drop-shadow(0 0 5px #18a7a0)}.net{stroke-linecap:round;stroke-linejoin:round}.net-hit{stroke:transparent;stroke-width:16;fill:none;cursor:pointer}.power-net{display:none}.show-power .power-net{display:initial}.selected-net{stroke-width:5!important;opacity:1!important}.dim-net{opacity:.12!important}.domain-wire{stroke-width:3}.wire-tag{paint-order:stroke;stroke:#f2f6f7;stroke-width:4;stroke-linejoin:round}</style>')
r(190,24,790,1114,'#d1dade',14,'#aab7be');r(203,37,764,1088,'#f9fbfc',8,'#b4c1c8');r(225,80,718,1016,'url(#backplate)',3,'#c3ced3')
for x in [214,955]:
 for y in [50,1112]:screw(x,y,5)
t(247,65,'MONG SHOT  /  NEW CONTROL CABINET',14,'#526571');t(925,65,'再배선 설계안'.replace('再','재'),12,'#526571',500,'end')

# Reused mains adapters, fixed as complete units in a segregated top zone.
r(238,95,692,163,'#eef1f2',4,'#ccd6da');t(254,115,'AC 구역 · 완제품 멀티탭/어댑터 고정 · 저압 배선과 덕트 분리',12,'#6f818b')
r(254,127,656,29,'#f8fafb',5,'#bfcbd1')
for x in range(284,891,76):
 c(x,141,9,'#dae2e6','#c2cdd1');c(x-3,141,1.7,'#657780');c(x+3,141,1.7,'#657780')
for part,name,volts,x in [('pslogic','PS-L','5V LOGIC',251),('psaudio','PS-A','12V AUDIO',419),('psmotor','PS-MOT','기존 모터전원',587),('psmag','PS-MAG','12V MAGNET',755)]:
 d.begin(part,name+' '+volts)
 r(x,174,147,59,'#37434b',5,'#29363e',extra='filter="url(#boardshadow)"');r(x+8,181,131,44,'#414e57',3)
 for yy in range(187,221,6):line(x+10,yy,x+23,yy,'#6c7981',1)
 t(x+82,199,name,13,'#e2e9ed',500,'middle');t(x+82,217,volts,10,'#aebfc9',500,'middle');line(x+25,174,x+25,158,'#7c8b94',3)
 d.end()
d.rail(241,280,684);r(237,270,692,16,'url(#duct-slots)',2)

def bus(part,x,y,w,color,label,net):
 d.begin(part,label)
 r(x,y,w,29,color,2,'#99aeb8')
 n=int(w//20)
 for i in range(n):
  xx=x+10+i*20
  r(xx-7,y+2,14,24,'#d7e2e4',1,'#bac9ce');screw(xx,y+9,3.4);r(xx-3,y+19,6,5,'#667d87',1)
 line(x+9,y+17,x+w-10,y+17,color,3)
 t(x,y-10,label,13,color)
 d.end()
bus('gnd',246,476,354,'#278d86','0V-L  共通GND'.replace('共通','공통'),'gnd')
bus('mag-ground',747,363,172,'#aa7941','0V-MAG  전자석 전용','mag-ground')
bus('motor-ground',747,879,172,'#8f72b8','0V-MOT  모터 귀환','motor-ground')

# Fused magnet supply distribution.
d.begin('mag-power','전자석 전용 +12V 개별 퓨즈')
t(747,310,'+12V-MAG · 개별 퓨즈',12,'#a37840')
for i in range(3):
 x=750+i*54;r(x,321,45,27,'#c7b99d',2,'#a9987b');r(x+8,324,28,18,'#f2e9d4',1,'#ac9b79');line(x+22,326,x+22,340,'#a38b63',2);t(x+22,356,'F'+str(i+1),10,'#8b774f',500,'middle')
d.end()

def place(part,dx,dy,scale=1):
 g=ET.tostring(devices[part],encoding='unicode')
 a(f'<g transform="translate({dx} {dy}) scale({scale})">{g}</g>')
place('amp',-14,195)  # 248 / 300
place('mp3',-154,195) # 515 / 313
place('uno',-52,34)   # 280 / 535
place('relayA',352,212) # 610 / 519
place('l298',38,191)  # 747 / 723
place('relayB',1,619) # full-size board at 610 / 926; preserve existing wiring
t(746,913,'4CH B · 기존 배선 보존',12,'#59707c',500,'middle')
t(746,1083,'사용 여부를 코드만으로 판단하지 않음',11,'#6f8590',500,'middle')

# User-confirmed large gray RFID enclosure: reserve its actual mechanical space.
d.begin('rfidbox','RFID 회색 제어함 · 기존 함체 전체 수용')
r(279,796,251,286,'#b9c3ca',7,'#8d9ba5',extra='filter="url(#boardshadow)"')
r(287,804,235,270,'#dce2e6',5,'#a6b3bc')
r(300,818,209,240,'#d4dce1',3,'#b1bec6')
for x in [299,510]:
 for y in [817,1061]:screw(x,y,5)
for y in range(839,929,11):line(314,y,328,y,'#a7b5bd',2)
r(347,852,141,60,'#edf1f3',2,'#bac7cf')
t(417,876,'RFID CONTROL',14,'#536d7a',500,'middle')
t(417,897,'기존 회색 제어함',12,'#6c828e',500,'middle')
t(407,955,'내부 장치·기존 전원 유지',12,'#718793',500,'middle')
t(407,978,'A5 감지 출력 경로 표시',11,'#718793',500,'middle')
t(407,1001,'실물 크기·케이블 여유 반영',11,'#718793',500,'middle')
for y in [1025,1051]:r(521,y,17,17,'#758892',4);c(537,y+8,4,'#4b6775')
line(279,1048,256,1048,'#7f8e97',4)
t(248,1043,'기존 급전',10,'#7e929d',500,'end')
d.end()

# Field connectors and external loads.
inputparts=[('frame','D8',561),('light','A0',631),('key','A1',701),('rfid','A5',771),('book','D6',841)]
for i,(part,pin,y) in enumerate(inputparts):
 d.begin(part,part+' '+pin)
 r(12,y-22,149,50,'#fff',6,'#ced9de');t(27,y-1,{'frame':'액자 리드','light':'조명','key':'열쇠','rfid':'RFID 출력','book':'책 리드'}[part],13,'#46616e');t(145,y-1,pin,11,'#60827f',500,'end');t(27,y+17,'함 내부 제어함 → A5' if part=='rfid' else 'S + 0V-L'+(' · 100Ω' if part=='book' else ''),10,'#8a9ca5')
 d.end()
 d.terminal(239,y-10,3,['S','V*','0'],'#739c84');t(297,y+2,'X1.'+str(i+1),10,'#5d7b86')
 line(162,y,239,y,'#2b9d97',2);line(162,y+12,239,y+12,'#94a5ad',1.3)

for j,(part,name,pin) in enumerate([('mold','몰딩 전자석',12),('slide','슬라이드 전자석',10),('bookload','책 전자석',9)]):
 y=420+j*94
 d.begin(part,name)
 r(1003,y-12,160,68,'#fff',6,'#d6ddd8');r(1015,y+5,37,25,'url(#metal)',2,'#9eafb8');screw(1022,y+17,2);screw(1045,y+17,2);t(1062,y+10,name,12,'#4f6871');t(1062,y+28,'12V / D'+str(pin),10,'#8c9b9f');c(994,y+21,4,'#8b9ca5',extra=f'id="new-load-led-{pin}"')
 d.end()
d.begin('window','창문 무전압 접점')
r(1003,723,160,69,'#fff',6,'#ced9de');t(1017,749,'창문 · A4 / D18',12,'#4f6871');t(1017,769,'무전압 접점만 인출',10,'#8c9b9f');d.end()
d.begin('motor','리니어 액추에이터')
r(1003,831,160,67,'#fff',6,'#ced9de');r(1015,859,46,13,'#8d9ba3',4);r(1055,855,60,22,'url(#metal)',3);r(1107,863,33,7,'#a4afb6');t(1080,848,'리니어 액추에이터',11,'#4f6871',500,'middle');d.end()

# A visible isolation gap. Relays bridge this gap through their contacts only.
line(713,306,713,450,'#c8b28b',2,extra='stroke-dasharray="5 5"')
t(703,446,'전자석 절연 경계',11,'#aa7941',500,'end')
t(622,466,'릴레이: 코일/제어 ↔ 접점 절연',11,'#6f8793')

def net(key,pts,color,layer='domain',dash=None):
 path='M'+'L'.join(f'{x} {y}' for x,y in pts)
 cls='net '+('power-net' if layer=='power' else 'domain-wire' if layer=='domain' else '')
 a(f'<path d="{path}" fill="none" stroke="#f1f5f6" stroke-width="6" class="{cls}" data-net="{key}"/>')
 a(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="2.5" class="{cls}" data-net="{key}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 a(f'<path d="{path}" class="net-hit '+('power-net' if layer=='power' else '')+f'" data-net="{key}"/>')

# Continuous control GND: each field return reaches a terminal on the same bridged bus.
for i,(_,_,y) in enumerate(inputparts):net('gnd',[(277,y+12),(315+i*6,y+12),(315+i*6,510),(267+i*20,510),(267+i*20,491)],'#278d86')
net('gnd',[(276,233),(276,264),(230,264),(230,490),(246,490)],'#278d86')
net('gnd',[(469.84,749.48),(469.84,778),(603,778),(603,491),(586,491)],'#278d86')
net('gnd',[(625,659),(625,691),(603,691)],'#278d86')
net('gnd',[(540,404),(540,460),(567,460),(567,491)],'#278d86')

# Magnet return never joins logic, motor, PE, or audio.
net('mag-ground',[(781,233),(781,263),(925,263),(925,378),(919,378)],'#aa7941')
for j in range(3):
 y=441+j*94
 net('mag-ground',[(1002,y+12),(969+j*6,y+12),(969+j*6,378),(898-j*20,378)],'#aa7941')
 net('mag-power',[(822,233),(822,264),(742,264),(742,334),(750+j*54,334)],'#c67a5b','power')
 net('load'+str([12,10,9][j]),[(773+j*54,348),(720-j*7,348+j*4),(720-j*7,488),(640+j*64,488),(640+j*64,515)],'#ab7558','power')
 net('load'+str([12,10,9][j]),[(653+j*64,515),(653+j*64,500-j*6),(954,500-j*6),(954,y),(1002,y)],'#ab7558','power')

# Motors retain a dedicated high-current loop and one explicit reference bond.
net('motor-ground',[(612,233),(612,260),(936,260),(936,894),(919,894)],'#8f72b8')
net('motor-ground',[(777,876),(777,894)],'#8f72b8')
net('motor-bond',[(747,894),(714,894),(714,790),(603,790),(603,491),(600,491)],'#8f72b8',dash='7 4')
t(705,810,'基準1点'.replace('基準1点','기준 한 점'),11,'#8f72b8',500,'end')
net('motor-supply',[(674,233),(674,272),(942,272),(942,876),(762,876)],'#b37264','power')
net('actuator',[(913,777),(990,777),(990,869),(1002,869)],'#ab7558','power')
net('window',[(847,515),(935,515),(935,757),(1002,757)],'#81959e','signal',dash='5 4')

# Signal harness: exact Uno pins, new terminal numbers.
ux,uy,sc=280,535,1.12
pin={8:(173,9),6:(198.5,9),12:(134.5,9),10:(153.5,9),9:(163,9),18:(246,191.5),'A0':(208,191.5),'A1':(217.5,191.5),'A5':(255.5,191.5),4:(217.5,9),5:(208,9),16:(227,191.5),2:(236.5,9),3:(227,9)}
def pp(p):x,y=pin[p];return ux+x*sc,uy+y*sc
for j,(name,p,y) in enumerate([('frame',8,561),('light','A0',631),('key','A1',701),('rfid','A5',771),('book',6,841)]):
 sx,sy=pp(p)
 if p in [8,6]:pts=[(239,y),(219-j*4,y),(219-j*4,521-j*5),(sx,521-j*5),(sx,sy)]
 else:pts=[(239,y),(219-j*4,y),(219-j*4,781+j*5),(sx,781+j*5),(sx,sy)]
 net(name,pts,'#2b9d97','signal')
net('rfidbox-output',[(538,1033),(557,1033),(557,789),(231,789),(231,771),(239,771)],'#2b9d97','signal',dash='6 4')
t(558,1039,'감지 출력',10,'#5e8f88')
for j,p in enumerate([12,10,9,18]):
 sx,sy=pp(p);tx=625+j*19
 if p!=18:pts=[(sx,sy),(sx,509-j*6),(tx,509-j*6),(tx,657)]
 else:pts=[(sx,sy),(sx,771),(tx,771),(tx,657)]
 net('out'+str(p),pts,'#597ac5','signal')
for j,p in enumerate([4,5,16]):
 sx,sy=pp(p);tx=828+j*11
 net('motor'+str(p),[(sx,sy),(sx,785+j*6),(tx,785+j*6),(tx,867)],'#8f72b8','signal')
net('audio',[(670,359),(687,359),(687,439),(353,439),(353,405)],'#9a80ae','signal')
for j,p in enumerate([2,3]):
 sx,sy=pp(p);tx=579+j*20
 net('uart'+str(p),[(sx,sy),(sx,511-j*7),(705+j*5,511-j*7),(705+j*5,429),(tx,429),(tx,404)],'#b99445','signal')
net('logic-power',[(337,233),(337,269),(236,269),(236,592),(281,592)],'#c26c66','power')
net('audio-power',[(483,233),(483,264),(551,264),(551,405)],'#c26c66','power')
t(244,1114,'RFID 회색함·릴레이 2장 모두 수용 / 0V-L 공통 버스와 0V-MAG 분리 유지',11,'#657e89')
t(242,1173,'설계 기준: 부품 누락 없이 재배치 · B 보드 예비/불필요 판단 철회 · RFID 기존 회로 유지',12,'#506d79')
t(242,1198,'기존 600×800×200 mm 후보는 보류 · RFID 함체 실측 후 외함 크기 확정 · 그림은 축척 아님',11,'#83959e')
a('</svg>')
svg='\n'.join(d.out)
# Keep SVG gradient IDs unique when both drawings are in the same HTML document.
for old in ['metal','backplate','ampbody','boardshadow','duct-slots','led-body','ledFilter','pin-female','pin-male','mcu-leads']:
 svg=svg.replace('id="'+old+'"','id="new-'+old+'"').replace('url(#'+old+')','url(#new-'+old+')').replace('href="#'+old+'"','href="#new-'+old+'"')
(ROOT/'hardware/cabinet-redesign.svg').write_text(svg,encoding='utf-8')
print('Redesign drawing ready')
