# -*- coding: utf-8 -*-
"""一次性脚本：把 r435 登记进 README 的源码树与判定树（r434 之后）。"""
import io, shutil
BASE = r'd:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化'
P = BASE + '/README.md'
BAK = BASE + '/_bak_README_pre_r435.md'
NAME = 'TUFT-r435_账基组选择反解定理_口径不变性元层边界与离散输入来源轴再定价_精算_2026-11-21'
with io.open(P, encoding='utf-8', newline='') as f:
    txt = f.read()
assert 'r435' not in txt
py_line = (
    '│   ├── ' + NAME + '.py  '
    '# 新增（**r435 · 2026-11-21**）：**走完 r434 §九裁决 3 未走的元层一步「账基组 D 怎么选」'
    '——账基组选择反解定理**（条目 8：PASS 2 / FAIL 4 / BOUNDARY 1 / INFO 1；守卫 15/15；'
    '控制组 2/2；退出码 0；判词 `BASIS-CHOICE-REVERSE-SOLVE--CALIBER-INVARIANCE-SUBDOMAIN-ONLY--'
    'GLOBAL-DOMAIN-UNREACHABLE--TWO-LEGS-BLOCKED--WINDOW-RANK3-ONLY--UNIQUE-EXIT-7FOLD-REAFFIRMED`）：'
    '① 账基组选择空间 —— 枚举 D1={c,ℏ}(rank2)/D2={c,ℏ,G}(rank3)/D4=full(rank4)，'
    'Fraction 精确求秩+增广秩判 span，复现 r434「D1 质量/D2 电荷不可陈述」⇒ 账基组决定可陈述目标量；'
    '② 定理 T1 —— 选择反解二分：(a) 按最小 N_ext 选 D4(rank4) ⇒ 选择随目标变化 ⇒ 目标反解撞 r421 C2；'
    '(b) 先验固定 D ⇒ r432 口径 II 原式 N_ext=1 经 r434 恒等式 diff=rank−3 修正为 4−rank，'
    '随 rank 2/3/4 取 2/1/0，仅 rank=3 一档给 1 ⇒ 相容窗口对 D 选择不稳健；'
    '③ 定理 T2/T3 —— 域分离：子域(D 固定 rank=3)三类保结构变换 N_ext 恒为 1，'
    '全局域(D 可选)不可达，子域恒等不能迁移为全局不变，r432 相容 Ω5 是 rank=3 特例；'
    '④ 定理 T4 —— 唯一出口七重复证(r429–r435 七侧面)同指体系外 E1–E4 预注册来料；'
    '⑤ 可迁移判据 M-4 与诚实边界。锚点实读 8/8。不代选账基组、不产生新物理、不销账。'
)
md_line = (
    '├── 判定_' + NAME + '.md  '
    '# 新增（**r435 · 2026-11-21**）：r435 判定册 —— '
    '§〇 一句话结论（口径不变性子域成立/全局不可达，r432 相容 Ω5 是 rank=3 特例）· '
    '§一 与既有册分工（承 r434/r433/r432/r421）· §二 靶点 · §三 账基组选择空间 · '
    '§四 选择反解二分定理（两腿全封）· §五 域分离定理 · §六 唯一出口七重复证 · '
    '§七 可迁移判据 M-4 · §八 裁决与下一步 · §九 守卫与自抓 · §十 红线 · '
    '§十一 产物清单 · §十二 锚点实读 8/8。评级 O/L2；不产生新物理、不销既有债务。'
)
nl = '\r\n' if '\r\n' in txt else '\n'
a1 = '│   ├── TUFT-r434_输入记账口径不变性'
a2 = '├── 判定_TUFT-r434_输入记账口径不变性'
assert txt.count(a1) == 1 and txt.count(a2) == 1
j1 = txt.index('\n', txt.index(a1)) + 1
j2 = txt.index('\n', txt.index(a2)) + 1
txt = txt[:j2] + md_line + nl + txt[j2:]
txt = txt[:j1] + py_line + nl + txt[j1:]
shutil.copyfile(P, BAK)
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    f.write(txt)
print('README r435 count =', txt.count('r435'))
print('backup ->', BAK)
