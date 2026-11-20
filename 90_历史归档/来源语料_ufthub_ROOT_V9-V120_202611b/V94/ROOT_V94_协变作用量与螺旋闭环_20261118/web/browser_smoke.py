"""Optional actual Chromium smoke test, loading HTML content for sandbox compatibility."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'web/index.html').read_text(encoding='utf-8')
with sync_playwright() as p:
    br=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    page=br.new_page(viewport={'width':1400,'height':1000},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda err:errors.append(str(err)))
    page.set_content(html,wait_until='load')
    page.wait_for_timeout(150)
    page.click('#play')  # freeze for deterministic values
    before=page.locator('#magnetic').inner_text()
    page.locator('#beta').fill('0.5')
    after=page.locator('#magnetic').inner_text()
    assert before!=after,(before,after)
    page.locator('#m').fill('3')
    assert page.locator('#closed').inner_text().startswith('是')
    page.locator('#reset').click()
    assert page.locator('#beta').input_value()=='0.8'
    assert len(errors)==0,errors
    screenshot=ROOT/'figures'/'CHROMIUM_ACTUAL_SCREENSHOT.png'
    page.screenshot(path=str(screenshot),full_page=True)
    result={'status':'PASS','method':'set_content of exact offline HTML; NOT direct file:// access','chromium_version':br.version,
            'controls_tested':['play','beta','m','reset'],'initial_B':before,'changed_B':after,
            'runtime_js_errors':errors,'screenshot':str(screenshot.relative_to(ROOT))}
    (ROOT/'results'/'BROWSER_SMOKE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    br.close()
    print(json.dumps(result,ensure_ascii=False))
