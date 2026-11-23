# -*- coding: utf-8 -*-
"""ASCII runner for TUFT r448. Locates the Chinese-named engine by glob."""
from pathlib import Path
import hashlib
import json
import subprocess

BASE = Path(r"D:\a10\aikjx\code\my_lib\openuft")
PY38 = r"C:\Users\mo\AppData\Local\Programs\Python\Python38\python.exe"
SOURCE_SHA = "aa8568914e8b3438ba77ac52ada2f110ab54098ae8e95930f168a2e33365c863"


def one(items, label):
    if len(items) != 1:
        raise SystemExit("expected one %s, got %d" % (label, len(items)))
    return items[0]


def md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def section_digest(raw, marker):
    start = raw.find(marker.encode("utf-8"))
    if start <= 0:
        raise SystemExit("missing r448 README section")
    end = raw.find(b"\n---\n", start)
    if end < 0:
        end = len(raw)
    return hashlib.sha256(raw[start:end]).hexdigest()


engine = one(list(BASE.glob("04_*/**/TUFT-r448_*.py")), "r448 engine")
alg_dir = engine.parent.parent
data_dir = alg_dir / "数据"
root_readme = BASE / "README.md"
alg_readme = alg_dir / "README.md"
before_root = sha256(root_readme)
before_section = section_digest(alg_readme.read_bytes(), "## 四十六、ROOT V142")
if b"README" in engine.read_bytes():
    raise SystemExit("engine must not write README")

json_path = one(list(data_dir.glob("TUFT-r448_*.json")), "r448 json") if list(data_dir.glob("TUFT-r448_*.json")) else data_dir / "TUFT-r448_ROOT_V142规范曲率与光子偏振判据_全维审计_2026-11-24.json"
md_path = data_dir / "TUFT-r448_ROOT_V142规范曲率与光子偏振判据_全维审计_2026-11-24.md"
rep_path = data_dir / "TUFT-r448_ROOT_V142规范曲率与光子偏振判据_全维审计_2026-11-24_report.txt"

out1 = subprocess.check_output([PY38, str(engine)], text=True, encoding="utf-8")
snap1 = {p.name: md5(p) for p in (json_path, md_path, rep_path)}
out2 = subprocess.check_output([PY38, str(engine)], text=True, encoding="utf-8")
snap2 = {p.name: md5(p) for p in (json_path, md_path, rep_path)}

if snap1 != snap2:
    raise SystemExit("non-idempotent outputs: %s != %s" % (snap1, snap2))
after_root = sha256(root_readme)
after_section = section_digest(alg_readme.read_bytes(), "## 四十六、ROOT V142")
if before_root != after_root:
    raise SystemExit("root README changed during engine runs")
if before_section != after_section:
    raise SystemExit("r448 README section changed during engine runs")

data = json.loads(json_path.read_text(encoding="utf-8"))
if data["entry_count"] != 21:
    raise SystemExit("entry count mismatch: %s" % data["entry_count"])
if data["guard_total"] != 18 or data["guard_pass"] != 18:
    raise SystemExit("guard mismatch: %s/%s" % (data["guard_pass"], data["guard_total"]))
if any(not g["ok"] for g in data["guards"]):
    raise SystemExit("some guard failed")
if data["source_sha256"] != SOURCE_SHA:
    raise SystemExit("source sha mismatch")
if not data["verdict"].endswith("NO-UFT-CLAIM"):
    raise SystemExit("verdict missing redline suffix")

print("OK", out1.strip(), "|", out2.strip())
for name, digest in sorted(snap2.items()):
    print("md5", name, digest)
print("root_readme_unchanged", len(root_readme.read_bytes()), after_root)
print("r448_section_unchanged", after_section)
print("alg_readme_full_sha256", sha256(alg_readme), len(alg_readme.read_bytes()))
