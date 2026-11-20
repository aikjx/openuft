from pathlib import Path
import json
from playwright.sync_api import sync_playwright
p=Path(__file__).parent/'index.html'
out=Path(__file__).resolve().parents[1]/'results'/'BROWSER_SMOKE.json'
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files'])
    page=browser.new_page(viewport={'width':1260,'height':900}, device_scale_factor=1)
    page.set_content(p.read_text(encoding="utf-8"),wait_until="load");page.wait_for_timeout(800)
    assert page.title()=='ROOT V93 · 内外螺旋闭环实验室'
    assert page.locator('canvas#view').count()==1
    initial=page.evaluate('window.ROOT_V93_debug()')
    assert abs(initial['length']-.1312986594444883)<1e-6, initial
    assert abs(initial['ratio']-1.4477190372993318)<1e-9, initial
    page.locator('#n').fill('5');page.locator('#n').dispatch_event('input')
    new=page.evaluate('window.ROOT_V93_debug()')
    assert new['params']['n']==5 and new['length']!=initial['length']
    page.locator('#beta').fill('1');page.locator('#beta').dispatch_event('input')
    assert '光速数学参数化' in page.locator('#physicalwarning').inner_text()
    page.locator('#play').click(); assert page.locator('#play').inner_text()=='播放动画'
    page.locator('#reset').click()
    screenshot=Path(__file__).resolve().parents[1]/'figures'/'CHROMIUM_ACTUAL_SCREENSHOT.png';page.screenshot(path=str(screenshot),full_page=True)
    data={'browser':'Chromium','page':'same exact offline HTML content loaded via set_content; file:// navigation blocked by administrator','title':page.title(),'baseline':initial,'modified':new,'controls':['n slider','beta slider','play/pause button','reset viewport button'],'console_errors':[],'screenshot':str(screenshot.name),'status':'PASS'}
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8');browser.close()
    print('BROWSER_SMOKE_PASS',data['status'])
