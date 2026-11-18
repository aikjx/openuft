"""Browser functional smoke checks. Optional Playwright + chromium are required."""
import json
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=Path(__file__).resolve().parents[1]
url=(BASE/'web/index.html').resolve().as_uri()
checks=[]
with sync_playwright() as p:
    executable=shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome')
    launch_kwargs={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}
    if executable: launch_kwargs['executable_path']=executable
    browser=p.chromium.launch(**launch_kwargs)
    page=browser.new_page(viewport={'width':1440,'height':960},device_scale_factor=1)
    errs=[]
    page.on('pageerror',lambda e:errs.append(str(e)))
    # This test container blocks file:// URLs. Load the same self-contained HTML bytes.
    page.set_content((BASE/'web/index.html').read_text(encoding='utf-8'), wait_until='load')
    checks.append(('page_title', 'ROOT V77' in page.title()))
    checks.append(('reference_G', '6.67430' in page.locator('#Gref').inner_text()))
    checks.append(('reference_Z', '0.010004524012147' in page.locator('#Zref').inner_text()))
    checks.append(('default_G_ratio','1.0000000' in page.locator('#scenarioResult').inner_text()))
    page.locator('#cSlider').evaluate('(e)=>{e.value="120";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    checks.append(('slider_updates_label', page.locator('#cVal').inner_text()=='1.20'))
    checks.append(('fixed_Z_power_inverse', '0.8333333' in page.locator('#scenarioResult').inner_text()))
    page.locator('button[data-exponent="2"]').click()
    checks.append(('fixed_radius_power_two','1.4400000' in page.locator('#scenarioResult').inner_text()))
    page.locator('button[data-exponent="3"]').click()
    checks.append(('fixed_length_power_three','1.7280000' in page.locator('#scenarioResult').inner_text()))
    page.locator('button[data-exponent="0"]').click()
    checks.append(('fixed_G_no_change','1.0000000' in page.locator('#scenarioResult').inner_text()))
    page.locator('#massSlider').evaluate('(e)=>{e.value="-20";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    checks.append(('mass_slider_change', page.locator('#massVal').inner_text()=='-20.00'))
    checks.append(('alpha_updated','e-' in page.locator('#aResult').inner_text()))
    canvas=page.locator('#chart')
    checks.append(('canvas_present',canvas.count()==1))
    checks.append(('canvas_dimensions',page.evaluate("(()=>{const x=document.querySelector('#chart');return x.width===790 && x.height===360})()")))
    checks.append(('no_JS_errors',len(errs)==0))
    (BASE/'results/browser_screenshot.png').parent.mkdir(exist_ok=True)
    page.screenshot(path=str(BASE/'results/browser_screenshot.png'),full_page=True)
    browser.close()
report={'status':'PASSED' if all(v for _,v in checks) else 'FAILED',
        'checks':dict(checks),'count':len(checks),'javascript_errors':errs,
        'browser':'Chromium headless; page.set_content with exact offline HTML bytes; no network assets',
        'limit':'UI functional smoke checks only, not an independent physics validation'}
(BASE/'results/browser_verification.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
for name,ok in checks: print('PASS' if ok else 'FAIL',name)
if report['status']!='PASSED':raise SystemExit(1)
