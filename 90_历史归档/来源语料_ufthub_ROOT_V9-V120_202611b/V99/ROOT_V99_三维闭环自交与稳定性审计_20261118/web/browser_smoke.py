from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
checks={}
with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1340,'height':930},device_scale_factor=1)
  page.set_content((ROOT/'web/index.html').read_text(encoding='utf-8'),wait_until='load')
  checks['heading']=page.locator('h1').inner_text().startswith('三维周期轨道')
  checks['canvas']=page.locator('canvas').count()==1
  checks['source_rows']=page.locator('#rows tr').count()==3
  checks['yaw_control']=page.locator('#yaw').input_value()=='-25'
  page.locator('#yaw').evaluate('(el)=>{el.value="90";el.dispatchEvent(new Event("input",{bubbles:true}))}')
  checks['yaw_changes']=page.locator('#yv').inner_text()=='90°'
  page.locator('#lift').evaluate('(el)=>{el.value="0.15";el.dispatchEvent(new Event("input",{bubbles:true}))}')
  checks['perturb_changes']=page.locator('#lv').inner_text()=='0.15 µm'
  page.locator('#reset').click()
  checks['reset']=page.locator('#yv').inner_text()=='-25°' and page.locator('#lv').inner_text()=='0.00 µm'
  checks['not_experiment']=page.get_by_text('非实验 / 未证四力统一').count()>=1
  page.screenshot(path=str(ROOT/'figures/03_CHROMIUM_ACTUAL_SCREENSHOT.png'),full_page=True)
  browser.close()
(ROOT/'results/BROWSER_SMOKE.json').write_text(json.dumps({'checks':checks,'pass':all(checks.values()),'total':len(checks)},ensure_ascii=False,indent=2),encoding='utf-8')
assert all(checks.values()),checks
print('BROWSER PASS:',len(checks),'checks')
