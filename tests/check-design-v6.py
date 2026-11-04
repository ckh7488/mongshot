"""v6 regression: topology, adverse extra bonds, original preservation, wiring and fit."""
from pathlib import Path
import csv,hashlib,json,math,re,zipfile
R=Path(__file__).resolve().parents[1];H=R/'hardware/v6';A=R/'archive/v5.3-preserved'
data=json.loads((H/'design-data.json').read_text(encoding='utf-8'));g=data['graph'];ww=data['wires'];parts=data['model']['parts']
def paths(start,end,edges):
    adj={}
    for e in edges:
        adj.setdefault(e['a'],[]).append((e['b'],e['label']));adj.setdefault(e['b'],[]).append((e['a'],e['label']))
    result=[]
    def visit(n,seen,route):
        if n==end:result.append(route);return
        for b,label in adj.get(n,[]):
            if b not in seen:visit(b,seen|{b},route+[label])
    visit(start,{start},[]);return result
ee=g['edges'];pp=paths('P0','G',ee);assert len(pp)==1 and 'BUCK-INTERNAL-GND' in pp[0]
assert len(paths('P0','G',g['originalInstructionEdges']))==2
assert not paths('P0','G',[e for e in ee if e['label']!='BUCK-INTERNAL-GND'])
# Counterexamples must fail the single-path invariant, not merely match a saved PASS flag.
assert len(paths('P0','G',ee+[dict(a='G',b='L298_GND',label='bad-motor-ref')]))==2
assert len(paths('P0','G',ee+[dict(a='P0',b='G',label='bad-direct-jumper')]))==2
assert len(paths('P0','G',ee+[dict(a='P0',b='PE',label='bad-chassis-power'),dict(a='G',b='PE',label='bad-chassis-logic')]))==2
assert not paths('PE','G',ee) and not paths('PE','P0',ee)
assert len(paths('ADAPTER_NEG','G',ee))==1 and 'AUD-GND' in paths('ADAPTER_NEG','G',ee)[0]
assert len(paths('ADAPTER_NEG','G',ee+[dict(a='ADAPTER_NEG',b='P0',label='bad-amp-jumper')]))==2
for n in ['L298_GND','MAG1−','MAG2−','MAG3−']:
    incident=[e for e in ee if n in [e['a'],e['b']]];assert len(incident)==1 and incident[0]['a']=='P0'
labels={w['label']:w for w in ww};assert len(labels)==len(ww)
for e in ee:
    if e['label'] not in ['BUCK-INTERNAL-GND','AMP-INTERNAL-GND']:assert e['label'] in labels,e
assert not any(w['start'].startswith('G.') and 'L298' in w['end'] for w in ww)
for bus,port,target,label in data['groundPorts']+data['positivePorts']:
    if label:
        w=labels[label];assert bus+'.'+port in [w['start'],w['end']],(bus,port,w)
assert len([w for w in ww if w['end']=='L298 GND'])==1
assert {'MOTOR-VMS-12','MOTOR-VMS-5'}<=labels.keys()
assert all(labels[l]['status']=='미확인' and labels[l]['condition'].startswith('U1') for l in ['MOTOR-VMS-12','MOTOR-VMS-5','L298-VSS-5'])
for w in ww:
    assert len(w['labels'])==3 and len(set(w['labels']))==3
    if w['condition']:assert w['status']=='미확인'
    if w['cable'].startswith(('CAB-','REED-')):
        if w['cable']=='CAB-MOT':assert '공유 기준' in w['pair']
        else:assert any(x['cable']==w['cable'] and x['returnWire'] for x in ww),w
route_labels={lab for r in data['routes'] for lab in r['labels']};assert set(labels)<=route_labels,sorted(set(labels)-route_labels)
assert route_labels<=set(labels)
for r in data['routes']:
    assert len(r['points'])>=2 and all(math.isfinite(v) for p in r['points'] for v in p),r
    # Every upper-to-lower cable passes through the represented existing opening.
    if r['id'] in ['TRK-P','TRK-N','AMP-P','AMP-N']:
        crosses=[]
        for a,b in zip(r['points'],r['points'][1:]):
            if min(a[1],b[1])<290<max(a[1],b[1]):crosses.append(a[0]+(b[0]-a[0])*(290-a[1])/(b[1]-a[1]))
        assert crosses and all(95<=x<=305 for x in crosses),(r['id'],crosses)
def overlap(a,b):return min(a[0]+a[2],b[0]+b[2])>max(a[0],b[0]) and min(a[1]+a[3],b[1]+b[3])>max(a[1],b[1])
for i,p in enumerate(parts):
    rect=[p['x'],p['y'],p['reserveW'],p['reserveH']]
    assert p['x']>=0 and p['y']>=0 and p['x']+p['reserveW']<=400 and p['y']+p['reserveH']<=(260 if p['bay']=='upper' else 560)
    assert p['bodyW']<=p['reserveW'] and p['bodyH']<=p['reserveH'] and p['bodyD']+15<=120
    for q in parts[i+1:]:
        if p['bay']==q['bay']:assert not overlap(rect,[q['x'],q['y'],q['reserveW'],q['reserveH']]),(p['id'],q['id'])
    for d in data['model']['ducts']['upperVertical'] if p['bay']=='upper' else data['model']['ducts']['lowerVertical']+data['model']['ducts']['lowerHorizontal']:
        assert not overlap(rect,d),('part/duct overlap',p['id'],d)
def bodygap(a,b):
    dx=max(0,a['bodyX']-b['bodyX']-b['bodyW'],b['bodyX']-a['bodyX']-a['bodyW']);dy=max(0,a['bodyY']-b['bodyY']-b['bodyH'],b['bodyY']-a['bodyY']-a['bodyH']);return math.hypot(dx,dy)
by={p['id']:p for p in parts};assert bodygap(by['uno'],by['gnd'])<=50 and bodygap(by['uno'],by['logic-positive'])<=50
v5bom=json.loads((A/'hardware/product-bom.json').read_text(encoding='utf-8'));old={x['id']:x for x in v5bom['items']};new={x['id']:x for x in data['bom']['items']}
assert set(old)-set(new)=={'DC-L'} and set(new)<set(old)
for id,x in new.items():assert x['part']==old[id]['part'] and x['qty']<=old[id]['qty']
assert not {'sensorif','loadif','audioiso','isogpio','isolated5'}&by.keys()
pres=json.loads((A/'preservation.json').read_text(encoding='utf-8'))
for rel,sha in pres.items():assert hashlib.sha256((A/rel).read_bytes()).hexdigest()==sha,('v5 snapshot changed',rel)
assert (R/'hardware/cabinet-fit-model.json').read_bytes()==(A/'hardware/cabinet-fit-model.json').read_bytes()
assert (R/'simulation/source/cabinet3d.js').read_bytes()==(A/'simulation/source/cabinet3d.js').read_bytes()
with zipfile.ZipFile(R/'evidence/original_debug_code.zip') as z:
    for zipped,local in [('디버깅 코드/mong_shot_minor_update/mong_shot_minor_update.ino','operating/operating.ino'),('디버깅 코드/mong_shot_minor_update/mong_shot_minor_update_test.ino','test/test.ino'),('디버깅 코드/school/shcool.ino','school/school.ino')]:assert hashlib.sha256(z.read(zipped)).digest()==hashlib.sha256((R/'firmware/original'/local).read_bytes()).digest()
assert len(data['unknowns'])==7 and not g['systemGalvanicIsolation']
page=(R/'simulation/index.html').read_text(encoding='utf-8');assert 'src="http' not in page
assert all(c['pass'] for c in data['checks'])
result=dict(pass_=True,revision=data['model']['revision'],scope='plan only; no physical measurements',checks=['single planned P0/G path','motor-reference/direct-jumper/chassis-loop fault injection','amp bypass fault injection','PE separate in planned graph','wire/port/route cross references','conditional VMS alternatives','paired control references with explicit CAB-MOT exception','part/duct fit and50mm proximity','BOM subset with only DDR removed','v5 snapshot hash integrity','original firmware byte preservation','offline entry page'],stats=data['stats'],bodyGapMm={x:bodygap(by['uno'],by[x]) for x in ['gnd','logic-positive']})
result['pass']=result.pop('pass_');(R/'tests/v6-design-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
