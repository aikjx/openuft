"""Chromium smoke and numerical cross-check on exactly same HTML bytes."""
from pathlib import Path
import json,math,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'web/index.html').read_text(encoding='utf8')
sys.path.insert(0,str(ROOT))
from src.bmv import Setup,phases,cross_phase,negativity,density,pure_concurrence
checks={}
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1280,'height':900},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
 page.set_content(html,wait_until='domcontentloaded')
 page.wait_for_selector('#phase')
 def numeric(which):return float(page.locator(which).inner_text().strip().split(' ')[0])
 def close(a,b,tol=1e-4):return math.isclose(a,b,rel_tol=tol,abs_tol=tol*max(abs(b),1e-10))
 p=Setup()
 checks['no_js_exceptions']=not errors
 checks['default_phase_matches_python']=close(numeric('#phase'),cross_phase(phases(p)))
 checks['default_concurrence_matches_python']=close(numeric('#conc'),pure_concurrence(phases(p)))
 checks['default_negativity_matches_python']=close(numeric('#neg'),negativity(density(p)))
 checks['default_distance_matrix']=('450.00' in page.locator('#rmat').inner_text())
 checks['offline_graph_canvas']=page.locator('#chart').evaluate('(n)=>n.getContext("2d").getImageData(30,30,1,1).data[3]>0')
 page.locator('#gamma').fill('0.02')
 checks['dephasing_negativity_matches_python']=close(numeric('#neg'),negativity(density(Setup(gamma1=.02,gamma2=.02))))
 page.locator('#gamma').fill('0.05')
 checks['strong_dephasing_zero']=abs(numeric('#neg'))<1e-9
 page.locator('#gamma').fill('0')
 page.locator('#s').fill('0')
 checks['collapsed_path_no_entanglement']=abs(numeric('#conc'))<1e-9 and abs(numeric('#phase'))<1e-9
 page.locator('#s').fill('200')
 page.locator('#charge').fill('1')
 checks['coulomb_can_cancel_gravity']=abs(numeric('#phase'))<1e-9
 page.locator('#charge').fill('0')
 page.locator('#t').fill('0')
 checks['zero_time_no_entanglement']=abs(numeric('#conc'))<1e-9
 page.locator('#t').fill('1')
 page.locator('#mass').fill('-13.5')
 p=Setup(m1=10**-13.5,m2=10**-13.5)
 checks['mass_slider_changes_phase']=close(numeric('#phase'),cross_phase(phases(p)))
 page.locator('#mass').fill('-14')
 page.locator('#d').fill('800')
 p=Setup(d=800e-6)
 checks['distance_slider_changes_phase']=close(numeric('#phase'),cross_phase(phases(p)))
 for b in page.locator('[data-tab]').all():b.click()
 checks['tabs_operational']=page.locator('[data-tab].active').count()==1
 page.locator('[data-tab="gamma"]').click()
 page.screenshot(path=str(ROOT/'results/browser_verified.png'),full_page=True)
 checks['screenshot_written']=(ROOT/'results/browser_verified.png').exists()
 checks['scientific_disclaimer']=('理论或合成模拟' in html and '不代表真实量子引力观测' in html)
 checks['final_no_js_errors']=not errors
 browser.close()
 (ROOT/'results/browser_checks.json').write_text(json.dumps({'count':len(checks),'passed':sum(checks.values()),'checks':checks,'page_errors':errors},ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({'count':len(checks),'passed':sum(checks.values()),'failed':[k for k,v in checks.items() if not v],'errors':errors},indent=2))
 if not all(checks.values()):raise SystemExit(1)
