from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
checks=[];errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
    page=browser.new_page(viewport={'width':1280,'height':900},device_scale_factor=1)
    page.on('pageerror',lambda x:errors.append(str(x)))
    page.set_content((root/'web'/'index.html').read_text(encoding='utf-8'),wait_until='load')
    assert 'ROOT V83' in page.title();checks.append('title')
    before=page.locator('#common').inner_text();assert 'e-' in before;checks.append('initial gravity')
    page.locator('#flip').click();after=page.locator('#common').inner_text();assert before!=after and after.startswith('−');checks.append('side reversal')
    page.locator('#flip').click();assert page.locator('#common').inner_text()==before;checks.append('reverse back')
    page.locator('#massv').fill('200');page.locator('#massv').dispatch_event('input');after_mass=page.locator('#common').inner_text();assert after_mass!=before;checks.append('mass slider')
    page.locator('#reset').click();assert page.locator('#mv').inner_text()=='100 kg';checks.append('reset')
    page.locator('button[data-target="em"]').click();assert page.locator('#em').is_visible();checks.append('em tab')
    ub0=page.locator('#UB').inner_text();page.locator('#Bfield').fill('0.5');page.locator('#Bfield').dispatch_event('input');assert page.locator('#UB').inner_text()!=ub0;checks.append('B slider')
    page.locator('button[data-target="qa"]').click();assert page.locator('#qa').is_visible();checks.append('protocol tab')
    page.locator('button[data-target="mass"]').click();page.screenshot(path=str(root/'results'/'browser_verified.png'),full_page=True);checks.append('screenshot')
    assert not errors,errors
    browser.close()
(root/'results'/'browser_report.json').write_text(json.dumps({'checks':checks,'count':len(checks),'page_errors':errors,'status':'PASS','note':'Chromium set_content HTML; file:// blocked by test environment; not hardware verification'},indent=2,ensure_ascii=False),encoding='utf-8')
print(len(checks),'checks PASS')
