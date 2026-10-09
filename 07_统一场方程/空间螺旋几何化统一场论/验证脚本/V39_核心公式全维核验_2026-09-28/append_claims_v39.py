# -*- coding: utf-8 -*-
"""Append this round's claims to claims.csv without touching a single standing byte.

Why a driver instead of hand editing:
  * claim ids must be READ from the ledger's last row at run time (concurrent writers exist in this folder);
  * the ledger is CRLF, statements must contain no ASCII comma, and the file has to re-parse to the same
    86 rows afterwards -- all three are cheaper to assert here than to regret later;
  * the write is all-or-restore, and the pre-write image is snapshotted OUTSIDE the repo with O_EXCL
    (a snapshot taken by a later run would capture the post-landing state instead of the pre-landing one).

Usage:  PYTHONIOENCODING=utf-8 python 验证脚本/V39_核心公式全维核验_2026-09-28/append_claims_v39.py [--check]
"""
import csv
import hashlib
import io
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SERIES = os.path.dirname(os.path.dirname(HERE))
CSV = os.path.join(SERIES, "claims.csv")
FACE = "V3_9_core_formula_checks.json"

ROWS = [
    ("θ 符号复用（N1：体系一的螺旋参数与体系二/四的倾角同写为一个 θ，仪器现读 ρ/ℓ 对螺旋参数的导数为 0 而 cosθ 的导数为 -sinθ）"
     "与 01A §3.2 α 本源验算的三处硬错误（N2：印出的 asin(α) 低于 α 本身；表中 1/asin(α) 行实为 1/α 行"
     "（对 01A 自家锚点差 -3.6958011e-9）；sin 形式在同一锚点上把吻合度从 -6.6865948e-9 破坏到 -8.8818885e-6 即约三个数量级）"
     "——读数面 %s 的 checks.N1_theta_conflation 与 checks.N2_asin_vs_sin_closure" % FACE,
     "元审计", "falsified"),
    ("N 的打印精度与四力表列的可达性各自只在一套 α 口径下成立（N7：总纲印 18916.90839 在主锚点不可达而 01A §3.2 旧锚可达"
     "（gap 4.94575e-6 对半格 5.0e-6）；两锚点相对差 6.80874e-10 为主锚点相对 1σ 的 4.44306 倍故不互为倒数；"
     "N8：主锚点下归一化列 S 不可达且强度因子列 G 印 18769=137² 而锚点给 18778.8650704）；"
     "正结果为体系七无穷级数 Σ_{n=-2}^{∞}α^n 的闭式即定义 A（残差 1.62199e-41 对删末项变异 5.32514e-5）"
     "——级数闭式判 PASS 而口径可达性判缺陷 故整条记 boundary；读数见 %s 的 checks.N7_anchor_vintage "
     "与 checks.S3_four_force_table 与 checks.S3_series_closure 与 checks.S3_N_definitions" % FACE,
     "一致性检查", "boundary"),
    ("量纲普查与应用式裁定（N3：κ_drive=ρω²/c² 量纲 L⁻¹ 与期望一致 是体系六唯一量纲自洽的应用式 PASS；"
     "N4：G_eff(E)∝1/E² 缺 ħ 与 c 的闭合因子 FAIL as written；N5：体系九「表观=归一化×耦合因子」的耦合因子由目标 10⁻³⁶ 反解 "
     "coupling_factor_needed_to_close=1.007351e-36 故无预言力；N6：体系十算术全对而物理为零——18917 双重素数成立"
     "但 α=1/137 口径下 round(N_B)=18907=7×37×73 为合数 该条复现 01A 已有的 X12 非新增缺陷）"
     "另有 X 命名空间实测：01A 台账为 X1-X5 加 X8-X15 而 X6/X7 在该文档中不存在——"
     "读数见 %s 的 checks.S2_dimension_sweep 与 checks.N5_apparent_strength_factorization "
     "与 checks.N6_prime_anchor" % FACE,
     "第一性审计", "info"),
]
REVIEWER = "本项目审计组"


def parse(raw):
    return list(csv.reader(io.StringIO(raw.replace("\r\n", "\n"))))


def main():
    dry = "--check" in sys.argv
    raw = open(CSV, "rb").read()
    assert raw.count(b"\r\n") == raw.count(b"\n") == raw.count(b"\r"), "claims.csv is not CRLF-pure"
    assert raw.endswith(b"\r\n"), "claims.csv does not end with a CRLF"
    text = raw.decode("utf-8")
    rows = parse(text)
    header, data = rows[0], rows[1:]
    assert header == ["claim_id", "statement", "category", "status", "reviewer"], header
    last_id = data[-1][0]
    assert re.fullmatch(r"C\d+", last_id), last_id
    ids = [int(r[0][1:]) for r in data]
    assert ids == sorted(ids), "claim ids are not monotonically appended"
    assert len(set(ids)) == len(ids), "duplicate claim ids on disk"
    start = ids[-1] + 1
    print("ledger read at run time: %d data rows, last id %s -> new ids %s"
          % (len(data), last_id, ", ".join("C%d" % (start + i) for i in range(len(ROWS)))))
    new_lines = []
    standing_statements = {r[1] for r in data}
    assert len({r[1] for r in ROWS}) == len(ROWS), "two of this round's rows carry the same statement"
    for i, (stmt, cat, status) in enumerate(ROWS):
        cid = "C%d" % (start + i)
        for token in (stmt, cat, status, cid):
            assert "," not in token, "ASCII comma inside cell would need quoting: %s" % token[:40]
            assert "\r" not in token and "\n" not in token
        line = "%s,%s,%s,%s,%s" % (cid, stmt, cat, status, REVIEWER)
        # A lander's own output is the next run's disk state.  The guard is on the STATEMENT, not the
        # rendered row: ids advance with the ledger, so a row-level comparison would re-append a
        # duplicate verdict under a fresh id.
        if stmt in standing_statements:
            print("already appended (statement found on disk, id %s not taken)" % cid)
            continue
        new_lines.append(line)
    if not new_lines:
        print("nothing to append: every statement is already on disk (idempotent no-op)")
        return 0
    out = (text + "\r\n".join(new_lines) + "\r\n").encode("utf-8")
    after = parse(out.decode("utf-8"))
    assert [r[0] for r in after[1:]][-len(new_lines):] == ["C%d" % (start + i) for i in range(len(ROWS))]
    assert len(after) - 1 == len(data) + len(new_lines), (len(after) - 1, len(data))
    assert [r[0] for r in after[1:1 + len(data)]] == [r[0] for r in data], "standing ids moved"
    assert out.startswith(raw), "the append is not byte-prefix-preserving"
    print("rows %d -> %d; bytes %d -> %d (+%d); CRLF %d -> %d"
          % (len(data), len(after) - 1, len(raw), len(out), len(out) - len(raw),
             raw.count(b"\r\n"), out.count(b"\r\n")))
    print("grew by exactly the new lines: %s"
          % (len(out) - len(raw) == sum(len(l.encode("utf-8")) + 2 for l in new_lines)))
    assert len(out) - len(raw) == sum(len(l.encode("utf-8")) + 2 for l in new_lines)
    for r in after[1:][start - 1:]:
        assert len(r) == 5 and r[3] in ("pass", "open", "falsified", "boundary", "BOUNDARY", "info"), r[:1]
    # teeth: every check key named in a statement must exist in the reading face
    import json
    face = json.load(open(os.path.join(SERIES, FACE), encoding="utf-8"))
    named = set(re.findall(r"(?<![A-Za-z0-9_])checks\.([A-Za-z0-9_]+)", "\r\n".join(new_lines)))
    missing = sorted(named - set(face["checks"]))
    print("check keys named by the new rows: %d; not present in the face: %s" % (len(named), missing))
    assert not missing, "a statement cites a reading-face key that does not exist: %s" % missing
    assert FACE in face["meta"]["checks_face"], "the face does not name itself"
    # teeth: every decimal in a new statement must be a reading of the face, sign included.
    # Section numbers (§3.2) are STRUCTURAL tokens: they are stripped before tokenizing, not exempted by value,
    # so an exemption bucket can never silently swallow a measurement.
    face_text = open(os.path.join(SERIES, FACE), encoding="utf-8").read()
    prose = re.sub(r"§\s*\d+(?:\.\d+)*", "", "\r\n".join(new_lines))
    tokens = sorted(set(re.findall(r"-?\d+\.\d+(?:e[-+]?\d+)?", prose)))
    unattached = [t for t in tokens if t not in face_text]
    print("decimals in the new rows: %d; face-attached %d; UNATTACHED %s"
          % (len(tokens), len([t for t in tokens if t in face_text]), unattached))
    assert not unattached, "a statement prints a number the face does not: %s" % unattached
    assert any(t.startswith("-") for t in tokens), "the sign is not part of any checked token"
    if dry:
        print("CHECK ONLY: nothing written")
        return 0
    backup = os.path.join(tempfile.gettempdir(), "v39_claims_backup_%d.bin" % os.getpid())
    fd = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
    with os.fdopen(fd, "wb") as fh:
        fh.write(raw)
    tmp = CSV + ".tmp"
    try:
        with open(tmp, "wb") as fh:
            fh.write(out)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, CSV)
        b = open(CSV, "rb").read()
        assert b == out and b.count(b"\r\n") == b.count(b"\n") == b.count(b"\r")
    except Exception as exc:
        if os.path.exists(tmp):
            os.remove(tmp)
        open(CSV, "wb").write(open(backup, "rb").read())
        print("FAILED (%s) -> restored claims.csv from %s" % (type(exc).__name__, backup), file=sys.stderr)
        raise
    print("WROTE claims.csv: %d bytes / %d CRLF-lines / %d data rows sha256[:16]=%s"
          % (len(b), b.count(b"\r\n"), len(parse(b.decode("utf-8"))) - 1,
             hashlib.sha256(b).hexdigest()[:16]))
    print("backup of the pre-write image: %s (%d bytes)" % (backup, os.path.getsize(backup)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
