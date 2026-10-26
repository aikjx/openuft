# -*- coding: utf-8 -*-
"""r218: upgrade scanner (boundary + framework-symbol + positive control), fix pricing,
verdict token number, ast.Str deprecation."""
import io
import re

ENG = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化\源码\TUFT-r218_四力统一方程_定义恒等式零判别力覆盖缺与修复定价_精算_2026-10-26.py"

t = io.open(ENG, encoding="utf-8").read()

# ---------- 1) replace derived_external_equations with upgraded version ----------
start = t.index("def derived_external_equations(md):")
end = t.index("def external_input_ledger(md):")
new_fn = '''def derived_external_equations(md):
    """
    找出「把某个外部符号写到等号左侧、且右侧不再复现同一符号」的方程，并且
    **右侧须含框架内部符号**（否则只是定义/换算，例如 \\alpha=e^2/4\\pi\\varepsilon_0\\hbar c
    是 α 的定义重排，不算推导）。
    · 边界匹配：避免 F_G 里的 "G"、\\alpha_w 里的 "\\alpha" 之类子串误命中。
    """
    hits = []
    for eq in tex_equations(md):
        left, right = eq.split("=", 1)
        if not any(re.search(p, right) for p in FRAMEWORK_PATTERNS):
            continue
        for name, pat in TOKEN_PATTERNS.items():
            if re.search(pat, left) and not re.search(pat, right):
                hits.append((name, eq.strip()))
    return hits


def scanner_positive_control():
    """正对照：注入两条含框架内部符号的合成方程，扫描器必须命中（否则它恒 0，无分辨力）。"""
    fake = (r"$G=\\ell^{-2}\\kappa\\hbar c$ \\qquad $m_W=\\omega\\hbar/c^2$")
    return {"n": len(derived_external_equations(fake)),
            "sample": fake}


'''
t = t[:start] + new_fn + t[end:]

# ---------- 2) insert patterns after EXTERNALS_LITERALS block ----------
anchor = 'TEX_EQ = re.compile(r"\\$([^$]*=[^$]*)\\$")'
assert anchor in t, "TEX_EQ anchor"
patterns = anchor + '''

# 外部参数符号的**边界**正则（防子串误命中）
TOKEN_PATTERNS = {
    "G": r"(?<![A-Za-z_\\\\^])G(?![A-Za-z_])",
    r"\\alpha": r"\\\\alpha(?![A-Za-z_])",
    "m_W": r"m_(?:\\{)?W(?:\\})?(?![A-Za-z0-9])",
    "m_Z": r"m_(?:\\{)?Z(?:\\})?(?![A-Za-z0-9])",
    r"m_{\\pi}": r"m_(?:\\{)?\\\\pi(?:\\})?(?![A-Za-z0-9])",
    "g_W": r"g_(?:\\{)?W(?:\\})?(?![A-Za-z0-9])",
    r"g_\\pi": r"g_(?:\\{)?\\\\pi(?:\\})?(?![A-Za-z0-9])",
    r"\\sigma": r"\\\\sigma(?![A-Za-z_])",
}
# 框架**内部**符号（推导的右侧必须至少含其一，否则只是定义/换算）
FRAMEWORK_PATTERNS = [r"\\\\kappa", r"\\\\tau", r"\\\\omega", r"\\\\Omega", r"\\\\ell",
                      r"\\\\beta", r"\\\\rho", r"\\\\Theta", "螺旋", "曲率", "挠率",
                      "频率", "分形", r"Z_\\{?4\\}?", "Q_H", "D_f", r"c_0"]
'''
t = t.replace(anchor, patterns)

# ---------- 3) repair pricing: survival requires ALL four conditions ----------
old_price = '''        if 1 in fixes or 2 in fixes:
            verdict = "SUICIDE"   # 必须越过单极线性齐次 Proca 形式 ⇒ 原方程被替换
        elif 0 not in fixes or 3 not in fixes:
            verdict = "EMPTY"     # 仍无跨通道关系或参数仍外部 ⇒ 宣称不被满足
        else:
            verdict = "SURVIVE"'''
new_price = '''        if not (0 in fixes and 1 in fixes and 2 in fixes and 3 in fixes):
            verdict = "EMPTY"     # 四条件缺任一 ⇒ 「四力统一到一个方程」不被满足
        else:
            # 四条件齐备 ⇒ 必含 C1/C2 ⇒ 单极线性齐次 Proca 形式被替换：修复即自杀
            verdict = "SUICIDE"'''
assert old_price in t, "pricing anchor"
t = t.replace(old_price, new_price)

# ---------- 4) controls C21/C22 + add C29 scanner positive control ----------
old_c21 = '''    ctl("C21", "修复定价 16 组合且 SURVIVE=0",
        price["n_combos"] == 16 and price["counts"]["SURVIVE"] == 0,
        str(price["counts"]))
    ctl("C22", "修复定价 SUICIDE=12 且 EMPTY=4",
        price["counts"]["SUICIDE"] == 12 and price["counts"]["EMPTY"] == 4,
        str(price["counts"]))'''
new_c21 = '''    ctl("C21", "修复定价 16 组合且 SURVIVE=0",
        price["n_combos"] == 16 and price["counts"]["SURVIVE"] == 0,
        str(price["counts"]))
    ctl("C22", "修复定价 EMPTY=15 且 SUICIDE=1（唯一齐备组合即自杀）",
        price["counts"]["EMPTY"] == 15 and price["counts"]["SUICIDE"] == 1,
        str(price["counts"]))
    ctl("C29", "扫描器正对照：注入含框架内部符号的合成方程应命中 2 条（否则恒 0 无分辨力）",
        scanner_positive_control()["n"] == 2,
        str(scanner_positive_control()["n"]))'''
assert old_c21 in t, "C21 anchor"
t = t.replace(old_c21, new_c21)

# ---------- 5) entry B1 text: mention the two excluded cases honestly ----------
old_b1 = '''    add("B1", "L2 预测预算",
        "框架内推导某外部参数的方程计数 = %d（扫描全部 $..$ 方程，要求该符号出现在等号左侧"
        "且右侧不复现）：所有 (G, α, m_W, m_Z, m_π⁰, α_w, g_π²/4π, σ) 均为外部给定，"
        "预测预算 = 0。" % len(derived),'''
new_b1 = '''    add("B1", "L2 预测预算",
        "框架内推导某外部参数的方程计数 = {0}（扫描全部 $..$ 方程：符号须**边界匹配**地出现在"
        "等号左侧、右侧不复现，且右侧须含框架内部符号）：(G, α, m_W, m_Z, m_π⁰, α_w, "
        "g_π²/4π, σ) 全为外部给定，预测预算 = 0。甄别排除 2 条：α=e²/(4πε₀ℏc) 是 α 的"
        "**定义重排**、F_E/F_G=α(m_P/m_p)² 中的 G 属**子串误命中**。".format(len(derived)),'''
assert old_b1 in t, "B1 anchor"
t = t.replace(old_b1, new_b1)

# ---------- 6) entry G1 pricing counts text ----------
old_g1 = '''    add("G1", "修复定价",
        "2⁴=%d 组合位掩码：%s ⇒ EMPTY %d / SUICIDE %d / SURVIVE %d。"
        % (price["n_combos"], "、".join(FIX_NAMES), price["counts"]["EMPTY"],
           price["counts"]["SUICIDE"], price["counts"]["SURVIVE"]),
        "FAIL",
        "任取 C1/C2 即须越过单极齐次 Proca 形式（原方程被替换 ⇒ 自杀）；不取 C0/C3 则宣称"
        "不被满足 ⇒ 空集")'''
new_g1 = '''    add("G1", "修复定价",
        "2⁴={0} 组合位掩码（必要条件：{1}）⇒ EMPTY {2} / SUICIDE {3} / SURVIVE {4}："
        "唯一满足四条件的组合（C0+C1+C2+C3 齐备）必然要求越过单极齐次 Proca 形式，"
        "即把原方程替换掉——**修复即自杀**；缺任一条件的 {2} 个组合下宣称不被满足。"
        .format(price["n_combos"], "、".join(FIX_NAMES), price["counts"]["EMPTY"],
                price["counts"]["SUICIDE"], price["counts"]["SURVIVE"]),
        "FAIL",
        "本线第 25 度「修复即自杀」（并行 r205–r217 计数归各会话）")'''
assert old_g1 in t, "G1 anchor"
t = t.replace(old_g1, new_g1)

# ---------- 7) verdict token number R215 -> R218 ----------
t = t.replace('        "R215", "FOUR-FORCE-UNIFIED-EQUATION",', '        "R218", "FOUR-FORCE-UNIFIED-EQUATION",')
t = t.replace("REPAIR-PRICING-16-COMBOS-SURVIVE-0-SUICIDE-12-EMPTY-4-LINE-25TH-DEGREE-FIX-EQUALS-SUICIDE",
              "REPAIR-PRICING-16-COMBOS-SURVIVE-0-SUICIDE-1-EMPTY-15-LINE-25TH-DEGREE-FIX-EQUALS-SUICIDE")

# ---------- 8) ast.Str deprecation -> ast.Constant ----------
old_ast = '''            first = node.args[0].s if node.args and isinstance(node.args[0], ast.Str) \\
                else getattr(node.args[0], "value", None) if node.args else None'''
new_ast = '''            first = None
            if node.args:
                a0 = node.args[0]
                if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
                    first = a0.value
                elif isinstance(a0, ast.Str):  # py<3.8 兜底
                    first = a0.s'''
if old_ast in t:
    t = t.replace(old_ast, new_ast)

# ---------- 9) pricing section in verdict md (counts auto) ----------
t = t.replace("    L.append(\"- **本线第 25 度「修复即自杀」**（并行 r205–r214 计数归各会话）。\")",
              "    L.append(\"- **本线第 25 度「修复即自杀」**（并行 r205–r217 计数归各会话）。\")")

io.open(ENG, "w", encoding="utf-8").write(t)
print("patched all 9 items")
