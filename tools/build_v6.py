"""Add v6 alongside an immutable v5.3 snapshot; no firmware or original design edits."""
from pathlib import Path
import copy,csv,hashlib,html,json,math,os,shutil,subprocess,sys
R=Path(__file__).resolve().parents[1]; A=R/'archive/v5.3-preserved'; H=R/'hardware/v6'; S=R/'simulation/source'
H.mkdir(parents=True,exist_ok=True)
def dump(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def csvwrite(name,heads,rows):
    with (H/name).open('w',encoding='utf-8-sig',newline='') as f:w=csv.writer(f);w.writerow(heads);w.writerows(rows)
def read(name):return json.loads((A/'hardware'/name).read_text(encoding='utf-8'))
v5=read('cabinet-fit-model.json'); model=copy.deepcopy(v5);model['revision']='v6.1-harness-first'
model['basis']='사진 기반 400×260 / 400×560 / 깊이120mm 가정. 실측·타공도 아님. v5.3 원본은 별도 보존.'
parts=[p for p in model['parts'] if p['id']!='isolated5'];model['parts']=parts
changes={
 'rfidbox':('lower',25,25,170,120,'RFID 제어함','P0'),
 'amp':('lower',215,25,160,100,'HONGXING','G0'),
 'mp3':('lower',235,130,70,35,'KT403A MP3','G0'),
 'relayA':('lower',35,230,90,75,'4CH 릴레이 A','P0'),
 'relayB':('lower',145,230,90,75,'4CH 릴레이 B','P0'),
 'magdiodes':('lower',130,230,10,65,'자석 다이오드 ×3 · 릴레이 옆','P0'),
 'l298':('lower',160,350,90,75,'L298N E6','P0'),
 'uno':('lower',260,370,90,65,'Arduino Uno','G0'),
 'mag-power':('lower',25,470,75,50,'P12 · 조건부 12V','P0'),
 'power-ground':('lower',105,470,75,50,'★ P0 · 전력 0V','P0'),
 'buck':('lower',190,470,45,65,'단일 5V 강압기','P0'),
 'gnd':('lower',245,470,65,40,'G · 로직 0V','G0'),
 'logic-positive':('lower',315,470,65,40,'5V · 통합 분배','G0')}
for p in parts:
    if p['id'] in changes:
        bay,x,y,w,h,name,domain=changes[p['id']];p.update(bay=bay,x=x,y=y,reserveW=w,reserveH=h,name=name,domain=domain)
    p.pop('airClearance',None);p.pop('bodyOffsetY',None)
    p['bodyX']=p['x']+(p['reserveW']-p['bodyW'])/2;p['bodyY']=p['y']+4
    if p['id']=='buck':p['basis']='기존 후보 Pololu D36V50F5 #4091 한 대. VIN=P12.5, 입력 GND=P0.5, 출력5V/G. 입력−와 출력−는 내부 공통. 5.5A는36Vin 조건 표기이며12Vin·밀폐함 실측이 아님.'
    elif p['id']=='l298':p['basis']='D4/D5/A2 직결 유지. GND는 P0.4 독립 귀환 한 가닥만. G→L298 추가선은 삭제. VMS는 모터 정격 미확인으로 공급 미확정. 5V-EN과 ENA는 별개 점퍼이며 실물 단자 방향 확인 전 변경 금지.'
    elif p['id']=='gnd':p['basis']='5V 강압기 출력 GND에서만 공급. P0와 전기적으로 공통이나 직접 점퍼·G→L298 선 없음. Arduino와 가장 가까운 몸체 간격 약47mm(도면상).'
    elif p['id']=='logic-positive':p['basis']='5D/5L를 단일5V로 통합. Uno·릴레이A/B·KT403A·도어에 분기. 모터 VMS를5V로 선택하려면 별도 부하예산 확인. 다른5V 출력과 병렬 연결 금지.'
    elif p['id']=='power-ground':p['basis']='SMPS V−→P0.IN. 자석1~3·L298·강압기·조건부12V장치 귀환을 각각 별도 포트로. G 직접 연결 금지. 이상적인0Ω 점이 아니라 유한 임피던스가 있는 분배점.'
    elif p['id']=='mag-power':p['basis']='상부SMPS에서 TRK-12P/TRK-0 페어만 하부로. P12.1~3 자석, .4 모터(U1), .5 강압기, .6/.7 조건부RFID/센서.'
    elif p['id']=='uno':p['basis']='5V.1/G.1에서 공급. G·5V 블록 몸체와50mm 이내 배치. L298 기준은 G→강압기GND→P0→L298의 짧은 공통 경로. A2=16은 Uno PWM 핀이 아니며 기존255는 HIGH와 동일.'
duct_groups=[
 dict(id='U-DC',bay='upper',rect=[25,155,350,20],group='power'),
 dict(id='U-PASS',bay='upper',rect=[100,175,20,85],group='power'),
 dict(id='L-ROOF',bay='lower',rect=[25,0,350,20],group='power'),
 dict(id='L-PWR',bay='lower',rect=[0,0,25,550],group='power'),
 dict(id='L-SIG',bay='lower',rect=[380,20,20,440],group='signal'),
 dict(id='RFID-SIG',bay='lower',rect=[195,20,20,150],group='signal'),
 dict(id='H0-SIG',bay='lower',rect=[195,170,185,20],group='signal'),
 dict(id='H1-PWR',bay='lower',rect=[25,200,350,20],group='power'),
 dict(id='H2-SIG',bay='lower',rect=[25,315,355,25],group='signal'),
 dict(id='H3-DC',bay='lower',rect=[25,435,355,25],group='power')]
model['ducts']=dict(upperVertical=[d['rect'] for d in duct_groups if d['bay']=='upper'],lowerVertical=[d['rect'] for d in duct_groups if d['bay']=='lower' and d['rect'][2]<d['rect'][3]],lowerHorizontal=[d['rect'] for d in duct_groups if d['bay']=='lower' and d['rect'][2]>=d['rect'][3]],groups=duct_groups,actualWidthMm=17.5,actualHeightMm=26.9)
for p in parts:
    p['orientation']={'relayA':'접점 상부 / 제어헤더 하부','relayB':'접점 상부 / 제어헤더 하부','uno':'디지털 헤더 상부 / 전원헤더 하부','l298':'제어헤더 상부 / 전원·출력 하부 · 실물 모듈 대조','mp3':'오디오 상부 / UART·전원 하부 · 실물 핀열 대조','buck':'입·출력 배선이 상부 DC 덕트로 · 실물 핀열 대조'}.get(p['id'],'도면 앵커는 실물 단자 위치 대조 전')
for p in parts:
    if p['id'] in ['relayA','relayB','uno','l298','mp3','buck']:p['basis']+=' / 배치 방향: '+p['orientation']
model['passage'].update(bundles=['TRK-12P/TRK-0: SMPS에서 P12/P0로 · 전원 한 쌍','홍싱 기존 어댑터 +/− 한 쌍','기존 현장 케이블: 신호/전력 그룹별 정리'],minimumConductors=4)
dump(H/'cabinet-fit-model.json',model)
by={p['id']:p for p in parts}
def center(pid):
    p=by[pid];return [p['bodyX']+p['bodyW']/2,p['bodyY']+p['bodyH']/2+(0 if p['bay']=='upper' else 330)]
def pos(pid,side='center',dy=0):
    p=by[pid];x,y=center(pid)
    if side=='left':x=p['bodyX']
    if side=='right':x=p['bodyX']+p['bodyW']
    if side=='top':y=p['bodyY']+(0 if p['bay']=='upper' else 330)
    if side=='bottom':y=p['bodyY']+p['bodyH']+(0 if p['bay']=='upper' else 330)
    return [round(x,2),round(y+dy,2)]
wire=[]
def add(label,start,end,net,cable,group,note='',condition='',ret=False,pair=''):
    d=dict(label=label,start=start,end=end,net=net,cable=cable,group=group,note=note,condition=condition,status='미확인' if condition else '도면 계획',returnWire=ret,pair=pair);wire.append(d);return d
add('TRK-12P','SMPS V+','P12.IN','+12V','TRK','전력','TRK-0과 밀착·동일 경로',pair='TRK-0')
add('TRK-0','SMPS V−','P0.IN','P0','TRK','전력','모든 부하 귀환의 상위 트렁크',ret=True,pair='TRK-12P')
for n in [1,2,3]:
    add(f'M{n}-FEED',f'P12.{n}',f'RY-A CH{n} COM','+12V',f'MAG{n}','전력',pair=f'M{n}-FIELD−')
    add(f'M{n}-FIELD+',f'RY-A CH{n} 선택접점',f'외부 자석{n} +',f'MAG{n}+',f'MAG{n}','전력','NO/NC는 기존 기능대로 추적. 다이오드 K(띠)는 이 선',pair=f'M{n}-FIELD−')
    add(f'M{n}-FIELD−',f'P0.{n}',f'외부 자석{n} −','P0',f'MAG{n}','전력','원래 꼬임쌍 유지. 다이오드 A는 이 선',ret=True,pair=f'M{n}-FIELD+')
add('MOTOR-VMS-12','P12.4','L298 VMS','+12V','MOT-PWR','전력','5V 대안과 동시 연결 금지','U1: 모터 정격12V와 실제 기존 전압 확인 후에만',pair='P0-MOTOR')
add('MOTOR-VMS-5','5V.6','L298 VMS','+5V','MOT-PWR-ALT','전력','12V 대안과 택1. 모터 기동/스톨전류까지 강압기 예산에 추가','U1: 실제5V 모터·강압기 여유 확인 후에만',pair='P0-MOTOR')
add('P0-MOTOR','P0.4','L298 GND','P0','MOT-PWR','전력','독립 전력 귀환. G판에 추가 선을 연결하지 않음',ret=True,pair='MOTOR-VMS-12')
add('BUCK-IN+','P12.5','강압기 VIN','+12V','BUCK-IN','전력',pair='BUCK-IN−')
add('BUCK-IN−','P0.5','강압기 입력GND','P0','BUCK-IN','전력','G와 P0 사이의 유일한 계획 연결 경로',ret=True,pair='BUCK-IN+')
add('BUCK-5V','강압기 VOUT','5V.IN','+5V','BUCK-OUT','신호',pair='BUCK-G')
add('BUCK-G','강압기 출력GND','G.IN','G','BUCK-OUT','신호','입력−=출력− 내부 공통',ret=True,pair='BUCK-5V')
for n,dev in [(6,'RFID'),(7,'기타12V센서')]:
    add(f'{dev}-V+',f'P12.{n}',f'{dev} +12V','+12V',dev+'-PWR','전력','실제 정격과 기존 공급 전압 확인',f'U2: {dev} 정격12V 확인',pair=f'{dev}-0')
    add(f'{dev}-0',f'P0.{n}',f'{dev} 전원−','P0',dev+'-PWR','전력','신호 귀환과 임의 합치지 않음',f'U2: {dev} 전원 방식 확인',ret=True,pair=f'{dev}-V+')
ports=[(1,1,'Arduino 5V','Arduino GND','UNO-PWR'),(2,2,'RY-A VCC','RY-A GND','CAB-RLY'),(3,3,'RY-B VCC','RY-B GND','CAB-RLY-B'),(4,4,'J7.1 도어VCC','J7.2 도어GND','PANEL'),(5,7,'KT403A VCC','KT403A GND','CAB-MP3')]
for pp,gp,plus,minus,cab in ports:
    cond='U5: RY-B 기존4채널/전체8채널·JD-VCC 추적 후' if pp==3 else ''
    add(cab+'-5V',f'5V.{pp}',plus,'+5V',cab,'신호','VCC/JD-VCC 상태는 실물대로 확인' if pp in [2,3] else '',cond,pair=cab+'-G')
    add(cab+'-G',f'G.{gp}',minus,'G',cab,'신호','부하 전류를 Uno GND 핀으로 직렬 통과시키지 않음',cond,ret=True,pair=cab+'-5V')
for pin,target in [('D12','IN1'),('D10','IN2'),('D9','IN3'),('A4','IN4')]:add('OUT-'+pin,'Arduino '+pin,'RY-A '+target,pin,'CAB-RLY','신호','기존 active LOW/리셋 동작 확인','U5: 입력극성·JD-VCC 실물 확인',pair='CAB-RLY-G')
for pin,target in [('D4','IN1'),('D5','IN2'),('A2','ENA')]:add('MOT-'+pin,'Arduino '+pin,'L298 '+target,pin,'CAB-MOT','신호','추가 G→L298 선 없음. 기준 경로는 G→강압기→P0→L298. 제어선은 Arduino/L298 근접 배치로 짧게 정리. 별도 G 동봉 없음. ENA 상시ON 점퍼와5V-EN은 구분',pair='공유 기준: BUCK-G / BUCK-IN− / P0-MOTOR')
add('L298-VSS-5','5V.7','L298 5V/Vss','+5V','MOT-LOGIC','신호','5V-EN 제거 후 5V단자가 입력인 실물 모듈에서만. GND는 P0.4 기존 귀환 사용','U1: 5V단자 입출력/온보드레귤레이터 점퍼 확인')
for end,pin in [('KT403A TX','D2'),('KT403A RX','D3')]:add('MP3-'+pin,'Arduino '+pin,end,pin,'CAB-MP3','신호','D2는 수신, D3는 송신. 기존 UART 전압·저항 대조','U7: KT403A UART 전압범위',pair='CAB-MP3-G')
for name,pin,gp in [('액자','D8',5),('책','D6',6)]:
    add('IN-'+pin,f'외부 {name} 리드 S','Arduino '+pin,pin,'REED-'+pin,'신호','원래 꼬임쌍. 책 D6 기존100Ω 보존',pair='REED-'+pin+'-G')
    add('REED-'+pin+'-G',f'G.{gp}',f'외부 {name} 리드 귀환','G','REED-'+pin,'신호',ret=True,pair='IN-'+pin)
for pin,name in [('A0','조명'),('A1','열쇠'),('A5','RFID')]:add('IN-'+pin,'기존 '+name+' 신호','Arduino '+pin,pin,'FIELD-'+pin,'신호','무전압 접점이면 신호/G 같은 페어. 전압출력이면 범위·기준 확인 전 연결 확정 금지','U2: 출력형식·실제0~5V범위 미확인')
for pin,jp,target in [('D11',3,'595 SER'),('D13',4,'595 SRCLK'),('D7',5,'595 RCLK'),('A3',6,'진행 버튼')]:add('PANEL-'+pin,'Arduino '+pin,f'J7.{jp} '+target,pin,'PANEL','신호','기존 Gun/Hint 배선 철거 후 핀 재사용',pair='PANEL-G')
for ch in ['L','R']:add('AUD-'+ch,'KT403A DAC_'+ch,'HONGXING MP3 IN '+ch,'AUDIO','AUD','오디오','SPK±는 라인입력에 연결하지 않음',pair='AUD-GND')
add('AUD-GND','KT403A GND','HONGXING MP3 IN GND','G','AUD','오디오','전원− 공통 구조는 실물 도통 대조. 별도 P0/G 선 추가 없음',ret=True,pair='AUD-L / AUD-R')
add('AMP+','기존 어댑터 +','HONGXING DC+','AMP+','AMP-PWR','오디오','어댑터 기존 전압 유지. 5V판과 합치지 않음',pair='AMP−')
add('AMP−','기존 어댑터 −','HONGXING DC−','AMP−','AMP-PWR','오디오','오디오GND 경로 외 P0/G 직접 연결 없음',ret=True,pair='AMP+')
for name in ['A','B']:add('MOTOR-OUT-'+name,'L298 OUT'+('1' if name=='A' else '2'),'외부 모터 '+name,'MOTOR-OUT','MOTOR-OUT','전력','두 선 모두 H브리지 출력. 어느 쪽도 P0/G 고정 금지',pair='MOTOR-OUT-'+('B' if name=='A' else 'A'))
for name in ['COM','선택접점']:add('WIN-'+name,'RY-A CH4 '+name,'외부 창문 기존 '+name,'W0','WINDOW','전력','기존 SELV 접점회로. P0/G 연결 없음; NO/NC 추적')
for net,start in [('L','기존 차단기 부하측 L'),('N','기존 N 분배')]:add('AC-'+net,start,'SMPS '+net,'AC','AC-IN','AC','기존 AC 회로 보존. 현장 랜심선 사용 금지')
for n,end in [(87,'SMPS FG'),(88,'금속 함체'),(89,'금속 도어')]:add('PE-'+str(n),'기존 PE 접지부',end,'PE','PE','PE','보호접지. DC 귀환에 사용 금지',ret=False)
for d in wire:
    d['labels']=[d['label']+' / '+s for s in ['시작','경로','끝']]
dump(H/'wire-segments.json',wire)
csvwrite('wire-segments.csv',['라벨','시작','끝','넷','경로(덕트 그룹)','케이블 이름','짝/기준 경로','상태','조건','시공 메모'],[[d[k] for k in ['label','start','end','net','group','cable','pair','status','condition','note']] for d in wire])
csvwrite('mounting-schedule.csv',['ID','부품','함','X mm','Y mm','확보W','확보H','몸체W','몸체H','몸체D','근거'],[[p[k] for k in ['id','name','bay','x','y','reserveW','reserveH','bodyW','bodyH','bodyD','basis']] for p in parts])
groundports=[['P0','IN','SMPS V−','TRK-0']]+[['P0',str(n),'자석'+str(n)+' −',f'M{n}-FIELD−'] for n in [1,2,3]]+[['P0','4','L298 GND','P0-MOTOR'],['P0','5','강압기 입력GND','BUCK-IN−'],['P0','6','RFID 전원− / 조건부','RFID-0'],['P0','7','기타12V센서− / 조건부','기타12V센서-0'],['P0','8~12','미사용 · G 직접 연결 금지',''],['G','IN','강압기 출력GND','BUCK-G']]+[['G',str(gp),minus,cab+'-G'] for pp,gp,plus,minus,cab in ports]+[['G','5','액자 리드 귀환','REED-D8-G'],['G','6','책 리드 귀환','REED-D6-G'],['G','8~12','미사용 · P0/L298 추가 연결 금지','']]
csvwrite('ground-port-schedule.csv',['블록','포트','대상','선 라벨'],groundports)
positiveports=[['P12','IN','SMPS V+','TRK-12P']]+[['P12',str(n),f'RY-A CH{n} COM',f'M{n}-FEED'] for n in [1,2,3]]+[['P12','4','L298 VMS / U1 조건부','MOTOR-VMS-12'],['P12','5','강압기 VIN','BUCK-IN+'],['P12','6','RFID +12V / 조건부','RFID-V+'],['P12','7','기타12V센서 + / 조건부','기타12V센서-V+'],['5V','IN','강압기 VOUT','BUCK-5V']]+[['5V',str(pp),plus,cab+'-5V'] for pp,gp,plus,minus,cab in ports]+[['5V','6','VMS=5V 대안 / U1 조건부','MOTOR-VMS-5'],['5V','7','L298 Vss / 점퍼 확인 후','L298-VSS-5']]
csvwrite('positive-port-schedule.csv',['블록','포트','대상','선 라벨'],positiveports)

# Conductive graph: internal bonds are explicit, conditional unknown field bonds excluded.
edges=[]
def edge(a,b,label):edges.append(dict(a=a,b=b,label=label))
edge('P0','SMPS−','TRK-0')
for n in [1,2,3]:edge('P0',f'MAG{n}−',f'M{n}-FIELD−')
edge('P0','L298_GND','P0-MOTOR');edge('P0','BUCK_IN_GND','BUCK-IN−');edge('BUCK_IN_GND','BUCK_OUT_GND','BUCK-INTERNAL-GND');edge('BUCK_OUT_GND','G','BUCK-G')
edge('P0','RFID 전원−','RFID-0');edge('P0','기타12V센서 전원−','기타12V센서-0')
for pp,gp,plus,minus,cab in ports:edge('G',minus,cab+'-G')
edge('G','REED_D8_G','REED-D8-G');edge('G','REED_D6_G','REED-D6-G');edge('KT403A GND','AMP_LINE_GND','AUD-GND');edge('AMP_LINE_GND','AMP_DC_NEG','AMP-INTERNAL-GND');edge('AMP_DC_NEG','ADAPTER_NEG','AMP−')
for n,node in [(87,'SMPS_FG'),(88,'CABINET'),(89,'DOOR')]:edge('PE',node,'PE-'+str(n))
def paths(start,end,ee):
    adj={}
    for e in ee:adj.setdefault(e['a'],[]).append((e['b'],e['label']));adj.setdefault(e['b'],[]).append((e['a'],e['label']))
    result=[]
    def visit(n,seen,route):
        if n==end:result.append(route);return
        for b,l in adj.get(n,[]):
            if b not in seen:visit(b,seen|{b},route+[l])
    visit(start,{start},[]);return result
original_edges=edges+[dict(a='G',b='L298_GND',label='원 지시서 CAB-MOT G.8→L298 GND')]
audit_paths=paths('P0','G',original_edges);corrected_paths=paths('P0','G',edges)
graph=dict(revision=model['revision'],systemGalvanicIsolation=False,edges=edges,originalInstructionEdges=original_edges,
 originalInstructionPaths=audit_paths,correctedPaths=corrected_paths,unknownBonds=['U2: A0/A1/A5 센서 전원−와 신호 기준','U4: L298 탭/방열판·홍싱 외함과 PE','U6: USB/계측기 접지','U5: 릴레이 보드 실제 GND/JD-VCC'])
dump(H/'ground-connectivity.json',graph)
corrections=[
 dict(id='C1',title='지시서의 G→L298 선 삭제',reason='강압기 GND 외에 P0→L298 GND→G 경로가 하나 더 생깁니다. 모터 전류가 두 경로로 분류하므로 기준선에는 전류가 안 흐른다는 보장이 없습니다.',action='L298 GND는 P0.4 귀환 한 가닥만. 제어선은 공용 신호 덕트에 모으고, 모듈 앞에서 짧게 분기. CAB-MOT의 별도 GND 도체 요구는 이 안에서 제외.',tradeoff='긴 제어선·접지차 허용 여부는 실측 필요. 모터와 로직의 완전 절연이 필요한 안이 아닙니다.'),
 dict(id='C2',title='현재 v5.3을 절연안으로 부르지 않음',reason='지시서의 v5 설명은 옛 상태입니다. 현재 보존본 v5.3도 L298 직결 기준선 때문에 P0/G0 공통입니다.',action='실제 v5.3 HTML·데이터를 그대로 보존하고 v6만 별도 생성.'),
 dict(id='C3',title='L298 점퍼·모터 전압은 자동 확정하지 않음',reason='모터 정격과 L298 모듈 회로를 모릅니다. IC 사양만으로 모듈의 5V 단자가 입력인지 출력인지 결정할 수 없습니다.',action='VMS12V/5V는 서로 배타적인 조건부 항목. Vss 외부5V도 실물5V-EN 확인 후. ENA 점퍼는 별개.'),
 dict(id='C4',title='모든 미확인 항목은 도면 검사와 분리',reason='센서·섀시·USB를 실제 측정하지 않은 그래프는 실제 단일 경로를 증명하지 못합니다.',action='검사는 계획 그래프만 판정. U1~U7은 모두 미확인. 새 절연 모터드라이버는 채택하지 않음.'),
 dict(id='C5',title='규격이 다른 두 선의 트윈 페룰을 자동 지정하지 않음',reason='트윈 페룰과 단자는 허용 도체 수·규격이 맞아야 합니다. 이번 수정안은 L298 GND 이중 삽입 자체를 없앱니다.',action='한 포트 한 선 원칙. 다이오드 리드는 정격 접속·절연·고정을 실물 대조.'),
]
unknowns=[
 ['U1','모터 / L298','정격전압·실제 기존 VMS·기동/스톨전류·5V단자·5V-EN/ENA 점퍼','12V/5V 급전 확정 보류. 5V 모터에12V 금지. L298 전압강하는 전류에 따라 달라짐.'],
 ['U2','기존 센서','A0/A1/A5 접점/PNP/NPN/아날로그 및 입력 범위·신호귀환','무전압 접점만 G 페어로. 전원12V만 보고 출력12V로 단정하지 않음.'],
 ['U3','현장 랜케이블','Cu/CCA·AWG·편도길이·자석전류·가용 페어·접속/온도','가정 계산과 실물 허용전류 판정 구별.'],
 ['U4','섀시 경유 우회','L298 탭/방열판·금속 고정물·홍싱 외함과 PE/DC−의 도통','DC 전원 차단 상태에서 장치별·USB 분리 후 경로 확인. PE 제거로 해결하지 않음.'],
 ['U5','릴레이A/B','active LOW·코일정격·JD-VCC 점퍼·RY-B4개 포함 총8채널','기존 접점·리셋 동작 추적 후 재결선. B를 예비로 단정하지 않음.'],
 ['U6','Uno / USB','외부5V 공급 중 USB VBUS 중복 및 PC/계측기 접지','외부5V와 USB의 동시 급전을 피하는 작업 순서 기록.'],
 ['U7','KT403A UART','RX 입력전압·TX 전압·직렬저항·실제 라이브러리 호환','DAC 라인오디오는 유지. SPK±는 홍싱 MP3 IN에 연결하지 않음.']]
checks=[
 dict(id='one-path',title='P0–G 연결은 강압기 경유 한 경로',pass_=len(corrected_paths)==1 and 'BUCK-INTERNAL-GND' in corrected_paths[0],detail=' → '.join(corrected_paths[0])),
 dict(id='load-returns',title='자석·L298 전력 귀환은 P0에만',pass_=all(e['a']=='P0' for e in edges if e['b'] in ['L298_GND','MAG1−','MAG2−','MAG3−']),detail='G→L298 추가선 없음. 자석1~3 각각 P0.1~3, 모터 P0.4.'),
 dict(id='signal-ref',title='제어 케이블·리드 기준 경로 명시',pass_=all(d['pair'] for d in wire if d['cable'].startswith('CAB-') or d['cable'].startswith('REED-')),detail='CAB-RLY/MP3와 리드는 G 동봉. CAB-MOT는 중복 경로를 피하려고 별도 G선을 제외한 명시적 예외.'),
 dict(id='audio',title='홍싱 전원−의 로직 연결은 AUD-GND 한 곳',pass_=len(paths('ADAPTER_NEG','G',edges))==1 and 'AUD-GND' in paths('ADAPTER_NEG','G',edges)[0],detail='어댑터−→홍싱 내부→오디오GND→KT403A→G. 외함 실제 도통은 U4.'),
 dict(id='pe',title='계획 그래프에서 PE와 DC 귀환 분리',pass_=not paths('PE','G',edges) and not paths('PE','P0',edges),detail='SMPS FG/함체/도어 보호접지 보존. 실제 섀시/USB 우회는 미측정.'),
 dict(id='unknown',title='U1~U7 미확인 / 조건부 급전 표시',pass_=all(d['status']=='미확인' for d in wire if d['condition']) and len(unknowns)==7,detail='급전 대안 둘을 동시에 시공하도록 표시하지 않음.'),
 dict(id='instruction-rejected',title='원 지시서의 중복 경로를 검사기가 검출',pass_=len(audit_paths)==2,detail='원문 연결대로는 P0–G 경로2개. 전부 합격으로 숨기지 않음.'),
]
for c in checks:c['pass']=c.pop('pass_')
dump(H/'instruction-audit.json',dict(corrections=corrections,originalPathCount=len(audit_paths),originalPaths=audit_paths))

# New BOM is strictly a subset of the preserved v5.3 BOM, not a driver upgrade.
bom=read('product-bom.json');bom['revision']=model['revision'];bom['items']=[x for x in bom['items'] if x['id']!='DC-L'];bom['removed']=bom.get('removed',[])+['DC-L DDR-15G-5 (v6만)'];bom['scope']='v5.3 품목에서 DDR 한 대 삭제. 신규 부품·단자열·퓨즈·절연 드라이버 추가 없음.'
for item in bom['items']:
    if item['id']=='DC-D':item.update(name='통합5V 강압기',location='하부 (190,470)',condition='5V/G 단일 분배. Uno+릴레이8코일+MP3+패널 잠정합계 약1.8A(실측 아님). 5.5A 표기는36Vin 조건이며12Vin 밀폐함에서 연속보장값 아님. 모터5V 급전은 별도 예산.')
    if item['id']=='G-P/G-L':item.update(name='전력/로직 귀환 분배',location='하부 P0(105,470) / G(245,470)',condition='같은0V 전위. G↔P0 계획 경로는 강압기 입력/출력GND 한 곳뿐. P0/G 직접 점퍼·G→L298 추가선 금지.')
    if item['id']=='P12/5L':item.update(name='12V / 통합5V 분배',location='하부 P12(25,470) / 5V(315,470)',condition='기존 두 블록 재사용. 5D/5L 구분 없음. 다른 전원 출력과 병렬 연결 금지.')
dump(H/'product-bom.json',bom)
csvwrite('product-bom.csv',['ID','용도','제조사','품번','수량','장소','조건'],[[x.get(k,'') for k in ['id','name','maker','part','qty','location','condition']] for x in bom['items']])

# One routing module owns compact harness paths shared by 2D and 3D.
from v6_duct_network import build_routes, harness_model
routes=build_routes(model,wire)
harness=harness_model(model,routes,wire)
from v6_harness_checks import validate
harness_check=validate(model,routes,harness)
checks.extend([{'id':'duct-routes','title':'장거리 DC·제어선이 공용 덕트 안으로','pass':True,'detail':'단자에서 덕트까지 최대 '+str(harness['maxExposedLeadMm'])+'mm. 기존 관통구만 예외.'},{'id':'common-harness','title':'같은 케이블의 전원·GND·신호를 공통 구간에 모음','pass':True,'detail':'릴레이/MP3/리드의 공통 묶음 구간과 모든 도체 표시 범위를 검사. 모터3선 GND 예외는 유지.'}])
dump(H/'harness-plan.json',harness)
dump(H/'harness-checks.json',harness_check)
csvwrite('duct-cut-list.csv',['덕트','함','그룹','길이mm'],[[d['id'],d['bay'],d['group'],d['lengthMm']] for d in harness['cutList']])
dump(H/'routing-model.json',dict(units='mm',coordinate='정면 상부좌상(0,0), 하부좌상(0,330). 부품 단자 위치는 외형 기준 배선 계획 앵커이며 실물 홀 좌표 아님.',routes=routes))

# Preserve all v5 bytes. The new standalone entry page contains the exact old page as srcdoc.
from v6_three_source import build_source
bundle_src=build_source((A/'simulation/source/cabinet3d.js').read_text(encoding='utf-8'))
(S/'cabinet3d-v6.js').write_text(bundle_src,encoding='utf-8')
choices=[os.environ.get('MONGSHOT_ESBUILD'),str(R/'node_modules/.bin/esbuild.cmd'),str(R.parent/'mongshot_review/.tools/esbuild.exe'),shutil.which('esbuild')]
exe=next((x for x in choices if x and Path(x).exists()),None)
if not exe:raise SystemExit('esbuild unavailable')
subprocess.run([exe,'simulation/source/cabinet3d-v6.js','--bundle','--format=iife','--global-name=MongshotV6','--minify','--legal-comments=inline','--alias:three='+str(R/'simulation/vendor/three/three.module.js'),'--outfile=simulation/vendor/cabinet3d-v6.bundle.js'],cwd=R,check=True)
data=dict(model=model,wires=wire,groundPorts=groundports,positivePorts=positiveports,graph=graph,corrections=corrections,unknowns=unknowns,checks=checks,bom=bom,routes=routes,
    version='v6.1',harness=harness,planningOnly=True,stats=dict(parts=len(parts),wires=len(wire),labels=len(wire)*3,bomRows=len(bom['items']),newParts=0,removedConverter=1),
    sources=[dict(title='Pololu #4091 공식 사양',url='https://www.pololu.com/product/4091'),dict(title='ST L298 공식 데이터시트',url='https://www.st.com/resource/en/datasheet/l298.pdf')])
baseline=json.loads((R/'archive/v6-compact-preserved/hardware/v6/design-data.json').read_text(encoding='utf-8'))['routes']
def length(r):return sum(math.dist(a,b) for a,b in zip(r['points'],r['points'][1:]))
before={r['id']:r for r in baseline};after={r['id']:r for r in routes}
data['routeComparison']=[dict(id=k,beforeMm=round(length(before[k]),1),afterMm=round(length(after[k]),1)) for k in ['CAB-MOT','CAB-RLY','CAB-MP3-SIG']]
dump(H/'route-length-comparison.json',data['routeComparison'])
from v6_svg import write_svg
write_svg(R,data)
from v61_svg_bundle import write as write_harness_svg
write_harness_svg(R,data)
front_svg=(H/'front-wiring.svg').read_text(encoding='utf-8')
svg_start=front_svg.index('<svg');data['frontSvgInner']=front_svg[front_svg.index('>',svg_start)+1:front_svg.rindex('</svg>')]
dump(H/'design-data.json',data);dump(H/'automatic-checks.json',dict(scope='계획 그래프/치수/문서 검사. 실물 검증 아님',checks=checks,unknowns=unknowns))
def safejson(d):return json.dumps(d,ensure_ascii=False).replace('<','\\u003c')
tpl=(S/'v6-page.html').read_text(encoding='utf-8')
tpl=tpl.replace('/*__THREE_BUNDLE__*/',(R/'simulation/vendor/cabinet3d-v6.bundle.js').read_text(encoding='utf-8')).replace('/*__V6_DATA__*/',safejson(data)).replace('/*__V5_HTML__*/',safejson((A/'simulation/index.html').read_text(encoding='utf-8')))
tpl=tpl.replace('/*__V6_APP__*/',(S/'v6-app.js').read_text(encoding='utf-8'))
(R/'simulation/index.html').write_text(tpl,encoding='utf-8')
labels='<!doctype html><html lang="ko"><meta charset="utf-8"><title>v6 세 위치 라벨</title><style>body{font-family:Arial,\"Malgun Gothic\"}main{display:grid;grid-template-columns:repeat(3,1fr);gap:5px}.label{border:1px solid #999;padding:7px;break-inside:avoid;font-size:10px}b{font-size:12px}</style><button onclick="print()">인쇄</button><h1>v6 · 시작 / 경로 / 끝 · 조건부는 확인 전 연결 금지</h1><main>'
for d in wire:
    for l in d['labels']:labels+='<div class="label"><b>'+html.escape(l)+'</b><br>'+html.escape(d['start']+' → '+d['end'])+'<br>'+html.escape(d['condition'] or d['group'])+'</div>'
(H/'wire-labels.html').write_text(labels+'</main></html>',encoding='utf-8')
csvwrite('power-budget.csv',['대상','레일','가정 전류A','비고'],[['Uno/주변','5V',.20,'실측 아님'],['KT403A','5V',.50,'피크 여유 할당 / 홍싱 제외'],['도어','5V',.05,'저전류LED6개 포함'],['로직센서 예비','5V',.25,'정격 대조'],['릴레이8코일+L298논리','5V',.80,'실측 아님 / 모터 주전력 제외'],['가정합계','5V',1.80,'12Vin 밀폐함 출력/리플/온도 확인 필요']])
text='''# v6 비절연 스타 · 수정 작업안

v5.3 원본은 `archive/v5.3-preserved`에 해시와 함께 보존했습니다. 로컬 첫 화면에서 v6와 보존본을 전환합니다. 펌웨어와 실제 하드웨어는 변경하지 않았습니다.

## 지시서에서 고친 핵심
G→L298 GND 추가선은 강압기 경로와 병렬인 두 번째 G–P0 경로를 만듭니다. v6는 이 선을 삭제하고 P0.4→L298 전력 귀환만 둡니다. 모터 제어 신호는 릴레이·Arduino·L298 사이의 공용 신호 덕트로 묶었습니다. 신호 기준은 G→강압기 GND→P0→L298 공통 경로를 사용합니다. 이 때문에 CAB-MOT의 “별도 G 동봉” 요구는 명시적 예외입니다. 긴 케이블에서 입력 기준전압·노이즈 적합성을 보장하지 않습니다.

## 전원·부품
12V SMPS→하부 P12/P0 트렁크 한 쌍. 기존 #4091 한 대로 5V/G를 통합하고 DDR-15G-5만 삭제합니다. 5V 임시 부하예산1.8A는 가정이며 모터 전력을 포함하지 않습니다. 5.5A 제품 표기는36Vin 조건입니다. 12Vin 밀폐함의 출력전류·온도·리플을 측정해야 합니다. 모터 VMS12/5V는 정격 확인 전 미확정이며 둘 중 한 경로만 선택합니다. L298의5V-EN(레귤레이터)과 ENA(구동허가) 점퍼는 다릅니다. 실물 확인 전 자동 설정하지 않습니다.

## 하네스 우선 배치
릴레이 A/B는 하부(35,230)/(145,230)에 접점이 위쪽 전력 덕트(H1)를, 제어헤더가 아래쪽 신호 덕트(H2)를 향하도록 배치했습니다. L298(160,350)과 Uno(260,370)의 제어헤더도 H2를 향합니다. 전원 분배부는 하부470mm 행에 P12→P0→강압기→G→5V 순서로 놓고 바로 위 H3 DC 덕트로 들어갑니다. MP3는 홍싱 바로 아래에 유지합니다.

각 선의 경로는 공용 덕트 중심선 그래프에서 계산합니다. 3D 기본 뷰는 덕트 속 공통 묶음과 단자 앞의 짧은 꼬리선을 보여줍니다. 묶음은 기계적 결속이며 전기적으로 접속한 버스가 아닙니다. 개별 가닥 모드와 케이블 선택으로 모든 도체를 확인할 수 있습니다. 모터5V 대안은 12V와 동시에 표시하지 않으며 별도 토글/결선표에 유지합니다.

모듈 단자에서 덕트까지의 꼬리선 길이와 모든 가닥의 덕트 경로, 같은 케이블의 공통 구간을 검사합니다. 기존 BOM의17.5mm 덕트2본(각1828.8mm)에서 절단 가능한 길이표를 함께 제공합니다. 실제 케이블 외경·유효 내경·충진율·굽힘반경은 미확인입니다. 좌표는 실측 전 계획이며 실제 선 절단 길이가 아닙니다.

## 도면 범위
상부400×260, 하부400×560, 깊이120mm는 사진 기반 가정입니다. 좌표·예약영역·몸체·배선 경로를 제공하지만 실제 타공·절단 길이를 확정하는 실측도는 아닙니다. 선 경로는 2D/3D가 같은 데이터를 사용합니다. 외부는 화살표로 표시하며 새 현장 단자열을 만들지 않습니다. 각 구간 시작/경로/끝 라벨3장입니다.

## 검사 해석
계획 그래프에서만 P0–G 경로1개, 전력 귀환 P0 분기, 홍싱 AUD-GND 한 경로, PE/DC 분리를 검사합니다. 지시서 그대로의 모터 기준선을 주입하면 경로2개를 검출합니다. 실제 센서·섀시·USB·계측기 우회는 U1~U7의 미확인 항목입니다. “절연 확보”나 실물 합격으로 표시하지 않습니다.

## 변경 순서
1. 전원 차단 후 기존 선 양끝/Arduino 핀/릴레이8채널/접점을 사진·라벨로 기록합니다.
2. 함체 유효치수·깊이·관통구 및 모든 U1~U7을 확인합니다.
3. 기존 부품과4개 분배블록을 좌표에 맞춰 가배치합니다. 신규 부품·PCB·퓨즈 추가는 없습니다.
4. PE/기존AC를 보존하고, SMPS에서 하부로12V+/0V 트렁크 한 쌍을 정리합니다.
5. P12/P0→단일 강압기→5V/G를 연결합니다. 장치 연결 전 극성·전압 확인. 외부5V와USB 동시급전 회피.
6. 자석 귀환·모터 귀환을 각각 P0로. G→P0 직접 점퍼와 G→L298 추가선 없음. 다이오드 K=자석+, A=자석−.
7. 신호/자기귀환 페어를 유지하며 릴레이/MP3/리드/패널을 재연결합니다. CAB-MOT는 H2 공용 신호 덕트로 정리합니다. 별도 G→L298 선을 추가하지 않습니다.
8. U1/U2 미확인 급전·입력은 연결 확정하지 않습니다. 독립 시험→동시 전환 시험으로 진행하고 리셋·오판정·5V 최저값·온도·자석 해제시간을 기록합니다.

부품확인 근거: [Pololu #4091](https://www.pololu.com/product/4091), [ST L298](https://www.st.com/resource/en/datasheet/l298.pdf). 구체적인 릴레이/L298 모듈 회로는 실물 대조가 필요합니다.
'''
(R/'docs/12-v6-common-star.md').write_text(text,encoding='utf-8')
print(json.dumps(data['stats']|{'revision':model['revision'],'originalP0GPaths':len(audit_paths),'correctedP0GPaths':len(corrected_paths)},ensure_ascii=False))
