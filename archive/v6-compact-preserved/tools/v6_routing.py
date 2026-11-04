"""Compact cabinet harness paths. Coordinates are mm plan anchors, not pin drill positions."""
import math
COLORS={'12':'#e96836','P0':'#204c8b','5':'#b68a20','G':'#0d9690','CTL':'#d25391','AUD':'#8260b4','PE':'#7b8591','AC':'#626b74'}
def build_routes(model,wires):
    parts={p['id']:p for p in model['parts']};routes=[]
    def pos(id,side='center',off=0):
        p=parts[id];x=p['bodyX']+p['bodyW']/2;y=p['bodyY']+p['bodyH']/2+(330 if p['bay']=='lower' else 0)
        if side=='left':x=p['bodyX'];y+=off
        elif side=='right':x=p['bodyX']+p['bodyW'];y+=off
        elif side=='top':y-=p['bodyH']/2;x+=off
        elif side=='bottom':y+=p['bodyH']/2;x+=off
        return [round(x,2),round(y,2)]
    def add(id,labels,a,b,via,kind,title,group,ret=False,cond=False):
        points=[a,*via,b];points=[p for i,p in enumerate(points) if i==0 or p!=points[i-1]]
        routes.append(dict(id=id,labels=labels,points=points,color=COLORS[kind],kind=kind,title=title,group=group,returnWire=ret,conditional=cond,
            planLengthMm=round(sum(math.dist(a,b) for a,b in zip(points,points[1:])),1)))
    # Upper/lower crossing uses the existing opening before fanning to the left power duct.
    add('TRK-P',['TRK-12P'],pos('smps','bottom',3),pos('mag-power','left'),[[190,158],[9,158],[9,252],[100,252],[100,332],[9,332],[9,818.3]],'12','TRK · SMPS→하부 P12 / 12V+','전력')
    add('TRK-N',['TRK-0'],pos('smps','bottom',-1),pos('power-ground','left'),[[186,162],[13,162],[13,256],[104,256],[104,336],[13,336],[13,758.3]],'P0','TRK · SMPS→하부 P0 / 0V','전력',True)
    # Power converter input pair follows a common, short bottom branch. Never through Arduino.
    add('BUCK-IN-P',['BUCK-IN+'],pos('mag-power','right',-2),pos('buck','left',-2),[[107,816.3],[107,714],[251,714],[251,659.7]],'12','BUCK-IN · P12.5→VIN','전력')
    add('BUCK-IN-N',['BUCK-IN−'],pos('power-ground','right',2),pos('buck','left',2),[[111,760.3],[111,718],[255,718],[255,663.7]],'P0','BUCK-IN · P0.5→GND','전력',True)
    add('BUCK-OUT-P',['BUCK-5V'],pos('buck','bottom',2),pos('logic-positive','top'),[[282,734],[257.5,734]],'5','단일 강압기→5V판','신호')
    add('BUCK-OUT-N',['BUCK-G'],pos('buck','bottom',-2),pos('gnd','top'),[[278,730],[182.5,730]],'G','단일 강압기→G판','신호',True)
    # Same stack: relays above, Uno and L298 directly beneath, ground distribution below.
    add('MOTOR-P',['MOTOR-VMS-12'],pos('mag-power','left',-4),pos('l298','bottom',-4),[[6,814.3],[6,716],[66,716]],'12','MOT-PWR · VMS12V 조건부','전력',False,True)
    add('MOTOR-N',['P0-MOTOR'],pos('power-ground','top',4),pos('l298','bottom',4),[[66.5,724],[74,724]],'P0','P0.4→L298 GND · 독립 귀환','전력',True)
    add('MOTOR-5ALT',['MOTOR-VMS-5'],pos('logic-positive','top',4),pos('l298','bottom',8),[[261.5,738],[78,738]],'5','VMS5V 대안 · 12V와 택1','전력',False,True)
    add('MOTOR-VSS',['L298-VSS-5'],pos('logic-positive','top',8),pos('l298','bottom',12),[[265.5,742],[115,742],[115,722],[82,722]],'5','L298 Vss · 점퍼 확인 후','신호',False,True)
    add('UNO-P',['UNO-PWR-5V'],pos('logic-positive','top',-4),pos('uno','bottom',4),[[253.5,726],[174,726]],'5','5V.1→Uno 5V','신호')
    add('UNO-N',['UNO-PWR-G'],pos('gnd','top',-4),pos('uno','bottom',-4),[[178.5,722],[166,722]],'G','G.1→Uno GND','신호',True)
    add('CAB-MOT',[f'MOT-{p}' for p in ['D4','D5','A2']],pos('uno','top',-8),pos('l298','top'),[[162,636],[70,636]],'CTL','CAB-MOT · D4 / D5 / A2 · 짧은 직결','신호')
    add('CAB-RLY',[w['label'] for w in wires if w['cable']=='CAB-RLY' and w['net'] not in ['G','+5V']],pos('uno','top',8),pos('relayA','bottom'),[[178,620],[70,620]],'CTL','CAB-RLY · D12 / D10 / D9 / A4','신호')
    # Six conductors share one cable route after the branch splices near the central signal duct.
    for cab,dev in [('CAB-RLY','relayA'),('CAB-RLY-B','relayB'),('CAB-MP3','mp3')]:
        for ret,source,kind,off,suffix in [(False,'logic-positive','5',4,'5V'),(True,'gnd','G',0,'G')]:
            a=pos(source,'top',off);b=pos(dev,'bottom',off);lane=230+off
            if cab=='CAB-RLY':via=[[a[0],734+off],[lane,734+off],[lane,624+off],[b[0],624+off]]
            elif cab=='CAB-RLY-B':via=[[a[0],734+off],[lane,734+off],[lane,616+off],[b[0],616+off]]
            else:via=[[a[0],734+off],[lane,734+off],[lane,506+off],[b[0],506+off]]
            add(cab+('-G' if ret else '-P'),[cab+'-'+suffix],a,b,via,kind,cab+' · '+('G 기준' if ret else '5V'),'신호',ret,cab=='CAB-RLY-B')
    add('CAB-MP3-SIG',['MP3-D2','MP3-D3'],pos('uno','top',12),pos('mp3','bottom',-4),[[182,632],[226,632],[226,502],[266,502]],'CTL','CAB-MP3 · D2 / D3','신호',False,True)
    # Door harness and field leads leave at the side; no new terminal rows.
    add('PANEL-SIG',[f'PANEL-{p}' for p in ['D11','D13','D7','A3']],pos('uno','top',16),[425,690],[[186,640],[238,640],[238,690]],'CTL','PANEL · J7.3~6 · 도어','신호')
    add('PANEL-P',['PANEL-5V'],pos('logic-positive','top',12),[425,694],[[269.5,740],[242,740],[242,694]],'5','PANEL · J7.1 5V','신호')
    add('PANEL-G',['PANEL-G'],pos('gnd','top',8),[425,698],[[190.5,736],[246,736],[246,698]],'G','PANEL · J7.2 G','신호',True)
    for n in [1,2,3]:
        x=42+(n-1)*18;yy=535+(n-1)*21
        add(f'MAG{n}-FEED',[f'M{n}-FEED'],pos('mag-power','left',n*3),[x,534],[[5+n,818.3+n*3],[5+n,522-n*3],[x,522-n*3]],'12',f'MAG{n} · P12.{n}→COM{n}','전력')
        add(f'MAG{n}-POS',[f'M{n}-FIELD+'],[x+5,534],[-25,yy],[[x+5,526-n],[21,526-n],[21,yy]],'12',f'외부 자석{n} + / 다이오드 K','전력')
        add(f'MAG{n}-NEG',[f'M{n}-FIELD−'],pos('power-ground','left',n*3),[-25,yy+4],[[13+n,758.3+n*3],[13+n,yy+4]],'P0',f'외부 자석{n} − / 다이오드 A','전력',True)
    for n,pin in enumerate(['D8','D6']):
        yy=708+n*10
        add('REED-'+pin,['IN-'+pin],[425,yy],pos('uno','top',-16+n*4),[[238+n*4,yy],[238+n*4,644-n*4],[154+n*4,644-n*4]],'CTL',f'외부 {pin} 리드 신호','신호')
        add('REED-'+pin+'-G',['REED-'+pin+'-G'],pos('gnd','top',12+n*4),[425,yy+4],[[194.5+n*4,738+n*2],[242+n*4,738+n*2],[242+n*4,yy+4]],'G',f'외부 {pin} 리드 G · 같은 페어','신호',True)
    add('FIELD-SENSOR',['IN-A0','IN-A1','IN-A5'],pos('uno','top',-20),[425,704],[[150,642],[250,642],[250,704]],'CTL','외부 A0/A1/A5 · 출력형식 미확인','신호',False,True)
    add('MOTOR-OUT',['MOTOR-OUT-A','MOTOR-OUT-B'],pos('l298','left'),[-25,679],[[24,679]],'12','외부 모터 OUT1/2 · GND 아님','전력')
    add('WINDOW',['WIN-COM','WIN-선택접점'],pos('relayA','left',12),[-25,600],[[25,576],[25,600]],'AUD','외부 창문 W0 · 기존 SELV','전력')
    for label,ret,block,kind in [('RFID-V+',False,'mag-power','12'),('RFID-0',True,'power-ground','P0')]:
        a=pos(block,'left',6 if ret else 2);b=pos('rfidbox','left',4 if ret else 0);x=18 if ret else 14
        add(label,[label],a,b,[[x,a[1]],[x,b[1]]],kind,'RFID 전원 · 정격 확인 후','전력',ret,True)
    for label,ret,block,kind,off in [('기타12V센서-V+',False,'mag-power','12',0),('기타12V센서-0',True,'power-ground','P0',4)]:
        a=pos(block,'left',-8+off);add('FIELD-12'+('N' if ret else 'P'),[label],a,[-25,853+off],[[20+off,a[1]],[20+off,853+off]],kind,'외부 기타12V 센서 · 조건부','전력',ret,True)
    add('AUD-SIG',['AUD-L','AUD-R'],pos('mp3','top',-2),pos('amp','bottom',-2),[[268,450],[293,450]],'AUD','AUD · DAC L/R→MP3 IN','오디오')
    add('AUD-GND',['AUD-GND'],pos('mp3','top',2),pos('amp','bottom',2),[[272,446],[297,446]],'G','AUD-GND · 홍싱의 유일한 로직 연결','오디오',True)
    add('AMP-P',['AMP+'],pos('amp-adapter','bottom',-2),pos('amp','top',-2),[[248,245],[280,245],[280,332],[293,332]],'AUD','홍싱 기존 DC +','오디오')
    add('AMP-N',['AMP−'],pos('amp-adapter','bottom',2),pos('amp','top',2),[[252,249],[284,249],[284,328],[297,328]],'AUD','홍싱 기존 DC −','오디오',True)
    for n,end in [(87,'smps'),(88,None),(89,None)]:
        a=pos('pe','left' if end else 'right',n-88);b=pos(end,'right') if end else ([409,280] if n==88 else [425,670]);via=[[318,a[1]],[318,b[1]]] if end else [[410+n-87,a[1]],[410+n-87,b[1]]]
        add('PE-'+str(n),['PE-'+str(n)],a,b,via,'PE','PE · '+{87:'SMPS FG',88:'함체',89:'도어'}[n],'PE')
    for net,off in [('L',0),('N',4)]:
        a=pos('ac','bottom',off);b=pos('smps','left',6+off);add('AC-'+net,['AC-'+net],a,b,[[35+off,145+off],[65-off,145+off],[65-off,b[1]]],'AC','기존 '+net+'→SMPS','AC')
    label_positions={'TRK-P':[108,255],'TRK-N':[108,268],'CAB-MOT':[105,631],'CAB-RLY':[100,615],'CAB-MP3-SIG':[231,501],'BUCK-IN-P':[117,709],'BUCK-IN-N':[117,725],'BUCK-OUT-P':[286,706],'BUCK-OUT-N':[286,689],'UNO-P':[184,711],'UNO-N':[122,711],'MOTOR-P':[24,704],'MOTOR-N':[39,733]}
    for route in routes:
        if route['id'] in label_positions:route['labelAt']=label_positions[route['id']]
    return routes
