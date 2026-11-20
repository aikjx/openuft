# -*- coding: utf-8 -*-
"""一次性脚本：把 r429 登记进 README 的源码树与判定树（r407 之后）。"""
import io
import shutil

BASE = r'd:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化'
P = BASE + '/README.md'
BAK = BASE + '/_bak_README_pre_r429.md'
NAME = 'TUFT-r429_W3候选可达性二分定理_四门禁体系内不可达与外部来料唯一出口定价_精算_2026-11-21'

with io.open(P, encoding='utf-8', newline='') as f:
    txt = f.read()
assert 'r429' not in txt, 'README 已含 r429，拒绝重复登记'

py_line = (
    '│   ├── ' + NAME + '.py  '
    '# 新增（**r429 · 2026-11-21**）：**攻 r423 §7 OPEN「继续不产生新 W3 候选」+ r428 实测 0/4 —— '
    'W3 候选可达性二分定理**（条目 10：PASS 3 / FAIL 4 / BOUNDARY 1 / INFO 2；守卫 18/18；'
    '控制组 3/3；退出码 0；判词 `W3-INTERNAL-UNREACHABLE--SOURCE-TAXONOMY-EXHAUSTIVE--'
    'FOUR-GATES-STRUCTURALLY-BLOCKED--ASSIGNMENT-ENTROPY-EXTERNAL--0OF4-IS-THEOREM-NOT-OBSERVATION--'
    'PREREGISTERED-EXTERNAL-INPUT-ONLY-EXIT`）：'
    '① 来源分类学 —— 体系内全部数值输出来源 = 六类 provenance(FIT/TOY/MATH/SCHEME/DEFINITION/ISSUE，承 r423) '
    '+ SYSTEM-DERIVED(承 r421 C2) = 7 类，每类 9 个布尔特征，四门禁只读特征不读类名 ⇒ 非循环；'
    '② 定理 T1（核心）—— r421 四门禁 C1 定量/C2 非反解/C3 未拟合盲测/C4 双锚逐类机核，七类无一 passed'
    ' ⇒ 体系内 W3 可达数=0，r421/r423/r428 的 7 个实测候选逐条归类全败，与 r428 0/4 逐位对表；'
    '③ 定理 T2 —— 指派熵 log2(4!)=4.5849625007 bits 与 r413 逐位一致，封死「形状固定+指派派生」；'
    '④ 定理 T3 —— 把 0/4 从观测偶然升级为结构性下界，不否证外生来料（阳性对照过四门）；'
    '⑤ 定理 T4 —— 唯一出口四条件 E1 预注册冻结/E2 provenance 在六类外/E3 过 C1–C4/E4 双锚一致，'
    '体系内候选四项全败、外生对照全过；⑥ 可迁移判据 M-2 与「观测零值升格为结构定理」族登记。'
    '锚点实读 8/8。不宣称发现候选、不产生新物理、不否证研究方向、不销既有债务。'
)

md_line = (
    '├── 判定_' + NAME + '.md  '
    '# 新增（**r429 · 2026-11-21**）：r429 判定册 —— '
    '§〇 一句话结论（0/4 从观测升级为结构性定理，唯一出口为体系外预注册来料）· '
    '§一 与既有册分工（承 r410/r413/r421/r423/r428 + A 线 r405/r406）· §二 靶点 · '
    '§三 来源分类学七类穷举 + 非循环特征 · §四 四门禁矩阵（七类全败、阳性对照过门）· '
    '§五 定理 T1 体系内不可达 · §六 定理 T2 指派熵外部性 · §七 定理 T3 0/4 是定理 · '
    '§八 定理 T4 唯一出口四条件 · §九 可迁移判据 M-2 与复发族 · §十 裁决与下一步 · '
    '§十一 守卫与自抓（两处实现缺陷修复）· §十二 红线 · §十三 产物清单 · §十四 锚点实读 8/8。'
    '评级 O/L2；不产生新物理、不销既有债务。'
)

nl = '\r\n' if '\r\n' in txt else '\n'
a1 = '│   ├── TUFT-r407_EC挠率源媒介子替代性二分'
a2 = '├── 判定_TUFT-r407_EC挠率源媒介子替代性二分'
assert txt.count(a1) == 1, '源码树 r407 锚点不唯一: %d' % txt.count(a1)
assert txt.count(a2) == 1, '判定树 r407 锚点不唯一: %d' % txt.count(a2)

j1 = txt.index('\n', txt.index(a1)) + 1
j2 = txt.index('\n', txt.index(a2)) + 1
txt = txt[:j2] + md_line + nl + txt[j2:]
txt = txt[:j1] + py_line + nl + txt[j1:]

shutil.copyfile(P, BAK)
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    f.write(txt)
print('README r429 count =', txt.count('r429'))
print('backup ->', BAK)
