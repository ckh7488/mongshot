"""Editable, deterministic cabinet illustration. No generated photographs.
Confirmed hardware/functions; the tidy arrangement/channel grouping is a proposal.
The Uno geometry is from @wokwi/elements (MIT); see vendor license.
"""
from pathlib import Path
from html import escape as esc
import json,re

ROOT=Path(__file__).resolve().parents[1]
out=[]
def add(s):out.append(s)
def text(x,y,t,size=14,fill='#34434d',weight=500,anchor=None,extra=''):
    add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}"'+(f' text-anchor="{anchor}"' if anchor else '')+f' {extra}>{esc(t)}</text>')
def rect(x,y,w,h,fill,rx=0,stroke=None,extra=''):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+f' {extra}/>')
def circle(x,y,r,fill,stroke=None,extra=''):
    add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+f' {extra}/>')
def line(x1,y1,x2,y2,c='#9aa8af',w=1,extra=''):
    add(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{c}" stroke-width="{w}" {extra}/>')
def screw(x,y,r=4):
    circle(x,y,r,'#b9c2c4','#7a868b');line(x-r*.65,y+r*.45,x+r*.65,y-r*.45,'#5d676c',1.3)
def begin(part,label):add(f'<g class="device" data-part="{part}" role="button" aria-label="{esc(label)}" tabindex="0"><title>{esc(label)}</title>')
def end():add('</g>')
def rail(x,y,w):
    rect(x,y,w,23,'url(#metal)',2,'#b6c0c4')
    for yy in [y+4,y+19]:line(x+3,yy,x+w-3,yy,'#a8b3b9',1)
    for xx in range(int(x+20),int(x+w),55):rect(xx,y+8,22,6,'#8d9ba2',3)
def terminal(x,y,n=3,labels=None,color='#7ca585'):
    for i in range(n):
        xx=x+i*15
        rect(xx,y,14,25,color,1,'#547661');screw(xx+7,y+8,3.6);rect(xx+3,y+18,8,5,'#30423a',1)
        if labels:text(xx+7,y-5,labels[i],9,'#34434d',500,'middle')
def relay(x,y,part,title,pins):
    begin(part,title)
    rect(x,y,276,136,'#1f5a75',4,'#143f57',extra='filter="url(#boardshadow)"')
    for xx in [x+9,x+267]:
        for yy in [y+9,y+127]:circle(xx,yy,4.5,'#d4c58e');circle(xx,yy,2,'#4b5b65')
    text(x+15,y+26,title,13,'#e9f2f4')
    for i in range(4):
        xx=x+16+i*64
        terminal(xx,y-4,3,['NC','C','NO'],'#70a8bd')
        rect(xx,y+42,51,47,'#247fbb',3,'#145e91')
        line(xx+4,y+46,xx+47,y+46,'#53a0cf',1)
        text(xx+25,y+61,'SONGLE',9,'#d1e8f7',500,'middle')
        text(xx+25,y+74,'SRD-05VDC',7,'#d1e8f7',400,'middle')
        pin=pins[i] if i<len(pins) else None
        rect(xx+6,y+103,9,5,'#28363b',1)
        circle(xx+31,y+106,3.2,'#697f89',extra=f'id="relay-led-{pin or str(part)+str(i)}"')
        text(xx+25,y+126,f'D{pin}' if pin not in [None,18] else 'A4' if pin==18 else f'CH{i+1}',10,'#e3f1f5',500,'middle')
    rect(x+10,y+133,119,10,'#263039',1)
    for i in range(6):rect(x+15+i*19,y+135,3,5,'#cfb86c')
    end()

add('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" id="cabinet-svg" width="1180" height="940" viewBox="0 0 1180 940" role="img" aria-label="몽샷 배전함 정리 배치안과 실제 코드 핀 연결">')
add('''<defs>
<linearGradient id="metal" x2="0" y2="1"><stop stop-color="#e4e9ec"/><stop offset=".5" stop-color="#bfcbd0"/><stop offset="1" stop-color="#e1e7ea"/></linearGradient>
<linearGradient id="backplate" x2="1" y2="1"><stop stop-color="#f0f3f4"/><stop offset="1" stop-color="#e4eaec"/></linearGradient>
<linearGradient id="ampbody" x2="0" y2="1"><stop stop-color="#5a517e"/><stop offset="1" stop-color="#343451"/></linearGradient>
<filter id="boardshadow" x="-15%" y="-15%" width="140%" height="145%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#283740" flood-opacity=".16"/></filter>
<pattern id="duct-slots" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="12" height="12" fill="#d7dfe2"/><path d="M3 0v8M9 0v8" stroke="#becbd0" stroke-width="3"/></pattern>
</defs>
<style>text{font-family:'Malgun Gothic','Noto Sans KR',Arial,sans-serif} .device{cursor:pointer;outline:none}.device:focus{filter:drop-shadow(0 0 3px #13a6a0)} .net{stroke-linecap:round;stroke-linejoin:round}.net-hit{stroke:transparent;stroke-width:16;fill:none;cursor:pointer}.wire-tag{paint-order:stroke;stroke:#eef2f3;stroke-width:5;stroke-linejoin:round}.power-net{display:none}.show-power .power-net{display:initial}.selected-net{stroke-width:5!important;opacity:1!important}.dim-net{opacity:.14!important}.selected-device{filter:drop-shadow(0 0 4px #18a7a0)}</style>''')

# Enclosure, backplate, ducting, and DIN rails.
rect(202,28,738,849,'#d1dade',14,'#aab7be');rect(214,40,714,825,'#f9fbfc',8,'#b4c1c8');rect(236,81,670,745,'url(#backplate)',3,'#c3ced3')
for xx in [225,917]:
    for yy in [53,853]:screw(xx,yy,5)
text(254,65,'MONG SHOT  /  CONTROL CABINET',14,'#526571')
text(889,65,'정리 배치안',12,'#526571',500,'end')
rect(240,253,660,26,'url(#duct-slots)',2)
rect(240,454,660,24,'url(#duct-slots)',2)
rect(240,752,660,22,'url(#duct-slots)',2)
rail(250,387,637);rail(250,658,637);rail(250,803,637)

# Amplifier as an actual ribbed enclosure, not a block diagram.
begin('amp','HONGXING 12V 앰프')
rect(262,105,287,124,'#656078',3,extra='filter="url(#boardshadow)"');rect(274,110,263,113,'url(#ampbody)',3)
for xx in range(282,532,11):rect(xx,114,4,78,'#76708c',1);line(xx+4,114,xx+4,192,'#35364e',1)
rect(274,192,263,35,'#494565',2)
text(405,144,'HONGXING',19,'#eeedf6',600,'middle')
text(405,164,'12V AUDIO AMPLIFIER',9,'#d0cce1',500,'middle')
for xx in [285,524]:screw(xx,202,3)
rect(293,199,22,21,'#22252d',2);circle(304,210,5,'#4b4c55');circle(342,210,7,'#cdcbd6','#91939c');circle(367,210,7,'#cdcbd6','#91939c')
for i,c in enumerate(['#ba5353','#333944','#333944','#ba5353']):rect(407+i*21,199,16,21,c,2)
text(406,244,'MP3 IN → 앰프 → 스피커',12,'#485b66',500,'middle')
end()

# MP3 module: PCB, SD cage, IC, jack, UART header.
begin('mp3','KT403A MP3 모듈 · D2 RX / D3 TX')
rect(669,118,174,104,'#2b866b',5,'#236652',extra='filter="url(#boardshadow)"')
for xx in [677,835]:
    for yy in [126,214]:circle(xx,yy,3.5,'#d9c48d');circle(xx,yy,1.5,'#4a5d5d')
rect(718,130,70,61,'url(#metal)',2,'#98a6aa');rect(726,132,54,22,'#3c4247',2);text(753,170,'micro SD',10,'#576871',500,'middle')
rect(690,156,18,27,'#29353a',1)
for yy in range(160,182,5):line(686,yy,690,yy,'#b5b9ae',2);line(708,yy,712,yy,'#b5b9ae',2)
rect(811,151,27,31,'#28323b',2);circle(824,164,8,'#b7bdc1','#697980');circle(824,164,4,'#1e2933')
rect(686,201,90,10,'#303940',1)
for xx in [693,713,733,753]:rect(xx,203,4,6,'#cfb86c')
text(759,114,'KT403A',13,'#485b66',500,'middle');text(759,242,'UART 9600 baud',12,'#485b66',500,'middle')
end()

relay(258,307,'relayA','4CH RELAY A',[12,10,9,18]);relay(609,307,'relayB','4CH RELAY B',[])
text(396,294,'機능별 채널 배치안'.replace('機','기'),12,'#59707c',500,'middle');text(746,294,'기존 2번째 보드 보존',12,'#59707c',500,'middle')

# The actual Wokwi Arduino Uno illustration, at real pin coordinates.
begin('uno','Arduino · 실제 AVR 코드 실행')
uno=(ROOT/'hardware/assets/arduino-uno-wokwi.svg').read_text(encoding='utf-8')
uno=uno.replace('&nbsp;','&#160;')
uno=re.sub(r'width="[^"]*"','width="307.2"',uno,count=1);uno=re.sub(r'height="[^"]*"','height="225.8"',uno,count=1)
uno=uno.replace('<svg','<svg class="arduino-native" x="332" y="501"',1)
uno=uno.replace('>', '><style>.arduino-native text{font-size:2px;font-family:monospace;font-weight:400}</style>',1)
add(uno)
text(485,744,'ARDUINO · UNO 시뮬레이션 모델',12,'#485b66',500,'middle')
end()

# L298N module: red PCB, power terminals, capacitors, finned heatsink.
begin('l298','L298N E6 · 액추에이터 구동')
rect(709,532,175,162,'#b53c3e',4,'#853537',extra='filter="url(#boardshadow)"')
for xx in [718,875]:
    for yy in [541,684]:circle(xx,yy,4,'#cfb97c');circle(xx,yy,2,'#6f4e47')
rect(755,541,78,72,'#262d31',2)
for xx in range(760,831,8):rect(xx,544,3,66,'#546067',1)
for xx in [730,850]:circle(xx,yy:=632,12,'#26333c','#bbc0c4');circle(xx,yy,8,'#a6b1b6');line(xx-4,yy,xx+4,yy,'#68777e');line(xx,yy-4,xx,yy+4,'#68777e')
terminal(719,656,3,['+Vs','0V','5V'],'#6f9fc0');terminal(841,570,2,['M+','M−'],'#6f9fc0')
rect(783,676,73,10,'#27333a',1)
for i in range(6):rect(788+i*11,678,3,6,'#cfb86c')
text(797,526,'L298N E6',14,'#485b66',500,'middle');text(797,713,'D4 / D5 / A2(16)',12,'#485b66',500,'middle')
text(797,732,'ENABLE = HIGH (PWM 아님)',10,'#59707c',500,'middle')
end()

# Five field input connectors and their cabinet-side terminals.
inputs=[('frame','액자 리드','D8',8,332),('light','조명','A0',0,422),('key','열쇠','A1',1,512),('rfid','RFID 감지','A5',5,602),('book','책 리드','D6 · 100Ω',6,692)]
for key,name,pin,_,y in inputs:
    begin(key,name+' 입력 '+pin)
    rect(15,y-24,158,62,'#ffffff',7,'#ced9de');rect(26,y-11,27,34,'#d9e2e5',3,'#a9b8c0')
    if key in ['frame','book']:
        rect(31,y-5,7,22,'#eee9db',3,'#a8a592');rect(42,y-5,6,22,'#899697',2)
    else:
        circle(39,y+6,9,'#303f49','#91a2aa');circle(39,y+6,4,'#78978d')
    text(64,y+1,name,15,'#34434d');text(64,y+20,pin,12,'#70818b')
    circle(174,y,4,'#1c9b95');circle(174,y+14,4,'#80939e')
    end()
    terminal(246,y-10,2,['S','G'],'#739c84')
    # Field cable to terminal; pair only, Vcc depends on actual sensor.
    line(177,y,246,y,'#2b9d97',2.6,extra=f'class="net" data-net="{key}"')
    line(177,y+14,246,y+14,'#82949e',1.5,extra=f'class="net" data-net="gnd-{key}"')

# Four functional loads and one actuator on the right side of the enclosure.
loads=[('mold','몰딩 전자석','D12',12,330),('slide','슬라이드 전자석','D10',10,424),('window','창문 출력','A4 / D18',18,518),('bookload','책 전자석','D9',9,612)]
for key,name,pin,num,y in loads:
    begin(key,name)
    rect(980,y-22,181,69,'#fff',7,'#ced9de')
    if key!='window':
        rect(991,y-9,40,29,'url(#metal)',3,'#a1afb5')
        for xx in [998,1024]:circle(xx,y+5,3,'#7e9199')
    else:
        rect(992,y-10,36,34,'#e3e9ec',1,'#7a919d');line(1010,y-10,1010,y+24,'#7a919d');line(992,y+6,1028,y+6,'#7a919d')
    text(1040,y+1,name,13,'#34434d');text(1040,y+22,pin,11,'#70818b')
    circle(972,y+8,5,'#8b9ca5',extra=f'id="load-led-{num}"');end()
begin('motor','리니어 액추에이터')
rect(979,714,184,73,'#fff',7,'#ced9de');rect(998,738,64,19,'#939fa8',5,'#677982');rect(1047,734,72,27,'url(#metal)',4,'#9caaaf');rect(1109,743,35,9,'#a6b1b7',1);circle(1147,747.5,6,'#b9c3c9','#748991');text(1071,733,'리니어 액추에이터',12,'#34434d',500,'middle');end()

# Terminal distribution layer is an arrangement proposal, not a measured PSU rating.
begin('power','기존 DC 어댑터군과 전원 분배 배치안')
text(265,791,'5V 제어 분기',12,'#59707c');text(580,791,'12V 부하 분기',12,'#59707c')
terminal(266,800,10,None,'#819da8');terminal(582,800,10,None,'#b39b7a')
text(576,856,'기존 어댑터군 유지 · 정격·급전 경로는 현장값 적용',11,'#5f747e',500,'middle')
end()

# Actual pin endpoints on Uno at a known native scale.
ux,uy,sc=332,501,1.12
pins={12:(134.5,9),10:(153.5,9),9:(163,9),8:(173,9),6:(198.5,9),5:(208,9),4:(217.5,9),3:(227,9),2:(236.5,9),16:(227,191.5),18:(246,191.5),'A0':(208,191.5),'A1':(217.5,191.5),'A5':(255.5,191.5),'5V':(160,191.5),'GND':(169.5,191.5)}
def pp(p):a,b=pins[p];return round(ux+a*sc,2),round(uy+b*sc,2)
nets=[]
def net(key,label,pts,color='#2b9d97',layer='signal',certainty='functional-confirmed',dash=None):
    d='M'+'L'.join(f'{a} {b}' for a,b in pts)
    cls='net '+('power-net' if layer=='power' else '')
    add(f'<path d="{d}" fill="none" stroke="#f0f3f4" stroke-width="5.3" class="{cls}" data-net="{key}"/>')
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" class="{cls}" data-net="{key}"'+(f' stroke-dasharray="{dash}"' if dash else '')+f'><title>{esc(label)}</title></path>')
    add(f'<path d="{d}" class="net-hit '+('power-net' if layer=='power' else '')+f'" data-net="{key}"><title>{esc(label)}</title></path>')
    nets.append({'id':key,'label':label,'layer':layer,'basis':certainty,'points':pts})

# Routed signal wiring with intentionally spaced harness lanes.
for p,i in [(12,0),(10,1),(9,2),(18,3)]:
    sx,sy=pp(p);tx=273+i*19
    if p!=18:pts=[(sx,sy),(sx,486+i*6),(tx,486+i*6),(tx,445)]
    else:pts=[(sx,sy),(sx,736),(676,736),(676,485),(tx,485),(tx,445)]
    net('out'+str(p),f'{"A4" if p==18 else "D"+str(p)} → 릴레이 기능 채널',pts,'#597ac5')

inputpaths={
 'frame':[(276,332),(292,332),(292,483),(pp(8)[0],483),pp(8)],
 'light':[(276,422),(287,422),(287,734),(pp('A0')[0],734),pp('A0')],
 'key':[(276,512),(282,512),(282,740),(pp('A1')[0],740),pp('A1')],
 'rfid':[(276,602),(277,602),(277,746),(pp('A5')[0],746),pp('A5')],
 'book':[(276,692),(302,692),(302,491),(pp(6)[0],491),pp(6)],
}
for k,pts in inputpaths.items():net(k,k+' sensor → Arduino',pts)
for j,(p,tx) in enumerate([(4,790),(5,801),(16,812)]):
    sx,sy=pp(p)
    pts=[(sx,sy),(sx,480+j*6),(691+j*5,480+j*6),(691+j*5,705+j*6),(tx,705+j*6),(tx,680)] if p!=16 else [(sx,sy),(sx,728),(tx,728),(tx,680)]
    net('motor'+str(p),f'{"A2" if p==16 else "D"+str(p)} → L298N',pts,'#8f72b8')
for j,p in enumerate([2,3]):
    sx,sy=pp(p);tx=733 if p==2 else 753
    net('uart'+str(p),f'D{p} ↔ KT403A UART',[(sx,sy),(sx,474-j*7),(909+j*6,474-j*7),(909+j*6,233+j*8),(tx,233+j*8),(tx,209)],'#b99445')
net('audio','KT403A LINE OUT → HONGXING MP3 IN',[(833,166),(864,166),(864,94),(568,94),(568,210),(367,210)],'#9a80ae')
for i,(key,_,_,pin,y) in enumerate(loads):
    relayindex={12:0,10:1,9:2,18:3}[pin]
    sx=258+16+relayindex*64+22
    net('load'+str(pin),f'릴레이 기능 접점 → {key}',[(sx,303),(sx,282-i*8),(949+i*6,282-i*8),(949+i*6,y+8),(977,y+8)],'#ab7558',layer='load',certainty='functional-only / terminal arrangement proposed',dash='6 4')
net('actuator','L298N → 리니어 액추에이터',[(871,586),(926,586),(926,747),(980,747)],'#a86c5a',layer='load',certainty='functional-confirmed')

for key,pts in [
 ('power5',[(279,800),(279,778),(518,778),pp('5V')]),
 ('powergnd',[(414,800),(414,785),(pp('GND')[0],785),pp('GND')]),
 ('power12',[(597,800),(597,785),(729,785),(729,682)]),
 ('poweramp',[(627,800),(627,835),(923,835),(923,103),(551,103),(551,210)]),
]:net(key,'전원 분기 배치안',pts,'#c26c66' if key!='powergnd' else '#7b8a94',layer='power',certainty='proposed / preserve actual supply specification',dash='5 4')

text(26,296,'현장 입력 5개',14,'#526c79');text(983,296,'기능별 출력',14,'#526c79')
text(254,898,'실선: 확정 기능·코드 핀    점선: 부하 접점의 기능 연결 / 채널 배치는 정리안',12,'#5d737e')
text(254,921,'릴레이 표시등은 Arduino GPIO 레벨을 표시합니다. 실제 코일 극성·접점 동작과 구별합니다.',11,'#6f818b')
add('</svg>')
(ROOT/'hardware/cabinet-layout.svg').write_text('\n'.join(out),encoding='utf-8')
(ROOT/'hardware/nets.json').write_text(json.dumps(nets,ensure_ascii=False,indent=2),encoding='utf-8')
print('Cabinet drawing:',len(nets),'nets')
