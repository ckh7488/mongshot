from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
s=[]
def a(v):s.append(v)
def t(x,y,v,size=15,c='#557382',anchor='start'):a(f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" text-anchor="{anchor}">{escape(v)}</text>')
def p(pts,c='#6b9d9d',w=2):a('<path d="M'+'L'.join(f'{x} {y}' for x,y in pts)+f'" stroke="{c}" stroke-width="{w}" fill="none"/>')
def r(x,y,w,h,c,rx=3):a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>')
a('<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="840" viewBox="0 0 1180 840"><style>text{font-family:"Malgun Gothic",Arial,sans-serif}</style>')
t(42,48,'외부 LED / 진행 버튼 · 실제 접속 핀',24)
t(42,81,'5mm 저전류 LED 6개 + SN74HC595N + 각 1.5kΩ · 기존 Gun/Hint 배선을 제거한 D11/A3를 새 기능으로 사용',13,'#91a2ab')
r(420,150,258,430,'#334d5b',9);t(549,184,'SN74HC595N',20,'#e9f0f3','middle');t(549,208,'PDIP-16 · 상면 기준',12,'#a8becb','middle')
left=[(14,'SER','D11',255),(11,'SRCLK','D13',310),(12,'RCLK','D7',365),(10,'/SRCLR','5V',420),(13,'/OE','G0',475)]
for pin,name,label,y in left:
 t(52,y+5,label,17);p([(170,y),(420,y)]);t(409,y-8,str(pin),11,'#93aab6','end');t(438,y+5,name,13,'#cadbe4')
t(470,552,'16 VCC → 5V',13,'#cadbe4');t(470,573,'8 GND → G0',13,'#cadbe4')
right=[(15,'QA','액자'),(1,'QB','조명'),(2,'QC','열쇠'),(3,'QD','RFID'),(4,'QE','책'),(5,'QF','완료')]
for i,(pin,name,label) in enumerate(right):
 y=249+i*51;t(660,y+5,name,13,'#cadbe4','end');t(687,y-8,str(pin),11,'#93aab6');p([(678,y),(760,y)]);r(760,y-8,64,16,'#dbcaa7',2);t(792,y+5,'1.5k',10,'#9b875e','middle');p([(824,y),(880,y)]);a(f'<circle cx="892" cy="{y}" r="10" fill="#b5d8c3" stroke="#78a391"/>');p([(902,y),(958,y),(958,560)]);t(1000,y+5,label,15)
p([(958,560),(958,597),(680,597)]);t(790,621,'LED 음극 공통 → G0',13,'#87a1af')
t(421,619,'QG(6), QH(7), QH′(9): 미접속',12,'#8da4b1')
t(47,663,'진행 버튼: A3 / INPUT_PULLUP',18)
p([(190,723),(480,723),(570,723)]);t(58,730,'A3',17);r(270,715,66,16,'#dbcaa7',2);t(303,727,'1k',10,'#9b875e','middle');p([(400,723),(400,687)]);t(400,681,'4.7k → 5V',12,'#91a4b0','middle')
p([(480,723),(480,770)]);t(480,795,'100nF → G0',12,'#91a4b0','middle');p([(570,723),(590,708)]);p([(610,723),(720,723),(720,763)]);t(625,700,'NO 순간 버튼',13,'#91a4b0','middle');t(720,789,'G0',12,'#91a4b0','middle')
t(790,691,'2초 누르면 현재 입력 단계 1회 완료',14);t(790,723,'누른 채 유지: 반복 넘김 없음',14);t(790,755,'기존 대기시간: 유지 / LED 점멸',14)
t(42,826,'595 VCC/GND 바로 옆 100nF 필수 · 12V 패널 램프를 이 회로에 직접 연결하지 않음 · SPI.begin()은 사용하지 않음',12,'#91a2ab')
a('</svg>')
(ROOT/'hardware/frontpanel-circuit.svg').write_text('\n'.join(s),encoding='utf-8')
print('Front-panel wiring ready')
