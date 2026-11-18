"""Chromium smoke checks. Load local HTML via set_content because sandbox blocks file:// navigation."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
html=(root/'web'/'index.html').read_text(encoding='utf-8')
report={'checks':[],'errors':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-gpu'])
 page=browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
 page.on('pageerror',lambda err:report['errors'].append(str(err)))
 page.set_content(html,wait_until='load',timeout=20000)
 def check(label,good):
  report['checks'].append({'label':label,'pass':bool(good)})
  if not good:raise AssertionError(label)
 check('页面标题', 'ROOT V73' in page.title())
 check('尺度初始值',page.locator('#rgLambda').inner_text()!='')
 a=page.locator('#rgLambda').inner_text()
 page.locator('#rgG').evaluate('(el)=>{el.value="0.600";el.dispatchEvent(new Event("input",{bubbles:true}))}')
 check('耦合参数影响尺度',page.locator('#rgLambda').inner_text()!=a)
 page.get_by_role('tab',name='星体有限尺寸').click()
 check('源模型显示',page.locator('#sphere').get_attribute('class')=='panel active')
 point0=page.locator('#yPoint').inner_text()
 page.locator('#logRange').evaluate('(el)=>{el.value="7";el.dispatchEvent(new Event("input",{bubbles:true}))}')
 check('作用距离影响点源',page.locator('#yPoint').inner_text()!=point0)
 check('均匀球曲线画布',page.locator('#sphereCanvas').evaluate('(el)=>el.width>100'))
 page.get_by_role('tab',name='八态三重反转').click()
 check('八状态行数',page.locator('#tripleRows tr').count()==8)
 check('β+γ初始值',abs(float(page.locator('#tripleEst').inner_text())-0.65)<1e-9)
 page.locator('#artifact').evaluate('(el)=>{el.value="0.35";el.dispatchEvent(new Event("input",{bubbles:true}))}')
 check('同形伪差影响测量',abs(float(page.locator('#tripleEst').inner_text())-.75)<1e-9)
 page.get_by_role('tab',name='统一证明检查').click()
 check('证明边界显示',page.get_by_text('尚未完成').count()>0)
 check('无JS错误',len(report['errors'])==0)
 page.get_by_role('tab',name='尺度如何生成').click()
 page.screenshot(path=str(root/'results'/'browser_real.png'),full_page=True)
 browser.close()
(root/'results'/'browser_smoke.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Browser checks:',len(report['checks']), 'passed:',sum(x['pass'] for x in report['checks']), 'errors:',report['errors'])
