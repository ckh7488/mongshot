# 8. 제품 BOM · v5.3

추가 GPIO 절연모듈2개/고정판/전용저항14개를 제거했습니다.

- **DUCT / Panduit G.5X1LG6 ×2** — 상하 배선 경로, 외형 폭17.5×높이26.9mm / 길이1.8288m. 호칭0.5인치와 외폭은 다름. 계획20mm 채널에 대조. 실제 선 외경·충전량은 현장 검토. [공식 자료](https://www.panduit.com/content/dam/panduit/en/products/media/4/34/334/2334/74122334.pdf)

- **DUCT-C / Panduit C.5LG6 ×2** — 위 덕트 전 길이, 본체와 별매 / 길이1.8288m. 덕트 높이26.9mm는 커버 포함. 실제 절단 길이 합과 여유를 대조. [공식 자료](https://www.panduit.com/content/dam/panduit/en/products/media/4/34/334/2334/74122334.pdf)

- **U1 / Texas Instruments SN74HC595N ×1** — 도어 PCB, PDIP16. 5V, QA~QF 사용. /OE=0V, /SRCLR=5V. 595 옆100nF. [공식 자료](https://www.ti.com/lit/ds/symlink/sn74hc595.pdf)

- **LED1~6 / Kingbright WP7113LGD ×6** — 도어 2행×3열, 5mm 관통형. 2mA 특성 제품. 각 LED1.5kΩ, 음극0V-L. 12V 패널 램프로 치환 금지. [공식 자료](https://www.kingbrightusa.com/product.asp?catalog_name=LED&product_id=WP7113LGD)

- **SW1 / OMRON A16-TAM-1 ×1** — 하부 도어 (25,200) / 180×75mm, 16mm형 / 패널 뒤28.5mm급, 단자 여유 별도. 비조광·청색·momentary SPDT의 COM/NO만 사용. 최소1mA@5V이므로 외부4.7k 풀업 적용. [공식 자료](https://www.ia.omron.com/product/item/13731/)

- **RLED / YAGEO MFR-25FBF52-1K5 ×6** — 도어 PCB, 6.3×Ø2.4mm급. 1.5kΩ,1%,0.25W. 포장 대체는 동일 전기/기구 사양으로만. [공식 자료](https://yageogroup.com/content/Resource%20Library/Datasheet/YAGEO-MFR_DATASHEET.pdf)

- **RPULL / YAGEO MFR-25FBF52-4K7 ×1** — 도어 PCB, 6.3×Ø2.4mm급. 4.7kΩ,1%,0.25W. 약1.06mA@5V를 접점으로 공급. [공식 자료](https://yageogroup.com/content/Resource%20Library/Datasheet/YAGEO-MFR_DATASHEET.pdf)

- **RSER / YAGEO MFR-25FBF52-1K ×1** — A3 입력 경로, 6.3×Ø2.4mm급. 1kΩ,1%,0.25W. LED 저항1.5k와 구별. [공식 자료](https://yageogroup.com/content/Resource%20Library/Datasheet/YAGEO-MFR_DATASHEET.pdf)

- **C1/C2 / KEMET C315C104K5R5TA ×2** — 595 옆 / 버튼 노드, 100nF50V radial. 595 VCC-GND 바로 옆1개, 버튼 RC1개. [공식 자료](https://search.kemet.com/component-documentation/download/specsheet/C315C104K5R5TA)

- **PCB / Adafruit Perma-Proto Half-sized / #1609 ×1** — 도어 표시판 뒤, 81×51mm. 무납땜 브레드보드로 운영하지 않음. 기존5-hole/전원 버스 패턴을 확인하고 절단/점퍼 후 조립. LED 패널 고정 위치는 실물 전사. [공식 자료](https://www.adafruit.com/product/1609)

- **J7-F / Molex 430250600 ×1** — 하부 J7 / 도어 연결, 6극 receptacle. Micro-Fit3.0 2×3. 제조사 정면도 기준핀1 표시. 본문 J7.1~6은 전기적 번호이므로 하우징 실제 캐비티 번호와 1:1 확인. [공식 자료](https://www.molex.com/en-us/products/part-detail/430250600)

- **J7-M / Molex 430200600 ×1** — 하부 J7 / 도어 연결, 6극 plug. Micro-Fit3.0 2×3. 제조사 정면도 기준핀1 표시. 본문 J7.1~6은 전기적 번호이므로 하우징 실제 캐비티 번호와 1:1 확인. [공식 자료](https://www.molex.com/en-us/products/part-detail/430200600)

- **J7-FC / Molex 430300007 ×6** — 하부 J7 / 도어 연결, 24~20AWG female contact. Micro-Fit3.0 2×3. 제조사 정면도 기준핀1 표시. 본문 J7.1~6은 전기적 번호이므로 하우징 실제 캐비티 번호와 1:1 확인. [공식 자료](https://www.molex.com/en-us/products/part-detail/430300007)

- **J7-MC / Molex 430310007 ×6** — 하부 J7 / 도어 연결, 24~20AWG male contact. Micro-Fit3.0 2×3. 제조사 정면도 기준핀1 표시. 본문 J7.1~6은 전기적 번호이므로 하우징 실제 캐비티 번호와 1:1 확인. [공식 자료](https://www.molex.com/en-us/products/part-detail/430310007)

- **PS1 / MEAN WELL LRS-200-12 ×1** — 상부, 215×115×30mm. 기존 후보 보존. 17A가 필요하다는 확정 아님; 얇은 현장선 허용 전류를 의미하지 않음 [공식 자료](https://www.meanwell.com/Upload/PDF/LRS-200/LRS-200-SPEC.PDF)

- **DC-L / MEAN WELL DDR-15G-5 ×1** — 하부 확보(100,405), 몸체(113.75,445), 17.5×90×54.5mm. 입력P12/P0, 출력5L/G0. 5V3A(입력12~36V), 9~12V에서는2.7A. 위40/아래20/좌우5mm 확보. 내부 입력/출력 간선은0.8mm² 이상 동선으로 분배블록까지 연결. 로직예산1.2A는 실측 아님. GPIO직결 공통GND 안에서는 절연형이 필수 아님; 이번 변경은 전원부 선택을 자동 변경하지 않음 [공식 자료](https://www.meanwell.com/Upload/PDF/DDR-15/DDR-15-spec.pdf)

- **DC-D / Pololu D36V50F5 / #4091 ×1** — 하부 (25,430), 25.4×25.4×9.5mm. 5D/P0: 릴레이코일 및 L298 Vss. 5L과5D의 양극끼리 연결 금지. GND는 제어 기준선으로 공통 [공식 자료](https://www.pololu.com/product/4091)

- **D-M1~3 / Vishay 1N5408-E3/54 ×3** — 릴레이 A 근처 자석선 +/− 사이, DO-201AD. 3A/1000V 소자 후보. 줄(K)=자석+, A=자석−. 코일전류/열/반복률/해제시간 확인. 3A는 케이블 허용 전류가 아님 [공식 자료](https://www.vishay.com/docs/88516/1n5400.pdf)

- **G-P/G-L / Phoenix Contact PTFIX 6/12X2,5-NS35 BU / 3273090 ×2** — 상부P0 / 하부G0, 58.1×28.6×32.4mm. 두 블록은 귀환 분기용이며 GND-MOTOR-REF로 전기적 공통. 절연 경계 아님. 가는 단선은 주황 버튼을 눌러 삽입 [공식 자료](https://www.phoenixcontact.com/en-nl/products/distribution-block-ptfix-6-12x25-ns35-bu-3273090)

- **P12/5L / Phoenix Contact PTFIX 6/12X2,5-NS35 RD / 3273092 ×2** — 상부12V / 하부로직5V, 58.1×28.6×32.4mm. 전위가 다른 블록 두 개. 5D는 기존 릴레이/L298 전원선의 분기접속으로 공급 [공식 자료](https://www.phoenixcontact.com/en-fr/products/distribution-block-ptfix-6-12x25-ns35-rd-3273092)

