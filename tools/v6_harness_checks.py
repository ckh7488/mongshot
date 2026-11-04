"""Independent physical checks of all conductor runs, not a renderer visibility test."""
import math
def validate(model,routes,harness):
    boxes=[]
    for d in model['ducts']['groups']:
        x,y,w,h=d['rect'];y+=330 if d['bay']=='lower' else 0;boxes.append((x,y,w,h))
    # Only the existing inter-cabinet opening is allowed as an un-ducted backbone.
    boxes.append((100,260,20,70))
    def contained(p):return any(x-.01<=p[0]<=x+w+.01 and y-.01<=p[1]<=y+h+.01 for x,y,w,h in boxes)
    for r in routes:
        main=r['mainPath']
        if not main:continue
        assert r['startLeadMm']<=50 and r['endLeadMm']<=50,('long uncovered tail',r['id'])
        for a,b in zip(main,main[1:]):
            assert a[0]==b[0] or a[1]==b[1],('diagonal duct run',r['id'])
            steps=max(1,math.ceil(math.dist(a,b)/1.5))
            assert all(contained([a[0]+(b[0]-a[0])*i/steps,a[1]+(b[1]-a[1])*i/steps]) for i in range(steps+1)),('outside all physical ducts',r['id'],a,b)
        # A device tail must depart outwards; excluding a connected body from collision checks is insufficient.
        for endpoint,tap in [(r['points'][0],main[0]),(r['points'][-1],main[-1])]:
            for p in model['parts']:
                x,y,w,h=p['bodyX'],p['bodyY']+(330 if p['bay']=='lower' else 0),p['bodyW'],p['bodyH']
                if not (x-.02<=endpoint[0]<=x+w+.02 and y-.02<=endpoint[1]<=y+h+.02):continue
                dx,dy=tap[0]-endpoint[0],tap[1]-endpoint[1]
                outward=(abs(endpoint[0]-x)<.02 and dx<=0) or (abs(endpoint[0]-x-w)<.02 and dx>=0) or (abs(endpoint[1]-y)<.02 and dy<=0) or (abs(endpoint[1]-y-h)<.02 and dy>=0)
                assert outward,('tail enters connected body',r['id'],p['id'],endpoint,tap)
    rr={r['id']:r for r in routes};shared={}
    for cable,minimum in [('CAB-RLY',200),('CAB-MP3',140),('REED-D8',40),('REED-D6',40)]:
        ids={r['id'] for r in routes if cable in r['cables']}
        length=sum(math.dist(t['a'],t['b']) for t in harness['trunks'] if ids<=set(t['routeIds']))
        assert length>=minimum,('same cable not gathered in common run',cable,length)
        shared[cable]=round(length,1)
    for r in routes:
        for a,b in zip(r['mainPath'],r['mainPath'][1:]):
            covered=sum(math.dist(t['a'],t['b']) for t in harness['trunks'] if r['id'] in t['routeIds'] and all((a[0]==b[0]==p[0] and min(a[1],b[1])<=p[1]<=max(a[1],b[1])) or (a[1]==b[1]==p[1] and min(a[0],b[0])<=p[0]<=max(a[0],b[0])) for p in [t['a'],t['b']]))
            assert abs(covered-math.dist(a,b))<.1,('bundled display drops conductor section',r['id'],a,b,covered)
    assert all(b['with3mmKerfMm']<=b['stockMm'] for b in harness['cutBars'])
    return dict(pass_=True,maxTailMm=harness['maxExposedLeadMm'],commonCableRunMm=shared,ductMm=harness['ductLengthMm'],cutBars=harness['cutBars'],scope='planned geometry; actual OD, fill, bending, noise and dimensions unmeasured')
