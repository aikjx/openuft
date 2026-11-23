# -*- coding: utf-8 -*-
"""ASCII runner for the exit-C cost audit.

The script under test has a Chinese path, so this runner locates it with glob
and never requires the user to pass that path in argv. It runs the engine twice,
checks idempotence, validates machine gates, and confirms README is untouched.
"""
import glob
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def one(pattern):
    hits = glob.glob(pattern)
    assert len(hits) == 1, (pattern, hits)
    return hits[0]


SCRIPT = one(os.path.join(HERE, "04_*", "本项目_*", "_出路C代价*", "exit_c_cost_audit.py"))
OUT_JSON = os.path.join(os.path.dirname(SCRIPT), "_exit_c_cost_meta.json")
REPORT = os.path.join(os.path.dirname(SCRIPT), "_exit_c_cost_meta_report.txt")
README = os.path.join(HERE, "README.md")


def md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


readme_before = md5(README) if os.path.exists(README) else None
snapshots = []
outputs = []
for run in (1, 2):
    cp = subprocess.run([sys.executable, SCRIPT], cwd=HERE,
                        capture_output=True, text=True, encoding="utf-8")
    if cp.returncode != 0:
        sys.stderr.write(cp.stdout or "")
        sys.stderr.write(cp.stderr or "")
        raise SystemExit(cp.returncode)
    outputs.append(cp.stdout.strip())
    snapshots.append((md5(OUT_JSON), md5(REPORT)))

if snapshots[0] != snapshots[1]:
    raise SystemExit("idempotence failed: %s != %s" % snapshots)

with open(OUT_JSON, encoding="utf-8") as f:
    data = json.load(f)

counts = data["counts"]
expect = {"gate": 15, "neg": 3, "identity": 0, "failed": 0}
if counts != expect:
    raise SystemExit("counts mismatch: %s != %s" % (counts, expect))

gates = {g["id"]: g for g in data["gates"]}
required_ok = [
    "G00-ast-precheck", "M1-price-chain-anchors", "M2-latest-no-reopen",
    "A1-two-path-ledger", "A2-rule-recompute", "B1-assignment-entropy",
    "B2-wrong-sample-space-neg", "B3-short-range-constraint",
    "C1-plus-one-pseudo", "C2-inject-four-constraints",
    "C3-assign-derivation-insufficient", "C4-free-function-collapse",
    "C5-chain-reprice-visible", "H1-axis-not-identical",
    "H2-criteria-not-identical", "H3-no-explicit-map",
    "H4-cross-axis-transfer-fails", "H5-fake-mapping-neg",
]
missing = [gid for gid in required_ok if gid not in gates or not gates[gid]["ok"]]
if missing:
    raise SystemExit("required gates missing or failed: %s" % missing)

if any(g["exp"] == g["act"] for g in data["gates"]):
    raise SystemExit("exp/act identical found: gate has no discrimination")

if any(g["ok"] is True and g["kind"] == "identity" for g in data["gates"]
       if "承重" in g["note"]):
    raise SystemExit("load-bearing identity gate found")

if data["independent_prediction_count"] != 0:
    raise SystemExit("independent prediction count must stay 0")

if not data["verdict"].startswith("EXIT-C-COST-META--"):
    raise SystemExit("verdict prefix mismatch: %s" % data["verdict"])

for marker in ("PLUS-ONE-PSEUDO-COST-REPRODUCED",
               "INJECT-FOUR-CONSTRAINTS-FLIPS-IDENTIFIABLE",
               "L0-L5-NOT-C0-C3-AXIS",
               "EXIT-C-CLOSED-R421",
               "UNIQUE-EXIT-R437-EXTERNAL"):
    if marker not in data["verdict"]:
        raise SystemExit("verdict marker missing: %s" % marker)

readme_after = md5(README) if os.path.exists(README) else None
if readme_before != readme_after:
    raise SystemExit("README changed by audit: %s -> %s" % (readme_before, readme_after))

print("VERIFY-OK gate=%d neg=%d identity=%d failed=%d" % (
    counts["gate"], counts["neg"], counts["identity"], counts["failed"]))
print("md5 json=%s report=%s" % snapshots[-1])
print("README-md5=%s unchanged" % readme_after)
print("verdict=%s" % data["verdict"])
