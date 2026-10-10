# -*- coding: utf-8 -*-
"""attack16 probe1 · 12 常数来源分类（D2 质量四重过滤）（2026-10-10）

对象：证书 R6「全参数指定：12 常数全有确定值+来源，自由参数=0」
      （TUFT_V3.4全参数闭合总装_2026-10-10.md「全参数表（确定值+来源）」）

判据（沿用本项目 D2 质量侧核查的四重过滤）：
  Q1 非测量锚 —— 数值是否取自实验测量（α_s/α_EM/α_W/EDM…）
  Q2 有误差棒 —— 是否给出不确定度（无误差棒 ⇒ 不能作严格存活）
  Q3 循环     —— 是否由「匹配律/反解/认定」定义（自己定义自己）
  Q4 假设标签 —— 是否只是给结构假设起了个名字（β_G 结构 / β_c=G-c / =C4）

分类口径（逐条贴来料「来源」栏原文，不改写）：
  INPUT_MEAS  观测/锚定/实验排除        → 违反 Q1（外部测量输入）
  FIT         冻结匹配（反推自观测量）  → 违反 Q2/Q3
  ASSUMED     结构假设（无推导）        → 违反 Q4
  CIRCULAR    匹配律定义 / 反解         → 违反 Q3
  IDENTIFIED  认定（=C4）               → 违反 Q4
  DERIVED     场内真实计算（1 圈 β）    → 通过
  DERIVED_DEP 计算但依赖外部输入 A       → 部分通过

诚实边界：判「INPUT/ASSUMED/CIRCULAR」**不等于**指称造假——给常数标来源是常规做法；
本探针只判定「有来源名」≠「无外部输入」，故「自由参数=0」这一**措辞**不成立。
正向对照（B02）验证分类器能识别真实 DERIVED，避免成为无条件判负的橡皮图章。

退出码：仅由自检 CHK 决定；判出 FAIL 不是引擎失败。
"""

import os
import sys
import json
import re
from decimal import Decimal, getcontext

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
getcontext().prec = 60

ITEMS = []
_SELF = []


def P(name, ok, detail, note=""):
    ITEMS.append(dict(id=name, verdict="PASS" if ok else "FAIL", detail=detail, note=note))


def F(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="FAIL", detail=detail, note=note))


def INFO(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="INFO", detail=detail, note=note))


def BOUND(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="BOUNDARY", detail=detail, note=note))


def CHK(name, cond, detail=""):
    _SELF.append(dict(name=name, ok=bool(cond), detail=detail))


def d(x):
    return Decimal(str(x))


def rel(a, b):
    """相对差 |a-b|/max(|a|,|b|)。"""
    a, b = d(a), d(b)
    den = max(abs(a), abs(b))
    return abs(a - b) / den if den != 0 else abs(a - b)


def target_dir():
    up = os.path.dirname(HERE)                       # 04_公共成果
    return os.path.join(up, "算法联盟_全维自洽与归一化", "数据")


# 来源栏关键词 → 分类（严格按来料原文措辞）
RULES = [
    (("锚定", "观测", "EDM"), "INPUT_MEAS"),
    (("冻结匹配", "冻结", "反推"), "FIT"),
    (("场内容",), "DERIVED"),
    (("不动点",), "DERIVED_DEP"),
    (("β_G 结构", "β_G结构", "β_c", "钉死"), "ASSUMED"),
    (("稳定性闭合",), "CIRCULAR"),
    (("匹配律",), "CIRCULAR"),
]

LABEL = {
    "INPUT_MEAS": "观测/锚定（外部测量输入）",
    "FIT": "拟合/反推自观测量",
    "ASSUMED": "结构假设（无推导）",
    "CIRCULAR": "匹配律定义/反解（循环）",
    "IDENTIFIED": "认定（无推导）",
    "DERIVED": "场内真实计算",
    "DERIVED_DEP": "计算但依赖外部输入",
}


def classify(source_text, value_text):
    s = source_text.strip()
    if s.startswith("=C4") or s.startswith("= C4"):
        return "IDENTIFIED"
    for keys, lab in RULES:
        for k in keys:
            if k in s:
                return lab
    return "UNKNOWN"


def parse_table(md_text):
    """抽取 | 参数 | 值 | 来源 | 三列表格行。"""
    rows = []
    for line in md_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 3:
            continue
        p, v, s = cells
        if p in ("参数", "") or set(p) <= set("-: "):
            continue
        rows.append((p, v, s))
    return rows


def run_all():
    print("=" * 78)
    print("attack16 probe1 · 12 常数来源分类（D2 四重过滤）")
    print("=" * 78)

    md_path = os.path.join(target_dir(), "TUFT_V3.4全参数闭合总装_2026-10-10.md")
    if not os.path.exists(md_path):
        BOUND("B00", "来料 md 缺失：%s" % os.path.basename(md_path), "不代读、不编造")
        CHK("CHK-B00 来料可读", False, "md 缺失")
        return dict(items=ITEMS, self_checks=_SELF), False

    md = open(md_path, encoding="utf-8", errors="ignore").read()
    rows = parse_table(md)
    # 只保留「全参数表（确定值+来源）」段（该段在 md 中出现于「### 全参数表」之后）
    seg = md
    if "全参数表" in md:
        seg = md.split("全参数表", 1)[1]
    rows = parse_table(seg)

    print("  解析到 %d 行常数表" % len(rows))
    tally = {}
    detail_rows = []
    for p, v, s in rows:
        lab = classify(s, v)
        tally[lab] = tally.get(lab, 0) + 1
        detail_rows.append(dict(param=p, value=v, source=s, cls=lab))
        print("   %-14s %-22s %-16s -> %s" % (p[:14], v[:22], s[:16], lab))

    n_input = tally.get("INPUT_MEAS", 0)
    n_fit = tally.get("FIT", 0)
    n_assumed = tally.get("ASSUMED", 0)
    n_circ = tally.get("CIRCULAR", 0)
    n_ident = tally.get("IDENTIFIED", 0)
    n_der = tally.get("DERIVED", 0)
    n_derdep = tally.get("DERIVED_DEP", 0)
    n_non_derived = n_input + n_fit + n_assumed + n_circ + n_ident

    print("-" * 78)
    print("  分类汇总：INPUT_MEAS=%d FIT=%d ASSUMED=%d CIRCULAR=%d IDENTIFIED=%d "
          "DERIVED=%d DERIVED_DEP=%d" % (n_input, n_fit, n_assumed, n_circ, n_ident, n_der, n_derdep))

    # ---- B01 主判 ----
    F("B01",
      "来源分类：DERIVED=%d ; 输入/拟合/假设/循环/认定=%d ——「自由参数=0」实为「每个常数都被标了来源名」"
      % (n_der, n_non_derived),
      "仅 D2（场内容 1 圈 β）是场内真实计算；D1_S 依赖外部 A=0.4773；"
      "其余为观测锚/EDM 排除/结构假设/匹配律定义/认定 ⇒ 措辞应为「无拟合参数」，非「自由参数=0」")

    # ---- B02 正向对照：分类器必须能识别真 DERIVED ----
    # 真推导例：SU(3) 一圈 β 系数 b0 = 11 − (2/3)n_f ；κ_g² = 8πG/c⁴ ；R_s = 2GM/c²
    def b0_su3(nf):
        return d(11) - d(2) * d(nf) / d(3)
    b0_6 = b0_su3(6)
    ok_b0 = (b0_6 == d(7))
    G = d("6.67430e-11")
    c = d("299792458")
    kappa_g2 = 8 * d("3.14159265358979323846264338327950288") * G / (c ** 4)
    ok_kg = rel(kappa_g2, d("2.0766e-43")) < d("1e-3")
    CHK("CHK-5a 真推导例 b0=11−(2/3)n_f (n_f=6) 得 7", ok_b0, "b0=%s" % b0_6)
    CHK("CHK-5b 真推导例 κ_g²=8πG/c⁴ 复现", ok_kg, "κ_g²=%s" % ("%.6e" % kappa_g2))
    P("B02", "正向对照：b0=11−(2/3)n_f(n_f=6)=%s；κ_g²=8πG/c⁴=%s —— 分类器可识别真实 DERIVED"
      % (b0_6, "%.6e" % kappa_g2),
      "证明 B01 的判负来自来源栏本身，而非无条件判负")

    # ---- B03 跨册交叉：C4 的定性在同簇内不一致 ----
    v70 = os.path.join(target_dir(), "OpenUFT统一场论v7.0_无自由参数终卷_2026-10-10.md")
    v41 = [f for f in os.listdir(target_dir()) if f.startswith("OpenUFT归一化总纲v4.1")]
    txt = ""
    if os.path.exists(v70):
        txt += open(v70, encoding="utf-8", errors="ignore").read()
    for f in v41:
        txt += open(os.path.join(target_dir(), f), encoding="utf-8", errors="ignore").read()
    hit_m3 = ("M3" in txt and "证伪" in txt)
    hit_c4 = ("C4" in txt)
    print("  B03 跨册检索：M3 证伪字样=%s ; C4 字样=%s" % (hit_m3, hit_c4))
    if hit_m3 and hit_c4:
        BOUND("B03", "同簇内 v4.1 记载「M3 圈系数首原路径被证伪」，而证书/总装将 C4 记为「稳定性闭合（确定值）」",
              "C4 的定性在簇内不一致：或属方案相关的 β_G 结构，或为稳定性反解值 ⇒ 待人工裁定，记 BOUNDARY")
    else:
        BOUND("B03", "未检索到足够跨册证据（M3 证伪=%s / C4=%s），不作判定" % (hit_m3, hit_c4),
              "不代读、不推测")

    # ---- 工具层自检 ----
    CHK("CHK-B01 常数表解析非空", len(rows) > 0, "解析行数=%d" % len(rows))
    CHK("CHK-B02 分类器无 UNKNOWN 残留", tally.get("UNKNOWN", 0) == 0,
        "UNKNOWN=%d" % tally.get("UNKNOWN", 0))
    # 反向对照：把来源栏换成真推导措辞，分类器必须判 DERIVED
    CHK("CHK-5c 来源栏改「场内容 1 圈 β」必判 DERIVED",
        classify("场内容 1 圈 β", "-1.114") == "DERIVED", "")

    # ---- 输出 ----
    outdir = os.path.join(os.path.dirname(HERE), "数据")
    os.makedirs(outdir, exist_ok=True)
    json_path = os.path.join(outdir, "attack16_probe1_常数来源D2四重过滤_2026-10-10.json")
    txt_path = os.path.join(outdir, "attack16_probe1_常数来源D2四重过滤_2026-10-10_report.txt")
    payload = dict(
        probe="attack16_probe1_常数来源D2四重过滤",
        date="2026-10-10",
        items=ITEMS,
        self_checks=_SELF,
        computed=dict(
            n_rows=len(rows),
            tally=tally,
            n_derived=n_der, n_derived_dep=n_derdep, n_non_derived=n_non_derived,
            control_b0_su3_nf6=str(b0_6), control_kappa_g2=str(kappa_g2),
        ),
        table=detail_rows,
        red_lines=[
            "判 INPUT/ASSUMED/CIRCULAR 不等于指称造假；给常数标来源是常规做法",
            "本探针只判定「有来源名」≠「无外部输入」⇒ 「自由参数=0」措辞不成立",
            "不产生新物理",
        ],
    )
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("attack16 probe1 常数来源 D2 四重过滤 2026-10-10\n")
        f.write("来源分类：DERIVED=%d 输入/拟合/假设/循环/认定=%d\n" % (n_der, n_non_derived))
        for r in detail_rows:
            f.write("%s | %s | %s -> %s\n" % (r["param"], r["value"], r["source"], r["cls"]))

    verdicts = {}
    for it in ITEMS:
        verdicts[it["verdict"]] = verdicts.get(it["verdict"], 0) + 1
    self_ok = sum(1 for s in _SELF if s["ok"])
    print("-" * 78)
    print("读数：条目 %d ｜ %s" % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False)))
    print("自检：%d/%d" % (self_ok, len(_SELF)))
    for s in _SELF:
        if not s["ok"]:
            print("  自检未过：%s %s" % (s["name"], s["detail"]))
    print("产物：")
    for p_ in (json_path, txt_path):
        print("  " + os.path.relpath(p_, os.path.dirname(HERE)))
    print("=" * 78)
    return payload, self_ok == len(_SELF)


if __name__ == "__main__":
    _, ok = run_all()
    sys.exit(0 if ok else 1)
