"""Offline Chromium smoke test. WebGL/production deployment not claimed."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright

BASE=Path(__file__).resolve().parents[1]

async def run():
    errors=[];checks=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
        page=await browser.new_page(viewport={'width':1366,'height':930},device_scale_factor=1)
        page.on('pageerror',lambda e: errors.append(str(e)))
        await page.set_content((BASE/'web'/'index.html').read_text(encoding='utf-8'),wait_until='load')
        await page.wait_for_timeout(300)
        checks.append(('title', 'V80' in await page.title()))
        checks.append(('body_visible',await page.locator('h1').is_visible()))
        initial=await page.locator('#metric_g').inner_text()
        checks.append(('earth_g_text',initial != '—' and ('9.820' in initial or '9.82' in initial)))
        await page.select_option('#star','12')
        after=await page.locator('#metric_g').inner_text()
        checks.append(('star_switch',after!=initial and 'e+' in after))
        Bval=await page.locator('#metric_q').inner_text()
        checks.append(('magnetar_qed',float(Bval.replace('e+','e'))>1))
        await page.locator('#beta').fill('3')
        checks.append(('beta_changes',await page.locator('#deltag').inner_text()!='—'))
        await page.locator('#bexp').fill('10.5')
        checks.append(('magnetic_slider',float((await page.locator('#metric_q').inner_text()).replace('e+','e'))>2))
        await page.locator('#az').fill('83')
        checks.append(('orientation','83°' in await page.locator('#azvalue').inner_text()))
        checks.append(('canvases',await page.locator('canvas').count()==2))
        await page.screenshot(path=str(BASE/'results'/'browser_smoke.png'),full_page=True)
        checks.append(('no_js_errors',len(errors)==0))
        await browser.close()
    result={'checks':len(checks),'passed':sum(ok for _,ok in checks),'details':checks,'pageerrors':errors,'render_mode':'Canvas2D / static local file','browser':'Chromium headless'}
    (BASE/'results'/'browser_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    for name,ok in checks:print(('PASS' if ok else 'FAIL'),name)
    if any(not ok for _,ok in checks) or errors: raise RuntimeError('Browser checks failed')

if __name__=='__main__':asyncio.run(run())
