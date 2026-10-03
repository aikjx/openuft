#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
guard_selftest.py —— 企业级多域守卫「测试验证」
==================================================
用隔离临时夹具（tempfile，不触碰 CURATED 真源）对 guard_all 各域做负向/正向自测：
  负向：制造违规（列错位 / 非法 evidence / 重复编号 / 缺字段）→ 断言能检出
  正向：合法文件 → 断言不误报
  机制：逃生门 SKIP / --json 结构化 / 各域扫描函数直接调用

用法：python -B 00_项目治理/维护工具/guard_selftest.py
退出码：0=全部通过；1=有失败用例
"""
from __future__ import print_function

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

MAINT = Path(r"D:\a10\aikjx\code\my_lib\openuft\00_项目治理\维护工具")
sys.path.insert(0, str(MAINT))
import guard_all as g

HEADER = ("claim_id,hypothesis_revision,statement,assumptions,derivation,prediction,"
          "prediction_value,prediction_urel,run_id,data_id,uncertainty,evidence_level,status,reviewer\n")
GOOD_SYS = json.dumps({"id": "f", "title": "F", "kind": "x", "status": "s", "directory": "F"})

fails = []


def check(name, cond, detail=""):
    print("  [%s] %s%s" % ("PASS" if cond else "FAIL", name, (" | " + detail if detail else "")))
    if not cond:
        fails.append(name)


def make_root():
    root = Path(tempfile.mkdtemp(prefix="openuft_guard_test_"))
    (root / "01_独立体系" / "FAKE").mkdir(parents=True, exist_ok=True)
    return root


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


print("== 域A · claims 结构（负向检出）==")
# 1) 列错位
r = make_root()
write(r, "01_独立体系/FAKE/claims.csv", HEADER + "F-C0001,h1,stmt,a,d,,,,run,data,,mathematical_result,verified,\nEXTRA,a,b,c,d,e,f,g,h,i,j,k,l,m,n\n")
w, _ = g._scan_claims_structure(r)
check("列错位检出", any("列数 != 表头" in x for x in w), str(w))
# 2) 重复 claim_id
r = make_root()
write(r, "01_独立体系/FAKE/claims.csv", HEADER + "F-C0001,h1,stmt1,a,d,,,,run,data,,mathematical_result,verified,\nF-C0001,h1,stmt2,a,d,,,,run,data,,mathematical_result,verified,\n")
w, _ = g._scan_claims_structure(r)
check("重复claim_id检出", any("claim_id 重复" in x for x in w), str(w))
# 3) 合法文件无误报
r = make_root()
write(r, "01_独立体系/FAKE/claims.csv", HEADER + "F-C0001,h1,stmt,a,d,,,,run,data,,mathematical_result,verified,\n")
w, _ = g._scan_claims_structure(r)
check("合法结构无误报", not w, str(w))

print("== 域B · claims 语义（负向检出）==")
# 4) 非法 evidence（中文长句污染）
r = make_root()
write(r, "01_独立体系/FAKE/claims.csv", HEADER + "F-C0001,h1,stmt,a,d,,,,run,data,,方法学为教科书级正确,verified,\n")
w, _ = g._scan_claims_semantic(r)
check("非法evidence检出", any("evidence_level 非法词" in x for x in w), str(w))
# 5) 单字母分级 → INFO
r = make_root()
write(r, "01_独立体系/FAKE/claims.csv", HEADER + "F-C0001,h1,stmt,a,d,,,,run,data,,O,verified,\n")
_, i = g._scan_claims_semantic(r)
check("单字母分级→INFO", any("单字母分级" in x for x in i), str(i))
# 6) 裸 VERIFIED → WARN（B1）
r = make_root()
write(r, "01_独立体系/FAKE/claims.csv", HEADER + "F-C0001,h1,stmt,a,d,,,,run,data,,VERIFIED,,\n")
w, _ = g._scan_claims_semantic(r)
check("裸VERIFIED拦截", any("裸 VERIFIED" in x for x in w), str(w))
# 7) 合法词组合不误报
r = make_root()
write(r, "01_独立体系/FAKE/claims.csv", HEADER + "F-C0001,h1,stmt,a,d,,,,run,data,,mathematical_result+numerical_check,verified,\n")
w, _ = g._scan_claims_semantic(r)
check("合法组合词无误报", not w, str(w))
# 7b) status 列放 evidence 词 → WARN（域B 增强：evidence 串入 status）
r = make_root()
write(r, "01_独立体系/FAKE/claims.csv", HEADER + "F-C0001,h1,stmt,a,d,,,,run,data,,mathematical_result,mathematical_result,\n")
w, _ = g._scan_claims_semantic(r)
check("status串列检出", any("status 列" in x and "evidence" in x for x in w), str(w))
# 7c) status=verified 合法 → 不误报
r = make_root()
write(r, "01_独立体系/FAKE/claims.csv", HEADER + "F-C0001,h1,stmt,a,d,,,,run,data,,mathematical_result,verified,\n")
w, _ = g._scan_claims_semantic(r)
check("status=verified无误报", not any("status 列" in x for x in w), str(w))
# 7d) status 列放完全非法词（unreproduced ∉ STATUS_WORDS/evidence）→ WARN（域B 增强：非法 status 词）
r = make_root()
write(r, "01_独立体系/FAKE/claims.csv", HEADER + "F-C0001,h1,stmt,a,d,,,,run,data,,mathematical_result,unreproduced,\n")
w, _ = g._scan_claims_semantic(r)
check("status非法词检出", any("status 列" in x and "非法词" in x for x in w), str(w))
# 7e) status 合法词 open/falsified → 不误报
r = make_root()
write(r, "01_独立体系/FAKE/claims.csv", HEADER + "F-C0001,h1,stmt,a,d,,,,run,data,,mathematical_result,open,\n")
w, _ = g._scan_claims_semantic(r)
check("status合法词无误报", not any("status 列" in x and "非法词" in x for x in w), str(w))

print("== 域C · system 身份（负向检出）==")
# 8) 缺必填字段
r = make_root()
write(r, "01_独立体系/FAKE/system.json", json.dumps({"id": "f", "title": "F", "kind": "x", "status": "s"}))
w, _ = g._scan_system(r)
check("缺directory检出", any("缺必填字段" in x for x in w), str(w))
# 9) A1 schema 缺口 → INFO
r = make_root()
write(r, "01_独立体系/FAKE/system.json", GOOD_SYS)
_, i = g._scan_system(r)
check("A1 schema缺口→INFO", any("A1 schema 缺字段" in x for x in i), str(i))
# 10) 合法 system 无误报
r = make_root()
write(r, "01_独立体系/FAKE/system.json", GOOD_SYS)
w, _ = g._scan_system(r)
check("合法system无误报", not w, str(w))

print("== 机制 · 逃生门 / JSON ==")
# 11) SKIP 逃生门（子进程，SKIP 分支在 verify 前，快速）
env = dict(os.environ)
env["OPENUFT_GUARD_SKIP"] = "1"
try:
    p = subprocess.run([sys.executable, "-B", str(MAINT / "guard_all.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=env, cwd=MAINT.parent.parent, timeout=30)
    check("SKIP逃生门", p.returncode == 0 and "跳过校验" in (p.stdout + p.stderr), str(p.returncode))
except subprocess.TimeoutExpired:
    check("SKIP逃生门", False, "timeout")
# 12) FORCE 强制（覆盖 SKIP）→ 会跑 verify，可能慢；仅验证机制不被 SKIP 吞
# 13) --json 合法
try:
    p = subprocess.run([sys.executable, "-B", str(MAINT / "guard_all.py"), "--json"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=MAINT.parent.parent, timeout=120)
    ok = p.returncode == 0
    obj = json.loads(p.stdout.strip().splitlines()[-1]) if p.stdout.strip() else None
    check("--json合法结构化", ok and obj and obj.get("ok") is True and "warns" in obj and "infos" in obj, "")
except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
    check("--json合法结构化", False, "err=%s" % e)

print()
if fails:
    print("自测失败 %d 项: %s" % (len(fails), fails))
    sys.exit(1)
print("全部自测用例通过 —— 企业级多域守卫测试验证 OK（负向检出 + 正向无误报 + 逃生门 + JSON 均验证）")

