"""Ground current-path drawing, deliberately distinct from physical layout."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
s=[]
def a(t):s.append(t)
def text(x,y,t,size=16,color='#3c5c69',anchor='start'):
 a(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(t)}</text>')
def path(points,c='#278d86',w=3,dash=None,net=None):
 a('<path d="M'+'L'.join(f'{x} {y}' for x,y in points)+f'" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+(f' class="net" data-net="{net}"' if net else '')+'/>')
def dot(x,y,c='#278d86'):a(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>')
def rect(x,y,w,h,c,rx=4):a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>')
def dev(key):a(f'<g data-part="{key}" class="device" tabindex="0" role="button">')
def end():a('</g>')
a('<svg xmlns="http://www.w3.org/2000/svg" id="ground-topology-svg" width="1180" height="770" viewBox="0 0 1180 770" role="img" aria-label="로직 공통 GND와 전자석 절연, 모터 전류 귀환 구조"><style>text{font-family:"Malgun Gothic",Arial,sans-serif}.device{cursor:pointer;outline:none}.device:focus{filter:drop-shadow(0 0 3px #20a297)}.selected-device{filter:drop-shadow(0 0 4px #20a297)}.selected-net{stroke-width:5!important;opacity:1!important}.dim-net{opacity:.25}</style>')
text(45,47,'GND 구조 · 어디로 전류가 돌아가는가',23)
text(45,77,'로직과 모터는 기준점 한 곳을 공유합니다. 전자석은 별도 전원과 릴레이 접점으로 전기적으로 분리합니다.',13,'#8598a2')
text(45,125,'CONTROL / 5V',13,'#278d86');text(750,125,'MAGNET / 12V ISOLATED',13,'#aa7941')

# Supplies are represented as power units with explicit + and − terminals.
for key,x,label,volts in [('pslogic',45,'PS-L','5V 로직'),('psmag',988,'PS-MAG','12V 전자석')]:
 dev(key);rect(x,151,139,73,'#3e505c',7);text(x+69,179,label,16,'#edf4f6','middle');text(x+69,202,volts,12,'#b3c5d0','middle');end()
path([(184,170),(580,170)],'#bd6f66',3,net='logic-power');text(202,159,'+5V 분기',12,'#a86f65')
path([(115,224),(115,407),(591,407)],'#278d86',6,net='gnd')
dev('gnd');rect(45,391,544,33,'#e4f1eb',3);path([(45,407),(590,407)],'#278d86',7,net='gnd');text(51,451,'0V-L  공통 GND 버스',18,'#278d86');end()

# Arduino (real-shaped board) and five field returns to the common bus.
uno=(ROOT/'hardware/assets/arduino-uno-wokwi.svg').read_text(encoding='utf-8').replace('&nbsp;','&#160;')
import re
uno=re.sub(r'width="[^"]*"','width="192"',uno,count=1);uno=re.sub(r'height="[^"]*"','height="141"',uno,count=1)
uno=uno.replace('<svg','<svg x="205" y="220" class="ground-uno" style="width:192px;height:141px"',1).replace('>','><style>.ground-uno text{font-size:2px;font-family:monospace}</style>',1)
dev('uno');a(uno);end()
path([(280,170),(280,215)],'#bd6f66',3,net='logic-power');path([(325,355),(325,407)],net='gnd');dot(325,407)
text(301,384,'Arduino GND',11,'#7c919b','middle')
for i in range(5):
 x=53+i*24;rect(x,272,15,31,'#86a598',2);a(f'<circle cx="{x+7}" cy="282" r="4" fill="#dce7e3"/>');path([(x+7,303),(x+7,407)],'#278d86',2,net='gnd');dot(x+7,407)
text(105,248,'센서 5개',13,'#5c7e87','middle');text(103,338,'개별 0V 귀환',10,'#7e939c','middle')

# Relay coil and the isolated contact are deliberately separated.
dev('relayA')
rect(453,216,113,114,'#eff5f6',5)
text(510,240,'릴레이 코일',13,'#597986','middle')
path([(482,257),(482,301)],'#6b8b96',2);path([(538,257),(538,301)],'#6b8b96',2)
a('<path d="M482 264q10-12 20 0q10 12 20 0q8-10 16 0" stroke="#6b8b96" fill="none" stroke-width="2"/>')
text(510,319,'제어부 5V/0V-L',10,'#7c939c','middle');end()
path([(482,170),(482,257)],'#bd6f66',2.5,net='logic-power')
path([(538,301),(538,338)],'#278d86',3,net='gnd');rect(526,338,24,29,'#718a94',2);text(538,357,'Q',12,'#edf4f5','middle');path([(538,367),(538,407)],'#278d86',3,net='gnd');dot(538,407)
path([(397,269),(420,269),(420,352),(526,352)],'#597ac5',3,net='out12');text(425,254,'GPIO ×3',10,'#6d86ad','middle')
path([(644,138),(644,443)],'#cbbca4',2,'5 6')
text(644,472,'접점 절연 경계',12,'#a38a60','middle')
path([(566,273),(708,273)],'#afbac0',1.5,'4 4')
text(643,260,'기계적 작동',10,'#8b9ca4','middle')

# Contact, branch protection and three magnet returns.
path([(988,170),(798,170)],'#aa7941',3,net='mag-power');text(815,158,'+12V-MAG',12,'#aa7941')
text(740,210,'각 접점',11,'#aa7941');text(740,229,'독립 제어',11,'#aa7941')
for i in range(3):
 x=820+i*68
 path([(x,170),(x,204)],'#aa7941',2,net='mag-power');rect(x-9,204,18,14,'#e5d7bf',2);text(x,214,'F'+str(i+1),8,'#a68a61','middle')
 path([(x,218),(x,239)],'#aa7941',2,net='load'+str([12,10,9][i]));dot(x,239,'#aa7941');dot(x,279,'#aa7941');path([(x,239),(x+18,262)],'#aa7941',2,net='load'+str([12,10,9][i]));text(x+13,296,'RY'+str(i+1),9,'#a68a61')
 path([(x,279),(x,309)],'#aa7941',2,net='load'+str([12,10,9][i]));rect(x-23,309,46,39,'#dbe2df',4);text(x,334,'MAG'+str(i+1),10,'#738b87','middle')
 path([(x,348),(x,407)],'#aa7941',2.5,net='mag-ground');dot(x,407,'#aa7941')
path([(1058,224),(1058,407),(749,407)],'#aa7941',6,net='mag-ground')
dev('mag-ground');text(750,451,'0V-MAG  전자석 전용',18,'#aa7941');end()
text(641,405,'연결 없음',12,'#a58b65','middle')

# Audio stays on its separate 12V supply; signal ground is part of control domain.
dev('amp');rect(45,514,145,62,'#53506f',5);text(117,540,'HONGXING',15,'#f0edf5','middle');text(117,562,'별도 12V 어댑터 유지',10,'#c7c8d7','middle');end()
dev('mp3');rect(255,514,126,62,'#4c8d78',5);text(318,540,'KT403A',15,'#edf5f1','middle');text(318,562,'LINE + signal GND',10,'#c7ded4','middle');end()
path([(190,545),(255,545)],'#9a80ae',4,net='audio');text(222,530,'오디오',10,'#8f7e9e','middle')
path([(318,514),(318,482),(357,482),(357,407)],'#278d86',3,net='gnd');dot(357,407)
text(46,605,'앰프 전원을 PS-MAG에 합치면 오디오 GND로 절연을 우회할 수 있습니다.',11,'#8b9ca4')

# Motor current is confined to its loop. One reference bond to logic remains.
dev('psmotor');rect(699,529,132,60,'#44515c',5);text(765,554,'PS-MOT',15,'#e0ebf0','middle');text(765,575,'모터 기존 정격',10,'#afc1cc','middle');end()
dev('l298');rect(892,515,116,84,'#b84c48',4);rect(914,527,72,35,'#38434a',2);text(950,585,'L298N E6',13,'#f7ece6','middle');end()
dev('motor');a('<circle cx="1093" cy="553" r="28" fill="#e0e6e8" stroke="#a4b6bf" stroke-width="2"/>');text(1093,560,'M',21,'#627c89','middle');end()
path([(800,529),(800,504),(918,504),(918,515)],'#b37264',3,net='motor-supply')
path([(1008,543),(1065,543)],'#b37264',3,net='actuator');path([(1065,565),(1008,565)],'#8f72b8',3,net='actuator')
path([(950,599),(950,653),(732,653),(732,589)],'#8f72b8',6,net='motor-ground');dot(950,653,'#8f72b8')
dev('motor-ground');text(730,687,'0V-MOT  모터 전용 귀환',15,'#8f72b8');end()
path([(590,407),(602,407),(602,653),(732,653)],'#8f72b8',3,'7 4','motor-bond');dot(732,653,'#8f72b8')
text(591,636,'기준 GND 한 점 결합',11,'#8f72b8','end')
path([(397,310),(420,310),(420,492),(885,492),(885,545),(892,545)],'#8f72b8',2,net='motor4');text(651,512,'D4 / D5 / A2 → L298N',11,'#8f72b8','middle')
text(45,736,'전기적으로 공통: 0V-L ↔ 0V-MOT     /     전기적으로 분리: 0V-MAG     /     PE는 별도 함체 보호',13,'#597785')
a('</svg>')
(ROOT/'hardware/ground-topology.svg').write_text('\n'.join(s),encoding='utf-8')
print('Ground topology ready')
