
# ------------------------------------------------------------------ 判词
def verdict_of(n2, n5, n6):
    if n2 and n5 and n6:
        return ("ROOTV128F-LAMBDA-UNIDENTIFIABLE-AT-NULL"
                "--FISHER-LAMBDA-COLUMN-IS-EXACTLY-ZERO"
                "--CRAMER-RAO-BOUND-DIVERGES"
                "--SIGMA-LAMBDA-SCALES-AS-ONE-OVER-BETA"
                "--ALPHA-AND-BETA-FITS-ARE-EXACT-RESCALE"
                "--CHI2-PEAK-IS-NOISE-NOT-A-LAMBDA-MEASUREMENT"
                "--INJECTION-RECOVERY-SHOWS-ONLY-NONZERO-BETA-GIVES-LAMBDA"
                "--UFT-NOT-BROKEN"
                "--NO-INDEPENDENT-PREDICTION")
    bad = []
    if not n2:
        bad.append("NULL-COLUMN-NOT-ZERO")
    if not n5:
        bad.append("CHI2-PEAK-MISMATCH")
    if not n6:
        bad.append("SIGMA-LAMBDA-SCALING-REFUTED")
    return "ROOTV128F-CLAIM-REFUTED--" + "--".join(bad)


def _ok_assigns(fn):
    out = []

    def walk(node, depth):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "ok" for t in ch.targets):
                out.append((ch, depth, ch.value))
            walk(ch, depth + (1 if isinstance(ch, (ast.If, ast.For, ast.While, ast.Try))
                              else 0))
    walk(fn, 0)
    return out


def gate_verdict_machine():
    base = verdict_of(True, True, True)
    vs = [verdict_of(False, True, True), verdict_of(True, False, True),
          verdict_of(True, True, False)]
    ok = all(v != base for v in vs)
    return {"id": "G-VERDICT-MACHINE", "kind": "guard", "ok": ok,
            "title": "判词机读：三个承重标志任一翻转必改判词串",
            "notes": ["基线 %d 字符；变体 %s" % (len(base), [len(v) for v in vs])],
            "readings": {}}


def gate_no_hardcode():
    src = open(os.path.abspath(__file__), "rb").read().decode("utf-8")
    tree = ast.parse(src)
    bad = []
    scanned = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        asg = _ok_assigns(node)
        if not asg:
            continue
        scanned += 1
        top = [a for a in asg if a[1] == 0 and isinstance(a[2], ast.Constant)]
        nested = [a for a in asg if a[1] >= 1]
        if top and not nested:
            bad.append((node.name, node.lineno))
    return {"id": "G-NO-HARDCODE-OK", "kind": "guard", "ok": not bad,
            "title": "AST 守卫：ok 不得顶层赋常量且无条件翻转",
            "notes": ["扫描 %d 个函数" % scanned, str(bad) if bad else "零命中"],
            "readings": {"n_functions_scanned": scanned}}


def gate_link(jp, rp, verdict):
    ok = True
    notes = []
    for p in (jp, rp):
        if not os.path.exists(p):
            ok = False
            notes.append("缺失 %s" % os.path.basename(p))
            continue
        t = open(p, "rb").read().decode("utf-8", "ignore")
        v, d = verdict in t, DATE in t
        ok = ok and v and d
        notes.append("%s: verdict=%s date=%s" % (os.path.basename(p), v, d))
    return {"id": "G-LINK", "kind": "guard", "ok": ok,
            "title": "链接体检：JSON 与报告均含判词串与日期",
            "notes": notes, "readings": {}}


def render_report(gates, verdict, final, sha, nbytes):
    L = []
    add = L.append
    add("=" * 78)
    add("ROOT V128 第六册 · beta 参数化 Fisher 重拟合与零假设处 lambda 不可辨识性")
    add("算法联盟可算审计（非判定册）  date : %s" % DATE)
    add("=" * 78)
    add("")
    add("target    : Phi(r) = -(mu/r)(1 + alpha exp(-r/lambda))")
    add("question  : 在零假设 beta = 0 处，lambda 本身可辨识吗")
    add("upstream  : %s" % os.path.basename(upstream_json()))
    add("up_sha256 : %s" % sha)
    add("up_bytes  : %d" % nbytes)
    add("")
    add("-" * 78)
    for g in gates:
        add("[%s] %s  %s" % (g["id"], "OK  " if g["ok"] else "FAIL", g["title"]))
        for n in g.get("notes", []):
            add("       " + n)
        for k, v in (g.get("readings") or {}).items():
            add("       .%-40s = %s" % (k, v))
        for r in (g.get("rows") or [])[:8]:
            add("       | " + "  ".join("%s=%s" % (kv, vv) for kv, vv in r.items()))
        add("")
    add("-" * 78)
    add("verdict   : %s" % verdict)
    add("final     : %s" % final)
    add("guards    : %s" % " ".join(g["id"] for g in gates if g["kind"] == "guard"))
    add("identity  : %s" % (" ".join(g["id"] for g in gates if g["kind"] == "identity") or "无"))
    add("bearing   : %s" % " ".join(g["id"] for g in gates
                                    if g["kind"].startswith("load-bearing")))
    add("n_gate_ok : %d / %d" % (sum(1 for g in gates if g["ok"]), len(gates)))
    add("")
    add("red_line  : 不宣称攻破统一场论；不产生新物理；独立实验预言 0；")
    add("            核与观测表与第三册同源，不算独立证据；不改任何既有判词。")
    add("boundary  : 判的是「beta=0 处 lambda 不可辨识」，不是「V128 被证伪」，")
    add("            也不是「任何 Yukawa 模型的 lambda 都不可测」。")
    add("            注入非零 beta 后 lambda 恢复（N7），边界清楚。")
    add("=" * 78)
    return "\n".join(L) + "\n"


def build_payload(gates, verdict, final, sha, nbytes):
    return {
        "kind": "algorithm-alliance-audit-recompute",
        "not_a_verdict_volume": True,
        "occupies_rid": False,
        "enters_readme": False,
        "title": "ROOT V128 第六册 beta 参数化 Fisher 重拟合与 lambda 不可辨识性",
        "date": DATE,
        "target": "Phi(r) = -(mu/r)(1 + alpha exp(-r/lambda))",
        "upstream": {"file": os.path.basename(upstream_json()), "sha256": sha,
                     "bytes": nbytes,
                     "relation": "核闭式与观测表同源；只做结构分析，不算独立证据"},
        "verdict": verdict,
        "verdict_type": "machine",
        "final": final,
        "n_gate_ok": sum(1 for g in gates if g["ok"]),
        "n_gate_total": len(gates),
        "guards": [g["id"] for g in gates if g["kind"] == "guard"],
        "identity_gates": [g["id"] for g in gates if g["kind"] == "identity"],
        "load_bearing_gates": [g["id"] for g in gates
                               if g["kind"].startswith("load-bearing")],
        "gates": gates,
        "discipline": [
            "恒等门 N4 单列不承重",
            "同源核与观测表只做结构判据，不计独立证据",
            "判据依赖导数正确计算，必须由 N1 的两种步长互验守门（N8 反噬）",
            "判词由唯一构造函数生成，三个承重标志任一翻转必变",
        ],
        "red_line": [
            "不宣称攻破统一场论",
            "不产生新物理，独立实验预言 0",
            "不改第三册与第五册任何判词",
            "lambda 在零假设不可辨识 != Yukawa 模型被证伪",
        ],
    }


def write_json(gates, verdict, final, sha, nbytes):
    p = out_json()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(build_payload(gates, verdict, final, sha, nbytes),
                            ensure_ascii=False, indent=1, sort_keys=False) + "\n")
    return p


def write_report(gates, verdict, final, sha, nbytes):
    p = report_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(render_report(gates, verdict, final, sha, nbytes))
    return p


def main():
    U, sha, nbytes = load_upstream()
    gates = [gate_N1(), gate_N2(), gate_N3(), gate_N4(), gate_N5(),
             gate_N6(), gate_N7(), gate_N8(),
             gate_verdict_machine(), gate_no_hardcode()]
    b = {g["id"]: g["ok"] for g in gates}
    verdict = verdict_of(b["N2"], b["N5"], b["N6"])

    def decide(gs):
        bad = [g["id"] for g in gs if not g["ok"]]
        if bad:
            return "GATES-FAIL--" + "-".join(bad)
        if b["N2"] and b["N5"] and b["N6"]:
            return "GATES-PASS-WITH-UNIDENTIFIABILITY-CONCLUSION"
        return "GATES-PASS-BUT-CONCLUSION-REFUTED"

    final = decide(gates)
    write_report(gates, verdict, final, sha, nbytes)
    write_json(gates, verdict, final, sha, nbytes)
    gates.append(gate_link(out_json(), report_path(), verdict))
    final = decide(gates)
    rp = write_report(gates, verdict, final, sha, nbytes)
    jp = write_json(gates, verdict, final, sha, nbytes)

    n_ok = sum(1 for g in gates if g["ok"])
    sys.stdout.write("verdict   : %s\n" % verdict)
    sys.stdout.write("final     : %s\n" % final)
    sys.stdout.write("n_gate_ok : %d / %d\n" % (n_ok, len(gates)))
    sys.stdout.write("gates     : %s\n" % ".".join("%s=%s" % (g["id"], g["ok"]) for g in gates))
    sys.stdout.write("report    : %s\n" % rp)
    sys.stdout.write("json      : %s\n" % jp)
    raw = open(jp, "rb").read()
    sys.stdout.write("json_bytes: %d\n" % len(raw))
    sys.stdout.write("json_sha  : %s\n" % hashlib.sha256(raw).hexdigest())
    for g in gates:
        if not g["ok"]:
            sys.stdout.write("FAILED GATE: %s\n" % g["id"])
            for n in g.get("notes", []):
                if n.startswith("FAIL"):
                    sys.stdout.write("    " + n + "\n")
    return 0 if n_ok == len(gates) else 1


if __name__ == "__main__":
    sys.exit(main())
