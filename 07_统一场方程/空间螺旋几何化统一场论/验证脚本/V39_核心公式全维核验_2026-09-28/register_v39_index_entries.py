# -*- coding: utf-8 -*-
"""Hand-insert the V39 round's artifacts into 00_项目治理/资料索引 (catalog + manifest).

refresh_catalog.py is NOT run here: it walks openuft/.git and pollutes the tracked index
(project memory: openuft-nested-git-and-index-refresh), and a full regeneration would also
re-mint 5,982 unrelated lines.  This driver therefore appends entries in place, keeps every
other byte identical, and proves that by rebuilding the ORIGINAL bytes from the new text after
deleting exactly the lines it added.  CRLF is preserved on both files; writes are all-or-restore.

Usage:  PYTHONIOENCODING=utf-8 python 验证脚本/V39_核心公式全维核验_2026-09-28/register_v39_index_entries.py [--check]
"""
import hashlib
import json
import os
import posixpath
import re
import sys
import tempfile
import time
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
OPENUFT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
IDX = os.path.join(OPENUFT, "00_项目治理", "资料索引")
CATALOG = os.path.join(IDX, "material_catalog.md")
MANIFEST = os.path.join(IDX, "structure_manifest.json")

SERIES = "07_统一场方程/空间螺旋几何化统一场论"
NEW = [
    SERIES + "/24_TUFT核心公式全维核验_体系一至十_2026-09-28.md",
    SERIES + "/V3_9_core_formula_checks.json",
    SERIES + "/验证脚本/V39_核心公式全维核验_2026-09-28/append_claims_v39.py",
    SERIES + "/验证脚本/V39_核心公式全维核验_2026-09-28/apply_01A_erratum.py",
    SERIES + "/验证脚本/V39_核心公式全维核验_2026-09-28/mutate_claims_v39.py",
    SERIES + "/验证脚本/V39_核心公式全维核验_2026-09-28/mutate_index_v39.py",
    SERIES + "/验证脚本/V39_核心公式全维核验_2026-09-28/register_v39_index_entries.py",
]
SECTION = "07_统一场方程"
# The index files hold posix-style paths, so the relative link base must be computed with posixpath
# on forward-slashed inputs (os.sep on Windows would otherwise leak backslashes into posixpath.relpath).
FWD = lambda p: p.replace(os.sep, "/")
RELDIR = posixpath.relpath(FWD(IDX), FWD(OPENUFT))


def parent(path):
    return path.rsplit("/", 1)[0] if "/" in path else ""


def group_sorted_labels(labels, note):
    """The index orders each same-parent folder group case-insensitively (verified on the standing text)."""
    by_parent = {}
    for l in labels:
        by_parent.setdefault(parent(l), []).append(l)
    unsorted_before = [p for p, g in by_parent.items() if g != sorted(g, key=str.casefold)]
    print("%s: %d groups, %d not casefold-sorted %s"
          % (note, len(by_parent), len(unsorted_before), unsorted_before[:3]))
    return by_parent, unsorted_before


def link_target(path):
    """Catalog links are relative to THIS index file's own directory, not to the series root."""
    return posixpath.relpath(path, RELDIR)


def check_catalog_link_rule(lines):
    """Witness: unquote(target) == relpath(label) must hold for every existing entry."""
    tot = mis = 0
    for l in lines:
        m = re.fullmatch(r"- \[(.+?)\]\((.+?)\)", l)
        if not m:
            continue
        tot += 1
        if urllib.parse.unquote(m.group(2)) != link_target(m.group(1)):
            mis += 1
            if mis <= 3:
                print("  rule violation:", m.group(1), "->", m.group(2))
    print("catalog link rule re-derived from %d standing entries: %d violations" % (tot, mis))
    assert mis == 0, "the catalog's own link convention does not match the rule used here"
    assert tot > 5000, "the parser found too few entries to witness the rule (%d)" % tot
    return tot, mis


CATALOG_RE = re.compile(r"- \[(.+?)\]\((.+?)\)")
ORDER_KEYS = {"identity": lambda s: s, "casefold": str.casefold}


def catalog_labels(lines):
    out = []
    for l in lines:
        m = CATALOG_RE.fullmatch(l)
        if m:
            out.append(m.group(1))
    return out


def ordering_of(labels):
    """Which candidate keys reproduce this group's STANDING order?  Empty list = no rule fits."""
    return [n for n in sorted(ORDER_KEYS) if labels == sorted(labels, key=ORDER_KEYS[n])]


def slot_of(labels, path, key):
    lo, hi = 0, len(labels)
    while lo < hi:
        mid = (lo + hi) // 2
        if key(labels[mid]) < key(path):
            lo = mid + 1
        else:
            hi = mid
    return lo


def place(labels, path, note):
    """Return the slot this path belongs to, and the order keys that admissibly put it there."""
    hits = ordering_of(labels)
    assert hits, "%s: standing order of this %d-entry group matches neither identity nor casefold" % (note, len(labels))
    cands = {n: slot_of(labels, path, ORDER_KEYS[n]) for n in hits}
    assert len(set(cands.values())) == 1, "%s: order keys disagree on the slot for %s -> %s" % (note, path, cands)
    return list(cands.values())[0], hits


def check_group_order_after(labels, admitted, note):
    for pk, keys in sorted(admitted.items()):
        g = [l for l in labels if parent(l) == pk]
        for n in sorted(keys):
            assert g == sorted(g, key=ORDER_KEYS[n]), "%s: %s no longer ordered by %s" % (note, pk, n)
        print("%s after: %d entries in %s still ordered by %s" % (note, len(g), pk, "+".join(sorted(keys))))


def patch_catalog_safe(dry):
    raw = open(CATALOG, "rb").read()
    assert raw.count(b"\r\n") == raw.count(b"\n") == raw.count(b"\r")
    lines = raw.decode("utf-8").split("\r\n")
    check_catalog_link_rule(lines)
    group_sorted_labels(catalog_labels(lines), "catalog before")
    key_of = {}
    for i, l in enumerate(lines):
        m = CATALOG_RE.fullmatch(l)
        if m:
            key_of[i] = m.group(1)
    added = []
    admitted = {}
    for path in NEW:
        if path in key_of.values():
            print("catalog: already registered ->", path)
            continue
        pk = parent(path)
        group = sorted([i for i, k in key_of.items() if parent(k) == pk])
        assert group, "catalog: no standing entry in group %r; this driver does not open a new group" % pk
        slot, hits = place([key_of[i] for i in group], path, "catalog")
        admitted.setdefault(pk, set()).update(hits)
        pos = group[slot] if slot < len(group) else group[-1] + 1
        target = link_target(path)
        # The corpus escapes spaces and parentheses in links but leaves CJK alone (98 of its 5,900 entries do).
        # This driver refuses such a path rather than inventing its own escaping rule.
        assert not any(c in target for c in " ()"), \
            "this driver does not percent-encode: the index escapes spaces/parens, target is %r" % target
        line = "- [%s](%s)" % (path, target)
        assert os.path.exists(os.path.join(IDX, *target.split("/"))), \
            "the link this driver would write does not resolve to a file on disk: %s" % target
        lines.insert(pos, line)
        key_of = {i + (1 if i >= pos else 0): k for i, k in key_of.items()}
        key_of[pos] = path
        added.append((path, pos, line))
        print("catalog: +%s at line %d (slot %d/%d, order key %s)"
              % (path, pos + 1, slot, len(group), "+".join(hits)))
    check_group_order_after(catalog_labels(lines), admitted, "catalog")
    return raw, lines, added


def patch_manifest(dry):
    raw = open(MANIFEST, "rb").read()
    assert raw.count(b"\r\n") == raw.count(b"\n") == raw.count(b"\r")
    text = raw.decode("utf-8")
    entries = [(i, m.start(), m.group(1)) for i, m in enumerate(re.finditer(r'"path": "(.+?)"', text))]
    paths = [k for _, _, k in entries]
    group_sorted_labels(paths, "manifest before")
    admitted = {}
    insertions = []
    for path in NEW:
        if path in paths:
            print("manifest: already registered ->", path)
            continue
        pk = parent(path)
        group = [e for e in entries if parent(e[2]) == pk]
        assert group, "manifest: no standing entry in group %r; this driver does not open a new group" % pk
        slot, hits = place([e[2] for e in group], path, "manifest")
        admitted.setdefault(pk, set()).update(hits)
        if slot < len(group):
            anchor = group[slot][1]                     # insert in front of this entry
        else:
            # appending to the group means inserting in front of the entry that FOLLOWS the group;
            # re-using the group's last entry would land the block one entry too early.
            li = group[-1][0]
            assert li + 1 < len(entries), \
                "manifest: group %r ends the array, this driver cannot append there" % pk
            anchor = entries[li + 1][1]
        # the "path" line sits one line below the "{" that opens the entry: walk back TWO line ends
        line_start = text.rfind("\r\n", 0, anchor) + 2
        bol = text.rfind("\r\n", 0, line_start - 2) + 2
        assert re.match(r'^    \{\r\n      "path": ', text[bol:bol + 30]), \
            "manifest: unexpected entry opening at char %d -> %r" % (bol, text[bol:bol + 30])
        block = ('    {\r\n      "path": "%s",\r\n      "section": "%s"\r\n    },\r\n'
                 % (path, SECTION))
        insertions.append((bol, block, path))
        print("manifest: +%s at char %d (slot %d/%d, order key %s)"
              % (path, bol, slot, len(group), "+".join(hits)))
    for bol, block, path in sorted(insertions, reverse=True):
        text = text[:bol] + block + text[bol:]
    new_paths = [m.group(1) for m in re.finditer(r'"path": "(.+?)"', text)]
    check_group_order_after(new_paths, admitted, "manifest")
    return raw, text.encode("utf-8"), insertions


def verify_roundtrip(orig_raw, new_bytes, inserted_lines):
    """Deleting exactly the inserted lines must rebuild the original bytes -> pure insertion."""
    lines = new_bytes.decode("utf-8").split("\r\n")
    keep = [l for l in lines if l not in inserted_lines]
    rebuilt = "\r\n".join(keep).encode("utf-8")
    assert rebuilt == orig_raw, (
            "not a pure insertion: rebuilt %d chars vs original %d chars"
            % (len(keep), len(orig_raw.decode("utf-8").split("\r\n"))))


def verify_manifest_roundtrip(orig_raw, new_bytes, blocks):
    """Removing each inserted block once must rebuild the original bytes -> pure insertion."""
    text = new_bytes.decode("utf-8")
    for block, path in blocks:
        assert text.count(block) == 1, "block for %s is not unique in the new text" % path
        text = text.replace(block, "", 1)
    assert text.encode("utf-8") == orig_raw, "manifest insertion is not byte-reversible"


def write(path, data):
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def main():
    dry = "--check" in sys.argv
    backups = {}
    for p in (CATALOG, MANIFEST):
        b = open(p, "rb").read()
        # O_EXCL keeps "never overwrite a snapshot", but a PID alone collides across runs of one process
        # (the mutant suite calls main() several times in-process), so the name carries a time stamp too.
        fd = os.open(os.path.join(tempfile.gettempdir(),
                                  "v39_idx_backup_%s_%d_%d.bin"
                                  % (os.path.basename(p), os.getpid(), time.time_ns())),
                     os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        with os.fdopen(fd, "wb") as fh:
            fh.write(b)
        backups[p] = b
    orig_cat, cat_lines, cat_added = patch_catalog_safe(dry)
    cat_ins = [l for _, _, l in cat_added]
    man_orig, man_new, man_added = patch_manifest(dry)
    man_ins = [(b, p) for _, b, p in man_added]
    orig_cat_lines = orig_cat.decode("utf-8").split("\r\n")
    verify_roundtrip(orig_cat, "\r\n".join(cat_lines).encode("utf-8"), cat_ins)
    verify_manifest_roundtrip(man_orig, man_new, man_ins)
    print("catalog: %d lines -> %d (inserted %d); manifest: %d bytes -> %d (inserted %d entries)"
          % (len(orig_cat_lines), len(cat_lines), len(cat_ins),
             len(man_orig), len(man_new), len(man_ins)))
    assert len(cat_lines) == len(orig_cat_lines) + len(cat_ins)
    man_block_bytes = sum(len(b.encode("utf-8")) for _, b, _ in man_added)
    assert len(man_new) == len(man_orig) + man_block_bytes, \
        "manifest grew by %d bytes, not the %d the inserted blocks hold" \
        % (len(man_new) - len(man_orig), man_block_bytes)
    json_probe = man_new.decode("utf-8")
    assert json_probe.count('"path": "') == man_orig.decode("utf-8").count('"path": "') + len(man_ins)
    json.loads(json_probe)                                     # validity proved BEFORE the write
    got_cat = catalog_labels(cat_lines)
    got_man = [m.group(1) for m in re.finditer(r'"path": "(.+?)"', json_probe)]
    for p in NEW:
        assert got_cat.count(p) == 1, "catalog holds %s %d times (want exactly 1)" % (p, got_cat.count(p))
        assert got_man.count(p) == 1, "manifest holds %s %d times (want exactly 1)" % (p, got_man.count(p))
    print("both indexes hold each of the %d new paths exactly once; manifest still parses as JSON" % len(NEW))
    if dry:
        print("CHECK ONLY: nothing written")
        return 0
    try:
        write(CATALOG, "\r\n".join(cat_lines).encode("utf-8"))
        write(MANIFEST, man_new)
        json.loads(open(MANIFEST, "rb").read().decode("utf-8"))     # must stay valid JSON
        for p in (CATALOG, MANIFEST):
            b = open(p, "rb").read()
            assert b.count(b"\r\n") == b.count(b"\n") == b.count(b"\r")
    except Exception as exc:
        for p, b in backups.items():
            write(p, b)
        print("FAILED (%s) -> restored both index files from %s" % (type(exc).__name__), file=sys.stderr)
        raise
    for p in (CATALOG, MANIFEST):
        b = open(p, "rb").read()
        print("WROTE %s: %d bytes / %d CRLF-lines sha256[:16]=%s"
              % (os.path.basename(p), len(b), b.count(b"\r\n"), hashlib.sha256(b).hexdigest()[:16]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
