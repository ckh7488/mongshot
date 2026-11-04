"""Current direct-control revision; no external GPIO isolation modules."""
from pathlib import Path

def write_docs(root,m,bom,review):
    def out(rel,text):(root/rel).write_text(text,encoding='utf-8')
    pins='\n'.join('- '+a+' → '+b for a,b in [('D4','L298 IN1'),('D5','L298 IN2'),('A2','L298 ENA'),('D12','릴레이 A IN1'),('D10','릴레이 A IN2'),('D9','릴레이 A IN3'),('A4','릴레이 A IN4')])
    out('docs/01-confirmed-hardware.md','# 1. 기존 HW·제어선 직결 · v5.3\n\nUno/기존 릴레이 A·B/L298N E6/KT403A/홍싱/RFID를 보존합니다. 추가 ISO-M/ISO-R과 고정판·전용저항14개는 제거했습니다.\n\n'+pins+'\n\nG0.4→L298 GND 기준선을 함께 연결합니다. P0-MOTOR 전력 귀환은 별도 유지합니다. D8/D6 기존 리드와 D6 기존100Ω, A0/A1/A5 기존 입력을 보존합니다. D2/D3 MP3, D11/D13/D7 표시부, A3 2초버튼. B의4채널은 실제 추적 전 예비라고 단정하지 않습니다.\n')
    out('docs/02-power-and-ground.md','''# 2. 공통 GND와 독립 전력 귀환 · v5.3

모터·릴레이 추가 절연모듈을 제거하고 기존 제어선 직결로 되돌렸습니다. GND-MOTOR-REF:G0.4→L298 GND로 신호 기준을 연결합니다. 따라서 P0와 G0는 전기적으로 공통입니다. 이름/색/분배블록 위치가 달라도 갈바닉 절연이 아닙니다. 같은12V전원을 쓰는 자석−도 같은 GND에 속합니다.

자석·모터·릴레이 코일 전류는 각각 정해진 전력 귀환선으로 돌아가게 배선하고 Arduino/센서 귀환에 직렬로 통과시키지 않습니다. 실제 단자의 허용 선 수·굵기에 맞춰 기준선을 분기하며 굵기가 다른 선을 나사 하나에 억지로 몰아넣지 않습니다. 회로도가 공통이라는 사실만으로 모든 물리 배선의 임피던스/노이즈가 같지는 않습니다.

P12/P0는12V 부하, DC-D는5D/P0 부하용5V, DC-L은5L/G0 로직용5V 분기입니다. 두5V 양극끼리 합치지 않습니다. DDR 자체는 절연형이지만 위 공통기준선이 시스템 절연을 우회합니다. 현재 안에서 절연형 변환기는 필수가 아니며 전원부 후보로 남긴 상태입니다. 이번 수정으로 다른 전원장치를 임의 구매/교체하도록 확정하지 않습니다.

홍싱은 기존 어댑터, MP3 DAC L/R·GND는 홍싱에 직결합니다. 홍싱 어댑터+를5L에 합치지 않습니다. PE는 기존 콘센트 보호접지→SMPS FG/함체/도어를 유지하며 정상 DC귀환 대용이 아닙니다.

[귀환 포트](../hardware/ground-terminal-schedule.csv) · [선 구간](../hardware/wire-segments.csv) · [연결성 모델](../hardware/ground-connectivity.json)
''')
    out('docs/03-cabinet-and-bom.md','# 3. 실장 배치\n\n계획 유효 폭400/상부260/하부560/깊이120mm. 실측값이 아닙니다. 모터·릴레이 절연모듈/고정판을 제거하고 그 공간을 비웠습니다. 센서판/자석접속판/오디오절연판도 없습니다.\n\nRFID 몸체160×100×65, 홍싱140×90×45는 배치 가정입니다. DDR는 위40/아래20/좌우5mm 방열 공간을 포함합니다. 도어 후면과 부품 깊이 조건은 유지합니다. 나사홀은 실물로 전사합니다.\n\n[치수](../hardware/cabinet-fit-model.json) · [좌표](../hardware/mounting-schedule.csv) · [배치도](../hardware/cabinet-redesign.svg)\n')
    out('docs/04-rebuild-sequence.md','''# 4. 재결선 순서

1. 전체 전원을 차단하고 기존 Arduino 핀/양끝 선/릴레이8채널을 먼저 기록합니다. 기존 차단기·PE를 보존합니다.
2. 케이블 재질/굵기/길이/사용 페어를 기록하고 부품 외곽·관통구를 실측합니다.
3. 전원과 부하별 전력 귀환을 배치합니다. 센서/자석/오디오/GPIO 추가 PCB는 만들지 않습니다.
4. 기존 제어선을 L298/릴레이에 직결하고 GND-MOTOR-REF로 공통 기준을 연결합니다. P0/G0를 절연됐다고 검사하지 않습니다.
5. L298 전원5V-EN과 ENA 점퍼, 기존 입력 바이어스/리셋 접점 동작을 각각 대조합니다. 외부5V와 내부레귤레이터/USB 중복급전을 피합니다.
6. 자석별 다이오드는 릴레이 근처 자석+와− 사이에 병렬 고정합니다. 줄(K)=+,A=−. 각 리드 절연/기계 고정과 해제시간을 확인합니다.
7. 전류제한 시험전원에서 입력전압/부하단 전압/기동·정지/리셋/발열을 확인하고 실제 시공대로 선표를 갱신합니다. 기록하지 않은 정격/측정값을 만들지 않습니다.
''')
    out('docs/06-review-summary.md','# 6. 현재 상태\n\n모터/릴레이 추가 절연모듈을 제거했고 기존 GPIO직결·공통GND입니다. 회로/포트/라벨/화면/BOM은 이 상태를 기준으로 합니다. 자석 다이오드와 독립 전력 귀환은 유지하지만 자석−를 포함한 전체 갈바닉 절연은 아닙니다.\n\n실물 치수/케이블 전류/온도/센서 출력/릴레이 점퍼와 리셋 동작은 현장 대조가 남습니다. 원본 펌웨어는 보존했으며 실물 업로드와 GitHub push는 하지 않았습니다.\n')
    out('docs/07-rfid-and-relay-correction.md','# 7. 기존 릴레이 보드 사용\n\n추가 ISO-M/ISO-R은 제거했습니다. 기존 모듈 IN1~4를 Arduino가 직접 구동합니다. VCC/JD-VCC/GND와 입력 극성은 실물에 맞춥니다. 기존 보드 자체의 옵토가 있더라도 현재 전체 시스템은 P0/G0 공통이므로 갈바닉 절연으로 표시하지 않습니다.\n\nA의4채널 재배치는 기존8채널 추적 후 적용합니다. B가 불필요하다고 단정하지 않습니다.\n')
    text='# 8. 제품 BOM · v5.3\n\n추가 GPIO 절연모듈2개/고정판/전용저항14개를 제거했습니다.\n\n'
    for it in bom['items']:
        text+=f"- **{it['id']} / {it['maker']} {it['part']} ×{it['qty']}** — {it['location']}, {it['size']}. {it['condition']}"+(f" [공식 자료]({it['url']})" if it['url'] else '')+'\n\n'
    out('docs/08-product-bom.md',text)
    cable=root/'docs/09-ethernet-wire-and-isolation.md'
    out('docs/09-ethernet-wire-and-isolation.md',cable.read_text(encoding='utf-8').replace('# 9. 이더넷 심선과 절연 결선','# 9. 이더넷 심선과 부하 배선'))
    out('docs/10-interface-assembly.md','''# 10. 추가 GPIO 절연부 없이 연결

L298 D4→IN1/D5→IN2/A2→ENA, 릴레이 D12/D10/D9/A4→IN1/2/3/4를 기존처럼 직결합니다. G0.4→L298 GND 공통 기준선과 별도 P0-MOTOR 전력 귀환을 사용합니다. 기존 단자에서 허용되는 선 수/굵기와 접속방법으로 분기합니다. ENA/전원5V-EN 점퍼와 기존 입력 기본상태는 서로 구별해 확인합니다.

새 센서판/필터 일괄 추가 없음. D6 기존100Ω 유지. 실제12V 신호를 Arduino에 직결하지 않습니다. 자석 다이오드는 릴레이 근처에서 각 자석 두 선에 병렬, K줄=+,A=−입니다. 별도 PCB 없이 리드를 절연하고 고정합니다. COM–NO 사이가 아닙니다. 일반 다이오드는 해제를 늦출 수 있으므로 실제 차단서지/해제시간을 대조합니다.

KT403A DAC L/R·GND는 홍싱 MP3 IN에 직결하며 홍싱은 기존 어댑터를 사용합니다. 외부 GPIO 절연모듈과 캐리어/전용저항은 사용하지 않습니다.

DDR 후보는 내부0.8mm² 이상 동선과 위40/아래20/좌우5mm 통풍 여유를 유지합니다. 현재 공통GND 연결로 시스템 절연은 우회되며 절연형이 필수인 상태는 아닙니다.
''')
    out('README.md','''# MONG SHOT · v5.3 기존 제어선 직결

로컬: http://127.0.0.1:8766/ · OPEN_MONGSHOT.cmd로 오프라인 HTML 열기.

모터/릴레이 추가 절연모듈2개와 고정판·전용저항14개를 제거했습니다. 기존 제어선과 공통GND로 연결합니다. P0/G0는 귀환 분기 이름이며 전기적으로 공통입니다. 자석−까지 갈바닉 절연된 설계가 아닙니다.

센서판/자석접속판/오디오절연판도 없습니다. 자석 다이오드3개만 릴레이 근처에 고정합니다. MP3/홍싱은 기존 라인·GND 직결, 홍싱 기존 어댑터를 사용합니다. 추가 퓨즈 제외 결정은 유지하며 기존 차단기·PE를 보존합니다.

[전원·GND](docs/02-power-and-ground.md) · [핀](docs/01-confirmed-hardware.md) · [BOM](docs/08-product-bom.md) · [재결선](docs/04-rebuild-sequence.md) · [조립](docs/10-interface-assembly.md) · [설계 이유](docs/11-design-review.md)

[배치도](hardware/cabinet-redesign.svg) · [GND도](hardware/ground-topology.svg) · [결선도](hardware/isolation-interfaces.svg) · [좌표](hardware/mounting-schedule.csv) · [전체 선표](hardware/wire-segments.csv) · [양끝 라벨](hardware/wire-labels.html) · [A3 배치 PDF](output/pdf/MongShot_TwoBay_Mounting_Templates.pdf)

RFID/홍싱 크기는 배치 가정이며 현장 치수/전류/센서 출력/케이블 정격은 미측정 상태입니다. Arduino/MP3 실물 통신과 노이즈가 검증됐다는 뜻은 아닙니다.

재생성: python tools/build_3d.py → python tools/build_project.py. 검사: python tests/check-design.py. PDF: python tools/build_mounting_templates.py. 원본스케치 보존, GitHub push/실물 flash 없음.
''')
