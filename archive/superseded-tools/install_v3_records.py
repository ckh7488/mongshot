"""One-time content migration; current builders remain the source of truth."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'tools/build_workbench.py'
s=p.read_text(encoding='utf-8')
if "('PANEL-DATA','J7.3'" not in s:
 insert="""
labels.extend([
('PANEL-5V','J7.1','5V 로직 분기','외부 LED 보드 VCC','panel'),
('PANEL-0V','J7.2','0V-L 분배블록','외부 LED/버튼 GND','gnd'),
('PANEL-DATA','J7.3','Arduino D11','74HC595 SER / pin14','panel'),
('PANEL-CLK','J7.4','Arduino D13','74HC595 SRCLK / pin11','panel'),
('PANEL-LATCH','J7.5','Arduino D7','74HC595 RCLK / pin12','panel'),
('BTN-NEXT','J7.6','Arduino A3','진행 버튼 / 2초 누름','panel')
])
import csv
"""
 s=re.sub(r'\n[ \t]*import csv\n','\n'+insert,s,count=1)
p.write_text(s,encoding='utf-8')

p=ROOT/'tools/build_field_records.py'
s=p.read_text(encoding='utf-8')
mapping={
 'PS-L / 운영 5V 급전':'DC-DC 5V OUT+ / USB 급전',
 'PS-L 5V 분기':'5V 로직 보호 분기',
 '0V-MAG BUS':'0V-PWR 분배블록',
 '0V-MOT BUS':'0V-PWR 분배블록',
 'PS-MOT + / 분기 보호':'12V 모터 정격 분기(필요 시 변환)',
 'PS-MOT −':'SMPS V−',
 'PS-MAG +12V':'SMPS +12V / 자석 보호 분기',
 'PS-MAG −':'SMPS V−',
 '기존 PS-A 12V +':'SMPS 12V / 오디오 보호 분기',
 '기존 PS-A −':'0V-PWR 분배블록',
 '0V-L/MOT/오디오/PE와 분리':'로직과 동일 전위; 부하 귀환은 PWR로 직접',
 "['GND-REF','X4.4 / 단일 결합점','0V-L BUS','0V-PWR 분배블록','기준 결합','이 지점 한 곳에서 전기적으로 공통','']":"['BUCK-IN-','X0.DC2','0V-PWR 분배블록','DC-DC IN−','공통 기준','비절연형 IN−/OUT− 내부 공통, 별도 결합점 추가 안 함','']",
 "('3 무전원','0V-MAG가 로직/모터/오디오/PE에 오결선되지 않음')":"('3 무전원','0V-PWR와 0V-L은 비절연 DC-DC를 통해 공통임을 확인')",
 "('3 무전원','PS-MAG 전원과 오디오 경유 우회 결합 없음')":"('3 무전원','모터/전자석 전력 귀환이 센서/Arduino GND선을 경유하지 않음')",
 "('3 무전원','0V-MOT ↔ 0V-L 기준 결합점 식별')":"('3 무전원','DC-DC IN−/OUT− 공통 경로와 오디오/RFID 우회 GND 기록')",
 'PS-MAG 임의 인가 없음':'12V를 정격 확인 없이 인가하지 않음',
 "('PS-L','5V 제어 전원'":"('5V-RAIL','DC-DC 기본안 / 별도 SMPS 대안'",
 "('PS-MAG','전자석 12V 전용'":"('MAIN12','메인 12V SMPS'",
 '정격 A / 절연 출력 문서 / 각 부하 A':'정격 A / 총 동시부하·기동 / 각 자석 A',
 "('PS-A','기존 앰프 12V'":"('AUDIO12','앰프 12V 분기'",
 "('PS-MOT','기존 모터 전원'":"('MOTOR-V','모터 정격 분기'",
 "('CABINET','외함 후보 600×800×200'":"('CABINET','RFID 회색함 포함 실측 후 선정'"
}
for old,new in mapping.items():s=s.replace(old,new)
if "['P5-RLY-B'" not in s:
 s=s.replace("# Two copies per cable", """rows.extend([
 ['P5-RLY-B','X2.B+','릴레이 정격 5V 분기','RY-B VCC/코일','릴레이 기존 회로 보존','모듈 정격/기존 연결 확인 후 적용',''],
 ['0VL-RLY-B','X2.B-','0V-L 분배블록','RY-B GND','로직 0V','기존 연결 보존, 예비/미접속으로 단정하지 않음',''],
 ['BUCK-IN+','X0.DC1','12V / DC-DC 보호 분기','DC-DC IN+','5V 생성','5V 전용 SMPS를 고르면 이 분기 대신 별도 5V 급전','']
])
# Refresh with the added B-board / DC-DC rows.
with (hw/'full-wiring-schedule.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(header);w.writerows(rows)

# Two copies per cable""")
 # The planned topology now has a common DC reference.
 begin=s.index('ground={')
 end=s.index("(hw/'ground-connectivity.json')",begin)
 topology="""ground={'status':'proposed single-SMPS non-isolated target; actual interfaces require verification',
 'nodes':['0VL','0VPWR','ARD_GND','SENSOR_GND','MP3_GND','RELAY_A_GND','RELAY_B_GND','PANEL_GND','L298_GND','MAG1_NEG','MAG2_NEG','MAG3_NEG','AMP_NEG','SMPS_NEG','BUCK_IN_NEG','BUCK_OUT_NEG'],
 'dc_connections':[['0VPWR','SMPS_NEG'],['0VPWR','MAG1_NEG'],['0VPWR','MAG2_NEG'],['0VPWR','MAG3_NEG'],['0VPWR','L298_GND'],['0VPWR','AMP_NEG'],['0VPWR','BUCK_IN_NEG'],['BUCK_IN_NEG','BUCK_OUT_NEG'],['BUCK_OUT_NEG','0VL'],['0VL','ARD_GND'],['0VL','SENSOR_GND'],['0VL','MP3_GND'],['0VL','RELAY_A_GND'],['0VL','RELAY_B_GND'],['0VL','PANEL_GND']],
 'isolated_supplies':{},'main_supply':'12V candidate / one SMPS',
 'five_volt_options':['non-isolated DC-DC basic','separate 5V SMPS alternative; define common signal reference'],
 'audio_rfid_rule':'record actual signal-ground bypass paths; do not infer true isolation',
 'pe_rule':'PE remains chassis protection, not a sensor return'}
"""
 s=s[:begin]+topology+s[end:]
p.write_text(s,encoding='utf-8')
print('V3 wiring/record generators updated')
