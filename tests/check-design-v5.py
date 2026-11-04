"""Physical envelope, isolation-bypass and original-source checks."""
from pathlib import Path
import csv,json,re,hashlib,zipfile,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
def rows(name):
    with (R/'hardware'/name).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))
g=json.loads((R/'hardware/ground-connectivity.json').read_text(encoding='utf-8'))
def component(node,extra=()):
    adj={n:set() for n in g['nodes']}
    for a,b in [*g['dc_connections'],*extra]:adj[a].add(b);adj[b].add(a)
    seen={node};todo=[node]
    while todo:
        for b in adj[todo.pop()]:
            if b not in seen:seen.add(b);todo.append(b)
    return seen
assert {'L298_GND','MAG1_NEG','MAG2_NEG','MAG3_NEG','RELAY_A_GND','SENSOR_12V_NEG'}<=component('P0')
assert {'P0','ARD_GND','MP3_GND','PANEL_GND','L298_GND','SENSOR_CONTACT_RETURN'}<=component('G0')
assert 'PE' not in component('G0')
assert 'PE' not in component('P0')
assert {'AMP_NEG','AMP_LINE_GND'}<=component('G0')
assert g['groundPolicy']=='common-reference' and g['systemGalvanicIsolation'] is False
assert not any('ISO_' in n for n in g['nodes'])
assert g['referenceBond']=={'label':'GND-MOTOR-REF','start':'G0.4','end':'L298 GND'}
m=json.loads((R/'hardware/cabinet-fit-model.json').read_text(encoding='utf-8'));plan=m['planning'];parts=m['parts']
def overlap(a,b):
    x,y,w,h=a;xx,yy,ww,hh=b
    return min(x+w,xx+ww)>max(x,xx) and min(y+h,yy+hh)>max(y,yy)
def box(p):return [p['x'],p['y'],p['reserveW'],p['reserveH']]
for p in parts:
    h=plan['upperHeight' if p['bay']=='upper' else 'lowerHeight']
    assert p['x']>=0 and p['y']>=0 and p['x']+p['reserveW']<=400 and p['y']+p['reserveH']<=h,p
    assert p['bodyW']<=p['reserveW'] and p['bodyH']<=p['reserveH'] and p['bodyD']+15<=plan['usableDepth'],p
    if 'airClearance' in p:
        c=p['airClearance'];oy=p.get('bodyOffsetY',4)
        assert oy>=c['top'] and p['reserveH']-oy-p['bodyH']>=c['bottom'] and (p['reserveW']-p['bodyW'])/2>=max(c['left'],c['right']),('ventilation envelope',p['id'])
    ducts=m['ducts']['upperVertical'] if p['bay']=='upper' else m['ducts']['lowerVertical']+m['ducts']['lowerHorizontal']
    for d in ducts:assert not overlap(box(p),d),('part/duct overlap',p['id'])
for i,a in enumerate(parts):
    for b in parts[i+1:]:
        if a['bay']==b['bay']:assert not overlap(box(a),box(b)),(a['id'],b['id'])
assert plan['usableDepth']>=m['doorPanel']['depthNeed'] and plan['lowerHeight']==560
bm=json.loads((R/'hardware/product-bom.json').read_text(encoding='utf-8'));ids={x['id'] for x in bm['items']}
assert len(ids)==len(bm['items']) and not {'FU0','F1~7/F5L','X1/X3/X4','END','XCOV'}&ids
assert next(x for x in bm['items'] if x['id']=='DC-L')['part']=='DDR-15G-5'
assert not {'ISO-M','ISO-R','R-10K','PCB-IF'}&ids
ww=rows('wire-segments.csv');labels={r['양쪽 선 라벨'] for r in ww};assert len(labels)==len(ww) and not any('0V-LINK' in x for x in labels)
for r in rows('ground-terminal-schedule.csv'):
    if r['분배부'] in ['P0','G0'] and r['선 라벨']:
        assert r['선 라벨'] in labels,('port label absent from physical wires',r)
        w=next(w for w in ww if w['양쪽 선 라벨']==r['선 라벨'])
        assert r['분배부']+'.'+r['포트'] in [w['시작'],w['끝']],('ground port mismatch',r,w)
motor_returns=[r for r in ww if r['끝']=='L298 GND']
assert {x['양쪽 선 라벨'] for x in motor_returns}=={'P0-MOTOR','GND-MOTOR-REF'},('independent power return and common signal reference',motor_returns)
assert {'OUT-D12','OUT-D10','OUT-D9','OUT-A4','MOT-D4','MOT-D5','MOT-A2','IN-A0','IN-A1','IN-A5','IN-D6','IN-D8'}<=labels
for pin,target in [('D4','IN1'),('D5','IN2'),('A2','ENA')]:assert any(w['시작']=='Arduino '+pin and w['끝']=='L298 '+target for w in ww)
assert not any('ISO-' in w['시작']+w['끝'] for w in ww)
for n in [1,2,3]:assert {'M'+str(n)+'-FIELD+','M'+str(n)+'-FIELD−'}<=labels
assert not {'sensorif','loadif','audioiso','isogpio'} & {p['id'] for p in parts}
assert not {'XT','SI-OPTO','R-SI','R-4K7','R-1K','C-SI','D-SI','T-L/R','AUDIO-C','AUDIO-VR'} & ids
assert not any('XS' in r['시작']+r['끝'] or 'XM' in r['시작']+r['끝'] or '센서PCB' in r['시작']+r['끝'] for r in ww)
assert g['unresolvedSignalInterfaces']==['A0','A1','A5']
component_nets={r['네트']:r['같은 네트의 부품 핀'] for r in rows('interface-component-netlist.csv')}
for n in [1,2,3]:
    assert 'D-M'+str(n)+'.K' in component_nets['MAG'+str(n)+'-K'] and '자석양극선' in component_nets['MAG'+str(n)+'-K']
    assert 'D-M'+str(n)+'.A' in component_nets['MAG'+str(n)+'-A'] and 'P0.'+str(n) in component_nets['MAG'+str(n)+'-A']
assert len(rows('field-terminal-landing.csv'))==10
for md in [R/'README.md',*(R/'docs').glob('*.md')]:
    for target in re.findall(r'\]\(([^)]+)\)',md.read_text(encoding='utf-8')):
        if '://' not in target and not target.startswith('#'):assert (md.parent/target).exists(),(md,target)
for name in ['cabinet-redesign.svg','ground-topology.svg','isolation-interfaces.svg']:ET.parse(R/'hardware'/name)
with zipfile.ZipFile(R/'evidence/original_debug_code.zip') as z:
    for zipped,local in [('디버깅 코드/mong_shot_minor_update/mong_shot_minor_update.ino','operating/operating.ino'),('디버깅 코드/mong_shot_minor_update/mong_shot_minor_update_test.ino','test/test.ino'),('디버깅 코드/school/shcool.ino','school/school.ino')]:assert hashlib.sha256(z.read(zipped)).digest()==hashlib.sha256((R/'firmware/original'/local).read_bytes()).digest()
result={'pass':True,'revision':m['revision'],'scope':'direct GPIO with common DC reference; physical hardware remains unmeasured','checks':['P0/G0 intentionally common; magnet negative shares reference; PE separate','GPIO modules/carrier/pull-resistor assembly removed','direct motor and relay control wiring','independent motor power return and common signal-reference wire','ground bus port numbers match wire endpoints','added fuses and 24-DIN field row removed','mounting/duct envelopes in bounds without overlaps','unique physical wire labels','original sketches preserved byte-for-byte','document links resolve','valid SVG XML'],'wireSegments':len(ww),'endLabels':2*len(ww),'mountingParts':len(parts),'bomRows':len(bm['items'])}
(R/'tests/design-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('v5 checks passed:',len(ww),'physical wires;',len(parts),'mounting envelopes;',len(bm['items']),'BOM rows')
