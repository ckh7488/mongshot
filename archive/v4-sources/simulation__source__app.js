/* MONG SHOT workbench. UI reads SRAM/GPIO from compiled AVR firmware. */
(()=>{'use strict';
const $=id=>document.getElementById(id),all=(s,r=document)=>[...r.querySelectorAll(s)];
const details={
 gnd:{title:'0V-L 공통 버스',desc:'센서마다 신호와 GND를 한 쌍으로 회수합니다. 절연형 단자대와 공통 점퍼가 하나의 낮은 저항 기준점을 만듭니다.',rows:[['연결','Arduino · 센서 · KT403A'],['연결','릴레이 제어/코일'],['구조','공통 점퍼 + 개별 귀환'],['분리','0V-MAG · PE'],['모터 기준','0V-MOT와 한 점 결합']],note:'로직 PCB에는 연속 GND 면을 둡니다. 모터·전자석 전류를 Arduino 보드의 GND 핀과 가는 센서선으로 흘리지 않습니다.',nets:['gnd','motor-bond']},
 'mag-ground':{title:'0V-MAG 전자석 전용',desc:'전자석 전용 12V 어댑터 음극입니다. 제어 GND·모터 GND·오디오 GND·PE와 전도성 연결을 만들지 않습니다.',rows:[['전원','PS-MAG · 별도 12V'],['부하','몰딩 / 슬라이드 / 책'],['제어 경계','릴레이 무전압 접점'],['GND-L 연결','없음']],note:'5V를 이 전원에서 일반 비절연 DC-DC로 만들면 GND가 합쳐집니다. 앰프를 같은 12V에 묶어도 오디오 케이블로 로직과 재연결될 수 있습니다.',nets:['mag-ground','mag-power','load12','load10','load9']},
 'motor-ground':{title:'0V-MOT 모터 귀환',desc:'모터의 큰 전류는 모터 전원 음극으로 직접 귀환합니다. L298N의 제어 기준은 로직 GND와 한 점에서 공유합니다.',rows:[['전원','PS-MOT · 기존 정격'],['모터 루프','전용 + / 0V 선'],['로직 기준','0V-L와 지정 한 점'],['완전 절연','3신호 절연기 추가 필요']],note:'기본안은 L298N을 유지하는 공통 기준 방식입니다. 모터까지 완전 절연하려면 D4/D5/A2에 절연 인터페이스가 필요합니다.',nets:['motor-ground','motor-bond','motor-supply','actuator']},
 'motor-bond':{title:'모터 기준 GND 한 점',desc:'별도 모터 귀환과 로직 버스 사이의 의도적인 기준 연결입니다. 전자석 절연 버스와는 무관합니다.',rows:[['연결','0V-MOT ↔ 0V-L'],['목적','L298N GPIO 기준'],['금지','Arduino PCB로 모터 귀환']],note:'모터 전원과 L298N의 실제 점퍼·GND 배선을 확인해 우회 결합이 생기지 않게 합니다.',nets:['motor-bond','gnd','motor-ground']},
 uno:{title:'Arduino 컨트롤러',desc:'현장 Arduino의 코드 핀을 그대로 사용합니다. 시뮬레이터는 ATmega328P 기반 Uno의 실제 명령어·타이머·GPIO·ADC를 실행합니다.',rows:[['입력','D8 / A0 / A1 / A5 / D6'],['릴레이','D12 / D10 / D9 / A4'],['모터','D4 / D5 / A2'],['오디오','D2 RX / D3 TX'],['급전안','5V USB · 외부 코일 별도']],note:'모든 부하를 Arduino의 5V/GND 핀에서 공급하지 않습니다. 운영 USB 급전과 PC 디버깅 급전이 충돌하지 않도록 전원 경로를 정합니다.',nets:['frame','light','key','rfid','book','out12','out10','out9','out18']},
 relayA:{title:'4채널 릴레이 A',desc:'새 배선안에서는 네 기능을 한 보드에 모읍니다. 이 채널 번호는 기존 실배선의 단정이 아니라 새 재결선 기준입니다.',rows:[['IN1 / CH1','D12 · 몰딩'],['IN2 / CH2','D10 · 슬라이드'],['IN3 / CH3','D9 · 책'],['IN4 / CH4','A4(18) · 창문'],['전원','별도 5V 분기 / 0V-L']],note:'입력 극성(Active LOW/HIGH)과 접점 선택은 아래 재결선표의 검증란을 채운 뒤 적용합니다. 화면의 LED는 GPIO HIGH/LOW이며 코일 여자 상태가 아닙니다.',nets:['out12','out10','out9','out18','load12','load10','load9','window','gnd']},
 relayB:{title:'4채널 릴레이 B',desc:'기존 두 번째 보드를 정상 크기로 배치하고 현재 연결을 보존합니다. Arduino 코드의 출력 4개만으로 다른 채널이 불필요하다고 판단하지 않습니다.',rows:[['기존 구성','4CH × 2장 / 총 8채널'],['새 배치','A/B 보드 모두 수용'],['기존 채널','양 끝 라벨 후 그대로 추적'],['불필요/예비','확정하지 않음']],note:'한 출력에 접점이 여러 개 쓰이거나 다른 제어 장치가 채널을 사용할 수 있습니다. 이는 가능성의 설명이며 확인된 실제 연결이라는 뜻은 아닙니다. 제거 여부는 채널별 실선 추적 뒤 결정합니다.',nets:[]},
 l298:{title:'L298N E6',desc:'기존 리니어 액추에이터 드라이버를 유지합니다. 모터 전류는 전용 전원선, 입력은 로직 기준 신호로 나눕니다.',rows:[['IN1','D4'],['IN2','D5'],['ENA','A2 / D16'],['PWM','A2는 PWM 아님'],['0V','0V-MOT → 0V-L 한 점']],note:'원본은 부팅 때 방향 LOW/HIGH, enable HIGH를 설정합니다. 시뮬레이터도 이 GPIO 상태를 그대로 표시합니다. 실제 모터 정지·리미트는 별도 확인합니다.',nets:['motor4','motor5','motor16','motor-ground','motor-bond','actuator']},
 motor:{title:'리니어 액추에이터',desc:'모터 정격전원과 내장 리미트·기계 동작을 유지합니다. 이 화면은 드라이버 입력 상태를 표시하며 실제 기구 운동을 모델링하지 않습니다.',rows:[['드라이버','L298N E6'],['방향','D4 / D5'],['ENABLE','A2(16) HIGH'],['전원 귀환','0V-MOT 전용']],note:'부팅부터 enable이 HIGH인 원본 동작을 보존했습니다. 실제 기동 여부를 사람·기구와 분리해 시험합니다.',nets:['actuator','motor-ground','motor4','motor5','motor16']},
 mp3:{title:'KT403A MP3',desc:'D2/D3 SoftwareSerial을 사용하는 음성 모듈입니다. 기존 9600 baud, SD 장치 선택, 볼륨 25/30 호출을 보존합니다.',rows:[['Arduino D2','RX ← MP3 TX'],['Arduino D3','TX → MP3 RX'],['전원 기준','모듈 정격 / 0V-L'],['오디오','LINE OUT → 앰프']],note:'기존 코드의 SpecifyMusicPlay(0,1)와 동봉 1인자 헤더가 달라 시뮬레이터에서는 MP3 API만 대역 처리했습니다. 음원·UART 응답은 검증하지 않습니다.',nets:['uart2','uart3','audio','gnd']},
 amp:{title:'HONGXING 앰프',desc:'사진과 이전 세션에서 확인한 12V 앰프를 재사용합니다. 기존 전용 어댑터를 유지하고 오디오 케이블의 GND 경로를 포함해 관리합니다.',rows:[['전원','DC 12V · 센터 +'],['입력','KT403A 오디오'],['GND 경로','신호 케이블로 로직과 연결 가능'],['전자석 전원','공유하지 않음']],note:'스피커 − 단자를 GND 버스로 사용하지 않습니다. 앰프가 전자석 12V를 공유하면 오디오 GND가 절연 경계를 우회할 수 있습니다.',nets:['audio','audio-power']},
 pslogic:{title:'PS-L 로직 전원',desc:'전자석 전원과 분리한 제어용 전원입니다. Arduino·센서·MP3·릴레이 코일에 각 분기를 줍니다.',rows:[['Arduino','5V USB 급전안'],['릴레이 코일','Arduino 핀 경유 금지'],['음극','0V-L 공통'],['전원 용량','동시 부하 합으로 선정']],note:'센서별 공급 전압은 원래 부품 정격을 따릅니다. 모든 센서 V단자에 5V를 일괄 인가하지 않습니다.',nets:['logic-power','gnd']},
 psmag:{title:'PS-MAG 전자석 전원',desc:'전자석만 공급하는 별도 12V 전원입니다. 제어·앰프·모터와 DC 음극을 공유하지 않습니다.',rows:[['출력','12V / 0V-MAG'],['분기','F1 / F2 / F3'],['제어','릴레이 접점'],['정격','전자석 동시 전류 기준']],note:'새 전원을 구매하기 전 기존 어댑터의 정격·절연 상태를 활용해 구성할 수 있습니다. 보호 정격은 부하와 배선에 맞춥니다.',nets:['mag-ground','mag-power','load12','load10','load9']},
 psaudio:{title:'PS-A 오디오 전원',desc:'기존 앰프용 12V 어댑터를 유지합니다. 전자석용 12V 전원과 합치지 않습니다.',rows:[['부하','HONGXING 12V'],['로직 기준','오디오 GND 경로 존재 가능'],['분리','PS-MAG와 별도']],note:'PS-A 음극을 로직 버스에 추가로 연결하기 전에 오디오 케이블을 통한 기존 결합을 확인합니다. 중복 경로를 임의로 만들지 않습니다.',nets:['audio','audio-power']},
 psmotor:{title:'PS-MOT 모터 전원',desc:'액추에이터의 기존 정격 전원을 유지합니다. 별도 귀환선과 모터 분기 보호를 둡니다.',rows:[['전압','모터/어댑터 라벨 기준'],['음극','0V-MOT'],['기준 연결','0V-L와 한 점']],note:'L298N 모듈의 5V 레귤레이터 점퍼와 외부 5V를 동시에 연결하지 않도록 실제 보드를 기준으로 확인합니다.',nets:['motor-supply','motor-ground','motor-bond']},
 'mag-power':{title:'전자석 개별 분기 보호',desc:'몰딩·슬라이드·책 전자석을 각각 퓨즈·단자로 나눕니다. 릴레이 접점 이후 각 부하로 인출합니다.',rows:[['F1','몰딩 전자석'],['F2','슬라이드 전자석'],['F3','책 전자석'],['서지 억제','부하 가까이 · 정격 선정']],note:'퓨즈·전선·TVS/다이오드 정격은 전자석 전류와 해제 시간, 접점의 DC 정격을 함께 보고 결정합니다.',nets:['mag-power','load12','load10','load9']},
 power:{title:'전원 분배 배치안',desc:'전원선을 Arduino에 몰아 꽂지 않고 단자대에서 기능별로 분기합니다.',rows:[['로직','PS-L / 0V-L'],['전자석','PS-MAG / 0V-MAG'],['모터','PS-MOT / 0V-MOT'],['오디오','기존 어댑터 유지']],note:'PE는 금속 함체 보호용이며 센서 GND 귀환선 대신 쓰지 않습니다.',nets:['logic-power','mag-ground','motor-ground','gnd']}
};
for(const [id,title,pin,condition,idx]of[['frame','액자 리드','D8','LOW / INPUT_PULLUP',1],['light','조명','A0','ADC < 500 / 3회',2],['key','열쇠','A1','ADC < 100',3],['rfid','RFID 감지','A5','ADC < 400',4],['book','책 리드','D6','LOW / 100Ω 직렬',5]]) details[id]={title,desc:'확정된 기능과 코드 핀을 새 단자대로 옮깁니다. 신호선과 해당 센서의 GND를 한 쌍으로 추적합니다.',rows:[['Arduino',pin],['새 단자','X1.'+idx+' S / V* / 0'],['신호 라벨','IN-'+pin],['GND 라벨','0VL-'+id.toUpperCase()],['판정',condition]],note:id==='book'?'D6은 IR이 아니라 책 리드스위치입니다. 기존 직렬 100Ω을 보존합니다.':idx===1?'2선 접점이므로 S와 0V-L를 사용합니다.':'센서 종류를 새로 가정하지 않고 기존 출력과 정격을 유지합니다. V*에는 해당 센서의 원래 전압만 공급합니다.',nets:[id,'gnd']};
details.rfidbox={title:'RFID 회색 제어함',desc:'사용자가 확인한 큰 회색 제어함 전체를 새 배전함 안에 수용합니다. 작은 RFID 센서 하나로 취급하지 않고 기존 함체·내부 장치·급전선을 보존합니다.',rows:[['설치','새 함체 안에 공간 확보'],['확인된 코드 연결','감지 출력 → A5'],['판정','ADC < 400'],['전원/내부 회로','기존 결선 보존'],['기구 공간','하부 (40,10) / 280×220 확보']],note:'회색함 전원 음극을 0V-L에 임의로 합치지 않습니다. A5 출력의 신호 기준과 회색함 전원은 구별하고 실제 인터페이스/기존 결선을 따릅니다.',nets:['rfidbox-output','rfid']};
details['rfidbox-output']=details.rfidbox;
details.rfid={...details.rfid,title:'RFID 제어함 감지 출력',desc:'함 안의 큰 회색 RFID 제어함에서 나오는 감지 출력을 Arduino A5로 전달하는 경로입니다.',note:'실제 회색함과 그 급전선을 유지합니다. 출력 기준/접점과 전원 음극을 같은 것으로 가정하지 않습니다.',nets:['rfid','rfidbox-output']};
Object.assign(details,{
 gnd:{title:'0V-L 로직 공통 분배블록',desc:'내부 도체로 모든 단자가 연결된 1전위 분배블록입니다. 상부 0V-PWR.7을 굵은 0V-LINK로 입력받고, 각 로직 회로를 개별 포트에 연결합니다.',rows:[['제품 예시','PTFIX 6/12X2,5-NS35 BU'],['품번','3273090 / 13접속점'],['입력','0V-PWR.7 → 0V-LINK'],['출력','Arduino · 센서 · MP3'],['출력','릴레이 제어 · 외부 조작부'],['PWR와 관계','굵은 0V-LINK로 직접 공통']],note:'독립 단자대는 전선만 꽂으면 공통이 아닙니다. 정격 공통 점퍼 또는 내부 공통 분배블록을 사용합니다. 각 포트의 정격·페룰·고정 방법을 따릅니다.',nets:['gnd','buck-reference']},
 'power-ground':{title:'0V-PWR 부하 귀환 분배블록',desc:'SMPS V−에 바로 연결되는 공통 분배부입니다. 전자석·모터·앰프 및 하부 0V-LINK를 각각 따로 받아 로직/센서 GND선으로 부하 전류가 흐르지 않게 합니다.',rows:[['입력','SMPS V−'],['부하 귀환','자석1 / 자석2 / 자석3'],['부하 귀환','L298N / 앰프 / RFID*'],['공통선','0V-PWR.7 → 0V-L.IN'],['로직과 절연','아님 · 동일 DC 기준']],note:'한 SMPS + 일반 DC-DC 기본안은 전체 GND가 공통입니다. 별도 귀환선은 전류 경로를 관리하기 위한 것이며 갈바닉 절연이 아닙니다. RFID는 실제 정격/인터페이스를 따릅니다.',nets:['power-ground','buck-reference']},
 smps:{title:'12V 메인 SMPS 1대',desc:'확인된 12V 전자석과 앰프를 기준으로 잡은 기본안입니다. 각 부하에 개별 보호 분기를 두고 5V는 별도 DC-DC로 만듭니다.',rows:[['기본 전압','12V 안'],['5V 생성','DC-DC 별도'],['전류 용량','최대 동시부하·모터 기동 기준'],['센서/RFID','기존 정격별 확인'],['PE','함체 보호 · 신호 0V와 구별']],note:'아직 모델/전류 정격을 확정하거나 구매하지 않았습니다. 센서 전원 12V와 Arduino 입력 신호 전압을 구별합니다.',nets:['logic-power','power-ground','mag-power']},
 buck:{title:'12V → 5V DC-DC',desc:'5V 레일은 필요하지만 별도 5V SMPS가 필수는 아닙니다. 기본안은 비절연 DC-DC로 제어 전원을 안정화합니다.',rows:[['IN+','12V 보호 분기'],['GND','0V-L.11'],['OUT+','5V 로직 분기'],['0V 기준','IN/OUT 공통 GND 한 경로'],['내부 음극','IN− = OUT− (공통, 0V-L.11 한 곳 종단)']],note:'Arduino 온보드 LDO에서 릴레이 코일을 급전하지 않습니다. 12V 부하의 전원 장애로부터 로직 급전을 더 독립시키려면 별도 5V SMPS를 선택할 수 있습니다. 어느 쪽도 GND 절연을 자동 보장하지 않습니다.',nets:['logic-power','gnd','buck-reference']},
 frontpanel:{title:'외부 LED·진행 버튼',desc:'현재 단계 LED 1개가 켜지고, 프로그램 대기에는 깜빡입니다. 진행 버튼을 2초 누르면 현재 센서 입력 단계를 한 번 완료합니다.',rows:[['LED','액자 / 조명 / 열쇠'],['LED','RFID / 책 / 완료'],['595 DATA','D11 → SER(14)'],['595 CLK','D13 → SRCLK(11)'],['595 LATCH','D7 → RCLK(12)'],['진행 버튼','A3 / 2초 / 재누름 필요']],note:'D11/A3는 기존 Gun/Hint 선을 제거한 뒤 재사용합니다. SPI.begin()은 D10 릴레이에 영향을 줄 수 있어 사용하지 않습니다. 실제 출력한 74HC595 래치 값으로 표시합니다.',nets:['panel','gnd']},
 'distribution-detail':{title:'분배블록의 내부 공통 도체',desc:'13개 접속점이 한 전위에 연결된 분배블록입니다. 내부 금속 버스가 전기적 공통을 만듭니다.',rows:[['예시','Phoenix Contact 3273090'],['방식','Push-in / DIN NS35'],['단자','입력 1 + 분기 12'],['전위','한 블록 안에서는 모두 공통']],note:'단자 정격을 넘지 않는 배선/페룰을 선택합니다. 일반 단자대 여러 개를 쓰면 제조사 정격 공통 점퍼로 연결해야 합니다.',nets:['gnd','power-ground']},
 'mag-power':{title:'12V 부하별 퓨즈 분기',desc:'한 SMPS에서 전자석·모터·오디오·DC-DC로 각각 분기합니다. 전자석 전용 분기는 릴레이 접점으로 ON/OFF합니다.',rows:[['전자석','F1/F2/F3 독립 분기'],['기타','모터 / 오디오 / DC-DC'],['귀환','0V-PWR로 각각'],['퓨즈/서지','부하·배선 기준 최종 선정']],note:'전원 한 대 기본안에서 자석 음극을 전기적으로 절연했다고 표현하지 않습니다.',nets:['mag-power','power-ground','load12','load10','load9']}
});
details['mag-ground']=details['power-ground'];details['motor-ground']=details['power-ground'];details['motor-bond']=details.buck;details['buck-reference']=details.buck;
details.amp={...details.amp,desc:'기본안에서는 메인 12V에서 별도 보호 분기로 공급하고 전력 음극은 0V-PWR로 직접 귀환합니다.',rows:[['급전','12V 메인 · 별도 보호 분기'],['전력 음극','0V-PWR'],['신호','KT403A 오디오'],['우회 GND','신호 케이블 경로까지 확인']],note:'오디오 GND가 로직과 추가 경로를 만들 수 있습니다. 전력 귀환을 신호 케이블에 의존하지 않고, 필요 시 라인 절연을 검토합니다.'};
details.l298={...details.l298,desc:'모터 전원은 정격에 맞는 분기로, 큰 전류 귀환은 0V-PWR로 직접 보냅니다. 로직 기준은 직접 0V-LINK로 공통입니다.',rows:[['IN1 / IN2','D4 / D5'],['ENA','A2 / D16'],['급전','모터 정격 분기'],['귀환','0V-PWR 직접'],['기준','0V-LINK 직접 연결']],note:'모터 전류가 Arduino/센서 GND를 통과하지 않게 합니다. L298N의 레귤레이터/ENA 점퍼와 부팅 구동 상태는 실제 보드에서 확인합니다.'};
details.power=details.smps;
details['field-terminals']={title:'현장 단자 24개 · RFID 옆',desc:'Phoenix PT2.5의 실제 외형을 반영해 두 그룹을 세로로 배치합니다. 일반 단자는 서로 독립이며 GND 블록과 다릅니다.',rows:[['제품','PT 2,5 / 3209510 ×24'],['그룹','신호12 / 부하12'],['위치','하부 (320,20), 75×210 확보'],['마감','D-ST2.5 / CLIPFIX35-5']],note:'센서 S/0V는 짝으로, 자석/모터는 부하군으로 종단합니다. 표의 X1/X3/X4 전기적 이름은 단자실장표의 위치에 대응합니다.',nets:[]};
details['main-fuse']={title:'FU0 · 주 DC 보호',desc:'Littelfuse FHAC0002ZXJ 32V/30A 홀더 후보입니다. 홀더 정격이 곧 장착할 퓨즈 전류는 아닙니다.',rows:[['위치','상부 (285,170)'],['확보','80×75mm / 리드 경로 대조'],['퓨즈','ATO · 실부하/전선 기준 선정']],note:'몸체 치수와 리드 굽힘은 실제 제품/제조사 도면으로 대조합니다. 30A 퓨즈를 무조건 넣으라는 뜻이 아닙니다.',nets:['mag-power']};
details.smps={...details.smps,rows:[['후보','MEAN WELL LRS-200-12'],['외형','215×115×30mm'],['출력 정격','12V17A / 필요용량은 별도 대조'],['5V','Pololu4091 → 5V 분배부']],note:'동시/기동 전류와 폐함 온도·장착 방향을 확인한 뒤 구매 용량을 확정합니다. 사진 속 제품 모델을 식별했다는 뜻은 아닙니다.'};
details.buck={...details.buck,rows:[['후보','Pololu D36V50F5 / #4091'],['몸체','25.4×25.4×9.5mm'],['입력','F6 VIN / 0V-L.11 GND'],['출력','F5L / 5V PTFIX RD'],['음극','비절연 / IN·OUT 공통']],note:'캐리어에 변환기·5V 분배블록·F5L을 함께 고정합니다. 입력 12V에서 실제 부하/폐함 온도를 확인하며 5.5A를 모든 조건의 보장값으로 사용하지 않습니다.'};

details.pe={title:'PE 보호접지 바',desc:'상부 금속 외함과 문 등 접지 대상의 보호접지용입니다. 센서 신호 귀환을 이 바나 외함으로 대신하지 않습니다.',rows:[['장소','상부 (325,15)'],['연결','인입 PE / SMPS PE / 외함'],['DC 0V','임의 결합 금지']],note:'기존 접지 경로와 제조사 요구를 확인해 적용합니다. DC 음극-PE의 의도적 결합 여부는 전원/시스템 사양에 따라 별도 기록합니다.',nets:[]};
details.ac={title:'상부 AC 전용 구역',desc:'기존 인입 회로를 추적한 뒤 차단기·SMPS AC·PE를 상부 안에 고정합니다. 아래 제어함으로 AC를 통과시키지 않는 배치입니다.',rows:[['장소','상부 (10,10)'],['상하 관통구','DC 전원선만'],['보호','단자 커버 / 고정 배선']],note:'이 사진에 보이는 기존 두 SMPS가 모두 이 장치용이라고 단정하지 않습니다. 다른 장치의 회로는 철거 전에 구별합니다.',nets:[]};
details.motor={...details.motor,rows:[['드라이버','L298N E6'],['방향','D4 / D5'],['ENABLE','A2(16) HIGH'],['귀환','L298N 전력 0V → 상부 0V-PWR']]};
for(const [id,title,pin,ch]of[['mold','몰딩 전자석',12,1],['slide','슬라이드 전자석',10,2],['bookload','책 전자석',9,3],['window','창문 출력',18,4]]) details[id]={title,desc:pin===18?'창문은 부하 전원을 임의로 바꾸지 않고 독립된 릴레이 무전압 접점만 인출합니다.':'기존 12V 전자석입니다. 상부 개별 퓨즈에서 내려온 양극을 하부 릴레이 접점으로 스위칭하며, 음극은 상부 0V-PWR로 직접 귀환합니다.',rows:[['Arduino',pin===18?'A4 / D18':'D'+pin],['릴레이 배치','RY-A CH'+ch],['단자',pin===18?'X3-WIN':('X3-M'+ch)],['귀환',pin===18?'창문 부하 자체 전원':'상부 0V-PWR 개별 포트']],note:'릴레이 입력 극성·접점 선택·부팅 상태를 무부하에서 검증한 뒤 부하를 연결합니다.',nets:['out'+pin,'load'+pin,...(pin===18?['window']:['mag-ground'])]};

const labels=[
['IN-D8','X1.1-S','Arduino D8','액자 리드 S','frame'],['0VL-FRAME','X1.1-0','0V-L BUS','액자 리드 0V','gnd'],
['IN-A0','X1.2-S','Arduino A0','조명 출력 S','light'],['0VL-LIGHT','X1.2-0','0V-L BUS','조명 0V','gnd'],
['IN-A1','X1.3-S','Arduino A1','열쇠 출력 S','key'],['0VL-KEY','X1.3-0','0V-L BUS','열쇠 0V','gnd'],
['IN-A5','X1.4-S','Arduino A5','RFID 출력 S','rfid'],['0VL-RFID','X1.4-0','0V-L BUS','RFID 0V','gnd'],
['IN-D6','X1.5-S','Arduino D6 / 100Ω','책 리드 S','book'],['0VL-BOOK','X1.5-0','0V-L BUS','책 리드 0V','gnd'],
['OUT-D12','X2.1','Arduino D12','RY-A IN1 / 몰딩','out12'],['OUT-D10','X2.2','Arduino D10','RY-A IN2 / 슬라이드','out10'],['OUT-D9','X2.3','Arduino D9','RY-A IN3 / 책','out9'],['OUT-A4','X2.4','Arduino A4(18)','RY-A IN4 / 창문','out18'],
['MOT-D4','X4.1','Arduino D4','L298N IN1','motor4'],['MOT-D5','X4.2','Arduino D5','L298N IN2','motor5'],['MOT-A2','X4.3','Arduino A2(16)','L298N ENA','motor16'],
['MP3-RX','X5.1','Arduino D2 RX','KT403A TX','uart2'],['MP3-TX','X5.2','Arduino D3 TX','KT403A RX','uart3'],
['MAG1+','X3-M1+','RY-A CH1 接点','몰딩 전자석 +','load12'],['MAG1-','X3-M1-','0V-MAG BUS','몰딩 전자석 −','mag-ground'],['MAG2+','X3-M2+','RY-A CH2 接点','슬라이드 전자석 +','load10'],['MAG2-','X3-M2-','0V-MAG BUS','슬라이드 전자석 −','mag-ground'],['MAG3+','X3-M3+','RY-A CH3 接点','책 전자석 +','load9'],['MAG3-','X3-M3-','0V-MAG BUS','책 전자석 −','mag-ground'],
['WIN-C','X3-WIN.C','RY-A CH4 COM','창문 회로 자체 전원','window'],['WIN-SW','X3-WIN.SW','RY-A CH4 선택 접점','창문 부하','window']
].map(r=>r.map(x=>typeof x==='string'?x.replace('接点','접점').replace('0V-MAG BUS','상부 0V-PWR'):x));
window.MONGSHOT_LABELS=labels;
const mode=$('firmware-mode');let runner,playing=false,lastWall=0,simDebt=0,currentView='new',selection='gnd',zoom=100,demoStart=null,demoEvents=[],prevStage=-1,hasPower=false,pendingManualReleaseAt=null;
const outputs=[[12,'몰딩 / D12'],[10,'슬라이드 / D10'],[9,'책 / D9'],[18,'창문 / A4'],[4,'모터 방향 / D4'],[5,'모터 방향 / D5'],[16,'ENABLE / A2']];
$('outputs').innerHTML=outputs.map(([p,name])=>`<div class="output-row"><span><i id="dot-${p}"></i>${name}</span><span class="level" id="out-${p}">Hi-Z</span></div>`).join('');
const row=(k,v)=>`<div class="info-row"><span>${k}</span><span class="v">${v}</span></div>`;
function select(id){
 selection=id;
 const idFallback=id.startsWith('out')?({out12:'mold',out10:'slide',out9:'bookload',out18:'window'})[id]:id.startsWith('motor')?'l298':id.startsWith('uart')?'mp3':id.startsWith('load')?({load12:'mold',load10:'slide',load9:'bookload',load18:'window'})[id]:id==='actuator'?'motor':id.startsWith('gnd-')?'gnd':id;
 const d=details[id]||details[idFallback]||details.gnd;
 $('detail-title').textContent=d.title;$('detail-desc').textContent=d.desc;$('detail-rows').innerHTML=d.rows.map(([k,v])=>row(k,v)).join('')+`<div class="inspector-note">${d.note}</div>`;
 const targets=d.nets||[id];
 all('.net').forEach(el=>{const yes=targets.includes(el.dataset.net);el.classList.toggle('selected-net',yes);el.classList.toggle('dim-net',targets.length>0&&!yes);});
 all('.device').forEach(el=>el.classList.toggle('selected-device',el.dataset.part===id||el.dataset.part===idFallback));
 all('[data-select-net]').forEach(el=>el.classList.toggle('selected-label',el.dataset.selectNet===id));
}
all('.device').forEach(el=>{const handler=()=>select(el.dataset.part);el.addEventListener('click',handler);el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();handler();}});});
all('.net-hit').forEach(el=>el.addEventListener('click',()=>select(el.dataset.net)));
all('[data-select-net]').forEach(el=>{const handler=()=>select(el.dataset.selectNet);el.addEventListener('click',handler);el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();handler();}});});
function clearHighlight(){all('.net').forEach(el=>el.classList.remove('selected-net','dim-net'));all('.device').forEach(el=>el.classList.remove('selected-device'));}
function reset(){runner=new MongshotAVR.Runner(MONGSHOT_FIRMWARE[mode.value]);playing=false;demoStart=null;demoEvents=[];pendingManualReleaseAt=null;lastWall=0;simDebt=0;prevStage=-1;update();$('run').textContent='▶ 실행';$('toast').classList.remove('visible');}
function requestManual(){if(!runner.firmware.frontpanel||runner.inputs.manual||runner.word('phase')===9)return;demoStart=null;demoEvents=[];if(runner.ms<1100)runner.runMs(1100-runner.ms);runner.setInputs({manual:true});pendingManualReleaseAt=runner.ms+2100;playing=true;lastWall=performance.now();$('run').textContent='Ⅱ 일시정지';$('toast').textContent='부팅을 마친 뒤 진행 버튼 입력 2초를 시뮬레이션합니다. 입력 단계는 1회 완료하고, 프로그램 대기 중 입력은 다음 단계로 예약하지 않습니다.';$('toast').classList.add('visible');select('frontpanel');}
$('manual-next').addEventListener('click',requestManual);
all('[data-action="manual-next"]').forEach(el=>el.addEventListener('click',e=>{e.stopPropagation();requestManual();}));
function setInput(values){runner.setInputs(values);update();}
for(const key of ['frame','book'])$('input-'+key).addEventListener('click',()=>setInput({[key]:!runner.inputs[key]}));
for(const key of ['light','key','rfid'])$('input-'+key).addEventListener('input',e=>setInput({[key]:Number(e.target.value)}));
$('pulse-light').addEventListener('click',()=>setInput({light:runner.inputs.light<500?900:100}));
for(const key of ['key','rfid'])$('toggle-'+key).addEventListener('click',()=>setInput({[key]:runner.inputs[key]<400?900:0}));
$('run').addEventListener('click',()=>{playing=!playing;lastWall=performance.now();$('run').textContent=playing?'Ⅱ 일시정지':'▶ 실행';update();});
$('reset').addEventListener('click',reset);mode.addEventListener('change',reset);
$('demo').addEventListener('click',()=>{
 reset();demoStart=0;demoEvents=[
 [1200,{frame:true}],[1500,{light:100}],[1750,{light:900}],[2000,{light:100}],[2250,{light:900}],[2500,{light:100}],
 [22900,{key:0}],[23400,{rfid:0}],[24800,{book:true}]
 ];playing=true;lastWall=performance.now();$('run').textContent='Ⅱ 일시정지';$('toast').textContent='자동 시연: 센서 입력만 순서대로 주입합니다. 코드의 20초·1초·10초 지연은 그대로 실행됩니다.';$('toast').classList.add('visible');
});
const views={bom:['실제 제품 BOM · 제조사/품번/외형','제품 도면과 설치 영역 대조 · 전류/기구/조달 조건을 함께 표시'],new:['사진 기준 상하 배전함 · 실장 계획','상부 전원 / 하부 RFID·제어 · mm 좌표·확보 영역·기존 관통구'],fit:['실장·치수 · 부품이 들어가는 조건','유효 폭·상하 높이·깊이·RFID 외곽을 입력해 계획 영역과 비교'],panel:['외부 LED·진행 버튼 · 실제 핀 회로','SN74HC595N / 1kΩ ×6 / A3 버튼 · 기존 Gun/Hint 선 제거 후 재사용'],gnd:['GND 분배블록 · 포트별 실제 연결','0V-PWR 부하 귀환 / 0V-L 로직 기준 · 비절연 기본안에서 전기적으로 공통'],cabinet:['기존 기능·코드 핀 연결','기존 어댑터 구성의 기능 추적도 · 새 전원 구성은 첫 번째 보기에 표시'],photo:['기존 현장 배전함','철거 전 커넥터·양 끝 라벨·사진 기록의 기준 자료'],labels:['핀·라벨 · 외부 조작부 포함','양 끝 라벨과 새 단자 대응 · J7 조작부 6선 추가']};
function setView(v){
 currentView=v;all('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===v));
 $('view-title').textContent=views[v][0];$('view-subtitle').textContent=views[v][1];
 $('drawing-stage').classList.toggle('photo',v==='photo');
 for(const [id,view] of [['design-drawing','new'],['ground-drawing','gnd'],['panel-drawing','panel'],['fit-drawing','fit'],['bom-drawing','bom'],['functional-drawing','cabinet'],['labels-drawing','labels']])$(id).hidden=v!==view;
 $('bay-controls').hidden=v!=='new';$('domain-notice').hidden=!['new','gnd'].includes(v);
 $('design-doc').classList.toggle('active',['new','gnd','labels','panel','fit','bom'].includes(v));
 if(v==='gnd'){hasPower=true;all('svg').forEach(s=>s.classList.add('show-power'));select('gnd');}
 else if(v==='new')select('smps');else if(v==='cabinet')select('uno');else if(v==='panel')select('frontpanel');
 updatePowerButton();applyZoom();
}
let bayFocus='all';
all('[data-bay]').forEach(b=>b.addEventListener('click',()=>{bayFocus=b.dataset.bay;all('[data-bay]').forEach(x=>x.classList.toggle('active',x===b));$('redesign-svg').setAttribute('viewBox',({all:'0 0 1420 2200',upper:'40 100 1370 700',lower:'45 730 970 1440'})[bayFocus]);zoom=100;applyZoom();}));
$('wide-drawing').addEventListener('click',()=>{const on=document.body.classList.toggle('wide-drawing');$('wide-drawing').setAttribute('aria-pressed',String(on));$('wide-drawing').textContent=on?'입력창 표시':'도면 크게';applyZoom();});
all('[data-view]').forEach(b=>b.addEventListener('click',()=>setView(b.dataset.view)));
function updatePowerButton(){$('power-layer').classList.toggle('active',hasPower);$('power-layer').textContent=hasPower?'전원선 켜짐':'전원선';}
$('power-layer').addEventListener('click',()=>{hasPower=!hasPower;all('svg').forEach(s=>s.classList.toggle('show-power',hasPower));updatePowerButton();});
function applyZoom(){const host=$('drawing-stage'),mobile=window.innerWidth<=760;all('#design-drawing>svg,#ground-drawing>svg,#panel-drawing>svg,#functional-drawing>svg').forEach(s=>{const box=s.viewBox.baseVal;const base=mobile?Math.max(680,host.clientWidth):Math.min(host.clientWidth,host.clientHeight*box.width/box.height);s.style.width=base*zoom/100+'px';s.style.height='auto';s.style.maxWidth='none';});}
new ResizeObserver(()=>applyZoom()).observe($('drawing-stage'));
$('zoom-in').addEventListener('click',()=>{zoom=Math.min(200,zoom+20);applyZoom();});$('zoom-out').addEventListener('click',()=>{zoom=Math.max(60,zoom-20);applyZoom();});$('zoom-fit').addEventListener('click',()=>{zoom=100;applyZoom();clearHighlight();});
function update(){
 const s=runner.snapshot();$('sim-time').textContent=(s.ms/1000).toFixed(2)+' s';$('light-count').textContent=Math.min(3,s.lightCount)+' / 3';$('filter-info').textContent=MONGSHOT_FIRMWARE[mode.value].sampleMs+'ms × 5회';
 for(const key of ['frame','book']){const active=s.inputs[key];$('value-'+key).textContent=active?'LOW':'HIGH';$('input-'+key).textContent=active?'감지 중 · 해제하기':'자석 감지시키기';$('input-'+key).classList.toggle('on',active);$('input-'+key).setAttribute('aria-pressed',String(active));}
 for(const key of ['light','key','rfid']){$('value-'+key).textContent=s.inputs[key];$('input-'+key).value=s.inputs[key];}
 for(const [p]of outputs){const val=s.pins[p],txt=val===null?'Hi-Z':val?'HIGH':'LOW';$('out-'+p).textContent=txt;$('out-'+p).classList.toggle('high',val===1);$('dot-'+p).classList.toggle('high',val===1);all(`[id="relay-led-${p}"],[id="load-led-${p}"],[id="new-load-led-${p}"]`).forEach(el=>el.setAttribute('fill',val===1?'#4dbb88':'#899ca5'));}
 all('.step').forEach((el,i)=>{el.classList.toggle('current',i===s.stage);el.classList.toggle('done',i<s.stage);});
 const title=['액자 감지 대기','조명 3회 판정','열쇠 감지 대기','RFID 감지 대기','책 감지 대기','종료 · 리셋 대기'];let note='';
 if(s.ms<1050)note='부팅·MP3 초기화 대기';else if(s.stage===2&&s.pins[10]===0)note='슬라이드 해제 전 20초 대기';else if(s.stage===4)note='창문 출력 HIGH · 1초 지연 후 책 입력';else if(s.stage===5)note=s.pins[9]===0?'책 전자석 출력 전 200ms 대기':'책 출력 HIGH · 10초 후 종료 루프';else if(s.stage===0)note='모터 GPIO: D4 LOW / D5 HIGH / EN HIGH';else note='현재 단계의 입력만 판정합니다.';
 if(runner.firmware.frontpanel){const phases={1:'부팅 준비',2:'MP3 초기화 대기',3:'슬라이드 해제 전 20초 대기',4:'슬라이드 해제 후 10ms 대기',5:'창문 출력 후 1초 대기',6:'책 출력 전 100ms',7:'음성 후 100ms',8:'최종 10초 대기',9:'완료 · LED 유지'};note=phases[s.phase]||'현재 LED 단계의 입력 대기 · 2초 버튼으로 1회 완료';}
 for(let i=0;i<6;i++){const on=runner.firmware.frontpanel&&!!(s.ledMask&(1<<i));$('front-led-'+i).classList.toggle('on',on);all(`[id="panel-led-${i}"]`).forEach(el=>el.setAttribute('fill',on?'#4cb58c':'#8a9ca6'));}
 $('manual-next').disabled=!runner.firmware.frontpanel||s.phase===9;$('manual-state').textContent=runner.firmware.frontpanel?`수동 진행 ${s.manualCount}회 · ${s.inputs.manual?'버튼 누름 중':'2초 누름 / 유지 반복 없음'}`:'원본/최소변경안은 외부 조작부 미지원';
 $('stage-title').textContent=title[s.stage]||'실행 중';$('stage-note').textContent=note;$('stage-progress').style.width=Math.min(100,s.stage/5*100)+'%';$('serial-log').textContent=runner.serial.slice(-6).map(x=>(x.ms/1000).toFixed(2)+'  '+x.text).join('\n');
 const runStatus=playing?(demoStart!==null?'자동 시연 실행 중':'실행 중'):'일시정지';if($('run-status').textContent!==runStatus)$('run-status').textContent=runStatus;
 if(s.stage!==prevStage){prevStage=s.stage;}
}
let lastPaint=0;
function frame(now){
 if(playing){
  const dt=Math.min(80,Math.max(0,now-lastWall||0));lastWall=now;simDebt=Math.min(500,simDebt+dt*Number($('speed').value));const wallLimit=performance.now()+16;
  while(simDebt>0&&performance.now()<wallLimit){
   let chunk=Math.min(5,simDebt);
   if(demoStart!==null&&demoEvents.length&&runner.ms+chunk>=demoEvents[0][0]){chunk=Math.max(.01,demoEvents[0][0]-runner.ms);}
   runner.runMs(chunk);simDebt-=chunk;
   if(pendingManualReleaseAt!==null&&runner.ms>=pendingManualReleaseAt){runner.setInputs({manual:false});pendingManualReleaseAt=null;}
   while(demoEvents.length&&runner.ms>=demoEvents[0][0]-.05){runner.setInputs(demoEvents.shift()[1]);}
   if(demoStart!==null&&runner.ms>=35500){playing=false;$('run').textContent='▶ 실행';$('toast').textContent='자동 시연 완료: 5단계 종료. 원본 지연시간과 최종 GPIO 상태를 유지했습니다.';break;}
  }
 }
 if(now-lastPaint>80){update();lastPaint=now;}requestAnimationFrame(frame);
}
reset();setView('new');select('gnd');requestAnimationFrame(frame);
window.mongshotWorkbench={get runner(){return runner;},select,setView,reset,setInput,get playing(){return playing;},details};
})();
