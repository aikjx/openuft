"""Browser smoke test; may use set_content if sandbox disallows file://."""
import json,asyncio
from pathlib import Path
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1]
async def main():
    report={'version':'ROOT V84','browser':'Chromium','checks':[],'errors':[],'render_mode':None}
    def ok(label,condition):
        report['checks'].append({'check':label,'pass':bool(condition)})
        if not condition:raise AssertionError(label)
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
        page=await browser.new_page(viewport={'width':1440,'height':950},device_scale_factor=1)
        page.on('pageerror',lambda e:report['errors'].append(str(e)))
        html=(R/'web'/'index.html').read_text(encoding='utf8')
        # Some isolated test environments block file:// navigation; load exact HTML as-is.
        # This validates the interactive page but not local file-URL permissions.
        await page.set_content(html,wait_until='domcontentloaded',timeout=30000)
        report['render_mode']='set_content_identical_html'
        await page.wait_for_timeout(300)
        ok('title',await page.title()=='ROOT V84｜多距离引力实验')
        ok('H1',await page.locator('h1').count()==1)
        ok('synthetic prominent', '合成' in (await page.locator('header').inner_text()))
        ok('control sliders',await page.locator('input[type="range"]').count()==6)
        ok('canvas count',await page.locator('canvas').count()==2)
        ok('initial Newton result', 'nm/s²' in (await page.locator('#nstat').inner_text()))
        ok('initial gradient', 's⁻²' in (await page.locator('#gstat').inner_text()))
        a=await page.locator('#nstat').inner_text()
        await page.locator('#mass').evaluate('(el)=>{el.value="150";el.dispatchEvent(new Event("input",{bubbles:true}))}')
        b=await page.locator('#nstat').inner_text()
        ok('mass input updates Newton',a!=b)
        await page.locator('#distance').evaluate('(el)=>{el.value="0.80";el.dispatchEvent(new Event("input",{bubbles:true}))}')
        c=await page.locator('#nstat').inner_text()
        ok('distance input updates Newton',b!=c)
        await page.locator('#range').evaluate('(el)=>{el.value="0.75";el.dispatchEvent(new Event("input",{bubbles:true}))}')
        ok('range updates label','0.75 m' in (await page.locator('#valL').inner_text()))
        await page.locator('#alpha').evaluate('(el)=>{el.value="0.15";el.dispatchEvent(new Event("input",{bubbles:true}))}')
        ok('alpha update','0.150' in (await page.locator('#valAl').inner_text()))
        await page.locator('[data-scenario="INJECTED"]').click()
        ok('injected scenario selects',await page.locator('[data-scenario="INJECTED"]').get_attribute('class')=='selected')
        ok('injected text','注入' in (await page.locator('#explanation').inner_text()))
        await page.locator('[data-scenario="CONFOUNDED"]').click()
        ok('confound text','伪差' in (await page.locator('#explanation').inner_text()))
        ok('confound fit nonzero',float((await page.locator('#fitAlpha').inner_text()).split('±')[0].strip())>.03)
        await page.locator('[data-scenario="NULL"]').click()
        ok('null fit near zero',abs(float((await page.locator('#fitAlpha').inner_text()).split('±')[0].strip()))<.03)
        await page.locator('#distance').evaluate('(el)=>{el.value="0.28";el.dispatchEvent(new Event("input",{bubbles:true}))}')
        await page.locator('#radius').evaluate('(el)=>{el.value="0.15";el.dispatchEvent(new Event("input",{bubbles:true}))}')
        await page.locator('#baseline').evaluate('(el)=>{el.value="0.15";el.dispatchEvent(new Event("input",{bubbles:true}))}')
        ok('geometry invalid warning',await page.locator('#error').is_visible())
        await page.locator('#distance').evaluate('(el)=>{el.value="0.70";el.dispatchEvent(new Event("input",{bubbles:true}))}')
        ok('geometry warning clears',not await page.locator('#error').is_visible())
        await page.screenshot(path=str(R/'results'/'browser_actual.png'),full_page=True)
        ok('no Javascript exception',len(report['errors'])==0)
        ok('screenshot generated',(R/'results'/'browser_actual.png').stat().st_size>2000)
        await browser.close()
    report['check_count']=len(report['checks']);report['passed']=all(x['pass'] for x in report['checks'])
    (R/'results'/'browser_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':asyncio.run(main())
