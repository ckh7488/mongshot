import html
"""Readable SVGs, offline interface and installation documents for v5."""
from pathlib import Path
from html import escape as E
import json,re,base64,xml.etree.ElementTree as ET
ET.register_namespace('','http://www.w3.org/2000/svg')

class SVG:
    def __init__(self,w,h,id,title):
        self.o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" id="{id}" role="img" aria-label="{E(title)}"><style>text{{font-family:"Malgun Gothic",Arial,sans-serif}}.device{{cursor:pointer;outline:none}}.selected-device{{filter:drop-shadow(0 0 4px #16a798)}}.selected-net{{stroke-width:5!important;opacity:1!important}}.dim-net{{opacity:.18}}.power-net{{display:none}}.show-power .power-net{{display:initial}}</style>']
    def add(self,s):self.o.append(s)
    def rect(self,x,y,w,h,c='#fff',stroke='#c8d6de',rx=5,extra=''):self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}" stroke="{stroke}" {extra}/>')
    def text(self,x,y,s,size=18,c='#405e70',anchor='start',weight=500):self.add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{c}" text-anchor="{anchor}">{E(str(s))}</text>')
    def line(self,pts,c='#688d99',w=3,net=None,extra=''):
        self.add('<path d="M'+' L'.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'+(f' class="net" data-net="{net}"' if net else '')+f' {extra}/>')
    def circle(self,x,y,r,c='#d3dce0',stroke='none',extra=''):self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{stroke}" {extra}/>')
    def finish(self):return '\n'.join(self.o+['</svg>'])

def render_all(root,m,details,graph,bom,wires,gports,positive,landing,sources,table):
    H=root/'hardware';S=root/'simulation/source';archive=root/'archive/v4-sources'
    def write(rel,s):p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
    C={'P0':'#b87e49','G0':'#238b86','A0':'#9475aa','PE':'#79984a','BOUNDARY':'#617b96'}
    ns={'s':'http://www.w3.org/2000/svg'};old=ET.parse(H/'cabinet-layout.svg').getroot()
    devs={g.attrib['data-part']:g for g in old.findall('s:g',ns) if 'data-part' in g.attrib}
    defs=ET.tostring(old.find('s:defs',ns),encoding='unicode')
    def native(s,id,x,y,w,h,bounds):
        bx,by,bw,bh=bounds;k=min(w/bw,h/bh)
        s.add(f'<g transform="translate({x-bx*k} {y-by*k}) scale({k})">'+ET.tostring(devs[id],encoding='unicode')+'</g>')
    # Same scale for both physical bays: 2 SVG px per mm.
    s=SVG(1320,2020,'redesign-svg','v5 상하 배전함 실장 배치. 절연 로직, 소형 제어함과 최소 접속부')
    s.add(defs);s.rect(0,0,1320,2020,'#f7fafc','none',0)
    s.text(100,48,'MONG SHOT  /  COMPACT CABINET 05',25,'#35576c',weight=700)
    s.text(100,83,'400mm 유효 폭 · 상부 260 / 하부 560mm · 같은 축척',20,'#8296a2')
    X=110;Y={'upper':160,'lower':790}
    def xy(b,x,y):return X+2*x,Y[b]+2*y
    def lr(b,x,y,w,h,*a,**kw):xx,yy=xy(b,x,y);s.rect(xx,yy,2*w,2*h,*a,**kw)
    for bay,hh,title in [('upper',260,'상부 · AC / 전원'),('lower',560,'하부 · 부하 / 절연 / 제어')]:
        yy=Y[bay];s.rect(X-22,yy-22,844,2*hh+44,'#b8c7cf','#9baeb9',12);s.rect(X,yy,800,2*hh,'#f0f5f7','#bccbd3',3)
        s.text(X,yy-40,title,24,weight=650)
        for v in range(0,401,50):
            xx=X+v*2;s.line([(xx,yy),(xx,yy+8)],'#a9bbc5',1);s.text(xx,yy-6,v,12,'#9aadb7','middle')
        s.line([(75,yy),(75,yy+2*hh)],'#9eafb9',1.5);s.text(65,yy+hh,str(hh)+'mm',16,'#8095a2','end')
    for b,ducts in [('upper',m['ducts']['upperVertical']),('lower',m['ducts']['lowerVertical']+m['ducts']['lowerHorizontal'])]:
        for x,y,w,h in ducts:
            lr(b,x,y,w,h,'#dce5ea','#c0cdd5',2)
            if w>h:
                for v in range(int(x)+4,int(x+w),8):xx,yy=xy(b,v,y+2);s.line([(xx,yy),(xx,yy+2*h-8)],'#c0cdd5',2)
            else:
                for v in range(int(y)+4,int(y+h),8):xx,yy=xy(b,x+2,v);s.line([(xx,yy),(xx+2*w-8,yy)],'#c0cdd5',2)
    for p in m['parts']:
        x,y=xy(p['bay'],p['x'],p['y']);rw,rh=p['reserveW']*2,p['reserveH']*2
        s.rect(x,y,rw,rh,'#fff','#c5d3dc',5,extra='fill-opacity=".45" stroke-dasharray="5 4"')
        s.text(x+4,y-5,p['id'].upper()+f" ({p['x']},{p['y']})",12,'#879ba7')
        # Body footprint is exact for catalog parts and explicitly assumed for legacy equipment.
        bx=x+(rw-2*p['bodyW'])/2;by=y+2*p.get('bodyOffsetY',4);bw=p['bodyW']*2;bh=p['bodyH']*2
        s.add(f'<g class="device" data-part="{p["id"]}" tabindex="0" role="button" aria-label="{E(p["name"])}">')
        id=p['id']
        if id in ['uno','relayA','relayB','l298','amp','mp3']:
            bounds={'uno':(332,501,307,226),'relayA':(258,303,276,150),'relayB':(609,303,276,150),'l298':(709,520,175,215),'amp':(262,105,287,140),'mp3':(669,105,174,140)}[id]
            native(s,id,bx,by,bw,bh,bounds)
        elif id=='smps':
            s.rect(bx,by,bw,bh,'#b6c4cc','#879da9',4);s.rect(bx+5,by+5,bw-10,bh-42,'#d9e0e5','#a8bac5',2)
            for row in range(8):
                for col in range(19):s.circle(bx+15+col*15,by+15+row*20,4,'#a6b6c0')
            s.rect(bx+bw-115,by+20,100,118,'#edf2f5','#c2cfd6',4);s.text(bx+bw-65,by+68,'12V',27,anchor='middle');s.text(bx+bw-65,by+95,'LRS-200',13,anchor='middle')
            for i,lab in enumerate(['L','N','PE','V−','V−','V+','V+']):
                xx=bx+20+i*55;s.rect(xx,by+bh-32,43,26,'#546976','none',2);s.circle(xx+21,by+bh-19,7,'#a7b8c2');s.text(xx+21,by+bh+19,lab,14,'#688390','middle')
        elif id=='rfidbox':
            s.rect(bx,by,bw,bh,'#aebcc7','#8198a7',7);s.rect(bx+7,by+7,bw-14,bh-14,'#d8e0e6','#bbc9d2',5)
            for xx in [bx+17,bx+bw-17]:
                for yy in [by+17,by+bh-17]:s.circle(xx,yy,4,'#8ea3af')
            s.rect(bx+35,by+45,bw-70,60,'#eff3f6','#c5d2da',4);s.text(bx+bw/2,by+83,'RFID CONTROL',22,anchor='middle')
            s.text(bx+bw/2,by+137,'160 × 100 × 65*',17,'#7b909d','middle')
            for i in range(4):s.rect(bx+40+i*50,by+bh-20,30,14,'#687c89','none',2)
        elif id in ['power-ground','mag-power','gnd','logic-positive']:
            count=1
            for row in range(count):
                yy=by+row*77;color='#6d9ab1' if id in ['power-ground','gnd'] else '#be7775'
                s.rect(bx,yy,116.2,57.2,color,'#8095a2',5);s.circle(bx+13,yy+28,8,'#385466')
                for j in range(12):
                    xx=bx+36+(j%6)*13;sy=yy+15+(j//6)*27;s.circle(xx,sy,4,'#365060');s.rect(xx-3,sy+7,6,4,'#dfb16e','none',1)
            s.text(bx+58,by+37,{'power-ground':'P0','mag-power':'P12','gnd':'G0','logic-positive':'5L'}[id],16,'#f4f8fb','middle')
        elif id=='magdiodes':
            for j in range(3):
                yy=by+7+j*30;s.line([(bx+bw/2,yy-6),(bx+bw/2,yy+24)],'#9aaeb7',2);s.rect(bx+1,yy,bw-2,19,'#2c3d45','none',2);s.line([(bx+1,yy+4),(bx+bw-1,yy+4)],'#dddcd0',3)
        elif id=='isolated5':
            s.rect(bx,by,bw,bh,'#e6e3dc','#a9aaa3',3);s.rect(bx+3,by+32,bw-6,bh-64,'#f4f2ec','#d2d0c8',1)
            for yy in [by+12,by+bh-22]:
                for xx in [bx+9,bx+bw-9]:s.circle(xx,yy,5,'#78858a')
            s.text(bx+bw/2,by+bh/2-10,'DDR',12,anchor='middle');s.text(bx+bw/2,by+bh/2+10,'15G',12,anchor='middle');s.text(bx+bw/2,by+bh/2+30,'5V',14,C['G0'],'middle')
        elif id=='ac':
            s.rect(bx,by,bw,bh,'#e8e7e0','#aab6b9',3);s.rect(bx+20,by+40,25,58,'#465763','none',3);s.text(bx+bw/2,by+bh-10,'AC',18,anchor='middle')
        elif id=='pe':
            s.rect(bx,by,bw,bh,'#a7ba79','#869e5f',3)
            for j in range(4):s.circle(bx+bw/2,by+20+j*38,8,'#b8ab7b')
        elif id=='amp-adapter':
            s.rect(bx,by,bw,bh,'#485867','#344653',9);s.rect(bx+20,by+20,bw-40,bh-40,'#d9e1e6','none',2);s.text(bx+bw/2,by+50,'기존 DC',18,anchor='middle')
        else:
            s.rect(bx,by,bw,bh,'#508b7c','#346b5e',3)
            for xx in [bx+6,bx+bw-6]:
                for yy in [by+6,by+bh-6]:s.circle(xx,yy,3,'#bfd0c8')
            if id in []:
                s.line([(bx+bw/2,by+4),(bx+bw/2,by+bh-4)],'#ebf1f3',5,extra='stroke-dasharray="4 4"')
            if id=='buck':s.rect(bx+8,by+8,28,28,'#ad9c6c','#82714c',3)
        s.add('</g>');s.text(x+rw/2,min(y+rh-6,by+bh+34),'D×3' if id=='magdiodes' else p['name'],12 if id=='magdiodes' else 17,C[p['domain']],'middle',650)
    # Existing passage: symbolic location only, not a new drilling instruction.
    s.rect(265,715,490,42,'#40586b','#253e51',16);s.text(510,744,'기존 상하 관통구 · DC 전원 묶음만',18,'#edf3f6','middle')
    # Optional representative routing lines; each actual conductor has its own schedule row.
    s.add('<g class="power-net">')
    s.line([(170,620),(135,620),(135,740),(130,740),(130,1540)],C['P0'],4,'P0')
    s.line([(390,620),(145,620),(145,730),(140,730),(140,1530)],'#bd6d60',4,'P0')
    s.line([(620,620),(800,620),(800,740),(885,740),(885,1045)],C['A0'],4,'A0')
    s.line([(355,1775),(430,1775),(430,1745),(700,1745)],C['G0'],4,'G0')
    s.add('</g>')
    def card(y,title,lines):
        s.rect(970,y,320,70+len(lines)*34,'#fff','#d8e2e8',9);s.text(988,y+34,title,20,weight=650)
        for i,v in enumerate(lines):s.text(988,y+68+i*34,v,17,'#7b92a0')
    card(145,'01 · 줄인 것',['추가 퓨즈/홀더 전부 제외','현장 DIN 단자24개 삭제','RFID·홍싱 확보 면적 축소','센서판·자석접속판 삭제'])
    card(420,'02 · 남긴 분배블록',['파랑2: P0 / G0 각각1','빨강2: P12 / 5L 각각1','5L/5D 양극은 합치지 않음','기존 PE 접지부는 보존'])
    card(800,'03 · 기존 GPIO 직결',['추가 절연모듈/고정판 제거','P0/G0는 전기적으로 공통','부하 전력 귀환은 별도 분기','기존 센서 신호/귀환 실물 대조','홍싱: 기존 라인/GND 직결'])
    card(1120,'04 · 이더넷 심선',['+와−를 원래 꼬임쌍으로','병렬은 여분 페어 확인 후','Cu/CCA·AWG·길이 기록','전압강하 ≠ 허용전류 판정'])
    card(1410,'05 · 크기와 도어',['RFID 160×100×65*','홍싱 140×90×45*','* 실측 전 배치 가정','도어 180×75 / 후면45','릴레이 맞은편에 표시판'])
    card(1720,'06 · 재결선 순서',['핀 기준 양끝 라벨 → 철거','전원 → 절연 경계 → 신호','케이블별 연속성/전류 확인','자석 해제·리셋 파형 시험'])
    s.text(110,1976,'실선 몸체 / 점선 배선 포함 확보 영역 · 실장 좌표와 전기적 절연은 별도 검증 · 나사홀은 실물 전사',17,'#8296a2')
    svg=s.finish()
    # Prefix every imported id/reference, including native board filters and pins.
    for ident in re.findall(r'\bid="([^"]+)"',defs):svg=svg.replace('id="'+ident+'"','id="v5-'+ident+'"').replace('url(#'+ident+')','url(#v5-'+ident+')').replace('href="#'+ident+'"','href="#v5-'+ident+'"')
    write('hardware/cabinet-redesign.svg',svg)

    # Ground topology: separate rails, barriers rather than disguised links.
    g=SVG(1240,1050,'ground-topology-svg','P0 부하 / G0 로직·MP3·홍싱 / PE 보호접지')
    g.rect(0,0,1240,1050,'#f8fafc','none',0);g.text(35,48,'GND · 직접 이어지는 선과 절연 경계를 구별',28,weight=650)
    g.text(35,82,'P0/G0 공통 기준선 있음 · 귀환 분배는 절연이 아닙니다 · 자석−도 공통입니다.',17,'#8296a2')
    for x,w,c,title in [(30,360,C['P0'],'P0 · 12V 부하측'),(850,360,C['G0'],'G0 · 로직 귀환 분기')]:
        g.rect(x,120,w,700,'#fff',c,10);g.text(x+22,157,title,24,c,weight=650)
    left=[(215,'SMPS V− → P0.IN'),(290,'자석1 / 자석2 / 자석3 −'),(365,'L298 GND / Vs·Vss 기준'),(440,'DC-D GND → 릴레이 코일'),(515,'RFID·12V센서 전원 −'),(590,'DC-L 입력 −'),(665,'릴레이 코일 귀환')]
    right=[(215,'DC-L 출력 − → G0.IN'),(290,'Arduino GND'),(365,'액자·책 리드 귀환'),(440,'센서 A0/A1/A5: 기존선 대조'),(515,'KT403A GND'),(590,'LED·버튼 GND'),(665,'L298 공통 신호기준')]
    for x,rows,c in [(55,left,C['P0']),(875,right,C['G0'])]:
        g.line([(x,190),(x,760)],c,5,'P0' if x<100 else 'G0')
        for y,txt in rows:g.line([(x,y),(x+25,y)],c,3);g.circle(x,y,4,c);g.text(x+34,y+6,txt,16)
    for y,title,sub in [(190,'DC-L · 전원 분기 후보','소자 절연 ≠ 현재 시스템 절연'),(335,'기존 제어선 직결','모터3선·릴레이4선 / 추가모듈 없음'),(480,'별도 센서 PCB 없음','기존 신호/귀환 실물 대조'),(625,'공통 신호 기준 필요','G0.4 → L298 GND')]:
        g.rect(425,y,390,105,'#fff','#c4d3dd',8);g.text(620,y+34,title,19,anchor='middle');g.text(620,y+70,sub,16,'#8298a5','middle');g.line([(610,y+85),(610,y+97)],'#94a9b6',2);g.line([(626,y+85),(626,y+97)],'#94a9b6',2)
    g.line([(55,760),(55,790),(875,790),(875,760)],'#927d4b',4);g.text(620,818,'P0 = G0 · 공통 기준선 / 갈바닉 절연 아님',17,'#927d4b','middle')
    g.rect(30,850,535,145,'#eef7f6',C['G0'],8);g.text(50,885,'홍싱 · 기존 어댑터 사용',23,C['G0']);g.text(50,920,'MP3 L/R와 GND를 홍싱 MP3 IN에 직결',18);g.text(50,953,'홍싱 전원−는 G0와 공통. 전원+는5L과 합치지 않음',17)
    g.rect(600,850,610,145,'#f3f7ee',C['PE'],8);g.text(620,885,'PE · 콘센트 보호접지',23,C['PE']);g.text(620,920,'기존 PE → SMPS FG / 금속 외함 / 도어',18);g.text(620,953,'P0·G0 귀환 대용 금지 · 보호접지를 끊어 절연하지 않음',17)
    g.text(35,1030,'이 모델은 공통0V의 귀환 분기를 표시합니다. 기생용량·전자파·공유 AC 전원 변동까지 0이 되는 것은 아닙니다.',17,'#879ba7')
    write('hardware/ground-topology.svg',g.finish())

    # Practical wiring schematic for the interfaces that make isolation real.
    q=SVG(1260,1640,'interface-svg','기존 모터/릴레이 직결, 공통GND와 자석 다이오드')
    q.rect(0,0,1260,1640,'#f8fafc','none',0);q.text(35,45,'기존 GPIO 직결 · 실제 핀과 전원',29,weight=650)
    q.text(35,82,'기존 GPIO와 공통GND로 연결합니다. 아래는 저전압 DC 회로이며 추가 절연모듈은 없습니다.',17,'#8397a3')
    def box(x,y,w,h,title,c):q.rect(x,y,w,h,'#fff',c,8);q.text(x+20,y+34,title,21,c,weight=650)
    box(35,115,1185,305,'모터 · 기존 제어선 직결',C['P0'])
    for i,(pin,target) in enumerate([('D4','IN1'),('D5','IN2'),('A2','ENA')]):
        yy=200+i*60;q.text(65,yy,'Arduino '+pin,20);q.line([(280,yy-6),(820,yy-6)],C['G0'],3);q.text(860,yy,'L298 '+target,20)
    q.text(55,390,'GND-MOTOR-REF: G0.4 → L298 GND. P0-MOTOR 전력 귀환은 별도 유지.',19)
    q.text(40,454,'L298 Vs=P12 / Vss=5D. 전원5V-EN과 ENA 점퍼, 리셋 기본상태는 기존 모듈에 대조.',17)
    box(35,490,1185,185,'릴레이 · 기존 모듈 입력 직결',C['P0'])
    q.text(55,565,'Arduino D12 / D10 / D9 / A4 → RY-A IN1 / IN2 / IN3 / IN4',21)
    q.text(55,604,'추가 ISO-M / ISO-R 없음. 기존 VCC/JD-VCC/GND와 입력 바이어스·active LOW 확인.',18)
    q.text(55,643,'P0/G0 공통 기준. 릴레이 접점/다이오드가 전체 시스템 GND 절연을 뜻하지는 않습니다.',17,'#8498a4')
    box(35,710,1185,335,'기존 센서 배선 보존 · 새 센서판 없음',C['G0'])
    q.text(60,790,'D8 액자 / D6 책: 기존 리드 신호와 G0 귀환. D6 기존100Ω 보존.',20)
    q.text(60,850,'A0 조명 / A1 열쇠 / A5 RFID: 기존 접속을 기록하고 실제 신호/귀환을 대조.',20)
    q.text(60,910,'12V 전원 장치라고 신호도12V인 것은 아닙니다. Arduino에12V 신호를 직결하지 않습니다.',18)
    q.text(60,970,'이 세 신호의 실제 출력/귀환 확인 전 전체 GND 절연이 완성됐다고 표시하지 않습니다.',18,'#a17d52')
    box(35,1080,1185,330,'자석 다이오드 · 별도 PCB 없이 릴레이 근처에서 병렬 연결',C['P0'])
    # Load-side rails; the diode is not across COM/NO.
    q.text(65,1158,'RY 선택접점 뒤 → 자석 +',19,C['P0']);q.text(65,1355,'P0 귀환 → 자석 −',19,C['P0'])
    q.line([(350,1150),(870,1150),(870,1190)],C['P0'],3);q.line([(350,1345),(870,1345),(870,1305)],C['P0'],3)
    q.rect(825,1190,90,115,'#d8e3e8','#8a9fac',5);q.text(870,1254,'자석',20,anchor='middle')
    q.line([(565,1150),(565,1220)],'#506a7c',3);q.line([(565,1270),(565,1345)],'#506a7c',3)
    q.add('<path d="M545 1270 L585 1270 L565 1230 Z" fill="none" stroke="#506a7c" stroke-width="3"/>');q.line([(543,1225),(587,1225)],'#506a7c',4)
    q.text(615,1215,'K · 줄 표시 → +',19);q.text(615,1300,'A → −',19)
    q.text(960,1195,'자석별1개',19);q.text(960,1233,'D-M1 / D-M2 / D-M3',17);q.text(960,1270,'극성 반대면 단락',17,'#b16e61')
    q.text(60,1385,'각 리드 절연·고정. COM–NO 사이 아님. 긴 선 서지/해제시간은 실측. 필요 시 억제방식 조정.',18,'#8396a3')
    box(35,1445,1185,150,'기존 오디오 · 절연 트랜스 없음',C['G0'])
    q.text(60,1514,'KT403A DAC_L/R 및 GND → HONGXING MP3 IN L/R 및 GND. 기존 라인오디오 결선 보존.',18)
    q.text(60,1558,'홍싱은 기존 어댑터 사용. 전원−는 오디오GND와 공통, 전원+는 로직5V에 합치지 않음. P0 연결 금지.',17,'#8396a3')
    write('hardware/isolation-interfaces.svg',q.finish())

    # Human-readable sections, no giant terminal bars.
    ground='<section class="fit-sheet"><h2>공통 GND · 분기별 귀환 포트</h2><p><b>P0와 G0는 공통 신호 기준선으로 연결됩니다.</b> 릴레이/모터 전류는 P0로, Arduino/MP3/리드/도어 전류는 G0로 돌아갑니다. 남은 파란 분배블록2개는 귀환 분기이며 전기적으로 공통입니다.</p>'+table(['분배부','포트','연결 대상','선 라벨'],gports)+'<h3>양극도 섞지 않음</h3>'+table(['분배부','포트','연결 대상'],positive)+'<h3>공통 기준선 검증</h3><p id="isolation-result" role="status"></p><p>이 결과는 지정된 배선 그래프의 DC 연결성입니다. 현장의 USB·실드·볼트·보드 배선까지 자동 검증한 것은 아닙니다. 전원 차단·잔류전압 확인 후 양방향 저항을 보고, 실드/오디오 연결 전후를 비교합니다. 도통음 한 번으로 절연을 인증하지 않습니다.</p></section>'
    write('simulation/source/ground-table.html',ground)
    bh=['ID','부품 / 품번','수량','장소 / 크기','조건 / 상태','자료']
    brows=[]
    for it in bom['items']:
        row=[it['id'],it['maker']+' '+it['part'],it['qty'],it['location']+' / '+it['size'],it['condition']+' / '+it['status'],it['url']]
        brows.append(row)
    bhtml='<section class="fit-sheet"><h2>v5 제품 BOM · 덜어낸 것과 추가한 것</h2><p>삭제: <b>추가 메인/분기 퓨즈, PT2.5 현장단자24개, 그 전용 커버/엔드브래킷, 0V-LINK</b>. 기존 차단기와 PE는 보존합니다.</p><p>추가: 로직5V 전원분기 후보, 부하5V, 자석 다이오드3개, 기존 오디오 직결. 새 센서판과 자석 접속PCB, 그 전용 MPT단자10개는 제거했습니다. 자석 다이오드는 릴레이 옆 배선에 절연 고정합니다.</p>'+table(bh,brows)+'<h3>제작/실측이 남은 항목</h3>'+table(['항목','조건'],[[x['name'],x['reason']] for x in bom['unselected']])+'<p>추가 GPIO 절연모듈/캐리어/전용저항은 제외했습니다. 제조사 재고·대체품은 발주 시 재확인합니다.</p></section>'
    # Convert escaped official URLs to links within the generated cell.
    bhtml=re.sub(r'<td>(https://[^<]+)</td>',r'<td><a href="\1" target="_blank" rel="noopener">공식 자료</a></td>',bhtml)
    write('simulation/source/bom-view.html',bhtml)
    fields=[('fit-width','유효 폭',400),('fit-upper','상부 높이',260),('fit-lower','하부 높이',560),('fit-depth','유효 깊이',120),('fit-rfid-w','RFID 폭*',160),('fit-rfid-h','RFID 높이*',100),('fit-rfid-d','RFID 깊이*',65),('fit-amp-w','홍싱 폭*',140),('fit-amp-h','홍싱 높이*',90),('fit-amp-d','홍싱 깊이*',45)]
    fit='<section class="fit-sheet"><h2>실물 치수 대조 · 줄인 배치를 그대로 들어가게</h2><p>기존 하부 높이650mm 계획을 <b>560mm</b>로 줄였습니다. RFID 확보280×220→170×130mm, 홍싱190×110→170×110mm. 홍싱은 몸체 폭을 줄이고 커넥터 여유를 확보했습니다. *몸체값은 실측 전 계획 가정입니다.</p><div class="fit-inputs">'+''.join(f'<label>{lab} mm<input type="number" id="{id}" min="1" value="{val}"></label>' for id,lab,val in fields)+'</div><div id="fit-result" class="fit-result" role="status"></div><h3>부품별 좌표 · 케이블 포함 확보 구역</h3>'+table(['부품','구역','X,Y','확보 W×H','몸체 W×H×D','근거'],[[p['name'],p['bay'],f"{p['x']},{p['y']}",f"{p['reserveW']}×{p['reserveH']}",f"{p['bodyW']}×{p['bodyH']}×{p['bodyD']}",p['basis']] for p in m['parts']])+'<p>방열 조건은 단순 외곽 적합과 별도입니다. DDR는 수직 DIN 장착과 제조사 설치 간격/온도경감을 지키고, SMPS 주변 발열체와 케이블이 통풍을 막지 않게 합니다. 나사홀은 실물로 전사합니다.</p></section>'
    write('simulation/source/fit-view.html',fit)
    cable='<section class="fit-sheet"><h2>얇은 이더넷 심선 · 자석 전원 검토</h2><p>아래 기본값은 <b>24AWG 구리 케이블의 계산 예시</b>입니다. 설치 케이블이 Cu/CCA인지, 24/26/28AWG인지, 실제 길이와 자석 전류를 확인하기 전 그대로 사용 가능하다고 판정하지 않습니다.</p><div class="fit-inputs cable-inputs">'
    for id,lab,val,step in [('wire-voltage','실제 전원 V',12,.1),('wire-length','편도 길이 m',10,.1),('wire-current','코일 전류 A',.5,.01),('wire-resistance','단심 저항 Ω/m @20°C',.0938,.001),('wire-temp','구리 온도 °C',20,1),('wire-pairs','병렬 페어 수',1,1),('wire-contact','접속부 합산 저항 Ω',0,.01)]:
        cable+=f'<label>{lab}<input id="{id}" type="number" value="{val}" step="{step}" min="{1 if id=="wire-pairs" else 0}"'+(' max="4"' if id=='wire-pairs' else '')+'></label>'
    cable+='</div><div id="wire-result" class="fit-result conditional" role="status"></div><div id="wire-compare"></div><p><b>전압강하 계산은 허용전류 합격 판정이 아닙니다.</b> 외피/다발/주변온도/접촉/단락을 따로 확인해야 합니다. 5%는 이 화면의 비교 기준이며 제품 규정이 아닙니다. 접속부 저항0은 이상화한 기본값입니다. CCA는 구리 온도모델을 적용하지 말고 실제 저항/제조사 자료를 사용합니다.</p><h3>페어 배정 원칙</h3><p>각 원래 꼬임쌍 안에 +와−를 넣습니다. 병렬은 사용하지 않는 페어를 확인한 뒤 양끝에서 +끼리/−끼리 동일하게 묶습니다. 신호가 이미 쓰는 심선을 임의로 전원에 합치지 않습니다. 한 가닥 신호에 여러 자석의 공통 귀환을 태우지 않습니다.</p>'+table(['회로','기본 배정','늘릴 때'],[['자석1/2/3','각 케이블 한 페어에 +/−','남는 페어가 확인됐을 때만 2/4페어 병렬'],['12V센서','전원 P12/P0 한 페어 + 옵토입력 한 페어','센서 종류별 실제 루프를 따라 라벨'],['액자/책 리드','신호/G0 한 페어','1k/100nF 필터; D6 기존100Ω 보존'],['모터','OUT1/OUT2 한 페어','정지/기동 전류가 큼. 스톨전류/전압강하 확인 전 사용 확정 금지']])+'<h3>얇은 선은 어디에 꽂나?</h3><p>PTFIX는 가는 단선에서 <b>주황 버튼을 눌러 삽입</b>합니다. 제조사의 직접 Push-in 최소 굵기와 접속 가능한 최소 굵기는 다릅니다. 센서/기존 릴레이/L298 단자는 실제 지원 굵기를 확인해 연결합니다. 단선은 맞는 규격으로 직접 조이고, 여기에 허용되지 않는 큰 페룰을 씌우지 않습니다. 외피를 고정해 심선이 굽힘 하중을 받지 않게 합니다.</p><div class="fit-warning">추가 퓨즈는 요청대로 제외했습니다. 기존 차단기/PE는 유지합니다. SMPS의 총 과전류 보호가 얇은 심선 각각을 보호하는 것은 아니므로, 부하 전류·배선 저항·온도·고장 시 전류 제한을 확인하기 전 현장선 전원 투입을 승인한 설계로 보지 않습니다.</div></section>'
    write('simulation/source/cable-view.html',cable)
    review='<section class="fit-sheet"><h2>v5.3 · 추가 절연모듈 제거</h2><p>모터/릴레이 절연모듈2개와 고정판·전용저항14개를 제거했습니다. 기존 GPIO를 L298/릴레이에 직결합니다.</p><h3>P0와 G0는 전기적으로 공통</h3><p>G0.4→L298 GND의 기준선이 있으므로 두 분배부는 절연된 GND가 아닙니다. 같은12V를 쓰는 자석−도 공통입니다. 부하 전류는 별도 전력 귀환으로 배선하여 Arduino/센서 귀환에 직렬로 통과시키지 않습니다.</p><h3>5V 변환기</h3><p>5D는 릴레이/L298용,5L은 Uno/MP3용 전원 분기입니다. 두 양극을 합치지 않습니다. DDR 소자 자체는 절연형이지만 현재 공통 기준선이 시스템 절연을 우회합니다. 절연형 변환기는 현 구성의 필수가 아니며 전원부 선택은 별도 검토 상태로 남겼습니다.</p><h3>기존 부품 사용</h3><p>새 센서판/자석접속판/오디오절연판 없음. 자석별 다이오드3개는 릴레이 근처 자석+/− 사이에 병렬 고정합니다. K줄=+,A=−,COM–NO 사이 아님. MP3/홍싱은 기존 라인·GND 직결이고 홍싱 기존 어댑터를 씁니다.</p><p>기존 센서 출력/귀환, 케이블 정격과 치수, 릴레이8채널/점퍼/리셋 동작은 실제 자료에 대조합니다. 추가모듈 제거와 현장 무고장 검증을 같은 뜻으로 표시하지 않습니다.</p></section>'
    write('simulation/source/review-view.html',review)
    plain=re.sub(r'<[^>]+>', '',review.replace('</h2>','\n\n').replace('</h3>','\n\n').replace('</p>','\n\n'))
    write('docs/11-design-review.md','# 11. 설계 이유와 최종 검토\n\n'+html.unescape(plain)+'\n\n[전력 예산](../hardware/power-budget.csv) · [전원 대안](../hardware/power-decisions.json) · [센서별 적용](../hardware/sensor-interface-modes.csv) · [제조사 자료](../hardware/source-register.json)\n')

    from direct_control_docs import write_docs
    write_docs(root,m,bom,review)

    # Offline workbench. Retain the tested AVR runtime, replace only design data/UI.
    page=(archive/'simulation__source__page.html').read_text(encoding='utf-8')
    page=page.replace('상하 함체 실장안 · 2026.11.03','v5.3 · 기존 GPIO 직결 / 공통GND')
    page=page.replace('<button type="button" data-view="cabinet">기능·배선 보기</button>','<button type="button" data-view="gnd">GND 구조</button><button type="button" data-view="interfaces">직결·다이오드</button><button type="button" data-view="cable">이더넷 심선</button><button type="button" data-view="labels">핀·라벨</button>')
    page=page.replace('12V SMPS 1대 + 5V DC-DC · RFID 회색함·릴레이 2장 · 외부 진행 표시','기존 모터/릴레이 GPIO 직결 · P0/G0 공통 · 추가 절연모듈 없음')
    page=re.sub(r'<div class="domain-notice" id="domain-notice">.*?</div>','<div class="domain-notice" id="domain-notice"><strong>v5.3: 기존 GPIO 직결 / P0·G0 공통</strong> · 추가 절연모듈 없음 · 자석−도 공통GND · 부하 전력 귀환은 별도 배선</div>',page)
    page=page.replace('<div id="ground-drawing" hidden>{{GROUND_SVG}}{{GROUND_TABLE}}</div>','<div id="ground-drawing" hidden>{{GROUND_SVG}}{{GROUND_TABLE}}</div><div id="interfaces-drawing" hidden>{{INTERFACES_SVG}}</div><div id="cable-drawing" hidden>{{CABLE_VIEW}}</div><div id="labels-drawing" hidden>{{LABELS_VIEW}}</div>')
    page=page.replace('0V-L 공통 버스','G0 · 로직 전용 기준')
    page=page.replace('<button type="button" data-view="labels">핀·라벨</button>','<button type="button" data-view="labels">핀·라벨</button><button type="button" data-view="review">설계 이유</button>')
    page=page.replace('<div id="cable-drawing" hidden>{{CABLE_VIEW}}</div>','<div id="cable-drawing" hidden>{{CABLE_VIEW}}</div><div id="review-drawing" hidden>{{REVIEW_VIEW}}</div>')
    viewer='<div id="cabinet-3d" class="cabinet-3d"><div class="three-toolbar"><span class="three-badge">3D 로딩</span><button type="button" data-3d="front">정면</button><button type="button" data-3d="iso">입체</button><button type="button" data-3d="fit">전체 맞춤</button><button type="button" data-3d="zoomin" aria-label="3D 확대">＋</button><button type="button" data-3d="zoomout" aria-label="3D 축소">−</button><button type="button" data-3d="labels" aria-pressed="true">부품 이름</button><button type="button" data-3d="door" aria-pressed="false">도어·LED</button><button type="button" data-3d="wires" aria-pressed="false">귀환선</button><button type="button" data-3d="expand">화면 채우기</button></div><div class="three-help">휠 확대 · 왼쪽 드래그 회전 · 오른쪽 드래그 이동 · 부품 클릭</div><div class="three-selection" hidden></div><div class="three-assumptions">* RFID·홍싱·어댑터는 임시 몸체 치수 · 배선 표시는 경로 설명용</div></div><details class="vector-reference"><summary>좌표·확보 영역을 2D 도면으로 확인</summary>{{DESIGN_SVG}}</details>'
    page=page.replace('{{DESIGN_SVG}}',viewer)
    page=page.replace('센서마다 신호와 GND를 한 쌍으로 회수합니다. Arduino 핀에 몰아 꽂지 않고 단자대에서 분배합니다.','기존 GPIO와 공통GND입니다. 부하 전류는 로직 장치 귀환에 직렬로 통과시키지 않습니다.')
    cards=[('기존 GPIO 직결','추가 모터/릴레이 절연모듈과 고정판 제거. D4/D5/A2와 D12/D10/D9/A4를 기존 입력에 직결합니다.'),('P0/G0 공통','G0.4→L298 GND 기준선으로 공통입니다. 자석−까지 갈바닉 절연된 설계가 아닙니다.'),('전력 귀환은 별도','모터/자석/코일 전류가 Arduino/센서 귀환에 직렬로 흐르지 않게 분기합니다.'),('기존 센서선 보존','추가 센서판 없음. 기존 핀·귀환·출력전압을 대조합니다.'),('자석 다이오드만','별도 접속PCB 없이 릴레이 근처에 각 자석 두 선 사이로 병렬 고정합니다.'),('기존 오디오/표시','MP3/홍싱 라인·GND 직결과 기존 LED·2초 진행 버튼을 유지합니다.')]
    docs='<section class="design-doc active" id="design-doc"><div class="design-grid">'+''.join('<article class="design-card"><h3>'+E(a)+'</h3><p>'+E(b)+'</p></article>' for a,b in cards)+'</div></section>'
    page=re.sub(r'<section class="design-doc active" id="design-doc">[\s\S]*?</div></section>',lambda _:docs,page,count=1)
    page=page.replace('RFID 큰 회색 제어함 · 릴레이 4ch × 2장 · L298N · KT403A · HONGXING · 기존 센서/부하.','RFID 소형 배치 · 릴레이 A/B · L298N · KT403A · HONGXING · 기존 센서/부하.')
    page=re.sub(r'<p>새 부품:.*?</p>','<p>추가 GPIO 절연모듈/고정판 없음. 자석 다이오드3개, 기존 센서/오디오/모터/릴레이 직결입니다.</p>',page)
    page=page.replace('확정 구성 반영 / 신규 정리 배치안','v5.3 기존 제어선 직결 / 공통GND')
    page=page.replace('<span><i></i>센서·GND-L</span><span><i class="out"></i>릴레이 제어</span><span><i class="motor"></i>모터 제어</span><span><i class="load"></i>접점·전력</span>','<span><i></i>G0 로직</span><span><i class="load"></i>P0 부하</span><span><i class="motor"></i>전원 변환부</span>')
    write('simulation/source/page.html',page)
    raw=(archive/'simulation__source__app.js').read_text(encoding='utf-8');runtime=raw[raw.index("const mode=$('firmware-mode')"):]
    views={'new':['v5.3 · 기존 제어선 직결','400mm 폭 / 상부260 / 하부560 · 부품을 누르면 좌표·영역 표시'],'gnd':['P0/G0 · 공통 기준과 별도 전력 귀환','공통 기준선 G0.4→L298 GND · 자석−도 공통 · PE는 별도 보호접지'],'interfaces':['직결·다이오드 · 실제 핀 회로','L2983신호 / 릴레이4입력 / 기존 센서 / 자석 양단 다이오드'],'cable':['가는 이더넷 심선 · 전원 검토','실제 길이·전류·단심저항 입력 · 전압강하와 페어 병렬 비교'],'bom':['제품 BOM · 제거/추가/제작 구분','일반 큰 단자열을 제거하고 필요한 접속부만 남긴 품번·수량'],'fit':['실장·치수 · 작은 확보 영역 대조','사진 기반 계획과 실물 치수를 비교 · 자동 설치승인 아님'],'panel':['외부 LED·버튼 · 기존 회로 유지','LED1.5kΩ×6 / 버튼4.7kΩ풀업 / A3 2초 진행'],'labels':['핀·라벨 · 실제 선 구간','가상의 T1/T2 단자열 없이 PCB 접속부와 모듈 핀에 직접 종단'],'photo':['기존 현장','철거 전 기록과 실제 배선 추적 기준'],'cabinet':['과거 기능 참고','v5 설치 결선도로 사용하지 않음']}
    views['review']=['왜 이 구성이 필요한가','분배블록/전원변환/MP3 위치/조건부 센서절연을 구별해 설명']
    runtime=re.sub(r'const views=\{[\s\S]*?\};\nfunction setView',lambda _:'const views='+json.dumps(views,ensure_ascii=False)+';\nfunction setView',runtime,count=1)
    runtime=runtime.replace("['labels-drawing','labels']","['labels-drawing','labels'],['interfaces-drawing','interfaces'],['cable-drawing','cable']")
    runtime=runtime.replace("['cable-drawing','cable']","['cable-drawing','cable'],['review-drawing','review']")
    runtime=runtime.replace("['new','gnd','labels','panel','fit','bom']","['new','gnd','labels','panel','fit','bom','interfaces','cable']")
    runtime=runtime.replace("all:'0 0 1420 2200',upper:'40 100 1370 700',lower:'45 730 970 1440'","all:'0 0 1320 2020',upper:'45 95 1250 680',lower:'45 750 900 1200'")
    runtime=runtime.replace('#panel-drawing>svg,#functional-drawing>svg','#panel-drawing>svg,#functional-drawing>svg,#interfaces-drawing>svg')
    runtime=runtime.replace("reset();setView('new');select('gnd');","reset();setView('new');select('gnd');")
    app="/* v5 design data + unchanged tested AVR workbench behavior. */\n(()=>{'use strict';\nconst $=id=>document.getElementById(id),all=(s,r=document)=>[...r.querySelectorAll(s)];\nconst details="+json.dumps(details,ensure_ascii=False)+';\n'+runtime
    write('simulation/source/app.js',app)
    write('simulation/source/fit.js',r'''/* v5 physical fit, cable voltage drop, and explicit DC connectivity. */
(()=>{'use strict';const $=id=>document.getElementById(id),n=id=>Number($(id).value);
function fit(){let fail=[];for(const [id,need,name]of [['fit-width',400,'폭'],['fit-upper',260,'상부'],['fit-lower',560,'하부'],['fit-depth',120,'깊이']]){const v=n(id);if(!Number.isFinite(v)||v<=0)fail.push(name+' 양수 입력');else if(v<need)fail.push(name+' '+(need-v)+'mm 부족');}
for(const [id,max,name]of [['fit-rfid-w',160,'RFID 폭'],['fit-rfid-h',100,'RFID 높이'],['fit-rfid-d',65,'RFID 깊이'],['fit-amp-w',140,'홍싱 폭'],['fit-amp-h',90,'홍싱 높이'],['fit-amp-d',45,'홍싱 깊이']]){const v=n(id);if(!Number.isFinite(v)||v<=0)fail.push(name+' 양수 입력');else if(v>max)fail.push(name+' 몸체 가정 대비 '+(v-max)+'mm 큼: 배치 재검토');}
$('fit-result').className='fit-result '+(fail.length?'bad':'conditional');$('fit-result').textContent=fail.length?fail.join(' / '):'입력한 외곽은 현재 확보 조건에 들어옴 · 방열/실측/관통구/도어 확인 전 설치 확정 아님';}
document.querySelectorAll('.fit-inputs:not(.cable-inputs) input').forEach(e=>e.addEventListener('input',fit));fit();
function cable(){const V=n('wire-voltage'),L=n('wire-length'),I=n('wire-current'),R=n('wire-resistance'),T=n('wire-temp'),P=n('wire-pairs'),C=n('wire-contact');
if([V,L,I,R,T,P,C].some(x=>!Number.isFinite(x))||V<=0||L<=0||I<=0||R<=0||T<0||P<1||P>4||!Number.isInteger(P)||C<0){$('wire-result').textContent='양수 전압/길이/전류/저항, 온도0이상, 정수 페어1~4, 접촉저항0이상을 입력하세요.';$('wire-result').className='fit-result bad';$('wire-compare').textContent='';return;}
const calc=p=>{const loop=2*L*R*(1+.00393*(T-20))/p+C,drop=I*loop;return {loop,drop,end:V-drop,loss:I*I*loop,percent:100*drop/V};},a=calc(P);
$('wire-result').className='fit-result '+(a.end<=0||a.percent>5?'bad':'conditional');$('wire-result').textContent=`왕복 ${a.loop.toFixed(3)}Ω · 강하 ${a.drop.toFixed(3)}V (${a.percent.toFixed(1)}%) · 부하단 ${a.end.toFixed(3)}V · 배선/접속 손실 ${a.loss.toFixed(3)}W · 허용전류/온도 판정 아님`;
$('wire-compare').innerHTML='<table><thead><tr><th>병렬 페어</th><th>심선 총수</th><th>전압강하</th><th>부하단 전압</th><th>총 손실</th></tr></thead><tbody>'+[1,2,4].map(p=>{let b=calc(p);return `<tr><td>${p}</td><td>${p*2}</td><td>${b.drop.toFixed(3)}V</td><td>${b.end.toFixed(3)}V</td><td>${b.loss.toFixed(3)}W</td></tr>`;}).join('')+'</tbody></table>';}
document.querySelectorAll('.cable-inputs input').forEach(e=>e.addEventListener('input',cable));cable();
const g=window.MONGSHOT_DESIGN.graph,adj=new Map(g.nodes.map(x=>[x,[]]));for(const [a,b] of g.dc_connections){adj.get(a).push(b);adj.get(b).push(a);}function connected(a,b){const seen=new Set([a]),q=[a];while(q.length){for(const v of adj.get(q.pop())||[])if(!seen.has(v)){seen.add(v);q.push(v);}}return seen.has(b);}
const ok=connected('P0','G0')&&connected('G0','AMP_NEG')&&!connected('P0','PE')&&!connected('G0','PE');$('isolation-result').textContent=ok?'P0/G0는 제어 기준선으로 공통입니다. 자석−/모터/Arduino도 같은 GND입니다. 부하 전력 귀환은 별도 분기하며 PE는 별도입니다.':'설계 연결성 오류: 전원 영역과 홍싱 공통 GND 경로를 확인해야 합니다.';
window.mongshotDesignChecks={connected,fit,cable};})();''')
    labels='<section class="fit-sheet"><h2>핀·라벨 · 실제로 존재하는 접속점</h2><p>큰 T1/T2 DIN 단자열을 삭제했습니다. 새 XS/XM 접속판을 제거했습니다. 아래는 Arduino·릴레이·L298 기존 단자와 선을 기준으로 한 접속표입니다. 기존 선은 Arduino 핀으로 먼저 라벨링하고 철거합니다.</p>'+table(['기존 접속위치','대상','영역','실제 연결'],landing)+table(['양끝 선 라벨','시작','끝','전원 영역','시공 조건'],wires)+'</section>'
    # Build one self-contained file, with no service deployment or external import.
    css=(S/'app.css').read_text(encoding='utf-8')+'\n.fit-inputs{display:grid;grid-template-columns:repeat(auto-fit,minmax(145px,1fr));gap:12px}.fit-inputs label{display:flex;flex-direction:column;gap:6px}.fit-inputs input{width:100%;box-sizing:border-box}.fit-sheet td a{color:#218b85}.domain-notice{font-size:12px}.drawing-stage{min-height:620px}.drawing-title{font-size:15px}.wide-drawing .workspace{grid-template-columns:minmax(0,1fr)}.wide-drawing .right-sidebar{display:none}.cabinet-3d{position:relative;width:100%;height:min(78vh,1000px);min-height:540px;overflow:hidden;background:#ecf1f5;border-bottom:1px solid #d3dfe6}.cabinet-3d.expanded{position:fixed;inset:0;width:100vw;height:100dvh;min-height:0;z-index:10000;border:0}.three-expanded{overflow:hidden}.cabinet-3d canvas{display:block;width:100%;height:100%;touch-action:none}.three-toolbar{position:absolute;top:12px;left:14px;right:14px;display:flex;align-items:center;gap:7px;z-index:4;flex-wrap:wrap;pointer-events:none}.three-toolbar>*{pointer-events:auto}.three-toolbar button{background:#fff;border:1px solid #c5d3dc;padding:7px 11px;border-radius:6px;color:#365a70;font-size:12px;cursor:pointer}.three-toolbar button[aria-pressed=true]{background:#e0f1ee;border-color:#90bdb3}.three-badge{font-size:12px;color:#55768b;margin-right:12px}.three-help{position:absolute;bottom:15px;left:18px;font-size:11px;color:#6b8394;pointer-events:none}.three-assumptions{position:absolute;bottom:34px;left:18px;font-size:10px;color:#8b9ba8;pointer-events:none}.three-part-label{position:absolute;z-index:3;width:205px;border:1px solid #d3dfe7;background:rgba(255,255,255,.91);box-shadow:0 2px 7px #52738b0b;text-align:left;display:flex;align-items:center;gap:9px;padding:7px 10px;border-radius:6px;color:#294c61;font:600 12px "Malgun Gothic",Arial;cursor:pointer}.three-part-label small{display:block;font:400 10px Arial;color:#8a9da9;margin-top:3px}.three-part-label i{width:5px;height:26px;border-radius:3px;flex-shrink:0}.three-part-label.selected{border-color:#c5a85b;background:#fffcf2}.three-part-label[hidden]{display:none}.three-leader{position:absolute;inset:0;width:100%;height:100%;z-index:1;pointer-events:none}.three-selection{position:absolute;right:16px;bottom:17px;width:260px;padding:14px 16px;background:#fffef9eb;border:1px solid #d8c78d;border-radius:8px;z-index:4;box-shadow:0 5px 20px #40576b12}.three-selection strong,.three-selection span,.three-selection small{display:block}.three-selection strong{font-size:14px;color:#355369}.three-selection span{font-size:11px;color:#889caa;margin-top:6px}.three-selection small{font-size:11px;line-height:1.6;color:#688091;margin-top:7px}.vector-reference{padding:15px;color:#7891a0;font-size:12px}.vector-reference>svg{width:100%;height:auto}.drawing-stage:has(#design-drawing:not([hidden])){overflow:hidden;height:auto;max-height:none;padding:0}.drawing-stage:has(#design-drawing:not([hidden])) .vector-reference{display:none}@media(max-width:760px){.drawing-stage{min-height:600px}.app-header h1{font-size:18px}.fit-sheet{padding:16px}.frontpanel-bar{flex-wrap:wrap}.cabinet-3d{min-height:600px;height:72vh}.three-selection{width:210px}.three-help{font-size:10px;bottom:8px}.three-toolbar{gap:4px}.three-toolbar button{padding:6px 8px}.three-badge{width:100%}}'
    replacements={'CSS':css,'DESIGN_SVG':(H/'cabinet-redesign.svg').read_text(encoding='utf-8'),'GROUND_SVG':(H/'ground-topology.svg').read_text(encoding='utf-8'),'GROUND_TABLE':ground,'INTERFACES_SVG':(H/'isolation-interfaces.svg').read_text(encoding='utf-8'),'CABLE_VIEW':cable,'REVIEW_VIEW':review,'LABELS_VIEW':labels,'FIT_VIEW':fit,'BOM_VIEW':bhtml,'FRONTPANEL_SVG':(H/'frontpanel-circuit.svg').read_text(encoding='utf-8'),'CABINET_SVG':(H/'cabinet-layout.svg').read_text(encoding='utf-8'),'PHOTO':'data:image/jpeg;base64,'+base64.b64encode((root/'evidence/cabinet-original.jpg').read_bytes()).decode(),'AVR_LIB':(root/'simulation/vendor/avr8js-0.21.1.min.js').read_text(encoding='utf-8'),'RUNNER':(S/'runner.js').read_text(encoding='utf-8'),'FIRMWARE_DATA':(S/'firmware-data.js').read_text(encoding='utf-8'),'APP':'window.MONGSHOT_DESIGN='+json.dumps(dict(graph=graph,model=m),ensure_ascii=False)+';\n'+app+'\n'+(S/'fit.js').read_text(encoding='utf-8'),'STEPS':''.join(f'<div class="step"><span class="step-num">{i}</span><span class="step-name">{name}</span></div>' for i,name in enumerate(['액자','조명 ×3','열쇠','RFID','책','완료']))}
    for key,value in replacements.items():page=page.replace('{{'+key+'}}',value)
    bundle=(root/'simulation/vendor/cabinet3d.bundle.js').read_text(encoding='utf-8')
    init='''try{window.mongshot3D=Mongshot3D.mount(document.getElementById('cabinet-3d'),window.MONGSHOT_DESIGN,{onSelect:id=>window.mongshotWorkbench.select(id),ledMask:()=>window.mongshotWorkbench.runner.ledMask});document.body.classList.add('wide-drawing');const b=document.getElementById('wide-drawing');b.setAttribute('aria-pressed','true');b.textContent='입력창 표시';}catch(e){console.error(e);document.querySelector('.three-badge').textContent='3D 초기화 실패: '+e.message;}'''
    page=page.replace('</body>', '<script>'+bundle+'</script><script>'+init+'</script></body>')
    assert not re.search(r'\{\{[A-Z_]+\}\}',page)
    write('simulation/index.html',page)
    with (root/'README.md').open('a',encoding='utf-8') as f:f.write('\nThree.js 보기: 휠 확대/왼쪽 회전/오른쪽 이동/전체화면/부품 선택/도어 LED. 소스 수정 후 `python tools/build_3d.py` → `python tools/build_project.py`. [인터페이스 조립 지침](docs/10-interface-assembly.md)을 함께 봅니다.\n')
