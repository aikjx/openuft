"""Optional UI checks. Only --capture replaces the reference screenshot."""
import asyncio,shutil,os,sys
from pathlib import Path
async def main():
    from playwright.async_api import async_playwright
    root=Path(__file__).resolve().parents[1]
    chromium=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
    if not chromium:
        print('SKIP: No installed Chromium found');return 2
    tests={}
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(executable_path=chromium,headless=True,args=['--no-sandbox'])
        page=await browser.new_page(viewport={'width':1270,'height':860})
        await page.set_content((root/'web/index.html').read_text(encoding='utf-8'))
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        tests['title']=(await page.title()).startswith('ROOT V113')
        tests['gamma_baseline']=(await page.locator('#gammaValue').inner_text())=='0.500000000'
        tests['baseline_excluded']='冲突' in await page.locator('#status').inner_text()
        await page.locator('#w').fill('5')
        tests['higher_omega_gamma_near_one']=float(await page.locator('#gammaValue').inner_text())>.99998
        await page.locator('#mass').fill('-13')
        tests['massive_gamma_near_one']=float(await page.locator('#massGamma').inner_text())>.99999999
        await page.locator('#mass').fill('-22')  # Restore long-range signal for nonzero-eta test
        await page.locator('#delta').fill('-9')
        tests['eta_nonzero']=abs(float(await page.locator('#etaValue').inner_text()))>0
        await page.locator('#r2').fill('1')
        tests['equal_radius_det_zero']=abs(float(await page.locator('#detValue').inner_text()))<1e-13
        await page.locator('#r2').fill('2')
        tests['different_radius_det_nonzero']=abs(float(await page.locator('#detValue').inner_text()))>1e-3
        tests['chart_active']=len(await page.locator('#curve').get_attribute('d'))>2000
        await page.locator('#reset').click()
        tests['reset']=(await page.locator('#gammaValue').inner_text())=='0.500000000'
        tests['javascript_error_free']=not errors
        if '--capture' in sys.argv:
            await page.screenshot(path=str(root/'figures/05_actual_browser.png'),full_page=True)
        await browser.close()
    for k,ok in tests.items():print(('PASS' if ok else 'FAIL'),k)
    print(sum(tests.values()),'/',len(tests),'browser checks passed')
    return 0 if all(tests.values()) else 1
if __name__=='__main__':sys.exit(asyncio.run(main()))
