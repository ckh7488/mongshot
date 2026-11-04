"""One SMPS: show the actual common metal path and numbered output ports."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
o=[]
def a(s):o.append(s)
def t(x,y,s,size=15,c='#4a6d7d',anchor='start'):a(f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" text-anchor="{anchor}">{escape(s)}</text>')
def r(x,y,w,h,c,rx=4,stroke=None):a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')
def p(points,c='#278d86',w=3,key='gnd',dash=None):
 a('<path d="M'+'L'.join(f'{x} {y}' for x,y in points)+f'" fill="none" stroke="{c}" stroke-width="{w}" class="net" data-net="{key}" stroke-linejoin="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def c(x,y,radius,color):a(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}"/>')
def dev(name):a(f'<g class="device" data-part="{name}" tabindex="0" role="button">')
def end():a('</g>')
a('<svg xmlns="http://www.w3.org/2000/svg" id="ground-topology-svg" width="1180" height="900" viewBox="0 0 1180 900" role="img" aria-label="한 SMPS의 공통 GND와 0V-PWR/0V-L 내부 공통 분배블록 포트"><style>text{font-family:"Malgun Gothic",Arial,sans-serif}.device{cursor:pointer;outline:none}.selected-device{filter:drop-shadow(0 0 4px #18a69e)}.selected-net{stroke-width:5!important;opacity:1!important}.dim-net{opacity:.22}</style>')
t(39,46,'GND는 이 두 분배블록에, 회로별로 따로 연결',24)
t(39,77,'상부: SMPS·0V-PWR / 하부: DC-DC·0V-L. 전위는 공통이며 큰 부하의 귀환 경로를 로직에서 분리합니다.',13,'#8a9eaa')

dev('smps');r(44,126,201,110,'#7c8e99',6);r(53,136,183,90,'#d3dfe5',4);t(144,173,'12V SMPS ×1',20,'#536e7d','middle');t(144,201,'V+ / V− / PE',13,'#8a9daa','middle');end()
p([(245,162),(515,162)],'#be7b65',3,'mag-power');t(292,147,'+12V → 부하별 퓨즈 → 부하',13,'#ae856e')
p([(245,212),(288,212),(288,290),(555,290),(555,199),(587,199)],'#997b5e',5,'power-ground');t(297,277,'SMPS V− : 굵은 공통 귀환',13,'#997b5e')

def block(name,x,y,color,title,labels):
 dev(name);t(x,y-23,title,19,color);r(x,y,540,139,'#e7eef2',6,'#c4d4de');r(x+12,y+15,64,96,color,4);c(x+44,y+40,13,'#486673');r(x+22,y+72,44,12,'#eab36b',2);t(x+44,y+130,'IN',11,'#6d8d9d','middle')
 # Brown line explicitly exposes the continuous internal common conductor.
 p([(x+44,y+62),(x+510,y+62)],'#b9975d',9,name)
 for i,label in enumerate(labels):
  xx=x+100+(i%6)*70;yy=y+27+(i//6)*72
  p([(xx,y+62),(xx,yy)],'#b9975d',3,name);r(xx-22,yy-17,44,35,color,3);c(xx,yy-4,6,'#4a6978');r(xx-10,yy+7,20,6,'#eab36b',1)
  t(xx,yy+29,f'{i+1} {label}',10,'#6f8b99','middle')
 end()
block('power-ground',587,134,'#9e815f','상부 0V-PWR : 부하별 전용 음극 귀환', ['자석1','자석2','자석3','모터','앰프','RFID*','L.IN','예비','예비','예비','예비','예비'])
t(588,304,'이 블록 안의 갈색 선 = 실제 내부 공통 금속 도체',13,'#a68b65')

dev('buck');r(72,380,214,125,'#4b907f',6);r(91,397,174,65,'#679c86',4);c(180,429,25,'#b6a26d');c(180,429,13,'#547c6d');t(180,492,'12V → 5V DC-DC',15,'#e9f4ed','middle');end()
t(74,363,'IN+ / IN−',12,'#859da8');t(236,528,'OUT+ / OUT−',12,'#859da8','end')
p([(383,162),(383,335),(107,335),(107,380)],'#be7b65',3,'logic-power')
p([(687,234),(505,234),(505,475),(587,475)],'#278d86',5,'gnd');t(311,350,'0V-LINK : 굵은 직접 공통선',13,'#438f8f')
p([(72,438),(144,438),(144,475),(286,475)],'#b9975d',5,'buck-reference')
t(171,563,'비절연형 내부: IN− = OUT−',13,'#9d885f','middle')

block('gnd',587,427,'#378f98','하부 0V-L : 굵은 0V-LINK가 IN으로 직접 연결', ['Arduino','액자','조명','열쇠','RFID REF*','책','MP3','릴레이 A','릴레이 B','외부 LED','BUCK GND','측정점'])
p([(286,475),(350,475),(350,615),(967,615),(967,544)],'#278d86',3,'buck-reference');t(43,597,'DC-DC 공통 GND → 0V-L.11 (한 경로)',13,'#438f8f')
t(588,598,'RFID*는 기존 급전·출력 형식에 맞춰 종단. 센서 Vcc와 신호 전압은 별도 확인.',12,'#8d9fa9')

dev('distribution-detail')
t(42,642,'분배블록 하나로 가능한 이유',19)
t(42,671,'PTFIX 같은 1전위 분배블록은 내부가 이미 공통입니다.',14,'#7794a2')
t(42,695,'일반 독립 단자대는 정격 점퍼를 넣어야 같은 구조가 됩니다.',14,'#7794a2')
for i in range(6):
 x=76+i*65;r(x,732,45,61,'#a4bec8',3);c(x+22,750,7,'#5a7582');r(x+17,773,10,11,'#647f8b',1);t(x+22,816,str(i+1),11,'#7996a4','middle')
p([(98,767),(423,767)],'#b9975d',9,'gnd');t(249,843,'연속 공통 점퍼 / 금속 버스',13,'#a48d64','middle')
end()

t(590,660,'실제 제품 예시',17)
t(590,691,'Phoenix Contact PTFIX 6/12X2,5-NS35 BU',14,'#7191a1')
t(590,716,'품번 3273090 · 1전위 · 13접속점 · DIN 35mm',13,'#8fa4ae')
t(590,747,'블록은 절연형으로 고정하고, PE 단자와 구별합니다.',13,'#7995a2')
t(590,774,'실제 전류·전선·페룰은 제조사 단자 정격 안에서 선정합니다.',13,'#7995a2')
t(590,808,'오디오/RFID 신호 GND로 우회 경로가 생길 수 있어',13,'#9a8c75')
t(590,832,'그 경로까지 기록하며, 필요 시 인터페이스 절연을 검토합니다.',13,'#9a8c75')
t(40,881,'중요: 이 기본안은 전기적 GND 절연이 아닙니다. 별도 5V SMPS를 추가해도 신호 GND가 연결되면 공통입니다.',14,'#607f8e')
a('</svg>')
(ROOT/'hardware/ground-topology.svg').write_text('\n'.join(o),encoding='utf-8')
print('Concrete common distribution block / single SMPS topology ready')
