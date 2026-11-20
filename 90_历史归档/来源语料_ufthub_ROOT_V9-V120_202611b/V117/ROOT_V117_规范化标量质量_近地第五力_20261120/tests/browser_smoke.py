"""Optional Chrome/Chromium Playwright validation. Never writes screenshot by default."""
import asyncio,sys,shutil,os
from pathlib import Path
async def run():
    try:from playwright.async_api import async_playwright
    except ImportError:
        print('SKIP: pip install playwright');return 2
    browser_path=os.getenv('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
    if not browser_path:
        print('SKIP: Chromium not installed');return 2
    root=Path(__file__).resolve().parents[1]
    checks={}
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(headless=True,executable_path=browser_path,args=['--no-sandbox'])
        page=await browser.new_page(viewport={'width':1280,'height':840})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        await page.set_content((root/'web/index.html').read_text(encoding='utf-8'))
        checks['page_title']='V117' in await page.title()
        checks['baseline_lambda']=(await page.locator('#lamlabel').inner_text())=='1'
        checks['baseline_range']=abs(float(await page.locator('#range').inner_text())-124.59948)<.003
        checks['default_positive']=float(await page.locator('#excess').inner_text())>.009
        await page.locator('#loglam').fill('1')
        checks['mass_varies']=float((await page.locator('#mass').inner_text()).replace('E','e'))>1e-12
        checks['range_decreases']=float(await page.locator('#range').inner_text())<50
        await page.locator('#height').fill('500')
        checks['altitude_applied']=(await page.locator('#hlabel').inner_text())=='500 km'
        await page.locator('#profile').select_option('inverse_r')
        checks['profile_applied']=float(await page.locator('#excess').inner_text())>0
        checks['plot_rendered']=len(await page.locator('#uplot').get_attribute('d'))>1000
        await page.locator('#reset').click()
        checks['reset_success']=(await page.locator('#lamlabel').inner_text())=='1' and (await page.locator('#hlabel').inner_text())=='0 km'
        checks['no_javascript_error']=not errors
        if '--capture' in sys.argv:
            await page.screenshot(path=str(root/'figures/05_actual_chromium.png'),full_page=True)
        await browser.close()
    for k,v in checks.items():print(('PASS' if v else 'FAIL'),k)
    print(f'{sum(checks.values())}/{len(checks)} Chromium tests')
    return 0 if all(checks.values()) else 1
if __name__=='__main__':sys.exit(asyncio.run(run()))
