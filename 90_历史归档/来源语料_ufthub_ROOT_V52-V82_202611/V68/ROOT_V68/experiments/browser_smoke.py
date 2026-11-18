"""Offline HTML byte-for-byte Chromium smoke test. Uses set_content if file:// blocked."""
from pathlib import Path
import json,os
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
result={'loader':'page.set_content from exact web/index.html bytes, not disk URL navigation',
        'tabs':{},'page_errors':[],'console_errors':[],'passed':False,
        'limitation':'Does not independently verify file:// access on local computers or GPU WebGL (Canvas2D only).'}
with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path=os.getenv('CHROMIUM_EXECUTABLE','/usr/bin/chromium'),args=['--no-sandbox','--disable-gpu'])
    p=b.new_page(viewport={'width':1360,'height':880},device_scale_factor=1)
    p.on('pageerror',lambda e:result['page_errors'].append(str(e)))
    p.on('console',lambda m:result['console_errors'].append(m.text) if m.type=='error' else None)
    p.set_content((root/'web/index.html').read_text(encoding='utf-8'),wait_until='load')
    tasks=[('helix','angle','52','hk'),('gravity','species','29','gl'),('gauge','alphas','0.12','r12'),('fifth','alpha5','-0.7','eta')]
    for tab,slider,setting,metric in tasks:
        p.locator('[data-tab="'+tab+'"]').click()
        p.locator('#'+slider).fill(setting)
        p.wait_for_timeout(120)
        measured=p.locator('#'+metric).inner_text()
        assert measured and measured!='—',(tab,measured)
        p.locator('#canvas-'+tab).screenshot(path=str(root/'results'/f'web_{tab}.png'))
        result['tabs'][tab]={'input':slider,'requested':setting,'output_metric':metric,'displayed':measured}
    p.locator('[data-tab="audit"]').click()
    assert p.locator('#tab-audit tbody tr').count()>=8
    assert not result['page_errors'] and not result['console_errors'],result
    result['passed']=True
    b.close()
(root/'results/browser_smoke.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
