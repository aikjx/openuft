"""Actual Chromium smoke verification on exactly local HTML bytes via set_content."""
from pathlib import Path
import sys,math,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.quantum_gravity_audit import Config,phases,cross,pure_concurrence,negativity,rho_dephased,scale_terms,q_equivalent
checks={}; errors=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    page=b.new_page(viewport={'width':1380,'height':1000},device_scale_factor=1)
    page.on('pageerror',lambda exc:errors.append(str(exc)))
    page.set_content((ROOT/'web/index.html').read_text(encoding='utf8'),wait_until='domcontentloaded')
    page.wait_for_selector('#phase')
    val=lambda s:float(page.locator(s).inner_text().split()[0].strip())
    close=lambda a,b:math.isclose(a,b,abs_tol=2e-8*max(1,abs(b)),rel_tol=2e-5)
    base=Config()
    checks['no_page_errors']=not errors
    checks['title_present']='ROOT V89' in page.title()
    checks['default_phase_python']=close(val('#phase'),cross(phases(base)))
    checks['default_concurrence_python']=close(val('#conc'),pure_concurrence(phases(base)))
    checks['default_negativity_python']=close(val('#neg'),negativity(rho_dephased(base)))
    checks['default_eft_python']=math.isclose(val('#qeft'),scale_terms(base)['eft_loop_potential'],rel_tol=1e-5)
    checks['default_pn_python']=math.isclose(val('#pn'),scale_terms(base)['one_pn_potential'],rel_tol=1e-5)
    checks['qequiv_python']=math.isclose(float(page.locator('#qeq').inner_text().split()[0]),q_equivalent(base),rel_tol=1e-4)
    checks['plot_pixel_rendered']=page.locator('#plot').evaluate('(c)=>c.getContext("2d").getImageData(20,20,1,1).data[3]>0')
    checks['matrix_shown']='450.00' in page.locator('#rmat').inner_text()
    page.locator('#gamma').fill('0.02')
    from dataclasses import replace
    checks['dephasing_python']=close(val('#neg'),negativity(rho_dephased(replace(base,gamma1=.02,gamma2=.02))))
    page.locator('#gamma').fill('0.12')
    checks['strong_dephasing_zero']=abs(val('#neg'))<1e-12
    page.locator('#gamma').fill('0')
    page.locator('#s').fill('0')
    checks['collapsed_path_phase_zero']=abs(val('#phase'))<1e-12
    checks['collapsed_path_entanglement_zero']=abs(val('#conc'))<1e-12
    page.locator('#s').fill('200')
    page.locator('#charge').fill('1')
    checks['charge_cancel']=abs(val('#phase'))<1e-12
    page.locator('#charge').fill('0')
    page.locator('#t').fill('0')
    checks['zero_time_phase']=abs(val('#phase'))<1e-12
    page.locator('#t').fill('1')
    page.locator('#m').fill('-13.5')
    p=replace(base,m1=10**-13.5,m2=10**-13.5)
    checks['mass_change_python']=close(val('#phase'),cross(phases(p)))
    page.locator('#m').fill('-14')
    page.locator('#d').fill('800')
    checks['distance_change_python']=close(val('#phase'),cross(phases(replace(base,d=.0008))))
    checks['EFT_tiny']=1e-65<abs(val('#qeft'))<1e-61
    checks['null_artifact_high']=abs(val('#artifactratio'))>1e30
    for tab in page.locator('[data-tab]').all(): tab.click()
    checks['all_tabs_work']=page.locator('[data-tab].active').count()==1
    page.locator('[data-tab="filter"]').click()
    page.screenshot(path=str(ROOT/'results/browser_verified.png'),full_page=True)
    checks['screenshot_created']=(ROOT/'results/browser_verified.png').exists()
    checks['disclaimer']='非真实量子引力观测' in page.content()
    checks['no_late_errors']=not errors
    b.close()
result={'count':len(checks),'passed':sum(checks.values()),'checks':checks,'errors':errors,
        'method':'actual Chromium set_content of identical HTML bytes','not_hardware_validation':True}
(ROOT/'results/browser_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'count':result['count'],'passed':result['passed'],'failed':[k for k,v in checks.items() if not v],'errors':errors},indent=2))
if not all(checks.values()):raise SystemExit(1)
