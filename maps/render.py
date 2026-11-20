import json,os
from playwright.sync_api import sync_playwright
here=os.path.dirname(os.path.abspath(__file__))
D=json.loads(open(os.path.join(here,'render.html')).read().split('const DATA=')[1].split(';const C=')[0])
posts=[p['name'] for p in D['sector'] if p['ours']]
jobs=[('overview','osm'),('overview','sat')]+[(p,l) for p in posts for l in ('osm','sat')]
os.makedirs(os.path.join(here,'img'),exist_ok=True)
with sync_playwright() as pw:
  b=pw.chromium.launch()
  pg=b.new_page(viewport={'width':1200,'height':800},device_scale_factor=2,user_agent='Milano21-CRA-briefing-render/1.0 (github.com/AndreaGlightburn/milano21-cra)')
  for p,l in jobs:
    pg.goto('file://'+os.path.join(here,'render.html')+f'?p={p}&l={l}')
    pg.wait_for_function('window.DONE===true',timeout=60000); pg.wait_for_timeout(1500)
    out=os.path.join(here,'img',f'{p}_{l}.jpg'); pg.locator('#m').screenshot(path=out,type='jpeg',quality=85); print('ok',out)
  b.close()
