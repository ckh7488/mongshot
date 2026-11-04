# 5. 코드와 검증 범위

v5는 전원/배치/인터페이스 재설계이며 Arduino 펌웨어는 변경하지 않습니다. ISO 보드는 비반전이라 GPIO HIGH/LOW를 유지합니다. 12V 스위칭 센서 옵토 출력은 감지LOW이며 기존 ADC 임계값 적용 여부를 센서 실물에서 확인합니다.

원본/10ms안4시험 + 외부LED·2초버튼6시험은 AVR 실행으로 검증합니다. 74HC595 래치 값은 GPIO에서 읽습니다.

MP3는 시뮬레이터용 API 대역이며 원본 라이브러리 호출의 인자 불일치가 남아 있어 실물 업로드 완료본이 아닙니다. 실제 자석/접점/전원서지/케이블 발열/절연 장벽을 AVR 시뮬레이터가 검증하지는 않습니다.

`python tools/build_project.py`, `python tests/check-design.py`, `npm test`. PDF는 `python tools/build_mounting_templates.py`로 재생성합니다.
