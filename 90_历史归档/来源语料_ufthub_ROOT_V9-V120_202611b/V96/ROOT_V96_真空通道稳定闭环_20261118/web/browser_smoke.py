"""Optional real Chromium test. Uses page.set_content for sandbox file URL restrictions."""
from pathlib import Path
import json, shutil
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
out=root/'results/BROWSER_SMOKE.json'
with sync_playwright() as p:
    exe=shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome')
    opts={'headless':True,'args':['--no-sandbox']}
    if exe: opts['executable_path']=exe
    browser=p.chromium.launch(**opts)
    page=browser.new_page(viewport={'width':1150,'height':900},device_scale_factor=1)
    page.set_content((root/'web/index.html').read_text(encoding='utf-8'),wait_until='load')
    before=page.locator('#n').inner_text()
    assert float(before)>.3
    assert 'A' in page.locator('#amps').inner_text()
    page.locator('#radius').fill('6')
    after=page.locator('#n').inner_text()
    assert abs(float(after)-float(before))>.1
    page.locator('#beta').evaluate("el=>{el.value='0.20';el.dispatchEvent(new Event('input',{bubbles:true}))}")
    assert page.locator('#bValue').inner_text()=='0.20'
    assert page.locator('#chart polyline').count()==1
    assert page.locator('#trajectory polyline').count()==1
    (root/'plots').mkdir(exist_ok=True)
    page.screenshot(path=str(root/'plots/04_CHROMIUM_ACTUAL_SCREENSHOT.png'),full_page=True)
    browser.close()
report={'browser':'Chromium Playwright headless actual execution','tests':5,'result':'PASS',
        'initial_field_index_n':before,'changed_field_index_n':after}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('V96 browser smoke',report)
