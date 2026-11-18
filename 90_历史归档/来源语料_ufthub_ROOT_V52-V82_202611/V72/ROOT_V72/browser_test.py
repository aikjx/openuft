"""Actual Chromium interactions with offline HTML; no network access required."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parent
results={'checks':[],'errors':[],'notes':['Canvas2D only; WebGL not claimed','synthetic interaction, not new physical observation']}
def check(name,condition):
    results['checks'].append({'name':name,'passed':bool(condition)})
    if not condition:raise AssertionError(name)
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1440,'height':980},device_scale_factor=1)
    page.on('pageerror',lambda e:results['errors'].append(str(e)))
    page.goto('about:blank')
    page.set_content((P/'web'/'index.html').read_text(encoding='utf-8'),wait_until='load')
    check('Title', 'ROOT V72' in page.title())
    check('Canvas helix visible',page.locator('#helix').is_visible())
    check('Canvas signal visible',page.locator('#signal').is_visible())
    check('Default earth g',abs(float(page.locator('#pg').inner_text())-9.82)<.01)
    page.locator('#planet').select_option('moon')
    check('Planet changes gravity',1.5<float(page.locator('#pg').inner_text())<1.75)
    page.locator('#planet').select_option('earth')
    page.locator('#height').fill('70')
    check('Height changes gravity',float(page.locator('#pg').inner_text())<5)
    page.locator('#height').fill('0')
    page.locator('#angle').fill('60')
    check('Helix decomposition',abs(float(page.locator('#vt').inner_text().replace('c',''))-.5)<.001)
    page.locator('#cam').fill('80')
    check('Camera slider callback',page.locator('#camTxt').inner_text()=='80°')
    page.locator('#beta').fill('5')
    check('Beta slider callback',page.locator('#betaTxt').inner_text()=='5.00')
    page.locator('#orient').fill('-1')
    check('Orientation reverses feature',float(page.locator('#fx').inner_text())<0)
    page.locator('#q').fill('0')
    check('Null material feature',float(page.locator('#fs').inner_text())==0)
    check('Four synthetic states shown',page.locator('#fourrows tr').count()==4)
    page.screenshot(path=str(P/'results'/'ROOT_V72_网页实测截图.png'),full_page=True)
    check('No JS page errors',len(results['errors'])==0)
    browser.close()
results['passed']=sum(x['passed'] for x in results['checks'])
results['failed']=len(results['checks'])-results['passed']
(P/'results'/'browser_test.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':results['passed'],'failed':results['failed'],'errors':results['errors']},ensure_ascii=False))
