"""Browser smoke tests of offline UI. Requires Playwright+Chromium (optional)."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from rootv71.physics import uniform_ratio,layered_ratio,same_mass_layered_shells
P=Path(__file__).resolve().parent
page_url=(P/'web'/'index.html').resolve().as_uri()
checks=[]; errors=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'])
    page=browser.new_page(viewport={'width':1366,'height':850},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    # The test runner policy blocks file:// access; load identical HTML as content.
    page.set_content((P/'web'/'index.html').read_text(encoding='utf-8'),wait_until='load')
    page.wait_for_timeout(350)
    checks.append(('title', 'ROOT V71' in page.title()))
    checks.append(('initial metrics', page.locator('#uniformVal').inner_text()!='—'))
    checks.append(('equations count', '95' in page.locator('#eqCount').inner_text()))
    checks.append(('methods count', '67' in page.locator('#methodCount').inner_text()))
    val1=page.locator('#uniformVal').inner_text()
    page.locator('#range').fill('-1.56');page.wait_for_timeout(110)
    checks.append(('Yukawa range updates prediction',page.locator('#uniformVal').inner_text()!=val1))
    page.locator('#body').select_option('Moon');page.wait_for_timeout(100)
    checks.append(('Body selection updates labels',page.locator('#kmVal').inner_text()!='—'))
    page.locator('#alpha').fill('0');page.wait_for_timeout(100)
    checks.append(('Zero alpha gives zero correction',float(page.locator('#uniformVal').inner_text())==0.))
    page.eval_on_selector('#alpha','el=>{el.value="0.10";el.dispatchEvent(new Event("input",{bubbles:true}));}');page.wait_for_timeout(80)
    checks.append(('Restored alpha nonzero',float(page.locator('#uniformVal').inner_text())>0.))
    page.locator('#core').fill('2.5');page.wait_for_timeout(80)
    checks.append(('Core source charge updates',page.locator('#coreShow').inner_text()=='2.5'))
    checks.append(('2D canvas rendered',page.evaluate("document.querySelector('#curve').width > 100")))
    page.screenshot(path=str(P/'results'/'web_lab.png'),full_page=True)
    page.locator('button[data-tab="equations"]').click()
    checks.append(('Equation tab open',page.locator('#equations').evaluate('(el)=>el.classList.contains("active")')))
    page.locator('#eqSearch').fill('Yukawa');page.wait_for_timeout(100)
    checks.append(('Equation search filters',page.locator('#eqRows tr').count()>0 and page.locator('#eqRows tr').count()<95))
    page.screenshot(path=str(P/'results'/'web_equations.png'),full_page=True)
    page.locator('button[data-tab="methods"]').click()
    page.locator('#methodSearch').fill('挠率');page.wait_for_timeout(100)
    checks.append(('Method search filters',0<page.locator('#methodRows tr').count()<67))
    page.locator('button[data-tab="status"]').click()
    checks.append(('Status warning visible','未从 ROOT' in page.locator('#status').inner_text()))
    # Cross-language verification of browser formulas against independent Python implementation.
    for label,R,lam,core,shell in [('short',6378137.,1e5,1.,1.),('mid',6378137.,1e6,2.,1.),('long',1737500.,5e7,-.5,1.4)]:
        js=page.evaluate('([R,lam,c,s])=>calc(R,0,lam,1,c,s)',[R,lam,core,shell])
        py_u=uniform_ratio(R,0,lam)
        py_l=layered_ratio(same_mass_layered_shells(R,qcore=core,qshell=shell),0,lam)
        checks.append((f'JS/Python finite-size crosscheck {label}', abs(js['uniform']-py_u)<max(1e-13,abs(py_u)*1e-10) and abs(js['layered']-py_l)<max(1e-13,abs(py_l)*1e-10)))
    checks.append(('No JavaScript page errors',len(errors)==0))
    browser.close()
result={'checks':len(checks),'passed':sum(int(ok) for _,ok in checks),'failed':[name for name,ok in checks if not ok],
        'page_errors':errors,'scope':'Chromium offline UI smoke; not physical empirical validation',
        'details':[{'name':n,'pass':bool(v)} for n,v in checks]}
(P/'results'/'browser_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
if result['passed']!=result['checks']:raise SystemExit(1)
