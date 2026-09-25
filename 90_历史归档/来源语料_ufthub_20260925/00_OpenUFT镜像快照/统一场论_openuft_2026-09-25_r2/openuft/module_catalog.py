# -*- coding: utf-8 -*-
"""
module_catalog.py — OpenUFT 体系注册表（registry）与派生视图
规则：
  * 每个体系（01_独立体系/<体系>/system.json）是权威注册源；
  * check() 比对的是 system.json 的**完整快照**（source_records、module_types、
    stable_ids、overview）与 .registry/snapshot.json 的一致性；
  * 任何 source_records 增删（如新增脚本）都会造成 registry 漂移，须 refresh；
  * refresh() 以当前 system.json 全量重写快照。
用法：
  python3 -B module_catalog.py check
  python3 -B module_catalog.py refresh
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
REGISTRY_DIR = os.path.join(REPO, ".registry")
SNAPSHOT_PATH = os.path.join(REGISTRY_DIR, "snapshot.json")


def discover_system_jsons():
    hits = []
    base = os.path.join(REPO, "01_独立体系")
    if not os.path.isdir(base):
        return hits
    for entry in sorted(os.listdir(base)):
        p = os.path.join(base, entry, "system.json")
        if os.path.isfile(p):
            hits.append(p)
    return hits


def derive_view(system_path):
    with open(system_path, encoding="utf-8") as f:
        data = json.load(f)
    recs = data.get("source_records", [])
    return {
        "system_id": data.get("system_id", os.path.basename(os.path.dirname(system_path))),
        "name": data.get("name", ""),
        "module_types": sorted({r.get("module_type", "") for r in recs if r.get("module_type")}),
        "stable_ids": sorted({r.get("stable_id", "") for r in recs if r.get("stable_id")}),
        "overview": sorted(r.get("path", "") for r in recs if r.get("path")),
        "source_records": [
            {"path": r.get("path", ""), "locator": r.get("locator", ""),
             "module_type": r.get("module_type", ""), "stable_id": r.get("stable_id", "")}
            for r in recs
        ],
    }


def build_current():
    views = {}
    for p in discover_system_jsons():
        v = derive_view(p)
        views[v["system_id"]] = v
    return views


def check():
    current = build_current()
    if not os.path.exists(SNAPSHOT_PATH):
        print("[FAIL] 快照不存在，请先运行: python3 -B module_catalog.py refresh")
        return 1
    with open(SNAPSHOT_PATH, encoding="utf-8") as f:
        snapshot = json.load(f)
    issues = []
    for sid, view in current.items():
        old = snapshot.get(sid)
        if old is None:
            issues.append(f"registry 漂移: 新体系 {sid} 未在快照中")
            continue
        if old != view:
            old_n, new_n = len(old.get("source_records", [])), len(view.get("source_records", []))
            issues.append(
                f"registry 漂移: {sid} source_records {old_n} → {new_n}（或派生视图变化）")
    return issues, current


def refresh():
    os.makedirs(REGISTRY_DIR, exist_ok=True)
    current = build_current()
    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False, indent=1)
    print(f"[PASS] 快照已刷新: {len(current)} 个体系 -> {SNAPSHOT_PATH}")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "refresh":
        sys.exit(refresh())
    issues, _ = check()
    if issues:
        print("[FAIL] module catalog 结构校验未通过:")
        for i in issues:
            print("  -", i)
        print("修复: python3 -B module_catalog.py refresh")
        sys.exit(1)
    print("[PASS] module types, stable ids and generated views 一致")
    sys.exit(0)
