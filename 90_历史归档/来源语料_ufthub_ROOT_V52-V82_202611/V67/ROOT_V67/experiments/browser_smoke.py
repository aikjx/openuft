"""Smoke-test actual offline browser interactions. Requires playwright and chromium."""
import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
url=(root/'web/index.html').resolve().as_uri()
report={'file_url':url,'tab_interactions':{},'console_errors':[],'page_errors':[]}
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path=os.getenv('CHROMIUM_EXECUTABLE','/usr/bin/chromium'),args=['--no-sandbox','--disable-gpu'])
    page=browser.new_page(viewport={'width':1350,'height':900},device_scale_factor=1)
    page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
    page.on('console',lambda m:report['console_errors'].append(m.text) if m.type=='error' else None)
    # This sandbox blocks file:// navigation, so load the exact offline HTML bytes.
    # This verifies inline script interactions, but does not test file URL permissions.
    report['load_method']='page.set_content (file URL navigation blocked in sandbox)'
    page.set_content((root/'web/index.html').read_text(encoding='utf-8'),wait_until='load',timeout=20000)
    page.wait_for_timeout(150)
    assert page.locator('#metrics .metric').count()==3
    for tab,slider,new_value in [('helix','pitch','49'),('earth','lat','62'),('rg','rgzoom','17'),('g','N','31'),('fifth','beta','-13.5')]:
        page.locator('[data-tab="'+tab+'"]').click()
        page.locator('#i_'+slider).fill(new_value)
        page.wait_for_timeout(45)
        count=page.locator('#metrics .metric').count()
        assert count==3,(tab,count)
        value=page.locator('#o_'+slider).inner_text()
        assert new_value in value,(tab,slider,new_value,value)
        report['tab_interactions'][tab]={'slider':slider,'new_value':value,'metrics_count':count}
        page.screenshot(path=str(root/'results'/f'web_{tab}.png'),full_page=False)
    assert not report['page_errors'] and not report['console_errors'],report
    report['pass']=True
    browser.close()
(root/'results/browser_smoke.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
