"""One-time reconciliation: a direct copper trunk, independent of the buck PCB."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=[ROOT/'README.md',*list((ROOT/'docs').glob('*.md')),ROOT/'simulation/source/page.html',ROOT/'simulation/source/current-design.html',ROOT/'simulation/source/app.js',ROOT/'tools/build_fit_view.py',ROOT/'tools/build_product_bom.py',ROOT/'tools/build_installation_records.py',ROOT/'tools/draw_two_bay.py']
replacements={
'두 블록은 DC-DC 내부 음극을 통해 전기적으로 공통입니다.':'두 블록은 굵은 0V-LINK 선으로 직접 연결되어 전기적으로 공통입니다.',
'두 블록은 비절연 DC-DC를 통해 전기적으로 공통입니다.':'두 블록은 굵은 0V-LINK 선으로 직접 공통 연결합니다. DC-DC GND는 하부 0V-L.11에 종단합니다.',
'두 블록은 비절연 DC-DC를 통해 전기적으로 공통':'두 블록은 굵은 0V-LINK 선으로 직접 공통',
'비절연 DC-DC 내부로 공통':'굵은 0V-LINK로 직접 공통',
'0V-PWR에 고전류 귀환, 0V-L에 로직·센서 기준 / 두 GND는 전기적으로 공통':'0V-PWR에 부하 귀환 / 0V-L에 신호 기준 / 0V-LINK로 직접 공통 연결',
'DC-DC OUT−를 입력으로 받고':'상부 0V-PWR.7을 굵은 0V-LINK로 입력받고',
"['입력','DC-DC OUT−']":"['입력','0V-PWR.7 → 0V-LINK']",
"['IN−','0V-PWR']":"['GND','0V-L.11']",
"['OUT−','0V-L']":"['0V 기준','IN/OUT 공통 GND 한 경로']",
'비절연 DC-DC를 통해 이미 공통입니다':'직접 0V-LINK를 통해 공통입니다',
'DC-DC를 통해 이미 공통':'직접 0V-LINK로 공통',
'일반 DC-DC의 공통 음극 경로':'0V-LINK 직접 연결',
'IN− = OUT− (공통)':'IN− = OUT− (공통, 0V-L.11 한 곳 종단)',
'2개 사이의 전위는 buck 음극으로 공통.':'2개는 굵은0V-LINK로 직결, buck GND는0V-L.11에 한 경로로 종단.',
'F6 / 0V-PWR.7':'F6 VIN / 0V-L.11 GND',
'DC-DC 입력 귀환을 각각':'하부 로직 공통 귀환을 각각',
'앰프, DC-DC 입력 귀환을 각각':'앰프, 하부 로직 공통선 귀환을 각각',
'0V-PWR.7 → DC-DC IN− → 내부 공통 음극 → OUT− → 0V-L.IN → 센서·Arduino의 각 포트':'0V-PWR.7 → 굵은 0V-LINK → 0V-L.IN → 센서·Arduino의 각 포트',
'별도 점퍼를 추가하지 않아도 내부 음극으로 이미 연결됩니다.':'직접 공통선은 DC-DC를 탈거해도 기준을 유지합니다. DC-DC의 공통 GND는0V-L.11에 한 경로로 종단합니다.',
'DC-DC OUT− / 0VL-MAIN':'상부0V-PWR.7 / 0V-LINK',
'DC-DC IN− |':'하부0V-L.IN / 0V-LINK |',
'TP-L0 측정점 |':'DC-DC GND / 0VL-BUCK |',
'예비 | 예비 |':'예비 | TP-L0 측정점 |',
'하부 DC-DC OUT−를 L.IN에 연결합니다. IN−와OUT−가 공통인 비절연형이므로 추가로 임의 점퍼를 달지 않습니다.':'상부 PWR.7을 굵은0V-LINK로 하부 L.IN에 직접 연결합니다. 하부 DC-DC의 공통 GND는 L.11에 짧은 한 경로로 종단합니다.',
'DC-DC IN+ / IN−':'DC-DC VIN / 0V-LINK',
'상부 F6 / 0V-PWR → 하부 DC-DC 입력':'상부 F6 → DC-DC VIN / 0V-PWR.7 → 0V-L.IN',
'DC-DC IN− = OUT−':'0V-PWR.7 → 0V-LINK → 0V-L.IN',
'<b>DC-DC IN− = OUT−</b> 구조':'<b>굵은0V-LINK 직접 연결</b> 구조',
'0V-PWR.7 → BUCK IN−':'0V-PWR.7 → 0V-LINK → 0V-L.IN',
'BUCK OUT− → 0V-L.IN → 각 로직·센서의 개별 음극':'0V-L.IN → 각 로직·센서의 개별 음극. BUCK 공통 GND는0V-L.11에 한 경로로 연결',
'0V-PWR와 0V-L에 임의로 추가 점퍼를 달지 않습니다.':'0V-LINK를 지정 주 공통선으로 사용하고 DC-DC GND는 하부 한 곳에 종단합니다.',
'DC-DC OUT− → 하부 0V-L':'PWR.7 → 0V-LINK → L.IN',
"['DC-DC','IN−']":"['공통선','0V-PWR.7 → 0V-L.IN']",
"['DC-DC OUT−','0VL-MAIN']":"['상부 0V-PWR.7','0V-LINK']",
"'BUCK−'":"'L.IN'",
"'DC common through non-isolated buck'":"'DC common via direct copper trunk'"
}
for p in files:
 s=p.read_text(encoding='utf-8')
 for old,new in replacements.items():s=s.replace(old,new)
 p.write_text(s,encoding='utf-8')
# Commissioning values are still blank in this review; fix the exact wording only.
p=ROOT/'hardware/commissioning-checklist.csv';s=p.read_text(encoding='utf-8-sig').replace('DC-DC IN−=OUT− 구조 확인. 전자석 귀환이 Arduino 선을 경유하지 않음','DC-DC를 분리해도0V-PWR↔0V-L 직접 공통선 연속성 유지. 자석 귀환은 Arduino 경유 없음');p.write_text(s,encoding='utf-8-sig')
print('Ground-trunk wording/ports reconciled')
