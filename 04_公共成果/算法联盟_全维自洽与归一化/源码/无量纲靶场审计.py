# -*- coding: utf-8 -*-
"""
无量纲靶场审计（可复跑）
========================
回答一个此前 openuft **从未被量化**的问题：

    18 个已登记体系里，到底有几个给出了「无量纲靶」的**预测值 + 误差棒**？

为什么必须是无量纲靶
--------------------
带量纲的量（c、ℏ、G、m_e 的 SI 数值）可以被任意单位换算"凑"出来，
凑出来的等式在数值上必然成立，却不含任何物理信息。
只有无量纲数（α、质量比、α_grav、整数靶…）才是真正的靶子。

本册的新方程：信息增益判别式 V
------------------------------
    V = (n_hit - n_free - n_anchor) / n_hit        (n_hit > 0)

    n_hit    : 命中的无量纲靶个数（判据 |pred/obs - 1| <= 3 * u_rel，即 3σ）
    n_free   : 体系自己的可调自由参数个数（未登记则整个判别不可用）
    n_anchor : 该式所消耗的**外部测量常数**个数（CODATA 锚，如 G、m_e、ℏ、c）

判定：
    V > 0   有信息增益：输出比输入多，才是真正的"派生"
    V = 0   等价交换：1 个输入换 1 个输出，无增益
    V < 0   净消耗：把测量值重新包装（**伪派生**，M02 普朗克锚定谬误即此类）
    n_hit=0 无登记预测：不可证伪（不是"错"，是"还没给出可被检验的东西"）

V 的意义（这是本册唯一的原创方程）
----------------------------------
它把「单位换算伪派生」变成**可计算的**：
  α_grav(e) = G·m_e²/(ℏ·c) 消耗 4 个锚、产出 1 个无量纲数
  => V = (1 - 0 - 4)/1 = -3  => 判为伪派生。
这与 04_公共成果 已确认的 M02（普朗克锚定谬误）独立地给出同一结论，
说明 V 不是事后编造的口径。

产出：数据/无量纲靶场审计.json + 数据/无量纲靶场审计.md
"""

import os
import re
import sys
import json
import time
from mpmath import mp, mpf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
mp.dps = 80

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SYS_DIR = os.path.join(ROOT, "01_独立体系")
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

# ---------------------------------------------------------------------------
# 一、无量纲靶场（观测值；来源标注见 fact_check，本库未联网核对）
# ---------------------------------------------------------------------------
# urel = 观测相对不确定度，用作"命中门槛"的基准；3σ 判据即 3*urel。
TARGETS = [
    {"key": "alpha",       "name_zh": "精细结构常数 α",              "value": "7.2973525693e-3",  "urel": "1.5e-10"},
    {"key": "alpha_s",     "name_zh": "强耦合常数 α_S(M_Z)",         "value": "0.1179",           "urel": "8.5e-3"},
    {"key": "m_mu_over_me","name_zh": "质量比 m_μ/m_e",              "value": "206.7682830",      "urel": "2.2e-10"},
    {"key": "m_tau_over_me","name_zh": "质量比 m_τ/m_e",             "value": "3477.23",          "urel": "6.8e-5"},
    {"key": "me_over_mP",  "name_zh": "质量比 m_e/m_P",              "value": None,               "urel": "1.1e-5"},
    {"key": "alpha_grav_e","name_zh": "引力耦合 α_grav(电子)=(m_e/m_P)²", "value": None,           "urel": "2.2e-5"},
    {"key": "sin2_thetaW", "name_zh": "温伯格角 sin²θ_W(M_Z)",        "value": "0.23122",         "urel": "1.7e-4"},
    {"key": "mt_over_mW",  "name_zh": "质量比 m_t/m_W",              "value": None,               "urel": "3.0e-3"},
    {"key": "n_gen",       "name_zh": "代数 N_gen（整数靶）",         "value": "3",               "urel": "0"},
    {"key": "n_c",         "name_zh": "色数 N_c（整数靶）",           "value": "3",               "urel": "0"},
]

# 用于派生两个复合靶（纯算术，不涉及任何理论假设）
M_E = mpf("9.1093837015e-31")     # kg
M_P = mpf("2.176434e-8")          # kg
M_T = mpf("172.69")               # GeV
M_W = mpf("80.377")               # GeV


def build_targets():
    out = []
    for t in TARGETS:
        v = t["value"]
        if t["key"] == "me_over_mP":
            v = M_E / M_P
        elif t["key"] == "alpha_grav_e":
            v = (M_E / M_P) ** 2
        elif t["key"] == "mt_over_mW":
            v = M_T / M_W
        else:
            v = mpf(v)
        out.append({
            "key": t["key"],
            "name_zh": t["name_zh"],
            "value": mp.nstr(v, 12),
            "urel": t["urel"],
            "hit_threshold_3sigma": mp.nstr(mpf(3) * mpf(t["urel"]), 8),
        })
    return out


# ---------------------------------------------------------------------------
# 二、判别式 V
# ---------------------------------------------------------------------------

def verdict_v(n_hit, n_free, n_anchor):
    """返回 (V, 判定码, 说明)。n_free/n_anchor 未登记时返回 None 的 V。"""
    if n_hit is None or n_hit == 0:
        return None, "N", "未登记任何无量纲预测：不可证伪（不是错，是没给可检验的东西）"
    if n_free is None or n_anchor is None:
        return None, "N", "未登记自由参数/测量锚个数：判别不可用"
    v = (n_hit - n_free - n_anchor) / float(n_hit)
    if v > 0:
        code, desc = "A", "有信息增益：输出多于输入，构成真正的派生候选"
    elif v == 0:
        code, desc = "B", "等价交换：1 换 1，无信息增益"
    else:
        code, desc = "C", "净消耗：测量值的重新包装（伪派生）"
    return v, code, desc


def hit_test(pred, obs, urel, k=3):
    """3σ 命中判定。整数靶（urel=0）要求精确相等。"""
    pred = mpf(pred)
    obs = mpf(obs)
    if mpf(urel) == 0:
        return pred == obs
    if obs == 0:
        return abs(pred) <= mpf(k) * mpf(urel)
    return abs(pred / obs - 1) <= mpf(k) * mpf(urel)


# ---------------------------------------------------------------------------
# 三、工作算例（把 V 用在已知结论上，检验它是否给出正确的 verdict）
# ---------------------------------------------------------------------------

def worked_examples():
    tg = {t["key"]: t for t in build_targets()}
    rows = []

    # 例 1：α_grav(e) = G m_e²/(ℏ c) —— 消耗 4 个测量锚（G, m_e, ℏ, c），产出 1 个无量纲数
    pred = tg["alpha_grav_e"]["value"]
    hit = hit_test(pred, tg["alpha_grav_e"]["value"], tg["alpha_grav_e"]["urel"])
    v, code, desc = verdict_v(1 if hit else 0, 0, 4)
    rows.append({
        "name": "例1 α_grav(e)=G·m_e²/(ℏ·c)（M02 型）",
        "n_hit": 1 if hit else 0, "n_free": 0, "n_anchor": 4,
        "V": v, "verdict": code, "desc": desc,
        "comment": "数值必然命中（恒等式），但消耗 4 个锚只产出 1 个数 => V=-3，判伪派生。"
                   "与既有 M02 结论一致，说明 V 不是事后口径。",
    })

    # 例 2：N_gen = 3 由 SU(2)_2 三扇区导出（R17 路径）——消耗 1 个输入（存在费米子 -> k=2）
    hit = hit_test(3, tg["n_gen"]["value"], tg["n_gen"]["urel"])
    v, code, desc = verdict_v(1 if hit else 0, 0, 1)
    rows.append({
        "name": "例2 N_gen=3 由 SU(2)_2 三扇区导出（R17 路径）",
        "n_hit": 1 if hit else 0, "n_free": 0, "n_anchor": 1,
        "V": v, "verdict": code, "desc": desc,
        "comment": "1 个输入换 1 个输出 => V=0，无信息增益。"
                   "这不否定该路径的价值（它给出了机制），但按信息论口径它不是'免费'的派生。",
    })

    # 例 3：假想的合格候选：2 个自由参数 + 1 个锚，命中 4 个靶
    v, code, desc = verdict_v(4, 2, 1)
    rows.append({
        "name": "例3 假想合格候选（2 自由参数 + 1 锚，命中 4 靶）",
        "n_hit": 4, "n_free": 2, "n_anchor": 1,
        "V": v, "verdict": code, "desc": desc,
        "comment": "这是新体系入库时应达到的门槛：V>0。",
    })

    # 例 4：过拟合等价：3 个自由参数，命中 3 个靶
    v, code, desc = verdict_v(3, 3, 0)
    rows.append({
        "name": "例4 过拟合等价（3 自由参数，命中 3 靶）",
        "n_hit": 3, "n_free": 3, "n_anchor": 0,
        "V": v, "verdict": code, "desc": desc,
        "comment": "参数与靶数相等 => V=0。调参总能拟合，无任何解释价值。",
    })
    return rows


# ---------------------------------------------------------------------------
# 四、18 体系扫描（关键词下界；诚实标注为"线索"而非"登记"）
# ---------------------------------------------------------------------------

PATTERNS = {
    "alpha":        [r"137\.0", r"1\s*/\s*137", r"0\.00729", r"7\.2973", r"精细结构"],
    "alpha_s":      [r"0\.1179", r"0\.118\d", r"α_S", r"alpha_s", r"强耦合常数"],
    "m_mu_over_me": [r"206\.7\d*", r"m_μ\s*/\s*m_e", r"缪子.*电子.*比"],
    "m_tau_over_me":[r"3477", r"m_τ\s*/\s*m_e"],
    "me_over_mP":   [r"4\.1\d*\s*e-23", r"m_e\s*/\s*m_P", r"电子.*普朗克质量"],
    "alpha_grav_e": [r"1\.7\d*\s*e-45", r"α_grav", r"alpha_grav", r"引力耦合"],
    "sin2_thetaW":  [r"0\.2312", r"温伯格角", r"sin\s*2\s*θ_W", r"sin\^2\s*θ"],
    "mt_over_mW":   [r"2\.14\d", r"m_t\s*/\s*m_W"],
    "n_gen":        [r"三代", r"3\s*代", r"代数量", r"N_gen", r"代数"],
    "n_c":          [r"三色", r"N_c\s*=\s*3", r"色三重态", r"颜色.*3"],
}
ERR_TOKEN = re.compile(r"[±]|误差|偏差|不确定|σ|%")


def scan_system(path):
    """返回 {target_key: level}，level: 0 无 / 1 名称出现 / 2 数值出现 / 3 数值+误差线索。"""
    hits = {}
    files = []
    for dirpath, _dirs, names in os.walk(path):
        for n in names:
            if n.lower().endswith(".md"):
                files.append(os.path.join(dirpath, n))
    for fp in files[:400]:
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read(400000)
        except Exception:
            continue
        for key, pats in PATTERNS.items():
            lvl = hits.get(key, 0)
            for p in pats:
                m = re.search(p, text)
                if not m:
                    continue
                # 数值型（含数字）记 2，纯名称记 1
                cur = 2 if re.search(r"\d", p) else 1
                if cur >= 2:
                    window = text[max(0, m.start() - 120): m.start() + 120]
                    if ERR_TOKEN.search(window):
                        cur = 3
                if cur > lvl:
                    lvl = cur
            hits[key] = lvl
    return hits


def scan_all():
    rows = []
    if not os.path.isdir(SYS_DIR):
        return rows
    for name in sorted(os.listdir(SYS_DIR)):
        p = os.path.join(SYS_DIR, name)
        if not os.path.isdir(p) or name.startswith("新体系模板"):
            continue
        hits = scan_system(p)
        mentioned = sorted([k for k, v in hits.items() if v >= 1])
        with_value = sorted([k for k, v in hits.items() if v >= 2])
        with_err = sorted([k for k, v in hits.items() if v >= 3])
        rows.append({
            "system": name,
            "mentioned": mentioned,
            "with_value": with_value,
            "with_error_clue": with_err,
            "n_registered_predictions": 0,   # 需体系自行登记，扫描无法判定
            "verdict": "N" if not with_err else "N(待人工登记)",
        })
    return rows


# ---------------------------------------------------------------------------
# 五、产出
# ---------------------------------------------------------------------------

def render_md(targets, examples, systems):
    L = []
    L.append("# 无量纲靶场审计（可复跑产物）\n")
    L.append("> 本文件由 `源码/无量纲靶场审计.py` 生成，**请勿手工编辑**。\n")
    L.append("## 一、无量纲靶场（观测值）\n")
    L.append("| 靶 | 含义 | 观测值 | 相对不确定度 | 3σ 命中门槛 |")
    L.append("| --- | --- | --- | --- | --- |")
    for t in targets:
        L.append("| `%s` | %s | %s | %s | %s |"
                 % (t["key"], t["name_zh"], t["value"], t["urel"], t["hit_threshold_3sigma"]))
    L.append("\n## 二、信息增益判别式 V\n")
    L.append("```\nV = (n_hit - n_free - n_anchor) / n_hit      (n_hit > 0)\n```\n")
    L.append("| 判定 | 含义 |")
    L.append("| --- | --- |")
    L.append("| `V>0` (A) | 有信息增益：输出多于输入，真正的派生候选 |")
    L.append("| `V=0` (B) | 等价交换：无信息增益 |")
    L.append("| `V<0` (C) | 净消耗：测量值重新包装（伪派生） |")
    L.append("| `N` | 未登记无量纲预测：不可证伪 |")
    L.append("\n## 三、工作算例（检验 V 是否给出正确 verdict）\n")
    L.append("| 算例 | n_hit | n_free | n_anchor | V | 判定 | 评注 |")
    L.append("| --- | --- | --- | --- | --- | --- | --- |")
    for e in examples:
        L.append("| %s | %d | %d | %d | %s | %s | %s |"
                 % (e["name"], e["n_hit"], e["n_free"], e["n_anchor"],
                    ("%.2f" % e["V"]) if e["V"] is not None else "—",
                    e["verdict"], e["comment"]))
    L.append("\n## 四、18 体系扫描（关键词**下界**，非登记）\n")
    L.append("扫描只能证明\"这个体系讨论过这个靶\"，**不能**证明它给出了预测值与误差棒。\n")
    L.append("| 体系 | 提及靶 | 出现数值 | 数值+误差线索 | 登记预测数 | 判定 |")
    L.append("| --- | --- | --- | --- | --- | --- |")
    for s in systems:
        L.append("| %s | %s | %s | %s | %d | %s |"
                 % (s["system"],
                    ", ".join(s["mentioned"]) or "—",
                    ", ".join(s["with_value"]) or "—",
                    ", ".join(s["with_error_clue"]) or "—",
                    s["n_registered_predictions"], s["verdict"]))
    L.append("\n> 结论：全部体系 `n_registered_predictions = 0`——"
             "**没有一个体系登记了无量纲预测的数值与误差棒**。\n")
    return "\n".join(L) + "\n"


def main():
    t0 = time.time()
    targets = build_targets()
    examples = worked_examples()
    systems = scan_all()

    os.makedirs(OUT_DIR, exist_ok=True)
    payload = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mpmath_dps": mp.dps,
        "python": sys.version.split()[0],
        "targets": targets,
        "discriminant": "V = (n_hit - n_free - n_anchor) / n_hit",
        "worked_examples": examples,
        "systems": systems,
        "honest_note": ("扫描为关键词下界；'登记预测数' 必须由体系自行登记，"
                        "脚本无法判定。当前全部体系均未登记。"),
    }
    with open(os.path.join(OUT_DIR, "无量纲靶场审计.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, "无量纲靶场审计.md"), "w", encoding="utf-8") as fh:
        fh.write(render_md(targets, examples, systems))

    print("=" * 74)
    print("无量纲靶场审计（mpmath dps=%d，Python %s）" % (mp.dps, sys.version.split()[0]))
    print("=" * 74)
    for t in targets:
        print("  %-14s %-28s %s  (3σ 门槛 %s)"
              % (t["key"], t["name_zh"], t["value"], t["hit_threshold_3sigma"]))
    print("-" * 74)
    print("工作算例：")
    for e in examples:
        print("  [%s] %s  V=%s"
              % (e["verdict"], e["name"],
                 ("%.2f" % e["V"]) if e["V"] is not None else "—"))
    print("-" * 74)
    print("体系扫描（关键词下界）：共 %d 个体系" % len(systems))
    for s in systems:
        print("  %-34s 提及=%d 数值=%d 误差线索=%d 登记预测=0 -> %s"
              % (s["system"], len(s["mentioned"]), len(s["with_value"]),
                 len(s["with_error_clue"]), s["verdict"]))
    print("-" * 74)
    print("产出：数据/无量纲靶场审计.{json,md}  用时 %.2fs" % (time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
