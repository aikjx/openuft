"""Chromium browser smoke for offline WebGL/Canvas UIs; requires playwright + system Chromium.
Does not prove physical theory; browser environment may not have real GPU hardware.
"""
import pathlib, json, threading, http.server, socketserver, time
from playwright.sync_api import sync_playwright
root=pathlib.Path(__file__).resolve().parents[1]
class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
 def log_message(self,*args):pass
class TCP(socketserver.ThreadingTCPServer):allow_reuse_address=True
server=TCP(('127.0.0.1',0),Handler);port=server.server_address[1]
threading.Thread(target=server.serve_forever,daemon=True).start()
report={'base_url':'HTML injected in browser document; local navigation policy blocks localhost','chromium_real_gpu_verified':False,'tests':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--enable-unsafe-swiftshader'])
 page=browser.new_page(viewport={'width':1250,'height':850},device_scale_factor=1)
 errs=[];page.on('pageerror',lambda exc:errs.append(str(exc)))
 page.set_content((root/'web/index.html').read_text(encoding='utf-8'),wait_until='load')
 page.wait_for_timeout(950)
 assert page.locator('#vp').inner_text()!=''
 before=page.locator('#kap').inner_text()
 page.locator('#btnHelix').click()
 page.locator('#angle').fill('65');page.locator('#angle').dispatch_event('input')
 after=page.locator('#kap').inner_text()
 assert before!=after,(before,after)
 assert page.locator('#btnHelix').get_attribute('class')=='sel'
 page.screenshot(path=str(root/'results/3D_helix_browser.png'),full_page=True)
 report['tests'].append({'name':'3D helix mode+controls','passed':True,'geometry_changed':True})
 page.locator('#btnEarth').click();page.wait_for_timeout(300)
 page.screenshot(path=str(root/'results/3D_earth_browser.png'),full_page=True)
 report['tests'].append({'name':'3D earth mode+controls','passed':True})
 page=browser.new_page(viewport={'width':1250,'height':850},device_scale_factor=1)
 page.on('pageerror',lambda exc:errs.append(str(exc)))
 page.set_content((root/'web/v64_audit.html').read_text(encoding='utf-8'),wait_until='load');page.wait_for_timeout(350)
 page.locator('[data-kind="gravity"]').click(); assert '圆柱内外' in page.locator('#chartTitle').inner_text()
 page.locator('#line').fill('50');page.locator('#line').dispatch_event('input')
 assert page.locator('#lineTxt').inner_text()=='50 kg/m'
 page.locator('[data-kind="induced"]').click(); assert 'G' in page.locator('#chartTitle').inner_text()
 page.locator('#ell').fill('2');page.locator('#ell').dispatch_event('input')
 page.locator('[data-kind="wave"]').click()
 page.screenshot(path=str(root/'results/audit_browser.png'),full_page=True)
 report['tests'].append({'name':'numeric tabs and sliders','passed':True})
 assert not errs,errs
 report['tests'].append({'name':'javascript uncaught exceptions','passed':True,'errors':errs})
 gl_type=page.evaluate('''() => {let a=document.createElement('canvas');return !!a.getContext('webgl2')}''')
 report['webgl2_context_created_in_headless_environment']=gl_type
 browser.close()
server.shutdown();(root/'results/browser_smoke.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))
