"""Dimensioned two-bay mounting plan. Coordinates are usable-backplate mm.
Photo estimates are explicitly not measured dimensions. No image generation.
"""
from pathlib import Path
from html import escape
import json, csv, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
NS={'s':'http://www.w3.org/2000/svg'}
ET.register_namespace('','http://www.w3.org/2000/svg')
old=ET.parse(ROOT/'hardware/cabinet-layout.svg').getroot()
devices={g.attrib['data-part']:g for g in old.findall('s:g',NS) if 'data-part' in g.attrib}

parts=[
 # part, bay, x/y, occupied reserve w/h, body footprint w/h/d, status
 ('smps','upper',70,10,240,145,215,115,30,'MEAN WELL LRS-200-12 후보; 12V17A/실부하 대조'),
 ('ac','upper',10,10,45,110,36,80,70,'기존 차단기 정격·회로 추적 후'),
 ('power-ground','upper',10,180,80,65,58.1,28.6,32.4,'단자/굽힘 여유 포함'),
 ('mag-power','upper',105,170,165,80,140,60,75.6,'PTFIX RD + UT6-HESI 7개; 분기 최대10A'),
 ('main-fuse','upper',285,170,80,75,35,35,25,'Littelfuse FHAC0002ZXJ; 몸체값은 확보 가정, 리드 경로 실측'),
 ('pe','upper',325,15,40,100,30,80,45,'PE 전용 바; 0V와 별도'),
 ('rfidbox','lower',40,10,280,220,260,180,90,'실측 전 확보 공간; 실제 크기 단정 아님'),
 ('field-terminals','lower',320,20,75,210,48.6,177.2,36.8,'PT2.5 24개 + 커버2 + 엔드브래킷4; 두 그룹'),
 ('relayA','lower',40,270,90,80,80,60,30,'채널 기능표는 조건부 재배치'),
 ('relayB','lower',140,270,90,80,80,60,30,'기존 채널 전부 추적·보존'),
 ('uno','lower',245,270,90,80,68.6,53.4,25,'핀/USB 삽입 여유 포함'),
 ('l298','lower',40,390,90,85,60,60,55,'방열판·나사단자 여유 포함'),
 ('buck','lower',145,390,90,85,80,70,75.6,'Pololu4091 + 5V PTFIX RD + F5L/CLIPFIX 캐리어'),
 ('gnd','lower',245,390,90,85,58.1,28.6,32.4,'0V-L 공통 분배블록'),
 ('amp','lower',40,510,190,110,180,90,50,'사진 기반 확보 공간; 실측 필요'),
 ('mp3','lower',245,510,90,65,65,45,25,'SD/잭 탈착 여유 포함'),
 ('frontpanel','lower',245,590,90,40,75,25,25,'J7 및 도어 하네스 접속부'),
]
names={'smps':'12V 메인 SMPS','ac':'차단기/AC 보호','power-ground':'0V-PWR 분배블록','mag-power':'12V 버스/분기 퓨즈','main-fuse':'FU0 주 DC 보호','pe':'PE 보호접지 바','rfidbox':'RFID 회색함 전체','field-terminals':'X1/X3/X4 현장 단자','relayA':'4CH 릴레이 A','relayB':'4CH 릴레이 B','uno':'Arduino','l298':'L298N E6','buck':'5V 변환·분배 캐리어','gnd':'0V-L 분배블록','amp':'HONGXING 앰프','mp3':'KT403A','frontpanel':'J7 도어 접속부'}
model={'revision':'v4-two-bay','units':'mm','basis':'사진 비율 추정 + 보수적 확보 치수. 실측 전 적합 확정 불가.',
 'photoEstimate':{'outerWidth':[450,550],'lowerOpeningHeight':[600,750],'upperOpeningHeight':[250,350],'depth':'사진만으로 추정 불가'},
 'planning':{'usableWidth':400,'upperHeight':260,'lowerHeight':650,'usableDepth':120},
 'photoAnchor':'상부 SMPS의 길쭉한 외형 비율을 200~220 × 100~115mm급으로 가정한 넓은 추정 범위. 사진 속 모델 식별 아님.',
 'parts':[dict(zip(['id','bay','x','y','reserveW','reserveH','bodyW','bodyH','bodyD','basis'],p),name=names[p[0]]) for p in parts],
 'ducts':{'lowerVertical':[[10,10,20,625],[375,240,20,395]],'lowerHorizontal':[[35,240,335,20],[35,365,335,20],[35,485,335,20]],'upperVertical':[[375,10,20,235]],'actualProduct':'Panduit G.5X1LG6 + C.5LG6; 外形17.5×26.9mm'},
 'doorPanel':{'x':40,'y':270,'width':180,'height':100,'rearReserve':45,'oppositeBackplateDepth':40,'requiredGap':15,'depthNeed':100,'button':'OMRON A16-TAM-1','locationRule':'RFID前・L298N放熱板前を避け、リレーA/B前のドアに置く'.replace('RFID前・L298N放熱板前を避け、リレーA/B前のドアに置く','RFID/L298N 앞을 피하고 릴레이 A/B 앞 도어에 배치')},
 'passage':{'basis':'사용자가 확인한 기존 상하 관통구. 위치·크기는 실측 전 기호로만 표시.', 'newHoleRequired':False,'mainsCrossing':False,'bundles':['P1: F1~F3 + 각 자석 음극 / 6선','P2: 모터·앰프 +/− / 4선','L1: F6 +12V 및 0V-PWR.7→0V-L.IN / 2선','조건부: RFID 정격 전원 +/− / 2선'], 'minimumConductors':12,'conditionalConductors':2},
 'fitConditions':['상·하 유효 폭 각각 400 이상','상부 유효 높이 260 이상','하부 유효 높이 650 이상','도어 안쪽에서 측정한 사용 가능 깊이 120 이상','RFID 몸체 260×180×90 이하 + 커넥터 방향 여유','앰프/릴레이/드라이버의 실제 몸체가 각 확보 구역 안에 들어옴','관통구에서 실제 외경·굽힘·보호 부싱·잔여 케이블을 포함해 통과 가능','SMPS·DC-DC 제조사 방열 간격/방향 충족'],
 'mounting':'좌표는 각 구역 유효 백플레이트 좌상단 기준. 외함 테두리/문턱 포함 치수 아님. 몸체 나사홀은 실물 전사; 이 파일로 바로 타공하지 않음.'}
(ROOT/'hardware/cabinet-fit-model.json').write_text(json.dumps(model,ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'hardware/mounting-schedule.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['부품','구역','X mm','Y mm','확보 폭 mm','확보 높이 mm','몸체 검토 폭','몸체 검토 높이','몸체 검토 깊이','치수 근거']);w.writerows([[names[p[0]]]+list(p[1:]) for p in parts])

o=[]
def a(s):o.append(s)
def r(x,y,w,h,c,rad=4,stroke=None,extra=''):a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rad}" fill="{c}"'+(f' stroke="{stroke}"' if stroke else '')+f' {extra}/>')
def t(x,y,s,size=23,c='#385866',anchor='start',weight=500):a(f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>')
def line(pts,c='#7d929b',w=3,key=None,dash=None):
 a('<path d="M'+'L'.join(f'{x} {y}' for x,y in pts)+f'" stroke="{c}" stroke-width="{w}" fill="none" stroke-linejoin="round" stroke-linecap="round"'+(f' class="net" data-net="{key}"' if key else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def circle(x,y,rad,c,extra=''):a(f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{c}" {extra}/>')
def begin(part):a(f'<g class="device" data-part="{part}" role="button" tabindex="0" aria-label="{escape(names.get(part,part))}">')
def end():a('</g>')
def screw(x,y):circle(x,y,6,'#a9b7bd');line([(x-3,y+3),(x+3,y-3)],'#718690',1.7)

a('<svg xmlns="http://www.w3.org/2000/svg" id="redesign-svg" width="1420" height="2200" viewBox="0 0 1420 2200" role="img" aria-label="상하 2구역 배전함 실장 계획: 상부 전원, 하부 RFID와 제어장치, 기존 관통구 및 mm 좌표">')
a(ET.tostring(old.find('s:defs',NS),encoding='unicode'))
a('<style>text{font-family:"Malgun Gothic",Arial,sans-serif}.device{cursor:pointer;outline:none}.device:focus,.selected-device{filter:drop-shadow(0 0 5px #20a297)}.net{stroke-linecap:round}.selected-net{stroke-width:7!important;opacity:1!important}.dim-net{opacity:.23!important}.power-net{display:none}.show-power .power-net{display:initial}</style>')
r(0,0,1420,2200,'#f7fafb',0)
t(90,55,'MONG SHOT / TWO-BAY INSTALLATION PLAN',25,'#477280',weight=650)
t(90,93,'기존 상하 함체 활용 · 배치 좌표 mm · 사진 추정치를 실측치로 표시하지 않음',21,'#8b9ea7')

# Each bay has a local usable backplate with origin at x150 / y170 or y810.
S=2;X=150;Y={'upper':170,'lower':810}
def xy(b,x,y):return X+x*S,Y[b]+y*S
def localrect(b,x,y,w,h,*args,**kw):xx,yy=xy(b,x,y);r(xx,yy,w*S,h*S,*args,**kw)
for bay,h,title in [('upper',260,'상부 / 전원·보호·12V 분배'),('lower',650,'하부 / RFID·제어·오디오')]:
 yy=Y[bay];r(X-32,yy-34,864,h*S+68,'#aebdc5',12,'#91a6b0');r(X-20,yy-22,840,h*S+44,'#f2f6f8',7,'#c5d2d8');r(X,yy,800,h*S,'url(#backplate)',2,'#c1cfd6')
 for sx in [X-10,X+810]:
  for sy in [yy-10,yy+h*S+10]:screw(sx,sy)
 if bay=='upper':t(X+8,yy-47,title,26,'#426c7b',weight=650)
 else:t(1018,855,title,24,'#426c7b',weight=650)
 # width / height dimension lines
 if bay=='upper':
  line([(X,yy-80),(X+800,yy-80)],'#9ab0ba',2)
  for xx in [X,X+800]:line([(xx,yy-88),(xx,yy-70)],'#9ab0ba',2)
  t(X+400,yy-90,'유효 폭 400 mm (상·하 공통 검토값)',20,'#7c98a5','middle')
 line([(X-65,yy),(X-65,yy+h*S)],'#9ab0ba',2)
 t(X-70,yy+h*S/2,str(h),20,'#7c98a5','end')
 for n in range(0,401,50):
  xx,yy2=xy(bay,n,0);line([(xx,yy2),(xx,yy2+8)],'#91a8b3',1);t(xx,yy2-5,str(n),14,'#9aabb3','middle')

# Duct channels and removable support rail. No AC crosses between bays.
for x,y,w,h in model['ducts']['lowerVertical']+model['ducts']['lowerHorizontal']:localrect('lower',x,y,w,h,'url(#duct-slots)',2,'#bfccd3')
localrect('upper',375,10,15,235,'url(#duct-slots)',2,'#bfccd3')
for y in [329,449,558]:localrect('lower',35,y,310,16,'url(#metal)',2,'#c1cdd3')

# Accurate reserved rectangles behind individual module illustrations.
for p in model['parts']:
 xx,yy=xy(p['bay'],p['x'],p['y']);r(xx,yy,p['reserveW']*2,p['reserveH']*2,'#ffffff',6,'#c1d1d8',extra='fill-opacity=".48" stroke-dasharray="7 5"')
 t(xx+8,yy-7,p['id'].upper()+f"  ({p['x']}, {p['y']})",15,'#849ca8')

def source_device(part,bay,x,y,w,h,bounds):
 bx,by,bw,bh=bounds;xx,yy=xy(bay,x,y);scale=min(w*S/bw,h*S/bh)
 a(f'<g transform="translate({xx-bx*scale} {yy-by*scale}) scale({scale})">'+ET.tostring(devices[part],encoding='unicode')+'</g>')
source_device('uno','lower',250,283,80,64,(332,501,307,226))
source_device('relayA','lower',43,283,84,54,(258,303,276,150))
source_device('relayB','lower',143,283,84,54,(609,303,276,150))
source_device('l298','lower',49,401,72,65,(709,520,175,215))
source_device('amp','lower',45,525,180,90,(262,105,287,140))
source_device('mp3','lower',250,522,80,48,(669,105,174,140))
for part,x in [('relayA',85),('relayB',185),('uno',290)]:
 xx,yy=xy('lower',x,347);t(xx,yy,names[part],19,'#527785','middle')
xx,yy=xy('lower',85,469);t(xx,yy,'L298N E6',19,'#527785','middle')

# Upper SMPS / AC guarded area.
begin('smps');localrect('upper',80,20,215,115,'#b7c4cb',5,'#8fa3af');localrect('upper',83,23,209,96,'#d6dfe4',3)
for row in range(8):
 for col in range(18):
  xx,yy=xy('upper',88+col*7.5,29+row*10);circle(xx,yy,4.3,'#a6b7c1')
localrect('upper',232,35,55,63,'#eff4f6',3,'#bdcbd3');xx,yy=xy('upper',260,58);t(xx,yy,'12V',30,'#547582','middle');t(xx,yy+32,'LRS-200-12',15,'#7d959f','middle')
for i,label in enumerate(['L','N','PE','V−','V−','V+','V+']):
 xx,yy=xy('upper',115+i*25,124);r(xx,yy,43,24,'#4b626f',2);screw(xx+21,yy+12);t(xx+21,yy+49,label,17,'#7a929f','middle')
localrect('upper',112,120,75,35,'#dbc58e',3,extra='fill-opacity=".7"');end()
begin('ac');localrect('upper',16,22,32,80,'#e9e5d7',3,'#9ba9a9');localrect('upper',30,42,10,27,'#3b4c53',2);xx,yy=xy('upper',33,116);t(xx,yy,'AC',20,'#9a815f','middle');end()
begin('pe');localrect('upper',330,25,30,80,'#a9be7c',3,'#8d9d6d');
for i in range(4):xx,yy=xy('upper',345,36+i*20);screw(xx,yy)
xx,yy=xy('upper',345,119);t(xx,yy,'PE',21,'#7e925c','middle');end()

def block(part,bay,x,y,w=58.1,h=28.6):
 begin(part);localrect(bay,x,y,w,h,'#6e9eaf',4,'#4a788e');
 xx,yy=xy(bay,x+6,y+14.3);circle(xx,yy,7,'#34596e')
 for i in range(12):
  xx,yy=xy(bay,x+17+(i%6)*6.5,y+7+(i//6)*14.6);circle(xx,yy,3.5,'#34596e');r(xx-3,yy+5,6,4,'#dba45c',1)
 end()
block('power-ground','upper',13,189);block('gnd','lower',253,413)
xx,yy=xy('upper',50,251);t(xx,yy,'0V-PWR',20,'#94774e','middle')
xx,yy=xy('lower',290,402);t(xx,yy,'0V-L',22,'#398b8e','middle');t(xx,yy+130,'全 포트 공통'.replace('全','모든'),18,'#7497a2','middle')
begin('mag-power');localrect('upper',111,182,29,58,'#c78a82',3,'#ac706a')
for i in range(12):
 xx,yy=xy('upper',117+(i%2)*15,188+(i//2)*9);circle(xx,yy,4,'#6c5360')
for i in range(7):
 xx,yy=xy('upper',159+i*9,181);r(xx,yy,16.4,115.6,'#647781',2,'#51656f');r(xx+3,yy+17,10,74,'#b9c7ce',2);t(xx+8,yy+108,'F'+str(i+1),10,'#e5edf1','middle')
end()
xx,yy=xy('upper',190,251);t(xx,yy,'12V 分기'.replace('分','분'),20,'#977d58','middle')
begin('main-fuse');localrect('upper',304,188,35,35,'#bb9567',5,'#9e7e5a');xx,yy=xy('upper',321,206);t(xx,yy,'FU0',22,'#faf3e6','middle');end()

begin('rfidbox');localrect('lower',50,25,260,180,'#b6c2ca',6,'#879da9');localrect('lower',55,30,250,170,'#d9e1e6',5,'#abbec8')
for x in [60,300]:
 for y in [35,195]:xx,yy=xy('lower',x,y);screw(xx,yy)
xx,yy=xy('lower',180,80);r(xx-130,yy-15,260,90,'#eff4f6',4,'#c2d1da');t(xx,yy+19,'RFID CONTROL',29,'#526f7f','middle');t(xx,yy+53,'회색 제어함 전체 보존',23,'#8096a2','middle')
t(xx,yy+122,'몸체 검토값 260 × 180 × 90',21,'#7895a3','middle');t(xx,yy+156,'실제 외곽·커넥터 돌출 실측 필요',19,'#9c8d73','middle');end()

begin('buck');localrect('lower',150,397,83,70,'#f0f5f6',3,'#b4c9d3');localrect('lower',185,400,25.4,25.4,'#3e8a7c',2,'#2d6d63');xx,yy=xy('lower',198,413);r(xx-12,yy-12,24,24,'#b4a26d',3);t(xx,yy+41,'4091',12,'#638b7d','middle');localrect('lower',152,405,28.6,58.1,'#c78a82',3);localrect('lower',218,408,8.2,57.8,'#677b86',2)
for i in range(12):xx,yy=xy('lower',157+(i%2)*15,412+(i//2)*9);circle(xx,yy,4,'#6c5360')
xx,yy=xy('lower',185,475);t(xx,yy,'5V 변환·분배',18,'#558878','middle');end()
begin('frontpanel');localrect('lower',251,597,78,22,'#5f8b9f',3);
for i,lab in enumerate(['5','0','D','C','L','B']):xx,yy=xy('lower',257+i*12,607);circle(xx,yy,4,'#d4b676');t(xx,yy+28,lab,12,'#839ba8','middle')
end()

# Two actual PT2.5 groups, each 12 terminals, with end covers and brackets.
begin('field-terminals')
for group in range(2):
 base=36+group*89
 localrect('lower',341,base-8,35,83,'url(#metal)',2,'#b6c7d0')
 for j in range(12):
  xx,yy=xy('lower',333,base+j*5.2);r(xx,yy,97.2,10.4,'#a5bec9',1,'#839eab');circle(xx+12,yy+5,3,'#496573');circle(xx+85,yy+5,3,'#496573')
xx,yy=xy('lower',357,30);t(xx,yy,'PT 2,5 ×24',15,'#64818f','middle');xx,yy=xy('lower',357,215);t(xx,yy,'신호 / 부하 분리',14,'#7c96a3','middle');end()

# The passage location is a symbol until actual edge position is measured.
r(250,720,600,56,'#526d7e',22,'#2f4e62');r(264,729,572,36,'#203b4b',15)
t(550,798,'기존 상하 관통구 / 위치·크기 실측 후 클립 경로 확정',19,'#8d9fa9','middle')
# Each return and positive branch gets its own conductor; bundle lines are schematic lanes.
for i,(key,c,x) in enumerate([('buck-reference','#398f8b',285),('power-ground','#987b59',575),('mag-power','#bc8063',725)]):
 line([(x,665),(x,747),(x,828)],c,8,key)
circle(285,747,10,'#83b6ac');circle(575,747,10,'#ba9a72');circle(725,747,10,'#d3aa90')
t(285,706,'L1 ×2',18,'#559d94','middle');t(575,706,'P2 ×4',18,'#a18b6e','middle');t(725,706,'P1 ×6',18,'#b38c76','middle')

# Routing inside ducts: representative paths, exact conductors listed in schedules.
line([(285,828),(182,828),(182,1595),(636,1595),(636,1665),(668,1665)],'#398f8b',5,'gnd')
line([(742,1679),(742,1725),(562,1725),(562,1656)],'#398f8b',4,'buck-reference')
line([(725,825),(168,825),(168,1308),(936,1308),(936,1350),(408,1350)],'#bd8064',5,'mag-power')
line([(575,820),(174,820),(174,1318),(925,1318),(925,1765),(593,1765),(593,1860)],'#987b59',5,'power-ground')
line([(754,1685),(855,1685),(855,1546),(685,1546),(685,1494)],'#398f8b',5,'gnd')
line([(755,1685),(841,1685),(841,1377),(350,1377),(350,1490)],'#398f8b',5,'gnd')
line([(755,1685),(829,1685),(829,1965),(710,1965)],'#398f8b',5,'gnd')
line([(815,1428),(815,1340),(345,1340),(345,1490)],'#6585bf',4,'out12')

# Door assembly outside cabinet, represented without occupying backplate area.
r(1030,900,326,400,'#d7e1e6',12,'#aebfc9');r(1042,912,302,376,'#f4f7f9',8)
t(1193,948,'함체 외부 표시·진행',25,'#567c8e','middle')
for i,lab in enumerate(['액자','조명','열쇠','RFID','책','완료']):
 yy=986+i*38;circle(1075,yy,12,'#8a9ca6',extra=f'id="panel-led-{i}"');t(1108,yy+8,lab,22,'#7492a1')
circle(1247,1217,31,'#536e7d',extra='data-action="manual-next"');circle(1247,1217,21,'#b2c4ce',extra='data-action="manual-next"');t(1193,1270,'진행 · 2초 누름',21,'#7d96a3','middle')

def card(y,title,lines):
 r(1018,y,370,85+len(lines)*38,'#fff',9,'#d7e2e7');t(1038,y+39,title,24,'#4e7685',weight=650)
 for i,txt in enumerate(lines):t(1038,y+78+i*38,txt,20,'#8199a5')
card(150,'01  상부는 전원 구역',['AC는 이 구역에서만 배선','12V SMPS → 개별 퓨즈','0V-PWR: 부하별 독립 귀환','PE는 금속 외함 보호용'])
card(480,'02  관통구를 활용',['상하 연결은 DC만 통과','최소 12선 + RFID 조건부 2선','부싱·양쪽 고정 클립 설치','기존 케이블 여유도 함께 확인'])
card(1340,'03  하부는 제어 구역',['RFID 옆 PT2.5 현장 단자24개','릴레이 A/B 두 장 보존','5V 변환·분배부를 함께 고정','신호/부하는 단자군을 구분'])
card(1660,'04  GND의 실제 경로',['부하 − → 상부 0V-PWR','PWR.7 → 0V-LINK → L.IN','모든 신호 기준은 0V-L','비절연형이므로 두 0V는 공통'])
card(1980,'05  설치 전 확인',['점선 사각형 = 배선 포함 확보 영역','나사홀은 실물 전사 후 타공','깊이·방열·도어 간섭 실측'])
t(150,2160,'좌표 기준: 각 유효 백플레이트 좌상단 (0, 0) / 단위 mm / 원근 사진으로 실측을 대체하지 않음',20,'#8da1ac')
a('</svg>')
svg='\n'.join(o)
for ident in ['metal','backplate','ampbody','boardshadow','duct-slots','led-body','ledFilter','pin-female','pin-male','mcu-leads']:
 svg=svg.replace('id="'+ident+'"','id="tb-'+ident+'"').replace('url(#'+ident+')','url(#tb-'+ident+')').replace('href="#'+ident+'"','href="#tb-'+ident+'"')
(ROOT/'hardware/cabinet-redesign.svg').write_text(svg,encoding='utf-8')
print('Two-bay mounting plan + dimensional model ready')
