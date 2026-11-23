# -*- coding: utf-8 -*-
"""ASCII runner for the Thomas attractor HTML recompute engine."""
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


SCRIPT = one(os.path.join(HERE, "04_*", "本项目_*", "_外部来料融合_托马斯吸引子_*", "thomas_attractor_recompute.py"))
HERE_SCRIPT = os.path.dirname(SCRIPT)
HTML = one(os.path.join(HERE_SCRIPT, "*来料原文*.html"))
OUT_JSON = os.path.join(HERE_SCRIPT, "_thomas_recompute.json")
REPORT = os.path.join(HERE_SCRIPT, "_thomas_recompute_report.txt")
README = os.path.join(HERE, "README.md")


def md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


readme_before = md5(README) if os.path.exists(README) else None
html_before = md5(HTML)
snapshots = []
stdout_last = ""
for _ in (1, 2):
    cp = subprocess.run([sys.executable, SCRIPT], cwd=HERE,
                        capture_output=True, text=True, encoding="utf-8")
    if cp.returncode != 0:
        sys.stderr.write(cp.stdout or "")
        sys.stderr.write(cp.stderr or "")
        raise SystemExit(cp.returncode)
    stdout_last = cp.stdout.strip()
    snapshots.append((md5(OUT_JSON), md5(REPORT)))

if snapshots[0] != snapshots[1]:
    raise SystemExit("idempotence failed: %s != %s" % snapshots)
if md5(HTML) != html_before:
    raise SystemExit("source HTML was modified by recompute")

with open(OUT_JSON, encoding="utf-8") as f:
    data = json.load(f)
counts = data["counts"]
expect = {"gate": 10, "neg": 2, "identity": 0, "failed": 0}
if counts != expect:
    raise SystemExit("counts mismatch: %s != %s" % (counts, expect))

gates = {g["id"]: g for g in data["gates"]}
required = ["G00-ast", "A1-two-path-constants", "A2-divergence", "A3-rk4-order",
            "B1-lyapunov-positive", "B2-lyapunov-cross-check", "B3-nonchaotic-neg",
            "B4-regime-labels-fact", "C1-poincare-crossings", "C2-box-dimension",
            "C3-box-scale-neg", "D1-redline"]
missing = [gid for gid in required if gid not in gates or not gates[gid]["ok"]]
if missing:
    raise SystemExit("gates missing or failed: %s" % missing)
if any(g["exp"] == g["act"] for g in data["gates"]):
    raise SystemExit("exp/act identical found")
if data["independent_prediction_count"] != 0:
    raise SystemExit("independent prediction count must be 0")
if not data["verdict"].startswith("THOMAS-HTML-RECOMPUTE--"):
    raise SystemExit("verdict prefix mismatch")
for marker in ("RK4-ORDER-4", "LYAPUNOV-POSITIVE-CROSSCHECK",
               "NONCHAOTIC-NEG", "BOX-DIM-FINITE", "NO-UFT-CLAIM"):
    if marker not in data["verdict"]:
        raise SystemExit("verdict marker missing: %s" % marker)

readme_after = md5(README) if os.path.exists(README) else None
if readme_before != readme_after:
    raise SystemExit("README changed: %s -> %s" % (readme_before, readme_after))

print("VERIFY-OK gate=%d neg=%d identity=%d failed=%d" % (
    counts["gate"], counts["neg"], counts["identity"], counts["failed"]))
print("html-md5=%s unchanged" % html_before)
print("md5 json=%s report=%s" % snapshots[-1])
print("README-md5=%s unchanged" % readme_after)
print("verdict=%s" % data["verdict"])
