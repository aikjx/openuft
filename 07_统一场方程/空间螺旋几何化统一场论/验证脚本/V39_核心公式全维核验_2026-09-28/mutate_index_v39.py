# -*- coding: utf-8 -*-
"""Mutants for register_v39_index_entries.py: each must redden the gate it aims at, in --check mode only.

The driver short-circuits paths that are already registered, so once this round's artifacts are in the index a
mutant would exit 0 for the wrong reason.  This suite therefore PLANTS its own probe file (PROBE, created on
disk so the "link resolves" gate is honest, deleted in a finally) and runs every mutant in --check mode, which
writes nothing.  T4 adds a spaced name as well: that is the shape the index escapes and this driver must refuse.
"""
import contextlib
import importlib.util
import io
import os
import posixpath
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location("reg", os.path.join(HERE, "register_v39_index_entries.py"))
SERIES_DIR = os.path.dirname(os.path.dirname(HERE))
PROBE = "07_统一场方程/空间螺旋几何化统一场论/V39_mutant_probe.md"
SPACED = "07_统一场方程/空间螺旋几何化统一场论/V3 9 spaced fixture.md"


def load():
    m = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(m)
    return m


def check(m, extra_new=()):
    m.NEW = list(m.NEW) + [PROBE] + list(extra_new)
    old = sys.argv
    sys.argv = ["x", "--check"]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = m.main()
        return rc, buf.getvalue()
    except AssertionError as exc:
        return 3, buf.getvalue() + "ASSERT: %s\n" % exc
    except Exception as exc:                       # a crash is NOT a caught mutant: name it, don't hide it
        return 9, buf.getvalue() + "CRASH %s: %s\n" % (type(exc).__name__, exc)
    finally:
        sys.argv = old


def run_all():
    m0 = load()
    rc, out = check(m0)
    pending = [l for l in out.splitlines() if l.startswith("catalog: +") or l.startswith("manifest: +")]
    already = len({l.split("-> ")[1] for l in out.splitlines() if "already registered" in l})
    print("T0 baseline --check: rc=%d; %d of the %d paths already registered -> %d pending insertion lines"
          % (rc, already, len(m0.NEW), len(pending)))
    assert rc == 0 and "CHECK ONLY" in out
    # check() appends the planted probe onto m0.NEW before running, so len(m0.NEW) here already counts it
    assert len(pending) == 2 * (len(m0.NEW) - already), "the driver is not inserting each unregistered path twice"
    assert any(PROBE.split("/")[-1] in l for l in pending), "the planted probe is not among the pending insertions"

    # T1 has to be aimed at the 95-entry series group: the pending paths (the probe and this round's scripts)
    # all live in groups of 1-3 entries, which are ordered the same way under both keys, so a corpus-level
    # run idles at rc=0 without ever reaching the ordering gate.  Probe place() directly, with a control.
    labels = load().catalog_labels(open(load().CATALOG, "rb").read().decode("utf-8").split("\r\n"))
    series_group = [l for l in labels if m0.parent(l) == m0.SERIES]
    probe = m0.SERIES + "/zzz_ordering_probe.md"
    slot_ref, hits_ref = m0.place(series_group, probe, "T1-control")
    print("T1 control (unmutated keys): slot %d/%d admitted by %s" % (slot_ref, len(series_group), hits_ref))
    assert hits_ref == ["casefold"], "the series group does not discriminate the two order keys: %s" % hits_ref

    m1 = load()
    m1.ORDER_KEYS = {"identity": lambda s: s}          # drop the convention the file actually uses
    caught = None
    try:
        m1.place(series_group, probe, "T1")
    except AssertionError as exc:
        caught = str(exc)
    print("T1 order key forced to identity: %s" % (caught[:100] if caught else "NOT CAUGHT"))
    assert caught and "matches neither" in caught, "identity-only ordering was not caught"

    m2 = load()
    m2.link_target = lambda p: posixpath.relpath(p, "")     # forget that links are relative to the index dir
    rc, out = check(m2)
    line = [l for l in out.splitlines() if "violations" in l]
    print("T2 naive link prefix: rc=%d" % rc)
    print("   ", line[-1:])
    assert rc == 3 and line and not line[-1].endswith(": 0 violations"), \
        "the naive prefix was not caught by the link-rule witness"

    m3 = load()
    src = open(os.path.join(HERE, "register_v39_index_entries.py"), encoding="utf-8").read()
    mutated = src.replace('        bol = text.rfind("\\r\\n", 0, line_start - 2) + 2', "        bol = line_start")
    assert mutated != src, "the walk-back anchor moved; T3 would be a silent no-op"
    m3 = types.ModuleType("reg3")
    m3.__dict__["__file__"] = os.path.join(HERE, "register_v39_index_entries.py")
    m3.__dict__["__name__"] = "reg3_mutant"
    exec(compile(mutated, "reg3_mutant", "exec"), m3.__dict__)
    rc, out = check(m3)
    line = [l for l in out.splitlines() if "unexpected entry opening" in l]
    print("T3 manifest block written one line too low: rc=%d" % rc)
    print("   ", [l[:110] for l in line[:1]])
    assert rc == 3 and line, "a block landing between { and \"path\" was not caught"

    # T4: the corpus already holds 98 percent-escaped links, so a spaced path must be REFUSED rather than
    # written unescaped.  The escape guard runs BEFORE the "link resolves" check, so no fixture file is needed.
    m4 = load()
    rc, out = check(m4, extra_new=[SPACED])
    line = [l for l in out.splitlines() if "percent-encode" in l or "does not resolve" in l]
    print("T4 a spaced path (must be refused, not silently written unescaped): rc=%d" % rc)
    print("   ", [l[:110] for l in line[:1]])
    assert rc == 3 and line and "percent-encode" in line[0],         "the spaced path did not reach the escape guard (%s)" % (line[:1] or out.splitlines()[-1:])
    print("ALL 4 MUTANTS REDDENED THEIR OWN CHANNEL")
    return 0


def main():
    probe_abs = os.path.join(SERIES_DIR, os.path.basename(PROBE))
    assert not os.path.exists(probe_abs), "a stray probe is already on disk: %s" % probe_abs
    open(probe_abs, "w", encoding="utf-8").write("mutant probe for the index driver" + chr(10))
    try:
        return run_all()
    finally:
        os.remove(probe_abs)
        assert not os.path.exists(probe_abs), "the probe was not cleaned up"



if __name__ == "__main__":
    sys.exit(main())
