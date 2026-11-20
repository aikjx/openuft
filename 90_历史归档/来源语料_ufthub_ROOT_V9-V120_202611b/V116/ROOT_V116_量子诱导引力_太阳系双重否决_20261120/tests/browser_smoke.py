"""Optional real Chromium smoke test: python tests/browser_smoke.py"""
import asyncio, os, shutil, sys
from pathlib import Path
async def main():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print('SKIP: playwright not installed');return 2
    browser_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome')
    if not browser_path: print('SKIP: Chromium not installed');return 2
    root=Path(__file__).resolve().parents[1]
    checks={}
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(executable_path=browser_path,args=['--no-sandbox'],headless=True)
        page=await browser.new_page(viewport={'width':1280,'height':900})
        await page.set_content((root/'web/index.html').read_text(encoding='utf-8'))
        checks['title']=(await page.title()).startswith('ROOT V116')
        checks['default_Xi']=(await page.locator('#xiLog').inner_text())=='0.0'
        checks['default_exclusion']='不相容' in await page.locator('#status').inner_text()
        checks['PPN_half']=(await page.locator('#gamma').inner_text()).startswith('5.555556e-1')
        await page.locator('#xi').fill('-7')
        checks['low_Xi_allowed']='相容' in await page.locator('#status').inner_text()
        await page.locator('#dist').fill('1')
        checks['changing_range']=(await page.locator('#distLog').inner_text())=='1.0'
        checks['plot']=(len(await page.locator('#curve').get_attribute('d'))>1000)
        await page.locator('#reset').click()
        checks['reset']=(await page.locator('#xiLog').inner_text())=='0.0'
        checks['gamma_fit_visible']=len(await page.locator('#gfit').inner_text())>4
        await page.screenshot(path=str(root/'figures/05_chromium_actual.png'),full_page=True)
        await browser.close()
    for name,ok in checks.items():print('PASS' if ok else 'FAIL',name)
    print(sum(checks.values()),'/',len(checks),'browser checks')
    return 0 if all(checks.values()) else 1
if __name__=='__main__':sys.exit(asyncio.run(main()))
