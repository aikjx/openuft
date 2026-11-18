"""Actual Chromium headless interaction; HTML runs offline, same bytes as delivered.
Requires playwright and existing chromium; optional for end user.
"""
import json,pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent
html=(ROOT/'web/index.html').read_text(encoding='utf-8')
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1420,'height':1000},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda ex: errors.append(str(ex)))
    page.set_content(html,wait_until='load')
    checks={}
    checks['page_title']='ROOT V74' in page.title()
    checks['canvas_present']=page.locator('#scene').count()==1
    checks['initial_g']='9.820' in page.locator('#gValue').inner_text()
    page.locator('#body').select_option('Moon')
    checks['planet_switch']='1.623' in page.locator('#gValue').inner_text()
    page.locator('#body').select_option('Earth')
    before=page.locator('#yValue').inner_text();page.locator('#lambdaLog').fill('7')
    checks['yukawa_slider_changes']=before!=page.locator('#yValue').inner_text()
    page.locator('button[data-mode="gb"]').click()
    checks['gauss_bonnet_mode']='m²eff' in page.locator('#equation').inner_text() or 'ηℓ' in page.locator('#equation').inner_text()
    page.locator('#massLog').fill('-14')
    checks['xi_computed']=page.locator('#xiValue').inner_text() not in ('','N/A')
    page.locator('button[data-mode="yukawa"]').click()
    checks['yukawa_mode']='gY/gN' in page.locator('#equation').inner_text()
    page.locator('button[data-mode="planet"]').click()
    checks['planet_mode']='K(R)' in page.locator('#equation').inner_text()
    page.locator('button[data-mode="helix"]').click()
    checks['helix_mode']='τ=' in page.locator('#equation').inner_text()
    page.locator('#pitch').fill('66');checks['pitch_moves']='66' in page.locator('#pitchV').inner_text()
    page.locator('#searchEq').fill('曲率')
    checks['equation_search']=page.locator('#eqBody tr').count()>=1
    page.locator('#searchEq').fill('不存在这种方程')
    checks['equation_search_empty']=page.locator('#eqBody tr').count()==0
    page.locator('#searchEq').fill('')
    checks['equation_search_restore']=page.locator('#eqBody tr').count()==20
    checks['no_js_errors']=not errors
    page.screenshot(path=str(ROOT/'results/v74_browser_actual.png'),full_page=True)
    browser.close()
report={'checks':checks,'passed':sum(checks.values()),'count':len(checks),'js_errors':errors}
(ROOT/'results/browser_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if not all(checks.values()):raise SystemExit('Browser smoke checks failed')
