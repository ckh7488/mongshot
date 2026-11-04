"""Portable 2D wiring exports from the exact v6 geometry and route data."""
from pathlib import Path
from html import escape
import json,math
def write_svg(root,data):
    out=root/'hardware/v6'
    cols={'12':'#e96836','P0':'#204c8b','5':'#b68a20','G':'#0d9690','CTL':'#d25391','AUD':'#8260b4','PE':'#7b8591','AC':'#626b74'}
    core={'TRK-P','TRK-N','BUCK-IN-P','BUCK-IN-N','BUCK-OUT-P','BUCK-OUT-N','MOTOR-N','MOTOR-P','UNO-P','UNO-N','CAB-MOT','CAB-RLY','CAB-MP3-SIG'}
    names={'power-ground':'★ P0','mag-power':'P12','logic-positive':'5V','gnd':'G','buck':'#4091','l298':'L298N','relayA':'RY-A / 4CH','relayB':'RY-B / 4CH','magdiodes':'D×3','rfidbox':'RFID CONTROL','amp-adapter':'홍싱 어댑터','ac':'차단기','pe':'PE'}
    for full in [False,True]:
        elements=['<rect x="-65" y="-25" width="600" height="960" fill="#f8fafb"/>']
        for y,h,label in [(0,260,'상부 · 전원'),(330,560,'하부 · 제어·부하')]:
            elements+=[f'<rect x="-8" y="{y-8}" width="416" height="{h+16}" fill="#dbe5eb" stroke="#648191" stroke-width="3"/>',f'<rect x="0" y="{y}" width="400" height="{h}" fill="#fff"/>',f'<text x="420" y="{y+18}" font-size="10" font-weight="bold">{label}</text>',f'<text x="420" y="{y+32}" font-size="7">400 × {h}mm 가정</text>']
        elements+=['<rect x="95" y="278" width="210" height="28" rx="4" fill="#dce8ed"/>','<text x="200" y="296" text-anchor="middle" font-size="8">기존 상하 관통구 · 실측 전</text>']
        for d in data['model']['ducts']['groups']:
            x,y,w,h=d['rect'];y+=330 if d['bay']=='lower' else 0;c='#f3dcca' if d['group']=='power' else '#d5ece6'
            elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>')
        for p in data['model']['parts']:
            y=p['y']+(330 if p['bay']=='lower' else 0);by=p['bodyY']+(330 if p['bay']=='lower' else 0);bx=p['bodyX'];c='#e8f4ef' if p['domain']=='G0' else '#eef2f6';cx=bx+p['bodyW']/2;cy=by+p['bodyH']/2
            elements+=[f'<g><title>{escape(p["basis"])}</title><rect x="{p["x"]}" y="{y}" width="{p["reserveW"]}" height="{p["reserveH"]}" fill="none" stroke="#b0c0cb" stroke-dasharray="3 3"/>',f'<rect x="{bx}" y="{by}" width="{p["bodyW"]}" height="{p["bodyH"]}" rx="3" fill="{c}" stroke="#91a6b3"/>',f'<text x="{cx}" y="{cy}" text-anchor="middle" font-size="{5.5 if p["id"]=="magdiodes" else 6.5 if p["id"]=="buck" else 7.5 if p["id"]=="mp3" else 9}" font-weight="bold">{escape(names.get(p["id"],p["name"]))}</text>',f'<text x="{p["x"]+2}" y="{y+p["reserveH"]-2}" font-size="5.3" fill="#708695">{p["x"]},{p["y"]} / {p["reserveW"]}×{p["reserveH"]}</text></g>']
        previous=[]
        for r in data['routes']:
            if not full and r['id'] not in core:continue
            points=r['points'];path=f'M{points[0][0]},{points[0][1]}'
            for a,b in zip(points,points[1:]):
                if a[1]==b[1] and a[0]!=b[0]:
                    crosses=[]
                    for old in previous:
                        for c,d in zip(old['points'],old['points'][1:]):
                            if c[0]==d[0] and min(a[0],b[0])+4<c[0]<max(a[0],b[0])-4 and min(c[1],d[1])+4<a[1]<max(c[1],d[1])-4:crosses.append(c[0])
                    sign=1 if b[0]>a[0] else -1;last=None
                    for x in sorted(set(crosses),reverse=sign<0):
                        if last is not None and abs(x-last)<9:continue
                        path+=f' L{x-sign*3},{a[1]} Q{x},{a[1]-5} {x+sign*3},{a[1]}';last=x
                path+=f' L{b[0]},{b[1]}'
            previous.append(r);c=r['color'];dash='stroke-dasharray="4 3"' if r['conditional'] or r['kind']=='PE' else ''
            label=r['labels'][0] if len(r['labels'])==1 else r['id'];mid=r.get('labelAt',points[len(points)//2]);w=2.1 if r['kind']=='CTL' else 1.5 if r['returnWire'] else 1.1
            elements+=[f'<g class="route"><title>{escape(r["title"])} / {escape(", ".join(r["labels"]))}</title><path d="{path}" fill="none" stroke="white" stroke-width="{w+2.2}" stroke-linejoin="round"/>',f'<path d="{path}" fill="none" stroke="{c}" stroke-width="{w}" {dash} stroke-linejoin="round"/>']
            for x,y in [points[0],points[-1]]:
                if x<0 or x>400:
                    sign=-1 if x<0 else 1
                    elements.append(f'<path d="M{x-sign*5},{y-3}L{x},{y}L{x-sign*5},{y+3}" fill="none" stroke="{c}"/><text x="{x+sign*6}" y="{y}" text-anchor="{"end" if sign<0 else "start"}" font-size="6" fill="{c}">외부</text>')
                else:elements.append(f'<circle cx="{x}" cy="{y}" r="1.7" fill="{c}"/>')
            if not full or r['id'] in core:elements.append(f'<text x="{mid[0]+3}" y="{mid[1]-4}" font-size="7" font-weight="bold" fill="{c}" stroke="white" stroke-width="2" paint-order="stroke">{escape(label)}</text>')
            elements.append('</g>')
        elements+=['<text x="0" y="917" font-size="8">v6 · 비절연 / 실측 전 배치안 · 좌표는 해당 함 좌상 기준</text>','<text x="0" y="932" font-size="7">점선: 미확인·조건부 / 모터 VMS12V·5V는 택1 / 실제 선 절단 길이·타공도 아님</text>']
        svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="-65 -25 600 960" width="1200" height="1920"><style>text{font-family:Arial,Malgun Gothic,sans-serif;fill:#254552}.route:hover{filter:drop-shadow(0 0 2px #152e3d)}</style>'+''.join(elements)+'</svg>'
        (out/('front-wiring-full.svg' if full else 'front-wiring.svg')).write_text(svg,encoding='utf-8')
    # PNG uses Windows Korean font directly, so the portable overview remains readable.
    from PIL import Image,ImageDraw,ImageFont
    scale=2.5;left=-65;top=-25
    im=Image.new('RGB',(1500,2400),'#f8fafb');draw=ImageDraw.Draw(im)
    def xy(x,y):return ((x-left)*scale,(y-top)*scale)
    def box(x,y,w,h,fill,outline=None,width=1):draw.rectangle([xy(x,y),xy(x+w,y+h)],fill=fill,outline=outline,width=width)
    def text(x,y,t,size=8,color='#254552',anchor='mm'):
        font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',max(8,round(size*scale)));draw.text(xy(x,y),t,font=font,fill=color,anchor=anchor)
    for y,h,label in [(0,260,'상부 · 전원'),(330,560,'하부 · 제어·부하')]:
        box(-8,y-8,416,h+16,'#dbe5eb','#648191',4);box(0,y,400,h,'white');text(420,y+15,label,10,anchor='lm');text(420,y+32,f'400×{h}mm 가정',7,anchor='lm')
    box(95,278,210,28,'#dce8ed');text(200,292,'기존 상하 관통구 · 실측 전',8)
    for d in data['model']['ducts']['groups']:
        x,y,w,h=d['rect'];y+=330 if d['bay']=='lower' else 0;box(x,y,w,h,'#f3dcca' if d['group']=='power' else '#d5ece6')
    for p in data['model']['parts']:
        by=p['bodyY']+(330 if p['bay']=='lower' else 0);bx=p['bodyX'];box(bx,by,p['bodyW'],p['bodyH'],'#e8f4ef' if p['domain']=='G0' else '#eef2f6','#91a6b3')
        text(bx+p['bodyW']/2,by+p['bodyH']/2,names.get(p['id'],p['name']),5.5 if p['id']=='magdiodes' else 6.5 if p['id']=='buck' else 7.5 if p['id']=='mp3' else 9)
        y=p['y']+(330 if p['bay']=='lower' else 0);text(p['x']+2,y+p['reserveH']-1,f'{p["x"]},{p["y"]} / {p["reserveW"]}×{p["reserveH"]}',5.5,'#708695','lm')
    for trunk in data['harness']['trunks']:
        draw.line([xy(*trunk['a']),xy(*trunk['b'])],fill='#405e69',width=max(4,round((2+math.sqrt(len(trunk['labels']))*.35)*scale)))
    for route in data['routes']:
        if route['alternative']:continue
        runs=[route['startLead'],route['endLead']] if route['mainPath'] else [route['points']]
        for run in runs:
            if len(run)<2:continue
            draw.line([xy(*point) for point in run],fill='#526a77' if len(route['labels'])>1 else route['color'],width=4 if len(route['labels'])>1 else 2)
    for yy,title in [(510,'H0 · MP3 / RFID'),(540,'H1 · 접점 전력'),(657.5,'H2 · 제어 묶음'),(777.5,'H3 · DC 분배')]:text(420,yy,title,8,anchor='lm')
    text(0,917,'v6 · 비절연 / 실측 전 배치안 · 좌표는 해당 함 좌상 기준',8,anchor='lm')
    text(0,933,'공용 덕트 묶음 + 짧은 꼬리선 / 묶음은 전기 접속 아님 / 실측 전 계획',7,anchor='lm')
    im.save(out/'front-wiring-overview.png')
