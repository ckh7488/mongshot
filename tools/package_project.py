"""Reproducible handoff with current source, offline HTML, BOM and field records."""
from pathlib import Path
import csv,hashlib,zipfile,json
R=Path(__file__).resolve().parents[1]
def include(p):
    return p.is_file() and not any(x in ['__pycache__','node_modules','.git'] for x in p.relative_to(R).parts) and p.suffix not in ['.pyc','.tmp']
files=sorted(p for p in R.rglob('*') if include(p) and p.name!='MANIFEST.csv')
with (R/'MANIFEST.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['path','bytes','sha256'])
    for p in files:w.writerow([p.relative_to(R).as_posix(),p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()])
out=R.parent/'mongshot_delivery/MongShot_Work_Handoff_2026-11-03.zip';out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for p in [*files,R/'MANIFEST.csv']:z.write(p,'mongshot/'+p.relative_to(R).as_posix())
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(json.dumps({'file':str(out),'bytes':out.stat().st_size,'files':len(files)+1,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
