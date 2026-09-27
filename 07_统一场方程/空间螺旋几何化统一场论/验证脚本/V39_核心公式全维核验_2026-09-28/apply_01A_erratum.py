# -*- coding: utf-8 -*-
"""Append the labelled 2026-09-28 erratum to 01A_附录_体系不自洽点专项复盘.md (round V39).

01A's own header promises append-only, so the three wrong rows of its §3.2 table stay on disk
untouched; this driver inserts (a) an erratum block right after §3.2's last line and (b) one row
at the end of the §7 patch-ledger table.  CRLF is preserved, the write is all-or-restore, and
every number in the inserted text is a reading of V3_9_core_formula_checks.json, whose size and
sha256 prefix this driver pins before touching the target.

Usage:  PYTHONIOENCODING=utf-8 python 验证脚本/V39_核心公式全维核验_2026-09-28/apply_01A_erratum.py [--check]
  --check  run every assertion on the would-be output and exit 0 WITHOUT writing
"""
import hashlib
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SERIES = os.path.dirname(os.path.dirname(HERE))          # .../空间螺旋几何化统一场论
TARGET = os.path.join(SERIES, "01A_附录_体系不自洽点专项复盘.md")
FACE = os.path.join(SERIES, "V3_9_core_formula_checks.json")

# --- pin of the reading face this erratum quotes (measured by stat, not typed from memory) ----
FACE_BYTES = 18518          # bytes on disk
FACE_LF_LINES = 440         # count of b'\n'
FACE_SHA16 = "17063a995f0b0276"

ANCHOR_32 = "三条路径的自洽性另见 §5（`N_twist` 链条与 `α=1/137` 互斥）。"
ANCHOR_7 = "| 频率控制（X11/X14/X15） | 每式补带量纲修正因子；或整式重写 | **+1～+3** |"

ERRATUM = [
    "> **【2026-09-28 勘误 · 本节表格的三行数值不成立（追加，上表原样保留）】** "
    "由新写的独立仪器 "
    "[`验证脚本/V39_核心公式全维核验_2026-09-28/core_formula_full_audit.py`]"
    "(验证脚本/V39_核心公式全维核验_2026-09-28/core_formula_full_audit.py) 复算，"
    "读数面 [`V3_9_core_formula_checks.json`](V3_9_core_formula_checks.json)"
    "（18,518 B / 440 行 LF / sha256 前 16 位 `17063a995f0b0276`），"
    "本节字段路径 `checks.N2_asin_vs_sin_closure`；叙述见 "
    "[`24_TUFT核心公式全维核验_体系一至十_2026-09-28.md`]"
    "(24_TUFT核心公式全维核验_体系一至十_2026-09-28.md) §2(c)。"
    "锚点取**本表自印**的 `α = 7.2973525693e-03`：",
    ">",
    "> | 本表原值 | 复算结果（读数面字段 = 值） | 裁定 |",
    "> |---|---|---|",
    "> | `asin(α)` = 7.29722e-03 | `asin_of_01A_alpha = 0.0072974173365035`、"
    "`asin_gt_alpha = true`、`gap_of_printed_asin_vs_true_asin = 1.9733153e-7` | "
    "**错**：x>0 时 asin(x)>x，印出的值却**小于** α ⇒ 该行不可能是 asin。"
    "退一步读成 sin 也救不回：`sin_of_01A_alpha = 0.007297287803821` 距印出的 7.29722e-03 差 "
    "`row2_sin_reading_in_half_ulps = 13.56` 个半格（该行 6 位有效 ⇒ `row2_half_ulp = 5.0e-9`），"
    "asin 读法差 `row2_asin_reading_in_half_ulps = 39.47` 个 ⇒ **两个算子都复现不出这一行**",
    "> | `1/asin(α)` = 137.03599908 | `equals_reciprocal_of_01A_alpha = 137.0359990837`（即 `1/α`）、"
    "`gap_doc_row_vs_reciprocal_of_01A_alpha = -3.6958011e-9` | "
    "**错**：填的是上一行 α 的倒数。真正的 `1/asin` 是 "
    "`one_over_asin_of_01A_alpha = 137.03478283992`；而把本表印出的 asin 字面取倒数得 "
    "`recip_of_doc_printed_asin = 137.03848862992`，与本行差 "
    "`internal_gap_of_doc_rows = 0.0024895499` ⇒ **相邻两行连互为倒数都不成立**",
    "> | `Δ_top` = 0.03599908，注「文献称 ≈0.036 ✔ 数值一致」 | "
    "`delta_top_sin_form_on_01A_anchor = 0.0347828399168`、"
    "`delta_top_linear_form_on_01A_anchor = 0.0359990836958` | "
    "**✔ 没有挣到**：sin 形式要求的 Δ_top 是 0.03478；0.035999 是**去掉 sin 的线性形式**反解出来的数",
    ">",
    "> 若真按 sin 形式算到底：`alpha_pred_from_doc_sin_form = 0.0072972877550278`，相对偏差 "
    "`rel_error_of_doc_sin_form_on_01A_anchor = -8.8818885e-6`，"
    "而线性形式同一处只差 `rel_error_of_linear_form_on_01A_anchor = -6.6865948e-9`"
    " ⇒ **写成 sin 反使吻合度恶化约三个数量级**，折成主锚点 1σ"
    "（`meta.external_anchors.alpha_inv_1sigma_relative = 1.532e-10`）为 "
    "`how_many_alpha_sigmas_off = 57954.532` 倍。",
    ">",
    "> **裁定不变、理由要换**：本节「该式对 α 的信息贡献 = 0」依然成立"
    "> （`N=137` 是输入、`Δ_top` 是反解输出），但支撑它的那张表本身算错了三行；"
    "> 且把 sin 换回线性近似就复现 α ⇒ **该式里的 sin 是装饰**，这正是它只是恒等式的证据。",
    ">",
    "> 另注（锚点口径）：本表把 `7.2973525693e-03` 标为「CODATA 2018」，它与 α⁻¹ = 137.035999177(21) "
    "的相对差 `checks.N7_anchor_vintage.rel_gap_between_anchors = 6.80874e-10`，已是后者 1σ 的 "
    "`rel_gap_in_units_of_primary_rel_sigma = 4.44306` 倍 ⇒ 两个锚点分属不同口径"
    "（本轮不裁定具体年份），**同一条推导里不得混用**；`18916.90839` 与 `18907` 两个「冲突值」"
    "各自只在不同锚点下可达（见 `24_…` §3 的 N7 条）。",
]

ROW_7 = ("| §3.2 三行验算（X4 的佐证，2026-09-28 勘误追加） | "
         "0 新假设：sin 换回线性近似即复现 α，X4 判定不变（仅表格三行需按勘误块读） | 0（纯治理） |")


def read_target():
    raw = open(TARGET, "rb").read()
    assert raw.count(b"\r\n") == raw.count(b"\n") == raw.count(b"\r"), (
        "01A is expected to be uniformly CRLF; got LF=%d CRLF=%d CR=%d"
        % (raw.count(b"\n"), raw.count(b"\r\n"), raw.count(b"\r")))
    return raw


def check_face():
    fb = open(FACE, "rb").read()
    got = (len(fb), fb.count(b"\n"), hashlib.sha256(fb).hexdigest()[:16])
    want = (FACE_BYTES, FACE_LF_LINES, FACE_SHA16)
    assert got == want, "reading face moved: disk=%s pinned=%s -> re-measure before writing" % (got, want)
    return got


def build(raw):
    lines = raw.decode("utf-8").split("\r\n")
    i1 = [i for i, l in enumerate(lines) if l == ANCHOR_32]
    i7 = [i for i, l in enumerate(lines) if l == ANCHOR_7]
    assert len(i1) == 1 and len(i7) == 1, "anchors must be unique: §3.2=%d §7=%d" % (len(i1), len(i7))
    n0 = len(lines)
    out = lines[:i1[0] + 1] + [""] + ERRATUM + lines[i1[0] + 1:]
    j7 = [i for i, l in enumerate(out) if l == ANCHOR_7]
    assert len(j7) == 1
    out = out[:j7[0] + 1] + [ROW_7] + out[j7[0] + 1:]
    assert len(out) == n0 + len(ERRATUM) + 2, (len(out), n0, len(ERRATUM))
    new_bytes = ("\r\n".join(out)).encode("utf-8")
    # append-only proof: every original line survives, in order, unchanged
    assert new_bytes.count(raw[:4000]) == 1, "head of the document moved -> not append-only"
    for l in lines:
        if l:
            assert new_bytes.count(l.encode("utf-8")) >= 1, "original line lost: %r" % l[:40]
    return raw, new_bytes, n0, len(out)


def flatten(node, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, (dict, list)):
                flatten(v, out)
            else:
                out.setdefault(k, set()).add(v if isinstance(v, str) else str(v))
    elif isinstance(node, list):
        for v in node:
            flatten(v, out)
    return out


QUOTE = re.compile(r"(?<![A-Za-z0-9_.])([A-Za-z][A-Za-z_0-9]*(?:\.[A-Za-z][A-Za-z_0-9]*)*)"
                   r" = (-?[0-9][0-9.e+-]*)")


def verify_quotes_against_face(face_sha16=None):
    """Every `key = value` the erratum prints must exist in the reading face with that exact value."""
    import json
    face = json.loads(open(FACE, "rb").read().decode("utf-8"))
    flat = flatten(face, {})
    quoted, bad, unchecked = [], [], []
    for line in ERRATUM + [ROW_7]:
        for path, val in QUOTE.findall(line):
            key = path.split(".")[-1]
            if len(key) < 4:
                continue          # N=137 and other prose tokens are not face readings
            quoted.append((key, val))
            if key not in flat:
                unchecked.append(key)
            elif val not in flat[key]:
                bad.append((key, val, sorted(flat[key])[:3]))
    print("erratum quotes %d `key = value` readings off the face; matched=%d mismatched=%d "
          "key-not-in-face=%r" % (len(quoted), len(quoted) - len(bad) - len(unchecked), len(bad),
                                  sorted(set(unchecked))))
    assert not bad, "printed value differs from the face: %r" % bad[:5]
    assert not unchecked, "quoted key is not a reading of the face: %r" % sorted(set(unchecked))
    return len(quoted)


def main():
    dry = "--check" in sys.argv
    assert os.path.dirname(TARGET) == SERIES
    print("face pin (bytes, LF-lines, sha16):", check_face())
    verify_quotes_against_face()
    raw = read_target()
    before, after, n0, n1 = build(raw)
    print("target: %d chars / %d CRLF-lines before -> %d CRLF-lines after; %d bytes before -> %d bytes after"
          % (len(raw.decode("utf-8")), n0, n1, len(before), len(after)))
    assert len(after) > len(before)
    exempt = []
    for probe in ERRATUM + [ROW_7]:
        if len(probe) < 8:
            # a bare blockquote marker cannot be attributed to this insertion; enumerate, do not hide
            exempt.append(probe)
            continue
        assert after.count(probe.encode("utf-8")) == 1, "inserted text not unique: %r" % probe[:40]
    print("uniqueness-checked lines: %d / %d inserted (exempt as too short to attribute: %r)"
          % (len(ERRATUM) + 1 - len(exempt), len(ERRATUM) + 1, exempt))
    assert sum(after.count(p.encode("utf-8")) for p in exempt) >= len(exempt), "blank quote rows vanished"
    if dry:
        print("CHECK ONLY: nothing written")
        return 0

    backup = os.path.join(tempfile.gettempdir(), "01A_erratum_backup_%d.bin" % os.getpid())
    fd = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL)   # refuse to overwrite an old image
    with os.fdopen(fd, "wb") as fh:
        fh.write(before)
    print("backup written (bytes) outside the repo:", backup, len(before))

    tmp = TARGET + ".tmp"
    try:
        with open(tmp, "wb") as fh:
            fh.write(after)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, TARGET)
        disk = read_target()
        assert disk == after, "disk does not equal the built image"
        assert disk.count(b"\r\n") == disk.count(b"\n") == disk.count(b"\r") == n1 - 1
    except Exception as exc:
        if os.path.exists(tmp):
            os.remove(tmp)
        with open(backup, "rb") as fh:
            restore = fh.read()
        with open(TARGET, "wb") as fh:
            fh.write(restore)
            fh.flush()
            os.fsync(fh.fileno())
        print("FAILED (%s) -> restored %d bytes from %s" % (type(exc).__name__, len(restore), backup))
        raise
    print("WROTE %s: %d bytes / %d CRLF-lines (was %d bytes / %d); sha256[:16]=%s"
          % (os.path.basename(TARGET), len(disk), n1 - 1, len(before), n0 - 1,
             hashlib.sha256(disk).hexdigest()[:16]))
    print("erratum block lines=%d + §7 row 1; original §3.2 table rows byte-identical (append-only asserted)"
          % len(ERRATUM))
    return 0


if __name__ == "__main__":
    sys.exit(main())
