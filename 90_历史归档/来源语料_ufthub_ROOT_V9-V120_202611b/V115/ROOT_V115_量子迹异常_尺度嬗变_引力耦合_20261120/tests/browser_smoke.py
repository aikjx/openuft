"""Chromium E2E checks. Optional --capture replaces screenshot in current project."""
import asyncio,os,shutil,sys
from pathlib import Path

async def main():
    from playwright.async_api import async_playwright
    exe=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
    if not exe: print('No Chromium executable installed');return 2
    base=Path(__file__).resolve().parents[1];checks={}
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(executable_path=exe,headless=True,args=['--no-sandbox'])
        page=await browser.new_page(viewport={'width':1350,'height':900})
        await page.set_content((base/'web/index.html').read_text(encoding='utf-8'))
        checks['title']=(await page.title()).startswith('ROOT V115')
        checks['alpha_base']=(await page.locator('#alphaValue').inner_text())=='0.1180'
        checks['b0_base']=(await page.locator('#beta0').inner_text())=='7.666667'
        checks['lambda_base']=abs(float(await page.locator('#lam').inner_text())-.08782708)<1e-6
        checks['hierarchy_large']=float(await page.locator('#Gdiff').inner_text())>1e38
        await page.locator('#alpha').fill('0.14')
        checks['alpha_update']=(await page.locator('#alphaValue').inner_text())=='0.1400'
        await page.locator('#flavours').select_option('3')
        checks['nf_update']=(await page.locator('#beta0').inner_text())=='9.000000'
        await page.locator('#matchScale').uncheck()
        checks['vev_active']=await page.locator('#vev').is_enabled()
        await page.locator('#vev').fill('10')
        checks['vev_update']=abs(float((await page.locator('#vActual').inner_text()).replace(' GeV',''))-1e10)<1e6
        await page.locator('#zeta').fill('20')
        checks['zeta_update']=(await page.locator('#zetaValue').inner_text())=='20.0'
        checks['graph']=len(await page.locator('#line').get_attribute('d'))>500
        await page.locator('#reset').click()
        checks['reset']=(await page.locator('#alphaValue').inner_text())=='0.1180' and await page.locator('#vev').is_disabled()
        if '--capture' in sys.argv:
            await page.screenshot(path=str(base/'figures/06_actual_browser.png'),full_page=True)
        await browser.close()
    for k,v in checks.items():print(('PASS' if v else 'FAIL'),k)
    print(f'{sum(checks.values())}/{len(checks)} checks passed')
    return 0 if all(checks.values()) else 1

if __name__=='__main__':sys.exit(asyncio.run(main()))
