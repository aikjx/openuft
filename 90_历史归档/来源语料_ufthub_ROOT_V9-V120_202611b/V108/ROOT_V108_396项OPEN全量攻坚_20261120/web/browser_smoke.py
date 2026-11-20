"""Actual Chromium interaction smoke, optional dependency playwright+chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright
here=Path(__file__).resolve().parent
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1280,'height':850})
    page.set_content((here/'index.html').read_text(encoding='utf-8'),wait_until='load')  # same offline HTML, avoids file:// administrator policy
    assert page.locator('#entry-count').inner_text().strip()=='396'
    assert page.locator('#issues tbody tr').count()>=1
    page.locator('#search').fill('U107-11')
    assert page.locator('#shown-count').inner_text().strip()=='1'
    page.locator('#search').fill('')
    page.locator('#status').select_option('GOAL_OPEN')
    assert int(page.locator('#shown-count').inner_text())>=100
    page.locator('#status').select_option('all')
    page.locator('#radius').fill('100')
    page.locator('#radius').dispatch_event('input')
    assert float(page.locator('#qval').inner_text().split('=')[-1].strip())>0
    page.locator('#masslog').fill('16')
    page.locator('#masslog').dispatch_event('input')
    assert float(page.locator('#lifetime').get_attribute('data-years'))>1e34
    page.screenshot(path=str(here.parent/'figures'/'04_ACTUAL_CHROMIUM_SMOKE.png'),full_page=True)
    browser.close()
print('PASS: chromium 8 checks; actual screenshot figures/04_ACTUAL_CHROMIUM_SMOKE.png')
