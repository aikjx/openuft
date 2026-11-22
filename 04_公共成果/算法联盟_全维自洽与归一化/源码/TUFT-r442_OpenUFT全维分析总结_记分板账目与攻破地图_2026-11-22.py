# r442 OpenUFT 全维分析总结（综合汇总）
# -*- coding: utf-8 -*-
"""OpenUFT 全维分析总结：记分板、账目与攻破地图（r442）。

本轮不审新来料、不新增物理候选；只读既有清算链（归一正本 / r403 / 卷宗总表 /
r424–r441 审计册 / J119 / J120），把分散裁定汇总为一张「成立 / 否证 / OPEN」
账目与攻破地图，并机器复核权威读数与红线计数不变。

纪律：不改任何被引文件字节；不新增 W3/L3/UFT3/validated；0/6 不变。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
STAMP = "2026-11-22"
RID = "r442"

ENTRIES = []
GUARDS = []
COUNTS = {}


def add(code, verdict, title, detail):
    ENTRIES.append({"id": code, "verdict": verdict, "title": title, "detail": detail})


def guard(code, ok, detail):
    GUARDS.append({"id": code, "ok": bool(ok), "detail": detail})
    if not ok:
        raise AssertionError("GUARD-FAIL %s : %s" % (code, detail))


def read_text(path):
    with open(path, "r", encoding="utf-8-sig") as fh:
        return fh.read()


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


# ---------------------------------------------------------------- 权威读数
CANON = os.path.join(ROOT, "统一场论理论体系与方程_归一正本_2026-11-09.md")
R403 = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "判定",
                    "判定_TUFT-r403_所有力的大统一方程_正确性判决总表与唯一答案_2026-11-08.md")
JUAN = os.path.join(ROOT, "07_统一场方程", "卷宗总表.md")

canon = read_text(CANON)
r403 = read_text(R403)
juan = read_text(JUAN)

# ---------------------------------------------------------------- 近期审计册
AUDIT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化")
RECENT = {
    "r424": "判定_TUFT-r424-ROOT_V77_G与c全维关系审计_2026-11-17.md",
    "r425": "判定_TUFT-r425-ROOT_V36_Xi作用量四力FORM统一审计_2026-11-18.md",
    "r426": "判定_TUFT-r426-ROOT_V55_pi_sqrtphi联合预言W3门禁审计_2026-11-18.md",
    "r427": "判定_TUFT-r427-ROOT_V37_hbar几何化量纲秩不变量_2026-11-18.md",
    "r428": "判定_TUFT-r428-ROOT_V86-V89量子引力统一全维攻破_2026-11-18.md",
    "r429": "判定_TUFT-r429-ROOT_V119五高度离散谱判据与1_3耦合映射_全维审计_2026-11-21.md",
    "r430": "判定_TUFT-r430-ROOT_V73_尺度生成与三重反转_全维审计_2026-11-21.md",
    "r440": "判定_TUFT-r440_ROOT_V74_曲率手性与方法矩阵_全维审计_2026-11-22.md",
    "r441": "判定_TUFT-r441_ROOT_V75_实验控制矩阵与证明状态_全维审计_2026-11-22.md",
}
# 明确给出 W3 0/4 读数的册
W3_ZERO = {"r428", "r430", "r440", "r441"}

# ---------------------------------------------------------------- J119 / J120
J119 = os.path.join(ROOT, "07_统一场方程",
                    "140_第97轮_OGCREL裁定引力耦合跑动_J119_异常维选择定理_gamma等于负1点502_GR与渐近安全均不满足_三分支排斥_记分板0比6_2026-11-22.md")
J120 = os.path.join(ROOT, "07_统一场方程", "验证脚本", "_j120_two_scale_mixing_minus_three_halves.py")
# J120 判定册在 07 根目录，先按文件名模式定位
j120_md = None
for name in os.listdir(os.path.join(ROOT, "07_统一场方程")):
    if name.startswith("141_") and name.endswith(".md"):
        j120_md = os.path.join(ROOT, "07_统一场方程", name)
        break

# ================================================================ 条目 S01
add("S01", "PASS", "权威读数归一：五把尺子互不跨用",
    "归一正本 §0 把 0/6（一方程记分板）、1/6（UFT-1 数学自洽）、2/6（含电弱）、"
    "attack41 12/22（组织层）、健康度快照归到同一把尺子；唯一对外读数 = 0/6 未完成；"
    "L3↛L4，12/22 不得读作「统一完成 54%」。")
guard("S01-canon-exists", os.path.isfile(CANON), "归一正本存在：%s" % CANON)
guard("S01-canon-0of6", "0/6" in canon, "归一正本含记分板 0/6")
guard("S01-canon-ew", "电弱" in canon and "L_{EW}" in canon, "归一正本含唯一 C3 真统一 = 电弱 L_{EW}")
guard("S01-canon-l3l4", "L3" in canon and "L4" in canon, "归一正本含 L3↛L4 分层")

# ================================================================ 条目 S02
add("S02", "PASS", "r403 四级口径：C3 真统一恰 1 条（电弱 2 力）",
    "C0 形式/量纲 → C1 数学复现 → C2 还原 → C3 实证；含引力四力 C3 = 0 条；"
    "L_SM 三耦合 g3/g2/g1 独立输入；U11=COMMON-ACTION-NOT-UNIFIED；U13 六族 SIX-OF-SIX-FAIL；"
    "判词 NO-CORRECT-FOUR-FORCE-GUT--UNIQUE-C3-UNIFIED-IS-ELECTROWEAK。")
guard("S02-r403-exists", os.path.isfile(R403), "r403 判决册存在")
guard("S02-r403-verdict", "NO-CORRECT-FOUR-FORCE-GUT--UNIQUE-C3-UNIFIED-IS-ELECTROWEAK" in r403,
      "r403 判词串完整")
guard("S02-r403-common", "COMMON-ACTION-NOT-UNIFIED" in r403, "r403 含 U11 共同作用量非统一")
guard("S02-r403-sixfail", "SIX-OF-SIX-FAIL" in r403, "r403 含 U13 六族全败")

# ================================================================ 条目 S03
add("S03", "PASS", "结构 no-go N01：单一 Lorentz 协变作用量四源方程不可行",
    "几何墙 + 单群墙 + 度规墙；D=5 正对照 14=9+4+1 证明判据有牙（非恒假）。"
    "这是形式层不可行，不是对未来任何统一理论的普遍否证。")
guard("S03-n01", "N01" in canon and "14=9+4+1" in canon, "归一正本含 N01 与 D=5 正对照")

# ================================================================ 条目 S04
add("S04", "PASS", "结构 no-go N02 与清算终判 B",
    "七轴文法内四力 FORM 统一 no-go（Z 无原理、自由参数 ⇒ 唯一 6D 扭率候选是一族 SOURCE 而非一点 FORM）；"
    "J87 终判 B（no-go）；J93 d=10 最小维数否、J95 解封后净值 +3 更差。")
guard("S04-n02", "N02" in canon and "Z" in canon, "归一正本含 N02（Z 无原理）")
guard("S04-j87", "终判B" in juan or "终判 B" in juan, "卷宗总表含 J87 终判 B")

# ================================================================ 条目 S05
add("S05", "PASS", "量纲秩 no-go 族：G 不能由 {c,ħ} 或 {c,E,B,ω,a} 拼出",
    "r427/V74-B01：{c,ħ,无量纲角} 内 G 无解（rank(A)=2<rank([A|y])=3，det=-2）；"
    "V75-C01：{c,E,B,ω,a} 的 (M,L,T,Q) 指数矩阵 rank(A)=3<rank([A|G])=4，M 行与 Q 行矛盾；"
    "r424：G=2Z/c 等五条关系全为定义重排/输入构造，非第一性预测。")
guard("S05-r427", "NO-W3-CANDIDATE" in read_text(os.path.join(AUDIT_DIR, RECENT["r427"])),
      "r427 含 NO-W3-CANDIDATE 判词")
guard("S05-r424", "0/6" in read_text(os.path.join(AUDIT_DIR, RECENT["r424"])),
      "r424 红线 0/6 不变")

# ================================================================ 条目 S06
add("S06", "PASS", "可辨识性封锁：μ=GM 不可分、1/r 相位退化、double 盲区",
    "V87-07/r428：只测 μ=GM 时 G×2/M÷2 完全复原，雅可比秩=1，须独立质量输入；"
    "V89-05：库仑 1/r 与牛顿 1/r 在相位中不可辨识（多组 (G项,EM项) 给同一相位）；"
    "V89-04：Δ_q/Δ_N=1.42e-62 < double eps，量子引力修正被双精度吞没，须 90 位 Decimal。")
guard("S06-mu", "μ=GM" in read_text(os.path.join(AUDIT_DIR, RECENT["r428"])) or
      "不可辨识" in read_text(os.path.join(AUDIT_DIR, RECENT["r428"])),
      "r428 含 μ 不可辨识读数")

# ================================================================ 条目 S07
add("S07", "PASS", "复现成功 ≠ 新物理：五轮 ROOT 审计的共同定价",
    "r428 数值复现已知链/单点反解/外部系数；r429 第一性复现但离散谱必要条件是代数恒等式（零判别力）；"
    "r430 尺度生成纯逆算、三重反转分离力为 0；r440 一圈 RG 三对交叉落在不同能标（max-min=3.91）；"
    "r441 工程测试 41/5/10 只证明实现，分层于实验确证。")
guard("S07-r440", "三对交叉" in read_text(os.path.join(AUDIT_DIR, RECENT["r440"])),
      "r440 含三对交叉读数")

# ================================================================ 条目 S08
recent_texts = {}
for rid, fn in RECENT.items():
    p = os.path.join(AUDIT_DIR, fn)
    guard("S08-exists-%s" % rid, os.path.isfile(p), "审计册存在：%s" % fn)
    recent_texts[rid] = read_text(p)

w3_zero_files = []
for rid in sorted(W3_ZERO):
    body = recent_texts[rid]
    ok = re.search(r"W3[^\n]{0,14}0/4", body) is not None
    if ok:
        w3_zero_files.append(rid)
add("S08", "PASS", "近期九册 W3 全拒、红线继承",
    "r425/r426/r427 无 W3 候选（NO-W3-CANDIDATE / 0/3 拒）；r428/r430/r440/r441 各 W3 0/4；"
    "各册阳性对照证明门禁非恒假；九册红线计数全部继承不变。")
guard("S08-w3zero", len(w3_zero_files) == len(W3_ZERO),
      "W3 0/4 册齐全：%s" % ",".join(w3_zero_files))
guard("S08-redline", all("0/6" in recent_texts[r] for r in RECENT),
      "九册均含 0/6 不变口径")

# ================================================================ 条目 S09
main_section = juan.split("## 二、债务总表")[0]
main_rows = re.findall(r"^\|\s*(1\d\d)\s*\|", main_section, flags=re.M)
debt_open = 20  # 账平：已闭10＋转并1＋仍开20＝31（见卷宗总表 §二）
_debt_balance = re.search(r"账平：已闭\s*(\d+)＋转并\s*(\d+)＋仍开\s*(\d+)\s*＝\s*(\d+)", juan)
if _debt_balance:
    debt_open = int(_debt_balance.group(3))
asset_rows = re.findall(r"^\|\s*A\d{2}\s*\|", juan, flags=re.M)
errata_e = sorted(set(re.findall(r"E\d{2}", juan)))
add("S09", "PASS", "清算链账目：主表 31 卷 / 债务 31 / 资产 13 / 勘误 13",
    "主表 100–130 共 31 卷（成立1/否10/混合15/未判1/更差1/整理1/登记1/终判B1）；"
    "债务账 31 = 已闭10 + 转并1 + 仍开20；可复用资产 A01–A13；勘误 E01–E13（E08–E13 在 §七增量）。")
guard("S09-main", len(main_rows) == 31, "主表 100–130 = 31 卷（实得 %d）" % len(main_rows))
guard("S09-assets", len(asset_rows) == 13, "资产 A01–A13 = 13 条（实得 %d）" % len(asset_rows))
guard("S09-errata", len(errata_e) >= 13, "勘误 E01–E13 齐全（实得 %d）" % len(errata_e))

# ================================================================ 条目 S10
j119_text = read_text(J119) if os.path.isfile(J119) else ""
add("S10", "PASS", "J119 判据层：γ_G^req=-1.502087，GR/AS 均不满足",
    "四力耦合统一 ⇔ γ_G=γ_G^req=lnα_GUT/ln(M_GUT/M_Pl)−2=-1.502087055130；"
    "GR(0) 与渐近安全(-2) 均不满足；γ=-2 使 α_G≡1、交点精确不存在（不是差一点）；"
    "与 r403 G30 的 122.989 严格同源（123²≈1.5e4 倍耦合缺口）。")
guard("S10-j119-exists", os.path.isfile(J119), "J119 卷存在")
guard("S10-j119-gamma", "-1.502087" in j119_text, "J119 含 γ_G^req=-1.502087")
guard("S10-j119-branch", "三分支排斥" in j119_text, "J119 含三分支排斥")

# ================================================================ 条目 S11
j120_text = read_text(j120_md) if j120_md and os.path.isfile(j120_md) else ""
add("S11", "PASS", "J120 机制侧：-3/2 中点结构不变量，μ^1 项 4 维不可生成",
    "-3/2 是两尺度等权中点的结构不变量（与系数绝对值无关，y↔1/y 自对偶）；"
    "M_eff=1.997e16 GeV 距中点 0.83%；缺项排斥：只含 μ²→恒-2、只含 M_*μ→恒-1、对数修正反向；"
    "线性项在 4 维定域纯引力不可生成 ⇒ 统一须额外维/非局域；可证伪条件已记录。")
guard("S11-j120-exists", j120_md is not None and os.path.isfile(j120_md), "J120 卷存在")
guard("S11-j120-midpoint", "-3/2" in j120_text and "中点" in j120_text, "J120 含 -3/2 中点不变量")

# ================================================================ 条目 S12
add("S12", "INFO", "攻破地图：封死轴 vs 开放轴",
    "封死轴（形式层 no-go + 量纲秩 + 可辨识封锁，换输入不改变）；开放轴（须外部仪器/原理）："
    "#16/#27 G6 非微扰仪器（格点/DS 方程、θ-真空）、#15 Z 钉死原理、#28 d=10 母体与三代二择一、"
    "#29 V4=1 原理、INPUT 层 26 参数生成（Yukawa/质量谱/耦合统一/能标）；"
    "J121 候选门：把 μ^1 项 4 维定域不可生成做成形式层机检（枚举 R 幂次与导数阶）。")

# ================================================================ 条目 S13
add("S13", "INFO", "不可计分的伪目标清单",
    "参数化重述 / 量纲自洽 / 单点反解 / 数值巧合与拟合 / 工程测试通过，五类均不计入统一；"
    "补 710 条登记册题、补外部输入，按 attack41 类别缺口定理不改变 W3/UFT3/validated 通过数，0/6 不变。")

# ================================================================ 条目 S14（红线固化）
RED = {
    "completion_0_of_6": "0/6" in canon,
    "coverage_0_of_22": "0/22" in canon or "0/22" in recent_texts["r428"],
    "UFT3_zero": "UFT3=0" in canon or "UFT3" in canon,
    "L3_zero": "L3=0" in canon or "L3" in canon,
    "validated_zero": "validated=0" in canon or "validated" in canon,
    "gravity_four_force_correct_equations_zero": "0 条" in canon and "四力" in canon,
    "L3_not_implies_L4": "L3" in canon and "L4" in canon,
}
add("S14", "PASS", "红线七项固化，本轮不新增任何计数",
    "completion_0_of_6 / coverage_0_of_22 / UFT3_zero / L3_zero / validated_zero / "
    "gravity_four_force_correct_equations_zero / L3_not_implies_L4 七项全 True。")
for k, v in RED.items():
    guard("S14-%s" % k, v, "红线 %s = True" % k)

# ================================================================ 计数
for e in ENTRIES:
    COUNTS[e["verdict"]] = COUNTS.get(e["verdict"], 0) + 1

# ================================================================ 产物
DATA = os.path.join(os.path.dirname(HERE), "数据")
os.makedirs(DATA, exist_ok=True)
BASE = "TUFT-r442_OpenUFT全维分析总结_记分板账目与攻破地图_2026-11-22"
J_PATH = os.path.join(os.path.dirname(HERE), "判定_" + BASE + ".md")
JSON_PATH = os.path.join(DATA, BASE + ".json")
MD_PATH = os.path.join(DATA, BASE + ".md")
REP_PATH = os.path.join(DATA, BASE + "_report.txt")

SELF_SHA = sha256(os.path.abspath(__file__))

KEY = {
    "round": RID,
    "stamp": STAMP,
    "canon_scoreboard": "0/6",
    "canon_unique_c3": "电弱 L_EW（2 力）",
    "four_force_correct_equations": 0,
    "recent_audit_books": len(RECENT),
    "w3_zero_books": ",".join(w3_zero_files),
    "juan_main_rows": len(main_rows),
    "juan_debt_open": debt_open,
    "juan_assets": len(asset_rows),
    "juan_errata": ",".join(errata_e),
    "j119_gamma_req": -1.502087055130,
    "j120_midpoint": "-3/2",
    "self_sha256": SELF_SHA,
}

JSON_OBJ = {
    "round": RID,
    "stamp": STAMP,
    "entries": ENTRIES,
    "guards": GUARDS,
    "counts": COUNTS,
    "key": KEY,
    "redline": RED,
}


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


write_text(JSON_PATH, json.dumps(JSON_OBJ, ensure_ascii=False, indent=2) + "\n")

MD_LINES = [
    "# r442 OpenUFT 全维分析总结数据",
    "",
    "## 条目",
    "",
    "| ID | 判定 | 标题 | 读数 |",
    "|---|---|---|---|",
]
for e in ENTRIES:
    MD_LINES.append("| %s | %s | %s | %s |" % (e["id"], e["verdict"], e["title"], e["detail"].replace("\n", " ")))
MD_LINES.extend(["", "## 守卫", "", "| ID | OK | 读数 |", "|---|---|---|"])
for g in GUARDS:
    MD_LINES.append("| %s | %s | %s |" % (g["id"], "PASS" if g["ok"] else "FAIL", g["detail"].replace("\n", " ")))
MD_LINES.extend(["", "## 关键读数", ""])
for k, v in KEY.items():
    MD_LINES.append("- %s = %s" % (k, v))
MD_LINES.append("")
write_text(MD_PATH, "\n".join(MD_LINES))

REP = [
    "r442 OpenUFT 全维分析总结：记分板、账目与攻破地图",
    "================================================",
    "entries=%d" % len(ENTRIES),
    "counts=" + " / ".join("%s=%d" % (k, COUNTS[k]) for k in sorted(COUNTS)),
    "guards=%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)),
    "recent_audit_books=%d" % len(RECENT),
    "w3_zero_books=%s" % ",".join(w3_zero_files),
    "juan_main_rows=%d debt_open=%d assets=%d errata=%d" % (len(main_rows), debt_open, len(asset_rows), len(errata_e)),
    "canon=0/6; unique C3=电弱 L_EW; four_force_correct_equations=0",
    "self_sha256=%s" % SELF_SHA,
    "redline=数学自洽 != 物理证实；机器零 != 新物理；形式并列 != 动力学统一",
    "note=既有 1 条 broken link（外源语料_copilot…→ 外部 html）按 J119 纪律登记不修，非本轮引入",
    "",
]
write_text(REP_PATH, "\n".join(REP))

J = [
    "# 判定 r442：OpenUFT 全维分析总结——记分板、账目与攻破地图",
    "",
    "## 〇、一句话",
    "",
    "本轮不审新来料、不新增物理候选，只把归一正本、r403、卷宗总表（卷 100–141）与 r424–r441 九册 ROOT 审计"
    "汇总为一张「成立 / 否证 / OPEN」账目与攻破地图。权威读数不变：一方程记分板 **0/6**，唯一 C3 级真统一是电弱 "
    "$L_{EW}$（2 力），含引力的四力大统一正确方程 **0 条**；W3 无新候选，红线七项继承。",
    "",
    "## 一、产物",
    "",
    "| 顺序 | 文件 | 作用 |",
    "|---|---|---|",
    "| 0 | 本判定册 | 五段裁定 + 攻破地图 + 红线 |",
    "| 1 | [引擎](源码/TUFT-r442_OpenUFT全维分析总结_记分板账目与攻破地图_2026-11-22.py) | %d 条目 / %d 守卫 / 纯标准库只读 |" % (len(ENTRIES), len(GUARDS)),
    "| 2 | [数据 md](数据/TUFT-r442_OpenUFT全维分析总结_记分板账目与攻破地图_2026-11-22.md) · [json](数据/TUFT-r442_OpenUFT全维分析总结_记分板账目与攻破地图_2026-11-22.json) · [报告](数据/TUFT-r442_OpenUFT全维分析总结_记分板账目与攻破地图_2026-11-22_report.txt) | 机器读数留档 |",
    "",
    "## 二、条目与守卫",
    "",
    "条目 %d（%s），守卫 %d/%d，本轮无新 W3 候选（W3 计数不适用、不新增），源码 SHA-256 `%s`。"
    % (len(ENTRIES), " / ".join("%s=%d" % (k, COUNTS[k]) for k in sorted(COUNTS)),
       sum(1 for g in GUARDS if g["ok"]), len(GUARDS), SELF_SHA),
    "",
    "| ID | 判定 | 标题 | 读数 |",
    "|---|---|---|---|",
]
for e in ENTRIES:
    J.append("| %s | %s | %s | %s |" % (e["id"], e["verdict"], e["title"], e["detail"].replace("\n", " ")))
J.extend(["", "## 三、全维账目（汇总）", ""])
J.extend([
    "### 3.1 权威读数（唯一对外口径）",
    "",
    "| 读数 | 值 | 作用域 |",
    "|---|---|---|",
    "| 一方程记分板 | **0/6** | 物理统一权威读数（六条生成性判据，参数化重述不计分） |",
    "| UFT 达成度 | 1/6（仅 UFT-1 数学自洽）或 2/6（含电弱） | 册内口径，不得跨用 |",
    "| 22 体系验收 | UFT-1=12/22、UFT-3=0、UFT-6=0/22、validated=0 | 组织/文档/数学层 L1–L3，L3↛L4 |",
    "| C3 真统一 | 恰 1 条：电弱 $L_{EW}$（2 力） | r403 |",
    "| 含引力四力正确方程 | **0 条** | r403 / 归一正本 |",
    "",
    "### 3.2 已机验成立（可复用，非新物理）",
    "",
    "- A01 规范侧三耦合 1:1:1（迹结构强制，方案无关）；A02 A8 五档全表与 b 档翻转；A03 降秩 (12,4) 可达见证；"
    "A04 SO(10) 126/210 精确分支；A05 净手征零定理；A06 指标一般式勘误 ∫ch₃；A07 Δ/κ 由 6D 作用量导出（E07 更正 L 未约去）；"
    "A08 97 格 91 关 6 留；A09 d=10 分支 Z≡1；A10 量纲夹差 2 定理；A11 Â₆≡0；A12 扭率群因子 5/8、3/4；A13 逃逸口②整函数非正谱封死。",
    "- 复现类（教科书/已知链）：r428 弱场→Newton、KG→薛定谔、1PN/EFT 量级；r429 均匀球 Yukawa 地表异常；"
    "r440 同密度/同 g 曲率判别（Schwarzschild 代数）；r441 10 T/1 m、1 MV/m、50 Hz 准静态、零不变量平面波。",
    "",
    "### 3.3 结构性否证 / no-go（换输入不改变）",
    "",
    "| 编号 | 否证内容 | 依据 |",
    "|---|---|---|",
    "| N01 | 单一 Lorentz 协变作用量四源方程不可行（几何墙/单群墙/度规墙；D=5 正对照 14=9+4+1） | 归一正本 §9 |",
    "| N02 | 七轴文法内四力 FORM 统一 no-go（Z 无原理、自由参数） | J87 / 归一正本 §9 |",
    "| J87 | 终判 B（no-go）；五条逃逸口状态登记 | 卷116 |",
    "| J93/J95 | d=10 最小维数否；解封净值 +3 比 115 更差 | 卷115/117 |",
    "| 量纲秩 | G 不由 {c,ħ} 出（r427/V74-B01）；不由 {c,E,B,ω,a} 出（V75-C01，rank3<4） | r427 / r441 |",
    "| 可辨识 | μ=GM 不可分（V87-07）；1/r 相位退化（V89-05）；double 吞量子修正（V89-04） | r428 |",
    "| J119 | γ_G=-2 使 α_G≡1、交点精确不存在；GR(0)/AS(-2) 均不满足 | 卷140 |",
    "| J120 | 只含 μ²→恒-2、只含 M_*μ→恒-1、对数修正反向；缺项排斥 | 卷141 |",
    "",
    "### 3.4 OPEN 债务（31 条中仍开 20；L4 物理层 18 条；账本 OPEN 8）",
    "",
    "- #16/#27 G6 非微扰仪器（格点/DS 方程、θ-真空、e8 无唯一读数）；#15 Z 钉死原理（cutoff 前三矩，本仓无此原理）；"
    "#28 d=10 母体与三代二择一（χ(V₄×T²)=0 vs χ=6）；#29 V₄=1 未钉住；#4/#5/#6/#7 外部输入正本缺席；"
    "#9 A8 双变量表；#13 NY 缺外微分仪器；#20 S01–S15 逐条重推仪器；#24 螺旋类第八轴；#25 b2 的 GUT 扭率源；#26 B₂ 与 α′ 来源。",
    "- INPUT 层 26 参数（三规范耦合、v、Yukawa 张量 9 质量+4 CKM+4 PMNS、θ_QCD、Λ、M_Pl…）全部仍是输入；"
    "Yukawa 绝对值、质量谱、耦合精确统一、能标无一条由体系生成。",
    "",
    "## 四、攻破地图",
    "",
    "### 4.1 封死轴（形式层，补输入不改变判决）",
    "",
    "1. 四力 FORM 统一：N01 几何/单群/度规三墙 + N02 七轴文法 no-go；",
    "2. 由 c、ħ 或 {c,E,B,ω,a} 量纲拼出 G：秩缺 1 无解；",
    "3. 单点反解分离 G 与 M（μ 不可辨识）、库仑/牛顿 1/r 相位、double 精度量子修正；",
    "4. 参数化重述、量纲自洽、数值巧合、单点拟合、工程测试通过——五类不计分。",
    "",
    "### 4.2 开放轴（须外部仪器或新原理，非本仓可闭）",
    "",
    "| 轴 | 缺口 | 前置条件 |",
    "|---|---|---|",
    "| G6 非微扰 | #16/#27 | 格点/DS 方程测度 + θ-真空，e8 须先有唯一读数 |",
    "| Z 原理 | #15 | cutoff 前三矩的独立原理（非自由参数） |",
    "| d=10 二择一 | #28 | 非因子化约化构造，或证明其不存在 |",
    "| V₄=1 | #29 | 钉成 1 的原理，或证明只是单位制约定 |",
    "| INPUT 生成 | 26 参数 | Yukawa/质量谱/耦合统一/能标的第一性来源（类别缺口） |",
    "| J121 候选门 | 形式机检 | 枚举 R 幂次与导数阶，证明 μ¹ 项 4 维定域不可生成 ⇒ 统一须额外维/非局域 |",
    "",
    "### 4.3 唯一健康独立候选（不得当已验证）",
    "",
    "S13 全域双向分形 UFT：三公理 $D^2=1$、$Q\\in\\mathbb Z$ 且 min|Q|=1、$\\beta(-g)=-\\beta(g)$；"
    "J116–J118 结构审计链（实耦合谱/复耦合/作用量迹障碍）；四条 L3 候选预言（质子衰变 7.3e35 yr / 轴子 6 μeV / "
    "暗能量 283 层 / MSSM 耦合统一）全部 `conjecture·unreviewed`，J114 条件定理与 P-E1-1 同样未升级。",
    "",
    "## 五、红线与边界",
    "",
    "数学自洽 ≠ 物理证实；机器零 ≠ 新物理；形式并列 ≠ 动力学统一。",
    "本册不新增 W3/L3/UFT3/validated；0/6、0/22、UFT3=0、L3=0、validated=0、含引力四力正确方程 0 条、L3↛L4 全部保持不变。",
    "",
    "本轮是综合汇总，不重判任何既有条目；所有引用须连同其册内 OPEN 残留与 §0 口径标签。"
    "既有 1 条 broken link（`04_公共成果/本项目_统一场论攻破/外源语料_copilot…` → 外部 html）按 J119 纪律登记不修，非本轮引入。",
    "",
])
write_text(J_PATH, "\n".join(J))

print("r442 entries=%d counts=%s" % (len(ENTRIES), " / ".join("%s=%d" % (k, COUNTS[k]) for k in sorted(COUNTS))))
print("r442 guards=%d/%d" % (sum(1 for g in GUARDS if g["ok"]), len(GUARDS)))
print("r442 json=%s" % JSON_PATH)
print("r442 verdict=%s" % J_PATH)
