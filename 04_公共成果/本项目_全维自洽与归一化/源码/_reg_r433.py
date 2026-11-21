# -*- coding: utf-8 -*-
"""一次性脚本：把 r433 登记进 README 的源码树与判定树（r432 之后）。"""
import io, shutil
BASE = r'd:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化'
P = BASE + '/README.md'
BAK = BASE + '/_bak_README_pre_r433.md'
NAME = 'TUFT-r433_离散输入预置二分定理_口径II过O1不可达与唯一出口复证_精算_2026-11-21'
with io.open(P, encoding='utf-8', newline='') as f:
    txt = f.read()
assert 'r433' not in txt
py_line = (
    '│   ├── ' + NAME + '.py  '
    '# 新增（**r433 · 2026-11-21**）：**接手 r432 §十一 未裁决 OPEN「群与代的 2 个离散输入是否算预置 SM 谱」'
    '——离散输入预置二分定理**（条目 8：PASS 2 / FAIL 4 / BOUNDARY 1 / INFO 1；守卫 12/12；'
    '控制组 2/2；退出码 0；判词 `DISCRETE-PRESET-DICHOTOMY--CALIBER-II-COMPATIBLE-NOT-O1-PASS--'
    'BOTH-LEGS-BLOCKED--PRESET-OR-NEEDS-EXTERNAL-CHOICE--O1-UNREACHABLE-UNDER-OMEGA5--'
    'UNIQUE-EXIT-5FOLD-REAFFIRMED`）：'
    '① 离散轴预置定义 —— r429 七类来源分类学到离散轴，取值来自拟合/反标定/历史给定判 PRESET，'
    '非预置须同时满足表示论导出+异常抵消固定+无外部选择唯一；'
    '② 定理 T1/T2 —— 群与代两来源腿全封：(a) 拟合/反解/历史给定⇒PRESET 撞 O1「从不预置 SM 谱」；'
    '(b) 第一性表示论+异常抵消⇒承 r413 指派熵 log2(24)=4.585 bits 外部输入⇒仍需外部选择原理⇒同样非零预置；'
    '两腿穷尽⇒口径 II 相容 Ω5 不等于过 O1，且是结构封死而非没做到；'
    '③ 定理 T3 —— 承 r432 N_ext=(|S|-3)+N_coupling，口径 II 连续轴 OK(1≤1) 但过 O1=连续OK∧离散OK，'
    '离散轴全败⇒O1_reachable=False；④ 定理 T4 —— 唯一出口五重复证(r429 体系内不可达/r430 外生0/40/'
    'r431 C4标度/r432 基组闭包/r433 离散预置)同指体系外 E1–E4 预注册来料；'
    '⑤ 可迁移判据 M-3 与诚实边界。锚点实读 8/8。不代选规范群/代数、不产生新物理、不销账。'
)
md_line = (
    '├── 判定_' + NAME + '.md  '
    '# 新增（**r433 · 2026-11-21**）：r433 判定册 —— '
    '§〇 一句话结论（口径 II 相容 Ω5 ≠ 过 O1，群与代两来源腿全封）· '
    '§一 与既有册分工（接手 r432 未裁决 OPEN）· §二 靶点 · §三 离散轴预置定义 · '
    '§四 来源二分定理（两腿全封）· §五 预算守恒+过 O1 合取不可达 · §六 唯一出口五重复证 · '
    '§七 可迁移判据 M-3 与诚实边界 · §八 裁决与下一步 · §九 守卫与自抓 · §十 红线 · '
    '§十一 产物清单 · §十二 锚点实读 8/8。评级 O/L2；不产生新物理、不销既有债务。'
)
nl = '\r\n' if '\r\n' in txt else '\n'
a1 = '│   ├── TUFT-r432_基组闭包定理'
a2 = '├── 判定_TUFT-r432_基组闭包定理'
assert txt.count(a1) == 1 and txt.count(a2) == 1
j1 = txt.index('\n', txt.index(a1)) + 1
j2 = txt.index('\n', txt.index(a2)) + 1
txt = txt[:j2] + md_line + nl + txt[j2:]
txt = txt[:j1] + py_line + nl + txt[j1:]
shutil.copyfile(P, BAK)
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    f.write(txt)
print('README r433 count =', txt.count('r433'))
print('backup ->', BAK)
