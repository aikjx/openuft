"""Actual offline Chromium smoke test. Page content loaded directly (file:// not required)."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'web/index.html').read_text(encoding='utf-8')
checks={}
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1200,'height':820},device_scale_factor=1)
    failures=[]
    page.on('pageerror',lambda e:failures.append(str(e)))
    page.set_content(html,wait_until='load')
    checks['default_rank6']=page.locator('#rank').inner_text().strip()=='6 / 6'
    checks['default_condition_finite']=page.locator('#cond').inner_text().strip() not in ('∞（欠定）','')
    page.locator('#probeN').select_option('2')
    checks['two_probes_rank5']=page.locator('#rank').inner_text().strip()=='5 / 6'
    page.locator('#probeN').select_option('1')
    checks['one_probe_rank3']=page.locator('#rank').inner_text().strip()=='3 / 6'
    page.locator('#probeN').select_option('3')
    page.locator('#angle').fill('0'); page.locator('#angle').dispatch_event('input')
    checks['collinear_rank5']=page.locator('#rank').inner_text().strip()=='5 / 6'
    page.locator('#angle').fill('60');page.locator('#angle').dispatch_event('input')
    checks['sixty_degree_rank6']=page.locator('#rank').inner_text().strip()=='6 / 6'
    checks['reconstructed_components']=('恢复磁场' in page.locator('#result').inner_text())
    checks['js_errors_empty']=not failures
    page.screenshot(path=str(ROOT/'figures/03_CHROMIUM_ACTUAL_THEORY_PAGE.png'),full_page=True)
    browser.close()
report={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'js_errors':failures}
(ROOT/'results/BROWSER_SMOKE.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))
if not all(checks.values()):raise SystemExit(1)
