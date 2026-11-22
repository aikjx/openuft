
# ------------------------------------------------------------------ 判词
def verdict_of(f2, f3, f5):
    if f2 and f3 and f5:
        return ("ROOTV128G-OBSERVABLE-SWAP-DOES-NOT-RESCUE-LAMBDA"
                "--ALL-POTENTIAL-FUNCTIONALS-HAVE-ZERO-LAMBDA-DERIVATIVE-AT-BETA-ZERO"
                "--NOT-A-LINEARITY-ISSUE-NONLINEAR-FUNCTIONALS-ALSO-DEGENERATE"
                "--CLAIM-S-FROM-OWN-PRIOR-VOLUMES-REFUTED"
                "--SWAPPING-OBSERVABLE-IMPROVES-BETA-PRECISION-ONLY"
                "--NONZERO-BETA-RESTORES-LAMBDA-INFORMATION"
                "--UFT-NOT-BROKEN"
                "--NO-INDEPENDENT-PREDICTION")
    bad = []
    if not f2:
        bad.append("LINEAR-FUNCTIONALS-NOT-DEGENERATE")
    if not f3:
        bad.append("NONLINEAR-FUNCTIONAL-DEGENERACY-REFUTED")
    if not f5:
        bad.append("CLAIM-S-NOT-REFUTED")
    return "ROOTV128G-CLAIM-REFUTED--" + "--".join(bad)


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


def render_report(gates, verdict, final, ups):
    L = []
    add = L.append
    add("=" * 78)
    add("ROOT V128 第七册 · 「换观测量」出路的可算自审")
    add("算法联盟可算审计（非判定册）  date : %s" % DATE)
    add("=" * 78)
    add("")
    add("claim_S : 换观测量可在 beta=0 处测出 lambda（本链前册留下的出路）")
    for tag, (data, sha, nb) in ups.items():
        add("upstream_%s : %s / %s / %d B" % (tag, data.get("verdict", "")[:40], sha[:16], nb))
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
    add("bearing   : %s" % " ".join(g["id"] for g in gates
                                    if g["kind"].startswith("load-bearing")))
    add("n_gate_ok : %d / %d" % (sum(1 for g in gates if g["ok"]), len(gates)))
    add("")
    add("red_line  : 不宣称攻破统一场论；不产生新物理；独立实验预言 0；")
    add("            本册判的是本链自己的命题 S，不引入任何外部读数。")
    add("boundary  : beta=0 处所有势泛函对 lambda 零导数；beta!=0 时恢复（P4）。")
    add("            不证明第五力不存在，不证明 Yukawa 的 lambda 永远不可测。")
    add("=" * 78)
    return "\n".join(L) + "\n"


def build_payload(gates, verdict, final, ups):
    return {
        "kind": "algorithm-alliance-audit-recompute",
        "not_a_verdict_volume": True,
        "occupies_rid": False,
        "enters_readme": False,
        "title": "ROOT V128 第七册 换观测量出路的可算自审",
        "date": DATE,
        "claim_under_test": "换观测量可在 beta=0 处测出 lambda（本链前册留下的出路）",
        "upstream": {tag: {"verdict": data.get("verdict", ""),
                           "sha256": sha, "bytes": nb}
                     for tag, (data, sha, nb) in ups.items()},
        "verdict": verdict,
        "verdict_type": "machine",
        "final": final,
        "n_gate_ok": sum(1 for g in gates if g["ok"]),
        "n_gate_total": len(gates),
        "guards": [g["id"] for g in gates if g["kind"] == "guard"],
        "load_bearing_gates": [g["id"] for g in gates
                               if g["kind"].startswith("load-bearing")],
        "gates": gates,
        "discipline": [
            "判据必反噬自己：本册判的是本链前册留下的命题 S",
            "结论与泛函线性性无关（P3 用 Phi^2 反证）",
            "必须给边界：非零 beta 时 lambda 恢复可测（P4）",
            "设计研究（P6 的 1e-9 相对精度）不得冒充观测约束",
            "判词由唯一构造函数生成，三个承重标志任一翻转必变",
        ],
        "red_line": [
            "不宣称攻破统一场论",
            "不产生新物理，独立实验预言 0",
            "不引入外部读数，不修改任何上游判词",
            "不可辨识 != 模型被证伪",
        ],
    }


def write_json(gates, verdict, final, ups):
    p = out_json()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(build_payload(gates, verdict, final, ups),
                            ensure_ascii=False, indent=1, sort_keys=False) + "\n")
    return p


def write_report(gates, verdict, final, ups):
    p = report_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(render_report(gates, verdict, final, ups))
    return p


def main():
    U = load_upstream()
    flags = {}
    gates = [gate_P1()]
    for gid, fn in (("P2", gate_P2), ("P3", gate_P3), ("P4", gate_P4),
                    ("P6", gate_P6), ("P7", gate_P7), ("P8", lambda: gate_P8(U))):
        g = fn()
        flags[gid] = g["ok"]
        gates.append(g)
    gates.append(gate_P5(flags))
    flags["P5"] = gates[-1]["ok"]
    gates.append(gate_verdict_machine())
    gates.append(gate_no_hardcode())

    verdict = verdict_of(flags["P2"], flags["P3"], flags["P5"])

    def decide(gs):
        bad = [g["id"] for g in gs if not g["ok"]]
        if bad:
            return "GATES-FAIL--" + "-".join(bad)
        if flags["P2"] and flags["P3"] and flags["P5"]:
            return "GATES-PASS-WITH-CLAIM-REFUTED"
        return "GATES-PASS-BUT-CLAIM-NOT-REFUTED"

    final = decide(gates)
    write_report(gates, verdict, final, U)
    write_json(gates, verdict, final, U)
    gates.append(gate_link(out_json(), report_path(), verdict))
    final = decide(gates)
    rp = write_report(gates, verdict, final, U)
    jp = write_json(gates, verdict, final, U)

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
