# -*- coding: utf-8 -*-
"""
企业级统一验收内核（ASCII 文件名，可 import）—— TUFT 审计线的生产级基础设施。

承载三件事：
  1. discriminate()   —— 唯一权威的「发现 vs 拟合 vs 结构进展」验收门禁。
                         r334 / r340 此前各持一份*自含副本*；本模块是**单一真相源**，
                         未来册一律 `from _audit_acceptance import discriminate`，
                         杜绝「同判据多实现、语义漂移」的维护隐患（判据联盟门禁族⑦可证伪性的工程落地）。
  2. NumberReserver  —— 撞号防御。落盘前扫 源码/判定/数据 三树 + 探针/输出占位，
                         断言目标 rN 空闲；防止 r335 / r338 式「扫号全空 → 写大文件 → 被并行链占号」事故重演。
  3. load_triplet()   —— 读取既有卷的 json 三元组，供回归套件断言完整性（exit_code / 全 guard 通过 / verdict 非空）。

纪律（固化）：
  - 本模块是**新增基础设施**，不修改任何已定稿卷字节；r334 / r340 保留其自含副本是刻意选择
    （避免触碰与并行册共存的现状），新册从本模块 import 即可。仅出新册，不回填 README / 09。
  - 门禁门槛常量（1e-5 基准率、5σ 带）不写死 True；任何「零」结论必须配正对照（见 r345 卷 POSCTRL_*）。
"""
import os
import re
import json
from decimal import Decimal
from _criteria_kernel import surplus_of


# ---------------------------------------------------------------------------
# 1. 唯一权威验收门禁
# ---------------------------------------------------------------------------
def discriminate(label, *, candidate, center, sigma, n_matched, n_free,
                 is_fit_to_target, predicts_target_quantity, circular=False):
    """四问闸门：surplus≥1 ？ 在 5σ 带内 ？ 是否针对目标量 ？ 残差是否 < 基准率 1e-5 ？

    返回 verdict ∈ {RELATION_OR_FIT, FALSIFIED_AS_PREDICTION,
                     STRUCTURAL_ADVANCE_NOT_TARGET, NOTABLE_INDEPENDENT_PREDICTION,
                     GENUINE_PREDICTION}。
    """
    surplus = surplus_of(n_matched, n_free, circular=circular)
    within_band = abs(candidate - center) <= 5 * sigma
    # 防零除：center 为 0 时回落到绝对残差（极少触发，防御性）
    if center == 0:
        residual_rel = abs(candidate - center)
    else:
        residual_rel = abs(candidate - center) / abs(center)
    if surplus < 1:
        verdict = "RELATION_OR_FIT"
    elif not within_band:
        verdict = "FALSIFIED_AS_PREDICTION"
    elif is_fit_to_target:
        verdict = "RELATION_OR_FIT"
    elif not predicts_target_quantity:
        verdict = "STRUCTURAL_ADVANCE_NOT_TARGET"
    elif residual_rel < 1e-5:
        verdict = "NOTABLE_INDEPENDENT_PREDICTION"
    else:
        verdict = "GENUINE_PREDICTION"
    return {"label": label, "surplus": surplus, "within_band": within_band,
            "residual_rel": float(residual_rel), "verdict": verdict,
            "is_discovery_of_target": verdict in ("NOTABLE_INDEPENDENT_PREDICTION",
                                                  "GENUINE_PREDICTION")}


# ---------------------------------------------------------------------------
# 2. 撞号防御
# ---------------------------------------------------------------------------
class NumberReserver:
    TREES = ["源码", "判定", "数据"]

    def __init__(self, base):
        self.base = base

    def _hits(self, n, self_files=frozenset()):
        n = int(n)
        token = "r%d" % n
        hits = []
        for tree in self.TREES:
            d = os.path.join(self.base, tree)
            if not os.path.isdir(d):
                continue
            for fn in os.listdir(d):
                if fn in self_files:
                    continue
                if fn.startswith("TUFT-%s" % token) or ("_%s." % token) in fn or ("_%s_" % token) in fn:
                    hits.append(os.path.join(tree, fn))
        # 探针 / 输出占位（并行册占号热区）
        src = os.path.join(self.base, "源码")
        if os.path.isdir(src):
            for fn in os.listdir(src):
                if fn in self_files:
                    continue
                if fn in ("_probe_r%d.py" % n, "_out_r%d.txt" % n, "_run_r%d.py" % n):
                    hits.append(os.path.join("源码", fn))
        return hits

    def is_free(self, n, self_files=frozenset()):
        return (len(self._hits(n, self_files)) == 0), self._hits(n, self_files)

    def assert_free(self, n, self_files=frozenset()):
        free, hits = self.is_free(n, self_files)
        if not free:
            raise RuntimeError("r%d 已被占用: %s" % (int(n), hits))
        return True

    def occupied(self):
        seen = set()
        for tree in self.TREES:
            d = os.path.join(self.base, tree)
            if not os.path.isdir(d):
                continue
            for fn in os.listdir(d):
                for m in re.findall(r"r(\d{2,4})", fn):
                    seen.add(int(m))
        return sorted(seen)


# ---------------------------------------------------------------------------
# 3. 三元组读取（回归用）
# ---------------------------------------------------------------------------
def load_triplet(base, basename):
    p = os.path.join(base, "数据", basename + ".json")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def triplet_integrity(d):
    """断言：exit_code==0 且 全部 guard 通过 且 verdict 非空。返回 (ok, 摘要)。"""
    guards = d.get("guards", [])
    ok = (d.get("exit_code", 1) == 0) and (len(guards) > 0) and all(g.get("pass") for g in guards) and bool(d.get("verdict"))
    summary = {"verdict": d.get("verdict"), "exit_code": d.get("exit_code"),
               "guards_n": len(guards), "guards_all_pass": all(g.get("pass") for g in guards)}
    return ok, summary
