"""Optional browser smoke test; requires playwright and Chromium.
It loads the standalone HTML into the browser document (set_content), to
work in sandboxed environments where file:// and localhost are prohibited.
It verifies live controls and reports WebGL2 capability (does not fake it).
"""
from __future__ import annotations
from pathlib import Path
import json, sys, datetime
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'web/index.html').read_text(encoding='utf-8')
OUT=ROOT/'results/browser_test_report.json'

def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        print('SKIP browser test: playwright not installed')
        return 2
    with sync_playwright() as p:
        exe='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None
        browser=p.chromium.launch(executable_path=exe,headless=True,
                                  args=['--no-sandbox','--disable-dev-shm-usage'])
        try:
            page=browser.new_page(viewport={'width':1280,'height':850})
            errors=[]
            page.on('pageerror',lambda err:errors.append(str(err)))
            page.set_content(HTML,wait_until='load')
            page.wait_for_timeout(200)
            webgl=page.evaluate("!!document.getElementById('globe').getContext('webgl2')")
            g=float(page.locator('#gRatio').inner_text())
            assert 37.69<g<37.71
            page.locator('#btnHelix').click()
            page.locator('#angle').fill('60')
            page.wait_for_timeout(150)
            a=page.locator('#aTxt').inner_text()
            vphi=float(page.locator('#vp').inner_text())
            assert a=='60°'
            assert abs(vphi-0.5)<1e-6
            page.locator('#btnEarth').click()
            page.locator('#N').fill('4')
            page.wait_for_timeout(150)
            g4=float(page.locator('#gRatio').inner_text())
            assert abs(g4-37.699111843/4)<0.0005
            assert not errors,errors
            report={'browser_engine':'Chromium','source_mode':'set_content, no navigation',
                    'webgl2_enabled_in_test_environment':webgl,
                    'canvas2d_fallback_used':not webgl,
                    'html_controls_verified':True,
                    'interactions':['earth/helix button','angle slider 60 degrees',
                                    'field N slider 4','G ratio changes'],
                    'page_javascript_errors':errors,
                    'webgl_gpu_rendering_verified':webgl,
                    'interpretation':'Interaction smoke test; not scientific empirical validation'}
            OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
            print(json.dumps(report,ensure_ascii=False,indent=2))
        finally:
            browser.close()
    return 0

if __name__=='__main__':sys.exit(main())
