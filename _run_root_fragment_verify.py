# -*- coding: utf-8 -*-
"""ASCII runner for the ROOT fragment audit."""
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


SCRIPT = one(os.path.join(HERE, "04_*", "本项目_*", "_外部来料融合_ROOT本源核心公式片段_*", "root_fragment_audit.py"))
D = os.path.dirname(SCRIPT)
FRAG = one(os.path.join(D, "*来料片段*.html"))
OUT = os.path.join(D, "_root_fragment_meta.json")
REPORT = os.path.join(D, "_root_fragment_meta_report.txt")
README = os.path.join(HERE, "README.md")


def md5(p):
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


readme_before = md5(README) if os.path.exists(README) else None
frag_before = md5(FRAG)
snaps = []
for _ in (1, 2):
    cp = subprocess.run([sys.executable, SCRIPT], cwd=HERE,
                        capture_output=True, text=True, encoding="utf-8")
    if cp.returncode != 0:
        sys.stderr.write(cp.stdout or "")
        sys.stderr.write(cp.stderr or "")
        raise SystemExit(cp.returncode)
    snaps.append((md5(OUT), md5(REPORT)))
if snaps[0] != snaps[1]:
    raise SystemExit("idempotence failed: %s" % snaps)
if md5(FRAG) != frag_before:
    raise SystemExit("fragment source changed")

with open(OUT, encoding="utf-8") as f:
    data = json.load(f)
expect = {"gate": 6, "neg": 2, "identity": 0, "failed": 0}
if data["counts"] != expect:
    raise SystemExit("counts mismatch: %s != %s" % (data["counts"], expect))
required = ["G00-ast", "F1-fragment-incomplete", "F2-title-overclaim",
            "F3-no-formula-body", "F4-redline-anchors", "F5-no-inline-3d",
            "N1-inject-close-neg", "N2-inject-formula-neg"]
gates = {g["id"]: g for g in data["gates"]}
missing = [g for g in required if g not in gates or not gates[g]["ok"]]
if missing:
    raise SystemExit("gates missing or failed: %s" % missing)
if any(g["exp"] == g["act"] for g in data["gates"]):
    raise SystemExit("exp/act identical found")
if data["independent_prediction_count"] != 0:
    raise SystemExit("independent prediction count must be 0")
if not data["verdict"].startswith("ROOT-FRAGMENT--"):
    raise SystemExit("verdict prefix mismatch")
for marker in ("INCOMPLETE-CONFIRMED", "TITLE-OVERCLAIM-DETECTED",
               "NO-FORMULA-BODY", "REDLINE-ANCHORS-OK", "NO-UFT-CLAIM"):
    if marker not in data["verdict"]:
        raise SystemExit("verdict marker missing: %s" % marker)
if not data["fragment"]["incomplete"]:
    raise SystemExit("fragment should remain incomplete")

readme_after = md5(README) if os.path.exists(README) else None
if readme_before != readme_after:
    raise SystemExit("README changed")

print("VERIFY-OK gate=%d neg=%d identity=%d failed=%d" % (
    data["counts"]["gate"], data["counts"]["neg"],
    data["counts"]["identity"], data["counts"]["failed"]))
print("fragment-md5=%s unchanged" % frag_before)
print("md5 json=%s report=%s" % snaps[-1])
print("README-md5=%s unchanged" % readme_after)
print("verdict=%s" % data["verdict"])
