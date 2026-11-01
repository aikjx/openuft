# -*- coding: utf-8 -*-
"""r306 README 注册脚本（纯插入、零删除、逐 RID 清点四处各=1）"""
import io, os, datetime, difflib, shutil

BASE = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(BASE, "README.md")
NOW = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BAK = os.path.join(BASE, "_backup", "README.bak_r306_%s.md" % NOW)
os.makedirs(os.path.dirname(BAK), exist_ok=True)

PFX = "TUFT-r306_磁通手征谱混合源可实现方程GMFRE_Smith标准形推广与多源整除性松动诚实边界_精算与可视化_2026-11-01"
JPFX = "判定_TUFT-r306_磁通手征谱混合源可实现方程GMFRE_Smith标准形推广与多源整除性松动诚实边界_精算与可视化_2026-11-01"

src_line = ("│   ├── %s.py  # 新增（**r306 · 2026-11-01**）："
            "**磁通手征谱混合源可实现方程 GMFRE（★判据方程层 · 攻 X-R296-2）**"
            "（主条目 **8**：PASS 18 / FAIL 1 / INFO 3；**控制组 4/4**、**守卫 10/10**、退出码 1——"
            "P7 预期 FAIL，标准机制下 R1–R8 = 0/8 = NO-GO）。★**不引外部来料**——攻靶是本库 r296 判定册自留 OPEN X-R296-2。"
            "★★**GMFRE（多源推广）**：把 FCSRE 推广为 多源整数线性系统 `A·t = s·N_gen`（A∈Z^{n×k}），"
            "可解性用 **行列式因子定理** 判定（D_k([A|b])=D_k(A), k=1..rank），无 Smith 标准形算法风险。"
            "★★**诚实结论**：纯通量（A=diag(d_i)）复现 lcm=6 阈值（N_gen=6 可 / 3 不可）；"
            "**非比例混合源确能松动 lcm**（g=(-9,-3,-3,-1,1,1) ⇒ N_gen=3 可解，特解 t=[2,1]）；"
            "但 **uniform-geometric 平凡逃逸**（t=[0,3]=把答案写进去）与「标准几何源耦合∝d_i」共同说明："
            "**标准机制下 NO-GO 稳定**，松动只在答案注入型源。**判词 NO-GO-STABLE + NEW-TOOL**。"
            "★**与 r296 不可相加**；**取号碰撞**：r304 被并行 ROOT V20 先占，顺延 r306。") % PFX

jud_line = ("├── %s.md  # 新增（**r306 · 2026-11-01**）："
            "磁通手征谱混合源可实现方程 GMFRE 判定册（★判据方程层 · 攻 X-R296-2）—— "
            "§判决主文（NO-GO-STABLE + NEW-TOOL）· §GMFRE 多源整数线性系统 A·t=s·N_gen 与行列式因子充要判据 · "
            "§诚实边界（标准几何源∝d_i ⇒ 落回 FCSRE NO-GO）· §混合源松动 lcm 的精确反证"
            "（g=(-9,-3,-3,-1,1,1) ⇒ N_gen=3 特解 t=[2,1]）· §uniform-geometric 平凡逃逸（答案注入）· "
            "§与既有卷（r296/r294/r302/r305）· §遗留 OPEN（X-R301-1）· §最终一句。") % JPFX

cmp_line = ("- **r306（2026-11-01）· 磁通手征谱混合源可实现方程 GMFRE：多源整除性松动的诚实边界"
            "（★判据方程层 · 攻 r296 自留 OPEN X-R296-2）**：**不引外部来料**，把 r296 的 FCSRE 推广为 "
            "**多源整数线性系统 `A·t = s·N_gen`**，用 **行列式因子定理** 给充要判据（D_k([A|b])=D_k(A)）。"
            "★★**诚实结论**：纯通量（A=diag(d_i)）复现 **lcm(d_i)=6 阈值**（N_gen=6 可 / 3 不可）；"
            "**非比例混合源确能松动 lcm**（g=(-9,-3,-3,-1,1,1) ⇒ N_gen=3 特解 t=[2,1]），"
            "但 **uniform-geometric（t=[0,3]）= 把答案写进去** 的平凡逃逸，加上「标准几何源耦合必∝d_i」，"
            "共同说明 **标准机制下 NO-GO 稳定**，松动只在答案注入型源。★**判词 NO-GO-STABLE + NEW-TOOL**；"
            "与 r296/r294/r302/r305 **不可相加**。★**取号碰撞**：r304 被并行 ROOT V20 先占（09:44:37），顺延 **r306**。"
            "**下轮从 r307 复查起（并行链活跃，取号前必扫三树 + README 四处）**。")

detail_block = (
"### r306 · 2026-11-01 · 磁通手征谱混合源可实现方程 GMFRE（★判据方程层 · 攻 r296 自留 OPEN X-R296-2）\n"
"- **产物**：源码 [`TUFT-r306_…py`](源码/%s.py)；"
"数据 [`…json`](数据/%s.json) / [`…md`](数据/%s.md) / [`…_report.txt`](数据/%s_report.txt)；"
"判定册 [`判定_TUFT-r306_…md`](判定/%s.md)；"
"runner `源码/_run_r306.py` → `源码/_out_r306.txt`；"
"交互可视化 [`四力统一方程_磁通手征谱混合源可实现方程可视化_2026-11-01.html`](四力统一方程_磁通手征谱混合源可实现方程可视化_2026-11-01.html)\n"
"- **复现**：`python -X utf8 源码\\_run_r306.py` ⇒ **rc=1**（P7 预期 FAIL：标准机制下 R1–R8 = 0/8 = NO-GO），"
"条目 **22**（主 **8**：PASS 18 / FAIL 1 / INFO 3），**控制组 4/4**，**守卫 10/10**。\n"
"- **与既有卷**：承 **r296** FCSRE（单类源 lcm 判据）⇒ 本卷推广为 **GMFRE**（多源整数线性系统 A·t=s·N_gen，行列式因子充要判据）；"
"与 **r294** 同题（三代不可实现）；与 **r302/r305** 等谱/扭转线互补而非重叠（本卷攻「混合源整除性松动」，r302/r305 攻「等谱唯一解是一代」）；"
"**不可相加**，强度取较新的一轮。★**判词 NO-GO-STABLE + NEW-TOOL**：标准几何源（耦合∝维数 d_i）下 3 代仍不可实现；"
"lcm 约束只在「非比例/答案注入型」混合源下被打破（OPEN X-R301-1：须给出具体非比例 A 且证其来自合法几何）。\n"
"- **取号**：落盘前实测 r304 已被并行会话占用（ROOT V20 跨现象 α 本源审计，09:44:37 先到）；"
"按「先到者保号、后到者改号」顺延取 **r306**（r305 亦被占用）；未抢未碰并行 r304 字节，已将本卷 r304(GMFRE) 孤儿文件移入 scratch，"
"并还原并行 `_run_r304.py`。**下轮从 r307 复查起（并行链活跃，取号前必扫三树 + README 四处）**。\n"
) % (PFX, PFX, PFX, PFX, JPFX)

def find_idx(lines, marker):
    for i, ln in enumerate(lines):
        if marker in ln:
            return i
    return -1

with io.open(README, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

# 备份（首次创建、不覆盖既有）
shutil.copy2(README, BAK)

# 先判本卷是否已存在（存在=原地刷新 / 不存在=插入）
already = any("TUFT-r306_" in ln for ln in lines)
assert not already, "r306 已存在于 README，应原地刷新而非插入"

# 锚点定位
i_src = find_idx(lines, "TUFT-r305_通量荷的等谱归一")   # 源码树 r305 行
i_jud = find_idx(lines, "判定_TUFT-r305_通量荷的等谱归一")  # 判定树 r305 行
i_cmp = find_idx(lines, "- **r305（2026-11-01）· 通量荷")  # compact r305 行
i_det = find_idx(lines, "### r304 · 2026-11-01 · ROOT V20")  # detail 插入点（r305 块之后、r304 块之前）
assert i_src >= 0 and i_jud >= 0 and i_cmp >= 0 and i_det >= 0, "锚点定位失败"

# 纯插入（倒序插入避免索引漂移）
new = list(lines)
# detail 插在 i_det 之前
new.insert(i_det, detail_block.rstrip("\n"))
new.insert(i_cmp + 1, cmp_line)
new.insert(i_jud + 1, jud_line)
new.insert(i_src + 1, src_line)

with io.open(README, "w", encoding="utf-8") as f:
    f.write("\n".join(new))

# 校验：逐 RID 固定串清点四处各=1
checks = {
    "src树": ("│   ├── TUFT-r306_", 1),
    "判定树": ("├── 判定_TUFT-r306_", 1),
    "compact": ("**r306（", 1),
    "detail": ("### r306 ·", 1),
}
ok = True
for name, (s, expect) in checks.items():
    c = sum(1 for ln in new if s in ln)
    flag = "OK" if c == expect else "FAIL"
    if c != expect:
        ok = False
    print("%s: %s 命中 %d (期望 %d) %s" % (name, s, c, expect, flag))

# 零删除校验
bak_lines = io.open(BAK, "r", encoding="utf-8").read().split("\n")
removed = [ln for ln in bak_lines if ln not in set(new)]
print("diff 删除行数: %d %s" % (len(removed), "OK" if len(removed) == 0 else "FAIL"))
if len(removed):
    ok = False
    for r in removed[:10]:
        print("  删: " + r[:80])

print("注册结果:", "PASS" if ok else "FAIL")
