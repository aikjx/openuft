import ast, io, os
ROOT = r'D:\a10\aikjx\code\my_lib\utf'
PAIR = {'predicted': 'observed', 'derived': 'reference', 'theory': 'experiment'}
TOL = ('tolerance', 'tolerance_pct', 'tol', 'rtol', 'atol')
selfcmp, broken_tol, fp, nb, tot = [], [], 0, 0, 0
for dirpath, dirs, fs in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', '.history')]
    for f in fs:
        if not f.endswith('.py'):
            continue
        p = os.path.join(dirpath, f)
        text = io.open(p, encoding='utf-8', errors='replace').read()
        lines = text.splitlines()
        try:
            tree = ast.parse(text); fp += 1
        except SyntaxError:
            nb += 1; continue
        sigs = {}
        for n in ast.walk(tree):
            if isinstance(n, ast.FunctionDef) and n.name in ('check', 'verify', 'check_eq'):
                sigs[n.name] = [a.arg for a in n.args.args]
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            fn = getattr(node.func, 'id', None) or getattr(node.func, 'attr', '')
            if fn not in sigs:
                continue
            names = sigs[fn]
            if len(node.args) > len(names):
                continue
            kw = {k.arg: k.value for k in node.keywords}
            pos = dict(zip(names, node.args))
            get = lambda nm: kw.get(nm, pos.get(nm))
            tot += 1
            rel = os.path.relpath(p, ROOT)
            src = lines[node.lineno-1].strip()[:88] if node.lineno <= len(lines) else '?'
            for a, b in PAIR.items():
                A, B = get(a), get(b)
                if A is None or B is None:
                    continue
                if ast.dump(A) == ast.dump(B):
                    try:
                        val = repr(ast.literal_eval(A))
                    except Exception:
                        val = '<同一表达式，两侧同值>'
                    selfcmp.append('%s:%d  %s≡%s=%s' % (rel, node.lineno, a, b, val))
                    break
                ref, tol = B, None
                for t in TOL:
                    if get(t) is not None:
                        tol = get(t); break
                if isinstance(ref, ast.Constant) and ref.value == 0 and \
                   isinstance(tol, ast.Constant) and tol.value == 0:
                    broken_tol.append('%s:%d  参照=0 且容差=0 ⇒ |derived|<0 永假' % (rel, node.lineno))
                break
print('解析成功 %d 份 .py（语法错误 %d 份＝其条款不产生任何证据）｜按本文件签名绑定到实参名的调用 %d 条' % (fp, nb, tot))
print('A 类｜预测与实测两侧写成同一个量 ⇒ 恒 PASS：%d 条' % len(selfcmp))
for x in selfcmp:
    print('  ' + x)
print('B 类｜参照=0 且容差=0 ⇒ 恒 FAIL（写坏的条款）：%d 条' % len(broken_tol))
for x in broken_tol:
    print('  ' + x)
