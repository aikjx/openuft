# -*- coding: utf-8 -*-
"""一次性脚本：把 r437 登记进 README 的源码树与判定树（r436 之后）。"""
import io, shutil
BASE = r'd:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化'
P = BASE + '/README.md'
BAK = BASE + '/_bak_README_pre_r437.md'
NAME = 'TUFT-r437_E2修法后果与分类学开放性定理_实证完备非逻辑完备与出口闭合性再审计_精算_2026-11-21'
with io.open(P, encoding='utf-8', newline='') as f:
    txt = f.read()
assert 'r437' not in txt
py_line = (
    '│   ├── ' + NAME + '.py  '
    '# 新增（**r437 · 2026-11-21**）：**接手 r436 §十裁决 1 BOUNDARY「E2 修法 + 名单不代填」'
    '——E2 修法后果与分类学开放性定理**（条目 8：PASS 2 / FAIL 4 / BOUNDARY 1 / INFO 1；'
    '守卫 13/13；控制组 2/2；退出码 0；判词 `E2-REPAIR-EMPIRICAL-ONLY--CLASSIFICATION-LOGICALLY-OPEN--'
    'KNOWN-COUNTEREXAMPLE-REMOVED--STRUCTURAL-CLOSURE-NOT-ACHIEVED--LIST-NOT-FILLABLE-BY-INDUCTION--'
    'UNIQUE-EXIT-9FOLD-REAFFIRMED`）：'
    '① 分类完备性两分 —— 实证完备=已知样本全落入(r429 七类 7/7)，逻辑完备=存在穷尽证明；'
    '机器检索 r429 判定册穷尽证明标记命中 0 ⇒ 实证完备、非逻辑完备；'
    '② 定理 T1 —— E2 修法后果二分：(a) 逻辑完备⇒「七类之外」可过集空⇒结构闭合；'
    '(b) 仅实证完备⇒未知第八类 C8 可满足「七类之外」而仍在体系内⇒不闭合；腿(b)不可排⇒修法只消已知反例；'
    '③ 定理 T2 —— 名单不代填的结构理由：名单有限枚举+分类非逻辑完备⇒任何有限名单不能证"无第八类"，'
    '代填把开放式开放伪装成封闭式闭合，r436 BOUNDARY 维持；'
    '④ 定理 T3 —— 归纳缺口 Laplace 下界 1/(n+2)=1/9>0(n=7)⇒7/7 不能把样本外风险归零；'
    '⑤ 定理 T4 —— 唯一出口九重复证(r429–r437 九侧面)；⑥ 可迁移判据 M-13 与诚实边界。'
    '锚点实读 10/10。不代填名单、不宣称 r429 七类错误、不产生新物理、不销账。'
)
md_line = (
    '├── 判定_' + NAME + '.md  '
    '# 新增（**r437 · 2026-11-21**）：r437 判定册 —— '
    '§〇 一句话结论（E2 修法只消字面冲突、结构仍开放）· '
    '§一 与既有册分工（接手 r436 BOUNDARY）· §二 靶点 · §三 分类完备性两分 · '
    '§四 修法后果二分（字面≠结构）· §五 名单不代填与归纳缺口 1/9 · §六 唯一出口九重复证 · '
    '§七 诚实边界与可迁移判据 M-13 · §八 裁决与下一步 · §九 守卫与自抓 · §十 红线 · '
    '§十一 产物清单 · §十二 锚点实读 10/10。评级 O/L2；不产生新物理、不销既有债务。'
)
nl = '\r\n' if '\r\n' in txt else '\n'
a1 = '│   ├── TUFT-r436_唯一出口门禁自审'
a2 = '├── 判定_TUFT-r436_唯一出口门禁自审'
assert txt.count(a1) == 1 and txt.count(a2) == 1
j1 = txt.index('\n', txt.index(a1)) + 1
j2 = txt.index('\n', txt.index(a2)) + 1
txt = txt[:j2] + md_line + nl + txt[j2:]
txt = txt[:j1] + py_line + nl + txt[j1:]
shutil.copyfile(P, BAK)
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    f.write(txt)
print('README r437 count =', txt.count('r437'))
print('backup ->', BAK)
