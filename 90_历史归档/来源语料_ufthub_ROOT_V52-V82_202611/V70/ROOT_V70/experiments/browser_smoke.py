"""Real Chromium browser smoke validation of offline ROOT V70 UI."""
import json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
base=Path(__file__).resolve().parents[1]
url=(base/'web'/'index.html').as_uri()
issues=[]; checks={}
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
    page=browser.new_page(viewport={'width':1360,'height':980},device_scale_factor=1)
    page.on('pageerror',lambda err:issues.append('PAGE '+str(err)))
    page.on('console',lambda msg:issues.append('CONSOLE '+msg.text) if msg.type=='error' else None)
    page.set_content((base/'web'/'index.html').read_text(encoding='utf-8'),wait_until='load',timeout=15000)
    checks['initial_title']=page.title().startswith('ROOT V70')
    checks['body_options']=page.locator('#body option').count()==9
    checks['mat_options']=page.locator('#matA option').count()==5
    checks['initial_earth']=page.evaluate('window.ROOTV70.calc().b.name === "Earth"')
    page.locator('#lat').fill('0')
    page.locator('#alt').fill('0')
    g0=page.evaluate('window.ROOTV70.calc().g')
    checks['earth_g_range']=9.7<g0<9.9
    page.locator('#body').select_option('Jupiter')
    checks['jupiter_change']=page.evaluate('window.ROOTV70.calc().g')>20
    page.locator('#body').select_option('Earth')
    page.locator('#alt').fill('50')
    checks['altitude_decreases_g']=page.evaluate('window.ROOTV70.calc().g')<g0
    page.locator('#alt').fill('0')
    page.locator('#matB').select_option('Ti')
    checks['same_material_zero_eta']=abs(page.evaluate('window.ROOTV70.calc().eta'))<1e-30
    page.locator('#matB').select_option('Pt')
    checks['different_material_eta']=abs(page.evaluate('window.ROOTV70.calc().eta'))>1e-20
    page.locator('button[data-tab="helix"]').click()
    checks['helix_pane_visible']=page.locator('#helixPane').is_visible()
    before=page.locator('#helixStats').inner_text()
    page.locator('#helixAngle').fill('60')
    checks['helix_changes']=page.locator('#helixStats').inner_text()!=before
    page.screenshot(path=str(base/'results'/'browser_v70_helix.png'),full_page=True)
    page.locator('button[data-tab="design"]').click()
    checks['rank_pane_visible']=page.locator('#designPane').is_visible()
    checks['rank_text']=('3 / 3' in page.locator('#designPane').inner_text())
    page.screenshot(path=str(base/'results'/'browser_v70_identifiability.png'),full_page=True)
    page.locator('button[data-tab="planet"]').click()
    checks['planet_back_visible']=page.locator('#planetPane').is_visible()
    page.locator('#body').select_option('Earth')
    page.screenshot(path=str(base/'results'/'browser_v70_real.png'),full_page=True)
    browser.close()
status=all(checks.values()) and not issues
report={'success':status,'checks':checks,'issues':issues,'url_scheme':'set_content because local file navigation is blocked by environment policy','render':'Canvas2D, not WebGL'}
(base/'results'/'browser_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if not status:sys.exit(1)
