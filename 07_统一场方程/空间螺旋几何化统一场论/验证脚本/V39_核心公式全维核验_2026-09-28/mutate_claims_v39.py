# -*- coding: utf-8 -*-
"""Mutants for append_claims_v39.py: each must redden the gate it is aimed at, in --check mode only."""
import importlib.util, io, os, sys, contextlib

DRIVER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "append_claims_v39.py")
spec = importlib.util.spec_from_file_location("ac", DRIVER)


def run(rows, argv):
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if rows is not None:
        m.ROWS = rows
    old = sys.argv
    sys.argv = ["x"] + argv
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            m.main()
        return 0, buf.getvalue()
    except AssertionError as exc:
        return 3, buf.getvalue() + "ASSERT: %s\n" % exc
    finally:
        sys.argv = old


def main():
    # M0: the lander's own output is now the disk state, so a re-run must be a statement-level no-op
    rc, out = run(None, ["--check"])
    skipped = [l for l in out.splitlines() if "already appended" in l]
    print("M0 idempotence guard on the three landed statements: rc=%d, %d rows skipped" % (rc, len(skipped)))
    for l in skipped:
        print("   ", l.strip())
    assert rc == 0 and len(skipped) == 3, "the landed rows are not recognised as already appended"

    mut = [("θ 符号复用（N1）读数面 V3_9_core_formula_checks.json 的 checks.N1_theta_conflation 差 -3.6958011e-8",
            "元审计", "falsified")]
    rc, out = run(mut, ["--check"])
    print("M1 last digit of a cited reading changed: rc=%d" % rc)
    print("   ", [l for l in out.splitlines() if "UNATTACHED" in l])
    assert rc == 3 and "UNATTACHED ['-3.6958011e-8']" in out

    mut = [("读数见 checks.N1_theta_conflation_x 与 checks.N6_prime_anchor", "元审计", "falsified")]
    rc, out = run(mut, ["--check"])
    print("M2 invented check key: rc=%d" % rc)
    print("   ", [l for l in out.splitlines() if "not present in the face" in l])
    assert rc == 3 and "['N1_theta_conflation_x']" in out

    mut = [("一句话，里面用了半角逗号, 来拆列", "元审计", "falsified")]
    rc, out = run(mut, ["--check"])
    print("M3 ASCII comma inside a cell: rc=%d" % rc)
    print("   ", [l for l in out.splitlines() if "ASCII comma" in l][:1])
    assert rc == 3 and "ASCII comma" in out

    mut = [("差 3.6958011e-9 但文档印的是 -3.6958011e-9", "元审计", "falsified")]
    rc, out = run(mut, ["--check"])
    print("M4 sign dropped from a cited reading: rc=%d (both tokens are on the face, so 0 is the honest answer)" % rc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
