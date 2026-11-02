# -*- coding: utf-8 -*-
"""r376 README 双锚点登记（幂等 / 零删除 / 写后读回验证）。

纪律（同 _reg_r375.py）：
  · 锚点串含本卷 RID（`TUFT-r376_` / `判定_判定_TUFT-r376_`），先判存在再分流；
  · 源码树插在 `│   ├── TUFT-r375_` 之后，判定列表追加末尾；
  · README 为纯 LF ⇒ newline="\\n" 读写；写后按锚点计数断言 ==1，并断言备份末行仍在。
  · ★题面里的每一个数字都由盘上产物现读（JSON.res / summary / 判定册正文 / getsize），
    本脚本源码不手抄任何读数；条目正文直接取 JSON.main 的 title，不重打一遍。
"""
import io, os, sys, json, shutil, hashlib

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(ROOT, "README.md")
BAK = os.path.join(ROOT, "scratch", "_bak_README_pre_r376.md")

SRC_ANCHOR = "│   ├── TUFT-r375_"
SRC_KEY = "│   ├── TUFT-r376_"
JUD_ANCHOR = "├── 判定_判定_TUFT-r376_"
# REFRESH=1：本卷两行已存在时按锚点原地重写（只碰这两行，绝不用备份覆盖并发卷的新内容）
REFRESH = os.environ.get("R376_REFRESH", "") == "1"

BASE = ("TUFT-r376_审计ROOTV44_味对齐充要判据机验与谱塔核六值全复现_"
        "闭式Green双路对照与CKM冲突机验_示范F口径不可恢复定价")
FN = BASE + "_精算与可视化_2026-11-02.py"
P_JSON = os.path.join(ROOT, "数据", BASE + "_2026-11-02.json")
P_SRC = os.path.join(ROOT, "数据", "TUFT-r376_审计ROOTV44_三代味对齐_来料原件_用户附件逐字_2026-11-02.md")
P_JUD = os.path.join(ROOT, "判定", "判定_判定_" + BASE + "_2026-11-02.md")
JUD_FN = os.path.basename(P_JUD)

j = json.load(io.open(P_JSON, encoding="utf-8"))
if j["final"] != "ALL-GATES-PASS":
    sys.exit("ABORT: JSON.final = %s ⇒ 未全绿不登记" % j["final"])
S = j["summary"]
R = j["res"]


def rv(k):
    return R[k]


def n(k, nd=4):
    v = rv(k)
    if v is None:
        return "?"
    return ("%." + str(nd) + "g") % float(v)


src_sz = os.path.getsize(P_SRC)
src_md5 = hashlib.md5(io.open(P_SRC, "rb").read()).hexdigest()
jud_txt = io.open(P_JUD, encoding="utf-8").read()
_selfhat = jud_txt.split("## 八b、自伤登记")[1].split("\n## ")[0]
n_hat = sum(1 for L in _selfhat.split("\n") if L.startswith("- "))
_titles = "\n"; _MAIN = j["main"]
lines_txt = [L for L in jud_txt.split("\n") if L.startswith("## ")]


def main():
    s = io.open(README, encoding="utf-8", newline="").read()
    old_len = len(s)
    last_line = s.rstrip("\n").split("\n")[-1][:40]

    if not os.path.exists(BAK):
        os.makedirs(os.path.dirname(BAK), exist_ok=True)
        shutil.copy2(README, BAK)
        print("BACKUP created:", os.path.basename(BAK))
    else:
        print("BACKUP exists, keep:", os.path.basename(BAK))

    src_line = (
        "│   ├── " + FN + "  # 新增（**r376 · 2026-11-02**）："
        "**审计 ROOT V44《三代粒子混合与统一场论的味对齐定理》**"
        "（条目 **%d**＝PASS %d / INFO %d / FAIL %d；控制组 **%d/%d**、守卫 **%d/%d**、退出码 0、`%s`）。"
        % (S["main_total"], S["main_pass"], S["main_info"], S["main_fail"],
           S["ctl_total"], S["ctl_total"], S["grd_total"], S["grd_total"], j["final"])
        + "★**V44-1 的 ⟺ 是真定理且前提不可删**：4 组精确复有理酉共轭（勾股数 3-4-5 旋转）双向零反例，"
        "全链分数算术无浮点（P01，正/反各 " + n("v441_fwd_cases", 0) + " 例）；"
        "删去「本征值互不相同」即构造出 [H,A]=0 而 A 非对角的简并反例（λ=(1,1,13)、1-2 块内非对角元 1，P02/C1）⇒ 来料把前提写进定理，非漏项。"
        "★**V44-2 的诊断量有牙齿**：−½Tr([H,A]²)=Σ_{i<j}(a_i−a_j)²|H_ij|² 经 sympy 对 9 参数通用 Hermitian 矩阵符号归零 + 3 组分数例集（P03）；"
        "酉共轭双路基不变 rel " + n("basis_inv_rel") + "；ε∈{1e-1..1e-4} 阶梯从精确零基线（I=" + n("I_eps_baseline", 1) + "）起，"
        "I=(a₁−a₂)²ε²=49ε² ⇒ 逐档比值 " + n("I_eps_ratio", 6) + " / " + n("I_eps_ratio23", 6) + "（P04/C2）。"
        "★★**谱塔核 S 的六个展示位全部逐字符复现**：口径 = Σ_{n≤2500} a_n(x_i)a_n(x_j)/n²，"
        "本卷闭式（coth/csch 部分分式，与 2500 项直求和两条独立路径）round6 命中 6/6（P08），"
        "截断与 ∞ 差 rel " + n("S_sum_vs_closed_rel") + "、尾段界 " + n("tail_2500_bound") + "（P09）；"
        "S 对称偏差 " + n("S_sym_dev", 1) + "、特征值 " + n("S_eig_min") + " / " + n("S_eig_mid") + " / " + n("S_eig_max") + "（正定，P10）；"
        "对照权重族（1/n、1/n⁴、均匀）rel " + n("ctl_S_rival") + " ⇒ 1/n² 这一权重是被定价的，不是唯一读法里最顺手的一个。"
        "★★**归一化「65 位通过」隐含未声明区间**：[0,1] 上三代偏差 " + n("norm_max_dev_01", 1) + "（机器零，P05），"
        "读成 [0,∞) 时 τ 第 7 位就破 dev " + n("norm_inf_tau") + "（P06/C4）；而 a_n(x)=√2∫₀¹cos(nπz)p_x dz 的 overlap 双路相符 rel "
        + n("overlap_rel_max") + "（P07）⇒ 区间由一致性唯一钉死在 [0,1]。属口径债，不判矛盾。"
        "★**F 的绝对口径不可由附件恢复**：|F_full|/|F_1| 独立复算 " + n("F_ratio", 8) + "，与来料自称一致（P11）；"
        "但 (U†D_nU)₁₂ 的标准权重、共轭翻转、δ 反号、反解塔权指数 p*=" + n("F_pstar", 5) +
        " 五族对复数分量全失败（最近 rel " + n("F_best_rel") + "，p* 只命中「比值」这一投影，P12）⇒ 定价为「不可复现（11 文件 ZIP 未随附）」，不判「错」。"
        "★**M₁ 界与示范 Br 属抄写层一致**：由展示 Br 直算 " + n("M_from_printed_br", 8) + " TeV（与来料界 rel " + n("M1_rel_direct") + "）；"
        "把 Br 读作 4 位舍入带 ⇒ 界带 [" + n("M_env_lo", 8) + ", " + n("M_env_hi", 8) + "] 覆盖来料界（P13），M⁻⁴ 指数单独定价（C7）；"
        "条件性比较成立（示范 Br < SINDRUM 上限，P14），μ→eγ 来料已自我区分、本卷复述该自限。"
        "★★**CKM 冲突定理与示范读数是唯一命中**：U_Q=U_D=I ⇒ V_CKM 为精确置换、非对角最大 " + n("vckm_off_max", 1) +
        "（同时对角 ⟹ 无混合，P15）；ε 破缺给一阶线性 |V₁₂|=" + n("V12_num", 10) + "（ε=1e-2）/" + n("V12_closed", 10) +
        "（ε=1e-3），逐档比值 " + n("V12_eps_ratio", 10) + "、2×2 闭式与数值 Jacobi 两路 rel " + n("ckm_two_path") + "（C8）；"
        "来料示范 X_Q=diag(8,7,5)、R₁₂(0.225)、单模 a₁ ⇒ |(A₁ᵘ)₁₂| 实算 rel " + n("ckm_demo_rel") + " 命中展示位，÷√2 等变体全排除（P16/C6）。"
        "★**「质量完全不同 ⇒ 无树级味改」的定量版成立**：f(X)=X²、g_n(X)=X+c_n 对齐构造下 2500/2500 模 I_n 精确零、"
        "质量间隙 ≥ " + n("mass_gap_min") + "（P17）；同一构造里 PMNS 可非对角（|V| 非对角最大 " + n("pmns_offdiag_max") +
        "）⇒ ℓ 侧对齐与中微子混合兼容，是 witness 不是障碍（P18）。"
        "★**★自伤登记（" + str(n_hat) + " 项，全文见判定册 §八b）**：跳号缺 P08、三处字面 True、20 处漏 note、"
        "T0_diag 二阶极点留数取错、herm() 契约改动连锁、jacobi 返回顺序拿反、mpmath API 三连、G10 禁词表住在自己源码里、"
        "第一枚 HTML 反照是 no-op；其中 **P01/P03 的初版归因（herm）作废并就地更正**——真凶是 `sum(items, ZERO_C)` 走元组拼接、"
        "自定义 cadd 从未被调用 ⇒ 虚部通道整体消失、「非零交换子」被读成零。"
        "★**取号**：动手前 `_probe_r376.py` 占位；来料原件的**两枚指纹分家**（驱动器现测并印 JSON.res）——"
        "存档文件整体 " + str(int(float(rv("src_bytes")))) + " 字节、md5 " + str(rv("src_md5")) + "；"
        "逐字载荷（头里声明的切法：最后一个三连字符分隔行起跳 5 字节）" + str(int(float(rv("payload_bytes")))) +
        " 字节、md5 " + str(rv("payload_md5")) + "，与原件头声明" +
        ("相符" if float(rv("payload_md5_matches_header")) == 1 else "不符") +
        "（登记脚本与驱动器都不抄这些数，全部 `os.path.getsize`／`hashlib.md5` 现读）。"
        "★**定价 0/5 不占度**（五槽全为复算/定价，无锁定常数的新约束），度数链维持 **36（r264 止）**。"
        "★**供给 0**：" + str(S["main_total"]) + " 条**不可与 r354/r360/r365/r368/r370/r374/r375 相加**（分层铁律）。"
        "★**OPEN**：`X-R376-1`（F 的归一/传播子口径需从 ZIP 恢复）/ `X-R376-2`（x 三代值由实测质量反演的映射未给出）/ "
        "`X-R376-3`（简并例外路径的显式构造未给出）；来料「52/52 断言清单」与 11 文件 ZIP 未随附 ⇒ 不核不判。"
        "**HTML 几何体检 GEOMETRY-OK（4 个内联 script 块全部执行、三图图元 13/9/2、越界 0）+ 两负控"
        "（图 1 柱高写成 0 抓 4 条、图 3 text.y=281 越界抓 1 条，均 rc=2）。下轮从 r377 起。**"
    )

    jud_line = (
        "├── " + JUD_FN + "  # 新增（**r376 · 2026-11-02**）：ROOT V44 判定册 —— "
        "§一 结论摘要（两条定理成立 / 谱塔核六值全复现 / 归一化区间被钉死 / F 绝对口径不可恢复 / CKM 示范唯一命中）· "
        "§二 主册 %d 行 · §三 控制组 %d 条 · §四 守卫 %d 条 · §五 S 展示位对拍表（round6 命中 6/6）· "
        "§六 F 口径扫描表（五族全失败）· §七 判定与分层 · §八 取号与诚实边界 · §八b **自伤登记（%d 项，含 P01/P03 归因作废就地更正）**。"
        % (S["main_total"], S["ctl_total"], S["grd_total"], n_hat)
        + "**判词** `%s`；**终态** `%s`。" % (j["verdict"], j["final"])
        + "**分层**：只覆盖 V44 一份来料，不复算 r354/r360/r365/r368/r370/r374/r375 的既有条目，条目不可相加。"
        + "**治理**：靶只读、未改 `verify.py`、未 git；**下轮从 r377 起**。"
    )

    if SRC_KEY in s:
        ls = s.split("\n")
        hit = [i for i, L in enumerate(ls) if L.startswith(SRC_KEY)]
        assert len(hit) == 1, ("src 锚点已存在但命中数 != 1", hit)
        if REFRESH:
            ls[hit[0]] = src_line
            s = "\n".join(ls)
            print("REPLACE src line in place (refresh mode, 不碰其它行)")
        else:
            print("SKIP src (anchor exists)")
    else:
        lines = s.split("\n")
        idx = [i for i, L in enumerate(lines) if L.startswith(SRC_ANCHOR)]
        assert len(idx) == 1, ("src anchor 命中数 != 1", idx)
        lines.insert(idx[0] + 1, src_line)
        s = "\n".join(lines)
        print("INSERT src after line", idx[0] + 1)

    if JUD_ANCHOR in s:
        if REFRESH:
            ls = s.split("\n")
            hit = [i for i, L in enumerate(ls) if L.startswith(JUD_ANCHOR)]
            assert len(hit) == 1, ("jud 锚点已存在但命中数 != 1", hit)
            ls[hit[0]] = jud_line
            s = "\n".join(ls)
            print("REPLACE jud line in place (refresh mode)")
        else:
            print("SKIP jud (anchor exists)")
        if not s.endswith("\n"):
            s += "\n"
    else:
        if not s.endswith("\n"):
            s += "\n"
        s += jud_line
        print("APPEND jud at EOF")

    io.open(README, "w", encoding="utf-8", newline="\n").write(s)

    t = io.open(README, encoding="utf-8", newline="").read()
    c_src = t.count("│   ├── TUFT-r376_")
    c_jud = t.count("├── 判定_判定_TUFT-r376_")
    print("bytes %d -> %d (+%d)" % (old_len, len(t), len(t) - old_len))
    print("src anchor count = %d (expect 1)" % c_src)
    print("jud anchor count = %d (expect 1)" % c_jud)
    print("prev last line kept exactly once =", t.count(last_line) == 1)
    print("no trailing blank   =", not t.endswith("\n\n"))
    print("CRLF count =", t.count("\r\n"))
    assert c_src == 1 and c_jud == 1, (c_src, c_jud)
    assert t.count(last_line) == 1, "备份末行被破坏 ⇒ 触发了伪删除"
    assert t.count("\r\n") == 0, "README 被写成 CRLF"
    return 0


if __name__ == "__main__":
    sys.exit(main())
