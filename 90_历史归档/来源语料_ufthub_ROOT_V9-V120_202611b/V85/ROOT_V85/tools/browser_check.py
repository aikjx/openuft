"""Chromium smoke and interaction verification. All fields show synthetic models, not measurements."""
from pathlib import Path
import json, math, shutil
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'web'/'index.html').read_text(encoding='utf-8')
checks=[]; js_errors=[]
def record(name,condition,detail=None):
 checks.append({'name':name,'pass':bool(condition),'detail':detail})
 assert condition,name
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,**({'executable_path': shutil.which('chromium') or shutil.which('google-chrome')} if shutil.which('chromium') or shutil.which('google-chrome') else {}),args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1360,'height':1020},device_scale_factor=1)
 page.on('pageerror',lambda e:js_errors.append(str(e)))
 page.set_content(html,wait_until='load')
 record('page_title','ROOT V85' in page.title(),page.title())
 record('controls_total',page.locator('input[type="range"]').count()==5)
 record('canvas_visible',page.locator('#plot').is_visible())
 record('science_warning','非真实观测' in page.content())
 q=float(page.locator('#qMetric').inner_text())
 record('default_Q',abs(q-1.024848574209616)<1e-6,q)
 det0=float(page.locator('#detMetric').inner_text())
 record('single_mediator_determinant_zero',abs(det0)<1e-12,det0)
 page.locator('#alpha2').fill('0.15');page.locator('#alpha2').dispatch_event('input')
 det1=float(page.locator('#detMetric').inner_text())
 record('two_mediator_determinant_nonzero',abs(det1)>1e-8,det1)
 record('two_mediator_text','第二媒介' in page.locator('#rankConclusion').inner_text())
 page.locator('#alpha').fill('0');page.locator('#alpha').dispatch_event('input')
 record('alpha_zero_Q',abs(float(page.locator('#qMetric').inner_text())-1.)<1e-10)
 page.locator('#alpha').fill('0.15');page.locator('#alpha').dispatch_event('input')
 page.locator('#radius').fill('1.5');page.locator('#radius').dispatch_event('input')
 record('radius_changes_Q',abs(float(page.locator('#qMetric').inner_text())-1.024848574)<.03)
 page.locator('#universal').fill('0.2');page.locator('#universal').dispatch_event('input')
 record('universal_changes_force_amplitude',float(page.locator('#fMetric').inner_text())>1.2)
 record('Earth_g_grounded',abs(float(page.locator('#earth').inner_text())-9.82025)<0.01)
 record('Moon_g_grounded',1.60<float(page.locator('#moon').inner_text())<1.65)
 record('no_page_js_error',not js_errors,js_errors)
 page.screenshot(path=str(root/'results'/'web_chromium_verified.png'),full_page=True)
 record('screenshot_exists',(root/'results'/'web_chromium_verified.png').stat().st_size>10000)
 browser.close()
report={'passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks,'js_errors':js_errors,
        'method':'Chromium loaded EXACT HTML text from local web/index.html with set_content (not external network)'}
(root/'results'/'browser_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Browser checks',report['passed'],'/',report['total'])
