# -*- coding: utf-8 -*-
"""ASCII runner: JSON gate check + idempotent double-run for geometry panorama."""
import glob
import hashlib
import json
import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))
HITS = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_外部来料融合_宇宙几何全景*", "geom_panorama_recompute.py"))
assert len(HITS) == 1, HITS
D = os.path.dirname(HITS[0])
JP = os.path.join(D, "_geom_panorama.json")
RP = os.path.join(D, "_geom_panorama_report.txt")


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

assert obj["verdict"].startswith("GEOM-PANORAMA--")
assert "INNER-RAY-B-2RS-BELOW-PHOTON-CAPTURE" in obj["verdict"]
assert obj["verdict"].endswith("--NO-UFT-CLAIM")
assert obj["counts"] == {"gate": 10, "neg": 3, "identity": 1, "failed": 0}, obj["counts"]
assert len(obj["gates"]) == 14, len(obj["gates"])
assert all(g["ok"] is True for g in obj["gates"])
assert obj["independent_prediction_count"] == 0
kr = obj["key_readings"]
assert kr["deflection_deg"] == ["57.30", "35.81", "23.87"]
assert kr["delta_inner_rad"] == "1"
assert kr["b_crit_over_rs"] == "2.598076" and kr["inner_ray_captured"] is True

runpy.run_path(HITS[0], run_name="__main__")
d2 = digest([JP, RP])
assert d1 == d2, (d1, d2)
print("JSON-GATE-OK gates=14 all_ok=True counts=", obj["counts"])
print("IDEMPOTENT-MD5", d1, d2)
