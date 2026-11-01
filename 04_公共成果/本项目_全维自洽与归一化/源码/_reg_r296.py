# -*- coding: utf-8 -*-
"""r296 README 注册（幂等补钉）：src 树 / jud 树 / compact 章 / full 章 四处
纪律：①锚点含本卷 RID；②先判存在再分流；③注册后逐 RID 清点；④diff 零删除；
⑤用「最后一条 r29x」动态锚点，避开并行会话的插入位置。
"""
import io
import os
import re
import shutil
from collections import Counter

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
RD = os.path.join(ROOT, "README.md")
BAK = os.path.join(ROOT, "_backup", "README.bak_r296_2026-11-01.md")
RID = "r296"
STAMP = "2026-11-01"
NAME = ("TUFT-r296_磁通手征谱可实现方程_多U1推广与充要判据与千组随机负对照_"
        "精算与可视化_2026-11-01")
TAIL = NAME[len("TUFT-r296_"):]

L_SRC = ("│   ├── %s.py  # 新增（**r296 · 2026-11-01**）：**磁通手征谱可实现方程 FCSRE"
         "（★多 U(1) 推广 + 充要判据 + 新方程产出）**（主条目 **8**：PASS 6 / FAIL 1 / INFO 1；"
         "**控制组 4/4**、**守卫 10/10**、退出码 0）。★**本卷产出的新方程（判据方程 / 机器筛选器）**："
         "**【FCSRE】d_i · Σ_{a=1..r} q_{i,a} M_a = s_i · N_gen**（i=1..n，s_i=±1），"
         "未知为电荷矩阵 Q ∈ Z^{n×r}、磁通 M ∈ Z^r；**可解 ⟺ lcm(d_1..d_n) ∣ N_gen** —— "
         "与 Q、磁通群秩 r、磁通取值 M **全部无关**。★**必要性**：(Q·M)_i ∈ Z ⇒ N_gen/d_i ∈ Z ⇒ "
         "d_i | N_gen ⇒ **提升磁通群的秩救不了三代**（机检 r=1..6 逐秩一致，全否）⇒ "
         "「多 U(1) 相互补偿凑三代」退路**彻底关闭**。★**充分性**：取 r=1、M_1=1、q_i = s_i·N_gen/d_i ∈ Z "
         "⇒ 构造性解，反代 index 全等于 N_gen（N=6、12 验证通过）。★**充要判据 9 算例全等**（SM 全谱×4 代数、"
         "无双重态 {3,3,1,1}、仅双重态 {2,2}、色三重 {3,3}、含 dim=4 {4,2}）。★**千组随机检验**："
         "N_gen=3 命中 **0/1000**（无反例）；**如实登记方法局限**——N_gen=6 随机命中同为 0/1000，"
         "因整数解在随机参数空间中极度稀疏 ⇒ 随机搜索只能给「无反例」证据，"
         "可行性由构造性解 + 两条正对照（{3,3,1,1} 下 3 代有解、构造 Q 反代成立）保证。"
         "★**X-R294-1 收口**：T² 上 H²=Z ⇒ U(N) 丛只由 c₁ 分类，平坦丛 F=0 ⇒ c₁=0 ⇒ **index=0** ⇒ "
         "非阿贝尔磁通不产生新的手征指标结构。★判据集新增 R7 ⇒ **R1–R7 = 0/7**。"
         "★判词：**NO-GO-STABLE + NEW-TOOL —— 结论对任意磁通群秩稳定，且本卷产出一个可机检的正向预筛器**"
         "（性质红线：判据方程，非动力学方程，不产新物理）。" % NAME)

L_JUD = ("├── 判定_TUFT-r296_%s.md  # 新增（**r296 · 2026-11-01**）：磁通手征谱可实现方程 FCSRE 判定册 —— "
         "§判定（8 主条目：多 U(1)^r 指标公式 / 必要性定理 / 充分性构造 / FCSRE 定稿充要判据 / "
         "千组随机检验 / 非阿贝尔收口 / 方程正向用途 / 判据集 R1–R7）· §控制组 **4/4**"
         "（{3,3,1,1} 下 3 代有解 / N=6 反代成立 / 整除否决独立复现 / r=6 仍无解）· §守卫 **10/10** · "
         "§本卷产出的方程（FCSRE + lcm 判据）· §判词（NO-GO-STABLE + NEW-TOOL）· §遗留（X-R296-1/2/3）。"
         % TAIL)

L_COMPACT = ("- **r296（2026-11-01）· 磁通手征谱可实现方程 FCSRE（★多 U(1) 推广 + 充要判据 + 新方程）**："
             "条目 **22**（主 **8**：PASS 6 / FAIL 1 / INFO 1），控制组 **4/4**，守卫 **10/10**，rc=0；"
             "源码 [`TUFT-r296_…py`](源码/%s.py)；判定册 [`判定_TUFT-r296_…md`](判定/判定_TUFT-r296_%s.md)；"
             "数据 [`…json`](数据/%s.json) / [`…md`](数据/%s.md) / [`…_report.txt`](数据/%s_report.txt)；"
             "runner `源码/_run_r296.py` → `源码/_out_r296.txt`；交互可视化 "
             "[`四力统一方程_磁通手征谱可实现方程可视化_2026-11-01.html`](四力统一方程_磁通手征谱可实现方程可视化_2026-11-01.html)。"
             "★**新方程 FCSRE**：d_i·Σ_a q_{i,a}M_a = s_i·N_gen，**可解 ⟺ lcm(d_i) ∣ N_gen**，"
             "与电荷矩阵、磁通群秩 r、磁通取值**全部无关** ⇒ **提升秩救不了三代**（r=1..6 逐秩实测全否）。"
             "★充分性由构造性解给出（r=1、M=1、q_i=N_gen/d_i，反代验证通过）；充要判据 **9 算例全等**。"
             "★千组随机：3 代 **0/1000** 无反例；**如实登记**——6 代随机命中亦 0/1000（整数解稀疏，"
             "随机搜索无判别力），可行性由构造性解 + 正对照保证。★**X-R294-1 收口**：T² 上 U(N) 丛只由 c₁ 分类，"
             "平坦丛 index=0 ⇒ 非阿贝尔磁通不产生新指标结构。★判据集 **R1–R7 = 0/7**。"
             "★判词：**NO-GO-STABLE + NEW-TOOL**（结论对任意秩稳定 + 产出可机检正向预筛器；"
             "**性质红线：判据方程，非动力学方程，不产新物理**）。"
             "★取号：三树实测 **r295 已被并行会话占用**（5 文件，03:4x 落盘）⇒ 取 **r296**（未抢未碰）。"
             "**下轮从 r297 复查起（并行链活跃，取号前必扫）**。"
             % (NAME, TAIL, NAME, NAME, NAME))

L_FULL = """
### r296 · 2026-11-01 · 磁通手征谱可实现方程 FCSRE（★多 U(1) 推广 + 充要判据 + 新方程）

- **产物**：源码 [`TUFT-r296_…py`](源码/%s.py)；数据 [`…json`](数据/%s.json) / [`…md`](数据/%s.md) / [`…_report.txt`](数据/%s_report.txt)；判定册 [`判定_TUFT-r296_…md`](判定/判定_TUFT-r296_%s.md)；runner `源码/_run_r296.py` → `源码/_out_r296.txt`；交互可视化 [`四力统一方程_磁通手征谱可实现方程可视化_2026-11-01.html`](四力统一方程_磁通手征谱可实现方程可视化_2026-11-01.html)
- **复现**：`python -X utf8 源码\\_run_r296.py` ⇒ **rc=0**，条目 **22**（主 **8**：**PASS 6 / FAIL 1 / INFO 1**），**控制组 4/4**，**守卫 10/10**，耗时 0.26 s。
- **命题**：把 r294 的 r=1 定理推广到**任意磁通群秩 r**，并给出**充要判据方程**（本轮同时回答「能否发现新的理论体系方程」）。
- **★本卷产出的方程**：**【磁通手征谱可实现方程 FCSRE】** `d_i · Σ_{a=1..r} q_{i,a} M_a = s_i · N_gen`（i = 1..n，s_i = ±1），未知 Q ∈ Z^{n×r}、M ∈ Z^r；**可解 ⟺ lcm(d_1,…,d_n) ∣ N_gen**。★**性质红线**：这是**判据方程 / 机器筛选器**，**不是动力学方程，不产生新物理、不预言新现象**——但它是本项目库中此前不存在的**可机检正向预筛工具**。
- **P2 · 必要性（与秩无关，★关键推广）**：(Q·M)_i = Σ_a q_{i,a}M_a 必为整数 ⇒ N_gen/d_i 必为整数 ⇒ **d_i | N_gen**。这一步**不涉及 Q 的形式、不涉及秩 r、不涉及磁通取值**，是整数性的直接后果 ⇒ **提升磁通群秩 r 救不了三代**。机检 r = 1..6（每组一个确定性电荷矩阵）：判据与实解搜索逐组一致，**全部为否**。「多 U(1) 磁通相互补偿凑三代」这条退路**彻底关闭**。
- **P3 · 充分性（构造性）**：若 lcm | N_gen，取 **r=1、M_1=1、q_{i,1} = s_i·N_gen/d_i ∈ Z** 即得解。反代验证：N_gen=6 ⇒ q = 6/d_i、index(D_i) 全等于 6；N_gen=12 同理 ⇒ 构造性证明，非空谈。
- **P4 · 充要判据 9 算例全等**：SM 全谱 × {3,6,12,2}、无双重态 {3,3,1,1}×3、仅双重态 {2,2}×{2,3}、色三重 {3,3}×3、含 dim=4 {4,2}×4 ⇒ **判据与实解逐组一致（9/9）**。
- **P5 · 千组随机检验（★如实登记两处方法局限）**：1000 组确定性伪随机电荷矩阵（秩循环 1..6，元素 ∈[−5,5]，LCG 可复现）⇒ **N_gen=3 命中 0/1000**（无反例）。**如实说明**：(i) 3 代的 0 命中是整除性前置否决（3/6、3/2 非整数）的**必然结果**，搜索在第一步即被短路，**不是随机搜索的独立证据**；(ii) **N_gen=6 的随机命中同样为 0/1000**，原因是整数解在随机参数空间中**极度稀疏**（目标向量须落在随机矩阵 Q 的**整数**列空间内）⇒ **随机搜索对可行性没有判别力**，只能提供「未发现反例」。可行性由 **P3 构造性解**与两条正对照独立保证：**C1** 维数集 {3,3,1,1}、N_gen=3 ⇒ 有解；**C2** 构造 Q_i=6/d_i、M=1 ⇒ 有解且反代 index 全等于 6。
- **P6 · X-R294-1 收口（非阿贝尔磁通）**：T² 的上同调 **H²(T²,Z) = Z**（秩 1）⇒ U(N) 丛的拓扑**只由第一陈数 c₁ 分类**，其余为**平坦模**（两条 Wilson 线）。平坦联络 F=0 ⇒ c₁ = (1/2π)∫tr F = **0** ⇒ **index = 0** ⇒ 非阿贝尔磁通在 T² 上**不产生任何新的手征指标结构**：要么归约到 U(1) 情形（仍受除性约束），要么什么也不产生。代价：想用非平坦非阿贝尔磁通须放弃 T²（c₂/瞬子数才进入指标）⇒ E3 诚实边界，本卷不断言。
- **控制组（4/4）**：C1 子集 {3,3,1,1} 下 3 代判据为真且有解（判据能给出肯定）；C2 N=6 有解且反代 index 全等于 6；C3 整除否决可独立复现（3 不被 6、2 整除）；C4 秩提升到 r=6（单位型电荷矩阵）仍无解。
- **P8 · 判据集**：在 r294 的 R1–R6 之外新增 **R7「磁通群秩提升能否绕过除性约束」＝否** ⇒ **R1–R7 = 0/7**。
- **判词**：**NO-GO-STABLE + NEW-TOOL** —— r294 的结论**对任意磁通群秩 r 都稳定**（NO-GO-STABLE），同时本卷产出一个**新的可机检工具** FCSRE + lcm 判据，用途是**正向预筛**：任何 T² 类高维手征谱构造，在写作用量之前即可用一次整除性检查判定可行性（NEW-TOOL）。
- **取号**：起草时三树实测 **r295 已被并行会话占用**（5 个文件，03:4x 落盘未注册）⇒ 顺延取 **r296**（未抢未碰任何他卷字节）；注册时用「最后一条 r29x」动态锚点，避免与并行会话的插入位置冲突。**下轮从 r297 复查起（并行链活跃，取号前必扫）**。
- **治理**：未改 `verify.py`；未跑 `refresh_catalog.py`；未改任何既有卷字节（守卫 G9 逐路径核验）；git 由收口提交统一处理；**本卷 22 条不可与 r292 的 30 条、r294 的 24 条相加**（同一命题的三轮攻防：r292 提命题 → r294 Schur 升定理 → r296 多秩推广 + 充要判据，结论强度取最新一轮）。
""" % (NAME, NAME, NAME, NAME, TAIL)


def last_index(lines, pred):
    for i in range(len(lines) - 1, -1, -1):
        if pred(lines[i]):
            return i
    return -1


def main():
    txt = io.open(RD, encoding="utf-8").read()
    os.makedirs(os.path.dirname(BAK), exist_ok=True)
    if not os.path.exists(BAK):
        shutil.copy2(RD, BAK)
        print("备份已建：", BAK)
    else:
        print("备份已存在，不覆盖：", BAK)

    if txt.count("TUFT-%s_" % RID) > 0:
        print("本卷条目已存在 ⇒ 幂等跳过。")
        return 0

    lines = txt.split("\n")
    i_src = last_index(lines, lambda s: bool(re.match(r"^│   ├── TUFT-r29\d_", s)) and ".py" in s)
    i_jud = last_index(lines, lambda s: bool(re.match(r"^├── 判定_TUFT-r29\d_", s)))
    i_cmp = last_index(lines, lambda s: bool(re.match(r"^- \*\*r29\d（", s)))
    print("动态锚点：src=%d jud=%d compact=%d" % (i_src, i_jud, i_cmp))
    if min(i_src, i_jud, i_cmp) < 0:
        print("锚点缺失 ⇒ 中止（不写入）")
        return 2

    out, done = [], {"src": 0, "jud": 0, "compact": 0, "full": 0}
    for k, ln in enumerate(lines):
        out.append(ln)
        if k == i_src:
            out.append(L_SRC)
            done["src"] += 1
        elif k == i_jud:
            out.append(L_JUD)
            done["jud"] += 1
        elif k == i_cmp:
            out.append(L_COMPACT)
            done["compact"] += 1
    if done["compact"] == 1:
        out.append(L_FULL.rstrip("\n"))
        done["full"] += 1

    io.open(RD, "w", encoding="utf-8").write("\n".join(out))
    print("插入统计：", done)

    back = io.open(RD, encoding="utf-8").read()
    for key in ["│   ├── TUFT-%s_" % RID, "├── 判定_TUFT-%s_" % RID,
                "- **%s（" % RID, "### %s ·" % RID]:
        print("清点 %-24s = %d" % (key, back.count(key)))

    old = io.open(BAK, encoding="utf-8").read().split("\n")
    cur = back.split("\n")
    co, cc = Counter(old), Counter(cur)
    lost = [k for k in co if cc[k] < co[k]]
    print("删除行检查：备份 %d → 新版 %d 行；丢失行种类 %d" % (len(old), len(cur), len(lost)))
    for k in lost[:5]:
        print("  !! 丢失：", k[:110])
    ok = (not lost) and all(v == 1 for v in done.values())
    print("RC =", 0 if ok else 2)
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
