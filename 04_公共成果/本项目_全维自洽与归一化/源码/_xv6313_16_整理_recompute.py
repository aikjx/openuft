# -*- coding: utf-8 -*-
"""
整理册机核：X-V63-13 → X-V63-16 公式用途与可算判决归总
========================================================
性质：整理册（不占 RID、不入 README、不与任何卷相加）。
红线：本册只归总「已算结果」与「标准公式」，不产新物理；
      四力大统一仍 0 条正确解；独立实验预言 0；
      数学自洽 ≠ 实验证实；不宣称攻破统一场论。
核心结论：本轮（X-V63-13/14/15/16）没有发现任何新理论公式，
          所用公式均为 6D(1,0) 超引力 / F-理论 教科书标准式，
          仅被全量复算验证；唯一产出是「本口径内 CS 级 k 无法被内部机制钉死」的可算判决。
"""
import json, os, glob, ast
from fractions import Fraction

BASE = "D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化"
DATA = os.path.join(BASE, "数据")
SRC  = os.path.join(BASE, "源码")
README = os.path.join(BASE, "README.md")


def load_kn(prefix):
    fs = sorted(glob.glob(os.path.join(DATA, prefix)))
    if not fs:
        raise FileNotFoundError("找不到前缀匹配: " + prefix)
    return json.load(open(fs[0], encoding="utf-8"))["key_numbers"]


def load_full(prefix):
    fs = sorted(glob.glob(os.path.join(DATA, prefix)))
    if not fs:
        raise FileNotFoundError("找不到前缀匹配: " + prefix)
    return json.load(open(fs[0], encoding="utf-8"))


kn16 = load_kn("_XV6316_recompute_2026-11-09.json")
kn15 = load_kn("_XV6315_recompute_2026-11-09.json")
kn14 = load_kn("_XV6314_recompute_2026-11-08.json")
kn13 = load_kn("_XV6313_recompute_2026-11-08.json")
kn404 = load_kn("TUFT-r404_*.json")
full13 = load_full("_XV6313_recompute_2026-11-08.json")
full14 = load_full("_XV6314_recompute_2026-11-08.json")
full15 = load_full("_XV6315_recompute_2026-11-09.json")
full16 = load_full("_XV6316_recompute_2026-11-09.json")
full403 = load_full("TUFT-r403_*.json")
full404 = load_full("TUFT-r404_*.json")


# ---------- 1. 反常系数矩阵 M = Σ_f v_f⊗v_f（来自 X-V63-16 机核逐元读数） ----------
M_str = kn16["m_left"]
M = [[Fraction(x) for x in row] for row in M_str]


def rank_frac(A):
    """有理数高斯消元求秩（行阶梯形，纯 Fraction）。"""
    n = len(A); m = len(A[0])
    B = [list(r) for r in A]
    r = 0
    for c in range(m):
        piv = None
        for i in range(r, n):
            if B[i][c] != 0:
                piv = i; break
        if piv is None:
            continue
        B[r], B[piv] = B[piv], B[r]
        lead = B[r][c]
        for i in range(n):
            if i != r and B[i][c] != 0:
                f = B[i][c] / lead
                B[i] = [B[i][j] - f * B[r][j] for j in range(m)]
        r += 1
    return r


def rank_frac_T(A):
    """第二路：转置后求秩（rank(M)=rank(M^T)）。"""
    Mt = [list(col) for col in zip(*A)]
    return rank_frac(Mt)


r_direct = rank_frac(M)
r_transpose = rank_frac_T(M)

# 规范子矩阵（去掉引力行/列，取左上 3×3）
Mg = [row[:3] for row in M[:3]]
rank_g = rank_frac(Mg)

# 引力块
grav = [Fraction(x) for x in kn16["grav_block"]]   # [42,16,25,257]
m_gg = Fraction(kn16["m_gg"])                        # 257


# ---------- 2. 通量量子化 gcd 引理 {a·f : f∈ℤ^r} = gcd(a)·ℤ ----------
def gcd_euclid(a):
    g = abs(a[0])
    for x in a[1:]:
        xx = abs(x)
        while xx:
            g, xx = xx, g % xx
    return g


def _factorize(n):
    n = abs(n); f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def gcd_prime(a):
    """gcd 的质因数实现：仅保留出现在所有数中的公共素因子，取最小指数。"""
    facts = [_factorize(x) for x in a]
    common = set(facts[0].keys())
    for f in facts[1:]:
        common &= set(f.keys())
    g = 1
    for p in common:
        g *= p ** min(f[p] for f in facts)
    return g


cs_a = [4, 6, 8]
cs_a2 = [3, 6, 9]
g_a_e = gcd_euclid(cs_a);  g_a_p = gcd_prime(cs_a)
g_a2_e = gcd_euclid(cs_a2); g_a2_p = gcd_prime(cs_a2)


def image_in(a, g, lo=-3, hi=4):
    vals = set()
    rng = range(lo, hi)
    for f1 in rng:
        for f2 in rng:
            for f3 in rng:
                k = a[0] * f1 + a[1] * f2 + a[2] * f3
                if k % g != 0:
                    return None  # 引理失败
                vals.add(k)
    return vals


vals_a = image_in(cs_a, g_a_e)
vals_a2 = image_in(cs_a2, g_a2_e)
img_reach_a = (vals_a is not None) and (-2 in vals_a) and (2 in vals_a)
img_reach_a2 = (vals_a2 is not None) and (-3 in vals_a2) and (3 in vals_a2)


# ---------- 3. 跨卷二次核对（第二路，直读 r404 / X-V63-13/14/15） ----------
r404_cand = kn404["four_force_candidates"]
r404_acc = kn404["four_force_accepted"]

r403_ff_14 = kn14["r403_four_force"]
r403_ff_16 = kn16["r403_four_force"]
r403_g_14 = kn14["r403_guards_pass"]; r403_gt_14 = kn14["r403_guards_total"]

rm14 = kn14["rankM"]; mgg14 = kn14["m_gg"]
rm15 = kn15["rankM"]; mgg15 = kn15["m_gg"]

r403_c3 = kn13.get("r403_c3_four_force")

# 本册自身命名不得出现在 README，且不得有需登记的大写 RID 文件
_rb = open(README, "rb").read()
no_rid_in_readme = (b"_xv6313_16" not in _rb)
no_uppercase_rid_file = True
for p in glob.glob(os.path.join(SRC, "TUFT-r40*_*.py")) + glob.glob(os.path.join(DATA, "TUFT-r40*_*")):
    pass  # 仅确认不对 r40x 新增文件；本册前缀为小写 _xv6313_16_整理
# 显式断言：源码/数据目录下不存在本册大写 RID 登记文件
no_uppercase_rid_file = (len(glob.glob(os.path.join(SRC, "TUFT-r4*_整理*.py"))) == 0)


# ---------- 4. NO-HARDCODE-OK：扫描本文件，ok 参数不得为字面量常量 ----------
def no_hardcode_ok():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    bad = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("add", "guard"):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, bool):
                bad += 1
    return bad == 0


# ---------- 5. 组装判据段 ----------
segs = []
def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("M-LOAD", len(M) == 4 and len(M[0]) == 4, "PASS",
    "反常系数矩阵 M 从 X-V63-16 逐元读数载入，尺寸 4×4（基 {SU3,SU2,U1,GRAV}）")
add("TWO-PATH-M-RANK", r_direct == r_transpose == 4, "PASS",
    "M 秩两路一致：直接=%d、转置=%d，均=4" % (r_direct, r_transpose))
add("GAUGE-SUBMATRIX-RANK", rank_g == 3, "PASS",
    "规范子矩阵（去引力行/列）秩=%d=3，说明单一 GS 张量因式分解不可能（需 rank=1）" % rank_g)
add("GRAVITY-BLOCK", grav == [Fraction(42), Fraction(16), Fraction(25), Fraction(257)], "PASS",
    "引力块 M[3][*]=[42,16,25,257]，不含 CS 级 k，故引力配平不为 k 加新约束")
add("M_GG", m_gg == 257, "PASS",
    "引力·引力项系数 M_GG=Σdim_C²=257，与 X-V63-14/15 读数额外一致")
add("GCD-EUCLID-PRIME-AGREE-A", g_a_e == g_a_p == 2, "PASS",
    "a=[4,6,8] 的 gcd：Euclid=%d、质因数=%d，两路一致=2" % (g_a_e, g_a_p))
add("GCD-EUCLID-PRIME-AGREE-A2", g_a2_e == g_a2_p == 3, "PASS",
    "对照 a2=[3,6,9] 的 gcd：Euclid=%d、质因数=%d，两路一致=3" % (g_a2_e, g_a2_p))
add("GCD-LEMMA-IMAGE-A", vals_a is not None and img_reach_a, "PASS",
    "枚举 f∈[-3,3]³ 得 k∈2ℤ 且同时取到 -2 与 +2 ⇒ 图像恰为 2ℤ（离散但不唯一）")
add("GCD-LEMMA-IMAGE-A2", vals_a2 is not None and img_reach_a2, "PASS",
    "对照 a2 图像恰为 3ℤ，取到 -3 与 +3 ⇒ 引理对一般 a 成立")
add("K-NOT-UNIQUE", (vals_a is not None) and (len(vals_a) > 1), "INFO",
    "图像含 >1 个元素 ⇒ CS 级 k 未被钉死到唯一值；选具体 f 是额外输入，非现有数据可导出")
add("CROSS-R404", r404_cand == 7 and r404_acc == 0, "PASS",
    "直读 r404：four_force_candidates=7 / four_force_accepted=0 ⇒ 四力统一仍 0 条")
add("CROSS-R403-TWO-PATH", r403_ff_14 == r403_ff_16 == "0 条" and r403_g_14 == 32, "PASS",
    "X-V63-14 与 X-V63-16 各自独立回读 r403 均得四力 0 条 / 守卫 32/32，两路一致")
add("CROSS-XV14-15-RANK", rm14 == rm15 == 4 and str(mgg14) == str(mgg15) == "257", "PASS",
    "X-V63-14 与 X-V63-15 的 rank(M)=4、M_GG=257 跨卷一致")
add("CROSS-XV13-C3", r403_c3 == 0, "INFO",
    "X-V63-13 回读 r403 的 C3 四力=0，与本册红线（四力未证）一致")
add("NO-NEW-RID-NO-README", no_rid_in_readme and no_uppercase_rid_file, "PASS",
    "本册前缀 _xv6313_16_整理 不在 README；未新增大写 RID 登记文件 ⇒ 不占号、不入 README")
add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS",
    "AST 扫描本文件：add/guard 的 ok 参数无字面量常量（均由计算布尔驱动）")
# 红线诚信校验：扫描全链 verdict，确认无任何卷宣称「新物理/新公式/攻破」
_pos_tokens = ["NEW-PHYSICS", "FORMULA-DISCOVERED", "BREAKTHROUGH", "UNIFIED-FIELD-SOLVED", "攻破"]
_all_verdicts = [full13.get("verdict", ""), full14.get("verdict", ""), full15.get("verdict", ""),
                 full16.get("verdict", ""), full403.get("verdict", ""), full404.get("verdict", "")]
_no_positive_claim = all(not any(tok in v.upper() for tok in _pos_tokens) for v in _all_verdicts)
add("HONEST-NO-NEW-FORMULA", _no_positive_claim, "INFO",
    "扫描全链 6 个 verdict：均不含 NEW-PHYSICS/FORMULA-DISCOVERED/BREAKTHROUGH 等正面宣称 ⇒ 本链未产出新公式/新物理")


# ---------- 6. 汇总 ----------
counts = {"INFO": 0, "PASS": 0, "FAIL": 0, "IDENTITY": 0}
for s in segs:
    counts[s["kind"]] = counts.get(s["kind"], 0) + 1

guard_pass = sum(1 for s in segs if s["ok"])
guard_count = len(segs)
any_fail = any((not s["ok"]) for s in segs)

final = "ORGANIZED--GATES-PASS-WITH-0-NEGATIVE" if not any_fail else "ORGANIZED--GATES-FAIL"
verdict = ("NO-NEW-FORMULA-DISCOVERED"
           "__STANDARD-FORMULAS-ONLY"
           "__WITHIN-SCOPE-K-NOT-PINNED"
           "__FOUR-FORCE-0"
           "__PRED-0")

declared_neg = []  # 整理册不判负、不占 OPEN

key_numbers = {
    "m_left": [[str(x) for x in row] for row in M],
    "rankM": r_direct,
    "rankM_transpose": r_transpose,
    "rankM3": rank_g,
    "grav_block": [int(x) for x in grav],
    "m_gg": int(m_gg),
    "cs_a": cs_a,
    "flux_gcd_a_euclid": g_a_e,
    "flux_gcd_a_prime": g_a_p,
    "flux_gcd_a2_euclid": g_a2_e,
    "flux_gcd_a2_prime": g_a2_p,
    "flux_image_a_samples": sorted(int(x) for x in (vals_a or []))[:7],
    "k_pinned": False,
    "r404_candidates": r404_cand,
    "r404_accepted": r404_acc,
    "r403_four_force": r403_ff_16,
    "r403_guards_pass": r403_g_14,
    "r403_guards_total": r403_gt_14,
    "prev14_rankM": rm14,
    "prev14_m_gg": int(mgg14),
    "prev15_rankM": rm15,
    "prev15_m_gg": int(mgg15),
    "prev13_r403_c3_four_force": r403_c3,
    "readme_bytes": len(_rb),
    "no_new_rid": bool(no_rid_in_readme),
    "no_new_formula_discovered": False,
}

out = {
    "title": "整理册：X-V63-13→X-V63-16 公式用途与可算判决归总",
    "verdict": verdict,
    "final": final,
    "counts": counts,
    "guard_pass": guard_pass,
    "guard_count": guard_count,
    "declared_negative": declared_neg,
    "key_numbers": key_numbers,
    "segments": segs,
}

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(DATA, "_XV6313_16_整理_recompute_2026-11-09.json")
    rep_path = os.path.join(DATA, "_XV6313_16_整理_recompute_report_2026-11-09.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, sort_keys=True, indent=0)
    lines = []
    lines.append("整理册 X-V63-13→X-V63-16 公式用途与可算判决归总")
    lines.append("=" * 60)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : %d/%d" % (guard_pass, guard_count))
    lines.append("四力统一 : 仍 0 条（r403=0 条 / r404=7 选 0）")
    lines.append("独立实验预言 : 0")
    lines.append("新理论公式 : 无（所用均为标准 6D 超引力 / F-理论公式）")
    lines.append("-" * 60)
    for s in segs:
        lines.append("[%s] %s :: %s" % (s["kind"], s["name"], "OK" if s["ok"] else "FAIL"))
        lines.append("    " + s["note"])
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("WRITE", out_path)
    print("WRITE", rep_path)
    print("final=", final, "guards=", guard_pass, "/", guard_count)
    print("ALL-CHECKS-PASS" if not any_fail else "GATES-FAIL")
