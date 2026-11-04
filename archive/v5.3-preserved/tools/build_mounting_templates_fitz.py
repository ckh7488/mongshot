"""v5 A3 reserve templates. No mounting-hole claims from assumed dimensions."""
from pathlib import Path
import fitz,json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'hardware/cabinet-fit-model.json').read_text(encoding='utf-8'))
MM=72/25.4;doc=fitz.open();font='C:/Windows/Fonts/malgun.ttf'
INK=(.20,.35,.43);MUTED=(.46,.57,.64);LINE=(.67,.77,.83)
colors={'P0':(.68,.45,.25),'G0':(.14,.52,.48),'A0':(.54,.40,.65),'PE':(.45,.57,.28),'BOUNDARY':(.35,.47,.59)}
def page(w,h):
 p=doc.new_page(width=w*MM,height=h*MM);p.insert_font(fontname='KO',fontfile=font);return p
def text(p,x,y,s,size=8,c=INK):p.insert_text((x*MM,y*MM),s,fontname='KO',fontsize=size,color=c)
def rect(p,x,y,w,h,c=LINE,fill=None,dash=None):p.draw_rect(fitz.Rect(x*MM,y*MM,(x+w)*MM,(y+h)*MM),color=c,fill=fill,width=.5,dashes=dash)
def bay(p,b,x,top,scale=1,offset=0,window=None):
 H=m['planning']['upperHeight' if b=='upper' else 'lowerHeight'];window=window or H
 bounds=fitz.Rect(x,top,x+400*scale,top+window*scale)
 def clipped(xx,yy,w,h,c=LINE,dash=None):
  rr=fitz.Rect(xx,yy,xx+w,yy+h)&bounds
  if not rr.is_empty:rect(p,rr.x0,rr.y0,rr.width,rr.height,c,None,dash)
 for n in range(0,401,50):p.draw_line(((x+n*scale)*MM,top*MM),((x+n*scale)*MM,(top+window*scale)*MM),color=(.92,.95,.96),width=.3)
 for a in m['parts']:
  if a['bay']!=b:continue
  xx=x+a['x']*scale;yy=top+(a['y']-offset)*scale;c=colors[a['domain']]
  clipped(xx,yy,a['reserveW']*scale,a['reserveH']*scale,c,'[3 2] 0')
  iw=(a['reserveW']-a['bodyW'])/2;ih=a.get('bodyOffsetY',4)
  clipped(xx+iw*scale,yy+ih*scale,a['bodyW']*scale,a['bodyH']*scale,LINE)
  if top+3<yy+5<top+window*scale:
   text(p,xx+1.3,yy+4,'D×3' if a['id']=='magdiodes' else a['name'],7.5 if scale==1 else 5.4,c)
   if scale==1 and a['id']!='magdiodes':text(p,xx+1.3,yy+9,f"({a['x']},{a['y']}) / {a['reserveW']}x{a['reserveH']}mm",6,MUTED)
 rect(p,x,top,400*scale,window*scale,INK)
p=page(297,420);text(p,17,20,'MONG SHOT / v5.3 직결 실장 계획',17)
text(p,17,30,'P0/G0 공통 기준 - 사진 실측값 또는 타공도면 아님',9,MUTED)
bay(p,'upper',17,48,.36);bay(p,'lower',17,163,.36)
text(p,17,44,'상부400x260mm',9);text(p,17,159,'하부400x560mm',9)
notes=['현재 설치 검토값','유효 폭400 / 깊이120','상부260 / 하부560','','RFID 몸체가정','160x100x65mm','홍싱 몸체가정','140x90x45mm','커넥터 돌출 실측','','P0와G0 공통 기준선','추가 퓨즈 없음','현장 DIN24개 삭제','','다음4장: A3가로1:1','100% 출력','페이지맞춤 금지','100mm 검정자로 확인','','점선: 배선 포함 확보','실선: 몸체 검토 외곽','나사홀: 실물 전사','방열/도어 별도 대조']
for i,s in enumerate(notes):text(p,177,52+i*9,s,8,MUTED)
text(p,17,405,'실장 외곽 검토와 전기적 적합은 별개. 케이블 전류/저항/온도와 실제 부품을 대조합니다.',8)
for i,(b,off,h,label) in enumerate([('upper',0,260,'상부 전체'),('lower',0,240,'하부1/3'),('lower',230,240,'하부2/3'),('lower',460,100,'하부3/3')],2):
 p=page(420,297);text(p,10,10,f'MONG SHOT v5 / {label} / A3가로 / 실제 크기100%',11)
 text(p,10,16,f'유효 백플레이트 원점 Y={off}~{off+h}mm / 점선=확보영역 / 체결홀 아님',8,MUTED)
 bay(p,b,10,23,1,off,h)
 if b=='lower':
  for gy in [230,240,460,470]:
   if off<=gy<=off+h:
    yy=23+gy-off;p.draw_line((10*MM,yy*MM),(410*MM,yy*MM),color=LINE,width=.6,dashes='[6 3] 0');text(p,12,yy+2,f'겹침 기준 Y={gy}',6,MUTED)
 p.draw_line((260*MM,290*MM),(360*MM,290*MM),color=INK,width=.8)
 for xx in [260,360]:p.draw_line((xx*MM,288*MM),(xx*MM,292*MM),color=INK,width=.8)
 text(p,285,287,'검정자100mm',7);text(p,10,291,'확보용 템플릿 / 실물대조 후 고정 / 나사홀 직접 타공 금지',7,MUTED);text(p,399,291,f'{i}/5',7,MUTED)
out=R/'output/pdf/MongShot_TwoBay_Mounting_Templates.pdf';out.parent.mkdir(parents=True,exist_ok=True)
doc.set_metadata({'title':'MONG SHOT v5 isolated compact cabinet reserve templates','author':'MONG SHOT review'})
doc.save(out,garbage=4,deflate=True);doc.close();print(out)
