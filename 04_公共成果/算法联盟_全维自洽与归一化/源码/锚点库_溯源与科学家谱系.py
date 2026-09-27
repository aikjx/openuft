# -*- coding: utf-8 -*-
"""
经典基准锚点库 · 溯源与科学家谱系（2026-09-28）
================================================================
目的：为 `锚点库_前沿引力五册A到E.py` 的每一条锚点登记**奠基者与奠基工作**——
回答「这条锚点是谁、在哪一年、以哪项工作确立的」。

口径（红线，必读）：
- 本册**不对人物作价值评判、不排名**；
  「伟大」的唯一可核验口径 = **其奠基工作构成本锚点库某一不可绕过的结果**（去掉该工作，该锚点不存在）。
- 每条溯源必须给出**奠基文献/年份**；无文献依据的条目按门禁判违规。
- 锚点只记录「结果与贡献者的对应（溯源）」，不含对科学家的褒贬形容词
  （禁词扫描见 G7）。
- 数学自洽 ≠ 实验证实；溯源不构成对该理论或该人物的认可/否定。

门禁（自检 8 条，任一失败即退出码 1）：
  G1 覆盖完整：上游 JSON 的每个 anchor ID 至少一条溯源
  G2 无孤儿：ATTRIBUTION 的 anchor 均存在于上游
  G3 每条溯源均有文献依据（reference 非空）
  G4 年份合法（1800–2026 整数）
  G5 五册分组齐全（A/B/C/D/E 各 ≥3 条）
  G6 贡献者人数下限（≥25）
  G7 生成内容不含夸大/排名表述（禁词扫描）
  G8 幂等：条目 ID 唯一且可覆盖重写

幂等覆盖输出：数据/锚点库_溯源与科学家谱系.json / .md
"""
import json, io, os, sys, datetime

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(HERE, "..", "数据"))
SRC_JSON = os.path.join(OUT_DIR, "锚点库_前沿引力五册.json")

# ------------------------------------------------------------------
# 溯源台账：anchor ID → (奠基者, 年份, 奠基工作, 文献/出处)
# ------------------------------------------------------------------
ATTRIBUTION = [
    # ---------- A 全息原理 / AdS-CFT ----------
    ("A1", "德西特 (Willem de Sitter)", 1917,
     "给出常曲率真空解（含负曲率一支，即 anti-de Sitter）", "de Sitter 1917, Proc. Kon. Ned. Acad. Wet."),
    ("A1", "弗罗因德、鲁宾 (Freund & Rubin)", 1980,
     "11 维超引力的 AdS×S 紧化，使 AdS 进入弦论主舞台（AdS5×S5 的 IIB 版本随之确立）",
     "Freund & Rubin 1980, Phys. Lett. B97, 233"),
    ("A1", "马尔达西那 (J. Maldacena)", 1997,
     "AdS5/CFT4 对偶：体时空的 Einstein 方程 ⇔ 边界 CFT 的能动张量约束",
     "Maldacena 1997, Int. J. Theor. Phys. 38, 1113 [hep-th/9711200]"),
    ("A2", "古布泽、克莱巴诺夫、波利亚科夫 (GKP)", 1998,
     "全息字典：体标量质量 m² ↔ 边界算符维数 Δ", "Gubser, Klebanov, Polyakov 1998, Phys. Lett. B428, 105"),
    ("A2", "威滕 (E. Witten)", 1998,
     "系统给出 AdS/CFT 配分函数与关联函数字典（Δ± 两支解）", "Witten 1998, Adv. Theor. Math. Phys. 2, 253"),
    ("A2", "布赖滕洛纳、弗里德曼 (Breitenlohner & Freedman)", 1982,
     "AdS 中正能定理 ⇒ 稳定性下界 m²L² ≥ −d²/4（BF 束缚）",
     "Breitenlohner & Freedman 1982, Ann. Phys. 144, 249"),
    ("A3", "巴尼亚多斯、泰特尔博伊姆、扎内利 (BTZ)", 1992,
     "发现 (2+1) 维 AdS 黑洞解（BTZ）及其热力学量", "Bañados, Teitelboim, Zanelli 1992, PRL 69, 1849"),
    ("A3", "布朗、埃诺 (Brown & Henneaux)", 1986,
     "AdS3 渐近对称群的经典中心荷 c = 3L/(2G₃)（全息中心荷的原型）",
     "Brown & Henneaux 1986, Commun. Math. Phys. 104, 207"),
    ("A3", "斯特罗明格 (A. Strominger)", 1998,
     "由近视界微观态计数给出 BTZ 熵 = 边界 CFT₂ 的 Cardy 熵", "Strominger 1998, JHEP 02, 009"),
    ("A-INFO", "瑞宇、高柳 (Ryu & Takayanagi)", 2006,
     "全息纠缠熵 = 极小曲面面积 / 4G（RT 公式）", "Ryu & Takayanagi 2006, PRL 96, 181602"),
    ("A-INFO", "霍洛威茨等 (Hubeny, Rangamani, Takayanagi)", 2007,
     "RT 的协变推广（HRT，极端曲面）", "Hubeny, Rangamani, Takayanagi 2007, JHEP 07, 062"),
    ("A-INFO", "'t Hooft / 萨斯坎德 (G. 't Hooft, L. Susskind)", 1993,
     "全息原理的提出：体积内的自由度由边界面积计数", "'t Hooft 1993 [gr-qc/9310026]; Susskind 1995, J. Math. Phys. 36, 6377"),
    # ---------- B 黑洞信息悖论 ----------
    ("B1", "贝肯斯坦 (J. Bekenstein)", 1973,
     "黑洞熵正比于视界面积（S = η·A/ℓ_P²）", "Bekenstein 1973, Phys. Rev. D7, 2333"),
    ("B1", "霍金 (S. Hawking)", 1975,
     "霍金辐射与温度 T = ħc³/(8πGMk_B)，把熵系数钉死为 1/4",
     "Hawking 1975, Commun. Math. Phys. 43, 199"),
    ("B2", "巴丁、卡特、霍金 (Bardeen, Carter, Hawking)", 1973,
     "黑洞力学四定律，其中第一律 dM = T dS + ΩdJ + ΦdQ",
     "Bardeen, Carter, Hawking 1973, Commun. Math. Phys. 31, 161"),
    ("B3a", "佩奇 (D. Page)", 1993,
     "子系统平均纠缠熵的精确公式（Page 定理；本锚点的二阶矩版本）",
     "Page 1993, PRL 71, 1291"),
    ("B3a", "佩奇 (D. Page)", 1993,
     "黑洞辐射中的信息：Page 曲线（纠缠熵先升后降）", "Page 1993, PRL 71, 3743"),
    ("B3b", "佩奇 (D. Page)", 1993,
     "同上（蒙特卡洛交叉验证复现的正是 Page 的随机纯态平均）", "Page 1993, PRL 71, 1291"),
    ("B4", "彭宁顿 (G. Penington)", 2020,
     "纠缠楔重建与信息悖论（量子极值面 QES）", "Penington 2020, JHEP 09, 002"),
    ("B4", "Almheiri, Engelhardt, Marolf, Maxfield", 2019,
     "体场纠缠熵与蒸发黑洞的纠缠楔 ⇒ 岛公式", "AEMM 2019, JHEP 12, 063"),
    ("B4", "Almheiri, Mahajan, Maldacena, Zhao", 2019,
     "副本虫洞（replica wormhole）给出 Page 曲线的引力路径积分推导",
     "AMMZ 2019, JHEP 03, 149"),
    ("B4", "AMPS (Almheiri, Marolf, Polchinski, Sully)", 2012,
     "火墙悖论：把信息悖论 sharpen 为等价原理/幺正性/有效场论的三难",
     "AMPS 2013, JHEP 02, 062 [arXiv:1207.3123]"),
    # ---------- C 广义相对论 EFT / 后牛顿 ----------
    ("C1", "爱因斯坦 (A. Einstein)", 1915,
     "由广义相对论解释水星近日点反常进动（每百年 ≈43″）",
     "Einstein 1915, Sitzungsber. Preuss. Akad. Wiss."),
    ("C1", "洛伦兹、德罗斯特 (Lorentz & Droste)", 1917,
     "后牛顿（1PN）两体运动方程的系统形式", "Lorentz & Droste 1917, Versl. Kon. Akad. Wetensch. 26, 392"),
    ("C1", "威尔 (C. Will)", 1993,
     "PPN 参数化框架与实验检验的统一口径", "Will 1993, Theory and Experiment in Gravitational Physics"),
    ("C2", "彼得斯、马修斯 (Peters & Mathews)", 1963,
     "开普勒轨道双星的引力波能流（Peters 公式与 F(e) 因子）",
     "Peters & Mathews 1963, Phys. Rev. 131, 435"),
    ("C2", "赫尔斯、泰勒 (Hulse & Taylor)", 1974,
     "发现双中子星 PSR B1913+16，首次以轨道衰变间接证认引力波（1993 诺贝尔物理学奖）",
     "Hulse & Taylor 1975, ApJ 195, L51"),
    ("C2", "Weisberg & Huang", 2016,
     "长期计时给出实测/预言 = 0.9983 ± 0.0016（本锚点比对的发表值）",
     "Weisberg & Huang 2016, ApJ 829, 55"),
    ("C3", "爱因斯坦 (A. Einstein)", 1916,
     "弱场极限 g00 = −(1+2φ/c²) 与牛顿力学恢复（对应原理）",
     "Einstein 1916, Ann. Phys. 49, 769"),
    ("C3", "温伯格、MTW (Weinberg; Misner–Thorne–Wheeler)", 1972,
     "把牛顿极限写成可复算的教材推导链（测地线 → Γ^i_00 → −∇φ）",
     "Weinberg 1972, Gravitation and Cosmology; MTW 1973"),
    ("C4", "多诺霍 (J. Donoghue)", 1994,
     "广义相对论作为有效场论：把后牛顿展开与量子修正纳入 EFT 计数规则",
     "Donoghue 1994, Phys. Rev. D50, 3874"),
    ("C4", "Goldberger & Rothstein", 2006,
     "NRGR：引力束缚系统的有效场论重整化", "Goldberger & Rothstein 2006, Phys. Rev. D73, 104029"),
    # ---------- D 宇宙学微扰 / CMB ----------
    ("D1", "栗弗席兹 (E. Lifshitz)", 1946,
     "宇宙学微扰理论的开创（规范固定的度规扰动分解）", "Lifshitz 1946, J. Phys. (USSR) 10, 116"),
    ("D1", "萨克斯、沃尔夫 (Sachs & Wolfe)", 1967,
     "Sachs-Wolfe 效应：引力势起伏 → CMB 温度各向异性", "Sachs & Wolfe 1967, ApJ 147, 73"),
    ("D1", "Hu & Sugiyama / Bond & Efstathiou", 1996,
     "声学峰位置与声学视界的解析/半解析处理（ℓ_A 口径）",
     "Hu & Sugiyama 1996, ApJ 471, 542; Bond & Efstathiou 1984, ApJ 285, L45"),
    ("D1", "Planck Collaboration", 2020,
     "Planck 2018 参数（θ*、ℓ_A = 301.63 ± 0.15 等），本锚点比对的观测真源",
     "Planck 2018 results VI, A&A 641, A6"),
    ("D2", "古斯 (A. Guth) / 林德 (A. Linde) / 斯塔罗宾斯基 (A. Starobinsky)", 1981,
     "暴胀宇宙学（Guth 1981；Linde 1982 混沌暴胀 m²φ²；Starobinsky 1980）",
     "Guth 1981, Phys. Rev. D23, 347; Linde 1982, Phys. Lett. B108, 389; Starobinsky 1980, Phys. Lett. B91, 99"),
    ("D2", "Mukhanov & Chibisov", 1981,
     "暴胀量子涨落作为结构起源（标量扰动的量子产生）", "Mukhanov & Chibisov 1981, JETP Lett. 33, 532"),
    ("D2", "BICEP/Keck Collaboration & Planck", 2021,
     "张标比上限 r_{0.05} < 0.036（本锚点据以排除 m²φ² 模型的观测真源）",
     "BICEP/Keck 2021, Phys. Rev. Lett. 127, 151301"),
    ("D3", "巴丁 (J. Bardeen)", 1980,
     "规范不变的宇宙学微扰变量（ζ 型变量的源头）", "Bardeen 1980, Phys. Rev. D22, 1882"),
    ("D3", "穆哈诺夫 (V. Mukhanov) / 佐佐木 (M. Sasaki)", 1985,
     "Mukhanov-Sasaki 方程与规范不变量 ζ（本锚点的模函数方程）",
     "Mukhanov 1985, JETP Lett. 41, 493; Sasaki 1986, Prog. Theor. Phys. 76, 1036"),
    ("D3", "Mukhanov, Feldman & Brandenberger", 1992,
     "宇宙学微扰理论的系统化教科书口径（P_R = k³|ζ|²/2π²）",
     "MFB 1992, Phys. Rep. 215, 203"),
    ("D4", "马尔达西那 (J. Maldacena)", 2003,
     "单场暴胀非高斯性的三阶作用量计算 ⇒ 自洽关系 f_NL^local = (5/12)(1−n_s)",
     "Maldacena 2003, JHEP 05, 013"),
    ("D4", "Komatsu & Spergel", 2001,
     "CMB 双谱 f_NL 的观测估计量（本锚点登记的现代口径）",
     "Komatsu & Spergel 2001, Phys. Rev. D63, 063002"),
    ("D4", "Planck Collaboration", 2020,
     "Planck 2018 非高斯性束缚 f_NL^local = −0.9 ± 5.1", "Planck 2018 results IX, A&A 641, A9"),
    # ---------- E 渐近平直 / 邦迪-萨克斯 ----------
    ("E1", "史瓦西 (K. Schwarzschild)", 1916,
     "真空球对称解（本锚点的时空本体）", "Schwarzschild 1916, Sitzungsber. Preuss. Akad. Wiss."),
    ("E1", "芬克尔斯坦 / 爱丁顿 (Finkelstein; Eddington)", 1958,
     "消除坐标奇性的 Eddington-Finkelstein 坐标（retarded/advanced 两支）",
     "Finkelstein 1958, Phys. Rev. 110, 965; Eddington 1924, Nature 113, 192"),
    ("E2", "瓦迪亚 (P. Vaidya)", 1951,
     "辐射恒星的度规（Vaidya 解：m(u) 依赖 retard 时间的出射零尘埃）",
     "Vaidya 1951, Proc. Indian Acad. Sci. A33, 264"),
    ("E2", "邦迪、范德堡、梅茨纳、萨克斯 (BvBM + Sachs)", 1962,
     "渐近平直时空的 Bondi-Sachs 框架与质量损失（辐射正能流 ⇒ M_B 单调下降）",
     "Bondi, van der Burg, Metzner 1962, Proc. R. Soc. A269, 21; Sachs 1962, Proc. R. Soc. A270, 103"),
    ("E2", "特劳特曼 (A. Trautman)", 1958,
     "引力辐射的边界条件与正能定理（Trautman 质量）", "Trautman 1958, Bull. Acad. Pol. Sci. 6, 407"),
    ("E3", "爱因斯坦 (A. Einstein)", 1918,
     "四极辐射公式：P = (G/5c⁵)⟨I⃛_ij I⃛_ij⟩", "Einstein 1918, Sitzungsber. Preuss. Akad. Wiss."),
    ("E3", "朗道、栗弗席兹 (Landau & Lifshitz)", 1941,
     "把四极公式写成可复算的教科书推导（本锚点圆轨道平均的同款路径）",
     "Landau & Lifshitz, The Classical Theory of Fields"),
    ("E3", "彼得斯 (P. Peters)", 1964,
     "双星轨道衰变与 (32/5) 系数的显式结果（与 C2 同源）", "Peters 1964, Phys. Rev. 136, B1224"),
    ("E-INFO", "纽曼、彭罗斯 (Newman & Penrose)", 1962,
     "自旋系数形式与 news 函数（Bondi 质量损失公式的标准语言）",
     "Newman & Penrose 1962, J. Math. Phys. 3, 566"),
    ("E-INFO", "彭罗斯 (R. Penrose)", 1963,
     "共形无穷与零无穷 ℐ 的几何（渐近平直的现代定义）",
     "Penrose 1963, Phys. Rev. Lett. 10, 66"),
    ("E-INFO", "Christodoulou & Klainerman", 1993,
     "闵可夫斯基时空的全局非线性稳定性（渐近平直时空动力学基石）",
     "Christodoulou & Klainerman 1993, The Global Nonlinear Stability of the Minkowski Space"),
    ("E-INFO", "斯特罗明格等 (Strominger; Hawking, Perry, Strominger)", 2014,
     "BMS 超平移对称性、软定理与引力波记忆效应的三角关系",
     "Strominger 2014, JHEP 07, 152; Hawking, Perry, Strominger 2016, PRL 116, 231301"),
]

BAN_WORDS = ["排名第一", "史上最", "史上最强", "终极", "彻底颠覆", "完美", "显然", "无与伦比", "空前绝后"]

BOOKS = [
    ("A", "全息原理 / AdS-CFT", "A1", "A-INFO"),
    ("B", "黑洞信息悖论", "B1", "B4"),
    ("C", "广义相对论 EFT / 后牛顿", "C1", "C4"),
    ("D", "宇宙学微扰 / CMB", "D1", "D4"),
    ("E", "渐近平直 / 邦迪-萨克斯", "E1", "E-INFO"),
]

# ------------------------------------------------------------------
# 读取上游锚点库（单一真源）
# ------------------------------------------------------------------
if not os.path.exists(SRC_JSON):
    print("读取上游失败：%s（请先运行 锚点库_前沿引力五册A到E.py）" % SRC_JSON)
    sys.exit(1)
with io.open(SRC_JSON, "r", encoding="utf-8") as f:
    upstream = json.load(f)
upstream_ids = [c.get("id") for c in upstream.get("checks", [])]

rows = []
for i, (aid, scientist, year, contribution, reference) in enumerate(ATTRIBUTION):
    rows.append({
        "entry_id": "P%03d" % (i + 1),
        "anchor": aid,
        "scientist": scientist,
        "year": year,
        "contribution": contribution,
        "reference": reference,
    })

# ---------------- 门禁 ----------------
checks = []

def guard(gid, name, ok, detail):
    checks.append({"id": gid, "name": name, "ok": bool(ok), "detail": detail})

missing = [a for a in upstream_ids if a not in [r["anchor"] for r in rows]]
guard("G1", "覆盖完整：上游每条锚点均有溯源", not missing, "缺失: %s" % (missing if missing else "无"))

orphan = sorted({r["anchor"] for r in rows} - set(upstream_ids))
guard("G2", "无孤儿：溯源条目均对应上游锚点", not orphan, "孤儿: %s" % (orphan if orphan else "无"))

noref = [r["entry_id"] for r in rows if not (r.get("reference") or "").strip()]
guard("G3", "每条溯源均有文献依据", not noref, "缺文献: %s" % (noref if noref else "无"))

badyear = [r["entry_id"] for r in rows if not isinstance(r["year"], int) or not (1800 <= r["year"] <= 2026)]
guard("G4", "年份合法（1800–2026 整数）", not badyear, "非法: %s" % (badyear if badyear else "无"))

book_counts = []
for code, title, lo, hi in BOOKS:
    n = sum(1 for r in rows if r["anchor"].startswith(code if code != "A" else "A"))
    book_counts.append((code, title, n))
under = [b for b in book_counts if b[2] < 3]
guard("G5", "五册分组齐全（每册 ≥3 条溯源）", not under,
      "分册计数: %s；不足: %s" % (book_counts, under if under else "无"))

people = sorted({r["scientist"] for r in rows})
guard("G6", "贡献者人数下限（≥25）", len(people) >= 25, "实际 %d 条独立署名/组合" % len(people))

blob = "\n".join([r["contribution"] + r["reference"] + r["scientist"] for r in rows])
hits = [w for w in BAN_WORDS if w in blob]
guard("G7", "生成内容不含夸大/排名表述", not hits, "命中禁词: %s" % (hits if hits else "无"))

ids = [r["entry_id"] for r in rows]
guard("G8", "条目 ID 唯一（幂等可覆盖）", len(ids) == len(set(ids)), "条目数 %d" % len(ids))

all_ok = all(c["ok"] for c in checks)

# ---------------- 产物 ----------------
res = {
    "title": "经典基准锚点库 · 溯源与科学家谱系",
    "date": "2026-09-28",
    "upstream": os.path.basename(SRC_JSON),
    "upstream_verdict": upstream.get("verdict"),
    "redline": "不给人物排名、不作价值评判；「伟大」的唯一可核验口径 = 其奠基工作构成本锚点库不可绕过的结果",
    "guards": checks,
    "n_entries": len(rows),
    "n_people": len(people),
    "book_counts": [{"book": b[0], "title": b[1], "count": b[2]} for b in book_counts],
    "entries": rows,
    "people_index": sorted(people),
}

os.makedirs(OUT_DIR, exist_ok=True)
json_path = os.path.join(OUT_DIR, "锚点库_溯源与科学家谱系.json")
md_path = os.path.join(OUT_DIR, "锚点库_溯源与科学家谱系.md")

with io.open(json_path, "w", encoding="utf-8", newline="") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)

md = []
md.append("# 经典基准锚点库 · 溯源与科学家谱系")
md.append("")
md.append("| 项 | 值 |")
md.append("|---|---|")
md.append("| 日期 | 2026-09-28 |")
md.append("| 上游 | `%s`（%s） |" % (os.path.basename(SRC_JSON), upstream.get("verdict")))
md.append("| 条目 / 贡献者 | %d 条 / %d 位（或组合署名） |" % (len(rows), len(people)))
md.append("| 门禁 | %s |" % ("全部通过" if all_ok else "存在失败"))
md.append("")
md.append("> 红线：**不排名、不作价值评判**。「伟大」的唯一可核验口径 = 其奠基工作构成本锚点库某一不可绕过的结果。")
md.append("")
md.append("## 分册计数")
md.append("")
md.append("| 册 | 主题 | 溯源条数 |")
md.append("|---|---|---|")
for b in book_counts:
    md.append("| %s | %s | %d |" % (b[0], b[1], b[2]))
md.append("")
md.append("## 逐锚点溯源")
md.append("")
for r in rows:
    md.append("- **[%s] %s（%d）** — %s；出处：%s" % (
        r["anchor"], r["scientist"], r["year"], r["contribution"], r["reference"]))
md.append("")
md.append("## 门禁结果")
md.append("")
for c in checks:
    md.append("- %s `%s`：%s — %s" % ("OK" if c["ok"] else "FAIL", c["id"], c["name"], c["detail"]))
md.append("")
md.append("---")
md.append("")
md.append("*算法联盟审计组 · 锚点库溯源与科学家谱系 · 2026-09-28*")

with io.open(md_path, "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(md) + "\n")

print("===== 锚点库 · 溯源与科学家谱系 =====")
for c in checks:
    print("  [%s] %s %s — %s" % ("OK" if c["ok"] else "FAIL", c["id"], c["name"], c["detail"]))
print("条目 %d / 贡献者（组合署名）%d / 五册计数 %s" % (len(rows), len(people), book_counts))
print("产出:", json_path)
print("     ", md_path)
sys.exit(0 if all_ok else 1)
