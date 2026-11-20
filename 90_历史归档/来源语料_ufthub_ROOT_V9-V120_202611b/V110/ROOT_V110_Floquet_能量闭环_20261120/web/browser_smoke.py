"""Headless browser UI sanity, no physical validation."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'web'/'index.html').read_text(encoding='utf-8')
checks={}
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1280,'height':900})
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.set_content(html,wait_until='domcontentloaded',timeout=20000)
    page.wait_for_function("document.getElementById('mu').textContent !== '—'",timeout=30000)
    checks['loaded']=page.title()=='ROOT V110 · 周期相位与能量闭环'
    checks['initial_growth']=float(page.locator('#mu').inner_text())>.02
    checks['initial_delta_theta_zero']=page.locator('#dtheta').inner_text()=='0'
    checks['initial_det_one']=abs(float(page.locator('#det').inner_text())-1)<2e-6
    page.locator('#g').evaluate("el=>{el.value='0';el.dispatchEvent(new Event('input',{bubbles:true}))}")
    checks['g_zero_has_zero_growth']=abs(float(page.locator('#mu').inner_text()))<1e-6
    page.locator('#reset').click()
    checks['reset_works']=float(page.locator('#mu').inner_text())>.02
    checks['drawing_exists']=page.locator('canvas').count()==1
    checks['no_js_error']=not errors
    # Preserve the archived screenshot: browser raster output is not bitwise stable.
    screenshot=root/'figures'/'05_BROWSER_ACTUAL_SCREENSHOT.png'
    if not screenshot.exists():
        page.screenshot(path=str(screenshot),full_page=True)
    browser.close()
out={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'errors':errors}
(root/'results'/'browser_smoke.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(out)
assert all(checks.values())
