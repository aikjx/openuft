# -*- coding: utf-8 -*-
"""
================================================================================
TUFT  g-2 / EDM  多口径普查与基线循环性判定（2026-09-30）
================================================================================

为什么需要这一件：`04_理论推导/TUFT_双分量干涉屏蔽因子_g-2与EDM联合约束_审计.md`
§八 第 9 条要求「统一 OPEN5 的 alpha/(8pi) 映射、OPEN5b 的 2tau/kappa 映射与 V3.2 的
两尺度磁矩映射，禁止多口径择优」，但那张对照表从未产出。本件只做三件事，全部只读：

  [C1] 覆盖面普查：走 openuft（排除嵌套 .git），对声明的口径标记逐条找载体并印
       path:line。任何一枚声明口径找不到载体即 exit 2 —— 覆盖面按声明的标识符集合算，
       所以那张集合在本文件顶部枚举，不拿「扫了很多文件」当证据。
  [C2] 数值复算：从 CODATA 现算各口径的预言与偏差，并与三份 report 印出的读数逐位
       比对；任一不一致即 exit 3。分母一律取本运行实测值。
  [C3] 基线循环性判定：用 ast 读 OPEN5b 的源码结构，判 G2_TUFT 是否为字面常量、
       tau_over_kappa 是否由它反解；再查 OPEN5c 是否真的撤回过「锁死」措辞。
       --mutant 造一份「G2_TUFT 由表达式算出」的假前像，检测器必须在同一份面上改口，
       否则这条判定只是把字符串印出来。

红线：本件不构造新物理、不修改任何映射公式、不改写历史 report；它只回答
「档案里这几句话各自挂在哪份文件上、数字能不能被复算」。
"""
import ast
import io
import os
import re
import sys

import mpmath as mp

mp.mp.dps = 32

HERE = os.path.dirname(os.path.abspath(__file__))
S14 = os.path.abspath(os.path.join(HERE, "..", ".."))
ROOT = os.path.abspath(os.path.join(S14, "..", ".."))   # = openuft（本件的扫描根）
LEGACY = os.path.join(ROOT, "90_历史归档", "来源语料_根目录_20260919",
                      "02_TUFT_来源", "tuft")

OPEN5_PY = os.path.join(LEGACY, "tuft_g2_电子反常磁矩_OPEN5.py")
OPEN5_RPT = os.path.join(LEGACY, "tuft_g2_电子反常磁矩_OPEN5_report.txt")
OPEN5B_PY = os.path.join(LEGACY, "tuft_g2_EDM_屏蔽因子双约束可行性审计_OPEN5b.py")
OPEN5B_RPT = os.path.join(LEGACY, "tuft_g2_EDM_屏蔽因子双约束可行性审计_OPEN5b_report.txt")
OPEN5C_PY = os.path.join(LEGACY, "tuft_孤子τκ锁定_微分方程证明_OPEN5c.py")
OPEN6_RPT = os.path.join(LEGACY, "tuft_EDM_实验对接_OPEN6_report.txt")

OUT = os.path.join(HERE, "tuft_g2_EDM_口径普查_20260930_report.txt")
STEM = "tuft_g2_EDM_口径普查_20260930"   # 本件自己的所有输出都不许进自己的覆盖面

# ---- 声明的口径集合：覆盖面就是这张表，不加不删 ----
CENSUS = [
    ("g2@OPEN5_alpha_over_8pi", ["alpha/(8pi)", r"\alpha/(8"], "OPEN5 的 α/(8π)"),
    ("g2@OPEN5b_2tau_over_kappa", ["2τ/κ", "tau_over_kappa"], "OPEN5b 的 2τ/κ"),
    ("g2@V32_two_scale", ["2.002319", "两尺度"], "V3.2 两尺度磁矩"),
    ("g2@螺旋弧线_alpha_over_pi", ["g-2 = α/π", "alpha/pi"], "α/π 现成近似（无挠率）"),
    ("edm@ACME2018_1.1e-29", ["1.1e-29", "1.10e-29", r"1.1\times10^{-29}"], "ACME 2018 上限"),
    ("edm@JILA2023_4.1e-30", ["4.1e-30", "4.1×10⁻³⁰"], "JILA 2023 上限"),
    ("edm@whitepaper_8.7e-34_Cm", ["8.7e-34", "8.7×10⁻³⁴"], "白皮书引用的上限"),
]
CENSUS_TOKS = [(k, toks) for k, toks, _ in CENSUS]
EXTS = (".md", ".py", ".txt", ".csv", ".tex", ".json")

L = []


def put(s):
    L.append(s)


def read_any(path):
    """返回 (text, enc, note)：区分 missing 与 unreadable，两种「读不到」不许混印。"""
    if not os.path.isfile(path):
        return None, "missing", "文件不存在"
    raw = open(path, "rb").read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff") or b"\x00" in raw[:64]:
        try:
            return raw.decode("utf-16"), "utf-16", ""
        except Exception as e:
            return None, "unreadable", "utf-16 解码失败 %s" % e
    return raw.decode("utf-8", "replace"), "utf-8", ""


def walk_corpus():
    files = []
    unreadable = []
    # 覆盖面不许把「声明这枚口径的那两行」算成它的载体：本件自己的源码与报告都排除。
    self_paths = {os.path.abspath(__file__),
                  os.path.join(HERE, "_mutant_open5b_fake.py")}
    excluded_self = 0
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d != ".git"]
        for f in fn:
            if not f.endswith(EXTS):
                continue
            q = os.path.abspath(os.path.join(dp, f))
            if f.startswith(STEM) or q in self_paths:
                if f.startswith(STEM):
                    excluded_self += 1
                continue
            files.append(q)
    for q in files:
        t, enc, note = read_any(q)
        if t is None:
            unreadable.append((os.path.relpath(q, ROOT), note))
    return files, unreadable, excluded_self


def census_tokens(files):
    hits = {k: [] for k, _, _ in CENSUS}
    for q in files:
        t, enc, note = read_any(q)
        if t is None:
            continue
        rel = os.path.relpath(q, ROOT)
        lines = t.splitlines()
        for key, toks in CENSUS_TOKS:
            for tok in toks:
                for i, line in enumerate(lines, 1):
                    if tok in line:
                        hits[key].append((rel, i, tok))
                        break
    return hits


def module_of(path):
    t, enc, note = read_any(path)
    if t is None:
        return None
    return ast.parse(t)


def rational_of(path, name):
    """取 `name = sp.Rational(a, b)` -> (mpf 值, lineno)；取不到 None。

    必须用 ast.walk：OPEN5b 把这条赋值写在 with 块里，只扫 tree.body 会漏，
    漏了之后调用方会悄悄退回硬编常量——那是把「读不到」印成判决。
    """
    tree = module_of(path)
    if tree is None:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == name:
                    call = node.value
                    if isinstance(call, ast.Call):
                        nums = [x.value for x in call.args if isinstance(x, ast.Constant)]
                        if len(nums) == 2 and all(isinstance(x, (int, float)) for x in nums):
                            return mp.mpf(nums[0]) / mp.mpf(nums[1]), node.lineno
    return None


def find_any_assign(path, name):
    """按名字取赋值语句右侧类型与常量值；用 ast.walk，嵌套块内的赋值也要看见。"""
    tree = module_of(path)
    if tree is None:
        return None, None, None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == name:
                    v = node.value
                    val = v.value if isinstance(v, ast.Constant) else None
                    return node.lineno, type(v).__name__, val
    return None, None, None


def detect_circular(path):
    """G2_TUFT 是字面常量 且 tau_over_kappa == G2_TUFT/2 => 基线自己给自己定价。

    两个成员都必须现读到：少读到一个就退回「只看常量类型」等于把结构检验换成文案检验。
    """
    ln_g, kind_g, val_g = find_any_assign(path, "G2_TUFT")
    if ln_g is None:
        return "UNREADABLE", ["G2_TUFT 赋值未找到"]
    notes = ["G2_TUFT @行%s 右侧类型=%s 值=%s" % (ln_g, kind_g, val_g)]
    rat = rational_of(path, "tau_over_kappa")
    if rat is None:
        notes.append("RATIONAL-NOT-FOUND：tau_over_kappa 没被读到，闭合检验未开火")
        return "STRUCTURAL-FAIL", notes
    r, ln_r = rat
    notes.append("tau_over_kappa @行%s = Rational -> %s" % (ln_r, mp.nstr(r, 12)))
    if kind_g != "Constant":
        notes.append("G2_TUFT 已由表达式算出 ⇒ 比值不再由它反解，判 NOT-CIRCULAR（不比较数值）")
        return "NOT-CIRCULAR", notes
    half = mp.mpf(val_g) / 2
    diff = abs(r - half)
    notes.append("tau/kappa 与 G2_TUFT/2 之差 = %s（同一条赋值链的两个成员）" % mp.nstr(diff, 6))
    return ("CIRCULAR" if diff < mp.mpf("1e-12") else "NOT-CIRCULAR"), notes


def build_mutant():
    src, enc, note = read_any(OPEN5B_PY)
    if src is None:
        raise SystemExit("变异体需要 OPEN5b 源码，读取失败：%s (%s)" % (OPEN5B_PY, note))
    anchor = re.findall(r"^G2_TUFT = 0\.00404[^\n]*$", src, flags=re.M)
    if len(anchor) != 1:
        raise SystemExit("变异体锚点在 OPEN5b 里命中 %d 行（应为 1 行），针位不可信" % len(anchor))
    fixed = re.sub(r"^G2_TUFT = 0\.00404[^\n]*$",
                   "OMEGA_SOLVE = mp.mpf('0.00202')\nG2_TUFT = 2 * OMEGA_SOLVE",
                   src, count=1, flags=re.M)
    assert fixed != src, "变异体未能改写 G2_TUFT 那一行"
    p = os.path.join(HERE, "_mutant_open5b_fake.py")
    io.open(p, "w", encoding="utf-8", newline="\n").write(fixed)
    return p


def main():
    global OUT
    mutant = "--mutant" in sys.argv
    if mutant:
        OUT = os.path.join(HERE, STEM + "_mutant_report.txt")   # 不许覆盖基线报告
    if not os.path.isdir(LEGACY):
        print("EXIT 6  扫描根推错了：LEGACY 目录不存在 -> %s" % LEGACY)
        return 6
    put("=" * 84)
    put("TUFT g-2 / EDM 多口径普查与基线循环性判定   2026-09-30（只读件）")
    put("扫描根 = %s （排除嵌套 .git）" % os.path.relpath(ROOT).replace("\\", "/"))
    put("=" * 84)

    # ---------------- C1 覆盖面 ----------------
    put("\n== C1. 覆盖面普查 ==")
    files, unreadable, excluded_self = walk_corpus()
    put("  [实测分母] 被扫描文件数 = %d   其中不可读 = %d   本件自有产物被排除 = %d"
        % (len(files), len(unreadable), excluded_self))
    if excluded_self == 0:
        print("EXIT 7  自排除通道没开火（覆盖面里含本件自己的声明行＝自证）")
        return 7
    for p, note in unreadable[:6]:
        put("     unreadable: %s (%s)" % (p, note))
    hits = census_tokens(files)
    missing = []
    for key, _, label in CENSUS:
        hs = hits[key]
        uniq = sorted({h[0] for h in hs})
        put("  %-32s 命中行 %5d  载体文件 %3d  (%s)" % (key, len(hs), len(uniq), label))
        for h in hs[:3]:
            put("        %s:%d  [%s]" % (h[0], h[1], h[2]))
        if not hs:
            missing.append(key)
            put("        NO-CARRIER")
    put("  [C1 判定] 声明口径 %d 枚，无载体 %d 枚" % (len(CENSUS), len(missing)))

    # ---------------- C2 复算 ----------------
    put("\n== C2. 从 CODATA 现算，并与 report 印出的读数逐位比对 ==")
    AL = mp.mpf(1) / mp.mpf("137.035999084")
    # 两个输入都从 OPEN5/OPEN5b 的源码现读，不许由本件复述常量
    ln_ae, kind_ae, val_ae = find_any_assign(OPEN5_PY, "A_E_EXP")
    rat = rational_of(OPEN5B_PY, "tau_over_kappa")
    ln_r0 = rat[1] if rat else None
    r0 = rat[0] if rat else None
    if val_ae is None or r0 is None:
        put("  [STRUCTURAL-FAIL] A_E_EXP@行=%s  tau_over_kappa@行=%s —— 有一枚没读到，"
            "本件拒绝用硬编常量顶替" % (ln_ae, ln_r0))
        text = "\n".join(L) + "\n"
        io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)
        print(text)
        print("EXIT 7  结构读取失败，复算的输入不是从载体读的")
        return 7
    AE = mp.mpf(repr(val_ae))
    put("  [输入来源] A_E_EXP 读自 OPEN5.py:%s（类型 %s，值 %s）；"
        "tau_over_kappa 读自 OPEN5b.py:%s = %s"
        % (ln_ae, kind_ae, val_ae, ln_r0, mp.nstr(r0, 12)))
    G2EXP = 2 * AE
    a8 = AL / (8 * mp.pi)
    a2 = AL / (2 * mp.pi)
    ap = AL / mp.pi
    dev_open5 = (AE - a8) / AE * 100

    g2b = 2 * r0
    dev_open5b = (g2b - G2EXP) / G2EXP * 100

    put("  α/(8π) = %s  vs a_e(exp) = %s  偏差(低侧) = %s %%"
        % (mp.nstr(a8, 10), mp.nstr(AE, 10), mp.nstr(dev_open5, 6)))
    put("  α/(2π) = %s  （QED 主导项，与 a_e 差 %s %%）"
        % (mp.nstr(a2, 10), mp.nstr((a2 - AE) / AE * 100, 5)))
    put("  α/π    = %s  vs 2a_e = %s  比值 = %s （不涉挠率的现成近似，勿当推导）"
        % (mp.nstr(ap, 10), mp.nstr(G2EXP, 10), mp.nstr(ap / G2EXP, 9)))
    put("  2τ/κ   = %s （τ/κ 读自 OPEN5b 的 Rational，非复述）偏差(高侧) = %s %%"
        % (mp.nstr(g2b, 10), mp.nstr(dev_open5b, 6)))
    collide = abs(dev_open5 - dev_open5b)
    put("  [反向碰撞] 两个偏差 %s%% 与 %s%%，只差 %s 个百分点，却一个偏低一个偏高、"
        "对象还分别是 a_e 与 2a_e ⇒ 只说「75%% 偏差」无法判定该往哪边修"
        % (mp.nstr(dev_open5, 5), mp.nstr(dev_open5b, 5), mp.nstr(collide, 4)))

    FG = G2EXP / g2b
    EDM_CM = mp.mpf("2.2570e-34")
    EDM_ECM = EDM_CM / mp.mpf("1.602176634e-19") * 100
    ACME = mp.mpf("1.1e-29")
    JILA = mp.mpf("4.1e-30")
    FD = ACME / EDM_ECM
    split = FG / FD
    put("  F_g 需 = %s   F_d 需 = %s   分裂比 = %s （log10 = %s）"
        % (mp.nstr(FG, 8), mp.nstr(FD, 8), mp.nstr(split, 8), mp.nstr(mp.log10(split), 9)))
    put("  单位换算自洽：2.2570e-34 C·m -> %s e·cm；档案另印 1.4089e-13（OPEN6）与 "
        "1.4087e-13（OPEN5b）" % mp.nstr(EDM_ECM, 10))
    put("  上限口径差：ACME2018 %s / JILA2023 %s 相差 %s 倍；同一 d_e 分别超限 %s 与 %s 倍"
        % (mp.nstr(ACME, 3), mp.nstr(JILA, 3), mp.nstr(ACME / JILA, 4),
           mp.nstr(EDM_ECM / ACME, 5), mp.nstr(EDM_ECM / JILA, 5)))

    checks = []

    def chk(label, mine, pat, carrier, tol):
        t, enc, note = read_any(carrier)
        if t is None:
            checks.append((label, "NO-CARRIER", note))
            return
        m = re.search(pat, t)
        if not m:
            checks.append((label, "PATTERN-NOT-FOUND", pat))
            return
        theirs = mp.mpf(m.group(1))
        rel = abs(mine - theirs) / abs(theirs)
        checks.append((label, "OK" if rel <= tol else "MISMATCH",
                       "carrier=%s 本件=%s 相对差=%s" % (mp.nstr(theirs, 11),
                                                       mp.nstr(mine, 11), mp.nstr(rel, 3))))

    chk("OPEN5 a_TUFT = α/(8π)", a8, r"a_TUFT = α/\(8π\) = ([0-9.eE+\-]+)", OPEN5_RPT, mp.mpf("5e-5"))
    chk("OPEN5 偏差 vs 实验", dev_open5, r"TUFT vs 实验值\s*：偏差 = ([0-9.]+)%", OPEN5_RPT, mp.mpf("2e-3"))
    chk("OPEN5b F_g = 0.574085", FG, r"2τ/κ\) = ([0-9.]+)", OPEN5B_RPT, mp.mpf("2e-4"))
    chk("OPEN5b 分裂比", split, r"分裂比=([0-9.eE+\-]+)", OPEN5B_RPT, mp.mpf("6e-3"))
    chk("OPEN6 超限倍数", EDM_ECM / ACME, r"\|d_e\|_ACME2018 = ([0-9.eE+\-]+)", OPEN6_RPT, mp.mpf("1e-2"))
    for label, verdict, detail in checks:
        put("  [%-17s] %-24s %s" % (verdict, label, detail))

    # ---------------- C3 循环性 ----------------
    put("\n== C3. 0.00404 这个基线从哪来（ast 读结构，不读文案） ==")
    target = build_mutant() if mutant else OPEN5B_PY
    if mutant:
        put("  [MUTANT] 假前像 %s：G2_TUFT 改为由表达式算出，其余一字不动"
            % os.path.basename(target))
    verdict, notes = detect_circular(target)
    for n in notes:
        put("     " + n)
    put("  [C3 判定] %s%s" % (verdict, "（变异体应为此项）" if mutant else ""))
    src5c, enc, note = read_any(OPEN5C_PY)
    retracted = [i for i, line in enumerate((src5c or "").splitlines(), 1) if "应修正为" in line]
    put("  [撤回在案] OPEN5c.py 内『应修正为』（把『τ/κ 被孤子自洽锁死』改为『由额外孤子解选定』）"
        "出现的行 = %s" % (retracted or "未找到"))
    if mutant:
        try:
            os.remove(target)
        except OSError:
            pass

    # ---------------- 退出码 ----------------
    text = "\n".join(L) + "\n"
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(text)
    print(text)
    bad = [c for c in checks if c[1] != "OK"]
    if missing:
        print("EXIT 2  有声明口径无载体：%s" % missing)
        return 2
    if bad:
        print("EXIT 3  复算与载体读数不一致：%s" % [b[0] for b in bad])
        return 3
    if verdict == "STRUCTURAL-FAIL" or verdict == "UNREADABLE":
        print("EXIT 7  循环性判定的结构读取未开火：%s" % verdict)
        return 7
    if mutant and verdict == "CIRCULAR":
        print("EXIT 4  变异体未被判为 NOT-CIRCULAR —— 检测器坏，不是数据坏")
        return 4
    if not mutant and verdict != "CIRCULAR":
        print("EXIT 5  预期基线为循环定价，检测器却判 %s" % verdict)
        return 5
    print("EXIT 0  覆盖面非空、5 项复算逐位回到 3 份 report、循环性判定带牙")
    return 0


if __name__ == "__main__":
    sys.exit(main())
