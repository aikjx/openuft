"""Optional actual Chromium verification of offline HTML UI."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main():
 checks={}
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1280,'height':950},device_scale_factor=1)
  errors=[]
  page.on('pageerror', lambda e:errors.append(str(e)))
  html=(ROOT/'web'/'index.html').read_text('utf-8')
  await page.set_content(html,wait_until='load')
  checks['heading']=await page.locator('h1').inner_text()=='ROOT V98｜三维非线性闭环科研实验室'
  checks['canvas']=await page.locator('#plot').count()==1
  checks['parameters']=await page.get_by_text('径向初始振幅').is_visible()
  checks['yaw_input']=await page.locator('#yaw').input_value()=='35'
  await page.locator('#yaw').fill('113')
  checks['yaw_updated']=await page.locator('#yaw').input_value()=='113'
  checks['boost_input']=await page.locator('#boost').input_value()=='50'
  await page.locator('#boost').fill('90')
  checks['boost_updated']=await page.locator('#boost').input_value()=='90'
  await page.locator('#toggle').click()
  checks['pause_label']=await page.locator('#toggle').inner_text()=='继续'
  await page.locator('#reset').click()
  checks['reset_yaw']=await page.locator('#yaw').input_value()=='35'
  checks['reset_boost']=await page.locator('#boost').input_value()=='50'
  checks['no_js_errors']=len(errors)==0
  await page.screenshot(path=str(ROOT/'plots'/'04_CHROMIUM_ACTUAL_SCREENSHOT.png'),full_page=True)
  await browser.close()
 result={'status':'PASS' if all(checks.values()) else 'FAIL','count':len(checks),'checks':checks,
         'JS_errors':errors,'method':'Chromium: embedded offline HTML with Playwright set_content'}
 (ROOT/'results'/'BROWSER_SMOKE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))
 if not all(checks.values()):raise SystemExit(1)
asyncio.run(main())
