from pathlib import Path
import csv,html,json
ROOT=Path(__file__).resolve().parents[1]
hw=ROOT/'hardware'
with (hw/'pin-and-wire-labels.csv').open(encoding='utf-8-sig') as f:
    pinrows=list(csv.reader(f))
rows=[row[:4]+['制御信号'.replace('制御信号','제어 신호') if row[0].startswith(('IN-','OUT-','MOT-','MP3-')) else '귀환/부하','', ''] for row in pinrows[1:]]
rows.extend([
 ['PWR-ARD-USB','X0.1','DC-DC 5V OUT+ / USB 급전','Arduino USB','급전 케이블','USB 급전과 PC VBUS 충돌 방지',''],
 ['P5-RLY','X2.5','5V 로직 보호 분기','RY-A VCC/코일 전원','로직 5V','코일은 Arduino에서 공급하지 않음',''],
 ['0VL-RLY','X2.6','0V-L BUS','RY-A GND','로직 0V','접점측 0V-MAG와 구별',''],
 ['VMP3+','X5.3','모듈 정격 전원 분기','KT403A VCC','로직 전원','실제 모듈 정격 유지',''],
 ['0VL-MP3','X5.4','0V-L BUS','KT403A GND','로직 0V','오디오 GND의 우회 경로 포함',''],
 ['0VL-ARD','X0.2','0V-L BUS','Arduino GND','로직 기준','급전/PCB 기준 경로와 함께 관리',''],
 ['VMOT+','X4.5','12V 모터 정격 분기(필요 시 변환)','L298N Vs','모터 전력','모터 정격 전압 유지',''],
 ['0VMOT-DRV','X4.6','0V-PWR 분배블록','L298N GND','모터 귀환','모터 전류 전용 굵은 귀환',''],
 ['0VMOT-PS','X4.7','SMPS V−','0V-PWR 분배블록','모터 귀환','Arduino 경유 금지',''],
 ['BUCK-IN-','X0.DC2','0V-PWR 분배블록','DC-DC IN−','공통 기준','비절연형 IN−/OUT− 내부 공통, 별도 결합점 추가 안 함',''],
 ['MOTOR-A','X4.M1','L298N OUT1','리니어 모터 A','모터 출력','리미트/방향 기존 상태 보존',''],
 ['MOTOR-B','X4.M2','L298N OUT2','리니어 모터 B','모터 출력','리미트/방향 기존 상태 보존',''],
 ['MAG12+','X3.P+','SMPS +12V / 자석 보호 분기','F1/F2/F3 입력 분배','전자석 전력','개별 퓨즈 후 각각 COM으로',''],
 ['0VMAG-PS','X3.P−','SMPS V−','0V-PWR 분배블록','전자석 귀환','로직과 동일 전위; 부하 귀환은 PWR로 직접',''],
 ['MAG-COM1','RY-A.1.COM','F1 출력','RY-A CH1 COM','전자석 전력','선택 접점은 무부하 동작 확인 후 결정',''],
 ['MAG-COM2','RY-A.2.COM','F2 출력','RY-A CH2 COM','전자석 전력','선택 접점은 무부하 동작 확인 후 결정',''],
 ['MAG-COM3','RY-A.3.COM','F3 출력','RY-A CH3 COM','전자석 전력','선택 접점은 무부하 동작 확인 후 결정',''],
 ['AUD12+','X6.1','SMPS 12V / 오디오 보호 분기','HONGXING DC +','오디오 전원','PS-MAG와 공유하지 않음',''],
 ['0VAUD-PS','X6.2','0V-PWR 분배블록','HONGXING DC −','오디오 귀환','신호 GND 결합 확인; 임의 추가 결합 금지',''],
 ['AUDIO-LINE','X6.AUDIO','KT403A LINE OUT','HONGXING MP3 IN','오디오 케이블','신호 GND 경로 존재 가능',''],
])
header=['양쪽 선 라벨','새 단자','출발','도착','도메인/기능','설계 메모','현장 확인/측정값']
with (hw/'full-wiring-schedule.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(header);w.writerows(rows)

rows.extend([
 ['P5-RLY-B','X2.B+','릴레이 정격 5V 분기','RY-B VCC/코일','릴레이 기존 회로 보존','모듈 정격/기존 연결 확인 후 적용',''],
 ['0VL-RLY-B','X2.B-','0V-L 분배블록','RY-B GND','로직 0V','기존 연결 보존, 예비/미접속으로 단정하지 않음',''],
 ['BUCK-IN+','X0.DC1','12V / DC-DC 보호 분기','DC-DC IN+','5V 생성','5V 전용 SMPS를 고르면 이 분기 대신 별도 5V 급전','']
])
# Refresh with the added B-board / DC-DC rows.
with (hw/'full-wiring-schedule.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(header);w.writerows(rows)

# Two copies per cable: one label at each end. Print uses ordinary HTML/CSS.
labels=[]
for row in rows:
    for end in ['A','B']:labels.append((row[0],row[1],end))
page='''<!doctype html><html lang="ko"><meta charset="utf-8"><title>MONG SHOT 양 끝 선 라벨</title><style>
body{font:12px 'Malgun Gothic',Arial;margin:15mm;color:#243c47}h1{font-size:20px;margin:0 0 7px}p{font-size:11px;color:#71848f}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}.label{border:1px solid #c3d2d8;padding:3mm;height:15mm;box-sizing:border-box;break-inside:avoid}.name{font:600 12px Consolas,monospace}.terminal{font-size:9px;margin-top:2mm;color:#728894}.end{float:right;color:#a4b3ba}@page{size:A4;margin:10mm}@media print{body{margin:0}.tools{display:none}}
</style><div class="tools"><h1>MONG SHOT · 양 끝 선 라벨</h1><p>A/B는 동일 회로의 두 끝입니다. 라벨명은 같게 붙이고 새 단자번호를 대응표와 대조합니다.</p><button onclick="print()">라벨 인쇄</button><hr></div><div class="grid">'''
for name,terminal,end in labels:page+=f'<div class="label"><span class="end">{end}</span><div class="name">{html.escape(name)}</div><div class="terminal">{html.escape(terminal)}</div></div>'
page+='</div></html>'
(hw/'wire-labels.html').write_text(page,encoding='utf-8')
checks=[
 ('1 라벨','Arduino 입력 5개와 각 상대 단자 양 끝 라벨 일치'),('1 라벨','Arduino 출력·모터·MP3 양 끝 라벨 일치'),('1 라벨','GND 각 회로와 짝지어 식별'),('1 라벨','전원·릴레이 IN/COM/NO/NC·오디오 배선 사진 보존'),
 ('2 기구','모듈 고정·덕트·커넥터 접근·스트레인 릴리프 확보'),('2 기구','AC 완제품 구역과 저압 구역 분리'),
 ('3 무전원','0V-L 점퍼 단자와 센서/Arduino 기준 연속성'),('3 무전원','0V-PWR와 0V-L은 비절연 DC-DC를 통해 공통임을 확인'),('3 무전원','모터/전자석 전력 귀환이 센서/Arduino GND선을 경유하지 않음'),('3 무전원','DC-DC IN−/OUT− 공통 경로와 오디오/RFID 우회 GND 기록'),('3 무전원','창문 회로가 독립 접점이며 12V를 정격 확인 없이 인가하지 않음'),
 ('4 로직','Arduino 5V/부팅 로그 정상'),('4 로직','D8/D6 정상·감지 LOW와 직렬 100Ω 확인'),('4 로직','A0/A1/A5 비활성/활성 전압과 raw ADC 기록'),('4 로직','D11/D17 제거 후 기존 부하선 정리'),
 ('5 릴레이','각 채널 IN LOW/HIGH·코일·COM-NO/NC 결과 기록'),('5 릴레이','원본 부팅 GPIO에 따른 목표 부하 상태 확인'),('5 모터','L298N 5V/ENA 점퍼와 전원 정격 확인'),('5 모터','부팅 모터 상태·회전방향·리미트·정지전류 확인'),('5 모터','모터 전류가 로직/센서 GND로 귀환하지 않음'),
 ('6 부하','전자석 각 분기 전류·전압·퓨즈/서지 억제 정격 기록'),('6 부하','앰프/모터/전자석 전환 때 5V·센서 raw·재부팅 확인'),('6 전체','액자→조명3회→열쇠→RFID→책 완료'),('6 전체','리셋·전원 재인가·반복 실행 통과'),('6 전체','문 잠금 용도인 부하의 비상해제·정전 상태 확인(해당 시)')]
with (hw/'commissioning-checklist.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['단계','검사 항목','판정(통과/실패/해당없음)','측정값/증거','담당/일시']);w.writerows([list(row)+['','',''] for row in checks])
ratings=[('5V-RAIL','DC-DC 기본안 / 별도 SMPS 대안','정격 A / 최대 동시 부하 A / Arduino 급전 경로'),('MAIN12','메인 12V SMPS','정격 A / 총 동시부하·기동 / 각 자석 A'),('AUDIO12','앰프 12V 분기','정격 A / 오디오 신호 GND 결합 경로'),('MOTOR-V','모터 정격 분기','정격 V/A / 기동·정지 전류 / L298N 점퍼'),('SENSOR','A0/A1/A5','각 센서 Vcc/출력 방식/활성·비활성 V/ADC'),('RY-A','4채널','Active LOW/HIGH / COM-NO/NC / 부팅 상태 / 접점 DC 정격'),('PROTECTION','F1/F2/F3 / 억제기','부하·전선 기준 퓨즈 / TVS·다이오드 정격 / 해제시간'),('WINDOW','독립 접점 부하','기존 전압/전류/접점 기능'),('CABINET','RFID 회색함 포함 실측 후 선정','부품 실측 / 발열·배선 공간 / 최종 외함 규격')]
with (hw/'final-rating-record.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['ID','구성','최종 정격에 필요한 기록','실물 값/문서','판정']);w.writerows([list(row)+['',''] for row in ratings])

# Connectivity model of the PROPOSED system, not a measured installation.
ground={'status':'proposed single-SMPS non-isolated target; actual interfaces require verification',
 'nodes':['0VL','0VPWR','ARD_GND','SENSOR_GND','MP3_GND','RELAY_A_GND','RELAY_B_GND','PANEL_GND','L298_GND','MAG1_NEG','MAG2_NEG','MAG3_NEG','AMP_NEG','SMPS_NEG','BUCK_IN_NEG','BUCK_OUT_NEG'],
 'dc_connections':[['0VPWR','SMPS_NEG'],['0VPWR','MAG1_NEG'],['0VPWR','MAG2_NEG'],['0VPWR','MAG3_NEG'],['0VPWR','L298_GND'],['0VPWR','AMP_NEG'],['0VPWR','BUCK_IN_NEG'],['BUCK_IN_NEG','BUCK_OUT_NEG'],['BUCK_OUT_NEG','0VL'],['0VL','ARD_GND'],['0VL','SENSOR_GND'],['0VL','MP3_GND'],['0VL','RELAY_A_GND'],['0VL','RELAY_B_GND'],['0VL','PANEL_GND']],
 'isolated_supplies':{},'main_supply':'12V candidate / one SMPS',
 'five_volt_options':['non-isolated DC-DC basic','separate 5V SMPS alternative; define common signal reference'],
 'audio_rfid_rule':'record actual signal-ground bypass paths; do not infer true isolation',
 'pe_rule':'PE remains chassis protection, not a sensor return'}
(hw/'ground-connectivity.json').write_text(json.dumps(ground,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(rows),'wiring rows,',len(labels),'end labels,',len(checks),'commissioning checks')
