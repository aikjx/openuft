from pathlib import Path
import json,asyncio
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
async def main():
  checks={}
  async with async_playwright() as p:
    browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=await browser.new_page(viewport={'width':1280,'height':950},device_scale_factor=1)
    html=(ROOT/'web'/'index.html').read_text(encoding='utf-8')
    await page.set_content(html,wait_until='load')
    checks['title']=await page.locator('h1').inner_text()=='ROOT V97 · 非线性内外螺旋闭环实验室'
    checks['radius_label']=await page.get_by_text('闭环参考半径').is_visible()
    checks['canvas_exists']=await page.locator('canvas').count()==1
    checks['initial_frame']=await page.locator('#timeIndex').input_value()=='0'
    await page.locator('#timeIndex').fill('660')
    checks['slider_moves']=await page.locator('#timeIndex').input_value()=='660'
    checks['info_updates']='t=' in await page.locator('#frameinfo').inner_text()
    await page.locator('#play').click()
    checks['play_changes_label']=await page.locator('#play').inner_text()=='暂停'
    await page.locator('#play').click()
    await page.locator('#reset').click()
    checks['reset']=await page.locator('#timeIndex').input_value()=='0'
    await page.screenshot(path=str(ROOT/'plots'/'04_CHROMIUM_ACTUAL_SCREENSHOT.png'),full_page=True)
    await browser.close()
  result={'success':all(checks.values()),'checks':checks,'count':len(checks),'browser':'Chromium headless, same embedded HTML loaded with set_content'}
  (ROOT/'results'/'BROWSER_SMOKE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
  print(json.dumps(result,ensure_ascii=False,indent=2))
  if not result['success']: raise SystemExit(1)
asyncio.run(main())
