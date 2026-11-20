from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
results={}
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1100,'height':780})
    # Restricted browser environment blocks file://. Test the exact same HTML via set_content.
    page.set_content((root/'web/index.html').read_text(encoding='utf-8'), wait_until='load')
    assert page.locator('h1').inner_text().startswith('ROOT V103')
    results['page_title']=True
    val=page.locator('#energy').inner_text();assert val.endswith(' J');results['initial_energy']=val
    before=page.locator('#torsion').inner_text()
    page.locator('#boost').fill('0')
    after=page.locator('#torsion').inner_text()
    assert after.startswith('0.0000') or after.startswith('-0.0000')
    results['boost_zero_torsion']=True
    page.locator('#beta').fill('0.3')
    assert page.locator('#energy').inner_text()!=val
    results['energy_slider']=True
    page.locator('#length').fill('0.3')
    assert '0.300 m' in page.locator('#lv').inner_text()
    results['length_slider']=True
    assert len(page.locator('#path').get_attribute('d'))>1000
    results['geometry_svg']=True
    page.screenshot(path=str(root/'figures/03_ACTUAL_CHROMIUM_SCREENSHOT.png'),full_page=True)
    browser.close()
(root/'results/BROWSER_SMOKE.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
