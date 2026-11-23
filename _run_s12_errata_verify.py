# -*- coding: utf-8 -*-
"""ASCII runner: JSON gate check + idempotent double-run for S12 errata audit."""
import glob
import hashlib
import json
import os
import runpy

BASE = os.path.dirname(os.path.abspath(__file__))
HITS = glob.glob(os.path.join(
    BASE, "04_*", "本项目_*", "_S12勘误残留元审计_*", "s12_errata_residue_audit.py"))
assert len(HITS) == 1, HITS
D = os.path.dirname(HITS[0])
JP = os.path.join(D, "_s12_errata_residue.json")
RP = os.path.join(D, "_s12_errata_residue_report.txt")


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

assert obj["verdict"].startswith("S12-ERRATA-RESIDUE--")
assert "SAME-CLAIM-BOTH-REVOKED-AND-CLOSED" in obj["verdict"]
assert "CH8-OLD-CLAIMS-NOT-RECOMPUTED" in obj["verdict"]
assert obj["verdict"].endswith("--NO-UFT-CLAIM")
assert obj["counts"] == {"gate": 4, "neg": 2, "identity": 1, "failed": 0}, obj["counts"]
assert len(obj["gates"]) == 7, len(obj["gates"])
assert all(g["ok"] is True for g in obj["gates"])
assert obj["independent_prediction_count"] == 0
kr = obj["key_readings"]
assert kr["errata_lines"] == 2 and kr["residue_lines"] == 4
assert kr["residue_marked_closed"] == 1 and kr["internal_conflict"] is True
assert kr["2pi_over_theta"].startswith("861")

runpy.run_path(HITS[0], run_name="__main__")
d2 = digest([JP, RP])
assert d1 == d2, (d1, d2)
print("JSON-GATE-OK gates=7 all_ok=True counts=", obj["counts"])
print("IDEMPOTENT-MD5", d1, d2)
