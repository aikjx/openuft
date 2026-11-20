"""Actual Chromium smoke for V101 offline HTML. This is UI-only, not physics validation."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1180,'height':850},device_scale_factor=1)
    page.set_content((R/'web/index.html').read_text(encoding='utf-8'),wait_until='load')
    assert 'ROOT V101' in page.title()
    before=page.locator('#knotted').inner_text()
    for sid in ['generic','knotted','voltage','field']:
        val=float(page.locator('#'+sid).inner_text())
        assert val>0
    page.locator('#beta').evaluate('el => { el.value="0.20"; el.dispatchEvent(new Event("input", {bubbles:true})); }')
    after=page.locator('#knotted').inner_text()
    assert before!=after
    page.locator('#length').evaluate('el => { el.value="0.30"; el.dispatchEvent(new Event("input", {bubbles:true})); }')
    afterlength=page.locator('#knotted').inner_text()
    assert afterlength!=after
    assert '0.30' in page.locator('#lengthLbl').inner_text()
    page.screenshot(path=str(R/'figures/04_CHROMIUM_ACTUAL_V101_SCREENSHOT.png'),full_page=True)
    result=dict(checks_passed=7,title=page.title(),initial_knot_J=before,beta_changed_knot_J=after,length_changed_knot_J=afterlength,screen='figures/04_CHROMIUM_ACTUAL_V101_SCREENSHOT.png')
    (R/'results/BROWSER_SMOKE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    browser.close()
    print(json.dumps(result,ensure_ascii=False,indent=2))
