from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
html=(root/'web/index.html').read_text(encoding='utf-8')
result={'checks':[],'browser':'Chromium','source':'local offline HTML, page.set_content'}
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1240,'height':900},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
    page.set_content(html,wait_until='load')
    page.wait_for_timeout(350)
    assert page.title()=='ROOT V95 · 有限磁能内外螺旋实验室';result['checks'].append('title')
    assert page.locator('#orbital').count()==1;result['checks'].append('canvas')
    base=page.locator('#energy').inner_text()
    page.locator('#eps').evaluate('(e)=>{e.value="0.50";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    assert page.locator('#energy').inner_text()!=base;result['checks'].append('radius_slider_energy')
    old=page.locator('#period').inner_text()
    page.locator('#beta').evaluate('(e)=>{e.value="0.50";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    assert page.locator('#period').inner_text()!=old;result['checks'].append('beta_slider_period')
    page.locator('#pause').click();assert page.locator('#pause').inner_text()=='继续动画';result['checks'].append('pause')
    page.locator('#angle').evaluate('(e)=>{e.value="80";e.dispatchEvent(new Event("input",{bubbles:true}))}')
    page.locator('#reset').click();assert page.locator('#angle').input_value()=='28';result['checks'].append('reset')
    assert not errors, errors
    result['checks'].append('no_page_errors')
    page.screenshot(path=str(root/'figures'/'05_CHROMIUM_ACTUAL_SCREENSHOT.png'),full_page=True)
    browser.close()
(root/'results'/'BROWSER_VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
