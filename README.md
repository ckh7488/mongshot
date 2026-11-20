# MONG SHOT · v6.1 하네스 우선 배치 + v5.3 보존본

현재 화면: **`http://127.0.0.1:8766/`** · `OPEN_MONGSHOT.cmd`로 오프라인 실행. 우측 상단에서 v5.3 원본과 비교할 수 있습니다.

v6는 기존 #4091 한 대로5V를 통합하고 DDR-15G-5만 삭제합니다. G→L298 중복 기준선을 없애 P0–G의 계획 연결을 강압기 경유 한 경로로 정리했습니다. 신규 부품·PCB·퓨즈·절연 모터드라이버 추가는 없습니다. 모터 VMS12/5V는 미확인 대안이며 동시에 연결하지 않습니다.

[하네스 조립 순서](docs/13-harness-assembly.md) · [v6 정면 배선도](hardware/v6/front-wiring.svg) · [모든 배선](hardware/v6/front-wiring-full.svg) · [v6 설명·작업 순서](docs/12-v6-common-star.md) · [배치 좌표](hardware/v6/mounting-schedule.csv) · [전체 결선표](hardware/v6/wire-segments.csv) · [0V 포트](hardware/v6/ground-port-schedule.csv) · [양극 포트](hardware/v6/positive-port-schedule.csv) · [BOM](hardware/v6/product-bom.csv) · [라벨3장](hardware/v6/wire-labels.html) · [지시서 검토](hardware/v6/instruction-audit.json)

v6.1은 접점 전력 H1 / 제어 H2 / DC분배 H3와 좌우 주 덕트를 먼저 정하고 모듈 단자를 향하게 배치합니다. 장거리 구간은 공용 덕트 그래프를 따르며 단자 앞 꼬리선은 최대46.5mm입니다. 3D 기본 묶음 뷰와 개별 가닥 뷰에서 같은 도체를 확인할 수 있습니다. 묶음은 전기적 접속이 아닙니다.

2D/3D는 같은 경로 데이터를 사용하며, 선을 누르면 구성 도체·양끝·케이블·조건을 표시합니다. 화면에서2D SVG/결선CSV/좌표CSV/BOM/라벨/검사JSON을 저장할 수 있습니다. 사진 기반 치수·부품 외형·실물U1~U7은 미확인입니다. 계획 도면 검사와 실제 시공·동작 시험을 구분합니다.

재생성: `python tools/build_project.py`. 검사: `python tests/check-design.py`. 아래 내용과 기존 A3 PDF/기존 hardware 루트 자료는 **v5.3 보존 자료**입니다. v6 타공도나 실물 합격으로 쓰지 않습니다.

---

# MONG SHOT · v5.3 기존 제어선 직결

로컬: `http://127.0.0.1:8766/` · `OPEN_MONGSHOT.cmd`로 오프라인 HTML 열기.

모터/릴레이 추가 절연모듈2개와 고정판·전용저항14개를 제거했습니다. 기존 제어선과 공통GND로 연결합니다. P0/G0는 귀환 분기 이름이며 전기적으로 공통입니다. 자석−까지 갈바닉 절연된 설계가 아닙니다.

센서판/자석접속판/오디오절연판도 없습니다. 자석 다이오드3개만 릴레이 근처에 고정합니다. MP3/홍싱은 기존 라인·GND 직결, 홍싱 기존 어댑터를 사용합니다. 추가 퓨즈 제외 결정은 유지하며 기존 차단기·PE를 보존합니다.

[전원·GND](docs/02-power-and-ground.md) · [핀](docs/01-confirmed-hardware.md) · [BOM](docs/08-product-bom.md) · [재결선](docs/04-rebuild-sequence.md) · [조립](docs/10-interface-assembly.md) · [설계 이유](docs/11-design-review.md)

[배치도](hardware/cabinet-redesign.svg) · [GND도](hardware/ground-topology.svg) · [결선도](hardware/isolation-interfaces.svg) · [좌표](hardware/mounting-schedule.csv) · [전체 선표](hardware/wire-segments.csv) · [양끝 라벨](hardware/wire-labels.html) · [A3 배치 PDF](output/pdf/MongShot_TwoBay_Mounting_Templates.pdf)

RFID/홍싱 크기는 배치 가정이며 현장 치수/전류/센서 출력/케이블 정격은 미측정 상태입니다. Arduino/MP3 실물 통신과 노이즈가 검증됐다는 뜻은 아닙니다.

재생성: python tools/build_3d.py → python tools/build_project.py. 검사: python tests/check-design.py. PDF: python tools/build_mounting_templates.py. 원본스케치 보존, GitHub push/실물 flash 없음.

Three.js 보기: 휠 확대/왼쪽 회전/오른쪽 이동/전체화면/부품 선택/도어 LED. 소스 수정 후 `python tools/build_3d.py` → `python tools/build_project.py`. [인터페이스 조립 지침](docs/10-interface-assembly.md)을 함께 봅니다.
