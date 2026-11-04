from pathlib import Path
import copy,json,sys
r=Path(__file__).resolve().parents[1];sys.path.insert(0,str(r/'tools'))
from v6_harness_checks import validate
d=json.loads((r/'hardware/v6/design-data.json').read_text(encoding='utf-8'))
result=validate(d['model'],d['routes'],d['harness'])
# The checks must catch the kinds of routing mistakes that made the previous view untidy.
bad=copy.deepcopy(d['routes']);next(x for x in bad if x['id']=='CAB-RLY')['mainPath'][1:1]=[[305,680],[110,680],[110,657.5]]
try:validate(d['model'],bad,d['harness'])
except AssertionError:pass
else:raise AssertionError('un-ducted reroute was accepted')
bad=copy.deepcopy(d['routes']);next(x for x in bad if x['id']=='UNO-P')['startLeadMm']=95
try:validate(d['model'],bad,d['harness'])
except AssertionError:pass
else:raise AssertionError('long exposed tail was accepted')
result['pass']=result.pop('pass_');result['negativeTests']=['off-duct reroute rejected','95mm exposed lead rejected'];(r/'tests/v61-harness-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
