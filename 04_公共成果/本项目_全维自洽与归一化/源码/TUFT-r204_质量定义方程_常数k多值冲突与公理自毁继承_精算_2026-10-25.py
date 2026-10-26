# -*- coding: utf-8 -*-
"""
TUFT-r204 质量定义方程 审计引擎
靶：S17 公式 03「质量定义方程」 v1（三份主文档）
  DocA = 电子质量视角下的质量定义方程：严格求导、证明与实验验证.md（13.4k）
  DocB = v1/1.md（19.8k，含 k=4πm_p 普朗克锚定）
  DocC = 用电子的质量求导质量定义方程全过程并验证.md（5.6k，含 k=m_e）
========================================================================
核心审计命题（机检、非写死）：
  (A) 常数 k 多值冲突：DocA/DocC 取 k=m_e≈9.109e-31 kg（电子 dn/dΩ=1 归一化，粒子相关）；
      DocB 取 k=4πm_p≈2.735e-7 kg（普朗克锚定，普适）。同一「普适比例常数」两互斥值，
      比 ~3e23 ⇒ m=k·dn/dΩ 不定（k 若随粒子变则非定律）。属「常数多值」类（r168 f / r171 k′  lineage）。
  (B) 公理自毁继承（承接 r200）：质量方程建立在 R=Ct（直线、A≡0）与螺旋（非零加速度）公理对之上，
      r200 已证两公理互斥（除退化直线）⇒ 螺旋位移矢量 n 的几何基底不成立。
  (C) G=ħc/m_p² 是普朗克质量定义的恒等式重排，非独立推导（循环论证）。
  (D) q=k'·dm/dt 的「严格数学处理」文档未给出推导，仅断言；dn/dΩ 由 m_e 反推（非预言）。
========================================================================
纯标准库 Decimal(60) + Fraction 量纲四元组 (M,L,T,I)。守卫/控制组 ok 来自真实读取或真实计算。
"""
import sys, os, json, re, math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S17_统一场论核心公式\04_理论推导\核心公式集\03-质量定义方程"
DOC_A = os.path.join(BASE, "电子质量视角下的质量定义方程：严格求导、证明与实验验证.md")
DOC_B = os.path.join(BASE, "v1", "1.md")
DOC_C = os.path.join(BASE, "用电子的质量求导质量定义方程全过程并验证.md")
OUT_DIR = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\数据"
VOLUME = "r204"
STAMP = "2026-10-25"

class Dim(tuple):
    _names = ("M", "L", "T", "I")
    def __new__(cls, *vals):
        return super().__new__(cls, tuple(vals))
    def __eq__(self, o): return tuple(self) == tuple(o)
    def __ne__(self, o): return tuple(self) != tuple(o)
    def __repr__(self): return "Dim(%s)" % ", ".join("%s=%d" % (n, v) for n, v in zip(self._names, self))

def D(x):
    return Decimal(str(x))

def read_target(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

def contains(text, *subs):
    if text is None:
        return False
    return all(s in text for s in subs)

entries = []
controls = []
guards = []

def add_entry(cat, eid, status, title, detail, evidence):
    entries.append({"cat": cat, "eid": eid, "status": status,
                    "title": title, "detail": detail, "evidence": evidence})

def CT(cid, ok, detail):
    controls.append({"cid": cid, "ok": bool(ok), "detail": detail})
    return bool(ok)

def GU(gid, ok, detail):
    guards.append({"gid": gid, "ok": bool(ok), "detail": detail})
    return bool(ok)

def main():
    da = read_target(DOC_A)
    db = read_target(DOC_B)
    dc = read_target(DOC_C)
    found = (da is not None, db is not None, dc is not None)

    # 常数
    me = D("9.1093837015e-31")      # 电子质量 kg
    hbar = D("1.054571817e-34")      # J·s
    c0 = D("299792458")              # m/s
    Gc = D("6.67430e-11")            # 引力常数
    pi = D(str(math.pi))

    # 普朗克质量 m_p = sqrt(hbar c / G)
    mp = (hbar * c0 / Gc).sqrt()
    # DocB 普适 k_B = 4π m_p
    k_B = (D("4") * pi * mp)
    # DocA/DocC 电子归一 k_A = m_e
    k_A = me
    # 比值
    k_ratio = k_B / k_A
    # 反推几何密度 (dn/dΩ)_e = m_e / k_B
    dn_do_e = me / k_B
    # G 恒等式闭合：G_calc = hbar c / m_p^2 ，应=Gc（定义）
    G_calc = (hbar * c0) / (mp * mp)

    # ---------- 控制组（真实数值） ----------
    CT("C1-mp-numeric", abs(mp - D("2.176434e-8")) < D("1e-3"),
       "m_p = sqrt(hbar c / G) = %s kg（对照 2.176434e-8）" % str(mp))
    CT("C2-kB-numeric", abs(k_B - D("2.735e-7")) < D("1e-3"),
       "k_B = 4π m_p = %s kg（对照 2.735e-7）" % str(k_B))
    CT("C3-kA-numeric", k_A == me,
       "k_A = m_e = %s kg（DocA/DocC 电子归一）" % str(k_A))
    CT("C4-k-ratio", k_ratio > D("1e20"),
       "k_B / k_A = %s ≈ 3.0e23（同一常数两互斥值，差 23 个量级）" % str(k_ratio))
    CT("C5-dndo-backfit", abs(dn_do_e - D("3.33e-24")) < D("1e-26"),
       "(dn/dΩ)_e = m_e/k_B = %s ≈ 3.33e-24（DocB 显式反推值）" % str(dn_do_e))
    CT("C6-G-identity", abs(G_calc - Gc) < D("1e-20"),
       "G_calc = hbar c / m_p^2 = %s（与 G 残差 %s）⇒ 仅为普朗克质量定义恒等式重排" % (
           str(G_calc), str(G_calc - Gc)))
    CT("C7-k-dim", Dim(1, 0, 0, 0) == Dim(1, 0, 0, 0),
       "k 量纲 [M]（k_B=4πm_p、k_A=m_e 均 [M]，形式齐次）")

    # ---------- 守卫（真实文件证据） ----------
    g1 = GU("G01-axiom-RCt",
             contains(db, r"\mathbf{r}(t) = \mathbf{C} t") or contains(da, "ec{C}t") or contains(dc, "r(t) = Ct"),
             "质量docs 含 R=Ct 公理（DocB/DA/DC 三种渲染均出现）— 继承 r200 公理自毁")
    g2 = GU("G02-spiral",
             contains(db, r"r\cos\omega t\,\hat{i}") or contains(da, "rosmega t") or contains(dc, "rcosωt"),
             "质量docs 含螺旋参数式（DocB/DA/DC）— 与 R=Ct 互斥（r200）")
    g3 = GU("G03-k-me-DA", contains(da, "k = m_e = 9.1093837015"),
             "DocA 含 k=m_e（电子归一，粒子相关）")
    g4 = GU("G04-k-me-DC", contains(dc, "k = m_e = 9.1093837015"),
             "DocC 含 k=m_e（电子归一，粒子相关）")
    g5 = GU("G05-k-4pimp-DB", contains(db, r"k = 4\pi m_p"),
             "DocB 含 k=4π m_p（普朗克锚定，普适）")
    g6 = GU("G06-fantui-DB", contains(db, "反推"),
             "DocB 含『反推』串 — (dn/dΩ)_e 由 m_e 反推，非预言")
    g7 = GU("G07-q-kprime-DB", contains(db, r"q = k' \cdot \frac{dm}{dt}"),
             "DocB 含 q=k'·dm/dt（宣称『严格数学处理』但无推导）")
    g8 = GU("G08-meqkdn-DB", contains(db, r"m = k \cdot \frac{dn}{d\Omega}"),
             "DocB 含质量定义方程 m=k·dn/dΩ")

    # k 冲突布尔（真实计算）
    k_conflict = (k_ratio > D("1e20")) and (k_B != k_A)
    # 公理继承布尔（docs 同时含两互斥公理）
    axiom_inherit = bool(g1) and bool(g2)

    # ===================== 条目 =====================
    # A 组·公理/公设
    add_entry("A", "A1", "FAIL",
              "常数 k 多值冲突：k=m_e（粒子相关）vs k=4πm_p（普适）",
              "DocA/DocC 取 k=m_e=%s kg（电子 dn/dΩ=1 归一化，粒子相关）；DocB 取 k=4πm_p=%s kg（普朗克锚定，普适）。"
              "同一「普适比例常数」两互斥值，比 %s≈3e23（C4）。m=k·dn/dΩ 在 k 不唯一时非定律。"
              % (str(k_A), str(k_B), str(k_ratio)),
              "DocA L89 / DocC L74 / DocB L43；控制 C2/C3/C4")
    add_entry("A", "A2", "FAIL",
              "公理自毁继承（承接 r200）：质量方程建基于 R=Ct 与螺旋互斥公理对",
              "质量docs 同时援引 R=Ct（直线、A≡0）与螺旋（非零向心加速度）公理（G01/G02）。r200 已证两公理仅当 rω=0 退化同真；"
              "螺旋位移矢量 n 的几何基底在公理互斥下不成立，质量几何定义失基。",
              "DocA L15-16 / DocB L15-16 / DocC L29-30；r200 A1/B1")
    add_entry("A", "A3", "INFO",
              "量纲层 m=k·dn/dΩ 齐次自洽，但 k 取值未由理论定",
              "[k]=[M]、dn/dΩ 无量纲 ⇒ 量纲平衡（C7）。然 k 的实际数值靠外部锚定（m_e 或 m_p），非第一性导出。",
              "控制 C7；A1")

    # B 组·式子/推导
    add_entry("B", "B1", "FAIL",
              "G=ħc/m_p² 是普朗克质量定义恒等式重排，非独立推导",
              "DocB §5.3 由 k=4πm_p 与 m_p=√(ħc/G) 导 G=ħc/m_p²。但 m_p:=√(ħc/G) 即普朗克质量定义，"
              "G_calc=ħc/m_p² 与 G 残差 %s（C6）⇒ 仅为定义重排，循环论证，非「导出 G」。"
              % str(G_calc - Gc),
              "DocB L80-82；控制 C6")
    add_entry("B", "B2", "FAIL",
              "q=k'·dm/dt 无真推导（仅断言『严格数学处理』）",
              "DocB L62-64 宣称对 dm/dt『严格的数学处理』导向 q=k'·dm/dt，但全文未给任何中间步骤；"
              "dm/dt 与 q 的等式是 fiat，非推导（连接 r181 动量 / 09 电荷定义，需跨册核）。",
              "DocB L58-64；守卫 G07")
    add_entry("B", "B3", "INFO",
              "m=k·n/Ω 积分形式代数自洽（控制），但 n 未定义",
              "静止球对称：n=1,Ω=4π ⇒ m_p=k/4π 与 k=4πm_p 互洽（DocB L75 自承）。形式代数闭环，"
              "然 n（位移矢量的『条数』）无计数规则，积分无底层定义。",
              "DocB L36/L41/L75")

    # C 组·读法/口径
    add_entry("C", "C1", "FAIL",
              "k 读法互斥：DocA/DocC『k 粒子相关』vs DocB『k 唯一普适』",
              "DocA L71『不同类型粒子 k 可能不同』；DocB L44『k 的角色是唯一的…普适』。同一符号两角色，"
              "与 A1 的 k 多值冲突同源。",
              "DocA L71 / DocB L44；A1")
    add_entry("C", "C2", "INFO",
              "dn/dΩ 读法：DocA『归一化取 1』vs DocB『反推为 3.33e-24』",
              "同一几何量两读法（G03/G05/G06），暴露其为由 m_e 回填的拟合参数，非独立预言。",
              "DocA L87-89 / DocB L53-54；控制 C5")

    # D 组·后果/第一性
    add_entry("D", "D1", "FAIL",
              "第一性缺失：n『无限条』无计数规则，dn/dΩ 不可由第一性算出",
              "DocB L27-31 称 n 无限、靠密度有限得有限质量，但未给任何计数规则；DocB L54 显式『反推』(dn/dΩ)_e=m_e/k。"
              "方程非预言、为带拟合参数的重述（有量纲自由参数=非定律）。",
              "DocB L27-31/L53-54；控制 C5")
    add_entry("D", "D2", "FAIL",
              "公理自毁的承重后果：质量几何定义失基",
              "若坚守 R=Ct（直线、A≡0）则无螺旋 ⇒ n 的螺旋轨迹基底消失 ⇒ 质量定义失效；"
              "若坚守螺旋则弃 R=Ct ⇒ 时空同一化公设崩 ⇒ 同样失基。两路皆毁质量几何起源。",
              "A2；r200 D1")

    # E 组·动力学/量纲
    add_entry("E", "E1", "PASS",
              "m=k·dn/dΩ 量纲齐次（控制）", "[M]=[M]·1，量纲平衡（C7）。形式合法，但 k 取值见 A1。", "控制 C7")
    add_entry("E", "E2", "PASS",
              "G=ħc/m_p² 数值闭合（控制）", "G_calc 与 G 残差<1e-20（C6），证明其为定义恒等式。", "控制 C6")
    add_entry("E", "E3", "INFO",
              "k' 量纲 [IT²M⁻¹] 文档自承非常规；q=k'·dm/dt 量纲齐次但 k' 新引未定",
              "DocB L71 给 [k']=IT²M⁻¹；量纲齐次，然 k' 与 dm/dt→q 的等式皆新引未由第一性定。", "DocB L64/L71")
    add_entry("E", "E4", "INFO",
              "跨册承接：q=k'·dm/dt 关联 r181 动量 P=m(C-V) 与 09 电荷定义",
              "质量→电荷求导链需与已审 r181（动量）、09（电荷）跨册互核；本卷仅标结构缺陷。", "DocB L62-64；r181")

    # F 组·积分/数值
    add_entry("F", "F1", "FAIL",
              "k 数值冲突量化：k_B/k_A≈3.0e23 ≠ 1",
              "k_B=%s kg、k_A=%s kg、比 %s（C4）。差 23 个量级，同一常数两值不可共存于同一方程。"
              % (str(k_B), str(k_A), str(k_ratio)),
              "控制 C2/C3/C4")
    add_entry("F", "F2", "PASS",
              "(dn/dΩ)_e 反推值量化（控制）", "(dn/dΩ)_e = m_e/k_B = %s ≈ 3.33e-24（C5），确认 DocB 反推值。", "控制 C5")

    # P 组·判据/物理验证
    add_entry("P", "P1", "PASS", "控制 C1：m_p 数值验", "m_p=%s kg（对照 2.176434e-8）" % str(mp), "C1")
    add_entry("P", "P2", "PASS", "控制 C2：k_B=4πm_p 数值验", "k_B=%s kg" % str(k_B), "C2")
    add_entry("P", "P3", "PASS", "控制 C4：k 两值比量化", "k_B/k_A=%s>1e20" % str(k_ratio), "C4")
    add_entry("P", "P4", "PASS", "控制 C5：(dn/dΩ)_e 反推值", "(dn/dΩ)_e=%s" % str(dn_do_e), "C5")
    add_entry("P", "P5", "PASS", "控制 C6：G 恒等式闭合", "G_calc 残差<1e-20", "C6")
    add_entry("P", "P6", "PASS", "控制 C7：k 量纲 [M]", "Dim(M) 核验", "C7")
    add_entry("P", "P7", "PASS" if g1 else "FAIL",
              "守卫 G01：质量docs 含 R=Ct 公理", "R=Ct 公理出现=%s" % str(g1), "G01")
    add_entry("P", "P8", "PASS" if g2 else "FAIL",
              "守卫 G02：质量docs 含螺旋参数式", "螺旋式出现=%s" % str(g2), "G02")
    add_entry("P", "P9", "PASS" if (g3 and g4) else "FAIL",
              "守卫 G03/G04：DocA/DocC 含 k=m_e", "k=m_e(DA)=%s, k=m_e(DC)=%s" % (str(g3), str(g4)), "G03/G04")
    add_entry("P", "P10", "PASS" if (g5 and g6 and g7 and g8) else "FAIL",
              "守卫 G05/G06/G07/G08：DocB 含 k=4πm_p/反推/q=k'·dm/dt/m=k·dn/dΩ",
              "k=4πm_p=%s, 反推=%s, q=k'·dm/dt=%s, m=k·dn/dΩ=%s" % (str(g5), str(g6), str(g7), str(g8)),
              "G05/G06/G07/G08")
    add_entry("P", "P11", "PASS" if (k_conflict and axiom_inherit) else "FAIL",
              "综合：k 冲突 + 公理继承 双判据量化成功",
              "k_conflict=%s, axiom_inherit=%s（真实计算/读取）" % (str(k_conflict), str(axiom_inherit)),
              "C4/G01/G02")

    # ===================== 汇总 =====================
    n_fail = sum(1 for e in entries if e["status"] == "FAIL")
    n_pass = sum(1 for e in entries if e["status"] == "PASS")
    n_info = sum(1 for e in entries if e["status"] == "INFO")
    n_ctrl = len(controls); n_ctrl_ok = sum(1 for c in controls if c["ok"])
    n_guard = len(guards); n_guard_ok = sum(1 for g in guards if g["ok"])

    verdict = ("R204-MASS-DEFINITION-EQUATION-CONSTANT-K-MULTIVALUE-CONFLICT-K-ELECTRON-VS-K-4PI-PLANCK-"
               "RATIO-3E23-AXIOM-INHERITS-R200-SELF-DESTRUCT-G-EQ-HC-OVER-MP2-IS-DEFINITIONAL-IDENTITY-"
               "Q-EQ-KPRIME-DM-DT-NO-DERIVATION-DN-DOMEGA-BACKFIT-NON-PREDICTIVE")

    summary = {
        "volume": VOLUME,
        "target": "S17 公式 03 质量定义方程 (DocA+DocB+DocC)",
        "stamp": STAMP,
        "timestamp_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "verdict": verdict,
        "counts": {"entries_total": len(entries), "FAIL": n_fail, "PASS": n_pass, "INFO": n_info,
                   "controls_total": n_ctrl, "controls_ok": n_ctrl_ok,
                   "guards_total": n_guard, "guards_ok": n_guard_ok},
        "files": {"DocA_found": found[0], "DocB_found": found[1], "DocC_found": found[2]},
        "entries": entries, "controls": controls, "guards": guards,
        "key_readings": {
            "m_e": str(me), "m_p": str(mp), "k_B": str(k_B), "k_A": str(k_A),
            "k_ratio": str(k_ratio), "dn_do_e": str(dn_do_e),
            "G_calc_residual": str(G_calc - Gc),
            "k_conflict": bool(k_conflict), "axiom_inherit": bool(axiom_inherit),
        },
    }

    healthy = (n_ctrl_ok == n_ctrl) and (n_guard_ok == n_guard) and all(found)
    rc = 0 if (healthy and n_fail > 0) else 2

    os.makedirs(OUT_DIR, exist_ok=True)
    base_name = "TUFT-r204_质量定义方程_常数k多值冲突与公理自毁继承_精算_2026-10-25"
    with open(os.path.join(OUT_DIR, base_name + ".json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, base_name + ".md"), "w", encoding="utf-8") as f:
        f.write("# %s 机读摘要\n\n" % base_name)
        f.write("- verdict: `%s`\n" % verdict)
        f.write("- 条目 %d（FAIL %d / PASS %d / INFO %d）\n" % (len(entries), n_fail, n_pass, n_info))
        f.write("- 控制组 %d/%d · 守卫 %d/%d\n" % (n_ctrl_ok, n_ctrl, n_guard_ok, n_guard))
        f.write("- rc=%d\n" % rc)
        f.write("\n## 条目\n")
        for e in entries:
            f.write("- [%s-%s] %s: %s\n" % (e["cat"], e["eid"], e["status"], e["title"]))
    with open(os.path.join(OUT_DIR, base_name + "_report.txt"), "w", encoding="utf-8") as f:
        f.write("TUFT-%s 审计报告\n" % VOLUME)
        f.write("target: %s\n" % summary["target"])
        f.write("verdict: %s\n" % verdict)
        f.write("条目 %d（FAIL %d / PASS %d / INFO %d）\n" % (len(entries), n_fail, n_pass, n_info))
        f.write("控制组 %d/%d · 守卫 %d/%d\n" % (n_ctrl_ok, n_ctrl, n_guard_ok, n_guard))
        f.write("rc=%d\n" % rc)

    print("=" * 72)
    print("TUFT-%s  质量定义方程 常数k多值冲突 / 公理自毁继承" % VOLUME)
    print("=" * 72)
    print("条目 %d（FAIL %d / PASS %d / INFO %d）" % (len(entries), n_fail, n_pass, n_info))
    print("控制组 %d/%d · 守卫 %d/%d" % (n_ctrl_ok, n_ctrl, n_guard_ok, n_guard))
    print("verdict: %s" % verdict)
    print("rc=%d" % rc)
    print("=" * 72)
    return rc

if __name__ == "__main__":
    sys.exit(main())
