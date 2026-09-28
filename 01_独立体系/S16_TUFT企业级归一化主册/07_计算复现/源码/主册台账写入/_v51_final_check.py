# -*- coding: utf-8 -*-
import io, json

base = r'D:\a10\aikjx\code\my_lib'
master = io.open(base + r'\TUFT_企业级归一化主册_v1.0.md', encoding='utf-8').read()
led = json.load(io.open(base + r'\TUFT_归一化台账_v1.0.json', encoding='utf-8'))
ch66 = io.open(base + r'\openuft\书籍\v1_正文\第十二编_动力学本征值路线_解锁UFT-3的真实尝试\第66章_复谱GradeA_TUFT基频极点与两路互证.md', encoding='utf-8').read()
chled = io.open(base + r'\openuft\书籍\v1_正文\第十二编_动力学本征值路线_解锁UFT-3的真实尝试\_章节账本.md', encoding='utf-8').read()
html = io.open(base + r'\TUFT_全物理现象关系流程图.html', encoding='utf-8').read()
report = io.open(base + r'\TUFT_v51_鲁棒两域合并报告.md', encoding='utf-8').read()

checks = []
def ck(name, cond): checks.append((name, bool(cond)))

ck('master v6.3 title', master.startswith('# TUFT 企业级归一化主册 v6.3'))
ck('master has v6.3 block', '> **★★ v6.3（v51 鲁棒两域单元轮收口' in master)
ck('master has E501', 'E501' in master)
ck('master v6.2 block not rolled back', 'v6.2 Grade-A 静态攻坚' in master)
ck('master v6.1 block retained', '> **★★ v6.1（v49 Chandrasekhar' in master)
ck('master erratum #42 held', '勘误 #42 held' in master)
ck('master four-state frozen', '35/61/18/27 冻结' in master)

ck('json version v6.3', led['version']=='v6.3')
ck('json latest_round', led['latest_round']=='v6.3_v51_twodomain')
ck('json equation_range', led['equation_range']=='E1-E501')
ck('json erratum 42', led['latest_erratum']==42 and led['erratum']==42)
ck('json four-state 35/61/18/27', led['four_state_counts_approx']['strict']==35 and led['four_state_counts_approx']['conditional']==61 and led['four_state_counts_approx']['definition']==18 and led['four_state_counts_approx']['open']==27)
ck('json v51 key results', 'v51_twodomain_key_results' in led)
ck('json backlog[0] v6.3', led['open_backlog'][0].startswith('v6.3/v51'))

ck('ch66 has 66.14', '## 66.14 v51 鲁棒两域单元' in ch66)
ck('ch66 len 26671', len(ch66)==26671)
ck('ch66 66.13 retained', '### 66.13.7' in ch66)
ck('ch66 E501', 'E501' in ch66)

ck('chledger 26671', '26671（len 实测）' in chled)
ck('chledger 66.14 in table', '66.12/66.13/66.14' in chled)
ck('chledger total 109928', '109928 字符' in chled)
ck('chledger v51 note', 'v51 append（2026-09-25）' in chled)

ck('html v6.3 subtitle', 'SSOT v6.3 / E1–E501' in html)
ck('html v51 block', 'v51 Q1 界面奇异工程修复 PASS' in html)
ck('html div balanced', html.count('<div')==html.count('</div>'))

ck('report exists & has sections', all(x in report for x in ['两域求导链','Q1 界面奇异根因与修复','GR 门','收敛扫描','卡点','未决项','勘误','文件清单']))

bad = [n for n,c in checks if not c]
for n,c in checks: print(('PASS' if c else 'FAIL'), n)
print('\n==== RESULT:', 'ALL PASS' if not bad else 'FAIL: '+str(bad), '====')
