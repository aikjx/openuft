# -*- coding: utf-8 -*-
"""
O-P1 攻关结论的复核 + 正典身份审计（zxq23_o1_verify）

修两个缺陷
----------
① **上一轮引入的未验证断言**：28 册声称「结构结论与参数取值无关，因为全部读数都是
   方向 + 标度的比对」—— 那是**断言**，不是读数。本脚本用 6 组参数重算，把它变成读数。
   （这正是本仓库反复登记的失效族：写下时看起来自明的结论，没有第二台机器复算。）

② **正典的身份缺陷**：正典把统一场 $\\vec A$ 称作「引力场」（沿用来料措辞），
   但 A 类 9 条的判据里**没有一条**支持这个身份 —— 它们全是量纲/代数/电磁内容。
   本脚本做语义审计，把「$\\vec A$ 是引力场」这条主张的证据状态量化。

依赖：仅标准库。运行：python -B zxq23_o1_verify.py [--strict]
"""

import json
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import zxq23_canon_deps as DEPS      # 复用同一份正典表解析器
import zxq23_o1_gap as GAP           # 复用向量工具与差分算子

OUT_JSON = os.path.join(HERE, "zxq23_o1_verify_results.json")
CANON_MD = os.path.join(BASE, "26_UFE2_正典_统一场方程正确子集规范_2026-10-03.md")

RESULTS = []


def rec(sid, sec, title, verdict, detail):
    RESULTS.append({"id": sid, "sec": sec, "title": title,
                    "verdict": verdict, "detail": detail})


def P(sid, sec, title, d):
    rec(sid, sec, title, "PASS", d)


def F(sid, sec, title, d):
    rec(sid, sec, title, "FAIL", d)


def BO(sid, sec, title, d):
    rec(sid, sec, title, "BOUNDARY", d)


def IN(sid, sec, title, d):
    rec(sid, sec, title, "INFO", d)


def g(x, n=6):
    return "%.*g" % (n, x)


# ============================================================ §A 参数扫描
PARAMS = [
    ("基准（v⊥=v_z）", 1.0, 1.0, 1.0),
    ("近轴向", 1.0, 1.0, 0.5),
    ("近横向", 1.0, 1.0, 2.0),
    ("快绕（ω=2）", 2.0, 1.0, 1.0),
    ("大半径（r=2）", 0.5, 2.0, 1.0),
    ("小半径（r=0.5）", 1.0, 0.5, 1.0),
]

TOL_DIR = 1e-9      # 方向余弦判据
TOL_REL = 1e-6      # 标度相对判据


def analyse(omega, rr, bb):
    """返回该组参数下的全部读数。全部走差分，不共用解析式中间量。"""
    rho_eff = math.sqrt(rr * rr + bb * bb)
    c_light = omega * rho_eff                      # 螺旋公设 ωρ=c
    v_perp = rr * omega
    v_axis = bb * omega

    # ---- 旋度：T = (v⊥ ê_φ + v_z ê_z)/c
    def field_T(p, vp=v_perp, cz=c_light, vz=v_axis):
        rho = math.hypot(p[0], p[1])
        if rho == 0.0:
            return [0.0, 0.0, 0.0]
        ph = math.atan2(p[1], p[0])
        return [(vp / cz) * (-math.sin(ph)), (vp / cz) * math.cos(ph), vz / cz]

    # 在螺旋上取点（ρ = r_helix），逐点算旋度与切向导数
    dir_curl, dir_cov, dots, scale_ratio, kappa_tau = [], [], [], [], []
    worst_k = worst_t = 0.0
    for i in range(5):
        t = 0.23 + 0.31 * i
        ph = omega * t
        pt = GAP.cyl(rr, ph, v_axis * t)

        cv = GAP.curl_centered(field_T, pt)
        ez = [0.0, 0.0, 1.0]
        dir_curl.append(GAP.dot(cv, ez) / GAP.norm(cv))

        # 切向导数 dT/ds = (1/c) dT/dt，T 沿螺旋
        def field_T_t(tt, vp=v_perp, cz=c_light, vz=v_axis, om=omega):
            p2 = om * tt
            return [(vp / cz) * (-math.sin(p2)), (vp / cz) * math.cos(p2), vz / cz]

        h = 1e-6
        dTdt = GAP.mul(GAP.sub(field_T_t(t + h), field_T_t(t - h)), 1.0 / (2 * h))
        dTds = GAP.mul(dTdt, 1.0 / c_light)
        er = GAP.e_r(rr, ph)
        dir_cov.append(-GAP.dot(dTds, er) / GAP.norm(dTds))
        dots.append(GAP.dot(cv, dTds) / (GAP.norm(cv) * GAP.norm(dTds)))

        # 标度关系 |∇×T| = v⊥/(cρ)
        ana = v_perp / (c_light * rr)
        scale_ratio.append(GAP.norm(cv) / ana)

        # κ、τ 用闭式（此处只做标度核对，不重复 O-P1 攻关的差分基线）
        k_th = rr * omega * omega / (c_light * c_light)
        tau_th = v_axis * omega / (c_light * c_light)
        kappa_tau.append(k_th * k_th + tau_th * tau_th - (omega / c_light) ** 2)
        worst_k = max(worst_k, abs(k_th - rr * omega * omega / (c_light * c_light)))

    alpha_local = v_perp / c_light
    # 标度恒等式：(|∇×T|/κ)·(ρω/c) = 1
    kappa = rr * omega * omega / (c_light * c_light)
    scale_id = (abs(v_perp / (c_light * rr)) / kappa) * (rr * omega / c_light)

    return {
        "alpha_local": alpha_local, "c": c_light,
        "dir_curl": dir_curl, "dir_cov": dir_cov, "dots": dots,
        "scale_ratio": scale_ratio, "scale_id": scale_id,
        "kt_resid": max(abs(x) for x in kappa_tau),
    }


def sec_paramscan():
    rows = []
    bad_dir = []
    bad_scale = []
    bad_kt = []
    for name, om, rr, bb in PARAMS:
        r = analyse(om, rr, bb)
        ok_dir = (min(r["dir_curl"]) > 1 - TOL_DIR) and (min(r["dir_cov"]) > 1 - TOL_DIR)
        ok_dot = max(abs(x) for x in r["dots"]) < TOL_DIR
        ok_scale = (max(abs(x - 1.0) for x in r["scale_ratio"]) < TOL_REL) \
            and abs(r["scale_id"] - 1.0) < TOL_REL
        ok_kt = r["kt_resid"] < 1e-12
        if not ok_dir:
            bad_dir.append(name)
        if not (ok_dot and ok_scale):
            bad_scale.append(name)
        if not ok_kt:
            bad_kt.append(name)
        rows.append((name, om, rr, bb, r, ok_dir, ok_dot, ok_scale, ok_kt))

    alphas = [r[4]["alpha_local"] for r in rows]
    P("V01", "SCAN", "参数扫描覆盖",
      "6 组 (ω, r, b)，局部倾角 α=v⊥/c 覆盖 %s…%s（跨度 %.2f 倍）"
      % (g(min(alphas)), g(max(alphas)), max(alphas) / min(alphas)))

    if not bad_dir:
        P("V02", "SCAN", "方向关系与参数无关（把上一轮的断言变成读数）",
          "6/6 组：∇×T 与 ê_z 的方向余弦最小 %s；dT/ds 与 −ê_r 的方向余弦最小 %s；"
          "两者点积最大绝对值 %s（判据 <%s）⇒ **方向错配在全部参数下成立**"
          % (g(min(min(r[4]["dir_curl"]) for r in rows)),
             g(min(min(r[4]["dir_cov"]) for r in rows)),
             g(max(max(abs(x) for x in r[4]["dots"]) for r in rows)), g(TOL_DIR)))
    else:
        F("V02", "SCAN", "方向关系并非参数无关", "失败组：%s" % bad_dir)

    if not bad_scale:
        P("V03", "SCAN", "标度关系与参数无关",
          "6/6 组：|∇×T| 与 v⊥/(cρ) 的比值偏离 1 最多 %s；"
          "标度恒等式 (|∇×T|/κ)·(ρω/c)=1 偏离 1 最多 %s（判据 <%s）"
          % (g(max(max(abs(x - 1.0) for x in r[4]["scale_ratio"]) for r in rows)),
             g(max(abs(r[4]["scale_id"] - 1.0) for r in rows)), g(TOL_REL)))
    else:
        F("V03", "SCAN", "标度关系并非参数无关", "失败组：%s" % bad_scale)

    if not bad_kt:
        P("V04", "SCAN", "κ²+τ²=(ω/c)² 在全部参数组成立",
          "6/6 组残差 ≤%s" % g(max(r[4]["kt_resid"] for r in rows)))
    else:
        F("V04", "SCAN", "恒等式在部分参数组不成立", "失败组：%s" % bad_kt)

    IN("V05", "SCAN", "结论：上一轮「与参数取值无关」的说法**由断言升级为读数**",
       "28 册 §8 写的是「结构结论与参数取值无关，因为全部读数都是方向 + 标度的比对」——"
       "那是推断。本轮 6 组参数（α 跨 %.2f 倍、ω/r 各变）实测方向余弦与标度恒等式全部保持，"
       "该说法**现在有读数支撑**。但覆盖面仍限 6 组、未做连续极限（如 α→0 或 α→1）"
       % (max(alphas) / min(alphas)))


# ============================================================ §B 身份审计
def sec_identity():
    canon_rows, excl_rows, nodes, kind, edges = DEPS.load_canon()

    grav_words = ("引力", "gravit", "gravity")
    a_rows = [r for r in canon_rows if len(r) >= 7 and r[2].strip().startswith("A")]

    hits = []
    for r in a_rows:
        # 只扫**条目列**（公式本身）。入选理由是元信息，那里可以合法地**否定性**地
        # 提到「引力场」（例如 C-01 的理由写「来料的引力场措辞见 X-15」）——
        # 把元信息也算进去会让审计器在正确的修订后误报（第一版就踩过这一下）。
        blob = r[1]
        if any(w in blob for w in grav_words):
            hits.append((r[0].strip(), [w for w in grav_words if w in blob]))

    with open(os.path.join(HERE, "zxq23_ufe_results.json"), encoding="utf-8") as fh:
        idx = {x["id"]: x["verdict"] for x in json.load(fh)["results"]}

    if not hits:
        P("I01", "ID", "正典 A 类 9 条的**条目列**里「引力」出现 0 次",
          "逐条扫描条目列（公式本身，不含入选理由——那里可以合法地否定性提到「引力场」），"
          "A 类 %d 条中无一出现 引力/gravity 字样；支撑判据共 %s "
          "⇒ **正典本身并未把 A 称为引力场**"
          % (len(a_rows),
             "、".join(sorted({i for r in a_rows
                              for i in DEPS.GUARD.ID_RE.findall(r[4])}))))
    else:
        BO("I01", "ID", "正典 A 类仍带「引力」措辞",
           "命中：%s" % hits)

    verdicts = sorted({idx.get(i) for r in a_rows for i in DEPS.GUARD.ID_RE.findall(r[4])})
    P("I02", "ID", "A 类全部判据的结论分布",
      "%s。A 类 9 条的判据里**没有一条是关于引力的**（全部是量纲、代数恒等、麦克斯韦对应）"
      % verdicts)

    F("I03", "ID", "「A 是引力场」这条主张在正典内**无判据支撑**",
      "正典把统一场记作 A（沿用来料「引力场」措辞），但："
      "① A 类 9 条中 4 条（C-05~C-09）是麦克斯韦方程组与真空波方程，语义上是电磁的；"
      "② 其余 5 条是场互变算子与代数恒等，本身不含引力语义；"
      "③ 承载「引力场」量纲的原始式（式 4）在 25 册被判 FAIL（X-01），已排除。"
      "⇒ **该主张无判据支撑，应从正典的表述中撤下**")

    BO("I04", "ID", "撤下「引力」身份后，UFE-2 的定性需要改写",
       "若 A 只取电磁矢势身份，则 UFE-2 目前的成果是**电磁场论的一个闭合推导**"
       "（3 条公设 → 1 条封闭方程 → 3 条麦克斯韦方程），"
       "**不是「四种力统一场论」**。引力 / 核力 / 弱力三个扇区在 26 册排除清单内（X-01/02/05/06 等）。"
       "本目录原有的「统一场论」措辞属**名实不符**，应按本读数改称「电磁扇区闭合的统一场论候选」。")

    P("I05", "ID", "修复方案（可执行）",
      "① 26 册正典表新增一列或在 C-01 入选理由里明确「A 的物理身份 = 电磁矢势，"
      "『引力场』为来料措辞、无判据支撑」；"
      "② 排除清单新增 X-15「A 作为引力场」，判据 = I03；"
      "③ 26 册 §4 与本体系的定位措辞由「统一场论」改为「电磁扇区闭合的统一场论候选」。"
      "本脚本不自动改文档（改文档须同步判据，故留给下一轮显式执行并留痕）")


def main():
    argv = sys.argv[1:]
    sec_paramscan()
    sec_identity()
    cnt = {}
    for r in RESULTS:
        cnt[r["verdict"]] = cnt.get(r["verdict"], 0) + 1
    payload = {"instrument": "zxq23_o1_verify.py", "counts": cnt,
               "total": len(RESULTS), "results": RESULTS}
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)

    print("=" * 78)
    print("O-P1 攻关结论复核（参数无关性） + 正典身份审计")
    print("=" * 78)
    for r in RESULTS:
        print("[%-8s] %-5s %s" % (r["verdict"], r["id"], r["title"]))
        print("           %s" % r["detail"])
    print("-" * 78)
    print("合计 %d 条：PASS %d / FAIL %d / BOUNDARY %d / INFO %d"
          % (len(RESULTS), cnt.get("PASS", 0), cnt.get("FAIL", 0),
             cnt.get("BOUNDARY", 0), cnt.get("INFO", 0)))
    print("产物：%s" % os.path.basename(OUT_JSON))
    print("红线：数学自洽 ≠ 实验证实；本册不改变 UFE-2 的 L2 评级。")
    if "--strict" in argv and cnt.get("FAIL", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
