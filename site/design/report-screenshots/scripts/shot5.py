import json
from playwright.sync_api import sync_playwright
from PIL import Image
D='/tmp/claude-0/-home-claude/84008d2b-0b07-5545-b0f7-272de5d2f19f/scratchpad/rep/v5/'
W=1240; S=1.5; meta={}
def save(src,name,box=None):
  im=Image.open(src).convert('RGB')
  if box: im=im.crop(tuple(int(v*S) for v in box))
  im.save(D+name+'.webp',quality=88); return im.size
JS_ROWCELL='''([label,col])=>{const td=[...document.querySelectorAll('td')].find(t=>t.innerText.trim().endsWith(label));
 const tr=td.parentElement; const d=tr.children[col].querySelector('div'); const r=d.getBoundingClientRect(); return [r.x,r.y+scrollY,r.width,r.height]}'''
with sync_playwright() as p:
  b=p.chromium.launch(); c=b.new_context(viewport={'width':W,'height':900},device_scale_factor=S)
  c.add_init_script("try{localStorage.setItem('honest-agent.sidebarMini','1')}catch(e){}")
  pg=c.new_page()
  def load(h,H=None):
    pg.set_viewport_size({'width':W,'height':900}); pg.goto('http://localhost:8766/index.html'+h); pg.wait_for_timeout(1300)
    H=H or pg.evaluate('document.documentElement.scrollHeight'); pg.set_viewport_size({'width':W,'height':H}); pg.mouse.move(W-20,H-20); pg.wait_for_timeout(500); return H
  # overview
  H=load('#/'); pg.screenshot(path=D+'t.png'); meta['overview']={'size':[W,H]}; save(D+'t.png','overview')
  hov=[]
  for lab in ['revenue_1997','order_total_1995','top_segment','top_nations_last_year']:
    x,y,w,h=pg.evaluate(JS_ROWCELL,[lab,10]); pg.mouse.move(x+w/2,y+h/2); pg.wait_for_timeout(350)
    pg.screenshot(path=D+'t.png'); box=(max(0,x-260),max(0,y-150),min(W,x+w+200),y+h+6)
    save(D+'t.png','ov_hover_'+lab,box); hov.append({'eval':lab,'cell':[x,y,w,h],'box':box})
  # below-threshold row hover
  r=pg.evaluate('''()=>{const tr=[...document.querySelectorAll('tbody tr')].find(t=>t.innerText.includes('Revenue in')&&t.innerText.includes('extract_match'));const b=tr.getBoundingClientRect();return [b.x,b.y+scrollY,b.width,b.height]}''')
  pg.mouse.move(r[0]+200,r[1]+r[3]/2); pg.wait_for_timeout(300); pg.screenshot(path=D+'t.png')
  box=(r[0]-2,r[1]-2,r[0]+r[2]+2,r[1]+r[3]+2); save(D+'t.png','ov_hover_row',box); hov.append({'eval':'row','cell':r,'box':box})
  meta['overview']['hovers']=hov; pg.mouse.move(0,0)
  # compare
  H=load('#/compare'); pg.screenshot(path=D+'t.png'); meta['compare']={'size':[W,H]}; save(D+'t.png','compare')
  hov=[]
  for col in [1,2,3]:
    x,y,w,h=pg.evaluate(JS_ROWCELL,['revenue_1997',col]); pg.mouse.move(x+w/2,y+h/2); pg.wait_for_timeout(350)
    pg.screenshot(path=D+'t.png'); box=(max(0,x-260),max(0,y-150),min(W,x+w+200),y+h+6)
    save(D+'t.png',f'cmp_hover_{col}',box); hov.append({'col':col,'cell':[x,y,w,h],'box':box})
  meta['compare']['hovers']=hov; pg.mouse.move(0,0)
  # result
  H=load('#/result/r53')
  bt=pg.evaluate('''()=>{const s=[...document.querySelectorAll('section')].find(s=>s.querySelector('h3')&&s.querySelector('h3').innerText.trim()=='Provenance');const b=s.getBoundingClientRect();return b.y+scrollY+b.height}''')
  pg.screenshot(path=D+'t.png'); save(D+'t.png','result'); meta['result']={'size':[W,H]}
  b.close()
json.dump(meta,open(D+'meta.json','w'),indent=1); print(json.dumps(meta,indent=1))
