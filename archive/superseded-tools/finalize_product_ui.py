"""One-time source/doc reconciliation after manufacturer-backed part choices."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
for p in [ROOT/'simulation/source/page.html',ROOT/'simulation/source/current-design.html',ROOT/'tools/draw_frontpanel.py',ROOT/'tools/build_installation_records.py',*list((ROOT/'docs').glob('*.md'))]:
 s=p.read_text(encoding='utf-8')
 s=s.replace('10kΩ','4.7kΩ').replace('10k →','4.7k →').replace('외부10k ','외부4.7k ').replace('10k 풀업','4.7k 풀업').replace('10kΩ/1kΩ','4.7kΩ/1kΩ')
 s=s.replace('각 1kΩ','각 1.5kΩ').replace('각1kΩ','각1.5kΩ').replace('LED 6개·1kΩ','LED 6개·1.5kΩ').replace('LED 6개·1k','LED 6개·1.5k')
 s=s.replace('17.5mm형','17.5mm형')
 p.write_text(s,encoding='utf-8')
p=ROOT/'tools/draw_frontpanel.py';s=p.read_text(encoding='utf-8').replace("'1k',10,'#9b875e','middle');p([(824", "'1.5k',10,'#9b875e','middle');p([(824")
p.write_text(s,encoding='utf-8')
p=ROOT/'simulation/source/page.html';s=p.read_text(encoding='utf-8').replace('<button type="button" data-view="fit">','<button type="button" data-view="bom">제품 BOM</button><button type="button" data-view="fit">',1).replace('<div id="fit-drawing" hidden>', '<div id="bom-drawing" hidden>{{BOM_VIEW}}</div><div id="fit-drawing" hidden>',1)
s=s.replace('센서선은 왼쪽, 부하는 오른쪽','신호/부하는 단자군을 구분')
p.write_text(s,encoding='utf-8')
p=ROOT/'simulation/source/app.js';s=p.read_text(encoding='utf-8').replace("const views={new:","const views={bom:['실제 제품 BOM · 제조사/품번/외형','제품 도면과 설치 영역 대조 · 전류/기구/조달 조건을 함께 표시'],new:")
s=s.replace("['fit-drawing','fit'],", "['fit-drawing','fit'],['bom-drawing','bom'],")
s=s.replace("['new','gnd','labels','panel','fit']", "['new','gnd','labels','panel','fit','bom']")
s=s.replace('외부 LED·진행 버튼', '외부 LED·진행 버튼')
s=s.replace("details.power=details.smps;", """details.power=details.smps;
details['field-terminals']={title:'현장 단자 24개 · RFID 옆',desc:'Phoenix PT2.5의 실제 외형을 반영해 두 그룹을 세로로 배치합니다. 일반 단자는 서로 독립이며 GND 블록과 다릅니다.',rows:[['제품','PT 2,5 / 3209510 ×24'],['그룹','신호12 / 부하12'],['위치','하부 (320,20), 75×210 확보'],['마감','D-ST2.5 / CLIPFIX35-5']],note:'센서 S/0V는 짝으로, 자석/모터는 부하군으로 종단합니다. 표의 X1/X3/X4 전기적 이름은 단자실장표의 위치에 대응합니다.',nets:[]};
details['main-fuse']={title:'FU0 · 주 DC 보호',desc:'Littelfuse FHAC0002ZXJ 32V/30A 홀더 후보입니다. 홀더 정격이 곧 장착할 퓨즈 전류는 아닙니다.',rows:[['위치','상부 (285,170)'],['확보','80×75mm / 리드 경로 대조'],['퓨즈','ATO · 실부하/전선 기준 선정']],note:'몸체 치수와 리드 굽힘은 실제 제품/제조사 도면으로 대조합니다. 30A 퓨즈를 무조건 넣으라는 뜻이 아닙니다.',nets:['mag-power']};
details.smps={...details.smps,rows:[['후보','MEAN WELL LRS-200-12'],['외형','215×115×30mm'],['출력 정격','12V17A / 필요용량은 별도 대조'],['5V','Pololu4091 → 5V 분배부']],note:'동시/기동 전류와 폐함 온도·장착 방향을 확인한 뒤 구매 용량을 확정합니다. 사진 속 제품 모델을 식별했다는 뜻은 아닙니다.'};
details.buck={...details.buck,rows:[['후보','Pololu D36V50F5 / #4091'],['몸체','25.4×25.4×9.5mm'],['입력','F6 / 0V-PWR.7'],['출력','F5L / 5V PTFIX RD'],['음극','비절연 / IN·OUT 공통']],note:'캐리어에 변환기·5V 분배블록·F5L을 함께 고정합니다. 입력 12V에서 실제 부하/폐함 온도를 확인하며 5.5A를 모든 조건의 보장값으로 사용하지 않습니다.'};
""")
p.write_text(s,encoding='utf-8')
# Reconcile prose with the final actual-sized terminal carrier.
for p in [ROOT/'README.md',ROOT/'docs/03-cabinet-and-bom.md']:
 s=p.read_text(encoding='utf-8').replace('80×85','90×85')
 s=s.replace('오른쪽 x345 부근에는 별도 좁은 단자 캐리어를 세워 현장 부하/모듈 선을 종단합니다.','RFID 옆 (320,20)의75×210mm 영역에 PT2.5 24개를 두 그룹으로 고정합니다. 커버/엔드 고정을 포함합니다. 오른쪽 수직 덕트는 y240 아래부터 배치합니다.')
 s=s.replace('x370~390','x375~395 (y240 아래)')
 s=s.replace('PDF 재생성에는 `reportlab`과 Windows Malgun Gothic 글꼴이 필요합니다.','PDF 재생성에는 `PyMuPDF`와 Windows Malgun Gothic 글꼴이 필요합니다.')
 if p.name=='README.md':s+='\n제품 품번/공식 외형/수량은 [실제 제품 BOM](docs/08-product-bom.md)과 [BOM CSV](hardware/product-bom.csv)에 있습니다. 단자부·변환기·버튼 저항은 이 제품 선정안에 맞춰 보완했습니다.\n'
 p.write_text(s,encoding='utf-8')
print('Product UI and resistor values reconciled')
