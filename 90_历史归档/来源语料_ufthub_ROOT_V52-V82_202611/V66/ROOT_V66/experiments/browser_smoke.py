"""Optional real Chromium smoke. No remote network; avoids claiming WebGL."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('SKIP: optional playwright absent'); return
    errors=[]; report={}
    with sync_playwright() as p:
        try:
            browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
        except Exception as ex:
            print('SKIP: chromium unavailable: ',str(ex)[:150]);return
        page=browser.new_page(viewport={'width':1280,'height':850},device_scale_factor=1)
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.set_content((ROOT/'web'/'index.html').read_text(encoding='utf-8'))
        page.locator('#angle').evaluate('(el)=>{el.value="42";el.dispatchEvent(new Event("input",{bubbles:true}))}')
        report['angle_changed']=page.locator('#angleOut').inner_text()
        assert report['angle_changed']=='42°'
        page.screenshot(path=str(ROOT/'results'/'browser_helix.png'),full_page=True)
        page.locator('[data-tab="earth"]').click()
        page.locator('#alt').evaluate('(el)=>{el.value="400";el.dispatchEvent(new Event("input",{bubbles:true}))}')
        report['alt_changed']=page.locator('#altOut').inner_text()
        assert report['alt_changed']=='400 km'
        page.screenshot(path=str(ROOT/'results'/'browser_earth.png'),full_page=True)
        page.locator('[data-tab="induction"]').click()
        page.locator('#mu').evaluate('(el)=>{el.value="1.5";el.dispatchEvent(new Event("input",{bubbles:true}))}')
        report['mu_changed']=page.locator('#muOut').inner_text()
        assert report['mu_changed']=='1.50'
        page.locator('[data-tab="fifth"]').click()
        report['fifth_force_out']=page.locator('#etaOut').inner_text()
        page.locator('[data-tab="audit"]').click()
        report['audit_visible']=page.get_by_text('从微观模态独立求 G').is_visible()
        assert report['audit_visible']
        report['page_errors']=errors
        assert not errors,errors
        (ROOT/'results'/'browser_smoke.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        browser.close()
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
