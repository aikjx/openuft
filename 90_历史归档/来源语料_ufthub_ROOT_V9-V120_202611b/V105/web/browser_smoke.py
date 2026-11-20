from pathlib import Path
from playwright.sync_api import sync_playwright
import json

p=Path(__file__).with_name('index.html').resolve()
checks={}
with sync_playwright() as t:
    browser=t.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1000,'height':800})
    errors=[]
    page.on('pageerror',lambda err:errors.append(str(err)))
    page.goto('about:blank'); page.set_content(p.read_text(encoding='utf-8'),wait_until='load')
    checks['header']=page.locator('h1').count()==1
    checks['default_U1']=page.locator('#u1').inner_text()=='1.000000'
    checks['default_SU2']=abs(float(page.locator('#su2').inner_text())-0.925026722)<1e-8
    page.locator('#a').evaluate("e=>{e.value='0';e.dispatchEvent(new Event('input',{bubbles:true}))}")
    checks['zero_angle_commutes']=abs(float(page.locator('#su2').inner_text())-1)<1e-9
    page.locator('#a').evaluate("e=>{e.value='1.570796327';e.dispatchEvent(new Event('input',{bubbles:true}))}")
    page.locator('#b').evaluate("e=>{e.value='1.570796327';e.dispatchEvent(new Event('input',{bubbles:true}))}")
    checks['SU2_special'] = abs(float(page.locator('#su2').inner_text())+1)<1e-7
    checks['SU3_special'] = abs(float(page.locator('#su3').inner_text())+1/3)<1e-7
    checks['canvas_present']=page.locator('canvas').count()==1
    checks['no_script_errors']=len(errors)==0
    page.screenshot(path=str(p.parents[1]/'figures'/'02_CHROMIUM_V105_THEORY.png'),full_page=True)
    browser.close()
assert all(checks.values()), {'checks':checks,'errors':errors}
with open(p.parents[1]/'results'/'BROWSER_SMOKE.json','w',encoding='utf8') as f:json.dump(checks,f,ensure_ascii=False,indent=2)
print('CHROMIUM checks passed',len(checks))
