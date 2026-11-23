# -*- coding: utf-8 -*-
"""ASCII runner: JSON gate check + idempotent double-run md5 for V51 self-attack."""
import glob
import hashlib
import json
import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))
HITS = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_V51自噬_WignerEckart*", "v51_selfattack_we_recompute.py"))
assert len(HITS) == 1, HITS
JP = os.path.join(os.path.dirname(HITS[0]), "_v51_selfattack_we_recompute.json")
RP = os.path.join(os.path.dirname(HITS[0]), "_v51_selfattack_we_report.txt")

RUNPY = os.path.join(BASE, "04_*")


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

assert obj["verdict"].startswith("V51-SELFATTACK-WE--"), obj["verdict"]
assert obj["verdict"].endswith("--NO-UFT-CLAIM"), obj["verdict"]
assert obj["counts"] == {"gate": 8, "neg": 2, "identity": 1, "failed": 0}, obj["counts"]
assert len(obj["gates"]) == 11, len(obj["gates"])
assert all(g["ok"] is True for g in obj["gates"]), [g["id"] for g in obj["gates"] if not g["ok"]]
assert obj["independent_prediction_count"] == 0
assert obj["dims"] == {"opspace_rep": 1, "opspace_k0k1": 4, "opspace_all": 9,
                       "herm_k0": 1, "herm_k0k1": 4, "herm_all": 9}
assert obj["cg_key_values"]["T00_diag"] == ["1", "1", "1"]

runpy.run_path(HITS[0], run_name="__main__")
d2 = digest([JP, RP])
assert d1 == d2, (d1, d2)
print("JSON-GATE-OK gates=11 all_ok=True counts=", obj["counts"])
print("IDEMPOTENT-MD5", d1, d2)
