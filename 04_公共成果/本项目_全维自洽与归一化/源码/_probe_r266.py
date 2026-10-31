# -*- coding: utf-8 -*-
"""r266 探针：盘点 数据/TUFT-r2*.json 的统一读取可行性与判词字段归一。"""
import io, os, re, json, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "数据")

files = sorted(glob.glob(os.path.join(DATA, "TUFT-r2*.json")))
print("files:", len(files))

rows = []
for p in files:
    b = io.open(p, "rb").read()
    try:
        j = json.loads(b.decode("utf-8", errors="replace"))
    except Exception as e:
        rows.append((os.path.basename(p)[:40], "PARSE_FAIL", str(e)[:60], 0, "", ""))
        continue
    rid = j.get("rid") or j.get("id") or ""
    if not rid:
        m = re.search(r"TUFT-(r\d+)_", os.path.basename(p))
        rid = m.group(1) if m else "?"
    ent = j.get("entries")
    n = len(ent) if isinstance(ent, list) else -1
    vk = ""
    if isinstance(ent, list) and ent and isinstance(ent[0], dict):
        ks = set(ent[0].keys())
        for cand in ("verdict", "state", "level", "result", "judgement"):
            if cand in ks:
                vk = cand
                break
        if not vk:
            vk = "|".join(sorted(ks))[:40]
    tk = ",".join(sorted(j.keys()))[:130]
    rows.append((rid, os.path.basename(p)[:34], vk, n, "", tk))

for r in rows:
    print("%-6s %-34s %-10s n=%-4s %s" % (r[0], r[1], r[2], r[3], r[5]))

print("\n=== 判词字段分布 ===")
print(collections.Counter(r[2] for r in rows))
print("\n=== 无 entries 的卷 ===")
print([r[0] for r in rows if r[3] == -1])
