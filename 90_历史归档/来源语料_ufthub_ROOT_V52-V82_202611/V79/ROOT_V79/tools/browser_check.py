"""Actual Chromium interactions, retaining exact HTML bytes due to file-URL policy."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parents[1]
checks=[];errors=[]
def check(name,cond):
    checks.append({'name':name,'passed':bool(cond)})
    if not cond: raise AssertionError(name)
with sync_playwright() as play:
    browser=play.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1400,'height':900},device_scale_factor=1)
    page.on('pageerror',lambda err:errors.append(str(err)))
    page.set_content((P/'web/index.html').read_text(encoding='utf8'),wait_until='load')
    check('title', 'ROOT V79' in page.title())
    check('default energy tab',page.locator('#panel-energy').is_visible())
    check('canvas created',page.locator('#energyChart').evaluate('(c)=>c.width>500&&c.height>200'))
    page.screenshot(path=str(P/'results/web_energy_chromium.png'),full_page=True)
    check('initial ratio numeric',float(page.locator('#ueratio').inner_text().split('e')[0])>0)
    initial=page.locator('#ubmax').inner_text()
    page.locator('#B').evaluate('(e)=>{e.value="20";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    check('B slider updates energy',page.locator('#ubmax').inner_text()!=initial)
    page.locator('#f').evaluate('(e)=>{e.value="100";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    check('frequency label updates',page.locator('#harmonic').inner_text()=='200 Hz')
    page.locator('[data-tab="parity"]').click()
    check('parity visible',page.locator('#panel-parity').is_visible())
    check('zero background selects no 1f',page.locator('#freq1').inner_text()=='0')
    page.locator('#a0').evaluate('(e)=>{e.value="0.5";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    check('nonzero background creates 1f',float(page.locator('#freq1').inner_text())>0)
    page.locator('[data-tab="ledger"]').click()
    check('ledger visible',page.locator('#panel-ledger').is_visible())
    check('no external energy default',page.locator('#added').inner_text()=='0 MJ')
    page.locator('#net').evaluate('(e)=>{e.value="50";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    check('added input updates',page.locator('#added').inner_text()=='50.0000 MJ')
    page.locator('[data-tab="eq"]').click()
    check('catalog loaded all',page.locator('#equationCount').inner_text().startswith('显示 66 / 66'))
    page.locator('#searchEquations').fill('平面波')
    check('equation search filters',len(page.locator('.equation').all())>0 and len(page.locator('.equation').all())<66)
    page.screenshot(path=str(P/'results/web_chromium.png'),full_page=True)
    check('no javascript exception',not errors)
    browser.close()
(P/'results/browser_report.json').write_text(json.dumps({'count':len(checks),'passed':all(x['passed'] for x in checks),'checks':checks,'page_errors':errors,'load_mode':'inline_html_due_to_sandbox_file_policy'},ensure_ascii=False,indent=2),encoding='utf8')
print('Chromium checks',len(checks),'passed')
