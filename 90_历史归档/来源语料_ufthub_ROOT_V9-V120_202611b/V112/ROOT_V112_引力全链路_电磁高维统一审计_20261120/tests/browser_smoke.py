"""Optional Chromium E2E. Run: python tests/browser_smoke.py
Requires playwright Python package and a Chromium executable. CHROMIUM_PATH overrides discovery.
Does not overwrite the archived screenshot unless --capture is supplied.
"""
import asyncio,os,sys,shutil
from pathlib import Path

async def main():
    try: from playwright.async_api import async_playwright
    except ImportError:
        print("SKIP: install playwright (optional browser validation)");return 2
    browser_path=os.environ.get("CHROMIUM_PATH") or shutil.which("chromium") or shutil.which("google-chrome")
    if not browser_path: print("SKIP: Chromium not found");return 2
    root=Path(__file__).resolve().parents[1]
    expected={}
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path=browser_path,headless=True,args=["--no-sandbox"])
        p=await b.new_page(viewport={"width":1280,"height":850})
        await p.set_content((root/"web/index.html").read_text(encoding="utf-8"))
        expected["title"]=(await p.title()).startswith("ROOT V112")
        expected["baseline"]=(await p.locator("#xiLabel").inner_text())=="0.60"
        expected["horizon"]="有经典" in await p.locator("#status").inner_text()
        await p.locator("#charge").fill("1.2")
        expected["superextremal"]="无经典" in await p.locator("#status").inner_text()
        expected["no_root"]=(await p.locator("#rplus").inner_text())=="无"
        await p.locator("#field").fill("0")
        expected["kk_zero"]="相容" in await p.locator("#kkstatus").inner_text()
        await p.locator("#reset").click()
        expected["reset"]=(await p.locator("#xiLabel").inner_text())=="0.60"
        expected["plot"]=len(await p.locator("#curve").get_attribute("d"))>1000
        if "--capture" in sys.argv:
            await p.screenshot(path=str(root/"figures/04_actual_browser.png"),full_page=True)
        await b.close()
    for k,v in expected.items():print(("PASS" if v else "FAIL"),k)
    print(f"{sum(expected.values())}/{len(expected)} browser checks")
    return 0 if all(expected.values()) else 1
if __name__=="__main__":sys.exit(asyncio.run(main()))
