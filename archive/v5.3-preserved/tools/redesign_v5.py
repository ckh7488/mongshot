"""Current compact cabinet with existing direct GPIO and explicit common ground.

All mounting sizes are reserve envelopes, not surveyed dimensions or hole patterns.
This is the single current generator; historical v4 generators are not build inputs.
"""
from pathlib import Path
import csv, json, html, re, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
H=ROOT/'hardware'; S=ROOT/'simulation/source'
REV='v5.3-direct-control'
def write(path,text):
    path=ROOT/path;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
def js(path,obj):write(path,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def csvout(name,heads,rows):
    with (H/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(heads);w.writerows(rows)
def table(heads,rows):
    esc=lambda v:html.escape(str(v))
    return '<div class="table-scroll"><table><thead><tr>'+''.join('<th>'+esc(x)+'</th>' for x in heads)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'

# Save a clearly historical source snapshot once. Do not overwrite field records.
backup=ROOT/'archive/v4-sources';backup.mkdir(parents=True,exist_ok=True)
for rel in ['simulation/source/app.js','simulation/source/page.html','simulation/source/fit.js','tests/check-design.py',
            'tools/draw_two_bay.py','tools/draw_ground_single.py','tools/build_fit_view.py','tools/build_product_bom.py',
            'tools/build_installation_records.py','tools/build_workbench.py','tools/build_mounting_templates_fitz.py']:
    dst=backup/rel.replace('/','__')
    if not dst.exists():shutil.copy2(ROOT/rel,dst)
write('archive/v4-sources/README.md','# Historical v4 sources\n\nNot current build inputs. The common 0V-LINK, 24 DIN field terminals, fuses and large equipment envelopes were superseded by v5. Do not run these sources as installation instructions.\n')

parts=[]
def part(id,bay,x,y,w,h,bw,bh,bd,name,basis,domain):
    parts.append(dict(id=id,bay=bay,x=x,y=y,reserveW=w,reserveH=h,bodyW=bw,bodyH=bh,bodyD=bd,name=name,basis=basis,domain=domain))
part('ac','upper',10,10,45,110,36,80,70,'기존 차단기','기존 회로 보존; 정격/실물 대조','PE')
part('smps','upper',70,10,240,145,215,115,30,'12V 메인 SMPS','LRS-200-12 후보; 17A 필요 확정 아님. 부하/가는 선에 맞춰 용량 재선정','P0')
part('pe','upper',325,15,55,100,30,80,35,'기존 PE 접지부','금속 함체/도어/SMPS FG; DC 귀환에 사용하지 않음','PE')
part('power-ground','upper',15,175,75,65,58.1,28.6,32.4,'부하 12V − (P0)','SMPS V− 1가닥을 여러 부하 귀환으로 분배. 내부13접속점 공통. 변환/절연 기능 없음','P0')
part('mag-power','upper',105,175,75,65,58.1,28.6,32.4,'부하 12V + (P12)','SMPS V+를 여러 회로로 분기. 전압변환기가 아닌 수동 분배블록','P0')
part('amp-adapter','upper',200,175,110,65,90,45,35,'홍싱 기존 어댑터','기존 DC 어댑터 재사용; 90×45×35는 배치 가정','G0')
part('rfidbox','lower',25,10,170,130,160,100,65,'RFID 제어함','소형화한 배치 가정 160×100×65; 확정 실측 아님','P0')
part('amp','lower',215,10,170,110,140,90,45,'HONGXING','몸체140×90×45 배치가정. MP3를 바로 아래로 이동. 기존 라인출력/GND 직결','G0')
part('mp3','lower',235,125,70,40,45,30,20,'KT403A MP3','홍싱 바로 아래. UART/라인 출력은G0, SPK±는 앰프 입력으로 쓰지 않음','G0')
part('relayA','lower',25,200,90,75,80,60,30,'4CH 릴레이 A','기존 보드; 3자석+창문을 조건부 재배치','P0')
part('relayB','lower',125,200,90,75,80,60,30,'4CH 릴레이 B','8채널 추적 전 철거/예비 단정 금지','P0')
part('magdiodes','lower',115,200,10,65,6,50,6,'자석 다이오드 ×3 · 릴레이 옆','별도 PCB 없음. 3개와 절연 리드 고정공간6×50mm는 배치값. 자석선 +/−에 병렬, 접점 COM/NO 사이 아님','P0')
part('l298','lower',25,315,90,75,60,60,55,'L298N E6','기존 제어선 D4/D5/A2 직결. Vs=P12/Vss=5D, GND는 G0와 공통. 모듈 점퍼/리셋상태 대조','P0')
part('buck','lower',25,430,60,65,25.4,25.4,9.5,'부하측 5V 변환기 (5D)','P12/P0에서5D/P0를 만듦. 릴레이 코일/L298 제어전원용. 12V→5V 강압, 입력/출력−는 P0 공통. 실물 기판25.4×25.4mm','P0')
part('isolated5','lower',100,405,45,150,17.5,90,54.5,'로직용 5V 변환기 · 현재 GND 공통','DDR-15G-5 전원분기 후보 유지. G0↔P0가 공통이므로 전체 시스템 절연용으로 보지 않음. 몸체 위40/아래20/좌우5mm 이상 비움. 낮은 입력전압에서는2.7A 제한','BOUNDARY')
part('gnd','lower',160,430,75,40,58.1,28.6,32.4,'로직 5V − (G0)','DDR OUT−를 Uno/MP3/센서기준/패널로 분배. P0 블록과 동일 제품/동일 크기','G0')
part('logic-positive','lower',160,480,75,40,58.1,28.6,32.4,'로직 5V + (5L)','DDR OUT+를 로직 장치로 분배. G0와 한 쌍이며 5D와 연결하지 않음','G0')
part('uno','lower',265,430,95,80,68.6,53.4,25,'Arduino Uno','USB/핀 삽입 여유 포함; 로직 G0','G0')
for p in parts:
    if p['id']=='isolated5':p.update(bodyOffsetY=40,airClearance=dict(top=40,bottom=20,left=5,right=5))
    p['bodyX']=p['x']+(p['reserveW']-p['bodyW'])/2
    p['bodyY']=p['y']+p.get('bodyOffsetY',4)
model=dict(revision=REV,units='mm',basis='사진 기반 계획. 작은 외형도 실측값으로 주장하지 않음.',
    planning=dict(usableWidth=400,upperHeight=260,lowerHeight=560,usableDepth=120),
    photoEstimate=dict(outerWidth=[450,550],upperOpeningHeight=[250,350],lowerOpeningHeight=[600,750],depth='사진으로 추정하지 않음'),
    parts=parts,ducts=dict(lowerVertical=[[0,0,20,550]],lowerHorizontal=[[25,170,360,20],[25,280,360,20],[25,395,60,20],[155,395,230,20]],upperVertical=[[380,10,20,230]],actualProduct='Panduit G.5X1LG6/C.5LG6; 외폭17.5 높이26.9. 하단 가로덕트는 DDR 상부 통풍기둥을 피해 분할'),
    doorPanel=dict(x=25,y=200,width=180,height=75,rearReserve=45,oppositeBackplateDepth=45,requiredGap=15,depthNeed=105,button='OMRON A16-TAM-1'),
    passage=dict(newHoleRequired=False,mainsCrossing=False,bundles=['P: P12/P0 두 쌍 (DDR/5D용 각각 독립)','M: 자석 음극3 + 릴레이 접점 급전1 (1쌍씩 권장)','S: RFID/12V센서 급전 쌍; 실제 필요한 수만','A: 홍싱 기존 어댑터 +/− 한 쌍'],minimumConductors=10,conditionalConductors='센서 전원/공유선의 실제 수에 따라 추가'),
    fitConditions=['유효 폭400/상부260/하부560/깊이120mm 이상','RFID160×100×65 및 앰프140×90×45는 임시 몸체값; 커넥터 포함 실측 대조','SMPS/DDR 제조사 방열 방향과 주변 열원 간격 별도 충족','관통구 위치/직경/기존 선 외경/굽힘을 실측','DIN 레일과 부품 고정부 설치높이 포함; 타공은 실물 홀 전사'],
    mounting='각 유효 백플레이트 좌상단 원점. 예약 외곽은 케이블 여유를 포함. 몸체 치수와 나사홀은 별도 실측.')
js('hardware/cabinet-fit-model.json',model)
csvout('mounting-schedule.csv',['ID','부품','구역','확보X mm','확보Y mm','확보 폭 mm','확보 높이 mm','몸체X mm','몸체Y mm','몸체 폭','몸체 높이','몸체 깊이','치수 근거'],[[p[k] for k in ['id','name','bay','x','y','reserveW','reserveH','bodyX','bodyY','bodyW','bodyH','bodyD','basis']] for p in parts])

sources={
 'DDR-MANUAL':'https://www.meanwell.com/Upload/PDF/DDR%20DIN%20rail%20power%20supply.pdf',
 'HDR-ALT':'https://www.meanwell.com/Upload/PDF/HDR-30/HDR-30-SPEC.PDF',
 'DDR':'https://www.meanwell.com/Upload/PDF/DDR-15/DDR-15-spec.pdf',
 'PS1':'https://www.meanwell.com/Upload/PDF/LRS-200/LRS-200-SPEC.PDF',
 'ISO-M':'https://www.pololu.com/product/5741','ISO-R':'https://www.pololu.com/product/5740',
 'BUCK':'https://www.pololu.com/product/4091',
 'DIODE':'https://www.vishay.com/docs/88516/1n5400.pdf',
  'BU':'https://www.phoenixcontact.com/en-nl/products/distribution-block-ptfix-6-12x25-ns35-bu-3273090',
 'RD':'https://www.phoenixcontact.com/en-fr/products/distribution-block-ptfix-6-12x25-ns35-rd-3273092',
 'XT':'https://www.phoenixcontact.com/ko-kr/products/mpt-05-2-254-1725656',
 'CABLE':'https://www.belden.com/products/cable/ethernet-cable/category-5e-cable/1583a',
 'SUPPRESSION':'https://www.ia.omron.com/product/cautions/36/safety_precautions.html',
 'POSITION':'https://industry.panasonic.com/ap/en/products/control/relay/cautions_use',
 'BUCK-SIZE':'https://www.pololu.com/product/4091/specs'}
js('hardware/source-register.json',dict(checkedOn='2026-11-04',sources=sources))

# Reuse verified front-panel parts, remove superseded distribution/fuse system.
oldbom=json.loads((H/'product-bom.json').read_text(encoding='utf-8'))
if not (backup/'product-bom.json').exists():shutil.copy2(H/'product-bom.json',backup/'product-bom.json')
oldbom=json.loads((backup/'product-bom.json').read_text(encoding='utf-8'))
keep={'U1','LED1~6','SW1','RLED','RPULL','RSER','C1/C2','PCB','J7-F','J7-M','J7-FC','J7-MC','DUCT','DUCT-C'}
items=[x for x in oldbom['items'] if x['id'] in keep]
for x in items:
    if x['id']=='SW1':x['location']='하부 도어 (25,200) / 180×75mm'
def bom(id,name,maker,part,qty,location,size,condition,key=None,status='제품 확인 / 적용 조건 확인'):
    url=sources.get(key or id,'')
    if maker=='YAGEO':url='https://yageogroup.com/content/Resource%20Library/Datasheet/YAGEO-MFR_DATASHEET.pdf'
    if maker=='KEMET':url='https://search.kemet.com/component-documentation/download/specsheet/C315C104K5R5TA'
    items.append(dict(id=id,name=name,maker=maker,part=part,qty=qty,location=location,size=size,condition=condition,url=url,status=status))
bom('PS1','12V 메인 SMPS','MEAN WELL','LRS-200-12',1,'상부','215×115×30mm','기존 후보 보존. 17A가 필요하다는 확정 아님; 얇은 현장선 허용 전류를 의미하지 않음','PS1','용량 재검토 / 신규 구매 보류')
bom('DC-L','절연 로직5V','MEAN WELL','DDR-15G-5',1,'하부 확보(100,405), 몸체(113.75,445)','17.5×90×54.5mm','입력P12/P0, 출력5L/G0. 5V3A(입력12~36V), 9~12V에서는2.7A. 위40/아래20/좌우5mm 확보. 내부 입력/출력 간선은0.8mm² 이상 동선으로 분배블록까지 연결. 로직예산1.2A는 실측 아님. GPIO직결 공통GND 안에서는 절연형이 필수 아님; 이번 변경은 전원부 선택을 자동 변경하지 않음','DDR')
bom('DC-D','부하측5V','Pololu','D36V50F5 / #4091',1,'하부 (25,430)','25.4×25.4×9.5mm','5D/P0: 릴레이코일 및 L298 Vss. 5L과5D의 양극끼리 연결 금지. GND는 제어 기준선으로 공통','BUCK')
bom('D-M1~3','자석 역기전력 억제','Vishay','1N5408-E3/54',3,'릴레이 A 근처 자석선 +/− 사이','DO-201AD','3A/1000V 소자 후보. 줄(K)=자석+, A=자석−. 코일전류/열/반복률/해제시간 확인. 3A는 케이블 허용 전류가 아님','DIODE','코일/해제시간 대조 전 적용 확정 아님')
bom('G-P/G-L','부하/로직 귀환 분배','Phoenix Contact','PTFIX 6/12X2,5-NS35 BU / 3273090',2,'상부P0 / 하부G0','58.1×28.6×32.4mm','두 블록은 귀환 분기용이며 GND-MOTOR-REF로 전기적 공통. 절연 경계 아님. 가는 단선은 주황 버튼을 눌러 삽입','BU')
bom('P12/5L','양극 분배','Phoenix Contact','PTFIX 6/12X2,5-NS35 RD / 3273092',2,'상부12V / 하부로직5V','58.1×28.6×32.4mm','전위가 다른 블록 두 개. 5D는 기존 릴레이/L298 전원선의 분기접속으로 공급','RD')
unselected=[dict(id='FIELD-WIRE',name='기존 이더넷 심선',reason='Cu/CCA,24/26/28AWG, 길이, 코일전류, 사용가능 페어, 접속상태/온도 미측정. 허용전류 확정 불가'),
 dict(id='SENSOR-CHECK',name='기존 센서 신호 확인',reason='새 센서판은 제거. 기존 접점/신호 결선을 보존하고 A0/A1/A5 출력형식과 실제 전압을 기록. 12V 전원 사용만으로 신호도12V라고 판단하지 않음'),
 dict(id='LEGACY',name='기존 보드/어댑터/센서',reason='RFID/홍싱 외곽, 센서 출력형식, 릴레이8채널/active LOW, L298 전원점퍼 실물 대조'),
 dict(id='MECH',name='레일·스탠드오프·부싱·체결재',reason='실물 홀/판두께/나사방향에 맞춰 선정; 범용 큰 단자열을 추가하지 않음')]
bomdata=dict(revision=REV,checkedOn='2026-11-04',items=items,unselected=unselected,removed=['FU0','F1~F7','F5L','PT2.5×24','D-ST2.5×2','필드/퓨즈용 CLIPFIX','0V-LINK','센서PCB/옵토일괄회로','자석접속PCB','MPT1725656×10','NTE1×2/오디오절연PCB/추가감쇠부품','ISO-M/ISO-R/고정캐리어/전용저항14개'],scope='품번 지정안 + 명시적 제작물/미확정 항목; 설치 승인 또는 완성 발주서 아님')
js('hardware/product-bom.json',bomdata)
bheads=['ID','용도','제조사','품번','수량','장소','실제 외형/확보값','적용 조건','제조사 자료','상태']
csvout('product-bom.csv',bheads,[[it[k] for k in ['id','name','maker','part','qty','location','size','condition','url','status']] for it in items])

# Named ground ports: two bus blocks now actually have no DC link.
gports=[('P0','IN','SMPS V−','P0-SOURCE'),('P0','1','자석1−','M1-FIELD−'),('P0','2','자석2−','M2-FIELD−'),('P0','3','자석3−','M3-FIELD−'),('P0','4','L298 GND','P0-MOTOR'),('P0','5','비절연DC-D GND','P0-5D'),('P0','6','절연DC-L INPUT−','P0-DDR'),('P0','7','RFID 전원− (12V일 때)','RFID-0'),('P0','8','12V센서 전원−','SENS-0'),('P0','9~12','미사용 / 지정 기준선 외 중복 연결 확인',''),
  ('G0','IN','절연DC-L OUTPUT−','G0-SOURCE'),('G0','1','Arduino GND','G0-1'),('G0','2','기존 액자 리드 귀환','REED-D8-0'),('G0','3','KT403A GND','G0-3'),('G0','4','L298 GND 공통 기준선','GND-MOTOR-REF'),('G0','5','예비',''),('G0','6','도어 LED/버튼','G0-6'),('G0','7','예비 / 오디오는 기존 케이블 GND로 공통',''),('G0','8','기존 책 리드 귀환','REED-D6-0'),('G0','9~12','미사용 / 지정 기준선 외 중복 연결 확인',''),
 ('5D-return','분기','RY-A GND / RY-B GND','P0에서 DC-D의 단일 귀환으로'),('홍싱','adapter−','기존 어댑터−. MP3 IN GND로 G0와 공통','AMP−'),('PE','기존부','콘센트PE → SMPS FG / 외함 / 도어','DC 귀환 대용 아님')]
csvout('ground-terminal-schedule.csv',['분배부','포트','연결 대상','선 라벨'],gports)
positive=[('P12','IN','SMPS V+'),('P12','1','RY-A CH1 COM'),('P12','2','RY-A CH2 COM'),('P12','3','RY-A CH3 COM'),('P12','4','L298 Vs'),('P12','5','DC-D VIN'),('P12','6','DC-L INPUT+'),('P12','7','RFID 정격+12V 조건부'),('P12','8','기타 정격12V센서'),('5L','IN','DC-L OUTPUT+'),('5L','1','Arduino 5V'),('5L','2','KT403A VCC'),('5L','3','예비 / 기존5V센서가 필요할 때 정격 대조'),('5L','4','예비'),('5L','5','예비'),('5L','6','도어PCB VCC'),('5D','분기','RY-A VCC/JD-VCC, RY-B VCC/JD-VCC, L298 Vss')]
csvout('positive-terminal-schedule.csv',['분배부','포트','연결 대상'],positive)
dc=[('P0','SMPS_NEG'),('P0','MAG1_NEG'),('P0','MAG2_NEG'),('P0','MAG3_NEG'),('P0','L298_GND'),('P0','BUCK_D_NEG'),('P0','DDR_INPUT_NEG'),('P0','RFID_POWER_NEG'),('P0','SENSOR_12V_NEG'),('P0','RELAY_A_GND'),('P0','RELAY_B_GND'),('G0','L298_GND'),
    ('G0','DDR_OUTPUT_NEG'),('G0','ARD_GND'),('G0','SENSOR_CONTACT_RETURN'),('G0','MP3_GND'),('G0','PANEL_GND'),('G0','AMP_NEG'),('G0','AMP_LINE_GND'),('PE','SMPS_FG'),('PE','CABINET'),('PE','DOOR')]
barriers=[dict(name='DC-L',a='DDR_INPUT_NEG',b='DDR_OUTPUT_NEG',type='converter internal isolation; system bypassed by common reference')]
graph=dict(revision=REV,nodes=sorted({x for pair in dc for x in pair}),dc_connections=dc,barriers=barriers,groundPolicy='common-reference',systemGalvanicIsolation=False,referenceBond=dict(label='GND-MOTOR-REF',start='G0.4',end='L298 GND'),unresolvedSignalInterfaces=['A0','A1','A5'],note='기존 제어선 직결을 위해 P0/G0는 공통이다. 자석−도 같은 전위이며 갈바닉 절연이 아니다. 부하 전류는 독립 귀환배선으로 분기한다. DDR 소자 자체의 절연을 시스템 절연으로 표시하지 않는다. 실제 센서/USB/PE 우회 연결과 노이즈는 현장에서 별도 대조.')
js('hardware/ground-connectivity.json',graph)

# Each row is one physical wire, avoiding phantom T1/T2 field terminal rows.
wires=[]
def wire(label,start,end,domain,note=''):
    wires.append([label,start,end,domain,note])
for label,start,end,dom in [('P12-SOURCE','SMPS V+','P12.IN','P0'),('P0-SOURCE','SMPS V−','P0.IN','P0'),('DDR-IN+','P12.6','DC-L IN+','P0'),('P0-DDR','P0.6','DC-L IN−','P0'),('5L-SOURCE','DC-L OUT+','5L.IN','G0'),('G0-SOURCE','DC-L OUT−','G0.IN','G0'),('BUCK-IN+','P12.5','DC-D VIN','P0'),('P0-5D','P0.5','DC-D GND','P0'),('5D-OUT','DC-D VOUT','5D 분기접속 +','P0')]:wire(label,start,end,dom)
for idx,plus,minus in [('1','Arduino 5V','Arduino GND'),('2','KT403A VCC','KT403A GND'),('6','도어PCB VCC','도어PCB GND')]:
    wire('5L-'+idx,'5L.'+idx,plus,'G0');wire('G0-'+('3' if idx=='2' else idx),'G0.'+('3' if idx=='2' else idx),minus,'G0')
for n,plus,minus in [(1,'RY-A VCC/JD-VCC','RY-A GND'),(2,'RY-B VCC/JD-VCC','RY-B GND'),(3,'L298 Vss (5V)','L298 GND')]:
    wire('5D-'+str(n),'5D 분기접속 +',plus,'P0','RY-B는 기존 채널 추적 후에만 연결' if n==2 else '')
    if n!=3:wire('P0-5D-'+str(n),'5D 분기접속 0V',minus,'P0','RY-B는 기존 채널 추적 후에만 연결' if n==2 else '')
wire('P0-5D-RETURN','DC-D GND / P0측','5D 분기접속 0V','P0','부하 전력 귀환을 로직 장치에 직렬로 통과시키지 않음')
relays=[('D12','IN1','몰딩'),('D10','IN2','슬라이드'),('D9','IN3','책'),('A4','IN4','창문')]
for pin,rin,name in relays:wire('OUT-'+pin,'Arduino '+pin,'RY-A '+rin,'공통0V',name+' / 기존 입력회로와 active LOW/리셋 상태 유지. 외부 절연모듈 없음')
for pin,target in [('D4','IN1'),('D5','IN2'),('A2','ENA')]:wire('MOT-'+pin,'Arduino '+pin,'L298 '+target,'공통0V','기존 제어선 직결. ENA 점퍼/리셋상태는 기존 동작에 대조')
wire('GND-MOTOR-REF','G0.4','L298 GND','공통0V','제어 신호기준 공통선. 모터 전력 귀환 P0-MOTOR는 별도 유지. 실제 단자 허용 선 수/굵기에 맞춰 분기하고 다른 굵기 선을 한 구멍에 억지로 끼우지 않음')
for n,pin in [(1,'D12'),(2,'D10'),(3,'D9')]:
    wire('M'+str(n)+'-FEED','P12.'+str(n),'RY-A CH'+str(n)+' COM','P0')
    wire('M'+str(n)+'-FIELD+','RY-A CH'+str(n)+' 선택접점','자석'+str(n)+' +','P0','릴레이 근처 이 선과 음극 귀환 사이에 다이오드K/A 병렬. 다른 굵기 리드와 한 나사에 억지로 몰아넣지 않고 절연 분기/고정')
    wire('M'+str(n)+'-FIELD−','P0.'+str(n),'자석'+str(n)+' −','P0','위 +선과 원래의 꼬임쌍 유지. 릴레이 근처에서 다이오드A를 이 귀환선에 연결')
wire('MOTOR-VS','P12.4','L298 Vs','P0');wire('P0-MOTOR','P0.4','L298 GND','P0','굵은 독립 귀환; G0 연결 금지')
for a,b in [('A','OUT1'),('B','OUT2')]:
    wire('MOTOR-'+a+'-FIELD','L298 '+b,'모터 '+a,'P0','기존 모듈 출력 단자 사용. 둘 다 모터 출력이며 GND에 고정하지 않음')
wire('WIN-C-FIELD','RY-A CH4 COM','창문 기존회로 C','W0','기존 SELV 접점회로 보존. P0/G0 임의 연결 금지')
wire('WIN-SW-FIELD','RY-A CH4 선택접점','창문 기존회로 SW','W0','NO/NC는 기존 동작 추적. Ethernet에 AC220V 인가 금지')
for name,pin,port in [('액자','D8','2'),('책','D6','8')]:
    wire('IN-'+pin,'기존 '+name+' 리드 S','Arduino '+pin,'G0','새 센서판/RC 일괄 추가 없음. D6 기존100Ω 보존')
    wire('REED-'+pin+'-0','G0.'+port,'기존 '+name+' 리드 귀환','G0','신호/G0를 원래 꼬임쌍으로 회수. 전원 구동부 귀환과 합치지 않음')
for name,pin in [('조명','A0'),('열쇠','A1'),('RFID','A5')]:
    wire('IN-'+pin,'기존 '+name+' 신호선','Arduino '+pin,'기존입력/실물대조','기존 접속/ADC 동작 보존. 0~5V 입력범위와 실제 출력형식 대조;12V 신호 직결 금지. 새 센서PCB 없음')
for label,start,end,dom in [('RFID-V+','P12.7','RFID 정격+12V','P0'),('RFID-0','P0.7','RFID 전원−','P0'),('SENS-V+','P12.8','기타 정격12V센서 +','P0'),('SENS-0','P0.8','기타 정격12V센서 −','P0'),('MP3-RX','KT403A TX','Arduino D2','G0'),('MP3-TX','Arduino D3','KT403A RX','G0')]:wire(label,start,end,dom,'전원 정격/출력형식 확인 후 연결' if 'RFID' in label or 'SENS' in label else '')
for label,start,end in [('AMP+','홍싱 기존 어댑터 +','HONGXING DC+'),('AMP−','홍싱 기존 어댑터 −','HONGXING DC−')]:wire(label,start,end,'G0 / 홍싱은 별도 전압','홍싱 기존 어댑터 사용. +를 로직5L에 합치지 않음. 음극은 MP3 IN GND를 통해 G0와 공통')
for ch in ['L','R']:wire('AUD-'+ch,'KT403A DAC_'+ch,'HONGXING MP3 IN '+ch,'G0','기존 라인오디오 직결; SPK± 출력과 구별')
wire('AUD-GND','KT403A GND','HONGXING MP3 IN GND','G0','기존 오디오선 GND. 홍싱 전원−와 공통인 구조이며 P0에는 연결하지 않음')
for n,label,src,target in [(1,'PANEL-5V','5L.6','도어 VCC'),(2,'PANEL-0V','G0.6','도어 GND'),(3,'PANEL-DATA','Arduino D11','595 SER pin14'),(4,'PANEL-CLK','Arduino D13','595 SRCLK pin11'),(5,'PANEL-LATCH','Arduino D7','595 RCLK pin12'),(6,'BTN-NEXT','Arduino A3','도어 버튼 COM/NO')]:wire(label,src,'J7.'+str(n)+' → '+target,'G0','기존 Gun/Hint 선 철거 후 재사용')
wire('AC-L','기존 차단기 부하측 L','SMPS L','AC','기존 AC 회로와 정격 보존. Ethernet 심선 사용 금지')
wire('AC-N','기존 N 분배','SMPS N','AC','PE나 DC 0V와 연결하지 않음')
for dest in ['SMPS FG','금속 함체','금속 도어']:wire('PE-'+str(len(wires)),'기존 PE 접지부',dest,'PE','보호접지 연속성 보존; Ethernet 심선으로 PE 구성 금지')
heads=['양쪽 선 라벨','시작','끝','전원 영역','시공 조건']
csvout('wire-segments.csv',heads,wires);csvout('full-wiring-schedule.csv',heads,wires)
csvout('pin-and-wire-labels.csv',heads,[r for r in wires if r[0].startswith(('IN-','OUT-','MOT-','PANEL','BTN','MP3'))])
landing=[('D8','액자','G0','기존 S→D8 / 귀환→G0.2'),('A0','조명','기존 입력','기존 신호→A0 / 출력형식 대조'),('A1','열쇠','기존 입력','기존 신호→A1 / 출력형식 대조'),('A5','RFID','기존 입력','기존 신호→A5 / 출력형식 대조'),('D6','책','G0','기존 S→D6 / 귀환→G0.8 / 기존100Ω'),('MAG1','몰딩 자석','P0','+→RY-A CH1 선택접점 / −→P0.1'),('MAG2','슬라이드 자석','P0','+→RY-A CH2 선택접점 / −→P0.2'),('MAG3','책 자석','P0','+→RY-A CH3 선택접점 / −→P0.3'),('L298 OUT','모터','P0','기존 OUT1 / OUT2 단자; GND 아님'),('RY-A CH4','창문','W0 기존 SELV','기존 COM / 선택접점')]
csvout('field-terminal-landing.csv',['기존 접속위치','대상','영역','실제 연결'],landing)
csvout('passage-schedule.csv',['묶음','내용','경로'],[['P','P12/P0 두 쌍','상부→DDR/DC-D 각각'],['M','3자석 귀환 + 릴레이 접점급전','상부P12/P0↔하부'],['S','RFID/정격12V센서 전원 쌍','필요 회로만'],['A','홍싱 기존 어댑터 +/−','상부→하부 HONGXING']])
labels='<!doctype html><html lang="ko"><meta charset="utf-8"><title>MONG SHOT v5 양끝 라벨</title><style>body{font-family:Arial,"Malgun Gothic"}main{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}.label{border:1px solid #777;padding:6px;font-size:10px;break-inside:avoid}b{font-size:12px}@media print{button{display:none}}</style><button onclick="print()">인쇄</button><h1>v5 · 같은 구간 라벨을 양 끝에</h1><main>'
for row in wires:
    for side in ['A','B']:labels+='<div class="label"><b>'+html.escape(row[0])+'</b> · '+side+'<br>'+html.escape(row[1]+' → '+row[2])+'<br>'+row[3]+'</div>'
write('hardware/wire-labels.html',labels+'</main></html>')
js('tests/installation-counts.json',dict(revision=REV,wireSegments=len(wires),endLabels=len(wires)*2,fieldTerminals=0,customSensorBoards=0,customMagnetBoards=0,groundBlocks=2,additionalFuses=0))

# Replace blank historical checks while retaining any future completed v5 cells.
checks=[
 ('기록','Arduino 핀 기준 양끝 라벨 및 릴레이8채널 IN/COM/NO/NC/코일전압 기록'),
 ('실측','상하 유효 폭/높이/깊이 및 RFID/홍싱/어댑터 커넥터 외곽 실측'),
 ('실측','기존 관통구 위치/직경/모서리/굽힘/클립/잔여 케이블 확인'),
 ('케이블','각 케이블 Cu/CCA/AWG/편도길이/사용가능 페어/접속저항 기록'),
 ('케이블','자석별 동작전류/말단전압/온도, 모터 기동/스톨전류 확인'),
 ('기구','부품/덕트 예약영역 및 도어후면105mm 필요조건 대조'),
 ('기구','SMPS/DDR 환기방향/제조사 간격/열원/온도경감 확인'),
 ('무전원','P0 포트내 연속성 및 부하별 독립 귀환 확인'),
 ('무전원','G0 포트내 연속성 및 Arduino/MP3/패널 귀환 확인'),
 ('무전원','GND-MOTOR-REF로 P0/G0 공통 확인. 절연으로 합격 판정하지 않음'),
 ('무전원','MP3↔홍싱 오디오GND 공통 확인. 홍싱 어댑터는 별도 출력이며 P0와 연결하지 않음'),
 ('무전원','기존 PE→SMPS FG/함체/도어 연속성 보존; DC귀환과 구별'),
 ('모터','L298 Vs=P12/Vss=5D/GND=P0; 5V-EN 전원점퍼와 ENA 점퍼를 각각 확인/제거 조건 대조'),
 ('모터','D4/D5/A2 직결과 공통 기준선 확인. 기동/정지/PWM 시 오작동·리셋 확인'),
 ('릴레이','기존 IN1~4 직결과 active LOW 확인. 기존 보드 입력 바이어스/무신호/리셋 접점 동작 확인'),
 ('릴레이','RY-B는8채널 추적 후에만 전원/IN 재접속; 미사용 IN 방치하지 않음'),
 ('센서','12V 출력형식 PNP/NPN/접점 확인; 연속 아날로그이면 옵토 회로 변경 승인 전 연결 금지'),
  ('센서','A0/A1/A5 입력전압0~5V, ADC 임계값/카운트 유지 확인'),
 ('센서','기존 D8/D6 리드 쌍 / D6 기존100Ω 보존 / 새 센서판이나 RC 일괄 추가 없음'),
 ('전원','DC-D=5D/P0, DC-L=5L/G0 각각5V 확인 후 장치 연결'),
 ('전원','외부5V와 USB VBUS 중복급전 방지, USB/계측기 PE 우회 경로 확인'),
 ('다이오드','전원차단/잔류전압0에서 다이오드단독 양방향 검사 / 자석+쪽 K줄 확인'),
 ('다이오드','자석별 접점 차단서지/접점아크/실제 해제시간 확인; 느리면 억제방식 변경'),
 ('오디오','기존 KT DAC L/R 및 GND→홍싱 MP3 IN 직결. SPK± 미사용, 홍싱 어댑터+를5L에 연결하지 않음'),
 ('표시','Gun/Hint 제거 후595 D11/D13/D7 및 A3버튼/4.7k풀업/6LED1.5k 확인'),
 ('표시','2초1회/누름유지 반복없음/대기 중 입력미예약/20초·1초·10초 유지'),
 ('전체','모든 부하 동시전환 시 Uno5V/입력파형·오판정·리셋 확인'),
 ('전체','닫힌문 온도/배선마찰/기동·정전복귀/필요시 별도 비상해제 확인'),
 ('인수','최종 시공대로 선 구간표·케이블기록·양끝라벨·치수/전류/검사결과 갱신')]
checkpath=H/'commissioning-checklist.csv'
if not (backup/'commissioning-checklist.csv').exists():shutil.copy2(checkpath,backup/'commissioning-checklist.csv')
with checkpath.open(encoding='utf-8-sig') as f:prior=list(csv.reader(f))[1:]
priorby={r[1]:r[2:] for r in prior if len(r)>1}
csvout('commissioning-checklist.csv',['단계','검사 항목','결과','측정값/사진','검사자/일시'],[[a,b,*priorby.get(b,['','',''])] for a,b in checks])
ratingpath=H/'final-rating-record.csv'
if not (backup/'final-rating-record.csv').exists():shutil.copy2(ratingpath,backup/'final-rating-record.csv')
with ratingpath.open(encoding='utf-8-sig') as f:prior=list(csv.reader(f))[1:]
priorby={r[0]:r[2:] for r in prior if r}
ratings=[('CABINET','상하 유효 폭/높이/깊이/관통구/도어'),('RFID','실제몸체/커넥터/전압/전류/출력PNP·NPN·접점·아날로그'),('AMP','홍싱 몸체/어댑터정격/MP3 IN 임피던스/입력GND 관계'),('MAIN12','SMPS 모델/동시부하/기동/전류제한/온도경감'),('CABLES','케이블별Cu·CCA/AWG/편도길이/단심저항/페어/접속/온도'),('5V','5D 및 절연5L의 부하/리플/최저입력/온도'),('ISOLATION','P0/G0 공통 기준선/독립 전력귀환/PE 대조. 홍싱도 오디오GND 공통'),('RELAYS','8채널/active LOW/코일정격/접점/NO·NC/리셋동작'),('MOTOR','정격/기동/스톨전류/Vs·Vss/5V-EN·ENA점퍼/리미트'),('SENSORS','기존 출력형식/귀환/입력전압/ADC/기존필터응답'),('MAGNETS','전류/말단전압/다이오드/차단서지/해제시간/정전동작'),('AUDIO','기존 DAC라인/GND 직결/홍싱 입력정격/왜곡/P0 우회 여부'),('PE','인입/SMPS/함체/도어의 보호접지 경로'),('PANEL','LED전류/2초버튼/도어하네스/USB중복급전 방지')]
csvout('final-rating-record.csv',['ID','기입할 실물 값','측정값/사진','검사자'],[[a,b.replace('DACレベル/DCバイアス','DAC레벨/DC바이어스'),*priorby.get(a,['',''])] for a,b in ratings])

# Point-to-point component netlist for building the new small interfaces.
nets=[]
def net(name,*pins):nets.append([name,' ; '.join(pins)])
for pin,rin,name in relays:net('DIRECT-'+pin,'Arduino.'+pin,'RY-A.'+rin)
for pin,target in [('D4','IN1'),('D5','IN2'),('A2','ENA')]:net('DIRECT-'+pin,'Arduino.'+pin,'L298.'+target)
net('COMMON-REFERENCE','Arduino.GND','G0','L298.GND','P0','RY-A.GND')
for index in [1,2,3]:
    net('MAG'+str(index)+'-K','RY-A.CH'+str(index)+'.선택접점뒤_자석양극선','D-M'+str(index)+'.K')
    net('MAG'+str(index)+'-A','P0.'+str(index),'D-M'+str(index)+'.A')
for ch in ['L','R']:net('AUD-'+ch,'KT403A.DAC_'+ch,'HONGXING.MP3_IN_'+ch)
net('AUD-GND','KT403A.GND','HONGXING.MP3_IN_GND','HONGXING.DC−','G0')
csvout('interface-component-netlist.csv',['네트','같은 네트의 부품 핀'],nets)

# Cable assignments are proposed only; actual legacy colors/available pairs must be traced.
pairs=[('P1','주황 / 흰주황'),('P2','녹색 / 흰녹색'),('P3','파랑 / 흰파랑'),('P4','갈색 / 흰갈색')]
cables=[]
for n in range(1,4):
    for pair,colors in pairs:cables.append(['C-M'+str(n),pair,colors,'자석'+str(n)+' +/−','기본 P1; P2~P4는 연속성/미사용 확인 후 병렬 후보','미측정','미측정','미확정'])
for name,signal in [('C-FRAME','액자 S/G0'),('C-BOOK','책 S/G0'),('C-LIGHT','조명 기존 신호/귀환 대조'),('C-KEY','열쇠 기존 신호/귀환 대조'),('C-RFID','RFID 기존 접점/신호 대조')]:
    cables.append([name,'P1','원래 꼬임쌍 확인',signal,'12V센서는 다른 페어에 정격 전원+/P0; G0와 혼용 금지','미측정','미측정','미확정'])
record=H/'ethernet-cable-register.csv'
if record.exists():
    with record.open(encoding='utf-8-sig') as f:oldrows=list(csv.reader(f))[1:]
    measured={(r[0],r[1]):r for r in oldrows if len(r)==8 and any(v and v not in ['미측정','미확정'] for v in r[5:])}
    cables=[measured.get((r[0],r[1]),r) for r in cables]
csvout('ethernet-cable-register.csv',['제안 케이블ID','페어','색상 예시','할당','병렬/전원 조건','편도길이 m','전류 A','Cu/AWG/저항 확인'],cables)
js('hardware/cable-design.json',dict(revision=REV,reference='Belden 1583A 24AWG Cu를 설명용으로만 사용. 설치 케이블의 품질/정격 보증 아님.',referenceOhmPerM=0.0938,temperatureCoefficient=0.00393,formula='Rloop=2*L*R20*(1+0.00393*(T-20))/parallelPairs; Vdrop=I*Rloop; Ploss=I*I*Rloop',parallelRule='가용 페어 전체의 +/−를 양끝에서 동일하게 병렬. 각 원래 페어 안에서 +와−를 구성. 한쪽만 병렬 금지.',status='전압강하 계산은 허용전류/온도/단락보호 적합 판정이 아님',extraFuseDecision='사용자 결정으로 추가 메인/분기 퓨즈 제외. 기존 차단기/PE 보존. SMPS 과전류 보호는 가는 심선의 개별 보호를 대체하지 않음.'))
csvout('sensor-interface-modes.csv',['입력','기존 임계값','실물 출력형식 기록','적용 원칙'],[['A0 조명','ADC<500','미기록','접점/5V아날로그는 기존 입력 보존. 12V스위칭만 절연. 12V연속아날로그에 일반 옵토 금지'],['A1 열쇠','ADC<100','미기록','동일. 전원 정격만으로 출력형식을 추정하지 않음'],['A5 RFID','ADC<400','미기록','무전압 접점이면 G0기준 접점만 연결. 현재 P0/G0 공통. 출력전압과 기존 접속을 대조']])
budget=[['Uno/주변','5L',0.20,'설계 할당; 실측 아님'],['KT403A DAC/UART','5L',0.50,'피크 여유를 둔 할당; 홍싱 전력/스피커는 포함하지 않음'],['도어LED/버튼','5L',0.05,'여유 할당; 실제 LED는 저전류'],['로직5V센서/입력','5L',0.25,'정격에 따라 재대조할 예비 할당'],['로직 합계','5L',1.00,'DDR5V3A 이하; 설계 한도1.2A로 관리'],['릴레이8코일+드라이버논리','5D',0.80,'코일 실물 전류/동시 동작 수 확인 전 잠정 한도']]
csvout('power-budget.csv',['대상','레일','계획 전류 A','근거/조건'],budget)
js('hardware/power-decisions.json',dict(revision=REV,primary='12V SMPS1대 + DDR-15G-5 절연로직5V + 4091 부하측5V',pairing={'P12':'P0','5D':'P0','5L':'G0'},logicBudgetA=1.2,logicConverterRatedA=3,logicConverterRatedW=15,logicConverterDerating='입력9~12V에서는 최대2.7A; 12~36V에서3A. 온도 경감 별도',inputExample='5V1A=5W / 효율84% / 12V입력 약0.50A. 5V3A full load면 약1.49A. 설명 계산이며 실측 아님.',reason='앞선 SMPS1대 조건 및 하부AC배선 추가 회피. GPIO 절연모듈을 제거하여 GND는 공통. DDR는 별도5V 분기 후보로 남겼지만 전체 갈바닉 절연은 제공하지 않음. 12V 급락/정전 시 로직도 영향받는 한계.',alternative=dict(maker='MEAN WELL',part='HDR-30-5',output='5V3A15W',sizeMm=[35,90,54.5],clearance='HDR 매뉴얼: 위40/아래20/좌우5mm 확보. 현재45×150mm 확보영역에 외곽상 들어가지만 AC단자 보호와 AC/DC 배선 분리를 재검토해야 함.',url='https://www.meanwell.com/Upload/PDF/HDR-30/HDR-30-SPEC.PDF',status='비교 대안; 현재 배치/구매수량에 포함하지 않음')))

details={p['id']:dict(title=p['name'],desc=p['basis'],rows=[['영역',p['domain']],['좌표',f"{p['bay']} ({p['x']},{p['y']}) mm"],['확보',f"{p['reserveW']}×{p['reserveH']} mm"],['몸체 검토',f"{p['bodyW']}×{p['bodyH']}×{p['bodyD']} mm"]],note='실측 전 설치 확정 아님. 현재 v5.3은 GND-MOTOR-REF로 P0/G0 공통이며 시스템 갈바닉 절연이 아닙니다.',nets=[p['domain']]) for p in parts}
details['gnd']['desc']='G0는 전압변환기가 아니라 DDR의 출력−를 나누는 분배블록입니다. 짝은5L(+5V)입니다. P0와 제품/크기가 같고 제어 기준선으로 공통입니다. 귀환 분기이며 절연이 아닙니다.'
details['logic-positive']['desc']='DDR의 출력+를 나누는 로직5V 분배블록입니다. G0와 한 쌍입니다. 부하측5V인5D와 연결하지 않습니다.'
details['l298']['desc']='D4/D5/A2를 기존처럼 직결합니다. G0.4에서 L298 GND로 기준선을 연결하므로 P0/G0는 공통입니다. 모터 전력 귀환은 별도 P0-MOTOR로 유지합니다.'
details['rfidbox']['desc']='기존 제어함을 보존하되 160×100×65mm 가정으로 줄였습니다. 정격12V일 때 전원은 P0. 무전압 접점은G0 입력으로,12V 비절연 스위칭 출력만 옵토로 전달합니다. 실제 출력형식 대조.'
details['frontpanel']=dict(title='외부 진행 LED·버튼',desc='6개 LED + 2초 진행 버튼. 기존 AVR 동작과 595 래치를 유지합니다.',rows=[['DATA / CLK / LATCH','D11 / D13 / D7'],['진행 버튼','A3 / J7.6'],['귀환','G0 / J7.2']],note='Gun/Hint 배선을 제거한 뒤 재사용. 실물 하드웨어 업로드 전 MP3 라이브러리 호환 문제 해결.',nets=['G0'])
js('simulation/source/design-data.json',dict(model=model,details=details,graph=graph))

# Rendering, documentation and UI assembly share the data above.
from render_v5 import render_all
render_all(ROOT,model,details,graph,bomdata,wires,gports,positive,landing,sources,table)
print('v5 design regenerated:',len(parts),'mounting envelopes,',len(wires),'physical wires,',len(items),'BOM rows')
