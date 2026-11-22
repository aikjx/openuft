
# ---------------------------------------------------------------- 判词（机读构造）
def verdict_of(f_l5, f_l6, f_l7):
    """唯一判词构造函数。三个输入任一翻转，判词串必须变化。"""
    if f_l5 and f_l6 and f_l7:
        return ("ROOTV128E-LARGE-LAMBDA-SCAN-VACUITY-PROVEN"
                "--ALPHA-IS-NOT-AN-OBSERVABLE-PARAMETER"
                "--ONLY-BETA-ALPHA-OVER-LAMBDA-SQUARED-IS-CONSTRAINED"
                "--TAIL-FIT-IS-A-RESCALED-BETA-FIT"
                "--EXCLUSION-BAND-EDGES-ARE-TWO-UNRELATED-MECHANISMS"
                "--EQUIVALENCE-PRINCIPLE-CANNOT-SEE-MASS-COUPLED-YUKAWA"
                "--MASS-AMPLITUDE-DEGENERACY-IS-EXACT"
                "--UFT-NOT-BROKEN"
                "--NO-INDEPENDENT-PREDICTION")
    bad = []
    if not f_l5:
        bad.append("TAIL-NOT-SCALING-AS-LAMBDA-SQUARED")
    if not f_l6:
        bad.append("TAIL-POINTS-NOT-COLLAPSED")
    if not f_l7:
        bad.append("BAND-EDGE-DECOMPOSITION-REFUTED")
    return "ROOTV128E-VACUITY-CLAIM-REFUTED--" + "--".join(bad)


def gate_verdict_machine():
    """VERDICT-MACHINE：任一输入翻转，判词串必须变化。"""
    base = verdict_of(True, True, True)
    variants = [verdict_of(False, True, True),
                verdict_of(True, False, True),
                verdict_of(True, True, False)]
    ok = all(v != base for v in variants)
    return {
        "id": "G-VERDICT-MACHINE",
        "kind": "guard",
        "title": "判词机读：三个承重标志任一翻转必须改变判词串",
        "ok": ok,
        "notes": ["基线长度 %d；三个变体长度 %s" % (len(base), [len(v) for v in variants])],
        "readings": {},
    }


def _ok_assigns(fn):
    """收集函数内所有对 ok 的赋值，附带「是否在条件/循环体内」的深度。"""
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


def gate_no_hardcode():
    """AST 守卫：ok 不得「只在函数体顶层赋常量、从不被条件翻转」。"""
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
        top_const = [a for a in asg if a[1] == 0 and isinstance(a[2], ast.Constant)]
        nested = [a for a in asg if a[1] >= 1]
        if top_const and not nested:
            bad.append((node.name, node.lineno))
    ok = not bad
    return {
        "id": "G-NO-HARDCODE-OK",
        "kind": "guard",
        "title": "AST 守卫：ok 不得写死（顶层常量且无任何条件翻转即为装饰判据）",
        "ok": ok,
        "notes": ["扫描 %d 个含 ok 的函数" % scanned,
                  ("命中 %s" % bad) if bad else "零命中"],
        "readings": {"n_functions_scanned": scanned},
    }


def gate_link_check(json_path, rep_path, verdict):
    """链接体检：json 与 report 都必须含判词串与日期。"""
    ok = True
    notes = []
    for p in (json_path, rep_path):
        if not os.path.exists(p):
            ok = False
            notes.append("缺失: %s" % os.path.basename(p))
            continue
        t = open(p, "rb").read().decode("utf-8", "ignore")
        has_v = verdict in t
        has_d = DATE in t
        if not (has_v and has_d):
            ok = False
        notes.append("%s: verdict=%s date=%s" % (os.path.basename(p), has_v, has_d))
    return {
        "id": "G-LINK",
        "kind": "guard",
        "title": "链接体检：JSON 与报告均含判词串与日期",
        "ok": ok,
        "notes": notes,
        "readings": {},
    }


# ---------------------------------------------------------------- 报告渲染
def render_report(gates, verdict, final, up_sha, up_bytes):
    L = []
    add = L.append
    n_ok = sum(1 for g in gates if g["ok"])
    n_tot = len(gates)
    guards = [g["id"] for g in gates if g["kind"] == "guard"]
    identity = [g["id"] for g in gates if g["kind"] == "identity"]
    bearing = [g["id"] for g in gates if g["kind"].startswith("load-bearing")]
    neg = [g["id"] for g in gates if g.get("negative_reading")]

    add("=" * 78)
    add("ROOT V128 第五册 · 大 lambda 扫描空转与整体幅度不可辨识性")
    add("算法联盟可算审计（非判定册）  date : %s" % DATE)
    add("=" * 78)
    add("")
    add("target    : ROOT V128 Yukawa 势 Phi(r) = -(mu/r)(1 + alpha exp(-r/lambda))")
    add("question  : 这个势里哪些参数组合真正可观测")
    add("upstream  : %s" % os.path.basename(upstream_json()))
    add("up_sha256 : %s" % up_sha)
    add("up_bytes  : %d" % up_bytes)
    add("")
    add("-" * 78)
    for g in gates:
        add("[%s] %s  %s" % (g["id"], "OK  " if g["ok"] else "FAIL", g["title"]))
        for n in g.get("notes", []):
            add("       " + n)
        for k, v in (g.get("readings") or {}).items():
            add("       .%-40s = %s" % (k, v))
        for r in (g.get("rows") or [])[:8]:
            add("       | " + "  ".join("%s=%s" % (k, v) for k, v in r.items()))
        add("")
    add("-" * 78)
    add("verdict   : %s" % verdict)
    add("final     : %s" % final)
    add("guards    : %s" % " ".join(guards))
    add("identity  : %s" % (" ".join(identity) if identity else "无"))
    add("bearing   : %s" % " ".join(bearing))
    add("negative  : %s" % " ".join(neg))
    add("n_gate_ok : %d / %d" % (n_ok, n_tot))
    add("")
    add("red_line  : 不宣称攻破统一场论；不产生新物理；独立实验预言 0；")
    add("            第三册读数只继承不重拟合；本册不修正任何既有判词。")
    add("boundary  : 本册判的是「alpha 在大 lambda 端不是可观测参数」，")
    add("            不是「第五力不存在」，也不是「V128 被证伪」。")
    add("            若将来有人在 beta 而非 alpha 上报告约束，本册结论不变。")
    add("=" * 78)
    return "\n".join(L) + "\n"


def build_payload(gates, verdict, final, up_sha, up_bytes):
    return {
        "kind": "algorithm-alliance-audit-recompute",
        "not_a_verdict_volume": True,
        "occupies_rid": False,
        "enters_readme": False,
        "title": "ROOT V128 第五册 大 lambda 扫描空转与整体幅度不可辨识性",
        "date": DATE,
        "target": "Phi(r) = -(mu/r)(1 + alpha exp(-r/lambda))",
        "upstream": {
            "file": os.path.basename(upstream_json()),
            "sha256": up_sha,
            "bytes": up_bytes,
            "relation": "只读继承；不重拟合；不改判词",
        },
        "verdict": verdict,
        "verdict_type": "machine",
        "final": final,
        "n_gate_ok": sum(1 for g in gates if g["ok"]),
        "n_gate_total": len(gates),
        "guards": [g["id"] for g in gates if g["kind"] == "guard"],
        "identity_gates": [g["id"] for g in gates if g["kind"] == "identity"],
        "load_bearing_gates": [g["id"] for g in gates if g["kind"].startswith("load-bearing")],
        "negative_gates": [g["id"] for g in gates if g.get("negative_reading")],
        "gates": gates,
        "discipline": [
            "恒等门（L3）单列不承重",
            "跨册读数只继承不重算，冲突时报负读数不改上游",
            "ok 由读数驱动，AST 守卫禁止常量赋值",
            "判词由唯一构造函数生成，三标志任一翻转必变",
            "回填顺序：占位 -> 回读 -> 再写 -> 守卫 -> FINAL -> 报告",
        ],
        "red_line": [
            "不宣称攻破统一场论",
            "不产生新物理，独立实验预言 0",
            "本册不修正第三册任何判词",
            "「大 lambda 空转」不等于「V128 被证伪」",
        ],
    }


def _write_json(gates, verdict, final, up_sha, up_bytes):
    jp = out_json()
    os.makedirs(os.path.dirname(jp), exist_ok=True)
    body = json.dumps(build_payload(gates, verdict, final, up_sha, up_bytes),
                      ensure_ascii=False, indent=1, sort_keys=False)
    with open(jp, "w", encoding="utf-8") as fh:
        fh.write(body + "\n")
    return jp


def _write_report(gates, verdict, final, up_sha, up_bytes):
    rp = report_path()
    os.makedirs(os.path.dirname(rp), exist_ok=True)
    with open(rp, "w", encoding="utf-8") as fh:
        fh.write(render_report(gates, verdict, final, up_sha, up_bytes))
    return rp


# ---------------------------------------------------------------- 主流程
def main():
    up, up_sha, up_bytes = load_upstream()

    gates = [gate_L1(), gate_L2(), gate_L3(), gate_L4(),
             gate_L5(up, up_sha, up_bytes), gate_L6(up), gate_L7(up), gate_L8(up),
             gate_verdict_machine(), gate_no_hardcode()]

    by_id = {g["id"]: g for g in gates}
    f5, f6, f7 = by_id["L5"]["ok"], by_id["L6"]["ok"], by_id["L7"]["ok"]
    verdict = verdict_of(f5, f6, f7)

    def decide(gs):
        bad = [g["id"] for g in gs if not g["ok"]]
        if bad:
            return "GATES-FAIL--" + "-".join(bad)
        if f5 and f6 and f7:
            return "GATES-PASS-WITH-VACUITY-CONCLUSION"
        return "GATES-PASS-BUT-VACUITY-CONCLUSION-REFUTED"

    final = decide(gates)

    # 回填 A：先落盘占位（让 link 门可读）
    _write_report(gates, verdict, final, up_sha, up_bytes)
    _write_json(gates, verdict, final, up_sha, up_bytes)

    # 守卫：链接体检
    gates.append(gate_link_check(out_json(), report_path(), verdict))
    final = decide(gates)

    # 回填 B：带 link 门再写一次（内容确定，两次跑逐字节相同）
    rp = _write_report(gates, verdict, final, up_sha, up_bytes)
    jp = _write_json(gates, verdict, final, up_sha, up_bytes)

    n_ok = sum(1 for g in gates if g["ok"])
    n_tot = len(gates)
    tag = ".".join(["%s=%s" % (g["id"], g["ok"]) for g in gates])

    sys.stdout.write("verdict   : %s\n" % verdict)
    sys.stdout.write("final     : %s\n" % final)
    sys.stdout.write("n_gate_ok : %d / %d\n" % (n_ok, n_tot))
    sys.stdout.write("gates     : %s\n" % tag)
    sys.stdout.write("report    : %s\n" % rp)
    sys.stdout.write("json      : %s\n" % jp)
    data = open(jp, "rb").read()
    sys.stdout.write("json_bytes: %d\n" % len(data))
    sys.stdout.write("json_sha  : %s\n" % hashlib.sha256(data).hexdigest())
    for g in gates:
        if not g["ok"]:
            sys.stdout.write("FAILED GATE: %s\n" % g["id"])
            for n in g.get("notes", []):
                if n.startswith("FAIL"):
                    sys.stdout.write("    " + n + "\n")
    return 0 if n_ok == n_tot else 1


if __name__ == "__main__":
    sys.exit(main())
