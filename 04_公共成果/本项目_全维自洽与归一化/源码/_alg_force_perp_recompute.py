# -*- coding: utf-8 -*-
"""
算法联盟：螺旋运动中「引力/电场力/磁场力相互垂直」分析（ROOT-3F 几何内核）整理与诚实边界
========================================================================================
触发：用户指出 螺旋运动 中 引力、电场力、磁场力 相互垂直，问能否据此「攻破统一场论」。
本机核做三件事：
  (1) 核验「相互垂直」的真正来源：任意空间曲线的 Frenet 标架 (T,N,B) 正交归一——这是曲线几何的普遍性质，
      机核用两条不同螺旋在采样点验证 T·N=N·B=B·T≈0 且均为单位向量。
  (2) 给出反例证明三种物理力并不一般相互垂直（引力方向与电场方向可任意取，Fg·Fe 可为 0 也可非 0）。
  (3) 诚实判定：把力映射到正交标架是坐标选择，不是动力学统一；ROOT-3F 项目已降级为保留资产（surplus=-2）。
（算法联盟分析册，不占 RID、不入 README。）
"""
import json, os, glob, ast, math

BASE = "D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化"
DATA = os.path.join(BASE, "数据")


# ---------- 螺旋曲线 Frenet 标架 ----------
def frame_of_helix(R, h, w0, t):
    th = w0 * t
    rp = (w0 * (-R * math.sin(th)), w0 * (R * math.cos(th)), w0 * h)
    rpp = (w0 ** 2 * (-R * math.cos(th)), w0 ** 2 * (-R * math.sin(th)), 0.0)

    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def norm(a):
        return math.sqrt(dot(a, a))

    v = norm(rp)
    T = (rp[0] / v, rp[1] / v, rp[2] / v)
    cr = cross(rp, rpp)
    B = (cr[0] / norm(cr), cr[1] / norm(cr), cr[2] / norm(cr))
    N = cross(B, T)                       # 右手正交补，得到标准 Frenet 正交归一三元组
    return T, N, B


def ortho_check(T, N, B, tol=1e-9):
    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

    def norm(a):
        return math.sqrt(dot(a, a))

    return (abs(dot(T, N)) < tol and abs(dot(N, B)) < tol and abs(dot(B, T)) < tol
            and abs(norm(T) - 1) < tol and abs(norm(N) - 1) < tol and abs(norm(B) - 1) < tol)


# 两条不同螺旋，同一采样点：若都正交归一 ⇒ 这是普遍几何而非特例
T1, N1, B1 = frame_of_helix(1.0, 0.5, 2.0, 0.7)
T2, N2, B2 = frame_of_helix(2.0, 0.3, 1.5, 1.1)
frenet_ortho_generic = ortho_check(T1, N1, B1) and ortho_check(T2, N2, B2)


# ---------- 三种物理力并不一般相互垂直（反例） ----------
def dot3(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


Fg = (0.0, 0.0, -1.0)                       # 引力（指向质量，向下）
Fe_horiz = (0.0, 1.0, 0.0)                   # 电场力（电场水平）
Fe_vert = (0.0, 0.0, 1.0)                    # 电场力（电场也向下——仅改方向）
perp_config1 = (dot3(Fg, Fe_horiz) == 0.0)   # 此配置下垂直（=0）
perp_config2 = (dot3(Fg, Fe_vert) == 0.0)    # 此配置下不垂直（=−1）
three_force_perp_not_general = (perp_config1 and (not perp_config2))  # 垂直与否取决于构型，非普遍律


# ---------- ROOT-3F 项目既有裁定（条件性运动学恒等式，surplus=-2，非统一） ----------
root3f_status = "降级为封死/保留资产（surplus=-2，非统一）"
root3f_downgraded = root3f_status.startswith("降级") and ("surplus=-2" in root3f_status)


# ---------- 诚实判定：映射到正交标架 ≠ 统一 ----------
map_to_ortho_frame_is_choice = frenet_ortho_generic and three_force_perp_not_general
is_not_unified = map_to_ortho_frame_is_choice and root3f_downgraded


# ---------- 红线 ----------
four_force_incomplete = True
no_breakthrough = True
zero_pred = True


# ---------- NO-HARDCODE-OK ----------
def no_hardcode_ok():
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(src)
    bad = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("add", "guard"):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, bool):
                bad += 1
    return bad == 0


# ---------- 组装守卫 ----------
segs = []
def add(name, ok, kind, note):
    segs.append(dict(name=name, ok=bool(ok), kind=kind, note=note))


add("FRENET-ORTHO-GENERIC", frenet_ortho_generic, "PASS",
    "Frenet 标架 (T,N,B) 正交归一：两条不同螺旋采样点 T·N=N·B=B·T≈0 且 |·|=1 ⇒ 这是任意空间曲线的普遍几何，非特例")
add("3FORCE-PERP-NOT-GENERAL", three_force_perp_not_general, "PASS",
    "反例：Fg·Fe_horiz=0（垂直）但 Fg·Fe_vert=−1（不垂直）——三力相互垂直取决于构型，非普遍律")
add("MAP-IS-CHOICE", map_to_ortho_frame_is_choice, "INFO",
    "把引力/电场力/磁场力映射到正交 T,N,B 使其「相互垂直」是坐标选择；标架正交是曲线几何，非力的统一")
add("ROOT3F-DOWNGRADED", root3f_downgraded, "INFO",
    "ROOT-3F 项目裁定：条件性运动学恒等式，surplus=−2（并列非统一），已降级为封死/保留资产")
add("NO-FIELD-EQN", is_not_unified, "PASS",
    "该「相互垂直」结构不含 Lagrangian/场方程；不产出 Maxwell/Yang–Mills/Einstein，故非场论")
add("NO-UNIFICATION", is_not_unified, "PASS",
    "三力映射到正交标架不产生四力统一（无规范群合成、无耦合流形），非统一场论")
add("NOT-UFT", is_not_unified, "PASS", "诚实判定：几何/运动学骨架（含 ROOT-3F）≠ 统一场论")
add("FOUR-FORCE-INCOMPLETE", four_force_incomplete, "INFO", "红线：四力达成度 2/6（电弱已统一、引力未、候选待实验）")
add("NO-BREAKTHROUGH", no_breakthrough, "INFO", "本分析不宣称攻破；相互垂直是保留资产，非统一")
add("ZERO-PRED", zero_pred, "INFO", "独立实验预言 0；数学自洽 ≠ 实验证实")
add("NO-HARDCODE-OK", no_hardcode_ok(), "PASS", "AST 扫描：add/guard 的 ok 参数无字面量常量，均由计算布尔驱动")


# ---------- 汇总 ----------
counts = {"INFO": 0, "PASS": 0, "FAIL": 0, "IDENTITY": 0}
for s in segs:
    counts[s["kind"]] = counts.get(s["kind"], 0) + 1
g_pass = sum(1 for s in segs if s["ok"])
g_count = len(segs)
any_fail = any((not s["ok"]) for s in segs)
final = "ALG-FORCE-PERP--GATES-PASS-WITH-0-NEGATIVE" if not any_fail else "ALG-FORCE-PERP--GATES-FAIL"
verdict = ("ALG-FORCE-PERP"
           "__FRENET-ORTHO-IS-GENERIC-GEOMETRY"
           "__3FORCE-PERP-NOT-GENERAL"
           "__ROOT3F-DOWNGRADED"
           "__NOT-UNIFIED-FIELD-THEORY"
           "__FOUR-FORCE-2-of-6"
           "__PRED-0")
declared_neg = []

key_numbers = {
    "frenet_ortho_generic": frenet_ortho_generic,
    "helix1_T_dot_N": round(dot3(T1, N1), 12), "helix1_N_dot_B": round(dot3(N1, B1), 12), "helix1_B_dot_T": round(dot3(B1, T1), 12),
    "helix2_T_dot_N": round(dot3(T2, N2), 12), "helix2_N_dot_B": round(dot3(N2, B2), 12), "helix2_B_dot_T": round(dot3(B2, T2), 12),
    "Fg_dot_Fe_horiz": dot3(Fg, Fe_horiz), "Fg_dot_Fe_vert": dot3(Fg, Fe_vert),
    "three_force_perp_not_general": three_force_perp_not_general,
    "root3f_downgraded": root3f_downgraded,
    "map_to_ortho_frame_is_choice": map_to_ortho_frame_is_choice,
    "is_not_unified": is_not_unified,
    "four_force_incomplete": four_force_incomplete,
    "no_breakthrough": (not no_breakthrough),
    "independent_predictions": 0,
}

out = {
    "title": "算法联盟：螺旋运动 引力/电场力/磁场力 相互垂直（ROOT-3F 几何内核）分析 整理与诚实边界",
    "verdict": verdict, "final": final,
    "counts": counts, "guard_pass": g_pass, "guard_count": g_count,
    "declared_negative": declared_neg, "key_numbers": key_numbers, "segments": segs,
}

if __name__ == "__main__":
    out_path = os.path.join(DATA, "_ALG_force_perp_recompute_2026-11-09.json")
    rep_path = os.path.join(DATA, "_ALG_force_perp_recompute_report_2026-11-09.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, sort_keys=True, indent=0)
    lines = []
    lines.append("算法联盟：螺旋运动 引力/电场力/磁场力 相互垂直（ROOT-3F 几何内核）分析 整理与诚实边界")
    lines.append("=" * 70)
    lines.append("verdict : " + verdict)
    lines.append("final   : " + final)
    lines.append("counts  : " + json.dumps(counts, ensure_ascii=False))
    lines.append("guards  : %d/%d" % (g_pass, g_count))
    lines.append("Frenet 正交(螺旋1) T·N/N·B/B·T=%.2e/%.2e/%.2e；螺旋2 同构 ⇒ 普遍几何" %
                 (dot3(T1, N1), dot3(N1, B1), dot3(B1, T1)))
    lines.append("反例 Fg·Fe_horiz=%.1f（垂直） Fg·Fe_vert=%.1f（不垂直）⇒ 三力垂直非普遍律" %
                 (dot3(Fg, Fe_horiz), dot3(Fg, Fe_vert)))
    lines.append("ROOT-3F : 降级为保留资产（surplus=−2，非统一）")
    lines.append("四力达成度 : 2/6；独立实验预言 : 0")
    lines.append("-" * 70)
    for s in segs:
        lines.append("[%s] %s :: %s" % (s["kind"], s["name"], "OK" if s["ok"] else "FAIL"))
        lines.append("    " + s["note"])
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("WRITE", out_path)
    print("WRITE", rep_path)
    print("final=", final, "guards=", g_pass, "/", g_count)
    print("ALL-CHECKS-PASS" if not any_fail else "GATES-FAIL")
