# -*- coding: utf-8 -*-
"""
给 `数据/预测登记源_*.json` 逐条标注 `formula_origin`（幂等，可复跑）
=====================================================================
为什么必须加这一列
------------------
上一版引擎把三类东西放在同一张表里计分：

    (a) 由体系自身公设导出的式子
    (b) 从既有文献移植过来的已知数值关系（Wyler α、Koide K、Barut m_μ/m_e …）
    (c) 小整数搜索型 numerology（π/14、π/21、3/13、6π⁵ …）

三类一起算，S10 会拿到 A 档。但那个 A 说明的是
「仓库里存在几个已知的数值巧合」，不是「S10 的频率—复螺旋公设能解释任何东西」。
把 (b)(c) 洗成分数是计分规则本身的缺陷 —— 这与本联盟反复记录的
「伪派生」是同一个病，只是发生在元层面。

因此逐条推定来源，并让引擎同时输出两套口径：
    全口径 V3     —— 三类都算（不隐藏，作为上界）
    自身公设口径  —— 只算 (a)（这才是评价一个**体系**的分数）

取值：system_postulate / known_literature / numerology / imported_constant
推定依据写在 reason 里，可逐条复核推翻。这不是判决ng，是登记：若有异议改这里即可。
"""
import io
import os
import sys
import json
import glob

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT_DIR = os.path.join(ROOT, "04_公共成果", "算法联盟_全维自洽与归一化", "数据")

ORIGIN = {
    # ---- S01
    "S01-P001": ("imported_constant", "标准 MSSM 单圈 RGE 结果复现，非本体系输出"),
    # ---- S03
    "S03-P001": ("system_postulate", "GAQ 几何因子，母体为本体系"),
    "S03-P002": ("system_postulate", "9×K_{μe} 为本册构造"),
    "S03-P003": ("known_literature", "√(m_d/m_s) 为 Gatto–Sartori–Tonin 关系（1968）"),
    "S03-P004": ("system_postulate", "π₃(SU(3)) 绕数类论证为本体系构造"),
    "S03-P005": ("system_postulate", "m_n=m_0(n+1/2)² 为本册构造（但自相矛盾）"),
    # ---- S06
    "S06-P001": ("system_postulate", "Cl(4,4) 边界态论证为本体系构造"),
    # ---- S07
    "S07-P001": ("system_postulate", "α=τ/κ 为本体系 v4 核心式（M02 恒等式类）"),
    "S07-P002": ("system_postulate", "同上之倒数写法"),
    "S07-P003": ("system_postulate", "R_e/R_p 为本体系几何比"),
    "S07-P004": ("system_postulate", "χ=α+1/α 为本册构造"),
    # ---- S08
    "S08-P001": ("system_postulate", "v5 核心式；本体系自认未导出，另计 not_declared_derivation"),
    # ---- S09
    "S09-P001": ("numerology", "α^{-3} 为 α 的小整数幂搜索"),
    "S09-P002": ("numerology", "6π⁵/α 为已知 numerology"),
    "S09-P003": ("numerology", "α^{-3/2}√(2π) 同族第三次尝试"),
    # ---- S10
    "S10-P001": ("known_literature", "Wyler 1969 闭式 α=9/(16π³)(π/5!)^{1/4}，本册移植"),
    "S10-P002": ("numerology", "(4π³+π²+π)⁻¹ 为 π 的多项式搜索"),
    "S10-P003": ("numerology", "上一式加 −ζ(3)/4000 修正，系数为事后拟合"),
    "S10-P004": ("numerology", "Wyler×(1−πα³/2) 的事后修正"),
    "S10-P005": ("system_postulate", "螺旋恒等式 α=τ/κ 为本体系构造（M02 恒等式类）"),
    "S10-P006": ("known_literature", "Koide 1982 关系的 φ=arccos(−19/28) 变体"),
    "S10-P007": ("known_literature", "同上，同一关系的第二个输出"),
    "S10-P008": ("known_literature", "Barut 1979 m_μ/m_e=1+3/(2α)"),
    "S10-P009": ("numerology", "6π⁵ 为已知 numerology"),
    "S10-P010": ("known_literature", "Koide 不变量 K=2/3（Koide 1982）"),
    "S10-P011": ("known_literature", "K=2/3 的代数重排"),
    "S10-P012": ("numerology", "3/13 为小整数比搜索"),
    "S10-P013": ("numerology", "π/21 为 π/n 搜索"),
    "S10-P014": ("numerology", "π/14 为 π/n 搜索"),
    "S10-P015": ("known_literature", "Koide 角关系,同属 Koide 1982 族"),
    "S10-P016": ("known_literature", "Koide 族第三次出现"),
    # ---- S12
    "S12-P001": ("system_postulate", "α⁻¹=2π/θ 为本体系构造（M02 恒等式类）"),
    "S12-P002": ("system_postulate", "同上"),
    "S12-P003": ("system_postulate", "CLOSED-scale 标注，无数值"),
    "S12-P004": ("system_postulate", "谐波缠绕数 1:2:3 为本体系构造"),
    "S12-P005": ("system_postulate", "同上"),
    # ---- S13
    "S13-P001": ("system_postulate", "CP² 嵌入树级结果为本书构造"),
    "S13-P002": ("system_postulate", "闭式 s*=(3a+7A3)/(15a) 为本书构造(依赖 MSSM RGE 输入)"),
    "S13-P003": ("imported_constant", "统一耦合 α_GUT⁻¹，模型输出"),
    "S13-P004": ("system_postulate", "Z4 Frobenius-Schur 指标论证为本书构造"),
    # ---- S14
    "S14-P001": ("system_postulate", "SU(2):U(1)=3:1 维度比论证为本体系构造(已被同仓库实算否证)"),
    "S14-P002": ("system_postulate", "ξ_max 自屏蔽求解为本体系构造"),
    "S14-P003": ("system_postulate", "挠率拓扑环绕数主张为本体系构造(已被实算否证)"),
}


def main():
    files = sorted(glob.glob(os.path.join(OUT_DIR, "预测登记源_*.json")))
    if not files:
        print("未找到登记源 JSON")
        return 1
    path = files[-1]
    with io.open(path, encoding="utf-8") as fh:
        data = json.load(fh)

    hit, miss = 0, []
    for e in data["entries"]:
        cid = e.get("claim_id")
        if cid in ORIGIN:
            origin, reason = ORIGIN[cid]
            e["formula_origin"] = origin
            e["formula_origin_reason"] = reason
            hit += 1
        else:
            miss.append(cid)
            e.setdefault("formula_origin", "unclassified")

    data["meta"]["formula_origin_legend"] = {
        "system_postulate": "由体系自身公设导出 —— 评价该体系时只计这一类",
        "known_literature": "既有文献的已知数值关系，本册移植/再表述",
        "numerology": "小整数或 π/n 型搜索式（多重比较风险，已用 Bonferroni 处理）",
        "imported_constant": "取自外部模型/数据库的常量或输出",
        "unclassified": "本轮未推定（应为空，非空即为工具缺陷）",
    }

    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    print("登记源文件：%s" % os.path.basename(path))
    print("  已标注 %d 条；未推定 %d 条 %s" % (hit, len(miss), miss if miss else ""))
    from collections import Counter
    c = Counter(e.get("formula_origin") for e in data["entries"])
    for k, v in c.most_common():
        print("  %-20s %d" % (k, v))
    return 0 if not miss else 1


if __name__ == "__main__":
    sys.exit(main())
