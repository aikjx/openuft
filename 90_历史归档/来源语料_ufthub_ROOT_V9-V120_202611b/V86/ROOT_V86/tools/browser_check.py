"""Actual Chromium UI smoke tests for the SAME offline HTML bytes."""
from pathlib import Path
import json,shutil
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'web/index.html').read_text(encoding='utf8')
checks=[];errors=[]
def assertcheck(name,ok,detail=''):
    checks.append({'name':name,'passed':bool(ok),'detail':detail})
    assert ok,(name,detail)
with sync_playwright() as p:
    execpath=shutil.which('chromium') or shutil.which('google-chrome')
    kw={'executable_path':execpath} if execpath else {}
    browser=p.chromium.launch(headless=True,**kw,args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1366,'height':1000},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(html,wait_until='load')
    assertcheck('Title','ROOT V86' in page.title())
    assertcheck('Six meaningful sliders',page.locator('input[type="range"]').count()==6)
    assertcheck('Chart visible',page.locator('#plot').is_visible())
    assertcheck('Warning of no real experiment','没有实际' in page.content())
    q0=float(page.locator('#qMetric').inner_text())
    assertcheck('Default Q is finite',.95<q0<1.05,str(q0))
    page.locator('#alpha').fill('0');page.locator('#alpha').dispatch_event('input')
    page.locator('#j2').fill('0');page.locator('#j2').dispatch_event('input')
    assertcheck('Newton Q equals 1',abs(float(page.locator('#qMetric').inner_text())-1)<1e-8)
    page.locator('#j2').fill('1.082626');page.locator('#j2').dispatch_event('input')
    qj=float(page.locator('#qMetric').inner_text())
    assertcheck('Known J2 shifts Q',abs(qj-1)>1e-5,str(qj))
    page.locator('#theta').fill('0');page.locator('#theta').dispatch_event('input')
    assertcheck('Pole differs from equator',float(page.locator('#qMetric').inner_text())<1)
    page.locator('#u').fill('0.15');page.locator('#u').dispatch_event('input')
    assertcheck('Universal u changes amplitude',float(page.locator('#forceMetric').inner_text())>1.1)
    page.locator('#alpha').fill('0.25');page.locator('#alpha').dispatch_event('input')
    assertcheck('Alpha changes Q',abs(float(page.locator('#qMetric').inner_text())-qj)>1e-4)
    page.locator('#range').fill('2.5');page.locator('#range').dispatch_event('input')
    assertcheck('Lambda label updates',page.locator('#rangeVal').inner_text()=='2.50')
    page.locator('#radius').fill('2');page.locator('#radius').dispatch_event('input')
    assertcheck('Radial control updates',page.locator('#radiusVal').inner_text()=='2.00')
    page.locator('#tab-rank').click()
    assertcheck('Rank tab visible',page.locator('#pane-rank').is_visible())
    assertcheck('D det zero',float(page.locator('#dRankMetric').inner_text())<1e-10)
    assertcheck('Eta det nonzero',float(page.locator('#etaRankMetric').inner_text())>1e-7)
    page.locator('#tab-constraints').click()
    assertcheck('2026 reference shown','PDG 2026' in page.locator('#pane-constraints').inner_text())
    page.locator('#tab-protocol').click()
    assertcheck('Protocol visible','RANDOMIZE' in page.locator('#pane-protocol').inner_text())
    page.locator('#tab-proof').click()
    assertcheck('Proof tab visible',page.locator('#pane-proof').is_visible())
    assertcheck('No JS page errors',not errors,str(errors))
    root.joinpath('results').mkdir(exist_ok=True)
    page.screenshot(path=str(root/'results/web_chromium_actual.png'),full_page=True)
    assertcheck('Screenshot generated',(root/'results/web_chromium_actual.png').stat().st_size>15_000)
    browser.close()
report={'checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),
        'method':'Chromium loaded exactly web/index.html HTML text with set_content; browser local file URL restricted in environment',
        'errors':errors}
(root/'results/browser_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
print('Chromium checks',report['passed'],'/',report['total'])
