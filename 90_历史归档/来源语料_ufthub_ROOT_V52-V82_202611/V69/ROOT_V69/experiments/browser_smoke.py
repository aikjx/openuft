"""Chromium browser smoke; loads actual HTML bytes with set_content due sandbox file URL restriction.
Cannot assert physically real 3D GPU rendering: canvas perspective only.
"""
from pathlib import Path
import json,sys,traceback
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parents[1]
LOG=P/'results/browser_smoke.json'
errors=[];checks={}
with sync_playwright() as play:
    browser=play.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1360,'height':910},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content((P/'web/index.html').read_text(encoding='utf-8'),wait_until='load',timeout=25000)
    page.wait_for_timeout(250)
    checks['title_loaded']=page.title().startswith('ROOT V69')
    checks['default_earth']=page.locator('#body').input_value()=='Earth'
    checks['all_bodies']=page.locator('#body option').count()==10
    checks['default_numeric_surface']=page.locator('#mv2').inner_text().strip() not in ('','—')
    page.locator('#body').select_option('Jupiter');page.wait_for_timeout(120)
    checks['jupiter_selector']=page.locator('#body').input_value()=='Jupiter'
    checks['jupiter_gravity']=float(page.locator('#mv1').inner_text())>20
    page.locator('#body').select_option('Earth')
    page.locator('#lat').fill('0');page.locator('#lat').dispatch_event('input');page.wait_for_timeout(150)
    eq=float(page.locator('#mv2').inner_text());
    page.locator('#lat').fill('90');page.locator('#lat').dispatch_event('input');page.wait_for_timeout(150)
    pole=float(page.locator('#mv2').inner_text());
    checks['earth_pole_greater_than_equator']=pole>eq
    page.locator('[data-tab=interior]').click();page.wait_for_timeout(120)
    checks['interior_tab']=page.locator('#mk2').inner_text()=='分层球内引力'
    page.locator('[data-tab=ep]').click();page.wait_for_timeout(120)
    checks['ep_tab']=page.locator('#mk1').inner_text()=='示例 η'
    page.locator('#alphaLog').fill('-12');page.locator('#alphaLog').dispatch_event('input');page.wait_for_timeout(120)
    checks['ep_alpha_changed']=page.locator('#alphaLog').input_value()=='-12'
    page.locator('[data-tab=helix]').click();page.wait_for_timeout(150)
    checks['helix_tab']=page.locator('#mk1').inner_text()=='环向速度'
    page.locator('#angle').fill('90');page.locator('#angle').dispatch_event('input');page.wait_for_timeout(120)
    checks['helix_axial_at90']=abs(float(page.locator('#mv2').inner_text())-1)<.001
    # actual canvas has drawn pixels; manually verify nonempty
    checks['canvas_pixels_nonempty']=page.evaluate('''() => {const c=document.getElementById('scene');const d=c.getContext('2d').getImageData(0,0,15,15).data;return Array.from(d).some((x,i)=>i%4===3&&x>0)}''')
    page.locator('[data-tab=planet]').click();page.wait_for_timeout(130)
    page.screenshot(path=str(P/'results/browser_real_screenshot.png'),full_page=True)
    checks['no_javascript_errors']=len(errors)==0
    browser.close()
result={'checks':checks,'errors':errors,'passed':sum(checks.values()),'total':len(checks),'warning':'Sandbox blocked file:// navigation; verified actual HTML bytes via set_content; Canvas2D perspective, not WebGL or field data.'}
LOG.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
if not all(checks.values()):sys.exit(1)
