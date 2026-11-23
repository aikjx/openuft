# -*- coding: utf-8 -*-
"""ASCII runner: JSON gate check + idempotent double-run for exit-zero audit."""
import glob
import hashlib
import json
import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))
HITS = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_出口归零元审计_*", "exit_zero_audit.py"))
assert len(HITS) == 1, HITS
D = os.path.dirname(HITS[0])
JP = os.path.join(D, "_exit_zero_meta.json")
RP = os.path.join(D, "_exit_zero_meta_report.txt")


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

assert obj["verdict"].startswith("EXIT-ZERO-META--")
assert "SURVIVE-ZERO-IS-CALIBER-BLOCKED-NOT-CANDIDATE-PHYSICS" in obj["verdict"]
assert "LATEST-REPRICE-R437-LOGICALLY-OPEN" in obj["verdict"]
assert obj["verdict"].endswith("--NO-UFT-CLAIM")
assert obj["counts"] == {"gate": 8, "neg": 3, "identity": 0, "failed": 0}, obj["counts"]
assert len(obj["gates"]) == 11, len(obj["gates"])
assert all(g["ok"] is True for g in obj["gates"])
assert obj["independent_prediction_count"] == 0
ir = obj["independent_recompute"]
assert ir["q_t"] == {"-1": "203/8", "0": "25", "1": "197/8"}
assert ir["survive_r404_quota1"] == ["E09"]
assert ir["survive_r405_repriced_quota1"] == []
assert ir["survive_r405_repriced_quota2"] == ["E09"]

runpy.run_path(HITS[0], run_name="__main__")
d2 = digest([JP, RP])
assert d1 == d2, (d1, d2)
print("JSON-GATE-OK gates=11 all_ok=True counts=", obj["counts"])
print("IDEMPOTENT-MD5", d1, d2)
