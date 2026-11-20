"""Optional actual Chromium UI smoke verification via Playwright, no server/internet."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def main():
 from playwright.sync_api import sync_playwright
 html=(ROOT/'web'/'index.html').read_text(encoding='utf-8')
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1300,'height':900}, device_scale_factor=1)
  page.set_content(html,wait_until='load');page.wait_for_timeout(250)
  start=page.evaluate('window.__v92State')
  page.screenshot(path=str(ROOT/'figures'/'offline_physical_chromium_screenshot.png'),full_page=True)
  assert start['mode']=='physical' and start['beta']==0.8 and start['B']==0.5,start
  assert start['closureError']<1e-12,start
  page.locator('#B').fill('0.7');page.locator('#B').dispatch_event('input')
  changed=page.evaluate('window.__v92State')
  assert changed['B']==0.7 and changed['omega']>start['omega']
  page.locator('#luminal').click()
  lum=page.evaluate('window.__v92State')
  assert lum['mode']=='luminal' and abs(lum['speed']/299792458-1)<1e-12 and lum['closureError']<1e-12
  assert page.locator('#force').inner_text()=='不适用'
  page.screenshot(path=str(ROOT/'figures'/'offline_interactive_chromium_screenshot.png'),full_page=True)
  page.locator('#physical').click()
  back=page.evaluate('window.__v92State')
  assert back['mode']=='physical'
  browser.close()
 result={'status':'PASS','checks':['offline HTML content loaded (browser policy blocks file:// scheme)','magnetic model default','B slider changes cyclotron frequency','luminal mode exactly c','luminal mode no finite massive force','switching back','closure both modes'], 'theoretical_only':True}
 (ROOT/'results'/'BROWSER_SMOKE_REPORT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
