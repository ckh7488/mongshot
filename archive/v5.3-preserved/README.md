# MONG SHOT · v5.3 기존 제어선 직결

로컬: http://127.0.0.1:8766/ · OPEN_MONGSHOT.cmd로 오프라인 HTML 열기.

모터/릴레이 추가 절연모듈2개와 고정판·전용저항14개를 제거했습니다. 기존 제어선과 공통GND로 연결합니다. P0/G0는 귀환 분기 이름이며 전기적으로 공통입니다. 자석−까지 갈바닉 절연된 설계가 아닙니다.

센서판/자석접속판/오디오절연판도 없습니다. 자석 다이오드3개만 릴레이 근처에 고정합니다. MP3/홍싱은 기존 라인·GND 직결, 홍싱 기존 어댑터를 사용합니다. 추가 퓨즈 제외 결정은 유지하며 기존 차단기·PE를 보존합니다.

[전원·GND](docs/02-power-and-ground.md) · [핀](docs/01-confirmed-hardware.md) · [BOM](docs/08-product-bom.md) · [재결선](docs/04-rebuild-sequence.md) · [조립](docs/10-interface-assembly.md) · [설계 이유](docs/11-design-review.md)

[배치도](hardware/cabinet-redesign.svg) · [GND도](hardware/ground-topology.svg) · [결선도](hardware/isolation-interfaces.svg) · [좌표](hardware/mounting-schedule.csv) · [전체 선표](hardware/wire-segments.csv) · [양끝 라벨](hardware/wire-labels.html) · [A3 배치 PDF](output/pdf/MongShot_TwoBay_Mounting_Templates.pdf)

RFID/홍싱 크기는 배치 가정이며 현장 치수/전류/센서 출력/케이블 정격은 미측정 상태입니다. Arduino/MP3 실물 통신과 노이즈가 검증됐다는 뜻은 아닙니다.

재생성: python tools/build_3d.py → python tools/build_project.py. 검사: python tests/check-design.py. PDF: python tools/build_mounting_templates.py. 원본스케치 보존, GitHub push/실물 flash 없음.

Three.js 보기: 휠 확대/왼쪽 회전/오른쪽 이동/전체화면/부품 선택/도어 LED. 소스 수정 후 `python tools/build_3d.py` → `python tools/build_project.py`. [인터페이스 조립 지침](docs/10-interface-assembly.md)을 함께 봅니다.
