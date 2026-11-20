"""Playwright actual Chromium test. Passes HTML source as content to avoid file scheme policy."""
from pathlib import Path
import json, shutil
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
def run():
  source=(ROOT/'web'/'index.html').read_text(encoding='utf-8')
  checks={}
  with sync_playwright() as p:
    exe=shutil.which('chromium') or shutil.which('chromium-browser') or shutil.which('google-chrome')
    args={'headless':True,'args':['--no-sandbox']}
    if exe:args['executable_path']=exe
    browser=p.chromium.launch(**args)
    page=browser.new_page(viewport={'width':1280,'height':880},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
    page.set_content(source,wait_until='load')
    checks['heading']=page.get_by_text('从单一螺旋相位，到规范曲率').count()==1
    js=page.evaluate('window.__v106Data')
    checks['baseline_invariant']=abs(js['I']+40.55073873604525)<1e-7
    checks['scale12']=abs(js['pair12']['scale']/1.0265958696446e13-1)<1e-8
    checks['canvas_drawn']=page.locator('canvas#plot').count()==1
    page.locator('#as').fill('0.119')
    new=page.evaluate('window.__v106Data')
    checks['slider_changes_invariant']=abs(new['I']-js['I'])>.1
    page.locator('#s2').fill('0.232')
    checks['weak_slider_changes_output']=abs(page.evaluate('window.__v106Data.I')-new['I'])>.01
    page.locator('#reset').click()
    checks['reset_restores_baseline']=abs(page.evaluate('window.__v106Data.I')-js['I'])<1e-9
    checks['no_page_errors']=len(errors)==0
    checks['anomaly_table']=page.locator('#anomaly tr').count()==6
    (ROOT/'figures'/'03_CHROMIUM_ACTUAL_SCREENSHOT.png').parent.mkdir(exist_ok=True)
    page.screenshot(path=str(ROOT/'figures'/'03_CHROMIUM_ACTUAL_SCREENSHOT.png'),full_page=True)
    browser.close()
  result={'checks':checks,'errors':errors,'passed':sum(checks.values()),'total':len(checks)}
  (ROOT/'results'/'BROWSER_SMOKE.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
  if not all(checks.values()):raise AssertionError(result)
  print(result)
  return result
if __name__=='__main__':run()
