"""Actual Chromium smoke check; exits nonzero on missing browser or UI malfunction."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(label,criterion):
    if not criterion:raise AssertionError(label)
    checks.append(label)

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1200,'height':800},device_scale_factor=1)
    errs=[]
    page.on('pageerror',lambda err:errs.append(str(err)))
    page.set_content((ROOT/'web/index.html').read_text(encoding='utf-8'),wait_until='load')
    check('page title',page.title().startswith('ROOT V109'))
    check('has 5 sliders',page.locator('input[type=range]').count()==5)
    check('benchmark rotation populated','rad' in page.locator('#full').inner_text())
    w0=page.locator('#wkb').inner_text()
    check('numerical full differs from WKB',page.locator('#full').inner_text()!=w0)
    page.locator('#lam').evaluate('(el)=>{el.value="0";el.dispatchEvent(new Event("input"))}')
    check('zero coupling yields zero WKB',page.locator('#wkb').inner_text().startswith('0.0000000'))
    check('zero coupling yields zero full',page.locator('#full').inner_text().startswith('0.0000000'))
    page.locator('#amp').evaluate('(el)=>{el.value="0.8";el.dispatchEvent(new Event("input"))}')
    check('slider value updates',page.locator('#ampout').inner_text()=='0.80')
    page.locator('#reset').click()
    check('reset reverts values',page.locator('#ampout').inner_text()=='0.40' and page.locator('#lamout').inner_text()=='0.080')
    check('chart SVG populated',len(page.locator('#theta_path').get_attribute('d'))>100)
    check('theory disclaimer present','无新实验' in page.locator('body').inner_text())
    check('no browser JS errors',not errs)
    page.screenshot(path=str(ROOT/'figures/05_CHROMIUM_ACTUAL_SCREENSHOT.png'),full_page=True)
    browser.close()
(ROOT/'results/browser_smoke.json').write_text(json.dumps({'checks':checks,'pass':len(checks),'errors':errs},ensure_ascii=False,indent=2),encoding='utf-8')
print('Chromium:',len(checks),'checks PASS')
