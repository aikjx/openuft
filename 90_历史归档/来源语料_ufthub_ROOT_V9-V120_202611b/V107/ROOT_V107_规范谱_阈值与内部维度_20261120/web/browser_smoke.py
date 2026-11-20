"""Optional Chromium UI test using installed Playwright; does not prove physical claims."""
from __future__ import annotations
from pathlib import Path
import json,shutil,os
root=Path(__file__).resolve().parent.parent

def run():
    from playwright.sync_api import sync_playwright
    checks={}
    with sync_playwright() as p:
        browser_path=os.environ.get('ROOT_CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
        launch_args={'headless':True,'args':['--no-sandbox']}
        if browser_path:launch_args['executable_path']=browser_path
        browser=p.chromium.launch(**launch_args)
        page=browser.new_page(viewport={'width':1280,'height':860},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda err: errors.append(str(err)))
        page.set_content((root/'web'/'index.html').read_text(encoding='utf-8'),wait_until='load')
        checks['page_title']='ROOT V107' in page.title()
        checks['default_sm_label']='最简 SM' in page.locator('#status').inner_text()
        checks['canvas_pixels']=page.evaluate("() => document.querySelector('canvas').width>300")
        page.locator('#applyTwo').click()
        checks['button_applies_two_pairs']=page.locator('#pairs').input_value()=='2'
        checks['triplet_mass_changed']='e+12' in page.locator('#mtVal').inner_text()
        page.locator('#applyDegenerate').click()
        checks['button_degenerate']=page.locator('#doublet').input_value()==page.locator('#triplet').input_value()
        page.locator('#pairs').select_option('1')
        checks['pair_select']='1 组' in page.locator('#status').inner_text()
        page.locator('#doublet').evaluate("el => {el.value='6'; el.dispatchEvent(new Event('input', {bubbles:true}));}")
        checks['slider_updates']='e+6' in page.locator('#mdVal').inner_text()
        checks['no_runtime_errors']=len(errors)==0
        (root/'figures').mkdir(exist_ok=True)
        page.locator('#applyTwo').click()
        page.screenshot(path=str(root/'figures'/'05_BROWSER_ACTUAL_SCREENSHOT.png'),full_page=True)
        checks['screenshot_created']=(root/'figures'/'05_BROWSER_ACTUAL_SCREENSHOT.png').exists()
        browser.close()
    (root/'results'/'BROWSER_SMOKE.json').write_text(json.dumps({'checks':checks,'errors':errors},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert all(checks.values()),checks
    print('Chromium UI checks passed:',len(checks))
    return checks
if __name__=='__main__':run()
