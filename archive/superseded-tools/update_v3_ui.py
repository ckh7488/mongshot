from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'simulation/source'
p=src/'page.html'
s=p.read_text(encoding='utf-8')
s=s.replace('<option value="candidate">합의 변경안 · 10ms</option>','<option value="frontpanel">외부 LED·버튼 추가안</option><option value="candidate">10ms 최소 변경안</option>')
s=s.replace('<section class="workspace">','''<section class="frontpanel-bar" aria-label="외부 진행 표시와 수동 진행">
<div class="frontpanel-caption">외부 진행 표시<small>실제 74HC595 출력</small></div><div class="frontpanel-leds">'''+''.join(f'<div class="front-led"><i id="front-led-{i}"></i><span>{name}</span></div>' for i,name in enumerate(['액자','조명','열쇠','RFID','책','완료']))+'''</div><button type="button" id="manual-next">진행 · 2초 누름</button><span id="manual-state">입력 대기에서 단계 완료</span></section><section class="workspace">''')
s=s.replace('확정 장치 재사용 · 전자석 전원/0V 분리 · 로직 GND 일체화','12V SMPS 1대 + 5V DC-DC · RFID 회색함·릴레이 2장 · 외부 진행 표시')
s=re.sub(r'<div class="domain-notice" id="domain-notice">.*?</div>','<div class="domain-notice" id="domain-notice"><strong>기본안: 12V SMPS + 5V DC-DC</strong> / 0V-PWR에 고전류 귀환, 0V-L에 로직·센서 기준 / 두 GND는 전기적으로 공통</div>',s,flags=re.S)
s=re.sub(r'<section class="design-doc active" id="design-doc">.*?</section>',(src/'current-design.html').read_text(encoding='utf-8'),s,flags=re.S)
s=re.sub(r'<section class="below">.*?</section>','''<section class="below"><article class="detail-box"><h3>기존 HW 보존 + 외부 조작부 추가</h3><p>RFID 큰 회색 제어함 · 릴레이 4ch × 2장 · L298N · KT403A · HONGXING · 기존 센서/부하.</p><p>새 부품: 74HC595N, LED 6개·1kΩ 저항, 진행 버튼, 디바운스 부품, 내부 공통 분배블록. 기존 함수 D11/D17 제거 후 GPIO를 새 용도로 재사용합니다.</p></article><article class="detail-box"><h3>검증 범위</h3><p>원본/10ms안의 시험에 더해, 외부 LED의 실제 595 래치 값·2초 버튼·누름 유지/바운스·타이머 대기·정상 센서 진행을 AVR로 시험했습니다.</p><p>MP3는 API 대역입니다. 실물 전류·전원 노이즈·접점·모터 역학·센서 인터페이스는 현장 검증이 필요합니다. 하드웨어에는 아직 업로드하지 않았습니다.</p></article></section>''',s,flags=re.S)
p.write_text(s,encoding='utf-8')
print('V3 page content installed')
