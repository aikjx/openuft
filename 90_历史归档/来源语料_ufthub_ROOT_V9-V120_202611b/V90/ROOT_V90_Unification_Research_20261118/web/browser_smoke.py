"""Optional Chromium GUI smoke with self-contained HTML inserted via set_content.
No network access and no physical evidence. Repro with local Playwright and Chromium installed.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
html=(Path(__file__).resolve().parent/'index.html').read_text(encoding='utf-8')
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1280,'height':1000},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(html,wait_until='load')
    assert 'ROOT V90' in page.title()
    before=page.locator('#nulled').inner_text()
    assert before.endswith('rad') and 'NaN' not in before
    page.locator('#lambda').fill('-2')
    after=page.locator('#nulled').inner_text()
    assert before!=after,(before,after)
    page.locator('#alpha').fill('0')
    assert '0.00000e+0' in page.locator('#nulled').inner_text()
    page.locator('#alpha').fill('0.5')
    assert not errors,errors
    screenshot=Path(__file__).resolve().parents[1]/'results'/'chromium_v90_smoke.png'
    page.screenshot(path=str(screenshot),full_page=True)
    print('PASS: Chromium title, rendered outputs, lambda & alpha controls, JS errors=0; screenshot:',screenshot)
    browser.close()
