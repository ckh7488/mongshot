"""One authoritative set of actual endpoint/route/ground installation records."""
from pathlib import Path
import csv,json,html
ROOT=Path(__file__).resolve().parents[1];hw=ROOT/'hardware'
rows=[]
def add(label,start,end,via,route,kind,note=''):
 rows.append([label,start,end,via,route,kind,note,''])
def write(name,heads,data):
 if name in ['relay-channel-trace.csv','commissioning-checklist.csv','final-rating-record.csv'] and (hw/name).exists():return
 with (hw/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(heads);w.writerows(data)

# Standard labels remain aligned with the rendered GPIO correspondence view.
with (hw/'pin-and-wire-labels.csv').open(encoding='utf-8-sig') as f:pins=list(csv.reader(f))[1:]
for label,term,start,end,net in pins:
 if label.startswith('MAG') or label.startswith('WIN'):continue
 if label.startswith('0VL-'):
  port={'FRAME':2,'LIGHT':3,'KEY':4,'RFID':5,'BOOK':6}[label[4:]]
  start=f'0V-L.{port}';note='RFID 출력이 전압형일 때만 해당 REF. 접점/절연형은 인터페이스에 맞게 미접속 처리.' if port==5 else '센서 S와 이 0V를 한 쌍으로 회수; 리드스위치는 Vcc 불필요'
 elif label=='PANEL-0V':start='0V-L.10';note='J7.2; 도어 595·버튼 음극 기준'
 elif label=='PANEL-5V':start='5V-DIST PANEL+';note='J7.1; 595 VCC/LED, 각 LED 1kΩ'
 elif label.startswith('OUT-'):note='A 채널 묶음은 조건부. 기존 A/B 모든 채널의 양 끝 실선 추적 후 적용'
 elif label=='IN-D6':note='직렬 100Ω 보존'
 elif label.startswith('PANEL-') or label=='BTN-NEXT':note='구 D11 Gun/A3 Hint 선을 먼저 분리; 595/버튼 회로 참조'
 else:note='센서 출력 전압을 측정; 12V 출력은 Arduino 직접 입력 금지' if label.startswith('IN-') else '기존 신호 방향 보존'
 route='하부: 왼쪽 신호 덕트 → Arduino/단자' if label.startswith(('IN-','0VL-')) else '하부: J7 → 문 힌지 쪽 여유 루프' if label.startswith(('PANEL-','BTN-')) else '하부: 수평 제어 덕트'
 add(label,start,end,term,route,'신호/로직',note)

add('MAIN12+','SMPS V+','FU0 IN','주 DC 홀더 입력','상부 내부','주 전력','단자 커버; FU0·버스·전선 정격은 실부하와 보호협조로 선정')
add('MAIN12-DIST','FU0 OUT','+12V-DIST.IN','주 DC 홀더 출력','상부 내부','주 전력','PTFIX RD 입력, 홀더 리드/접속부 굽힘 여유 포함')
add('MAIN0V','SMPS V−','0V-PWR.IN','단일 주 음극선','상부 내부','주 귀환','입력에 제조사가 허용하지 않는 복수선을 한 구멍에 밀어 넣지 않음')
for n in range(1,8):add(f'F{n}-IN',f'+12V-DIST.{n}',f'F{n} IN','퓨즈 입력 단자','상부 내부','12V 분기','RFID F7은 12V 공용 급전 확인 때만 사용' if n==7 else '각 입력에 개별 분배선; 정격 불명의 공통 점퍼를 만들지 않음')
for n,name,pin in [(1,'몰딩','D12'),(2,'슬라이드','D10'),(3,'책','D9')]:
 add(f'MAG-COM{n}',f'F{n} OUT',f'RY-A.CH{n}.COM',f'F{n} / X3-M{n} feed','상부→관통 P1→하부 오른쪽','12V 분기','RY-A 채널 번호는 재배치안; 기존 접점 선택·극성 기록 후 연결')
 add(f'MAG{n}+',f'RY-A.CH{n}.선택 접점',f'{name} 전자석 +',f'X3-M{n}+','하부 오른쪽→현장','12V 스위칭','NO/NC는 원하는 유지/해제·정전 동작과 실측으로 결정; GPIO HIGH와 여자 상태 동일시 금지')
 add(f'MAG{n}-',f'{name} 전자석 −',f'0V-PWR.{n}',f'X3-M{n}-','현장→하부 오른쪽→관통 P1→상부','고전류 귀환','0V-L/Arduino/센서 단자를 경유하지 않음; 서지 억제는 코일 가까이')
add('VMOT+','F4 OUT','L298N Vs','X4.5','상부→관통 P2→하부 오른쪽','모터 전원','모터가 12V 정격일 때. 다른 정격이면 해당 변환/전원 보존')
add('0VMOT-DRV','L298N GND','0V-PWR.4','X4.6','하부 오른쪽→관통 P2→상부','모터 귀환','Arduino에 모터 전류를 통과시키지 않음. 5V/ENA 점퍼는 실물 확인')
add('MOTOR-A','L298N OUT1','액추에이터 A','X4.M1','하부 오른쪽→현장','모터 출력','리미트·방향·부팅 enable HIGH를 무부하 검증')
add('MOTOR-B','L298N OUT2','액추에이터 B','X4.M2','하부 오른쪽→현장','모터 출력','스피커 음극처럼 GND에 연결하지 않음')
add('AUD12+','F5 OUT','HONGXING DC +','X6.1','상부→관통 P2→하부 오른쪽','12V 오디오','센터 + 보존; 오디오 정격 확인')
add('0VAUD-PS','HONGXING DC −','0V-PWR.5','X6.2','하부 오른쪽→관통 P2→상부','오디오 전력 귀환','신호 케이블을 전력 귀환선으로 쓰지 않음; 추가 우회 GND 경로 기록')
add('AUDIO-LINE','KT403A LINE OUT','HONGXING MP3 IN','기존 오디오 커넥터','하부 오디오 구역','오디오 신호','신호 실드/GND의 중복 경로 확인; BTL 스피커 −는 DC GND가 아님')
add('BUCK-IN+','F6 OUT','DC-DC IN+','X0.DC1','상부→관통 L1→하부 왼쪽','12V 로직 원천','큰 부하 묶음과 나눠 고정; 정격 5V 출력과 UVLO/리플 확인')
add('0V-LINK','0V-PWR.7','0V-L.IN','굵은 공통 0V 주 귀환선','상부→관통 L1→하부 로직','로직 원천 귀환','2.5mm² 구리선 + 적합한 페룰을 설계 후보로 사용. 두 분배블록 직결; DC-DC 탈거와 무관하게 기준 유지. 길이/전압강하/단자 범위 대조')
add('F5L-IN','DC-DC VOUT','F5L IN','하부 5V 퓨즈 입력','하부 캐리어 내부','5V 전력','Pololu 전력 패드에 직접 납땜·장력 고정; EN/PG/VRP 미사용')
add('P5-MAIN','F5L OUT','5V-DIST.IN','하부 PTFIX RD 입력','하부 로직 구역 짧게','5V 전력','Arduino/릴레이/MP3/패널을 별도 분기; 출력 전류 합산')
add('0VL-BUCK','0V-L.11','DC-DC GND','IN−/OUT− 공통 노드','하부 캐리어→로직 분배블록 짧게','로직 기준','Pololu의 GND는 공통. 입력/출력용으로 별도 두 경로를 만들지 않고 하나의 짧은 GND 연결로 종단')
for label,end,port in [('0VL-ARD','Arduino GND',1),('0VL-MP3','KT403A GND',7),('0VL-RLY','RY-A 제어 GND',8),('0VL-RLY-B','RY-B 제어 GND',9)]:
 add(label,f'0V-L.{port}',end,'각 전용 포트','하부 로직 구역','로직 귀환','릴레이 VCC/JD-VCC/GND는 실제 보드의 절연/점퍼 구조를 확인')
for label,end,note in [('PWR-ARD-USB','Arduino USB 5V','PC 서비스 연결 시 운영 USB 전원을 분리; 역급전 방지 경로 확인'),('VMP3+','KT403A VCC','모듈 정격 확인 후 5V 분기 적용'),('P5-RLY','RY-A VCC/JD-VCC','코일이 5V일 때. Arduino 핀·온보드 LDO 경유 금지'),('P5-RLY-B','RY-B VCC/JD-VCC','B 보드 기존 회로·실제 코일 전압 보존; 5V 코일인 경우만 이 분기')]:
 add(label,'5V-DIST 전용 분기',end,'하부 5V 분배부','하부 로직 구역','5V/기존 정격',note)
add('RFID-PWR+','F7 OUT (12V 정격인 경우)','RFID 회색함 전원 +','기존 전원 커넥터','상부→관통 조건부→하부','조건부 전력','12V가 아니면 F7 사용 금지; 기존 정격 공급 유지')
add('RFID-PWR-','RFID 회색함 전원 −','0V-PWR.6 (공용 12V인 경우)','기존 전원 커넥터','하부→관통 조건부→상부','조건부 귀환','출력 REF/0VL-RFID와 구별; 접점형 출력이면 불필요한 공통 결합 금지')
add('WIN-C','창문 부하 자체 전원','RY-A.CH4.COM','X3-WIN.C','하부 오른쪽 별도 단자','무전압 접점','Arduino 12V 전원과 임의 합치지 않음')
add('WIN-SW','RY-A.CH4.선택 접점','창문 부하','X3-WIN.SW','하부 오른쪽 별도 단자','무전압 접점','접점 DC/AC 정격과 부하 전압을 실물로 확인')

write('full-wiring-schedule.csv',['양쪽 선 라벨','시작 단자','끝 단자','경유/새 단자','실제 설치 경로','회로 종류','작업 조건','실물 확인/검사자'],rows)

# Field strip landing: 2 x 12 electrically independent PT2.5 terminals.
# X2 and X5 are module/header aliases, not extra field-strip connections.
landings=[
 ('T1.01','X1.1-S','IN-D8'),('T1.02','X1.1-0','0VL-FRAME'),
 ('T1.03','X1.2-S','IN-A0'),('T1.04','X1.2-0','0VL-LIGHT'),
 ('T1.05','X1.3-S','IN-A1'),('T1.06','X1.3-0','0VL-KEY'),
 ('T1.07','X1.4-S','IN-A5'),('T1.08','X1.4-0','0VL-RFID'),
 ('T1.09','X1.5-S','IN-D6'),('T1.10','X1.5-0','0VL-BOOK'),
 ('T1.11','V-SENSOR1','미접속 / 정격 확인 후'),('T1.12','V-SENSOR2','미접속 / 정격 확인 후'),
 ('T2.01','X3-M1+','MAG1+'),('T2.02','X3-M1-','MAG1-'),
 ('T2.03','X3-M2+','MAG2+'),('T2.04','X3-M2-','MAG2-'),
 ('T2.05','X3-M3+','MAG3+'),('T2.06','X3-M3-','MAG3-'),
 ('T2.07','X3-WIN.C','WIN-C'),('T2.08','X3-WIN.SW','WIN-SW'),
 ('T2.09','X4.M1','MOTOR-A'),('T2.10','X4.M2','MOTOR-B'),
 ('T2.11','예비','미접속'),('T2.12','예비','미접속')]
write('field-terminal-landing.csv',['실물 자리','전기적 별칭','회로 라벨'],landings)
write('positive-terminal-schedule.csv',['블록','포트','대상','라벨'],[['+12V-DIST','IN','FU0 OUT','MAIN12-DIST']]+[['+12V-DIST',str(n),f'F{n} IN',f'F{n}-IN'] for n in range(1,8)]+[['5V-DIST','IN','F5L OUT','P5-MAIN'],['5V-DIST','1','Arduino USB 5V','PWR-ARD-USB'],['5V-DIST','2','RY-A VCC/JD-VCC','P5-RLY'],['5V-DIST','3','RY-B VCC/JD-VCC','P5-RLY-B'],['5V-DIST','4','KT403A VCC','VMP3+'],['5V-DIST','5','J7.1 / PANEL 5V','PANEL-5V']])
index={r[2]:r[0] for r in landings if r[2] not in ['미접속','미접속 / 정격 확인 후']}
segments=[]
for row in rows:
 if row[0] in index:
  mid=index[row[0]]+' / '+row[3]
  segments.append([row[0]+'-C',row[1],mid,'함체 안쪽 선',row[4],row[5],row[6],row[0]])
  segments.append([row[0]+'-F',mid,row[2],'현장 쪽 선',row[4],row[5],row[6],row[0]])
 else:segments.append(row[:7]+[row[0]])
write('wire-segments.csv',['새 선 양 끝 라벨','시작 단자','끝 단자','선 구간','설치 경로','회로 종류','작업 조건','기존 회로 ID'],segments)

pwr=[['IN','SMPS V−','MAIN0V'],['1','몰딩 전자석 −','MAG1-'],['2','슬라이드 전자석 −','MAG2-'],['3','책 전자석 −','MAG3-'],['4','L298N GND','0VMOT-DRV'],['5','앰프 전력 −','0VAUD-PS'],['6','RFID 전력 − / 공용 12V일 때만','RFID-PWR-'],['7','하부 0V-L.IN 직접 연결','0V-LINK']]+[[str(i),'미접속 / 예비',''] for i in range(8,13)]
logic=[['IN','상부 0V-PWR.7 / 직접 공통선','0V-LINK'],['1','Arduino GND','0VL-ARD'],['2','액자 리드 0V','0VL-FRAME'],['3','조명 신호 기준','0VL-LIGHT'],['4','열쇠 신호 기준','0VL-KEY'],['5','RFID 출력 REF / 실제 방식 조건부','0VL-RFID'],['6','책 리드 0V','0VL-BOOK'],['7','KT403A GND','0VL-MP3'],['8','릴레이 A 제어 GND','0VL-RLY'],['9','릴레이 B 제어 GND','0VL-RLY-B'],['10','도어 표시·버튼 GND','PANEL-0V'],['11','DC-DC GND (입력/출력 공통)','0VL-BUCK'],['12','TP-L0 측정용 접속점','']]
write('ground-terminal-schedule.csv',['블록','위치','포트','연결 대상','선 라벨'],[['0V-PWR','상부 (10,180)']+r for r in pwr]+[['0V-L','하부 (245,390)']+r for r in logic])
ground_html='<section class="fit-sheet"><h2>분배블록의 각 단자에 무엇을 꽂는가</h2><p>한 블록의 IN 및 1~12는 내부 금속으로 모두 공통입니다. 분배블록 두 개 사이의 전기적 연결은 <b>0V-PWR.7 → 0V-LINK → 0V-L.IN</b> 구조입니다. 일반 단자대라면 제조사 정격 공통 점퍼가 필요합니다.</p><table><thead><tr><th>포트</th><th>상부 0V-PWR</th><th>선 라벨</th><th>하부 0V-L</th><th>선 라벨</th></tr></thead><tbody>'
for up,lo in zip(pwr,logic):ground_html+='<tr>'+''.join('<td>'+html.escape(v)+'</td>' for v in [up[0],up[1],up[2],lo[1],lo[2]])+'</tr>'
ground_html+='</tbody></table><h3>전자석 한 개의 실제 폐회로</h3><p>SMPS V+ → 보호/공통 +12V → F1 → MAG-COM1 → 릴레이 COM/선택 접점 → MAG1+ → 전자석 → MAG1− → 상부 0V-PWR.1 → MAIN0V → SMPS V−.</p><h3>Arduino와 센서의 기준</h3><p>SMPS V+ → F6 → BUCK IN+ / 0V-PWR.7 → 0V-LINK → 0V-L.IN. BUCK OUT+ → 보호된 5V 분배부 → Arduino/센서·패널의 정격 분기. 0V-L.IN → 각 로직·센서의 개별 음극. BUCK 공통 GND는0V-L.11에 한 경로로 연결.</p><p><b>0V-LINK를 지정 주 공통선으로 사용하고 DC-DC GND는 하부 한 곳에 종단합니다.</b> L298N 입력 기준, 오디오 케이블, RFID는 우회 경로가 생길 수 있으므로 그 경로도 기록합니다. 따라서 이 구성은 완전한 단일점 GND나 갈바닉 절연을 보장한다고 표현하지 않습니다.</p></section>'
(ROOT/'simulation/source/ground-table.html').write_text(ground_html,encoding='utf-8')
write('passage-schedule.csv',['묶음','선 라벨','방향','비고'],[['P1',x,'상하','자석 공급/귀환; 신호 묶음과 별도 고정'] for x in ['MAG-COM1','MAG1-','MAG-COM2','MAG2-','MAG-COM3','MAG3-']]+[['P2',x,'상하','모터·앰프 공급/귀환'] for x in ['VMOT+','0VMOT-DRV','AUD12+','0VAUD-PS']]+[['L1',x,'상하','F6→buck VIN / 공통0V 주 귀환선→0V-L.IN'] for x in ['BUCK-IN+','0V-LINK']]+[['조건부',x,'상하','RFID 12V 공용화 확인 시에만'] for x in ['RFID-PWR+','RFID-PWR-']])
channels=[[board,str(ch),'','','','','','',''] for board in ['A','B'] for ch in range(1,5)]
write('relay-channel-trace.csv',['보드','채널','현재 IN 출처','현재 COM 출처','현재 NO 도착','현재 NC 도착','코일 정격/점퍼','LOW/HIGH 접점 결과','재배치 결정/검사자'],channels)

labels=[]
for row in segments:
 term=row[2] if row[0].endswith('-C') else row[1] if row[0].endswith('-F') else row[3]
 for end in ['A','B']:labels.append((row[0],term,end))
page='''<!doctype html><html lang="ko"><meta charset="utf-8"><title>MONG SHOT 양 끝 라벨</title><style>body{font:12px 'Malgun Gothic',Arial;margin:15mm;color:#294b5b}h1{font-size:20px}p{color:#7893a1}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}.label{border:1px solid #bed1db;padding:3mm;min-height:18mm;break-inside:avoid}.name{font:600 12px Consolas,monospace}.terminal{font-size:9px;margin-top:2mm}.end{float:right;color:#a1b7c3}@page{size:A4;margin:10mm}@media print{body{margin:0}.tools{display:none}}</style><div class="tools"><h1>MONG SHOT 양 끝 라벨</h1><p>A/B는 같은 전선의 양 끝입니다. 릴레이 보드 A/B와 구별하세요. 조건부 회로 라벨은 적용 결정 후 사용합니다.</p><button onclick="print()">라벨 인쇄</button><hr></div><div class="grid">'''
for name,term,end in labels:page+=f'<div class="label"><span class="end">{end}</span><div class="name">{html.escape(name)}</div><div class="terminal">{html.escape(term)}</div></div>'
(hw/'wire-labels.html').write_text(page+'</div></html>',encoding='utf-8')
checks=[
 ('1 기록','인입 AC/기존 두 SMPS/어댑터가 담당하는 다른 장치 회로까지 구별'),
 ('1 기록','A/B 릴레이 8채널의 IN/COM/NO/NC·코일전압·극성을 모두 기록'),
 ('1 기록','Arduino 모든 선에 양 끝 라벨; GND는 함께 다 뽑지 말고 회로별 추적'),
 ('1 실측','상하 유효 폭·각 높이·닫힌 문까지 깊이·문 잠금장치 돌출 기록'),
 ('1 실측','RFID 회색함·앰프·커넥터 돌출 실측, 계획 확보 영역에 대조'),
 ('1 실측','관통구 위치/폭/높이·모서리·잔여 케이블·묶음 굽힘·클립 공간 확인'),
 ('2 배치','백플레이트에 실물/실제 크기 종이로 놓아 도어·단자·서비스 공간 확인'),
 ('2 배치','SMPS/DC-DC 제조사 환기 간격·장착 방향·폐함 온도 조건 확인'),
 ('2 기구','절연 스탠드오프·탈착 캐리어·덕트·부싱·상하 클립·힌지 루프 고정'),
 ('3 무전원','0V-L 전 포트 및 각 센서/Arduino GND 연속성 확인'),
 ('3 무전원','0V-PWR 전 포트 및 각 부하 − 연속성 확인'),
 ('3 무전원','DC-DC를 분리해도0V-PWR↔0V-L 직접 공통선 연속성 유지. 자석 귀환은 Arduino 경유 없음'),
 ('3 무전원','PE 보호접지와 0V 구별; 의도치 않은 외함/스크린 결합 조사'),
 ('3 무전원','L298N/오디오/RFID를 통한 우회 GND 경로 기록'),
 ('3 무전원','도어 하네스 5V-0V 단락 없음; 595 OE/SRCLR/100nF/LED 방향 확인'),
 ('4 전원','부하 분리 상태에서 DC-DC 출력 5V 확인 후 Arduino/595 연결'),
 ('4 전원','운영 USB와 PC VBUS 중복 급전 방지 경로 확인'),
 ('4 입력','각 센서 Vcc·출력 방식·비활성/활성 전압·ADC 기록, 12V 직접 입력 없음'),
 ('4 입력','D8/D6 LOW 판정과 책 직렬 100Ω 보존 확인'),
 ('4 입력','기존 D11 Gun/A3 Hint 분리 후 595/버튼 핀 재사용 확인'),
 ('5 표시','6개 LED 액자/조명/열쇠/RFID/책/완료 순서와 단계 점멸 확인'),
 ('5 버튼','짧은 누름 무시·2초 1회 진행·계속 누름 반복 없음·재누름 확인'),
 ('5 버튼','20초/1초/10초 대기 유지, 대기 중 누름이 다음 단계로 예약되지 않음'),
 ('5 출력','무부하로 전원 투입/리셋/코드 업로드 시 릴레이 접점 상태 확인'),
 ('5 모터','Vs/5V/ENA 점퍼·기동/구속 전류·리미트·방향·부팅 HIGH 확인'),
 ('6 부하','자석 3개 정상/기동 전류·접점 DC 정격·퓨즈·전선·서지 억제·해제 시간 확인'),
 ('6 부하','모든 부하 동시 전환 시 Arduino 근처 5V/0V 변동과 오판정 확인'),
 ('6 전체','자동 센서 순서 및 수동 진행을 반복, 실음원/MP3 UART 동작 별도 확인'),
 ('6 전체','닫힌 문 온도 상승·덕트/관통구 마찰·배선 장력·정전/복귀 상태 확인'),
 ('6 인수','탈출/사람 안전과 관련된 부하라면 수동 진행과 별도로 비상 해제 동작 확인')]
write('commissioning-checklist.csv',['단계','검사 항목','결과','측정값/사진','검사자/일시'],[list(x)+['','',''] for x in checks])
ratings=[('CABINET','상/하 유효 폭·높이·깊이 / 관통구 위치·폭·높이'),('RFID','몸체·커넥터 치수 / 정격 V/A / 출력 타입 / 전원−와 REF 관계'),('MAIN12','SMPS 모델 / 연속 전류 / 최대 동시부하 / 모터 기동 / 온도 디레이팅'),('FUSES','FU0·F1~F7·F5L 정격/차단 용량 / 전선 허용전류 / DC 접점 정격'),('5V','DC-DC 모델 / 정격·부하전류 / 최저 입력 / 과도·리플 / 온도'),('RELAYS','A/B 8채널 극성·코일 V/A·점퍼·NO/NC·리셋 접점 상태'),('MOTOR','정격 V/A / 기동·구속 전류 / L298N 손실·방열 / 리미트'),('SENSORS','각 Vcc / 출력 타입 / 활성·비활성 V / ADC'),('MAGNETS','3개 전류 / 억제 소자 / 해제 시간 / 정전 동작'),('AUDIO','앰프 치수 / 12V 전류 / MP3 정격 / 오디오 GND 경로'),('PE','인입·SMPS·외함·문 접지 경로 / DC-PE 결합 여부'),('PANEL','595·LED 전류 / 5V 전압 / 버튼 필터 / 도어 하네스 길이')]
write('final-rating-record.csv',['ID','기입할 실물 값','측정값/사진','검사자'],[list(x)+['',''] for x in ratings])

ground={'status':'proposed two-bay single-SMPS routing; no actual installation measurements',
 'nodes':['0VL','0VPWR','ARD_GND','SENSOR_GND','MP3_GND','RELAY_A_GND','RELAY_B_GND','PANEL_GND','L298_GND','MAG1_NEG','MAG2_NEG','MAG3_NEG','AMP_NEG','SMPS_NEG','BUCK_IN_NEG','BUCK_OUT_NEG'],
 'dc_connections':[['0VPWR','SMPS_NEG'],['0VPWR','MAG1_NEG'],['0VPWR','MAG2_NEG'],['0VPWR','MAG3_NEG'],['0VPWR','L298_GND'],['0VPWR','AMP_NEG'],['0VPWR','0VL'],['0VL','BUCK_IN_NEG'],['BUCK_IN_NEG','BUCK_OUT_NEG'],['0VL','ARD_GND'],['0VL','SENSOR_GND'],['0VL','MP3_GND'],['0VL','RELAY_A_GND'],['0VL','RELAY_B_GND'],['0VL','PANEL_GND']],
 'locations':{'0VPWR':'upper (10,180)','0VL':'lower (245,390)','BUCK':'lower (145,390)'},
 'conditional':['RFID power negative to 0VPWR only if shared12V','RFID REF to0VL only for compatible voltage output','audio/L298/RFID may introduce parallel signal ground paths'],
 'isolated_supplies':{},'pe_rule':'PE is chassis protection, not signal return','main_supply':'one12V main + non-isolated5V buck'}
(hw/'ground-connectivity.json').write_text(json.dumps(ground,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'tests/installation-counts.json').write_text(json.dumps({'circuitRows':len(rows),'wireSegments':len(segments),'endLabels':len(labels),'commissioningChecks':len(checks),'relayChannelsToTrace':8},indent=2),encoding='utf-8')
print(len(rows),'circuits /',len(segments),'new wire segments /',len(labels),'end labels /',len(checks),'commissioning checks')
