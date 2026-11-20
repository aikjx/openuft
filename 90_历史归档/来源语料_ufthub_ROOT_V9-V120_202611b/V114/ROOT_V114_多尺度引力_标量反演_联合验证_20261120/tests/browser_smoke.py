"""Chromium smoke test of offline ROOT V114 browser (no network).

Optional: pip install playwright, install system chromium, run python tests/browser_smoke.py
"""
from pathlib import Path
import asyncio,sys,shutil,os

async def main():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print('SKIP: Playwright not installed');return 2
    chrome=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
    if not chrome:
        print('SKIP: Chromium not found');return 2
    root=Path(__file__).resolve().parents[1]
    checks={}
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(executable_path=chrome,headless=True,args=['--no-sandbox'])
        page=await browser.new_page(viewport={'width':1280,'height':900},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        await page.set_content((root/'web/index.html').read_text(encoding='utf-8'))
        checks['title']=(await page.title()).startswith('ROOT V114')
        checks['gamma_baseline']=abs(float(await page.locator('#gamma').inner_text())-.781536)<1e-5
        checks['force_baseline']=abs(float(await page.locator('#force').inner_text())-1.24525296)<1e-5
        checks['different_gamma_fits']=abs(float(await page.locator('#gamma').inner_text())-float(await page.locator('#gamfit').inner_text()))>.1
        checks['inverse_baseline']=abs(float(await page.locator('#infer').inner_text())-1)<2e-5
        checks['plot_curves']=all([len(await page.locator(f'#{x}').get_attribute('d'))>1500 for x in ['lineGamma','lineForce','linePotential']])
        await page.locator('#lambda').fill('2')
        checks['lambda_updates']=abs(float(await page.locator('#infer').inner_text())-2)<1e-4
        await page.locator('#r').fill('2')
        checks['radius_updates']=abs(float(await page.locator('#rout').inner_text())-2)<1e-6
        await page.locator('#a').fill('0.5')
        checks['coupling_updates']=abs(float(await page.locator('#aout').inner_text())-.5)<1e-6
        await page.locator('#reset').click()
        checks['reset']=abs(float(await page.locator('#infer').inner_text())-1)<2e-5
        checks['no_script_errors']=not errors
        if '--capture' in sys.argv:
            await page.screenshot(path=str(root/'figures/06_actual_browser.png'),full_page=True)
        await browser.close()
    for name,ok in checks.items(): print(('PASS' if ok else 'FAIL'),name)
    print(f'{sum(checks.values())}/{len(checks)} browser checks passed')
    return 0 if all(checks.values()) else 1

if __name__=='__main__':sys.exit(asyncio.run(main()))
