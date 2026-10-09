# -*- coding: utf-8 -*-
"""证伪阈值门禁 · 牙齿（变异驱动）
================================================================================

做法（与仓库既有牙齿同款纪律）：
1. 在**临时目录**里造一份**干净夹具**（1 个体系 × 2 条合法登记）；
2. 把 `空间螺旋_证伪阈值门禁.py` **整份复制**进临时目录，用 importlib 从副本导入；
3. 逐个植入缺陷后重跑 `judge()`，要求每个变异体把**点名的那条判据**打红；
4. 另加一条**良性改动**（只改 statement 文案）必须 **CLEAN**（不得误报）；
5. 基线必须全绿，否则整轮 `INVALID`（夹具自己没电时不许冒充通过）。

要求：崩溃不算捕获；每个变异体只点名一条判据；`missed` / `false_alarm` 必须为空。
产物：`数据/空间螺旋_证伪阈值门禁_牙齿.json`（退出码即结论）。
"""

import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))          # -> openuft
OUT_DIR = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")
ENGINE = os.path.join(HERE, "空间螺旋_证伪阈值门禁.py")

HEADER = ["claim_id", "hypothesis_revision", "statement", "assumptions",
          "derivation", "prediction", "prediction_value", "prediction_urel",
          "run_id", "data_id", "uncertainty", "evidence_level", "status", "reviewer"]

CLEAN = [
    ["FIX-C0001", "rev-1", "合成靶一（m_W 预测）", "A1", "d1", "m_W",
     "80.409", "0.00015", "r1", "obs_mW_PDG", "PDG 80.377±0.012", "数值", "open", "teeth"],
    ["FIX-C0002", "rev-1", "合成靶二（统一点）", "A1", "d2", "M_GUT",
     "2.0e16", "0.05", "r2", "obs_tau_p_SK", "SK >2.4e34 yr", "数值", "open", "teeth"],
    # 第三条刻意**不声明预测**：用来走通"未声明预测 ⇒ 不是候选"那条分支（M10 需要它）
    ["FIX-C0003", "rev-1", "未声明预测的条目（恒等式类）", "A1", "d3", "",
     "", "", "r3", "obs_none", "", "代数恒等式", "verified", "teeth"],
]

# 变异体：(编号, 点名判据, 说明, 变换函数(csv_text, engine_text) -> (csv_text, engine_text))
ANCHOR_SKIP = "                    continue                      # 未声明预测 ⇒ 不是候选"


def m_misalign(csv_text, eng):
    lines = csv_text.rstrip("\n").split("\n")
    lines[1] = lines[1] + ",EXTRA,EXTRA2"          # 行宽 ≠ 表头宽
    return "\n".join(lines) + "\n", eng


def m_nonnumeric(csv_text, eng):
    lines = csv_text.rstrip("\n").split("\n")
    parts = lines[1].split(",")
    parts[6] = "MSSM M_GUT=2.0e16 GeV; spread=5.58"   # 数值列被自由文本占用
    lines[1] = ",".join(parts)
    return "\n".join(lines) + "\n", eng


def m_half(csv_text, eng):
    lines = csv_text.rstrip("\n").split("\n")
    parts = lines[2].split(",")
    parts[7] = ""                                     # 只填 value 不填 urel
    lines[2] = ",".join(parts)
    return "\n".join(lines) + "\n", eng


def m_urel_zero(csv_text, eng):
    lines = csv_text.rstrip("\n").split("\n")
    parts = lines[1].split(",")
    parts[7] = "0"                                    # urel 非正
    lines[1] = ",".join(parts)
    return "\n".join(lines) + "\n", eng


def m_no_obs(csv_text, eng):
    lines = csv_text.rstrip("\n").split("\n")
    parts = lines[1].split(",")
    parts[9] = ""
    parts[10] = ""                                    # 无观测侧
    lines[1] = ",".join(parts)
    return "\n".join(lines) + "\n", eng


def m_hardcode(csv_text, eng):
    old = "    return 2 * erfinv(mpf(\"0.95\")) ** 2"
    if old not in eng:
        raise RuntimeError("anchor-missing: erfinv")
    return csv_text, eng.replace(old, "    return mpf(\"3.84145882069\")")


def m_wrong_sqrt(csv_text, eng):
    old = "dmin = sigma * sqrt(chi2_crit_closed_form())"
    if old not in eng:
        raise RuntimeError("anchor-missing: sqrt")
    return csv_text, eng.replace(old, "dmin = sigma * chi2_crit_closed_form()")


def m_drop_rows(csv_text, eng):
    lines = csv_text.rstrip("\n").split("\n")
    for i in (1, 2):
        parts = lines[i].split(",")
        parts[6] = ""
        parts[7] = ""
        parts[5] = ""
        lines[i] = ",".join(parts)
    return "\n".join(lines) + "\n", eng


def m_header(csv_text, eng):
    lines = csv_text.rstrip("\n").split("\n")
    head = lines[0].split(",")
    head.remove("prediction_urel")
    lines[0] = ",".join(head)
    return "\n".join(lines) + "\n", eng


def m_unbalanced(csv_text, eng):
    """在"未声明预测 ⇒ 不是候选"那条 continue 之前多计一次候选 ⇒ 账目失衡（G11）。"""
    import re as _re
    pat = _re.compile(r"^([ \t]*)continue[ \t]*#\s*未声明预测", _re.M)
    m = pat.search(eng)
    if not m:
        raise RuntimeError("anchor-missing: skip")
    indent = m.group(1)
    new = pat.sub(indent + "candidates += 1\n" + indent + "continue  # 未声明预测", eng, count=1)
    return csv_text, new


def m_no_registry(csv_text, eng):
    """不改数据、不改引擎：只把"单一真源"指向一个不存在的文件 ⇒ G0 必须变红。"""
    return csv_text, eng


def benign(csv_text, eng):
    lines = csv_text.rstrip("\n").split("\n")
    parts = lines[1].split(",")
    parts[2] = "合成靶一（仅改文案，语义不动）"
    lines[1] = ",".join(parts)
    return "\n".join(lines) + "\n", eng


MUTANTS = [
    ("M1", "G2", "某行多两列（模拟 S15 的 16 vs 14）", m_misalign),
    ("M2", "G3", "prediction_value 被自由文本占用（模拟 P03）", m_nonnumeric),
    ("M3", "G4", "只填 value 不填 urel", m_half),
    ("M4", "G5", "urel = 0", m_urel_zero),
    ("M5", "G6", "data_id 与 uncertainty 全空", m_no_obs),
    ("M6", "G8", "χ²_crit 改回硬编码常量", m_hardcode),
    ("M7", "G9", "δ_min 漏掉根号", m_wrong_sqrt),
    ("M8", "G7", "删掉全部登记数值 ⇒ UFT-3 = 0", m_drop_rows),
    ("M9", "G1", "表头删掉 prediction_urel 列", m_header),
    ("M10", "G11", "候选计数多计一条（账目失衡）", m_unbalanced),
    ("M11", "G0", "单一真源指向不存在的文件 ⇒ 委托失效", m_no_registry),
]
BENIGN = ("B1", "-", "只改 statement 文案（良性）", benign)


def write_fixture(root, csv_text):
    d = os.path.join(root, "FIX_夹具体系")
    os.makedirs(d, exist_ok=True)
    with io.open(os.path.join(d, "claims.csv"), "w", encoding="utf-8", newline="") as f:
        f.write(csv_text)


def load_engine(engine_path):
    spec = importlib.util.spec_from_file_location("gate_" + str(abs(hash(engine_path))), engine_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_case(tmp, csv_text, engine_text, gid, env_registry=None):
    if env_registry:
        os.environ["UFT3_REGISTRY_GATE"] = env_registry
    case_dir = os.path.join(tmp, "case_" + gid + "_" + str(time.time_ns()))
    sys_root = os.path.join(case_dir, "01_独立体系")
    os.makedirs(sys_root, exist_ok=True)
    write_fixture(sys_root, csv_text)
    ep = os.path.join(case_dir, "gate.py")
    with io.open(ep, "w", encoding="utf-8") as f:
        f.write(engine_text)
    mod = load_engine(ep)
    gates, _, _, _ = mod.judge(sys_root)
    return gates


def main():
    base_csv = ",".join(HEADER) + "\n" + "\n".join(",".join(r) for r in CLEAN) + "\n"
    with io.open(ENGINE, encoding="utf-8") as f:
        base_eng = f.read()

    results = []
    missed, false_alarm = [], []
    # 副本在临时目录里，副本旁边没有真源 ⇒ 用环境变量指回仓库里的单一真源
    REG_REAL = os.path.join(HERE, "靶场登记列校验_写入侧门禁.py")
    tmp = tempfile.mkdtemp(prefix="uft3_teeth_")
    try:
        # ---- 基线必须全绿 ----
        gates0 = run_case(tmp, base_csv, base_eng, "baseline", env_registry=REG_REAL)
        bad0 = [g for g in gates0 if not gates0[g]["ok"]]
        if bad0:
            print("INVALID：基线未全绿 —— %s" % ",".join(bad0))
            return 2
        print("基线：%d 条判据全 PASS" % len(gates0))

        for mid, gid, desc, fn in MUTANTS + [BENIGN]:
            try:
                csv2, eng2 = fn(base_csv, base_eng)
            except RuntimeError as e:
                results.append({"id": mid, "gate": gid, "desc": desc,
                                "status": "ANCHOR-MISSING", "detail": str(e)})
                missed.append(mid)
                print("%-4s %-4s %-16s %s" % (mid, gid, "ANCHOR-MISSING", desc))
                continue
            env_reg = REG_REAL
            if mid == "M11":      # 把真源指向不存在的文件
                env_reg = os.path.join(tmp, "不存在的真源.py")
            gates = run_case(tmp, csv2, eng2, mid, env_registry=env_reg)
            if mid.startswith("B"):
                flipped = [g for g in gates if not gates[g]["ok"]]
                ok = not flipped
                status = "CLEAN" if ok else "FALSE-ALARM"
                if not ok:
                    false_alarm.append(mid)
                detail = ",".join(flipped) if flipped else "无任何判据变红"
            else:
                ok = (gid in gates) and (not gates[gid]["ok"])
                status = "CAUGHT" if ok else "MISS"
                if not ok:
                    missed.append(mid)
                detail = ("点名判据 %s → %s" % (gid, gates[gid]["verdict"])) if gid in gates else "判据缺失"
            results.append({"id": mid, "gate": gid, "desc": desc,
                            "status": status, "detail": detail})
            print("%-4s %-4s %-16s %s" % (mid, gid, status, desc))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    total = len(MUTANTS) + 1
    caught = sum(1 for r in results if r["status"] == "CAUGHT")
    clean = sum(1 for r in results if r["status"] == "CLEAN")
    ok_all = (not missed) and (not false_alarm)
    payload = {"generated": time.strftime("%Y-%m-%d %H:%M:%S"),
               "total_cases": total, "mutants": len(MUTANTS), "caught": caught,
               "benign_clean": clean, "missed": missed, "false_alarm": false_alarm,
               "verdict": "PASS" if ok_all else "FAIL", "results": results}
    os.makedirs(OUT_DIR, exist_ok=True)
    with io.open(os.path.join(OUT_DIR, "空间螺旋_证伪阈值门禁_牙齿.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("判定 %s ｜ 变异体 %d/%d CAUGHT ｜ 良性 %d CLEAN ｜ missed=%s ｜ false_alarm=%s"
          % (payload["verdict"], caught, len(MUTANTS), clean, missed or "无", false_alarm or "无"))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
