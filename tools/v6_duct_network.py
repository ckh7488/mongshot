"""Route cabinet conductors on shared physical duct centre-lines, then fan out at ports."""
from collections import defaultdict
import heapq,math
COLORS={'12':'#e96836','P0':'#204c8b','5':'#b68a20','G':'#0d9690','CTL':'#d25391','AUD':'#8260b4','PE':'#7b8591','AC':'#626b74'}

class Network:
    def __init__(self,segments):self.segments=[(tuple(a),tuple(b)) for a,b in segments]
    def project(self,p):
        options=[]
        for a,b in self.segments:
            q=(min(max(p[0],min(a[0],b[0])),max(a[0],b[0])),a[1]) if a[1]==b[1] else (a[0],min(max(p[1],min(a[1],b[1])),max(a[1],b[1])))
            options.append((math.dist(p,q),q))
        return min(options)[1]
    def path(self,p,q):
        start=self.project(p);end=self.project(q);nodes={start,end}
        for a,b in self.segments:nodes|={a,b}
        for a,b in self.segments:
            for c,d in self.segments:
                if a[1]==b[1] and c[0]==d[0] and min(a[0],b[0])<=c[0]<=max(a[0],b[0]) and min(c[1],d[1])<=a[1]<=max(c[1],d[1]):nodes.add((c[0],a[1]))
        adj=defaultdict(list)
        for a,b in self.segments:
            nn=sorted(n for n in nodes if (a[0]==b[0]==n[0] and min(a[1],b[1])<=n[1]<=max(a[1],b[1])) or (a[1]==b[1]==n[1] and min(a[0],b[0])<=n[0]<=max(a[0],b[0])))
            for x,y in zip(nn,nn[1:]):
                w=math.dist(x,y);adj[x].append((y,w));adj[y].append((x,w))
        queue=[(0,start,[])];seen=set()
        while queue:
            cost,node,path=heapq.heappop(queue)
            if node in seen:continue
            seen.add(node);path=path+[node]
            if node==end:return [list(n) for n in path]
            for n,w in adj[node]:
                if n not in seen:heapq.heappush(queue,(cost+w,n,path))
        raise ValueError(('disconnected physical duct',start,end))

def build_routes(model,wires):
    pp={p['id']:p for p in model['parts']};routes=[]
    def port(pid,side,off=0):
        p=pp[pid];x=p['bodyX']+p['bodyW']/2;y=p['bodyY']+p['bodyH']/2+(330 if p['bay']=='lower' else 0)
        if side in ['top','bottom']:x+=off;y+=(-1 if side=='top' else 1)*p['bodyH']/2
        else:x+=(-1 if side=='left' else 1)*p['bodyW']/2;y+=off
        return [round(x,2),round(y,2)]
    power=Network([([25,165],[375,165]),([110,165],[110,340]),([12.5,340],[375,340]),([12.5,340],[12.5,880]),([12.5,540],[375,540]),([12.5,777.5],[390,777.5])])
    signal=Network([([390,350],[390,790]),([205,350],[205,510]),([205,510],[390,510]),([25,657.5],[390,657.5]),([235,777.5],[390,777.5])])
    ampdc=Network([([25,165],[375,165]),([110,165],[110,340]),([25,340],[375,340])])
    def add(id,labels,a,b,network,kind,title,group,ret=False,condition=False,alternative=False,via=None):
        main=network.path(a,b) if network else []
        points=([a,*main,b] if network else [a,*(via or []),b])
        points=[p for i,p in enumerate(points) if i==0 or p!=points[i-1]]
        if network:
            # All terminal tails leave normal to the nearest horizontal/vertical channel.
            for p,q in [(a,main[0]),(b,main[-1])]:
                assert p[0]==q[0] or p[1]==q[1],('diagonal terminal tail',id,p,q)
        labels=list(labels);lookup={w['label']:w for w in wires};cables=sorted({lookup[l]['cable'] for l in labels})
        routes.append(dict(id=id,labels=labels,points=points,mainPath=main,startLead=[a,main[0]] if main else [],endLead=[main[-1],b] if main else [],startLeadMm=round(math.dist(a,main[0]),2) if main else None,endLeadMm=round(math.dist(main[-1],b),2) if main else None,
            color=COLORS[kind],kind=kind,title=title,group=group,returnWire=ret,conditional=condition,alternative=alternative,cables=cables,network=('power' if network is power else 'signal' if network is signal else 'ampdc' if network else 'direct'),planLengthMm=round(sum(math.dist(p,q) for p,q in zip(points,points[1:])),1)))
    add('TRK-P',['TRK-12P'],port('smps','bottom',2),port('mag-power','top'),power,'12','TRK · 12V+/0V 한 묶음','전력')
    add('TRK-N',['TRK-0'],port('smps','bottom',-2),port('power-ground','top'),power,'P0','TRK · 전력 0V','전력',True)
    add('BUCK-IN-P',['BUCK-IN+'],port('mag-power','top',4),port('buck','top',-6),power,'12','P12.5→강압기 VIN','전력')
    add('BUCK-IN-N',['BUCK-IN−'],port('power-ground','top',4),port('buck','top',-2),power,'P0','P0.5→강압기 입력GND','전력',True)
    add('BUCK-OUT-P',['BUCK-5V'],port('buck','top',6),port('logic-positive','top'),power,'5','강압기 VOUT→5V.IN','신호')
    add('BUCK-OUT-N',['BUCK-G'],port('buck','top',2),port('gnd','top'),power,'G','강압기 출력GND→G.IN','신호',True)
    add('MOTOR-P',['MOTOR-VMS-12'],port('mag-power','top',8),port('l298','bottom',-12),power,'12','MOT-PWR · VMS12V 미확인','전력',condition=True)
    add('MOTOR-N',['P0-MOTOR'],port('power-ground','top',8),port('l298','bottom',-6),power,'P0','P0.4→L298 GND','전력',True)
    add('MOTOR-5ALT',['MOTOR-VMS-5'],port('logic-positive','top',8),port('l298','bottom',-12),power,'5','대안 VMS5V · 12V와 택1','전력',condition=True,alternative=True)
    add('MOTOR-VSS',['L298-VSS-5'],port('logic-positive','top',12),port('l298','bottom'),power,'5','L298 Vss · 점퍼 대조 후','신호',condition=True)
    add('UNO-P',['UNO-PWR-5V'],port('logic-positive','top',-4),port('uno','bottom',4),signal,'5','Uno 5V','신호')
    add('UNO-N',['UNO-PWR-G'],port('gnd','top',-4),port('uno','bottom',-4),signal,'G','Uno GND','신호',True)
    add('CAB-MOT',['MOT-D4','MOT-D5','MOT-A2'],port('uno','top',-8),port('l298','top'),signal,'CTL','모터 제어 · D4/D5/A2','신호')
    add('CAB-RLY',[w['label'] for w in wires if w['cable']=='CAB-RLY' and w['net'] not in ['G','+5V']],port('uno','top'),port('relayA','bottom'),signal,'CTL','릴레이A · 신호4 + 전원2','신호')
    for cab,pid in [('CAB-RLY','relayA'),('CAB-RLY-B','relayB'),('CAB-MP3','mp3')]:
        for ret,src,kind,suffix,offset in [(False,'logic-positive','5','5V',2),(True,'gnd','G','G',-2)]:
            add(cab+('-G' if ret else '-P'),[cab+'-'+suffix],port(src,'top',offset),port(pid,'bottom',offset),signal,kind,cab+' · '+('G' if ret else '5V'),'신호',ret,cab=='CAB-RLY-B')
    add('CAB-MP3-SIG',['MP3-D2','MP3-D3'],port('uno','top',6),port('mp3','bottom',-6),signal,'CTL','MP3 · UART + 전원4선','신호',condition=True)
    door=[425,690]
    add('PANEL-SIG',[f'PANEL-{p}' for p in ['D11','D13','D7','A3']],port('uno','top',12),door,signal,'CTL','도어 J7 · 6선 한 묶음','신호')
    add('PANEL-P',['PANEL-5V'],port('logic-positive','top',4),door,signal,'5','도어 J7.1','신호')
    add('PANEL-G',['PANEL-G'],port('gnd','top',4),door,signal,'G','도어 J7.2','신호',True)
    for n in [1,2,3]:
        contact=port('relayA','top',-26+(n-1)*18);field=[-25,550+(n-1)*14]
        add(f'MAG{n}-FEED',[f'M{n}-FEED'],port('mag-power','top',-16+n*4),contact,power,'12',f'자석{n} 접점 급전','전력')
        add(f'MAG{n}-POS',[f'M{n}-FIELD+'],[contact[0]+5,contact[1]],field,power,'12',f'자석{n} + · 다이오드 K','전력')
        add(f'MAG{n}-NEG',[f'M{n}-FIELD−'],port('power-ground','top',-16+n*4),field,power,'P0',f'자석{n} − · 다이오드 A','전력',True)
    for n,pin in enumerate(['D8','D6']):
        field=[425,600+n*12]
        add('REED-'+pin,['IN-'+pin],field,port('uno','top',-16+n*4),signal,'CTL',pin+' · 리드 신호/G 한 쌍','신호')
        add('REED-'+pin+'-G',['REED-'+pin+'-G'],port('gnd','top',8+n*4),field,signal,'G',pin+' · 리드 G','신호',True)
    for pin,off,yy in [('A0',16,624),('A1',20,636)]:add('FIELD-'+pin,['IN-'+pin],[425,yy],port('uno','top',off),signal,'CTL',pin+' · 센서 출력 미확인','신호',condition=True)
    add('RFID-SIG',['IN-A5'],port('rfidbox','right'),port('uno','top',24),signal,'CTL','RFID A5 · 출력형식 미확인','신호',condition=True)
    add('MOTOR-OUT',['MOTOR-OUT-A','MOTOR-OUT-B'],port('l298','bottom',16),[-25,750],power,'12','모터 OUT1/2 · GND 아님','전력')
    add('WINDOW',['WIN-COM','WIN-선택접점'],port('relayA','top',28),[-25,600],power,'AUD','창문 · 기존 SELV 접점회로','전력')
    for ret,block,kind,label in [(False,'mag-power','12','RFID-V+'),(True,'power-ground','P0','RFID-0')]:add(label,[label],port(block,'top',16),port('rfidbox','left',2 if ret else -2),power,kind,'RFID 기존 전원 · 정격 대조','전력',ret,True)
    for ret,block,kind,label in [(False,'mag-power','12','기타12V센서-V+'),(True,'power-ground','P0','기타12V센서-0')]:add('FIELD-12'+('N' if ret else 'P'),[label],port(block,'top',20),[-25,765],power,kind,'기타12V센서 · 전원 한 쌍','전력',ret,True)
    for ret,kind,id,labels,off,ym in [(False,'AUD','AUD-SIG',['AUD-L','AUD-R'],-2,456),(True,'G','AUD-GND',['AUD-GND'],2,460)]:
        a=port('mp3','top',off);b=port('amp','bottom',off);add(id,labels,a,b,None,kind,'홍싱 바로 아래 · 오디오 L/R/G','오디오',ret,via=[[a[0],ym],[b[0],ym]])
    for ret,id,kind,off in [(False,'AMP+','AUD',-2),(True,'AMP−','AUD',2)]:add('AMP-N' if ret else 'AMP-P',[id],port('amp-adapter','top',off),port('amp','top',off),ampdc,kind,'홍싱 기존 어댑터 · DC 한 쌍','오디오',ret)
    for n,end in [(87,'smps'),(88,None),(89,None)]:
        a=port('pe','left' if end else 'right',n-88);b=port(end,'right') if end else ([409,280] if n==88 else [425,670]);via=[[318,a[1]],[318,b[1]]] if end else [[410+n-87,a[1]],[410+n-87,b[1]]]
        add('PE-'+str(n),['PE-'+str(n)],a,b,None,'PE','PE · '+{87:'SMPS FG',88:'함체',89:'도어'}[n],'PE',via=via)
    for net,off in [('L',0),('N',4)]:
        a=port('ac','bottom',off);b=port('smps','left',6+off);add('AC-'+net,['AC-'+net],a,b,None,'AC','기존 AC '+net,'AC',via=[[35+off,145+off],[65-off,145+off],[65-off,b[1]]])
    return routes

def harness_model(model,routes,wires):
    # Split at every tap. A common route segment means mechanical bundling only.
    raw=[]
    for r in routes:
        for a,b in zip(r['mainPath'],r['mainPath'][1:]):
            if a!=b:raw.append((a,b,r))
    segments={}
    for a,b,r in raw:
        points={tuple(a),tuple(b)}
        for c,d,_ in raw:
            for p in [c,d]:
                if a[0]==b[0]==p[0] and min(a[1],b[1])<=p[1]<=max(a[1],b[1]):points.add(tuple(p))
                if a[1]==b[1]==p[1] and min(a[0],b[0])<=p[0]<=max(a[0],b[0]):points.add(tuple(p))
        points=sorted(points)
        for c,d in zip(points,points[1:]):
            key=(c,d);obj=segments.setdefault(key,dict(a=list(c),b=list(d),routeIds=set(),labels=set(),cables=set()))
            obj['routeIds'].add(r['id']);obj['labels'].update(r['labels']);obj['cables'].update(r['cables'])
    result=[]
    for i,(_,v) in enumerate(sorted(segments.items())):
        v=dict(v,id='TRUNK-'+str(i+1));v.update(routeIds=sorted(v['routeIds']),labels=sorted(v['labels']),cables=sorted(v['cables']));result.append(v)
    heads=[r for r in routes if r['mainPath']]
    tails=[r[k] for r in heads for k in ['startLeadMm','endLeadMm']]
    cut=[]
    for d in model['ducts']['groups']:
        x,y,w,h=d['rect'];cut.append(dict(id=d['id'],bay=d['bay'],group=d['group'],lengthMm=max(w,h),widthReserveMm=min(w,h)))
    bars=[[],[]];sums=[0,0]
    for c in sorted(cut,key=lambda c:-c['lengthMm']):
        k=min(range(2),key=lambda k:sums[k]);bars[k].append(c['id']);sums[k]+=c['lengthMm']+3
    assert max(sums)<=1828.8,(sums,bars)
    zones=[]
    for key,y in [('H1',540),('H2',657.5),('H3',777.5)]:
        ids={id for t in result if t['a'][1]==t['b'][1]==y for id in t['routeIds']}
        zones.append(dict(id='ZONE-'+key,routeIds=sorted(ids)))
    for key,test in [('FIELD',lambda c:c.startswith(('REED-','FIELD-'))),('MP3',lambda c:c=='CAB-MP3')]:
        zones.append(dict(id='ZONE-'+key,routeIds=[r['id'] for r in routes if any(test(c) for c in r['cables'])]))
    return dict(trunks=result,zones=zones,scope='하네스는 기계적 묶음이며 전기적 연결점이 아닙니다. 표시 외경/가닥 간격은 도면 표현값입니다.',maxExposedLeadMm=max(tails),wireRouteCount=len(heads),cutList=cut,cutBars=[dict(bar=i+1,stockMm=1828.8,with3mmKerfMm=sums[i],segments=bars[i]) for i in range(2)],ductLengthMm=sum(c['lengthMm'] for c in cut),routePolicy='shared-duct-graph',assumptions=['단자 앵커·회전방향은 실물 핀열 대조 전 계획','실제 케이블 외경·덕트 유효 내경·충진율·굽힘반경 미확인','기존 랜케이블은 외피 고정 후 원래 꼬임쌍을 유지해 내부 덕트로','모터5V 대안은 기본 뷰 제외; 결선표에 유지'])
