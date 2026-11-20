# -*- coding: utf-8 -*-
"""一次性脚本：把 r407 登记进 README 的源码树与判定树（r406 之后），保留原行尾。"""
import io
import shutil

BASE = r'd:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化'
P = BASE + '/README.md'
BAK = BASE + '/_bak_README_pre_r407.md'

with io.open(P, encoding='utf-8', newline='') as f:
    txt = f.read()

assert 'r407' not in txt, 'README 已含 r407，拒绝重复登记'

py_line = (
    '│   ├── TUFT-r407_EC挠率源媒介子替代性二分与挠率作为统一力载体不可行性_精算_2026-11-13.py  '
    '# 新增（**r407 · 2026-11-13**）：**攻 r32 判定册 §十一 方向丙 P1-2 遗留必答「接触型挠率源是否可被一个传递子替代」'
    ' —— 媒介子二分定理**（条目 14：PASS 5 / FAIL 5 / BOUNDARY 1 / INFO 2 / CORRECTED 1；守卫 24/24；'
    '控制组 5/5；退出码 0；判词 `MEDIATOR-DICHOTOMY-CLOSED--MASSLESS-BRANCH-EXCLUDED-BY-DIMENSION--'
    'MEDIATION-SCALE-LOCKED-BY-ALPHA--NO-INDEPENDENT-TORSION-CONTENT--UNIFIED-FORCE-CARRIER-FAIL`）：'
    '① 质量维数台账（13 条，9 条 SI 四元组逐条机核 d=m-l-t + 2 负对照）锁定 d(alpha)=+2、d(lambda)=0 '
    '⇒ 有效四费米子算符系数 C=lambda^2/(4 alpha) 的 d=-2，必写成 1/Lambda^2、Lambda^2=4 alpha/lambda^2；'
    '② 定理 T1 质量分支缺失（维数计数、非循环）：无质量媒介子在本机制内不可能，Lambda 有质量维数 +1；'
    '③ 代数 slave 精确复算（24 分量、Hessian 2alpha*I 满秩、T*=-lambda*J/(2alpha) 梯度残差 0、C=2/3）'
    '三路线一致（双源代入比=1、数值最小化+二阶差分相对偏差 4.25e-47）、四错误因子变体全鉴别；'
    '④ 定理 T2 尺度锁死：alpha 取引力匹配值 R=2sqrt(pi)ell_P=5.729e-35 m、媒介子 3.444e18 GeV、'
    '1 fm 处 e^{-Lambda r} 下溢为 0（宏观严格无力）；要可观测力程须 alpha 偏离引力匹配值 30+ 数量级'
    ' ⇒ 挠率扇区与引力解耦；⑤ 定理 T3 与质量 Lambda 的重矢量媒介子在费米子扇区不可区分'
    '（同一 dim-6 算符 C*O6、同一系数 1/Lambda^2）⇒ r32 必答=是、替代物唯一到质量 2sqrt(alpha)/lambda '
    '的重矢量、r32 附条件「挠率无独立物理内容」被兑现；⑥ 定理 T4 Yukawa vs 1/r^2 函数形式不齐'
    '（10 倍力程处 Yukawa 力远大于 1/r^2 预言 0.01）；⑦ MT10 更正 r32 P1-2「不可重整」为'
    '「dim-6 算符须在 Lambda^2 处 UV」；⑧ Omega5-S 判 NO-INFORMATION-GAIN（Z\' 阳性对照 ACCEPTED）、'
    '可迁移判据 M-1 与「新几何载体=旧规范结构改写」族登记。锚点实读 7/7。'
    '否证的是「挠率作为额外长程统一力载体」资格，不否证 EC 自洽性(r32 Y13)、传播挠率路线(r341)'
    '或普朗克尺度修正；不产生新物理、不销既有债务。'
)

md_line = (
    '├── 判定_TUFT-r407_EC挠率源媒介子替代性二分与挠率作为统一力载体不可行性_精算_2026-11-13.md  '
    '# 新增（**r407 · 2026-11-13**）：r407 判定册 —— '
    '§〇 一句话结论（r32 P1-2 必答「接触项是否等价于交换传递子」=是，挠率无独立物理内容）· '
    '§一 与既有册分工（防重复）· §二 靶点 r32 P1-2 · §三 质量维数台账（两个新自由量被动作强制锁定）· '
    '§四 代数 slave 精确复算（C=2/3、三路线一致）· §五 定理 T1 质量分支缺失 · §六 定理 T2 尺度锁死定价表 · '
    '§七 定理 T3 与重矢量不可区分 · §八 定理 T4 Yukawa vs 1/r^2 不齐 · §九 表述更正/参数账/可迁移判据 M-1 · '
    '§十 裁决与下一步 · §十一 自抓与守卫（两处实现缺陷修复）· §十二 红线 · §十三 产物清单 · '
    '§十四 锚点实读 7/7。评级 O/L2；决定性判决，不产生新物理。'
)

nl = '\r\n' if '\r\n' in txt else '\n'

a1 = '│   ├── TUFT-r406_继续攻破口径重定义'
a2 = '├── 判定_TUFT-r406_继续攻破口径重定义'
assert txt.count(a1) == 1, '源码树 r406 锚点不唯一: %d' % txt.count(a1)
assert txt.count(a2) == 1, '判定树 r406 锚点不唯一: %d' % txt.count(a2)

j1 = txt.index('\n', txt.index(a1)) + 1
j2 = txt.index('\n', txt.index(a2)) + 1

# 先插靠后的判定树，再插靠前的源码树，避免偏移失效
txt = txt[:j2] + md_line + nl + txt[j2:]
txt = txt[:j1] + py_line + nl + txt[j1:]

shutil.copyfile(P, BAK)
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    f.write(txt)

print('README r407 count =', txt.count('r407'))
print('py_line len =', len(py_line), ' md_line len =', len(md_line))
print('backup ->', BAK)
