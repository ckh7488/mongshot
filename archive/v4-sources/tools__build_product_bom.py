"""Manufacturer-backed candidates. Exact ratings not inferred from photographs."""
from pathlib import Path
import csv,json,html
ROOT=Path(__file__).resolve().parents[1]
pfx='https://www.phoenixcontact.com/en-us/products/'
items=[]
def item(id,name,maker,part,qty,where,size,condition,url,status='제품 선정 / 설치 조건 대조'):
 items.append(dict(id=id,name=name,maker=maker,part=part,qty=qty,location=where,size=size,condition=condition,url=url,status=status))
item('PS1','12V 메인 SMPS','MEAN WELL','LRS-200-12',1,'상부 (70,10)','215×115×30mm','12V17A. 17A가 필요하다고 확정한 값 아님. 동시/기동·온도/장착 방향 대조. 230V 입력 전환 확인.','https://www.meanwell.com/Upload/PDF/LRS-200/LRS-200-SPEC.PDF','용량 조건부 후보')
item('DC1','5V 비절연 buck','Pololu','D36V50F5 / #4091',1,'하부 5V 캐리어','25.4×25.4×9.5mm','VIN/GND/VOUT 사용, EN·PG·VRP 미사용. 굵은 전력선은 PCB 패드에 직접 납땜·고정. 5.5A는 특정조건 전형값이며 12V/폐함 온도에서 별도 확인.','https://www.pololu.com/product/4091','공급 제한 표시 있음 / 조달 확인')
item('GND-P/L','0V 공통 분배블록','Phoenix Contact','PTFIX 6/12X2,5-NS35 BU / 3273090',2,'상부 PWR / 하부 L','28.6×58.1×32.4mm (NS35/7.5)','각 블록 IN+12분기 한 전위. 2개는 굵은0V-LINK로 직결, buck GND는0V-L.11에 한 경로로 종단.','https://www.phoenixcontact.com/ko-kr/products/distribution-block-ptfix-6-12x25-ns35-bu-3273090')
item('POS12/5','+12V/+5V 공통 분배블록','Phoenix Contact','PTFIX 6/12X2,5-NS35 RD / 3273092',2,'상부 퓨즈캐리어 / 하부 5V캐리어','28.6×58.1×32.4mm','서로 다른 전압의 별도 블록이며 서로 연결 금지. 전체/접속점·전선 정격 준수. 12V 블록1~7→F1~F7, 5V 블록은 각 로직 분기.','https://www.phoenixcontact.com/en-fr/products/distribution-block-ptfix-6-12x25-ns35-rd-3273092')
item('FU0','주 DC 퓨즈홀더','Littelfuse','FHAC0002ZXJ',1,'상부 (285,170)','80×75mm 확보; 리드 경로 포함 대조','ATO, 32V/30A 홀더·12AWG 리드. 퓨즈 전류는 별도 선정. 몸체/리드 실제 외곽 확인.','https://www.littelfuse.com/products/fuses-overcurrent-protection/fuse-holders-fuse-blocks-accessories/fuse-holders/in-line-fuse-holders/ato-fhac/fhac0002zxj','홀더 선정 / 퓨즈값 미선정')
item('F1~7/F5L','분기 퓨즈 단자','Phoenix Contact','UT 6-HESI (6,3X32) / 3046401',8,'상부7 / 하부5V1','8.2×57.8×75.6mm (NS35/7.5)','6.3×32퓨즈. 홀더 최대10A이므로 모터 등 분기가 넘으면 제품을 교체해야 함. 8개 중 F7은 RFID12V일 때만 사용.','https://www.phoenixcontact.com/en-gb/products/fuse-terminal-block-ut-6-hesi-63x32-3046401','홀더 선정 / 소자 정격은 실측 후')
item('X1/X3/X4','현장 종단 단자','Phoenix Contact','PT 2,5 / 3209510',24,'하부 (320,20) 두 그룹','각5.2×48.6×36.8mm (NS35/7.5)','회로별 독립. GND 공통블록과 다름. 12개 신호군 +12개 부하군. 공통 점퍼를 넣지 않음.','https://www.phoenixcontact.com/en-sg/products/feed-through-terminal-block-pt-25-3209510')
item('XCOV','현장단자 끝 커버','Phoenix Contact','D-ST 2,5 / 3030417',2,'PT2.5 각 그룹 끝','폭2.2mm','PT2.5에 맞는 제조사 커버. 개방 측면을 마감.','https://www.phoenixcontact.com/en-us/products/end-cover-d-st-25-3030417')
item('END','DIN 엔드 고정','Phoenix Contact','CLIPFIX 35-5 / 3022276',10,'현장2군/퓨즈2군/PE군 양 끝','폭5.15mm; 제조사 실제 외형 대조','필수8개 + PE군2개. 분배블록은 자체DIN 고정 사용.','https://www.phoenixcontact.com/en-us/products/end-block-clipfix-35-5-3022276')
item('PE','보호접지 단자','Phoenix Contact','PT 2,5-PE / 3209536',3,'상부 PE 구역','5.2×48.6×36.8mm급','인입/SMPS/외함·문 접지 분기. PE는 레일과 전기 연결되므로 DC 0V 대용 금지.','https://www.phoenixcontact.com/en-ca/products/ground-terminal-block-pt-25-pe-3209536')
item('DUCT','덕트 본체','Panduit','G.5X1LG6',2,'상하 배선 경로','외형 폭17.5×높이26.9mm / 길이1.8288m','호칭0.5인치와 외폭은 다름. 계획20mm 채널에 대조. 실제 선 외경·충전량은 현장 검토.','https://www.panduit.com/content/dam/panduit/en/products/media/4/34/334/2334/74122334.pdf')
item('DUCT-C','덕트 커버','Panduit','C.5LG6',2,'위 덕트 전 길이','본체와 별매 / 길이1.8288m','덕트 높이26.9mm는 커버 포함. 실제 절단 길이 합과 여유를 대조.','https://www.panduit.com/content/dam/panduit/en/products/media/4/34/334/2334/74122334.pdf')
item('U1','LED 직렬 출력 IC','Texas Instruments','SN74HC595N',1,'도어 PCB','PDIP16','5V, QA~QF 사용. /OE=0V, /SRCLR=5V. 595 옆100nF.','https://www.ti.com/lit/ds/symlink/sn74hc595.pdf')
item('LED1~6','저전류 녹색 LED','Kingbright','WP7113LGD',6,'도어 2행×3열','5mm 관통형','2mA 특성 제품. 각 LED1.5kΩ, 음극0V-L. 12V 패널 램프로 치환 금지.','https://www.kingbrightusa.com/product.asp?catalog_name=LED&product_id=WP7113LGD')
item('SW1','진행 순간 버튼','OMRON','A16-TAM-1',1,'하부 도어 (40,270) 표시판','16mm형 / 패널 뒤28.5mm급, 단자 여유 별도','비조광·청색·momentary SPDT의 COM/NO만 사용. 최소1mA@5V이므로 외부4.7k 풀업 적용.','https://www.ia.omron.com/product/item/13731/')
item('RLED','LED 저항','YAGEO','MFR-25FBF52-1K5',6,'도어 PCB','6.3×Ø2.4mm급','1.5kΩ,1%,0.25W. 포장 대체는 동일 전기/기구 사양으로만.','https://yageogroup.com/content/Resource%20Library/Datasheet/YAGEO-MFR_DATASHEET.pdf')
item('RPULL','버튼 풀업','YAGEO','MFR-25FBF52-4K7',1,'도어 PCB','6.3×Ø2.4mm급','4.7kΩ,1%,0.25W. 약1.06mA@5V를 접점으로 공급.','https://yageogroup.com/content/Resource%20Library/Datasheet/YAGEO-MFR_DATASHEET.pdf')
item('RSER','버튼 직렬 저항','YAGEO','MFR-25FBF52-1K',1,'A3 입력 경로','6.3×Ø2.4mm급','1kΩ,1%,0.25W. LED 저항1.5k와 구별.','https://yageogroup.com/content/Resource%20Library/Datasheet/YAGEO-MFR_DATASHEET.pdf')
item('C1/C2','필터/디커플링','KEMET','C315C104K5R5TA',2,'595 옆 / 버튼 노드','100nF50V radial','595 VCC-GND 바로 옆1개, 버튼 RC1개.','https://search.kemet.com/component-documentation/download/specsheet/C315C104K5R5TA')
item('PCB','납땜식 조작부 PCB','Adafruit','Perma-Proto Half-sized / #1609',1,'도어 표시판 뒤','81×51mm','무납땜 브레드보드로 운영하지 않음. 기존5-hole/전원 버스 패턴을 확인하고 절단/점퍼 후 조립. LED 패널 고정 위치는 실물 전사.','https://www.adafruit.com/product/1609')
for id,part,qty,role in [('J7-F','430250600',1,'6극 receptacle'),('J7-M','430200600',1,'6극 plug'),('J7-FC','430300007',6,'24~20AWG female contact'),('J7-MC','430310007',6,'24~20AWG male contact')]:
 item(id,'도어 잠금식 하네스','Molex',part,qty,'하부 J7 / 도어 연결',role,'Micro-Fit3.0 2×3. 제조사 정면도 기준핀1 표시. 본문 J7.1~6은 전기적 번호이므로 하우징 실제 캐비티 번호와 1:1 확인.','https://www.molex.com/en-us/products/part-detail/'+part)

unselected=[
 ('FUSE-ELEMENTS','FU0 ATO + F1~F7/F5L 6.3×32 소자','실측 전류·기동·전선/홀더 제한·DC 차단정격/시간특성 확인 후 값 결정'),
 ('AC-PROTECTION','기존 차단기·AC 단자 커버','현재 인입회로/다른장치 분리, 차단정격·전선/PE 현장 확인'),
 ('DIN-RAIL','NS35/7.5 규격레일·나사','절단표와 접지/마감에 맞는 실제 제품 및 길이 대조'),
 ('CABLES','DC/센서/도어 케이블·페룰','각 전류·거리·외경·단자/압착 접점 범위·관통구 실측으로 색상별 길이 확정'),
 ('SURGE','자석/모터 억제 소자','실전압·전류·회로 극성·자석 해제 시간 기준으로 부품/정격 선정'),
 ('MECHANICAL','백플레이트·캐리어·절연 스탠드오프·부싱·클립','실측 홀/판두께/기판 나사홀에 맞춘 가공물 및 체결 부품'),
 ('SENSOR-IF','센서/RFID 입력 인터페이스','출력형식/레벨 확인 후 필요한 회로만 선정. 무전압 접점에는 불필요한 변환기 추가하지 않음'),
 ('LEGACY','Arduino·RFID함·릴레이A/B·모터·오디오·센서','기존 실물 재사용. 모델/회로가 다른 새 제품을 임의로 대입하지 않음')]
bom={'checkedOn':'2026-11-03','scope':'manufacturer-backed product candidates with explicit sizing/field gates; not a completed purchase order','items':items,'unselected':[dict(zip(['id','name','reason'],r)) for r in unselected]}
(ROOT/'hardware/product-bom.json').write_text(json.dumps(bom,ensure_ascii=False,indent=2),encoding='utf-8')
heads=['ID','용도','제조사','품번','수량','장소','실제 외형/확보값','적용 조건','제조사 자료','상태']
with (ROOT/'hardware/product-bom.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(heads);w.writerows([[r[k] for k in ['id','name','maker','part','qty','location','size','condition','url','status']] for r in items])
o=['<section class="fit-sheet"><h2>실제 제품 BOM · 부품 도면과 배치 대조</h2><p>제조사 자료 확인: 2026-11-03. 아래는 주문 가능한 품번을 기준으로 만든 <b>제품 선정안</b>입니다. 부하 전류·실물 치수·조달 상태를 확인하기 전 전체 구매발주가 완료된 BOM으로 표시하지 않습니다.</p><div class="fit-warning">특히 SMPS 용량, 퓨즈 소자 값, 센서/RFID 인터페이스, 기존 릴레이8채널 용도는 사진만으로 확정하지 않습니다. 확인되지 않은 품번/전류를 지어내지 않았습니다.</div><h3>제품 선정으로 바뀐 부분</h3><p>PT2.5 단자24개는 RFID 옆 75×210mm 구역으로 옮겼습니다. 덕트는 실제 외폭17.5mm인 제품을 선택했습니다. OMRON 버튼의 최소1mA 조건을 맞추기 위해 풀업을 <b>4.7kΩ</b>으로 변경했고, 저전류 LED에는 <b>1.5kΩ×6</b>을 적용합니다.</p><div class="table-scroll"><table><thead><tr>']
for h in heads:o.append('<th>'+h+'</th>')
o.append('</tr></thead><tbody>')
for it in items:
 o.append('<tr>')
 for key in ['id','name','maker','part','qty','location','size','condition','url','status']:
  value=str(it[key]);o.append('<td>'+('<a href="'+html.escape(value,quote=True)+'" target="_blank" rel="noopener">공식 자료</a>' if key=='url' else html.escape(value))+'</td>')
 o.append('</tr>')
o.append('</tbody></table></div><h3>값을 채워야 발주가 완성되는 항목</h3><table><thead><tr><th>항목</th><th>남은 결정</th></tr></thead><tbody>')
for _,name,reason in unselected:o.append('<tr><td>'+html.escape(name)+'</td><td>'+html.escape(reason)+'</td></tr>')
o.append('</tbody></table><h3>도어 뒤 공간</h3><p>표시판은 하부 도어 기준 (40,270), 180×100mm 영역으로 잡고 뒤쪽45mm를 확보합니다. 맞은편 릴레이/스탠드오프40mm + 패널45mm + 최소 검토 간격15mm =100mm입니다. 유효 깊이120mm 검토값 안에 들어가지만, RFID 또는 L298N 방열판 앞에는 이 패널을 놓지 않습니다. 실제 문/잠금쇠와 버튼 단자 방향을 대조합니다.</p></section>')
(ROOT/'simulation/source/bom-view.html').write_text(''.join(o),encoding='utf-8')
md='# 8. 실제 제품 BOM\n\n'+ '\n\n'.join(f"- **{it['id']} / {it['maker']} {it['part']} ×{it['qty']}** — {it['location']}, {it['size']}. {it['condition']} [공식 자료]({it['url']})" for it in items)
md+='\n\n## 발주 전에 남은 결정\n\n'+'\n'.join('- **'+n+'**: '+r for _,n,r in unselected)+'\n\n도어 표시판: 하부(40,270),180×100mm. 후면45mm, 맞은편 릴레이40mm, 검토 간격15mm를 합산합니다. 실물 단자/도어 간섭을 확인합니다.\n'
(ROOT/'docs/08-product-bom.md').write_text(md,encoding='utf-8')
print(len(items),'manufacturer-backed BOM rows;',len(unselected),'explicit field-dependent categories')
