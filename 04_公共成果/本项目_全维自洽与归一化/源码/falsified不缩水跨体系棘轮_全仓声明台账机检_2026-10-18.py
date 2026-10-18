# -*- coding: utf-8 -*-
"""§七.5 falsified-set ratchet: cross-system, read-only check, explicit-approval growth.

Total ledger §七.5 requires: the `falsified` set must never shrink, archive hashes
unchanged, anti-regression guard stays a CI gate. The existing guard
(空间螺旋判定_总览与防回潮守卫.py) covers only its own 审计组 subset (40 ids) and it
auto-writes growth into its baseline. This engine covers the whole live corpus and
registers growth ONLY through an explicit --update-baseline.

Membership currency is positional-any (the token 'falsified' appears as a whole field
value anywhere in the row), because 113/587 live rows have a field count different from
their header, which moves the status token into a neighbouring column.

Usage:
    python -B falsified_census_v1.py                 # build/refresh face, check vs baseline
    python -B falsified_census_v1.py --update-baseline
    python -B falsified_census_v1.py --selftest
Exit: 0 ok | 1 shrinkage or channel disagreement | 2 hard throw (scope/schema)
"""
import csv
import glob
import hashlib
import io
import json
import os
import subprocess
import sys
import time

TOK = "falsified"
HERE = os.path.dirname(os.path.abspath(__file__))
# scratch copy walks 1 level; the registered copy under 源码/ walks 4 levels.
ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir, os.pardir))
OPENUFT = os.path.join(ROOT, "openuft")
DATA = os.path.join(ROOT, "openuft", "04_公共成果", "本项目_全维自洽与归一化", "数据")
FACE = "falsified不缩水跨体系台账_2026-10-18.json"
BASE = "falsified不缩水基线_跨体系台账_2026-10-18.json"
AUDIT_BASELINE = "空间螺旋判定_不变量基线.json"


class Fatal(Exception):
    pass


def live_scope():
    out = []
    for f in sorted(glob.glob(os.path.join(OPENUFT, "01_独立体系", "*", "claims.csv"))):
        out.append((os.path.basename(os.path.dirname(f)), f))
    g = os.path.join(OPENUFT, "07_统一场方程", "空间螺旋几何化统一场论", "claims.csv")
    if os.path.isfile(g):
        out.append(("07:空间螺旋几何化统一场论", g))
    return out


def archive_scope():
    return sorted(glob.glob(os.path.join(OPENUFT, "90_历史归档", "**", "claims.csv"),
                            recursive=True))


def read_rows(path):
    txt = io.open(path, encoding="utf-8-sig", newline="").read()
    rows = [r for r in csv.reader(io.StringIO(txt)) if r and any(x.strip() for x in r)]
    if not rows:
        raise Fatal("no header/rows in %s" % path)
    return rows[0], rows[1:]


def classify(hdr, body, sysname="?"):
    """Pure row classifier shared by the census and every mutant control.

    Uniqueness lives here, not in the caller, so a control that feeds classify() a
    hand-made row set gets the same guarantee as the corpus scan.
    """
    if "claim_id" not in hdr:
        raise Fatal("header lacks claim_id: %r" % (hdr[:3],))
    si = hdr.index("status") if "status" in hdr else None
    res = []
    seen = set()
    for r in body:
        cid = r[0].strip()
        if not cid:
            raise Fatal("row without claim_id: %r" % (r[:2],))
        if cid in seen:
            raise Fatal("duplicate claim_id %r inside %s (a set ratchet cannot "
                        "index it)" % (cid, sysname))
        seen.add(cid)
        fields = [x.strip() for x in r]
        res.append({
            "id": cid,
            "any": TOK in fields,
            "stat": si is not None and len(r) > si and fields[si] == TOK,
            "wf": len(r) == len(hdr),
            "width": len(r),
            "npos": [i for i, x in enumerate(fields) if x == TOK],
        })
    return res


def census(pairs):
    per = {}
    detail = {}
    files = 0
    rown = 0
    wf_tok_outside = []
    shifted_tok = []
    for sysname, path in pairs:
        files += 1
        hdr, body = read_rows(path)
        got = classify(hdr, body, sysname)
        rown += len(got)
        for g in got:
            if g["any"] and not g["wf"]:
                shifted_tok.append((sysname, g["id"], g["width"], g["npos"]))
            if g["any"] and g["wf"] and not g["stat"]:
                wf_tok_outside.append((sysname, g["id"]))
        detail[sysname] = {"n_hdr": len(hdr), "n_rows": len(got),
                           "ids": sorted(g["id"] for g in got if g["any"]),
                           "ids_status_col": sorted(g["id"] for g in got if g["stat"])}
        per[sysname] = sorted(g["id"] for g in got if g["any"])
    if files == 0 or rown == 0:
        raise Fatal("scan set EMPTY (files=%d rows=%d) — zero defects read here is not "
                    "evidence" % (files, rown))
    adopted = {}
    for s, ids in per.items():
        adopted.setdefault(s, set())          # empty systems stay on the roster too
        for i in ids:
            adopted[s].add(i)
    return {"files": files, "rows": rown, "per_system": per, "detail": detail,
            "adopted_sets": adopted,
            "shifted_falsified": sorted(shifted_tok),
            "wf_token_outside_status": sorted(wf_tok_outside)}


def all_ids(c):
    s = set()
    for ids in c["per_system"].values():
        s |= set(ids)
    return s


def load_base():
    p = os.path.join(DATA, BASE)
    if not os.path.isfile(p):
        return None
    return json.load(io.open(p, encoding="utf-8"))


def diff(base_sets, cur_sets):
    shrink, grow = {}, {}
    for s, blist in base_sets.items():
        cur = cur_sets.get(s, set())
        miss = sorted(set(blist) - cur)
        if miss:
            shrink[s] = miss
    for s, cl in cur_sets.items():
        extra = sorted(cl - set(base_sets.get(s, [])))
        if extra:
            grow[s] = extra
    return shrink, grow


def arch_stratum():
    out = []
    for p in archive_scope():
        try:
            hdr, body = read_rows(p)
            got = classify(hdr, body)
            n = sum(1 for g in got if g["any"])
        except Fatal as e:
            n = -1
            out.append({"path": os.path.relpath(p, ROOT).replace("\\", "/"), "note": str(e)})
            continue
        out.append({"path": os.path.relpath(p, ROOT).replace("\\", "/"),
                    "rows": len(got), "falsified": n})
    return out


def md5(path):
    if not os.path.isfile(path):
        return None
    return hashlib.md5(io.open(path, "rb").read()).hexdigest()


def archive_hashes():
    """Archives are immutable by definition, so their digests belong in the baseline.

    A short digest is what the face and baseline carry: the ratchet compares short forms
    against each other and never mixes them with full-length citations.
    """
    out = {}
    for p in archive_scope():
        out[os.path.relpath(p, ROOT).replace("\\", "/")] = hashlib.sha256(
            io.open(p, "rb").read()).hexdigest()[:16]
    return out


def run_check(write_face=True, update=False, quiet=False):
    c = census(live_scope())
    ah = archive_hashes()
    base = load_base()
    verdicts = []
    rc = 0
    shrink = grow = {}
    if base is None:
        base = {"sets": {s: list(v) for s, v in c["adopted_sets"].items()}}
        verdicts.append(("B0", "baseline absent -> first run records it", True))
    else:
        bs = {s: set(v) for s, v in base["sets"].items()}
        shrink, grow = diff(bs, c["adopted_sets"])
        ok = not shrink
        verdicts.append(("B1", "falsified 集合不缩水（基线 %d 条）：缩水 %d 体系 / 生长 %d 体系"
                         % (sum(len(v) for v in base["sets"].values()), len(shrink), len(grow)), ok))
        if not ok:
            rc = 1
        lost = sorted(set(base["sets"]) - set(c["adopted_sets"]))
        verdicts.append(("B6", "体系名册不缩水（基线 %d 个体系，缺席 %d 个：%s）"
                         % (len(base["sets"]), len(lost), lost if lost else "无"), not lost))
        if lost:
            rc = 1
        # B7：归档层不可变——90_历史归档 下的 claims.csv 一旦被改动就是溯源事故
        bh = base.get("archive_sha256")
        if bh is None:
            verdicts.append(("B7", "归档哈希基线未登记（跑一次 --update-baseline 即建档）", True))
        else:
            chg = sorted(k for k in set(bh) | set(ah) if bh.get(k) != ah.get(k))
            verdicts.append(("B7", "归档 claims.csv 哈希不变（%d 个文件，变动/缺失 %d 个：%s）"
                             % (len(ah), len(chg), chg if chg else "无"), not chg))
            if chg:
                rc = 1
    ok2 = not c["wf_token_outside_status"]
    verdicts.append(("B2", "well-formed 行两通道一致（status 列 vs 位置任意）：%d 例不一致"
                     % len(c["wf_token_outside_status"]), ok2))
    if not ok2:
        rc = 1
    n_status = sum(len(v["ids_status_col"]) for v in c["detail"].values())
    n_adopt = sum(len(v) for v in c["per_system"].values())
    verdicts.append(("B3", "扫描集非空且 id 在体系内唯一（%d 文件 / %d 行 / 采纳 %d 条）"
                     % (c["files"], c["rows"], n_adopt), c["files"] > 0 and c["rows"] > 0))
    verdicts.append(("B4", "列位移行上的 falsified 单列可见性：%d 条只在位移列上（status 列口径 %d 条，"
                            "并集 %d 条）——纯 status 口径会漏这 %d 条"
                     % (len(c["shifted_falsified"]), n_status, n_adopt, n_adopt - n_status), True))
    if update:
        os.makedirs(DATA, exist_ok=True)
        with io.open(os.path.join(DATA, BASE), "w", encoding="utf-8", newline="\r\n") as fh:
            fh.write(json.dumps({"purpose": "跨体系 falsified 只许不缩水的基线；生长须经 --update-baseline 明确核准",
                                 "currency": "positional-any（'falsified' 作为整字段值出现即计入）",
                                 "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                 "files": c["files"], "rows": c["rows"],
                                 "sets": {s: sorted(v) for s, v in c["adopted_sets"].items()},
                                 "archive_sha256": ah},
                                ensure_ascii=False, indent=2) + "\n")
        verdicts.append(("B5", "基线已按明确指令更新（--update-baseline）", True))
    else:
        verdicts.append(("B5", "只读模式：未写基线（生长须经 --update-baseline 核准）", True))
    face = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "scope_live_files": c["files"], "scope_live_rows": c["rows"],
            "n_adopted_falsified": n_adopt, "n_status_column_falsified": n_status,
            "n_only_on_shifted_columns": n_adopt - n_status,
            "per_system": c["detail"],
            "shifted_falsified_rows": c["shifted_falsified"],
            "wf_token_outside_status": c["wf_token_outside_status"],
            "shrinkage": shrink, "growth_unregistered": grow,
            "archive_stratum_advisory": arch_stratum(),
            "archive_sha256_now": ah,
            "checks": [{"id": i, "name": n, "ok": bool(o)} for i, n, o in verdicts],
            "rc": rc}
    if write_face:
        os.makedirs(DATA, exist_ok=True)
        with io.open(os.path.join(DATA, FACE), "w", encoding="utf-8", newline="\r\n") as fh:
            fh.write(json.dumps(face, ensure_ascii=False, indent=2) + "\n")
    if not quiet:
        print("falsified 不缩水跨体系台账  rc=%d" % rc)
        print("  扫描 %d 个 live claims.csv / %d 行" % (c["files"], c["rows"]))
        print("  采纳 falsified %d 条（status 列口径 %d，只在位移列上 %d）"
              % (n_adopt, n_status, n_adopt - n_status))
        for s in sorted(c["per_system"]):
            print("    %-38s %3d" % (s, len(c["per_system"][s])))
        for i, n, o in verdicts:
            print("  [%s] %s %s" % ("PASS" if o else "FAIL", i, n))
        if shrink:
            print("  !! 缩水：%s" % json.dumps(shrink, ensure_ascii=False))
        if grow:
            print("  生长未登记：%s（要登记请跑 --update-baseline）"
                  % json.dumps(grow, ensure_ascii=False))
    return rc, face, c


def selftest():
    outs = []

    def ck(name, fired, note):
        outs.append((name, bool(fired), note))
        print("  %-4s %s | %s" % ("FIRED" if fired else "MISS", name, note))

    rc, face, c = run_check(quiet=True)
    sets = {s: set(v) for s, v in c["adopted_sets"].items()}
    tot = sum(len(v) for v in sets.values())
    # C1 drop-one mutant must be read as shrinkage
    victim = sorted([s for s in sets if sets[s]])[0]
    one = sorted(sets[victim])[0]
    mut = {k: set(v) for k, v in sets.items()}
    mut[victim].discard(one)
    sh, gr = diff(sets, mut)
    ck("C1 删一条 id 必须点火", sh.get(victim) == [one] and not gr,
       "%s/%s -> shrink=%s grow=%d" % (victim, one, sh.get(victim), len(gr)))
    # C2 column-shift repair must NOT change membership (currency stability)
    hdr, body = read_rows(dict(live_scope())["07:空间螺旋几何化统一场论"])
    row = [r for r in body if r[0].strip() == sorted(sets["07:空间螺旋几何化统一场论"])[0]][0]
    shifted = list(row)
    shifted.insert(2, "半段")                 # an unquoted comma splits one field in two
    base_cls = classify(hdr, [row])
    mut_cls = classify(hdr, [shifted])
    ck("C2 列位移不改成员资格（并集口径稳）",
       base_cls[0]["any"] and mut_cls[0]["any"] and mut_cls[0]["stat"] != base_cls[0]["stat"],
       "wf=%s->%s  any=%s->%s  status列=%s->%s"
       % (base_cls[0]["wf"], mut_cls[0]["wf"], base_cls[0]["any"], mut_cls[0]["any"],
          base_cls[0]["stat"], mut_cls[0]["stat"]))
    # C3 duplicate claim_id must hard-throw
    try:
        classify(hdr, [row, row])
        ck("C3 体系内重名 claim_id 必须硬抛", False, "未抛")
    except Fatal as e:
        ck("C3 体系内重名 claim_id 必须硬抛", True, str(e)[:48])
    # C4 empty scan set must hard-throw, not report "no defects"
    try:
        census([])
        ck("C4 空扫描集必须硬抛", False, "未抛")
    except Fatal as e:
        ck("C4 空扫描集必须硬抛", True, str(e)[:48])
    # C5 cross-instrument: the existing guard's own 40 audit ids must live inside
    #    this census's membership for that same file
    p = os.path.join(DATA, AUDIT_BASELINE)
    if os.path.isfile(p):
        audit = set(json.load(io.open(p, encoding="utf-8"))["falsified_audit_ids"])
        have = sets.get("07:空间螺旋几何化统一场论", set())
        ck("C5 与既有防回潮守卫基线同口径（40 条 ⊆ 本册该文件采纳集）",
           audit and audit.issubset(have),
           "守卫基线 %d 条，本册 %d 条，缺 %d 条" % (len(audit), len(have), len(audit - have)))
    else:
        ck("C5 与既有防回潮守卫基线同口径", False, "基线文件缺失 " + AUDIT_BASELINE)
    # C6 --check must not write the baseline (prove with md5 before/after a subprocess run)
    bp = os.path.join(DATA, BASE)
    before = md5(bp)
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    subprocess.run([sys.executable, "-B", os.path.abspath(__file__)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, env=env)
    ck("C6 只读跑不写基线", before is not None and before == md5(bp),
       "md5 %s -> %s" % (str(before)[:8], str(md5(bp))[:8]))
    # C7 known-good positive control: real corpus check passes
    ck("C7 正对照：真实语料 --check rc=0", rc == 0 and tot > 0, "rc=%d 采纳 %d 条" % (rc, tot))
    # C8 archive immutability must have teeth: perturb the recorded digest, expect rc=1,
    #    then restore the baseline byte-for-byte (this control never touches the corpus)
    bp2 = os.path.join(DATA, BASE)
    snap = io.open(bp2, "rb").read()
    bd = json.loads(snap.decode("utf-8"))
    ah_now = archive_hashes()
    if bd.get("archive_sha256"):
        k = sorted(bd["archive_sha256"])[0]
        bd["archive_sha256"][k] = "0" * 16
        io.open(bp2, "wb", ).write(json.dumps(bd, ensure_ascii=False, indent=2).replace(
            "\n", "\r\n").encode("utf-8"))
        r8 = subprocess.run([sys.executable, "-B", os.path.abspath(__file__)],
                            capture_output=True, encoding="utf-8", errors="replace", env=env)
        io.open(bp2, "wb").write(snap)
        ck("C8 归档哈希被改必须点火（并逐字节还原基线）",
           r8.returncode == 1 and "B7" in r8.stdout and "FAIL" in r8.stdout
           and hashlib.md5(io.open(bp2, "rb").read()).hexdigest()
           == hashlib.md5(snap).hexdigest() and len(ah_now) > 0,
           "rc=%d 归档文件 %d 个，还原=%s"
           % (r8.returncode, len(ah_now),
              hashlib.md5(io.open(bp2, "rb").read()).hexdigest() == hashlib.md5(snap).hexdigest()))
    else:
        ck("C8 归档哈希被改必须点火", False, "基线尚未登记 archive_sha256（先跑 --update-baseline）")
    bad = [n for n, f, _ in outs if not f]
    print("控制组 %d/%d 点火" % (len(outs) - len(bad), len(outs)))
    return 0 if not bad else 1


GUARD = os.path.join(OPENUFT, "04_公共成果", "本项目_全维自洽与归一化", "源码",
                     "空间螺旋判定_总览与防回潮守卫.py")


def ci():
    """CI entry: existing anti-regression guard + this cross-system ratchet, one rc.

    Deliberately does NOT edit the shared guard_all.py — wiring is documented instead.
    """
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    outs = []
    if os.path.isfile(GUARD):
        r = subprocess.run([sys.executable, "-B", GUARD], capture_output=True,
                           encoding="utf-8", errors="replace", env=env)
        tail = [l for l in (r.stdout or "").splitlines() if "守卫" in l or "结论" in l][-2:]
        outs.append(("既有防回潮守卫（审计组 40 条 + 归档哈希）", r.returncode, " / ".join(tail)))
    else:
        outs.append(("既有防回潮守卫", 2, "脚本缺失：" + GUARD))
    rc, _, _ = run_check(quiet=True)
    outs.append(("本册跨体系 falsified 棘轮（24 文件）", rc, "见台账 JSON"))
    worst = max(o[1] for o in outs)
    for n, c, d in outs:
        print("  [%s] %s rc=%d | %s" % ("PASS" if c == 0 else "FAIL", n, c, d))
    print("CI 入口合计 rc=%d" % worst)
    return worst


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    if "--ci" in args:
        return ci()
    try:
        rc, _, _ = run_check(update="--update-baseline" in args)
    except Fatal as e:
        print("HARD THROW: %s" % e)
        return 2
    return rc


if __name__ == "__main__":
    sys.exit(main())
