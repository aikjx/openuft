"""Optional real Chromium smoke run for new dashboard, not a physics experiment."""
from pathlib import Path
import json,threading,shutil
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
root=Path(__file__).resolve().parents[1]
results={'browser_available':False,'page_loaded':False,'sliders_interactive':False,'screenshot':None,'js_errors':[]}
try:
    from playwright.sync_api import sync_playwright
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,executable_path=shutil.which('chromium') or shutil.which('google-chrome'),args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
            results['browser_available']=True
            page=browser.new_page(viewport={'width':1440,'height':980},device_scale_factor=1)
            page.on('pageerror',lambda error:results['js_errors'].append(str(error)))
            try:
                page.goto(f'http://127.0.0.1:{server.server_port}/web/index.html',wait_until='domcontentloaded',timeout=8000)
                results['loading_method']='local HTTP'
            except Exception:
                # Managed browser policy may reject localhost; still test JS and controls.
                page.set_content((root/'web'/'index.html').read_text(encoding='utf-8'),wait_until='load')
                results['loading_method']='set_content: inline JS, no local file navigation'
            page.wait_for_timeout(300)
            results['page_loaded']=page.title().startswith('ROOT V65')
            before=page.locator('#kappa').inner_text()
            page.eval_on_selector('#angle',"el => {el.value='65';el.dispatchEvent(new Event('input',{bubbles:true}))}")
            after=page.locator('#kappa').inner_text()
            assert before!=after, 'angle changes must update computed curvature'
            page.eval_on_selector('#alpha',"el => {el.value='2';el.dispatchEvent(new Event('input',{bubbles:true}))}")
            eta=page.locator('#eta').inner_text(); assert 'e-' in eta
            page.get_by_role('button',name='暂停旋转').click()
            assert page.get_by_role('button',name='恢复旋转').is_visible()
            page.locator('#reset').click()
            page.eval_on_selector('#angle',"el => {el.value='35';el.dispatchEvent(new Event('input',{bubbles:true}))}")
            page.eval_on_selector('#alpha',"el => {el.value='0';el.dispatchEvent(new Event('input',{bubbles:true}))}")
            page.wait_for_timeout(300)
            results['sliders_interactive']=True
            img=root/'results'/'v65_browser_smoke.png'
            page.screenshot(path=str(img),full_page=True)
            results['screenshot']=str(img.relative_to(root))
            browser.close()
    finally:server.shutdown();server.server_close()
except Exception as exc:
    results['error']=f'{type(exc).__name__}: {exc}'
(root/'results'/'v65_browser_smoke.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
if not results['page_loaded'] or not results['sliders_interactive'] or results['js_errors']:raise SystemExit(1)
