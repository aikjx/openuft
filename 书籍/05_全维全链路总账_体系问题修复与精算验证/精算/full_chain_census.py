# -*- coding: utf-8 -*-
"""《全维全链路总账》只读普查（本书全部聚合数字的唯一载体）。

审计对象（只读，不写任何被审文件）：
  账一 体系   00_项目治理/system_registry.json         —— 编号、类型、状态
  账二 主张   01_独立体系/<体系>/claims.csv            —— 条目数、status 分布、证据等级
  账三 书稿   书籍/**.md                               —— 件数、字节、章数、编数
  账四 仪器   openuft/**.py（活跃区/历史区分开）        —— 脚本存量
  账五 定理   v1_正文/**.md                            —— 十二道 no-go 定理的落名次数

纪律：
  · 只读；不改被审字节。
  · 提取失败一律硬失败（return 2），不印任何聚合数；「没提取到」≠「值为 0」。
  · 对照必须有牙：正对照造面命中、负对照改一个自由度必须让读数移动。
  · 数字只在本脚本 stdout 里现印；正文不手打聚合数。

运行：python -X utf8 full_chain_census.py > _census_report.txt 2>&1
"""
import collections
import csv
import io
import json
import os
import re
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)                        # .../书籍/05_...
BOOKS = os.path.dirname(BOOK)                       # .../书籍
ROOT = os.path.dirname(BOOKS)                       # .../openuft

REGISTRY = os.path.join(ROOT, "00_项目治理", "system_registry.json")
SYSTEMS = os.path.join(ROOT, "01_独立体系")
V1 = os.path.join(BOOKS, "v1_正文")

CHECKS = []
FAILS = []
DATA = {}


def _inside_book(path):
    p = os.path.normcase(os.path.abspath(path))
    b = os.path.normcase(os.path.abspath(BOOK))
    return p == b or p.startswith(b + os.sep)


def ctl(name, ok, detail):
    CHECKS.append((name, ok, detail))
    if not ok:
        FAILS.append("%s :: %s" % (name, detail))
    print("  [%s] %s :: %s" % ("绿" if ok else "红", name, detail))


def read_text(path):
    with io.open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().replace("\r\n", "\n").replace("\r", "\n")


def parse_claims_rows(rows):
    """rows: list[list[str]]（首行表头）。

    返回 (非空行, 列宽合格行, status 计数, evidence 计数, 列宽异常行号)。
    纪律：status/evidence 分布**只统计列宽 == 表头**的行；列宽不符者计入
    「列宽异常」单独点出，绝不把错位列的值当成 status（那是第二本假账）。
    """
    if not rows:
        return 0, 0, collections.Counter(), collections.Counter(), []
    header = rows[0]
    if "status" not in header:
        return 0, 0, collections.Counter(), collections.Counter(), []
    i_status = header.index("status")
    i_ev = header.index("evidence_level") if "evidence_level" in header else None
    status = collections.Counter()
    evidence = collections.Counter()
    width_bad = []
    total = 0
    width_ok = 0
    for n, row in enumerate(rows[1:], start=2):
        if not any(c.strip() for c in row):
            continue
        total += 1
        if len(row) != len(header):
            width_bad.append(n)
            continue
        width_ok += 1
        status[(row[i_status] or "(空)").strip()] += 1
        if i_ev is not None:
            evidence[(row[i_ev] or "(空)").strip()] += 1
    return total, width_ok, status, evidence, width_bad


def scan_claims(path):
    with io.open(path, "r", encoding="utf-8-sig", errors="replace", newline="") as fh:
        rows = list(csv.reader(fh))
    return parse_claims_rows(rows)


def count_scripts():
    active = 0
    archived = 0
    shared = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        # 本书自身不计入被审面：否则每加一件正文，读数就自己移动
        if _inside_book(dirpath):
            continue
        for fn in filenames:
            if not fn.lower().endswith(".py"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            if ("90_历史归档" in rel) or ("99_待整理资料" in rel):
                archived += 1
            else:
                active += 1
                if rel.startswith(os.path.join("02_共享基础", "公共计算")):
                    shared += 1
    return active, archived, shared


RE_CH = re.compile(r"第(\d+)章")


def scan_books():
    md_files = 0
    md_bytes = 0
    chapters = set()
    chapter_files = 0
    for dirpath, dirnames, filenames in os.walk(BOOKS):
        dirnames[:] = [d for d in dirnames if d not in (".git", "发布")]
        # 本书自身不计入被审面：写盘不移动自家读数
        if _inside_book(dirpath):
            continue
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            if fn.lower().endswith(".md"):
                md_files += 1
                md_bytes += os.path.getsize(full)
                # 章号只从 v1_正文 取：02 科普书稿另有 47 章同名号，混入会虚增覆盖
                if os.path.commonpath([V1, full]) == V1:
                    m = RE_CH.search(fn)
                    if m:
                        chapters.add(int(m.group(1)))
                        chapter_files += 1
    return md_files, md_bytes, sorted(chapters), chapter_files


NOGO = ["A", "C", "D", "E", "F", "H", "J", "K", "L", "N", "P", "Q"]


def scan_theorems():
    hits = collections.Counter()
    if not os.path.isdir(V1):
        return hits
    for dirpath, dirnames, filenames in os.walk(V1):
        for fn in filenames:
            if not fn.lower().endswith(".md"):
                continue
            text = read_text(os.path.join(dirpath, fn))
            for tag in NOGO:
                hits[tag] += len(re.findall(r"定理\s*%s(?!\w)" % tag, text))
    return hits


def main():
    print("== 《全维全链路总账》只读普查 ==")
    print("root = %s" % ROOT)

    # ---------------- 账一 体系
    print("\n[账一] 体系")
    if not os.path.isfile(REGISTRY):
        print("HARD-FAIL 缺 system_registry.json: %s" % REGISTRY)
        return 2
    reg = json.loads(read_text(REGISTRY)).get("systems")
    if not isinstance(reg, list) or not reg:
        print("HARD-FAIL systems 非列表或为空")
        return 2
    kinds = collections.Counter(x.get("kind", "(空)") for x in reg)
    states = collections.Counter(x.get("status", "(空)") for x in reg)
    ids = [x.get("id", "") for x in reg]
    ctl("S1", len(ids) == len(set(ids)), "体系 id 唯一（%d 个）" % len(ids))
    ctl("S2", len(reg) >= 10, "体系数 %d" % len(reg))
    DATA["systems"] = {
        "count": len(reg),
        "kinds": dict(kinds),
        "status": dict(states),
        "rows": [
            {
                "id": x.get("id"),
                "title": x.get("title"),
                "kind": x.get("kind"),
                "status": x.get("status"),
                "revision": x.get("hypothesis_revision"),
            }
            for x in reg
        ],
    }

    # ---------------- 账二 主张
    print("\n[账二] 主张")
    total_claims = 0
    width_ok_claims = 0
    status_all = collections.Counter()
    evidence_all = collections.Counter()
    per_system = []
    malformed_all = []
    for x in reg:
        p = os.path.join(SYSTEMS, x.get("directory", ""), "claims.csv")
        if not os.path.isfile(p):
            per_system.append({"id": x.get("id"), "claims": 0, "missing": True})
            continue
        n, n_ok, st, ev, bad = scan_claims(p)
        total_claims += n
        width_ok_claims += n_ok
        status_all.update(st)
        evidence_all.update(ev)
        per_system.append({"id": x.get("id"), "claims": n, "width_ok": n_ok, "missing": False})
        if bad:
            malformed_all.append({"id": x.get("id"), "lines": bad[:20], "n": len(bad)})
    zeros = [r["id"] for r in per_system if r["claims"] == 0 and not r.get("missing")]
    ctl("C1", total_claims > 0, "claims 非空行 Σ = %d" % total_claims)
    ctl("C2", len(per_system) == len(reg), "逐体系读取面 %d/%d" % (len(per_system), len(reg)))
    ctl("C3", width_ok_claims + sum(m["n"] for m in malformed_all) == total_claims,
        "列宽账闭合：合格 %d + 异常 %d = %d"
        % (width_ok_claims, sum(m["n"] for m in malformed_all), total_claims))
    DATA["claims"] = {
        "total": total_claims,
        "width_ok": width_ok_claims,
        "width_bad": total_claims - width_ok_claims,
        "status": dict(status_all),
        "evidence": dict(evidence_all),
        "per_system": per_system,
        "malformed": malformed_all,
        "zero_systems": zeros,
    }

    # ---------------- 账三 书稿
    print("\n[账三] 书稿")
    md_files, md_bytes, chapters, chapter_files = scan_books()
    vols = [d for d in os.listdir(V1) if os.path.isdir(os.path.join(V1, d))] if os.path.isdir(V1) else []
    ctl("B1", md_files > 0, "md 件数 = %d，字节 = %d" % (md_files, md_bytes))
    ctl("B2", len(chapters) > 0, "章号覆盖 %d..%d（去重 %d；章文件 %d）"
        % (chapters[0], chapters[-1], len(chapters), chapter_files))
    ctl("B3", len(vols) > 0, "v1_正文 编目录 %d" % len(vols))
    DATA["books"] = {
        "md_files": md_files,
        "md_bytes": md_bytes,
        "chapters_min": chapters[0] if chapters else None,
        "chapters_max": chapters[-1] if chapters else None,
        "chapters_unique": len(chapters),
        "chapter_files": chapter_files,
        "volumes": len(vols),
    }

    # ---------------- 账四 仪器
    print("\n[账四] 仪器")
    active, archived, shared = count_scripts()
    ctl("P1", active > 0, "活跃脚本 %d（历史归档 %d）" % (active, archived))
    ctl("P2", shared > 0, "02_共享基础/公共计算 %d" % shared)
    DATA["scripts"] = {"active": active, "archived": archived, "shared": shared}

    # ---------------- 账五 定理
    print("\n[账五] no-go 定理落名")
    thm = scan_theorems()
    named = [t for t in NOGO if thm.get(t, 0) > 0]
    ctl("T1", len(named) >= 6, "落名定理 %d/%d" % (len(named), len(NOGO)))
    DATA["theorems"] = {"counts": dict(thm), "named": named}

    # ---------------- 对照（尺必须有牙）
    print("\n[对照] 尺的牙")
    synth = [
        ["claim_id", "statement", "evidence_level", "status"],
        ["X1", "s", "mathematical_result", "verified"],
        ["X2", "s", "numerical_check", "falsified"],
        ["X3", "s", "conjecture", "unreviewed"],
        ["X4", "short"],
    ]
    n, n_ok, st, ev, bad = parse_claims_rows(synth)
    ctl("P1a", n == 4 and n_ok == 3 and st["verified"] == 1 and st["falsified"] == 1 and bad == [5],
        "正对照：4 行（3 列宽合格；1 verified/1 falsified/1 unreviewed；1 行宽异常）")
    synth_bad = [row[:] for row in synth]
    synth_bad[1][3] = "falsified"
    n2, n2_ok, st2, _, _ = parse_claims_rows(synth_bad)
    ctl("N1", n2 == 4 and n2_ok == 3 and st2["verified"] == 0 and st2["falsified"] == 2,
        "负对照：改一条 status ⇒ 读数随动（verified %d→0）" % st["verified"])
    ch_a = {int(m.group(1)) for fn in ["第1章_x.md", "第02章_y.md"] for m in [RE_CH.search(fn)] if m}
    ch_b = {int(m.group(1)) for fn in ["第1章_x.md"] for m in [RE_CH.search(fn)] if m}
    ctl("N2", len(ch_a) == 2 and len(ch_b) == 1, "负对照：删一章 ⇒ 章数 2→1")

    # ---------------- 汇总
    print("\n[汇总] 聚合数（唯一权威面）")
    if FAILS:
        print("CONTROL-RED · 对照 %d/%d 绿 · 不印聚合数" % (len(CHECKS) - len(FAILS), len(CHECKS)))
        return 2
    print("体系 = %d" % len(reg))
    print("主张非空行 Σ = %d（列宽合格 %d／异常 %d）"
          % (total_claims, width_ok_claims, total_claims - width_ok_claims))
    print("书稿 md = %d 件 / %d B" % (md_files, md_bytes))
    print("章 = %d..%d（去重 %d）" % (chapters[0], chapters[-1], len(chapters)))
    print("编目录 = %d" % len(vols))
    print("活跃脚本 = %d（历史 %d；共享基础 %d）" % (active, archived, shared))
    print("对照 %d/%d 绿" % (len(CHECKS), len(CHECKS)))
    print("CENSUS-GREEN")

    out = os.path.join(HERE, "full_chain_census.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(DATA, fh, ensure_ascii=False, indent=2)
    print("json -> %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
