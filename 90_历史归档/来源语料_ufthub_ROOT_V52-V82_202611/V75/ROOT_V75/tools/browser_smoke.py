"""Offline browser test, runs with playwright + local chromium if installed.
Run: python tools/browser_smoke.py
"""
import json, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
from playwright.sync_api import sync_playwright
report={'checks':[],'console_errors':[],'page_errors':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1440,'height':1050},device_scale_factor=1)
 page.on('pageerror', lambda e:report['page_errors'].append(str(e)))
 page.on('console', lambda msg:report['console_errors'].append(msg.text) if msg.type=='error' else None)
 page.set_content((root/'web/index.html').read_text(encoding='utf-8'),wait_until='load')
 page.wait_for_timeout(300)
 report['checks'].append(('title',page.title().startswith('ROOT V75')))
 report['checks'].append(('metric initialized',page.locator('#grav').inner_text()!='—'))
 before=page.locator('#grav').inner_text()
 page.locator('#B').fill('20')
 page.wait_for_timeout(100)
 after=page.locator('#grav').inner_text()
 report['checks'].append(('B slider changes gravity',before!=after))
 page.locator('#phase').fill('90')
 page.wait_for_timeout(100)
 phase_energy=page.locator('#U').inner_text()
 report['checks'].append(('phase changes energy',phase_energy!=after))
 page.locator('#mode').select_option('rotating')
 report['checks'].append(('rotating mode updates', '磁场方向转动' in page.locator('#vnote').inner_text()))
 page.locator('#mode').select_option('earth')
 report['checks'].append(('earth mode updates','地球重力箭头' in page.locator('#vnote').inner_text()))
 page.locator('#reset').click()
 report['checks'].append(('reset B=10',page.locator('#vB').inner_text()=='10.0 T'))
 page.locator('#play').click();page.wait_for_timeout(100)
 report['checks'].append(('play control', '暂停' in page.locator('#play').inner_text()))
 page.locator('#play').click()
 report['checks'].append(('pause control', '演示' in page.locator('#play').inner_text()))
 report['checks'].append(('canvases visible',page.locator('canvas').count()==2))
 page.screenshot(path=str(root/'results'/'V75_交互网页实际截图.png'),full_page=True)
 browser.close()
report['passed']=sum(bool(c[1]) for c in report['checks']);report['total']=len(report['checks'])
(root/'results/browser_smoke.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if report['passed']!=report['total'] or report['console_errors'] or report['page_errors']:
 raise SystemExit('browser checks failed')
