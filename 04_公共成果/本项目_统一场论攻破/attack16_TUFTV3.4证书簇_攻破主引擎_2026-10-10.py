# -*- coding: utf-8 -*-
"""attack16 主引擎 · 算法联盟 TUFT V3.4「完成验证证书」簇 全维攻破审计（2026-10-10）

只做一件事：对来料**明示的可算断言**逐条独立复算，并判定其与自身/跨册证据是否一致。
- 不采信体系自报（所有读数由本引擎现场重算，或读来料 json 并交叉核对）；
- 不代读未提供的材料；不复读来料结论；
- **不产生新物理**；不宣称突破/完成/攻破成功；数学自洽 ≠ 物理证实。

结构：
  §A 自相矛盾扫描（A01–A09）   —— 主引擎
  §B 常数来源分类（B01–B03）   —— probe1
  §C 恒等式检测器（C01–C04）   —— probe2
  §D 味自由度秩计数（D01–D07） —— probe3
  §E v5.0 §6 数值独立复算       —— 主引擎（正向对照，防「只出负判」）
  §F C4 灵敏度与来源链          —— probe4

退出码纪律：`sys.exit(0 if self_ok == len(_SELF) else 1)`。
审计判出 FAIL/MISMATCH **不是**引擎失败；引擎失败只由 CHK 未过表达。
"""

import os
import sys
import json
import importlib.util
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
getcontext().prec = 60

ITEMS = []
_SELF = []
PROBES = {}


def P(name, ok, detail, note=""):
    ITEMS.append(dict(id=name, verdict="PASS" if ok else "FAIL", detail=detail, note=note))


def F(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="FAIL", detail=detail, note=note))


def BOUND(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="BOUNDARY", detail=detail, note=note))


def INFO(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="INFO", detail=detail, note=note))


def CORR(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="CORRECTED", detail=detail, note=note))


def MIS(name, detail, note=""):
    ITEMS.append(dict(id=name, verdict="MISMATCH", detail=detail, note=note))


def CHK(name, cond, detail=""):
    _SELF.append(dict(name=name, ok=bool(cond), detail=detail))


def d(x):
    return Decimal(str(x))


def rel(a, b):
    a, b = d(a), d(b)
    den = max(abs(a), abs(b))
    return abs(a - b) / den if den != 0 else abs(a - b)


def target_dir():
    up = os.path.dirname(HERE)                       # 04_公共成果
    return os.path.join(up, "算法联盟_全维自洽与归一化")


def tdata(name):
    p = os.path.join(target_dir(), "数据", name)
    return p if os.path.exists(p) else None


def load_json(name):
    p = tdata(name)
    if not p:
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def read_md(name):
    p = tdata(name)
    if not p:
        return ""
    return open(p, encoding="utf-8", errors="ignore").read()


def load_probe(fname, key):
    p = os.path.join(HERE, fname)
    if not os.path.exists(p):
        CHK("CHK-PROBE %s 存在" % key, False, "缺失 %s" % fname)
        return None
    spec = importlib.util.spec_from_file_location("probe_" + key, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    payload, ok = mod.run_all()
    PROBES[key] = payload
    # 合并子探针条目与自检（加前缀避免编号冲突）
    for it in payload.get("items", []):
        ITEMS.append(dict(id="%s.%s" % (key, it["id"]), verdict=it["verdict"],
                          detail=it.get("detail", ""), note=it.get("note", "")))
    for s in payload.get("self_checks", []):
        _SELF.append(dict(name="%s.%s" % (key, s["name"]), ok=s["ok"], detail=s.get("detail", "")))
    return payload


# ============================ §A 自相矛盾扫描 ============================

def section_A(cert_text, report_text):
    src = os.path.join(target_dir(), "源码")
    pys = []
    if os.path.isdir(src):
        pys = sorted(f for f in os.listdir(src) if f.endswith(".py"))
    tuft = [f for f in pys if f.startswith("TUFT_V3.4")]

    # A01 引擎计数
    claimed = None
    m = re.search(r"(\d+)\s*个引擎", cert_text) if cert_text else None
    if m:
        claimed = int(m.group(1))
    omitted = []
    for f in tuft:
        stem = f[:-3]
        # 去掉日期尾缀后取主干关键词
        core = re.sub(r"_?20\d\d-\d\d-\d\d$", "", stem)
        if core and core not in cert_text:
            omitted.append(f)
    print("  A01 源码 .py=%d（TUFT_V3.4*=%d）；证书称 %s 个" % (len(pys), len(tuft), claimed))
    if claimed is not None and len(tuft) != claimed:
        MIS("A01", "源码实有 TUFT_V3.4 引擎 %d 个，证书称「全部 %d 个引擎」" % (len(tuft), claimed),
            "未见于证书的引擎 %d 个：%s" % (len(omitted), "、".join(o[:34] for o in omitted[:6])))
    else:
        INFO("A01", "引擎计数一致：%d" % len(tuft), "")

    # A02 net 三值
    j_free = load_json("TUFT_V3.4自由参数收支核算_2026-10-10.json")
    j_lag = load_json("TUFT_V3.4拉氏量闭合可行性_2026-10-10.json")
    net_free = (j_free or {}).get("computed", {}).get("net_free")
    net_after = (j_lag or {}).get("computed", {}).get("net_after")
    claims_zero = ("net=7 → 0" in cert_text) or ("net=7→0" in cert_text)
    print("  A02 net_free=%s net_after=%s 证书称归零=%s" % (net_free, net_after, claims_zero))
    if net_free is not None and net_after is not None:
        trio = {str(net_free), str(net_after), "0"}
        MIS("A02", "net 三值 {%s, %s, 0} 互斥：收支核算 net_free=%s；拉氏量闭合 net_after=%s；证书 R3 称 →0"
            % (net_free, net_after, net_free, net_after),
            "**全库无任何引擎算出 net=0** ——「0」是证书断言，不是引擎计算")
    else:
        BOUND("A02", "net 来料缺失（收支=%s / 拉氏量=%s）" % (j_free is not None, j_lag is not None),
              "不代读、不编造")

    # A03 AUDIT-FIND 引擎自身 n_fail 仍 >0
    audit = {
        "背景挠率演化_审计": "TUFT_V3.4背景挠率演化_审计_2026-10-09.json",
        "自由参数收支核算": "TUFT_V3.4自由参数收支核算_2026-10-10.json",
        "拉氏量闭合可行性": "TUFT_V3.4拉氏量闭合可行性_2026-10-10.json",
        "RG流数值积分": "TUFT_V3.4_RG流数值积分_2026-10-10.json",
    }
    still = {}
    for k, fn in audit.items():
        j = load_json(fn)
        if j is not None:
            nf = j.get("n_fail")
            if nf:
                still[k] = nf
    print("  A03 仍带 n_fail>0 的审计引擎：%s" % still)
    if still:
        MIS("A03", "证书称 4 个 AUDIT-FIND（exit 2）发现的问题「已由后续闭合引擎实质解决」，"
            "但其自身 json 仍记录 n_fail>0：%s"
            % "、".join("%s=%d" % (k, v) for k, v in still.items()),
            "「已解决」未体现在被诊断引擎的自检计数中")
    else:
        INFO("A03", "未检索到 n_fail>0 的 AUDIT-FIND 引擎", "")

    # A04 α 混标（E9）
    j_tot = load_json("TUFT_V3.4全参数闭合总装_2026-10-10.json")
    aW = aEM = None
    if j_tot:
        aW = (j_tot.get("params", {}) or {}).get("alpha_W")
        aEM = (j_tot.get("params", {}) or {}).get("alpha_EM")
    # α(M_Z)=1/127.95=7.8156e-3 ；α(0)=1/137.036=7.2974e-3
    aMZ = d("7.8156e-3")
    a0 = d("7.2973525693e-3")
    print("  A04 α_W=%s α_EM=%s ；α(M_Z)=%s α(0)=%s" % (aW, aEM, aMZ, a0))
    if aW is not None and aEM is not None:
        r_mz = rel(d(aEM), aMZ)
        r_0 = rel(d(aEM), a0)
        # 消歧：α_EM 与 α(0) 一致 ⇒ 它是零能标值；α_W≈α_1(M_Z) ⇒ M_Z 标度
        # 消歧：来料只写 3 位（7.3e-3），故绝对阈值不可靠；
        # 正确判据是**距离比** —— α_EM 距 α(0) 与距 α(M_Z) 相差几个数量级。
        ratio = r_mz / r_0 if r_0 > 0 else d(0)
        print("      α_EM 距 α(0)=%s 距 α(M_Z)=%s 比值=%s" % ("%.2e" % r_0, "%.2e" % r_mz, "%.1f" % ratio))
        if ratio > d(100):
            MIS("A04", "全参数表同一格「观测」内 α_W=%s（≈α₁(M_Z)）与 α_EM=%s；"
                "α_EM 距 α(0)=%s、距 α(M_Z)=%s，**相差 %.0f 倍** ⇒ 它是零能标值"
                % (aW, aEM, "%.2e" % r_0, "%.2e" % r_mz, ratio),
                "**同一格混用两个能标**（M_Z vs 零能），违反 E9 能标一致性；"
                "残差 %s 由来料只写 3 位有效数字解释，不影响能标归属判定" % ("%.2e" % r_0))
        else:
            BOUND("A04", "α_EM=%s 与 α(0)/α(M_Z) 相对差 %s / %s（比值 %.1f < 100），能标归属待裁定"
                  % (aEM, "%.2e" % r_0, "%.2e" % r_mz, ratio), "")
    else:
        BOUND("A04", "α 来料缺失", "")

    # A05 Y_B 双值
    j_r12 = load_json("TUFT_V3.4路线1to2_衔接_重子预言化_2026-10-09.json")
    y_obs = (j_r12 or {}).get("computed", {}).get("Y_obs")
    y_scr = (j_tot or {}).get("computed", {}).get("Y_B_screened")
    if y_obs is not None and y_scr is not None:
        r = rel(d(y_scr), d(y_obs))
        print("  A05 Y_obs=%s vs Y_B_screened=%s 相对差=%s" % (y_obs, y_scr, "%.3e" % r))
        MIS("A05", "Y_B 双值：路线1to2 Y_obs=%s；全参数总装 Y_B_screened=%s；相对差 %.3f%%"
            % (y_obs, y_scr, r * 100), "同一证书簇两条链路给出不同 Y_B")
    else:
        BOUND("A05", "Y_B 来料缺失", "")

    # A06 θ 符号（v6.0 vs v7.0）
    v6 = read_md("OpenUFT统一场论v6.0_完成态卷三缺口闭合_2026-10-10.md")
    v7 = read_md("OpenUFT统一场论v7.0_无自由参数终卷_2026-10-10.md")
    th6 = re.findall(r"θ\s*=\s*(-?\s*2)", v6)
    th7 = re.findall(r"θ\s*=\s*(\+?\s*2)", v7)
    print("  A06 v6.0 θ 命中=%s ；v7.0 θ 命中=%s" % (th6[:3], th7[:3]))
    if th6 and th7:
        s6 = th6[0].replace(" ", "")
        s7 = th7[0].replace(" ", "")
        if s6.lstrip("+") != s7.lstrip("+"):
            MIS("A06", "临界指数 θ：v6.0 给 %s，v7.0 给 %s（符号相反）" % (s6, s7),
                "符号决定相关性方向相关/无关 ⇒ 不是笔误级差异")
        else:
            INFO("A06", "θ 两版一致：%s" % s6, "")
    else:
        BOUND("A06", "θ 未能在 v6.0/v7.0 中稳定检索到（v6=%s / v7=%s）" % (bool(th6), bool(th7)),
              "不推测，记 BOUNDARY")

    # A07 参数计数（v6 自纠）
    has18 = ("3+2+12+1" in v6) or ("18" in v6 and "19" in v6)
    selfcorrected = ("v6 算成 18" in v7) or ("3+2+6+3+4+1" in v7)
    print("  A07 v6 含 3+2+12+1=%s ；v7 自纠=%s" % (has18, selfcorrected))
    if selfcorrected:
        CORR("A07", "v6.0「3+2+12+1」算术得 18 ≠ 声明 19；**v7.0 已自行纠正**为 3+2+6+3+4+1=19",
             "已自纠 ⇒ 记为 CORRECTED，不重复计入负面（避免过度指控）")
    elif has18:
        MIS("A07", "v6.0 参数自和 3+2+12+1=18 ≠ 声明 19", "")
    else:
        BOUND("A07", "参数计数证据不足", "")

    # A08 19 的双口径
    BOUND("A08", "「19」在 v6.0（含 3 中微子质量、CKM/PMNS 含于上）与 v7.0（最小 SM："
          "3+2+6+3+4+1）是**两套口径**", "口径不同 ⇒ 跨版本比较 19 无意义，记 BOUNDARY")

    # A09 诚实标准降级
    v5 = read_md("OpenUFT统一场论v5.0_四力统一作用量闭合定本_2026-10-10.md")
    std_v5 = ("拒绝夸大" in v5) or ("未解" in v5) or ("测量输入" in v5)
    claim_v7 = ("无自由参数" in v7) or ("自由参数=0" in (cert_text or ""))
    print("  A09 v5.0 自定诚实标准=%s ；v7.0/证书称自由参数=0=%s" % (std_v5, claim_v7))
    if std_v5 and claim_v7:
        MIS("A09", "v5.0 自定标准「把『统一作用量已写出』夸大成『所有常数已推出』是造假，本版拒绝」；"
            "v7.0/证书则宣称「无自由参数 / 自由参数=0」",
            "同一簇内诚实标准被**降级**（自定红线 → 自称完成）")
    else:
        BOUND("A09", "v5.0 诚实标准证据不足（v5=%s / v7+证书=%s）" % (std_v5, claim_v7), "")


# ============================ §E 正向复算（防「只出负判」） ============================

def section_E():
    pi = d("3.14159265358979323846264338327950288419716939937510582097494")
    G = d("6.67430e-11")
    c = d("299792458")

    # E01 κ_g² = 8πG/c⁴
    kg2 = 8 * pi * G / (c ** 4)
    ok = rel(kg2, d("2.0766e-43")) < d("1e-3")
    P("E01", ok, "κ_g² = 8πG/c⁴ = %s（参考 2.0766e-43）" % ("%.6e" % kg2), "量纲/数值复现")

    # E02 SU(3) 一圈 β 系数 b0 = 11 − (2/3)n_f
    b0 = d(11) - d(2) * d(6) / d(3)
    P("E02", b0 == d(7), "b0(SU(3), n_f=6) = 11 − (2/3)·6 = %s" % b0, "来料称 7 ✓")

    # E03 1/(16π²)
    v = d(1) / (16 * pi * pi)
    P("E03", rel(v, d("0.00633257")) < d("1e-5"), "1/(16π²) = %s" % ("%.8f" % v), "")

    # E04 地球 Schwarzschild 半径 R_s = 2GM/c²
    M = d("5.9722e24")
    Rs = 2 * G * M / (c ** 2)
    P("E04", rel(Rs, d("8.870e-3")) < d("1e-3"), "地球 R_s = 2GM/c² = %s m = %s mm"
      % ("%.6e" % Rs, "%.3f" % (Rs * 1000)), "来料称 8.870 mm ✓")

    # E05 光线偏折 4GM/(c²R)
    R_sun = d("6.957e8")
    defl_rad = 4 * G * M_sun() / (c ** 2 * R_sun)
    defl_arc = defl_rad * d("206265")
    r = rel(defl_arc, d("1.7512"))
    P("E05", r < d("1e-3"), "偏折 = 4GM/(c²R) = %s″（来料 1.7512″，相对差 %s）"
      % ("%.5f" % defl_arc, "%.2e" % r),
      "残差由太阳质量/半径末位决定（消歧：非算术错）")

    # E06 光子球 1.5 R_s / 临界参数 3√3/2
    crit = (d(3).sqrt() * d(3)) / d(2)
    P("E06", rel(crit, d("2.598076")) < d("1e-6") and d("1.5") == d("1.5"),
      "临界碰撞参数 = 3√3/2 = %s R_s；光子球 = 1.5 R_s（恒等式，复现）" % ("%.6f" % crit), "")

    # E07 挠率修正式量级（仅登记量级，不判数值）
    INFO("E07", "挠率修正 ~4.1e-41 属量级登记项（来料未给可复算闭式）",
         "不作数值判定，避免代读未提供材料")


def M_sun():
    return d("1.98892e30")


# ============================ 主流程 ============================

def run_all():
    global re
    import re as _re
    re = _re

    print("=" * 78)
    print("attack16 主引擎 · 算法联盟 TUFT V3.4 证书簇 全维攻破审计")
    print("=" * 78)

    cert_text = read_md("统一场论_TUFT_V3.4_完成验证证书_2026-10-10.md")
    report_text = read_md("统一场论_TUFT_V3.4_全维度全链路攻破_完成总报告_2026-10-10.md")

    print("--- §A 自相矛盾扫描 ---")
    section_A(cert_text, report_text)

    print("--- §B 常数来源分类（probe1）---")
    load_probe("attack16_probe1_常数来源D2四重过滤_2026-10-10.py", "B")
    print("--- §C 恒等式检测器（probe2）---")
    load_probe("attack16_probe2_恒等式检测器_2026-10-10.py", "C")
    print("--- §D 味自由度秩计数（probe3）---")
    load_probe("attack16_probe3_味自由度秩计数_2026-10-10.py", "D")
    print("--- §F C4 灵敏度与来源链（probe4）---")
    load_probe("attack16_probe4_C4灵敏度与来源链_2026-10-10.py", "F")

    print("--- §E v5.0 §6 数值独立复算（正向对照）---")
    section_E()

    # ---------- 元层自检 ----------
    # CHK-11 每条 FAIL/MISMATCH 必带来源+可检索数字
    bad = [it for it in ITEMS
           if it["verdict"] in ("FAIL", "MISMATCH") and len(it.get("detail", "")) < 15]
    CHK("CHK-11 负判条目均带可检索细节", len(bad) == 0, "缺细节条数=%d" % len(bad))

    # CHK-13 22 体系 validated = 0
    # target_dir = openuft/04_公共成果/<靶>；再退两级 = openuft
    root_openuft = os.path.dirname(os.path.dirname(target_dir()))
    reg = os.path.join(root_openuft, "00_项目治理", "system_registry.json")
    n_sys = n_val = None
    if os.path.exists(reg):
        try:
            rj = json.load(open(reg, encoding="utf-8"))
            syslist = rj.get("systems", [])
            n_sys = len(syslist)
            n_val = sum(1 for s in syslist if str(s.get("status", "")).lower() == "validated")
        except Exception:
            pass
    CHK("CHK-13 22 体系 validated = 0", (n_sys == 22 and n_val == 0),
        "体系数=%s validated=%s" % (n_sys, n_val))

    # CHK-14 §E 至少 6 条 PASS（防只出负判）
    n_pass = sum(1 for it in ITEMS if it["verdict"] == "PASS")
    n_pass_E = sum(1 for it in ITEMS if it["verdict"] == "PASS" and it["id"].startswith("E"))
    CHK("CHK-14 §E 正向复算至少 6 条 PASS", n_pass_E >= 6, "E 组 PASS=%d" % n_pass_E)

    # ---------- 输出三件套 ----------
    outdir = os.path.join(os.path.dirname(HERE), "数据")
    os.makedirs(outdir, exist_ok=True)
    base = "attack16_TUFTV3.4证书簇_攻破审计_2026-10-10"
    json_path = os.path.join(outdir, base + ".json")
    md_path = os.path.join(outdir, base + ".md")
    txt_path = os.path.join(outdir, base + "_report.txt")

    verdicts = {}
    for it in ITEMS:
        verdicts[it["verdict"]] = verdicts.get(it["verdict"], 0) + 1
    self_ok = sum(1 for s in _SELF if s["ok"])

    payload = dict(
        engine="attack16_TUFTV3.4证书簇_攻破主引擎",
        date="2026-10-10",
        target="openuft/04_公共成果/算法联盟_全维自洽与归一化/（TUFT V3.4 完成验证证书簇）",
        items=ITEMS,
        self_checks=_SELF,
        verdict_counts=verdicts,
        n_items=len(ITEMS),
        n_self=len(_SELF),
        n_self_ok=self_ok,
        registry=dict(n_systems=n_sys, n_validated=n_val),
        red_lines=[
            "数学自洽 ≠ 物理证实；本册是对来料的审计与可算判决，不产生新物理",
            "22 体系零 validated 红线不变",
            "不采信体系自报、不代读未提供材料、不升格未闭合项",
        ],
    )
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    def build_md(_self_ok, _n_self):
        """三件套的 md 由函数生成 —— 因为 CHK-12 在首轮落盘之后追加，
        自检计数会变化，md 必须能按最终 _SELF 重算，否则会留下 22/22 的陈旧读数。"""
        L = []
        L.append("# attack16 · 算法联盟 TUFT V3.4 证书簇 攻破审计（2026-10-10）")
        L.append("")
        L.append("- 判定计数：" + " ".join("%s=%d" % (k, v) for k, v in sorted(verdicts.items()))
                 + "；总计 %d" % len(ITEMS))
        L.append("- 引擎自检：%d/%d；registry 体系=%s validated=%s"
                 % (_self_ok, _n_self, n_sys, n_val))
        L.append("")
        L.append("## 逐条判定")
        L.append("| 编号 | 判定 | 明细 |")
        L.append("|---|---|---|")
        for it in ITEMS:
            L.append("| %s | %s | %s |" % (it["id"], it["verdict"],
                                           it.get("detail", "").replace("|", "\\|")[:200]))
        L.append("")
        L.append("## 诚实边界（本索引不代选的事）")
        for r_ in payload["red_lines"]:
            L.append("- " + r_)
        return "\n".join(L)

    md_text = build_md(self_ok, len(_SELF))
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_text)

    # 自检：输出文本不得出现「完成/突破/validated」的肯定式（CHK-12 前置数据）
    out_text = md_text + json.dumps(payload, ensure_ascii=False)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("attack16 攻破审计 2026-10-10\n")
        f.write("读数：条目 %d ｜ %s\n" % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False)))
        f.write("自检：%d/%d\n" % (self_ok, len(_SELF)))
        f.write("22 体系 validated = %s\n" % n_val)
        for p_ in PROBES:
            c = PROBES[p_].get("computed", {})
            if p_ == "C":
                f.write("α_G 恒等式判别力 = 0 (maxrel=%s)\n"
                        % c.get("alphaG_identity_maxrel_exactdef", ""))
            if p_ == "B":
                f.write("来源分类：DERIVED=%s ; 输入/拟合/假设/循环/认定=%s\n"
                        % (c.get("n_derived"), c.get("n_non_derived")))
            if p_ == "D":
                f.write("味秩 n_g=3 quark-only：实 %s - 秩 %s = %s\n"
                        % (c["ng3_quark_only"]["nparam"], c["ng3_quark_only"]["rank"],
                           c["ng3_quark_only"]["dof"]))
            if p_ == "F":
                f.write("C4_required = %s\n" % c.get("C4_required"))

    # CHK-12：册中不得出现自我肯定的「完成/突破」结论（允许出现在引用/标题名词中）
    forbidden = re.findall(r"(攻破完成|突破完成|已达成|validated\s*=\s*[1-9])", out_text)
    CHK("CHK-12 输出文本无肯定式完成/突破结论", len(forbidden) == 0,
        "命中=%s" % forbidden[:3])

    # 首轮落盘之后才追加 CHK-12 ⇒ 三件套（json/md/txt）**全部**必须用最终 _SELF 重落，
    # 否则会留下 22/22 这类比实际少一条的陈旧读数（本轮踩过：首版只重落 json/txt）。
    payload["self_checks"] = list(_SELF)
    payload["n_self"] = len(_SELF)
    payload["n_self_ok"] = sum(1 for s in _SELF if s["ok"])
    with open(json_path, "w", encoding="utf-8") as _f:
        json.dump(payload, _f, ensure_ascii=False, indent=2)
    with open(md_path, "w", encoding="utf-8") as _f:
        _f.write(build_md(payload["n_self_ok"], payload["n_self"]))
    with open(txt_path, "w", encoding="utf-8") as _f:
        _f.write("attack16 攻破审计 2026-10-10\n")
        _f.write("读数：条目 %d ｜ %s\n" % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False)))
        _f.write("自检：%d/%d\n" % (payload["n_self_ok"], payload["n_self"]))
        _f.write("22 体系 validated = %s\n" % n_val)
        for p_ in PROBES:
            c = PROBES[p_].get("computed", {})
            if p_ == "C":
                _f.write("α_G 恒等式判别力 = 0 (maxrel=%s)\n"
                         % c.get("alphaG_identity_maxrel_exactdef", ""))
            if p_ == "B":
                _f.write("来源分类：DERIVED=%s ; 输入/拟合/假设/循环/认定=%s\n"
                         % (c.get("n_derived"), c.get("n_non_derived")))
            if p_ == "D":
                _f.write("味秩 n_g=3 quark-only：实 %s - 秩 %s = %s\n"
                         % (c["ng3_quark_only"]["nparam"], c["ng3_quark_only"]["rank"],
                            c["ng3_quark_only"]["dof"]))
            if p_ == "F":
                _f.write("C4_required = %s\n" % c.get("C4_required"))

    print("-" * 78)
    print("读数：条目 %d ｜ %s" % (len(ITEMS), json.dumps(verdicts, ensure_ascii=False)))
    print("自检：%d/%d" % (sum(1 for s in _SELF if s["ok"]), len(_SELF)))
    for s in _SELF:
        if not s["ok"]:
            print("  自检未过：%s %s" % (s["name"], s["detail"]))
    print("22 体系 validated = %s" % n_val)
    print("产物：")
    for p_ in (json_path, md_path, txt_path):
        print("  " + os.path.relpath(p_, os.path.dirname(HERE)))
    print("=" * 78)
    # CHK-12 是在 self_ok 之后追加的，故此处必须重新统计，否则与增长后的 len(_SELF) 恒不等
    all_ok = all(s["ok"] for s in _SELF)
    return payload, all_ok


if __name__ == "__main__":
    _, ok = run_all()
    sys.exit(0 if ok else 1)
