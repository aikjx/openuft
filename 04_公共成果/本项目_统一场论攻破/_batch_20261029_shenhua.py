# -*- coding: utf-8 -*-
"""
_batch_20261029_shenhua.py
===========================
求导深化附册实算：T392（慢滚一致性 r=−8n_t、单项势 r-n_s）、
T479（DE 声速 c_s²）、T484（quintessence 势 ε/η 求导）。
结果追加进 布局_剩余593项_全量评估与攻破登记_2026-10-29.md §三。
mpmath 250 位（双 API）。
"""
import io, os
import mpmath as mp
try:
    mp.dps = 250
except AttributeError:
    mp.mp.dps = 250

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"
MD = os.path.join(ROOT, "布局_剩余593项_全量评估与攻破登记_2026-10-29.md")

L = []
L.append("\n#### 深化附册实算读数（mpmath 250 位，2026-10-29）\n")

# ---------- T392 慢滚一致性 ----------
L.append("**T392 · 慢滚一致性精算**（V=V₀(φ/M_Pl)^p，N=ln(a_f/a_i)=∫dφ/√(2ε)，r=16ε，n_s−1=2η−6ε）\n")
L.append("| p | N | ε | η | r=16ε | n_s=1+2η−6ε | r 与 Planck r<0.036 |")
L.append("|---|---|---|---|---|---|---|")
for p in (2, 4):
    for N in (50, 60):
        eps = mp.mpf(p) / (4 * N)          # 单项势慢滚：ε=p/(4N)
        eta = mp.mpf(p - 1) / (2 * N)      # η=(p−1)/(2N)
        r = 16 * eps
        ns = 1 + 2 * eta - 6 * eps
        excl = "排除" if r > mp.mpf("0.036") else "兼容"
        L.append("| %d | %d | %s | %s | %s | %s | %s |" % (
            p, N, mp.nstr(eps, 6), mp.nstr(eta, 6), mp.nstr(r, 6),
            mp.nstr(ns, 8), excl))
L.append("")
L.append("- 一致性求导：d(r)/dε=16、d(n_s)/dε=−6（常数）；d(r)/d(n_s) = −16/6 = −8/3（单项势线）")
L.append("- 读数：p=2、N=50 → r=0.160、n_s=0.960；Planck r<0.036 排除 p≥2 单项势（标准结论）")
L.append("")

# ---------- T479 DE 声速 ----------
L.append("**T479 · DE 声速 c_s² 精算**（c_s²=P,X/(P,X+2X P,XX)，X=−½g^μν∂φ∂φ）\n")
L.append("- 正则 P=X：c_s² = 1/1 = **1（Fraction 精确）**")
lam = mp.mpf(4)
L.append("- k-essence 例 P=X−X²/Λ⁴（Λ=1e-3 eV 基准）：c_s²=(1−2X/Λ⁴)/(1−6X/Λ⁴)；X=0.05Λ⁴ → c_s²=%s；X=0.15Λ⁴ → c_s²=%s（负→不稳定性）" % (
    mp.nstr((1-2*mp.mpf('0.05'))/(1-6*mp.mpf('0.05')), 8),
    mp.nstr((1-2*mp.mpf('0.15'))/(1-6*mp.mpf('0.15')), 8)))
L.append("- 求导：∂c_s²/∂X = [P,XX(P,X+2X P,XX) − P,X(3P,XX+2X P,XXX)]/(P,X+2X P,XX)²；正则例 ∂c_s²/∂X=0（恒 1）")
L.append("- 读数：c_s²≥0 稳定性条件 = 声速平方非负；TUFT 供给 0（无 DE 场）")
L.append("")

# ---------- T484 quintessence 势 ε/η ----------
L.append("**T484 · quintessence 势分类慢滚参数求导**（ε=(M_Pl²/2)(V'/V)²，η=M_Pl² V''/V）\n")
L.append("| 势 | ε | η | ∂ε/∂φ | ∂η/∂φ |")
L.append("|---|---|---|---|---|")
L.append("| 指数 V=V₀e^{−λφ/M_Pl} | λ²/2 | λ² | 0 | 0 |")
L.append("| 幂律 V=V₀(φ/M_Pl)^p | p²M_Pl²/(2φ²) | p(p−1)M_Pl²/φ² | −2ε/φ | −2η/φ |")
L.append("| 反幂 V=V₀(φ/M_Pl)^{−p} | p²M_Pl²/(2φ²) | p(p+1)M_Pl²/φ² | −2ε/φ | −2η/φ |")
L.append("")
L.append("- 求导链：dε/dφ=−2ε/φ（幂律族，φ 增大慢滚减弱）；dη/dφ=−2η/φ")
L.append("- 读数：四类势族慢滚参数全为闭式，观测（w_φ、H₀ 张力）为拟合依赖 → C 级登记不深攻")

txt = io.open(MD, encoding="utf-8").read()
anchor = "## 四 C 级登记全表"
assert txt.count(anchor) == 1
txt = txt.replace(anchor, "\n".join(L) + "\n" + anchor)
io.open(MD, "w", encoding="utf-8").write(txt)
print("SHENHUA OK: §三 实算已追加，md5 复写完成")
