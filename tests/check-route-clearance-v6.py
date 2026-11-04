from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];d=json.loads((r/'hardware/v6/design-data.json').read_text(encoding='utf-8'))
def rect(p):return [p['bodyX'],p['bodyY']+(330 if p['bay']=='lower' else 0),p['bodyW'],p['bodyH']]
def inside(a,p):
    x,y,w,h=rect(p);return x-.1<=a[0]<=x+w+.1 and y-.1<=a[1]<=y+h+.1
def crosses(a,b,p):
    x,y,w,h=rect(p);x+=.1;y+=.1;w-=.2;h-=.2;t0,t1=0,1;dx,dy=b[0]-a[0],b[1]-a[1]
    for v,q in [(-dx,a[0]-x),(dx,x+w-a[0]),(-dy,a[1]-y),(dy,y+h-a[1])]:
        if v==0:
            if q<0:return False
        else:
            t=q/v
            if v<0:t0=max(t0,t)
            else:t1=min(t1,t)
    return t0<t1 and t0<1 and t1>0
bad=[]
for route in d['routes']:
    for p in d['model']['parts']:
        if inside(route['points'][0],p) or inside(route['points'][-1],p):continue
        for a,b in zip(route['points'],route['points'][1:]):
            if crosses(a,b,p):bad.append((route['id'],p['id'],a,b));break
assert not bad,bad
print('v6 route centre-lines: no unrelated component body crossings')
