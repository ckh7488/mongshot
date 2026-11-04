"""A legible assembly drawing: common looms in ducts and short individual tails."""
from pathlib import Path
import math,xml.etree.ElementTree as ET
def write(root,data):
    ns='http://www.w3.org/2000/svg';ET.register_namespace('',ns)
    p=root/'hardware/v6/front-wiring.svg';tree=ET.parse(p);svg=tree.getroot()
    for parent in svg.iter():
        for child in list(parent):
            if child.get('class')=='route':parent.remove(child)
    def path(points,color,width,dash=None,title=None):
        attrs=dict(d='M'+' L'.join(str(x)+','+str(y) for x,y in points),fill='none',stroke=color,**{'stroke-width':str(width),'stroke-linejoin':'round','stroke-linecap':'round'})
        if dash:attrs['stroke-dasharray']=dash
        e=ET.SubElement(svg,'{'+ns+'}path',attrs)
        if title and title.startswith('기계적 묶음'):
            e.set('data-trunk',current_trunk);e.set('class','bundle-trunk');e.set('style','cursor:pointer')
        if title:ET.SubElement(e,'{'+ns+'}title').text=title
    for trunk in data['harness']['trunks']:
        current_trunk=trunk['id'];count=len(trunk['labels']);path([trunk['a'],trunk['b']],'#405e69',min(5.0,2.0+math.sqrt(count)*.35),title='기계적 묶음 / '+', '.join(trunk['cables'])+' / '+', '.join(trunk['labels']))
    for r in data['routes']:
        if r['alternative']:continue
        if r['mainPath']:
            for line in [r['startLead'],r['endLead']]:path(line,'#526a77' if len(r['labels'])>1 else r['color'],1.6 if len(r['labels'])>1 else .9,title=r['title']+' / '+', '.join(r['labels']))
        else:path(r['points'],r['color'],.9,'4 3' if r['kind']=='PE' else None,title=r['title'])
    external=set()
    for r in data['routes']:
        if r['alternative']:continue
        for x,y in [r['points'][0],r['points'][-1]]:
            if 0<=x<=400 or (x,y) in external:continue
            external.add((x,y));sign=-1 if x<0 else 1
            path([[x-sign*5,y-3],[x,y],[x-sign*5,y+3]],'#405e69',.9)
            ET.SubElement(svg,'{'+ns+'}text',dict(x=str(x+sign*6),y=str(y),**{'font-size':'6','text-anchor':'end' if sign<0 else 'start'})).text='외부'
    for y,t in [(510,'H0 · MP3 / RFID'),(540,'H1 · 접점 전력'),(657.5,'H2 · 제어 묶음'),(777.5,'H3 · DC 분배')]:
        ET.SubElement(svg,'{'+ns+'}text',dict(x='420',y=str(y),**{'font-size':'8','font-weight':'bold','class':'bundle-caption'})).text=t
    ET.SubElement(svg,'{'+ns+'}text',dict(x='0',y='947',**{'font-size':'7'})).text='묶음은 기계적 결속 / 전기 접속 아님 · 단자 앞 최대46.5mm · 실물 외경·충진율·굽힘 미확인'
    tree.write(p,encoding='utf-8',xml_declaration=True)
