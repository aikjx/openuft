# -*- coding: utf-8 -*-
"""ASCII runner: JSON gate check + idempotent double-run md5 for V51 attack."""
import glob
import hashlib
import json
import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))
HITS = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_V51攻破_*", "v51_attack_recompute.py"))
assert len(HITS) == 1, HITS
JP = os.path.join(os.path.dirname(HITS[0]), "_v51_attack_recompute.json")
RP = os.path.join(os.path.dirname(HITS[0]), "_v51_attack_report.txt")


def digest(paths):
    h = hashlib.md5()
    for p in paths:
        with open(p, "rb") as f:
            h.update(f.read())
    return h.hexdigest()


runpy.run_path(HITS[0], run_name="__main__")
d1 = digest([JP, RP])
with open(JP, "r", encoding="utf-8") as f:
    obj = json.load(f)

assert obj["verdict"].startswith("V51-ATTACK--"), obj["verdict"]
assert "POSITIVITY-FIX-14-OF-40-PD-ALL-14-VIOLATE-26-TACHYONIC-EXCLUDED" in obj["verdict"]
assert obj["verdict"].endswith("--NO-UFT-CLAIM")
assert obj["counts"] == {"gate": 10, "neg": 4, "identity": 1, "failed": 0}, obj["counts"]
assert len(obj["gates"]) == 15, len(obj["gates"])
assert all(g["ok"] is True for g in obj["gates"]), [g["id"] for g in obj["gates"] if not g["ok"]]
assert obj["independent_prediction_count"] == 0
pa = obj["positivity_audit"]
assert pa["samples_total"] == 40 and pa["positive_definite"] == 14
assert pa["non_positive_tachyonic_excluded"] == 26 and pa["violations_within_pd"] == 14
assert pa["first_nonpositive_k"] == 15
b4 = [g for g in obj["gates"] if g["id"] == "B4-similarity"][0]
assert "实测" in b4["exp"] and "|Δtrace|=" in b4["act"]
c2 = [g for g in obj["gates"] if g["id"] == "C2-arbitrary-h"][0]
assert "无上界" in c2["exp"] and "N=" in c2["act"]

runpy.run_path(HITS[0], run_name="__main__")
d2 = digest([JP, RP])
assert d1 == d2, (d1, d2)
print("JSON-GATE-OK gates=15 all_ok=True counts=", obj["counts"])
print("IDEMPOTENT-MD5", d1, d2)
