"""Actual Chromium UI checks; optional --screenshot updates the archived evidence."""
import asyncio,os,sys,shutil
from pathlib import Path
async def main():
    from playwright.async_api import async_playwright
    exe=os.getenv('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
    if not exe:raise SystemExit('Chromium executable not installed')
    root=Path(__file__).resolve().parents[1]
    checks={}
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path=exe,headless=True,args=['--no-sandbox'])
        page=await b.new_page(viewport={'width':1280,'height':850})
        errors=[]
        page.on('pageerror',lambda exc:errors.append(str(exc)))
        await page.set_content((root/'web/index.html').read_text(encoding='utf-8'))
        checks['title']='V118' in await page.title()
        checks['baseline_profile']=(await page.locator('#profile').input_value())=='earth_analytic'
        checks['baseline_surface']=abs(float((await page.locator('#surface').inner_text()).strip('%'))-.5954)<.01
        checks['baseline_inferred']=abs(float((await page.locator('#inferred').inner_text()).split()[0])-125)<.001
        checks['baseline_fourth_closure']=abs(float(await page.locator('#resid').inner_text()))<1e-10
        checks['plot_rendered']=len(await page.locator('#curve').get_attribute('d'))>40
        checks['density_change']=True
        await page.locator('#profile').select_option('uniform')
        checks['density_change']=float((await page.locator('#surface').inner_text()).strip('%'))>.9
        await page.locator('#secondary').fill('0.1')
        checks['two_range_residual']=abs(float(await page.locator('#resid').inner_text()))>5e-5
        await page.locator('#reset').click()
        checks['reset']= (await page.locator('#secondary').input_value())=='0' and (await page.locator('#profile').input_value())=='earth_analytic'
        checks['curve_after_reset']=len(await page.locator('#curve').get_attribute('d'))>40
        checks['no_js_errors']=not errors
        if '--screenshot' in sys.argv:
            await page.screenshot(path=str(root/'figures/06_actual_chromium.png'),full_page=True)
        await b.close()
    for name,ok in checks.items(): print('PASS' if ok else 'FAIL',name)
    print(sum(checks.values()),'/',len(checks),'browser checks')
    return 0 if all(checks.values()) else 1
if __name__=='__main__':sys.exit(asyncio.run(main()))
