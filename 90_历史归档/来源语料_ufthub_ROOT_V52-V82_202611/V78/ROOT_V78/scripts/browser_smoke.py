"""Actual Chromium smoke test via Playwright, optional dependency."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
from playwright.sync_api import sync_playwright, Error as PlaywrightError
issues=[]; checks=[]
def check(name, condition):
    checks.append({'name':name,'passed':bool(condition)})
    if not condition: raise AssertionError(name)
with sync_playwright() as play:
    browser=play.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1280,'height':920}, device_scale_factor=1)
    page.on('pageerror',lambda err:issues.append(str(err)))
    # Automated Chromium blocks local file URLs by administrator policy.
    # Render identical HTML content directly; no external resources are used.
    load_mode='inline_html_due_to_file_policy'
    page.set_content((root/'web'/'index.html').read_text(encoding='utf8'),wait_until='load')
    check('title', 'ROOT V78' in page.title())
    check('magnetic starts', page.locator('#sectionTitle').inner_text()=='磁场储能和质量当量')
    first=page.locator('#k1').inner_text()
    page.locator('#B').evaluate('(e)=>{e.value="20";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    check('magnetic slider updates', first!=page.locator('#k1').inner_text())
    check('magnetic formula plotted',page.locator('canvas').evaluate('(c)=>c.width===800&&c.height===280'))
    page.locator('[data-tab="par"]').click()
    check('parity tab',page.locator('#sectionTitle').inner_text()=='平行 E/B 的磁场反转实验')
    check('parity zero background',float(page.locator('#k4').inner_text())==0)
    page.locator('#P').evaluate('(e)=>{e.value="0.5";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    check('parity with background',float(page.locator('#k4').inner_text())!=0)
    page.locator('[data-tab="gc"]').click()
    check('G c tab',page.locator('#sectionTitle').inner_text()=='同一恒等式可以对应不同 G(c)')
    page.locator('#gmode').select_option(value='3')
    page.locator('#cratio').evaluate('(e)=>{e.value="1.2";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    check('conditional G c responds',abs(float(page.locator('#k2').inner_text())-1.2**3)<1e-5)
    page.locator('[data-tab="yuk"]').click()
    check('Yukawa tab',page.locator('#sectionTitle').inner_text()=='有限源与点源的区别')
    check('Yukawa finite positive',float(page.locator('#k2').inner_text())>0)
    page.screenshot(path=str(root/'results'/'web_actual_chromium.png'),full_page=True)
    check('no JS pageerrors',not issues)
    browser.close()
(root/'results'/'browser_report.json').write_text(json.dumps({'count':len(checks),'checks':checks,'page_errors':issues,'load_mode':load_mode},ensure_ascii=False,indent=2),encoding='utf8')
print('Actual Chromium checks:',len(checks),'passed')
