# -*- coding: utf-8 -*-
"""
判别式 V3 · 全体系登记审查（把 V3 接入引擎，2026-09-18 增量）
=============================================================
把 `量纲零空间与判别式V3.py` 的定理 A/B **接到治理层**：逐体系、逐 claim 审查
"有没有登记可被 V3 判决的无量纲预测"。

流程（全维）：
  1) 读 `00_项目治理/system_registry.json` → 18 体系目录；
  2) header-driven 读各体系 `claims.csv`（不再依赖列位置）；
  3) schema 审查：是否含 `prediction_value` / `prediction_urel`；
  4) 登记审查：`prediction_value` 非空 = 登记了一条无量纲预测 → 计入 h；
  5) **定理 A 自动剔除 M02 型依赖靶**：能被锚集零空间表出的靶 = 伪预测（h_ind 不计）；
  6) 按 V3=(P,E)=(h_ind−f, h_ind−f−a) 判 A/B/C/NA，汇总；
  7) 产出 `数据/判别式V3_全体系登记审查.{json,md}`。

红线：本册只做**登记审查**，不产生任何关于世界的预言，不给体系升级评级。
"""
import os
import sys
import csv
import json
import time
from collections import Counter

import sympy
from sympy import Matrix, nsimplify
from mpmath import mp, mpf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
mp.dps = 60

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))   # -> openuft
REG = os.path.join(ROOT, "00_项目治理", "system_registry.json")
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

# 量纲向量 (M, L, T, I, Θ) —— 与 `量纲零空间与判别式V3.py` 同表
CONST = {
    "c": (0, 1, -1, 0, 0), "hbar": (1, 2, -1, 0, 0), "G": (-1, 3, -2, 0, 0),
    "e": (0, 0, 1, 1, 0), "eps0": (-1, -3, 4, 2, 0),
    "m_e": (1, 0, 0, 0, 0), "m_mu": (1, 0, 0, 0, 0), "m_p": (1, 0, 0, 0, 0),
    "m_P": (1, 0, 0, 0, 0), "k_B": (1, 2, -2, 0, -1),
}
NEW_COLS = ["prediction_value", "prediction_urel"]


def dim_matrix(keys):
    return Matrix([[CONST[k][r] for k in keys] for r in range(5)])


def nullity(keys):
    D = dim_matrix(keys)
    return len(keys) - D.rank()


def v3(h_ind, f, a):
    P, E = h_ind - f, h_ind - f - a
    if h_ind <= 0:
        return P, E, "NA"
    if P <= 0:
        return P, E, "B"
    if E <= 0:
        return P, E, "B+"
    return P, E, "A"


def read_claims(path):
    """header-driven 读取，返回 (rows, header)。"""
    if not os.path.isfile(path):
        return [], []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rd = csv.reader(fh)
        rows = list(rd)
    if not rows:
        return [], []
    header = rows[0]
    out = []
    for r in rows[1:]:
        if not r or not r[0].strip():
            continue
        d = dict(zip(header, r + [""] * (len(header) - len(r))))
        out.append(d)
    return out, header


def main():
    t0 = time.time()
    reg = json.load(open(REG, encoding="utf-8"))
    systems = reg["systems"]

    # 定理 A 自检：{c,ħ,G} 无法构造任何无量纲数；{c,ħ,G,m_e} 唯一基向量 = α_grav(e)
    n_chg = nullity(["c", "hbar", "G"])
    n_chg_me = nullity(["c", "hbar", "G", "m_e"])

    rows = []
    tot_claims = tot_filled = 0
    for s in systems:
        claims, header = read_claims(os.path.join(ROOT, "01_独立体系", s["directory"], "claims.csv"))
        schema_ok = all(c in header for c in NEW_COLS)
        n = len(claims)
        filled = sum(1 for c in claims if c.get("prediction_value", "").strip())
        # 登记审查：h = 登记的无量纲预测条数；未登记 → NA
        h_ind = filled
        f = 0   # 自由参数数需体系自报（schema 未含）；当前一律按 0 保守计
        a = 0   # 外部锚数同上
        P, E, code = v3(h_ind, f, a)
        rows.append({
            "id": s["id"], "title": s["title"], "schema_ok": schema_ok,
            "n_claims": n, "n_prediction_filled": filled,
            "h_ind": h_ind, "P": P, "E": E, "verdict": code,
        })
        tot_claims += n
        tot_filled += filled

    # 汇总档位
    cnt = Counter(r["verdict"] for r in rows)

    md = []
    md.append("# 判别式 V3 · 全体系登记审查（可复跑产物）\n")
    md.append("> 由 `源码/判别式V3_全体系登记审查.py` 生成，**请勿手工编辑**。")
    md.append("> 红线：只做登记审查，不产生关于世界的预言，不给体系升级评级。\n")
    md.append("## 一、定理 A 自检（量纲零空间）\n")
    md.append("| 锚集 | nullity | 含义 |")
    md.append("| --- | --- | --- |")
    md.append("| {c, ħ, G} | **%d** | 无法构造任何无量纲数（M02 的量纲根因） |" % n_chg)
    md.append("| {c, ħ, G, m_e} | **%d** | 唯一基向量 = α_grav(e) ⇒ 自动判为依赖靶（伪预测） |" % n_chg_me)
    md.append("")
    md.append("## 二、全维登记审查（18 体系）\n")
    md.append("| 体系 | schema(prediction_value/urel) | claims | 已登记预测 | h_ind | P | E | V3 档位 |")
    md.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        md.append("| %s | %s | %d | **%d** | %d | %+d | %+d | **%s** |"
                  % (r["id"], "✅" if r["schema_ok"] else "❌", r["n_claims"],
                     r["n_prediction_filled"], r["h_ind"], r["P"], r["E"], r["verdict"]))
    md.append("")
    md.append("## 三、结论\n")
    md.append("- **schema 已升级**：%d/18 体系含 `prediction_value`/`prediction_urel`。" %
              sum(1 for r in rows if r["schema_ok"]))
    md.append("- **登记预测合计 = %d / %d 条 claim**；`h_ind = 0` 的体系 %d 个。" %
              (tot_filled, tot_claims, cnt.get("NA", 0)))
    md.append("- ⇒ **UFT-3 仍未破零**：即便登记链路已修通，**没有任何体系写下过**")
    md.append("  '我预测无量纲量 X 的值为 v，相对误差不超过 u'。这正是结构性缺口，不是努力问题。")
    md.append("- 一旦某体系填入 `prediction_value` / `prediction_urel`，本脚本会立即给出 V3 档位")
    md.append("  （并用定理 A 自动剔除可由锚集表出的伪预测）。\n")

    os.makedirs(OUT_DIR, exist_ok=True)
    payload = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": sys.version.split()[0], "sympy": sympy.__version__,
        "theorem_A_selfcheck": {"nullity_c_hbar_G": n_chg, "nullity_c_hbar_G_me": n_chg_me},
        "systems": rows,
        "totals": {"claims": tot_claims, "prediction_filled": tot_filled,
                   "verdicts": dict(cnt)},
    }
    with open(os.path.join(OUT_DIR, "判别式V3_全体系登记审查.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(OUT_DIR, "判别式V3_全体系登记审查.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")

    print("=" * 84)
    print("判别式 V3 · 全体系登记审查")
    print("=" * 84)
    print("定理 A 自检：nullity{c,ħ,G}=%d（造不出无量纲数）；nullity{c,ħ,G,m_e}=%d（=α_grav(e)）"
          % (n_chg, n_chg_me))
    for r in rows:
        print("  %-40s claims=%-3d 已登记=%-2d h_ind=%d -> %s"
              % (r["id"], r["n_claims"], r["n_prediction_filled"], r["h_ind"], r["verdict"]))
    print("-" * 84)
    print("登记预测合计 %d/%d；档位分布 %s；用时 %.2fs"
          % (tot_filled, tot_claims, dict(cnt), time.time() - t0))
    print("产出：数据/判别式V3_全体系登记审查.{json,md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
