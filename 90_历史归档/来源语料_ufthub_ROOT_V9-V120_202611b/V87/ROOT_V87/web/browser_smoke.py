"""UI regression; Chromium can render same HTML via set_content if file:// blocked.
No remote network access needed.
"""
from pathlib import Path
import asyncio,json,math
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent.parent

async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  page=await browser.new_page(viewport={'width':1365,'height':1000},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda ex:errors.append(str(ex)))
  content=(ROOT/'web'/'index.html').read_text(encoding='utf8')
  await page.set_content(content,wait_until='load');await page.wait_for_timeout(300)
  assert not errors,errors
  assert await page.title()=='ROOT V87 · 量子—牛顿—爱因斯坦衔接实验室'
  assert await page.locator('h1').count()==1
  assert await page.locator('[data-chart]').count()==3
  base_phase=float(await page.locator('#phase').inner_text())
  assert math.isclose(base_phase,-.9821125881956593,rel_tol=5e-5),base_phase
  g1=float(await page.locator('#gN').inner_text())
  await page.locator('#sourceMass').evaluate('(e)=>{e.value=200;e.dispatchEvent(new Event("input",{bubbles:true}))}')
  g2=float(await page.locator('#gN').inner_text())
  assert math.isclose(g2/g1,2,rel_tol=3e-5)
  phase2=float(await page.locator('#phase').inner_text())
  assert math.isclose(phase2/base_phase,2,rel_tol=3e-5)
  await page.locator('#sourceMass').evaluate('(e)=>{e.value=100;e.dispatchEvent(new Event("input",{bubbles:true}))}')
  await page.locator('#height').evaluate('(e)=>{e.value=.02;e.dispatchEvent(new Event("input",{bubbles:true}))}')
  shape=float(await page.locator('#shape').inner_text())
  assert math.isclose(shape,.3/.32,rel_tol=1e-6)
  await page.locator('#height').evaluate('(e)=>{e.value=.01;e.dispatchEvent(new Event("input",{bubbles:true}))}')
  await page.locator('#hold').evaluate('(e)=>{e.value=2;e.dispatchEvent(new Event("input",{bubbles:true}))}')
  assert math.isclose(float(await page.locator('#phase').inner_text())/base_phase,2,rel_tol=1e-5)
  await page.locator('#hold').evaluate('(e)=>{e.value=1;e.dispatchEvent(new Event("input",{bubbles:true}))}')
  await page.locator('#alpha').evaluate('(e)=>{e.value=0;e.dispatchEvent(new Event("input",{bubbles:true}))}')
  assert math.isclose(float(await page.locator('#Q').inner_text()),1,rel_tol=1e-10)
  await page.locator('#alpha').evaluate('(e)=>{e.value=.20;e.dispatchEvent(new Event("input",{bubbles:true}))}')
  assert float(await page.locator('#Q').inner_text())>1
  await page.locator('[data-chart="shape"]').click()
  assert 'Yukawa' in await page.locator('#chartCaption').inner_text()
  assert await page.locator('[data-chart="shape"]').get_attribute('aria-selected')=='true'
  await page.locator('[data-chart="sn"]').click()
  assert '高斯' in await page.locator('#chartCaption').inner_text()
  await page.locator('[data-chart="phase"]').click()
  assert '球外' in await page.locator('#chartCaption').inner_text()
  ck=float(await page.locator('#clock').inner_text())
  assert 1e-17<ck<1e-15
  assert await page.locator('#plot').evaluate('(e)=>e.width')==1030
  # Original defaults again for screenshot
  await page.screenshot(path=str(ROOT/'results'/'browser_chromium.png'),full_page=True)
  await browser.close()
  checks=[
   'HTML parsed and no JS exceptions','title','single h1','three interactive charts',
   'default phase reference','Newton inverse distance mass scaling','phase mass scaling',
   'finite height normalized geometry','hold time scaling','Yukawa alpha=0 -> Q=1',
   'Yukawa alpha positive -> Q>1','shape tab updates','selected ARIA state',
   'Gaussian toy chart tab','phase chart restore','clock redshift SI value',
   'canvas width','actual screenshot written']
  report={'checks':len(checks),'passed':len(checks),'names':checks,'render_strategy':'Chromium set_content of exact HTML source','not_hardware_test':True}
  (ROOT/'results'/'browser_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
  print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':asyncio.run(main())
