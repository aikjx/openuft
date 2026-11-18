"""Chromium smoke tests with page content, never access external sites."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
html=(root/'web'/'index.html').read_text(encoding='utf-8')
from playwright.sync_api import sync_playwright
report={'tests':[],'engine':'Chromium','source':'local HTML file content','safety':'simulation only'}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1250,'height':950},device_scale_factor=1)
 errs=[]
 page.on('pageerror',lambda e:errs.append(str(e)))
 page.set_content(html,wait_until='load')
 def check(name,ok):
  report['tests'].append({'name':name,'passed':bool(ok)});
  if not ok: raise AssertionError(name)
 check('heading',page.locator('h1').count()==1)
 check('initial mass',page.locator('#aOne').inner_text().startswith('2.6697'))
 check('initial difference',page.locator('#aDiff').inner_text().startswith('5.3394'))
 page.locator('#massK').fill('200')
 check('mass scale',page.locator('#aDiff').inner_text().startswith('1.0679'))
 page.locator('#distK').fill('1')
 check('distance response',page.locator('#aDiff').inner_text().startswith('2.6697'))
 page.locator('#signK').fill('0')
 check('sign switch',page.locator('#signV').inner_text()=='−x')
 page.locator('button[data-mode="em"]').click()
 check('em panel visible',page.locator('#em').is_visible())
 check('initial U',page.locator('#uB').inner_text().startswith('3.9789'))
 page.locator('#BK').fill('0.2')
 check('field energy square',page.locator('#uB').inner_text().startswith('15.9155'))
 page.locator('button[data-mode="protocol"]').click()
 check('protocol panel',page.locator('#protocol').is_visible())
 check('explicit safety',page.get_by_text('无真实设备控制').count()>0)
 check('no Javascript error',len(errs)==0)
 page.locator('button[data-mode="mass"]').click()
 check('return to mass',page.locator('#mass').is_visible())
 page.screenshot(path=str(root/'results'/'browser_verified.png'),full_page=True)
 browser.close()
report['passed']=sum(t['passed'] for t in report['tests']);report['total']=len(report['tests']);report['errors']=errs
(root/'results'/'browser_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
