"""Run Chromium on offline embedded HTML. Does NOT overwrite evidence when --no-screenshot."""
import json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'web/index.html').read_text(encoding='utf-8')
checks={}
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
    page=browser.new_page(viewport={'width':1200,'height':860},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(html,wait_until='load')
    checks['page_title']=page.title()=='ROOT V111 独立验收实验室'
    checks['three_cases']=page.locator('#mode option').count()==3
    checks['five_metrics']=page.locator('#metric option').count()==5
    checks['canvas_rendering']=page.locator('#curve').evaluate('(el)=>el.width>100 && el.height>100')
    checks['initial_charge_label']='Q' in page.locator('#metric-name').inner_text()
    page.select_option('#mode','shift_symmetric')
    checks['mode_switch']='shift_symmetric' in page.locator('#metric-name').inner_text()
    page.select_option('#metric','Eem')
    checks['metric_switch']='Eem' in page.locator('#metric-name').inner_text()
    checks['has_model_residual']='H 相对漂移' in page.locator('#summary').inner_text()
    page.select_option('#mode','tachyonic_backreaction')
    checks['tachyonic_model_select']='tachyonic_backreaction' in page.locator('#metric-name').inner_text()
    checks['no_js_errors']=len(errors)==0
    if '--screenshot' in sys.argv:
        page.screenshot(path=str(ROOT/'figures/05_CHROMIUM_ACTUAL_SCREENSHOT.png'),full_page=True)
    browser.close()
output={'check_count':len(checks),'passes':sum(checks.values()),'checks':checks,'page_errors':errors}
(ROOT/'results/browser_smoke.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(output,ensure_ascii=False,indent=2))
assert all(checks.values())
