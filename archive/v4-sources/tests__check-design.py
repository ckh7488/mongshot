"""Check the proposed target topology and documentation cross references."""
from pathlib import Path
import json,csv,re,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1]
g=json.loads((ROOT/'hardware/ground-connectivity.json').read_text(encoding='utf-8'))
adj={n:set() for n in g['nodes']}
for a,b in g['dc_connections']:adj[a].add(b);adj[b].add(a)
def component(node,removed=None):
    visited={node};pending=[node]
    while pending:
        a=pending.pop()
        for b in adj[a]:
            if removed and {a,b}==set(removed):continue
            if b not in visited:visited.add(b);pending.append(b)
    return visited
assert {'0VPWR','SMPS_NEG','BUCK_IN_NEG','BUCK_OUT_NEG','MAG1_NEG','MAG2_NEG','MAG3_NEG','L298_GND','AMP_NEG'}<=component('0VL')
assert {'ARD_GND','SENSOR_GND','MP3_GND','RELAY_A_GND','RELAY_B_GND','PANEL_GND'}<=component('0VL')
assert '0VPWR' in component('0VL',('BUCK_IN_NEG','BUCK_OUT_NEG'))
assert '0VPWR' not in component('0VL',('0VPWR','0VL'))
with (ROOT/'hardware/full-wiring-schedule.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
labels=[r['양쪽 선 라벨'] for r in rows]
assert len(labels)==len(set(labels)),'Duplicated wire labels'
assert not any(x in labels for x in ['OUT-D11','OUT-D17'])
assert {'IN-D8','IN-A0','IN-A1','IN-A5','IN-D6'}<=set(labels)
for md in [ROOT/'README.md',*list((ROOT/'docs').glob('*.md'))]:
    for target in re.findall(r'\]\(([^)]+)\)',md.read_text(encoding='utf-8')):
        if '://' not in target and not target.startswith('#'):assert (md.parent/target).exists(),f'Broken reference {md.name} -> {target}'
original=ROOT/'firmware/original'
with zipfile.ZipFile(ROOT/'evidence/original_debug_code.zip') as z:
    pairs=[('디버깅 코드/mong_shot_minor_update/mong_shot_minor_update.ino',original/'operating/operating.ino'),('디버깅 코드/mong_shot_minor_update/mong_shot_minor_update_test.ino',original/'test/test.ino'),('디버깅 코드/school/shcool.ino',original/'school/school.ino')]
    for zipped,local in pairs:assert hashlib.sha256(z.read(zipped)).digest()==hashlib.sha256(local.read_bytes()).digest()
model=json.loads((ROOT/'hardware/cabinet-fit-model.json').read_text(encoding='utf-8'))
parts=model['parts'];plan=model['planning']
for p in parts:
    height=plan['upperHeight' if p['bay']=='upper' else 'lowerHeight']
    assert p['x']>=0 and p['y']>=0 and p['x']+p['reserveW']<=plan['usableWidth'] and p['y']+p['reserveH']<=height,p
    assert p['bodyW']<=p['reserveW'] and p['bodyH']<=p['reserveH'],p
    assert p['bodyD']+15<=plan['usableDepth'],p
for i,a in enumerate(parts):
    for b in parts[i+1:]:
        if a['bay']!=b['bay']:continue
        overlap=min(a['x']+a['reserveW'],b['x']+b['reserveW'])>max(a['x'],b['x']) and min(a['y']+a['reserveH'],b['y']+b['reserveH'])>max(a['y'],b['y'])
        assert not overlap,('Reserved mounting areas overlap',a['id'],b['id'])
for p in parts:
    ducts=model['ducts']['upperVertical'] if p['bay']=='upper' else model['ducts']['lowerVertical']+model['ducts']['lowerHorizontal']
    for x,y,w,h in ducts:
        assert not(min(p['x']+p['reserveW'],x+w)>max(p['x'],x) and min(p['y']+p['reserveH'],y+h)>max(p['y'],y)),('Part/duct overlap',p['id'])
assert plan['usableDepth']>=model['doorPanel']['depthNeed']
bom=json.loads((ROOT/'hardware/product-bom.json').read_text(encoding='utf-8'))
assert len({x['id'] for x in bom['items']})==len(bom['items'])
assert next(x for x in bom['items'] if x['id']=='GND-P/L')['qty']==2
assert next(x for x in bom['items'] if x['id']=='X1/X3/X4')['qty']==24
assert next(x for x in bom['items'] if x['id']=='RPULL')['part'].endswith('4K7')
assert next(x for x in bom['items'] if x['id']=='RLED')['part'].endswith('1K5')
counts=json.loads((ROOT/'tests/installation-counts.json').read_text(encoding='utf-8'))
with (ROOT/'hardware/wire-segments.csv').open(encoding='utf-8-sig') as f:segments=list(csv.reader(f))[1:]
assert len(segments)==counts['wireSegments'] and counts['endLabels']==len(segments)*2
assert len({r[0] for r in segments})==len(segments)
for base in ['IN-D8','0VL-FRAME','MAG1+','MAG1-','MOTOR-A','WIN-C']:
    assert {base+'-C',base+'-F'}<=set(r[0] for r in segments)
result={'pass':True,'scope':'proposed two-bay mounting and routing, not measured installation','checks':['DC common via direct copper trunk','power/logic branch routing specified','physical wire segments and labels unique','field terminal cabinet/field segments separated','old Gun/Hint removed before pin reuse','all document links exist','three original sketches preserved byte for byte','reserved mounting rectangles in bounds without overlap','duct/part reserves do not overlap','depth envelope and door reserve checked','manufacturer BOM with conditional rating/measurement gates'],**counts,'mountingParts':len(parts),'bomRows':len(bom['items'])}
(ROOT/'tests/design-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Design/source checks passed;',len(rows),'unique wire labels')
