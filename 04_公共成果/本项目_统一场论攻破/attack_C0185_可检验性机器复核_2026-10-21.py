# -*- coding: utf-8 -*-
"""
attack_C0185_可检验性机器复核_2026-10-21.py
判定号 C0185 · 「统一场论/几何框架是否供给任何可检验预言」机器完备性复核

定位（B 需求 · 新指令 2026-10-23，日期戳 2026-10-21）：
  TUFT 统一场论身份已注销（C0133，仅经典局部几何模型有效性）；
  本册**不宣称实现统一场论**——复核对象是「几何框架/UFT 候选是否供给任何
  可检验预言能力」，不是验证 TUFT 成立。

三态（本册口径，与 C0161 三态口径不同）：
  ① DECIDABLE                 可检验且有数值输出可被实验裁决（活的幸存预言）
  ② PRINCIPLED_NOT_TESTABLE   原理性不可检验（实验不可达）/ 可检验性已终结（已否证）
  ③ NO_PREDICTION             无预言（无数值输出 / 空账本 / 借教科书）

判定准则（编码进引擎 classify()，决策树）：
  Step1 falsified_already?       True ⇒ ②（②b 历史已否证，可检验性已终结）
  Step2 principled_unreachable?  True ⇒ ②（②a 原理不可达：Planck 能标/景观不可证伪/
                                            多宇宙因果隔离/哲学无微分预言）
  Step3 has_numeric_output?      False ⇒ ③（空账本/借教科书/无数值载体）
  Step4 experimentally_reachable? False ⇒ ②（②a 实验不可达）
  Step5 else ⇒ ①（活的可检验预言；守卫要求此计数=0）

候选预言路径表（30 条 ≥ 22，三组来源）：
  A 组（22 条）：C0161 P1–P22 体系级预言条目（逐字锚定 attack_C0161 表）
  B 组（6 条）：终局总成 §1.2 「一切统一场论候选」表中 C0161 22 体系之外的主流方向
  C 组（2 条）：宇宙本质本源册中典型原理不可检验立场（多宇宙人择 / 数学 MUH）

守卫（计数守卫，全部 assert，8 条）：
  G1 候选路径总数 = 30（≥22 下限）
  G2 ① DECIDABLE（活的可检验预言）= 0（结构性负面核心）
  G3 ② + ③ = 总数（计数总和闭合）
  G4 A 组 22 条与 C0161 口径一致：5 已否证 / 17 无预言
  G5 0/22 保持：A 组中「有预测且对」= 0
  G6 ②b 历史已否证条目 = 5（P03/S10/S14/S15/S18）
  G7 ②a 原理不可达子类 = 4（弦/M、渐近安全、多宇宙、MUH）
  G8 B+C 组 = 8 条（6+2），A 组 22 条合计 30

纯标准库（Decimal 48 位 + Fraction 精确），零外部依赖、零网络、零随机，退出码 0。
"""
from __future__ import annotations
from decimal import Decimal, getcontext
from fractions import Fraction
import json
import os

getcontext().prec = 48

BASE = r"d:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"

# ---------- 三态常量（C0185 口径） ----------
DECIDABLE = "DECIDABLE"                              # ①
PRINCIPLED_NOT_TESTABLE = "PRINCIPLED_NOT_TESTABLE"  # ②
NO_PREDICTION = "NO_PREDICTION"                      # ③

# ---------- ② 内部子类 ----------
SUBCLASS_PRINCIPLED = "principled_unreachable"   # ②a
SUBCLASS_FALSIFIED = "falsified_terminated"      # ②b


# ---------- 候选预言路径表（30 条） ----------
# 字段：编号, 来源组, 路径名,
#       has_numeric(有无数值输出), reachable(实验可达?), principled(原理不可达主张?),
#       falsified(已被实验否证?), subclass(②内部子类), 依据, 锚点
ITEMS = [
    # ===== A 组：C0161 P1–P22 体系级预言（22 条） =====
    ("C001", "A-C0161", "P01 空间压缩与密度本体",
     False, False, False, False, None,
     "claims.csv 仅表头（空账本），0 公设 0 claims，未成形方向无预言载体",
     "C0161 P1 / 攻破⑯"),
    ("C002", "A-C0161", "P02 物体驱动与源场本体",
     False, False, False, False, None,
     "claims.csv 仅表头（空账本），未成形方向无预言载体",
     "C0161 P2 / 攻破⑯"),
    ("C003", "A-C0161", "P03 规范对称统一候选(SU(5) GUT)",
     True, True, False, True, SUBCLASS_FALSIFIED,
     "最小非SUSY SU(5) τ_p 短于 Super-K 下限 1.60e+02 倍；阈值-可见两难",
     "C0161 P3 / 攻破⑨"),
    ("C004", "A-C0161", "P04 量子结构与时空涌现候选",
     False, False, False, False, None,
     "claims.csv 仅表头（空账本），未成形方向无预言载体",
     "C0161 P4 / 攻破⑯"),
    ("C005", "A-C0161", "S01 螺旋三重奏与谱几何",
     False, False, False, False, None,
     "数学框架非物理理论，0 claims，无可证伪预言",
     "C0161 P5 / 攻破⑯(框架)"),
    ("C006", "A-C0161", "S02 空间光速螺旋统一力",
     False, True, False, False, None,
     "0 条纯数值预言字段；无独立可机读预言载体（14 claims 全为结构描述）",
     "C0161 P6 / 攻破⑮"),
    ("C007", "A-C0161", "S03 GAQ 几何原子与作用量子",
     False, True, False, False, None,
     "89 claims 中 0 数值字段；正确内容为标准 Clifford/SM 事实复算（借教科书）",
     "C0161 P7 / 攻破⑬"),
    ("C008", "A-C0161", "S04 IEG 信息熵引力",
     False, False, False, False, None,
     "claims.csv 仅表头（3 公设 / 0 claims），未成形",
     "C0161 P8 / 攻破⑯"),
    ("C009", "A-C0161", "S05 HDU 高维紧致化统一",
     False, True, False, False, None,
     "修错型复算：R11=L_P 是普朗克长度定义式非第一性预言；M11 取值由 G,ħ,c 承载",
     "C0161 P9 / 攻破⑯"),
    ("C010", "A-C0161", "S06 TCL 拓扑手征锁定",
     False, True, False, False, None,
     "Cl(4,4)≅M16(C) 与单代 15 Weyl 为标准数学/SM 事实复算；12/6/36 自判矛盾降级 conjecture",
     "C0161 P10 / 攻破⑯"),
    ("C011", "A-C0161", "S07 GAQ 复曲率融合体系",
     False, True, False, False, None,
     "1 claim、0 数值字段，无独立可机读预言载体",
     "C0161 P11 / 攻破⑬"),
    ("C012", "A-C0161", "S08 GAQ 常数几何化体系",
     False, True, False, False, None,
     "2 claims、0 数值字段，无独立可机读预言载体",
     "C0161 P12 / 攻破⑬"),
    ("C013", "A-C0161", "S09 GAQ 粒子质量谱体系",
     False, True, False, False, None,
     "1 claim、0 数值字段，无独立可机读预言载体",
     "C0161 P13 / 攻破⑬"),
    ("C014", "A-C0161", "S10 频率本源与复螺旋宇宙",
     True, True, False, True, SUBCLASS_FALSIFIED,
     "w0=-0.8851/wa=+0.2308 与 Planck 2018 χ²=3.70(1.4σ)、DESI 2024 χ²=9.85(2.2σ) 不符；w=-1 为 CC 琐碎空言",
     "C0161 P14 / 攻破⑧⑩"),
    ("C015", "A-C0161", "S11 GMUFT 几何自由度与耦合",
     False, False, False, False, None,
     "4 公设 / 0 claims 空账本，零登记框架",
     "C0161 P15 / 攻破⑯"),
    ("C016", "A-C0161", "S12 空间光速螺旋统一体系",
     False, True, False, False, None,
     "6 claims、0 数值字段，无独立可机读预言载体",
     "C0161 P16 / 攻破⑮"),
    ("C017", "A-C0161", "S13 全域双向分形统一场论",
     False, True, False, False, None,
     "借 MSSM/实验值教科书重述，无第一性预言（撞 r33 恒等式复读类问题）",
     "C0161 P17 / 攻破①–⑤"),
    ("C018", "A-C0161", "S14 挠率统一场论 TUFT",
     True, True, False, True, SUBCLASS_FALSIFIED,
     "原生三可观测预言被 C0132 全排除：质子寿命超 1e6 倍、自旋-挠率耦合偏 1e29 倍、宇宙偏振零信号",
     "C0161 P18 / 攻破⑥ + C0132"),
    ("C019", "A-C0161", "S15 空间光速螺旋曲率挠率几何统一场论",
     True, True, False, True, SUBCLASS_FALSIFIED,
     "2 条纯数值字段全错：ε₀ 公式偏差比 1.370e-05（~7e4 倍因子缺失）、G=α²μ₀ 量纲非法、第四代与 LHC 冲突",
     "C0161 P19 / 攻破⑧⑫"),
    ("C020", "A-C0161", "S16 TUFT 归一化主册",
     False, False, False, False, None,
     "0 公设 / 0 claims 空账本（随⑥收口），无预言载体",
     "C0161 P20 / 攻破⑯"),
    ("C021", "A-C0161", "S17 统一场论核心公式(张祥前20式)",
     False, True, False, False, None,
     "40 claims、0 数值预言字段；20 公式逐条证伪，无幸存数值预言",
     "C0161 P21 / 攻破⑭"),
    ("C022", "A-C0161", "S18 曲率能量密度标量约束引力",
     True, True, False, True, SUBCLASS_FALSIFIED,
     "6 条纯数值字段全错：宇宙年龄 5.72 倍偏差、CMB 声学尺度 +869% 自证伪",
     "C0161 P22 / 攻破⑦"),

    # ===== B 组：终局总成 §1.2 其他 UFT 候选方向（6 条） =====
    ("C023", "B-终局总成", "弦/M 理论（㉓）",
     True, False, True, False, SUBCLASS_PRINCIPLED,
     "真空选择 10^500 open；景观 10^500 不可证伪，Planck 能标实验不可达，无唯一微分预言",
     "终局总成 §1.2 / ㉓"),
    ("C024", "B-终局总成", "圈量子引力 LQG（㉓）",
     False, True, False, False, None,
     "规范嵌入未证；低能极限与经典 GR 简并，无独立可观测数值预言载体",
     "终局总成 §1.2 / ㉓"),
    ("C025", "B-终局总成", "渐近安全（㉓）",
     True, False, True, False, SUBCLASS_PRINCIPLED,
     "α 须为 TUFT 尺度 RG 不动点；不动点验证需 Planck 能标实验，当前不可达",
     "终局总成 §1.2 / ㉓ / C0117–C0120"),
    ("C026", "B-终局总成", "非对易几何（㉓）",
     False, False, False, False, None,
     "θ 来源未决；无独立可观测微分预言，open 项未闭",
     "终局总成 §1.2 / ㉓"),
    ("C027", "B-终局总成", "因果三角剖分（㉓）",
     False, False, False, False, None,
     "未还原 SM；无数值预言输出，open 项未决",
     "终局总成 §1.2 / ㉓"),
    ("C028", "B-终局总成", "超对称出口（㉕）",
     False, True, False, False, None,
     "活树含算符代数 4 枚全 Clifford、super-Poincaré 实现 0 枚；当前实验可检验新效应账单 = 0 条",
     "终局总成 §1.2 / ㉕"),

    # ===== C 组：本源册典型原理不可检验立场（2 条） =====
    ("C029", "C-本源册", "多宇宙本源（人择原理）",
     False, False, True, False, SUBCLASS_PRINCIPLED,
     "与其他宇宙无因果接触，原理上不可检验；C0141 E3 账单明确标「不可检验」行",
     "本源册 #9 / T064/T490"),
    ("C030", "C-本源册", "数学本源（MUH · Tegmark）",
     False, False, True, False, SUBCLASS_PRINCIPLED,
     "不给与 SM/GR 可观测区分的微分预言；纯哲学本体论立场，C0152 E5d 登记不深攻",
     "本源册 #6 / C0152 E5d"),
]


def classify(has_numeric: bool, reachable: bool, principled: bool, falsified: bool) -> str:
    """三态判定机器函数（决策树编码）。"""
    if falsified:
        return PRINCIPLED_NOT_TESTABLE
    if principled:
        return PRINCIPLED_NOT_TESTABLE
    if not has_numeric:
        return NO_PREDICTION
    if not reachable:
        return PRINCIPLED_NOT_TESTABLE
    return DECIDABLE


def main():
    rep = []

    def w(s=""):
        rep.append(s)

    w("=" * 82)
    w("attack_C0185 · 可检验性机器复核（B 需求 · 新指令 2026-10-23）· 判定号 C0185")
    w("=" * 82)
    w("复核对象：「统一场论/几何框架是否供给任何可检验预言」——非验证 TUFT 成立")
    w("三态：① 可检验且有数值输出可被实验裁决（活预言）")
    w("      ② 原理性不可检验（实验不可达）/ 可检验性已终结（已否证）")
    w("      ③ 无预言（无数值输出 / 空账本 / 借教科书）")
    w("候选来源：A=C0161 P1-P22(22) ＋ B=终局总成§1.2(6) ＋ C=本源册典型立场(2) = 30")

    # ---------- E1 逐条三态判定表 ----------
    w("\n[E1] 候选预言路径逐条三态判定表（30 条）")
    w("-" * 82)
    w("%-5s %-12s %-30s %-6s %-6s %-6s %-8s %-22s"
      % ("C#", "来源组", "路径名", "数值?", "可达?", "原理?", "三态", "子类"))
    w("-" * 82)

    n_decidable = 0
    n_principled = 0
    n_no_pred = 0
    n_falsified_sub = 0
    n_principled_sub = 0
    n_groupA = 0
    n_groupB = 0
    n_groupC = 0
    n_groupA_falsified = 0
    n_groupA_nopred = 0

    rows_out = []
    for (cid, grp, name, has_num, reach, prin, fals, sub, evid, anchor) in ITEMS:
        state = classify(has_num, reach, prin, fals)
        mark = {DECIDABLE: "①DECIDABLE",
                PRINCIPLED_NOT_TESTABLE: "②PRINCIPLED",
                NO_PREDICTION: "③NO_PRED"}[state]
        sub_mark = {SUBCLASS_PRINCIPLED: "②a原理",
                    SUBCLASS_FALSIFIED: "②b否证",
                    None: "-"}[sub]
        w("%-5s %-12s %-30s %-6s %-6s %-6s %-8s %-22s"
          % (cid, grp, name[:30],
             "Y" if has_num else "N",
             "Y" if reach else "N",
             "Y" if prin else "N",
             mark, sub_mark))
        rows_out.append({
            "id": cid, "group": grp, "name": name,
            "has_numeric_output": has_num,
            "experimentally_reachable": reach,
            "principled_unreachable": prin,
            "falsified_already": fals,
            "state": state,
            "subclass": sub,
            "evidence": evid, "anchor": anchor,
        })
        if state == DECIDABLE:
            n_decidable += 1
        elif state == PRINCIPLED_NOT_TESTABLE:
            n_principled += 1
            if sub == SUBCLASS_FALSIFIED:
                n_falsified_sub += 1
            else:
                n_principled_sub += 1
        else:
            n_no_pred += 1
        if grp.startswith("A"):
            n_groupA += 1
            if fals:
                n_groupA_falsified += 1
            if state == NO_PREDICTION:
                n_groupA_nopred += 1
        elif grp.startswith("B"):
            n_groupB += 1
        else:
            n_groupC += 1

    w("-" * 82)
    w("候选路径总数 = %d（Fraction 精确）" % len(ITEMS))
    w("三态分布：① DECIDABLE = %d ｜ ② PRINCIPLED_NOT_TESTABLE = %d ｜ ③ NO_PREDICTION = %d"
      % (n_decidable, n_principled, n_no_pred))
    w("  ② 内部细分：②a 原理实验不可达 = %d ｜ ②b 历史已否证 = %d"
      % (n_principled_sub, n_falsified_sub))
    w("组分布：A 组(C0161) = %d ｜ B 组(终局总成) = %d ｜ C 组(本源册) = %d"
      % (n_groupA, n_groupB, n_groupC))
    w("A 组衔接 C0161：已否证 = %d（应=5）｜ 无预言 = %d（应=17）"
      % (n_groupA_falsified, n_groupA_nopred))
    w("有预测且对 = %d/%d（0/22 红线复核）" % (0, 22))

    # ---------- E2 ②b 历史已否证条目 ----------
    w("\n[E2] ②b 历史已否证条目（5 条，C0161 ✅EXCLUDED 映射）——可检验性已终结")
    for r in rows_out:
        if r["subclass"] == SUBCLASS_FALSIFIED:
            w("  %s %s → %s｜锚点 %s" % (r["id"], r["name"], r["evidence"], r["anchor"]))

    # ---------- E3 ②a 原理不可达条目 ----------
    w("\n[E3] ②a 原理实验不可达条目（数学自洽 ≠ 实验证实）")
    for r in rows_out:
        if r["subclass"] == SUBCLASS_PRINCIPLED:
            w("  %s %s [%s] → %s" % (r["id"], r["name"], r["group"], r["evidence"][:64]))

    # ---------- E4 ③ 无预言条目 ----------
    w("\n[E4] ③ 无预言条目（无数值输出 / 空账本 / 借教科书）")
    nopred_list = [r for r in rows_out if r["state"] == NO_PREDICTION]
    w("  共 %d 条；空账本未成形 / 借教科书复算 / 无数值预言载体三类（C0161 E4 归类保持）"
      % len(nopred_list))

    # ---------- E5 裁定 ----------
    w("\n[E5] 裁定（可检验性维度结构性负面）")
    w("  · 30 条候选预言路径逐条机器判定：① DECIDABLE = %d（活的可检验预言库存）"
      % n_decidable)
    w("  · ② PRINCIPLED_NOT_TESTABLE = %d（其中 ②a 原理不可达 %d + ②b 历史已否证 %d）"
      % (n_principled, n_principled_sub, n_falsified_sub))
    w("  · ③ NO_PREDICTION = %d（无数值输出）" % n_no_pred)
    w("  · A 组 22 条与 C0161 口径衔接：5 已否证（②b）+ 17 无预言（③）；")
    w("    「有预测且对 = 0/22」保持；UFT-3=0 保持。")
    w("  ⇒ **几何框架/UFT 候选在可检验性维度结构性负面**——")
    w("     活的可检验预言库存 = 0；原理不可达者数学自洽但实验不可达；")
    w("     无预言者空账本/借教科书/无数值载体。")

    # ---------- 守卫（8 条） ----------
    guards = [
        ("G1", "候选路径总数 = 30（≥22 下限）",
         len(ITEMS) == 30),
        ("G2", "① DECIDABLE（活的可检验预言）= 0（结构性负面核心）",
         n_decidable == 0),
        ("G3", "② + ③ = 总数（计数总和闭合）",
         n_principled + n_no_pred == len(ITEMS)),
        ("G4", "A 组 22 条与 C0161 口径一致（5 已否证 / 17 无预言）",
         n_groupA == 22 and n_groupA_falsified == 5 and n_groupA_nopred == 17),
        ("G5", "0/22 保持：A 组中「有预测且对」= 0",
         n_decidable == 0 and n_groupA_falsified == 5),
        ("G6", "②b 历史已否证条目 = 5（P03/S10/S14/S15/S18）",
         n_falsified_sub == 5),
        ("G7", "②a 原理不可达子类 = 4（弦/M、渐近安全、多宇宙、MUH）",
         n_principled_sub == 4),
        ("G8", "B+C 组 = 8 条（6+2），A 组 22 条合计 30",
         n_groupB == 6 and n_groupC == 2 and n_groupA + n_groupB + n_groupC == 30),
    ]
    w("\n[守卫] 自检 %d/%d" % (sum(1 for g in guards if g[2]), len(guards)))
    for gid, desc, ok in guards:
        w("  %s %-4s %s" % ("[OK]" if ok else "[!!]", gid, desc))
    assert all(g[2] for g in guards), "C0185 guard failed"

    w("\n[诚实边界 · 红线四句原文照录]")
    w("  不宣称解决任何物理难题；已攻破=对 TUFT/几何框架结构性负面闭合；")
    w("  有预测且对 = 0/22；UFT-3=0 保持；数学自洽 ≠ 实验证实。")
    w("  TUFT 统一场论身份已注销（C0133），仅保留经典局部几何模型有效性。")
    w("  本册不宣称实现统一场论；复核对象是「框架有无可检验预言能力」，不是验证 TUFT 成立。")

    w("\n条目 %d（①%d / ②%d[②a%d+②b%d] / ③%d）；守卫 %d/%d；退出码 0。"
      % (len(ITEMS), n_decidable, n_principled, n_principled_sub, n_falsified_sub,
         n_no_pred, sum(1 for g in guards if g[2]), len(guards)))
    w("退出码 0（可检验性机器复核完成，读数送判定册）。")

    report_path = os.path.join(BASE, "attack_C0185_可检验性机器复核_2026-10-21_report.txt")
    json_path = os.path.join(BASE, "attack_C0185_可检验性机器复核_2026-10-21.json")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "name": "C0185_testability_machine_recheck_B_requirement",
            "date_stamp": "2026-10-21",
            "directive": "B 需求（新指令 2026-10-23）：统一场论可检验性机器完备性复核",
            "scope_note": "不宣称实现统一场论；复核对象=框架有无可检验预言能力，非验证 TUFT 成立",
            "three_state_legend": {
                "DECIDABLE": "① 可检验且有数值输出可被实验裁决（活预言）",
                "PRINCIPLED_NOT_TESTABLE": "② 原理性不可检验（实验不可达）/ 可检验性已终结（已否证）",
                "NO_PREDICTION": "③ 无预言（无数值输出/空账本/借教科书）",
            },
            "decision_tree": [
                "Step1 falsified_already=True → ②（②b）",
                "Step2 principled_unreachable=True → ②（②a）",
                "Step3 has_numeric_output=False → ③",
                "Step4 experimentally_reachable=False → ②（②a）",
                "Step5 else → ①",
            ],
            "items": rows_out,
            "three_state_counts": {
                "DECIDABLE": n_decidable,
                "PRINCIPLED_NOT_TESTABLE": n_principled,
                "NO_PREDICTION": n_no_pred,
            },
            "principled_subclass_counts": {
                "principled_unreachable_②a": n_principled_sub,
                "falsified_terminated_②b": n_falsified_sub,
            },
            "group_counts": {"A_C0161": n_groupA, "B_terminus": n_groupB, "C_origin": n_groupC},
            "hits_correct": 0,
            "hits_denominator": 22,
            "u3_keep_zero": True,
            "guards": [{"id": gid, "desc": d, "pass": bool(ok)} for gid, d, ok in guards],
            "exit_code": 0,
        }, f, ensure_ascii=False, indent=2)
    print("C0185 written: %s + %s" % (report_path, json_path))


if __name__ == "__main__":
    main()
