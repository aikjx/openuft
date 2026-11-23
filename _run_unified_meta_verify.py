# -*- coding: utf-8 -*-
"""ASCII runner: JSON gate check + idempotent double-run for unified meta-audit."""
import glob
import hashlib
import json
import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))
HITS = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_统一方程元审计_*", "unified_label_audit.py"))
assert len(HITS) == 1, HITS
D = os.path.dirname(HITS[0])
JP = os.path.join(D, "_unified_label_meta.json")
RP = os.path.join(D, "_unified_label_meta_report.txt")


def digest(paths):
    h = hashlib.md5()
    for p in paths:
        with open(p, "rb") as f:
            h.update(f.read())
    return h.hexdigest()


runpy.run_path(HITS[0], run_name="__main__")
d1 = digest([JP, RP])
with open(JP, encoding="utf-8") as f:
    obj = json.load(f)

assert obj["verdict"].startswith("UNIFIED-LABEL-META--")
assert "U12-BREAKS-C0-C1-LEVEL-IMPLICATION-TRUE-ANOMALY" in obj["verdict"]
assert obj["verdict"].endswith("--NO-UFT-CLAIM")
assert obj["counts"] == {"gate": 9, "neg": 4, "identity": 0, "failed": 0}, obj["counts"]
assert len(obj["gates"]) == 13, len(obj["gates"])
assert all(g["ok"] is True for g in obj["gates"])
assert obj["independent_prediction_count"] == 0
assert obj["two_path"]["rows"] == 13 and obj["two_path"]["mismatch"] == 0
s = obj["strata"]
assert s["C3_unified"] == ["U01"]
assert s["C3_fourforce_unified"] == []
assert s["C2_unified_fourforce"] == ["U09", "U10"]
assert s["C0_false_positive"] == ["U03", "U04", "U05", "U06", "U09", "U10"]
assert s["C0_false_positive_rate"] == "6/7"

runpy.run_path(HITS[0], run_name="__main__")
d2 = digest([JP, RP])
assert d1 == d2, (d1, d2)
print("JSON-GATE-OK gates=13 all_ok=True counts=", obj["counts"])
print("IDEMPOTENT-MD5", d1, d2)
