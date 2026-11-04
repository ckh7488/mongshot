"""A3 vector 1:1 reserve templates using the available PyMuPDF runtime."""
from pathlib import Path
import json,fitz
ROOT=Path(__file__).resolve().parents[1];m=json.loads((ROOT/'hardware/cabinet-fit-model.json').read_text(encoding='utf-8'))
MM=72/25.4;doc=fitz.open();FONT='C:/Windows/Fonts/malgun.ttf'
INK=(.20,.35,.43);MUTED=(.49,.60,.66);LINE=(.69,.79,.84)
def page(w,h):
 p=doc.new_page(width=w*MM,height=h*MM);p.insert_font(fontname='KO',fontfile=FONT);return p
def text(p,x,y,s,size=8,c=INK):p.insert_text((x*MM,y*MM),s,fontname='KO',fontsize=size,color=c)
def rect(p,x,y,w,h,c=LINE,fill=None,dash=None):p.draw_rect(fitz.Rect(x*MM,y*MM,(x+w)*MM,(y+h)*MM),color=c,fill=fill,width=.5,dashes=dash)
def bay(p,b,x,top,scale=1,offset=0,window=None):
 H=m['planning']['upperHeight' if b=='upper' else 'lowerHeight'];window=window or H
 bounds=fitz.Rect(x,top,x+400*scale,top+window*scale)
 def clipbox(xx,yy,w,h,c=LINE,fill=None,dash=None):
  rr=fitz.Rect(xx,yy,xx+w,yy+h)&bounds
  if not rr.is_empty:rect(p,rr.x0,rr.y0,rr.width,rr.height,c,fill,dash)
 for n in range(0,401,50):p.draw_line(((x+n*scale)*MM,top*MM),((x+n*scale)*MM,(top+window*scale)*MM),color=(.91,.94,.95),width=.3)
 for pp in m['parts']:
  if pp['bay']!=b:continue
  xx=x+pp['x']*scale;yy=top+(pp['y']-offset)*scale
  clipbox(xx,yy,pp['reserveW']*scale,pp['reserveH']*scale,LINE,None,'[3 2] 0')
  iw=(pp['reserveW']-pp['bodyW'])/2;ih=min(10,(pp['reserveH']-pp['bodyH'])/2)
  clipbox(xx+iw*scale,yy+ih*scale,pp['bodyW']*scale,pp['bodyH']*scale,MUTED)
  if top+3<yy+5<top+window*scale:
   text(p,xx+1.5,yy+4,pp['name'],8 if scale==1 else 5.5)
   if scale==1:text(p,xx+1.5,yy+9,f"({pp['x']}, {pp['y']}) / {pp['reserveW']}x{pp['reserveH']}mm",6,MUTED)
 rect(p,x,top,400*scale,window*scale,INK)
p=page(297,420);text(p,17,20,'MONG SHOT / 상하 배전함 실장 검토',17);text(p,17,30,'사진 추정 기반 계획 - 설치 전 유효 치수/제품을 대조합니다.',9,MUTED)
bay(p,'upper',17,47,.36);bay(p,'lower',17,158,.36)
text(p,17,44,'상부 400x260',9);text(p,17,154,'하부 400x650',9)
notes=['설치 검토값','유효 폭 400mm','상부 높이 260mm','하부 높이 650mm','유효 깊이 120mm','','RFID 몸체 가정','260x180x90mm','실측 전 확정 아님','','다음 4장: A3 가로1:1','100%로 출력','페이지에 맞춤 금지','100mm 검정자로 확인','','점선: 확보 영역','실선: 몸체 검토값','나사홀은 실물 전사','바로 타공하지 않음','','PT2.5 단자24개','RFID 옆 별도 자리','제품 BOM과 함께 대조']
for i,s in enumerate(notes):text(p,177,52+i*9,s,8,MUTED)
text(p,17,405,'확보 영역은 케이블 여유를 포함합니다. 몸체 가정값은 현장 실측을 대체하지 않습니다.',8)
for i,(b,off,h,label) in enumerate([('upper',0,260,'상부 전체'),('lower',0,240,'하부 1/3'),('lower',230,240,'하부 2/3'),('lower',460,190,'하부 3/3')],2):
 p=page(420,297);text(p,10,10,f'MONG SHOT / {label} / A3 가로 / 실제 크기100%',11)
 text(p,10,16,f'유효 백플레이트 원점 기준 Y={off}~{off+h}mm / 점선=확보 영역 / 체결홀 아님',8,MUTED)
 bay(p,b,10,23,1,off,h)
 if b=='lower':
  for gy in [230,240,460,470]:
   if off<=gy<=off+h:
    yy=23+gy-off;p.draw_line((10*MM,yy*MM),(410*MM,yy*MM),color=LINE,width=.6,dashes='[6 3] 0');text(p,12,yy+2,f'겹침 기준 Y={gy}',6,MUTED)
 p.draw_line((260*MM,290*MM),(360*MM,290*MM),color=INK,width=.8)
 for xx in [260,360]:p.draw_line((xx*MM,288*MM),(xx*MM,292*MM),color=INK,width=.8)
 text(p,285,287,'검정자100mm',7);text(p,10,291,'1:1 출력 후 자로 확인 / 실물 대조 후 고정 / 도어·단자·방열 확인',7,MUTED);text(p,399,291,f'{i}/5',7,MUTED)
out=ROOT/'output/pdf/MongShot_TwoBay_Mounting_Templates.pdf';out.parent.mkdir(parents=True,exist_ok=True);doc.set_metadata({'title':'MONG SHOT two-bay mounting reserve templates','author':'MONG SHOT review'});doc.save(out,garbage=4,deflate=True);doc.close();print(out)
