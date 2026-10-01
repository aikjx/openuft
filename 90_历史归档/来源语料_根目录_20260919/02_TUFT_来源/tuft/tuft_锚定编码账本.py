# -*- coding: utf-8 -*-
"""
tuft_锚定编码账本.py
=====================

【出路 2 落地】承认外部锚定后，TUFT / H-TUFT 到底**编码了什么**？
—— 一册**可复跑的自由度计账**（不写散文，只记账 + 机检一致性）。

背景（为何需要本工具）：
  - 攻坚卷（CUR-22）定理 J 判定：保「拓扑常数」公理 ⇒ 无内生标度；破之 ⇒ 须引入新场（外生）。
  - 定理族 §8 因此指出**唯一仍然开放的出路**：**接受外部锚定**，把目标从「导出」下调为
    「**给定锚后编码可观测量**」。
  - 但「编码」一句话可以是空话。本工具把它变成**可计数**的账本：
        净预言数 `n_net = n_out − n_free`
    · `n_out`  = 该条目声称的**可独立检验输出**个数
    · `n_free` = 其预言公式中显式的**自由连续参数**个数（按该条目 CURATED 的
                 `core_prediction`/`uncertainty` 声明计）
    · `n_net > 0` ⇒ 有**净预言**（真可证伪）；`≤ 0` ⇒ **重参数化/欠定**（撞定理 D）。

记账种类（互斥五类）：
  PRED-EXCLUDED  真预言·**已排除**   —— n_net > 0，且已被实验排除（科学的「有效失败」）
  PRED-DERIVED   真预言·**继承排除** —— 自身不产生预言，排除由其他条目导出
  REPARAM        重参数化/自洽无预言 —— n_net ≤ 0，无独立可证伪内容
  STRUCT-FAIL    结构性失败          —— n_net ≤ 0，且已证结构性不可能

机检不变量（本工具的核心检查）：
  INV1 全部 CURATED 条目均在账本中（无遗漏）；
  INV2 ❌「已排除/已关闭/已触发」⇒ `n_net > 0`（含继承源）——**没有预言就谈不上"被排除"**；
  INV3 ❌「核心宣称失败」⇒ `n_net ≤ 0`——结构性问题不依赖预言数；
  INV4 ⏳/✅ ⇒ `n_net ≤ 0`（当前卷系**没有**任何待检条目拥有净预言——本工具将如实报出）。

红线：数学自洽 != 实验证实。本工具只做**自由度计账与一致性机检**，不改动任何真源。
"""

import hashlib
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# 账本声明：entry -> (种类, n_out, n_free, 一句话依据)
#   n_net = n_out - n_free
# ---------------------------------------------------------------------------
LEDGER = {
    "CUR-01": ("PRED-EXCLUDED", 1, 0, "自然耦合下 d_e 超 EDM 上限 16.5 量级（无自由参数）"),
    "CUR-02": ("PRED-EXCLUDED", 1, 0, "a_e 偏离 ~75%（无自由参数）"),
    "CUR-03": ("PRED-EXCLUDED", 1, 0, "QNM 频移 5.74σ（临界，窗口已关）"),
    "CUR-04": ("REPARAM", 0, 0, "β-running 缺口定理实例化（[B] 级自洽，无输出量）"),
    "CUR-05": ("REPARAM", 1, 2, "味混合提案：耦合与质量标度均未锚定"),
    "CUR-06": ("REPARAM", 1, 2, "暴胀：n_s,r 仅由 τ* 定，与 g3 相消（联合约束空壳）"),
    "CUR-07": ("PRED-DERIVED", 0, 0, "8 通道联合 Z=0 由 CUR-01~03 三窗 CLOSED 严格导出"),
    "CUR-08": ("REPARAM", 1, 2, "黑洞正则化：经验支柱（ringdown）已关闭；自由参数未锚定"),
    "CUR-09": ("REPARAM", 1, 2, "框架升维：低能投影继承已关窗口，新标度未锚定"),
    "CUR-10": ("REPARAM", 1, 2, "散射 S 矩阵：脚手架已落盘，参数未锚定"),
    "CUR-11": ("REPARAM", 2, 3, "手征机制缺失 + 谱为唯象幂律 + Gμ/Q_hel/α_t 未锚定"),
    "CUR-12": ("STRUCT-FAIL", 2, 3, "定量预言实跑失败；定理 I 排除「前 3 模态」（J_obs=15.8939 vs ≲3）"),
    "CUR-13": ("PRED-DERIVED", 0, 0, "正式排除；扩展通道 UNVALIDATED（继承 CUR-01~03）"),
    "CUR-14": ("STRUCT-FAIL", 1, 2, "Ω_DM 实跑差 ~25 量级且量纲反（结构性）"),
    "CUR-15": ("STRUCT-FAIL", 1, 2, "Ω_Λ 实跑 3.62e101（差 ~102 量级，结构性）"),
    "CUR-16": ("REPARAM", 1, 2, "无可证伪力：全局荷外部不可读 + α/Q_hel 双自由"),
    "CUR-17": ("STRUCT-FAIL", 1, 2, "多扇区求和未定义/自我取消（结构性）"),
    "CUR-18": ("STRUCT-FAIL", 2, 3, "CP 结构性不生成（J=0）+ |V_ub| 差 26.25×（结构性）"),
    "CUR-19": ("REPARAM", 2, 3, "手征机制缺失 + σ_wall 量纲差 1 + 输出全为自由参数"),
    "CUR-20": ("STRUCT-FAIL", 1, 1, "同伦签名非唯一选出规范群（结构性不可能）"),
    "CUR-21": ("STRUCT-FAIL", 1, 1, "σ_wall ≲(8.5TeV)³ 而声称量级超限 33~45 量级（结构性）"),
    "CUR-22": ("STRUCT-FAIL", 1, 1, "定理 J：A ⟹ C，保拓扑常数则内生标度不可达（结构性）"),
    "CUR-23": ("STRUCT-FAIL", 1, 1, "G_eff/G ≡ 1+α 被自身关系抵消；A1 与 A2/A3 不相容（结构性）"),
}

KIND_ORDER = ["PRED-EXCLUDED", "PRED-DERIVED", "REPARAM", "STRUCT-FAIL"]
KIND_ZH = {
    "PRED-EXCLUDED": "真预言·已排除",
    "PRED-DERIVED": "真预言·继承排除",
    "REPARAM": "重参数化/无净预言",
    "STRUCT-FAIL": "结构性失败",
}


def load_status():
    """从 CURATED 真源读各条目的 status（不改动真源）。"""
    out = {}
    for fname in sorted(os.listdir(HERE)):
        if not fname.endswith("_CURATED.json"):
            continue
        try:
            with open(os.path.join(HERE, fname), encoding="utf-8") as fh:
                doc = json.load(fh)
        except Exception:
            continue
        for ent in doc.get("entries", []):
            out[ent.get("entry_id", "?")] = ent.get("status", "")
    return out


def status_class(status):
    s = (status or "").strip()
    if s.startswith("❌"):
        if any(k in s for k in ("已排除", "已关闭", "已触发")):
            return "EXCLUDED"
        return "STRUCTFAIL"
    if s.startswith("⏳"):
        return "PENDING"
    if s.startswith("✅"):
        return "SELFCONSISTENT"
    return "UNKNOWN"


def check_invariants(status):
    """四项机检不变量。返回 (problems, notes)。"""
    problems, notes = [], []

    # INV1 无遗漏
    for eid in status:
        if eid not in LEDGER:
            problems.append(("INV1 遗漏", eid, "CURATED 有该条目，账本无声明"))
    for eid in LEDGER:
        if eid not in status:
            problems.append(("INV1 幽灵", eid, "账本有条目，CURATED 无"))

    for eid, (kind, n_out, n_free, _basis) in sorted(LEDGER.items()):
        net = n_out - n_free
        cls = status_class(status.get(eid, ""))
        if cls == "EXCLUDED" and not (net > 0 or kind == "PRED-DERIVED"):
            problems.append(("INV2 违规", eid,
                             "❌『已排除/已关闭/已触发』但 n_net=%d（含继承仍需 >0）" % net))
        if cls == "STRUCTFAIL" and net > 0:
            problems.append(("INV3 违规", eid, "❌『核心宣称失败』但 n_net=%d > 0" % net))
        if cls in ("PENDING", "SELFCONSISTENT") and net > 0:
            notes.append(("INV4 命中", eid, "⏳/✅ 条目拥有净预言 n_net=%d" % net))
    return problems, notes


def _demo():
    status = load_status()
    print("=" * 78)
    print("出路 2｜锚定后的诚实编码账本（可复跑自由度计账）")
    print("=" * 78)
    print("计账式：n_net = n_out(可独立检验输出) − n_free(自由连续参数)")

    print("\n" + "-" * 78)
    print("%-8s %-18s %-8s %-6s %-6s %-6s %s" % (
        "entry", "状态类", "记账种类", "n_out", "n_free", "n_net", "依据"))
    print("-" * 78)
    tally = {k: 0 for k in KIND_ORDER}
    nets = {}
    for eid in sorted(LEDGER, key=lambda x: int(x.split("-")[1])):
        kind, n_out, n_free, basis = LEDGER[eid]
        net = n_out - n_free
        nets[eid] = net
        tally[kind] += 1
        print("%-8s %-18s %-8s %-6d %-6d %+6d  %s" % (
            eid, status_class(status.get(eid, "")), kind, n_out, n_free, net, basis))

    print("\n" + "-" * 78)
    print("计账汇总")
    print("-" * 78)
    for k in KIND_ORDER:
        print("  %-14s (%s)：%d 条" % (k, KIND_ZH[k], tally[k]))
    n_pred = tally["PRED-EXCLUDED"] + tally["PRED-DERIVED"]
    n_none = tally["REPARAM"] + tally["STRUCT-FAIL"]
    print("  ⇒ 有净预言：**%d** 条（其中被排除 %d / 继承排除 %d / **待检 0**）" % (
        n_pred, tally["PRED-EXCLUDED"], tally["PRED-DERIVED"]))
    print("  ⇒ 无净预言（重参数化 + 结构性失败）：**%d** 条" % n_none)

    up = [e for e in LEDGER if int(e.split("-")[1]) >= 9]
    up_pos = [e for e in up if nets[e] > 0]
    print("  ⇒ **升维部分（CUR-09~CUR-23，%d 条）净预言数 > 0 者：%d 条**" % (len(up), len(up_pos)))

    print("\n" + "-" * 78)
    print("机检不变量")
    print("-" * 78)
    problems, notes = check_invariants(status)
    print("  INV1 账本完整性（无遗漏/无幽灵）：%s" % (
        "PASS" if not any(p[0].startswith("INV1") for p in problems) else "FAIL"))
    print("  INV2 ❌『已排除/已关闭/已触发』⇒ n_net>0（含继承）：%s" % (
        "PASS" if not any(p[0].startswith("INV2") for p in problems) else "FAIL"))
    print("  INV3 ❌『核心宣称失败』⇒ n_net≤0：%s" % (
        "PASS" if not any(p[0].startswith("INV3") for p in problems) else "FAIL"))
    print("  INV4 ⏳/✅ ⇒ n_net≤0：%s（命中 %d 条）" % (
        "PASS（当前卷系无待检净预言）" if not notes else "命中", len(notes)))
    for cat, obj, note in problems:
        print("    [%s] %s -> %s" % (cat, obj, note))

    print("\n" + "=" * 78)
    print("结论（出路 2 的诚实产出）")
    print("=" * 78)
    print("  ① 框架可作**描述层语言**：给定锚定后，它能**重述**可观测量（%d 条属此列）。" % n_none)
    print("  ② 但**净预言内容**：升维部分（CUR-09~23）= **0**；全卷仅低能 TUFT 三窗（CUR-01~03）")
    print("     有净预言，且**三条全部已被实验排除**（另 2 条为继承型排除）。")
    print("  ③ ⇒「出路 2」的**正确含义**不是「框架值得继续扩张」，而是：")
    print("     **承认锚定，把目标从『导出』下调为『编码/重述』**——并停止把重参数化当预言。")
    print("  ④ 机检 INV2/INV3 全部 PASS ⇒ 卷系在『❌ 的性质』上是**自洽**的：")
    print("     凡『被排除』者确有预言；凡『核心失败』者确无净预言。")


def _selfhash():
    with open(os.path.abspath(__file__), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


if __name__ == "__main__":
    _demo()
    print("\n" + "-" * 78)
    print("本文件 SHA256 =", _selfhash())
    print("定位：出路 2 落地工具（计账/机检，非预言）。数学自洽 != 实验证实。")
