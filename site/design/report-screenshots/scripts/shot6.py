import json
from playwright.sync_api import sync_playwright
from PIL import Image
D='/tmp/claude-0/-home-claude/84008d2b-0b07-5545-b0f7-272de5d2f19f/scratchpad/rep/v6/'
import os; os.makedirs(D,exist_ok=True)
W=1240; S=1.5
with sync_playwright() as p:
  b=p.chromium.launch(); c=b.new_context(viewport={'width':W,'height':1200},device_scale_factor=S)
  c.add_init_script("try{localStorage.setItem('honest-agent.sidebarMini','1')}catch(e){}")
  pg=c.new_page(); pg.goto('http://localhost:8767/index.html#/'); pg.wait_for_timeout(1500); pg.mouse.move(W-10,1190); pg.wait_for_timeout(300)
  card=pg.evaluate('''()=>{const s=[...document.querySelectorAll('section')].find(s=>s.innerText.includes('Scores by eval run'));const r=s.getBoundingClientRect();return [r.x,r.y,r.width,r.height]}''')
  cells=pg.evaluate('''()=>{const s=[...document.querySelectorAll('section')].find(s=>s.innerText.includes('Scores by eval run'));
   return [...s.querySelectorAll('tbody tr, tfoot tr')].map(tr=>{const lab=tr.children[0].innerText.trim().split('\\n').pop();
     const box=i=>{const d=tr.children[i].querySelector('div');const r=d.getBoundingClientRect();return [r.x,r.y,r.width,r.height]};
     return {label:lab,n:tr.children.length,c10:box(tr.children.length-3),c11:box(tr.children.length-2)}})}''')
  pg.screenshot(path=D+'full.png')
  im=Image.open(D+'full.png').convert('RGB')
  x,y,w,h=card; crop=im.crop((int(x*S),int(y*S),int((x+w)*S),int((y+h)*S))); crop.save(D+'heat.webp',quality=90)
  for cl in cells:
    cx,cy,cw,ch=cl['c10']; px=im.getpixel((int((cx+cw/2)*S),int((cy+ch/2)*S))); cl['c10color']='#%02x%02x%02x'%px
  hov=[]
  for cl in cells:
    if cl['label'] in ('revenue_1997','order_total_1995','top_segment','top_nations_last_year'):
      cx,cy,cw,ch=cl['c11']; pg.mouse.move(cx+cw/2,cy+ch/2); pg.wait_for_timeout(350); pg.screenshot(path=D+'t.png')
      tb=pg.evaluate("""()=>{const els=[...document.querySelectorAll('div')].filter(d=>{const t=d.innerText||'';return t.includes('2026-10-11')&&t.includes('Combined')&&getComputedStyle(d).position==='fixed'});const e=els[0];const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]}""")
      bx=(tb[0]-2,tb[1]-2,tb[0]+tb[2]+2,tb[1]+tb[3]+2)
      Image.open(D+'t.png').convert('RGB').crop(tuple(int(v*S) for v in bx)).save(D+f"hov_{cl['label']}.webp",quality=90)
      hov.append({'label':cl['label'],'cell':cl['c11'],'box':bx})
  b.close()
json.dump({'card':card,'cells':cells,'hov':hov},open(D+'meta.json','w'),indent=1)
print(json.dumps({'card':card,'cells':[(c['label'],c['n'],c['c10color']) for c in cells]},indent=0))
