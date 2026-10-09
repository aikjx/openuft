# -*- coding: utf-8 -*-
# TUFT V3.4 RG 审计续链：D3 (κ+τc 量纲非法) 的 R1 零成本合法化
# 机器核验两种零成本归一形式 + 重推 β_G 量纲。
# 纯标准库；质量维 (L, M, T)。
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

OUT = "d:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化/数据/TUFT_V34_RG_κ+τc_量纲合法化_R1_2026-10-07.json"

L, M, T = (1, 0, 0), (0, 1, 0), (0, 0, 1)

def add(a, b):
    return tuple(x + y for x, y in zip(a, b))

def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))

def mul(a, b):
    return tuple(x + y for x, y in zip(a, b))

def same(a, b):
    return a == b

def dim_str(a):
    parts = []
    for name, e in (("L", a[0]), ("M", a[1]), ("T", a[2])):
        if e != 0:
            parts.append(name + ("" if e == 1 else ("^%d" % e)))
    return "·".join(parts) if parts else "无量纲(1)"

PR = []  # 判定记录

def P(ok, name, info):
    PR.append({"check": name, "pass": bool(ok), "info": info})
    print(("PASS " if ok else "FAIL ") + name + " :: " + info)

# 基本量纲（与判定册 / 第十九轮一致）
kappa = (-1, 0, 0)      # [κ] = L^-1  (弧长倒数，v_eq_c 第7层已冻结)
tau = (-1, 0, 0)        # [τ] = L^-1
c = (1, 0, -1)          # [c] = L T^-1
G = (3, -1, -2)         # [G] = L^3 M^-1 T^-2
tauc = mul(tau, c)      # [τc] = T^-1

P(not same(kappa, tauc), "D3_RAW_MISMATCH",
  "κ+τc : [%s] + [%s] 不同维 => 加法无定义（确认 D3 缺陷存在）" % (dim_str(kappa), dim_str(tauc)))

# ---- R1 零成本合法化：用既有常数 c 把其中一项归一 ----
# 选项 R1a：给 κ 补一个 c -> κc + τc，两项均为 T^-1
kappac = mul(kappa, c)  # [κc] = T^-1
P(same(kappac, tauc), "R1a_HOMOGENEOUS",
  "R1a κc+τc : [%s] + [%s] 同维(T^-1) => 合法可加" % (dim_str(kappac), dim_str(tauc)))

# 选项 R1b：给 τc 除一个 c -> κ + τc/c = κ + τ，两项均为 L^-1
tauc_over_c = sub(tauc, c)  # [τc/c] = L^-1
P(same(tauc_over_c, kappa), "R1b_HOMOGENEOUS",
  "R1b κ+τc/c = κ+τ : [%s] + [%s] 同维(L^-1) => 合法可加" % (dim_str(kappa), dim_str(tauc_over_c)))

# ---- 重推 β_G = G*(4β_c/c − β_{κτ}/(κ+τc)) 量纲 ----
# 选 R1a 分母 κc+τc；须显式声明跑动参数量纲（原稿缺此声明，同 D4 性质）：
#   β_c 取速度维（c 的跑动），β_{κτ} 取 T^-1。
beta_c = c                 # [β_c] = L T^-1
beta_ktaut = (0, 0, -1)   # [β_{κτ}] = T^-1
denom = kappac            # R1a 分母已合法，齐次 T^-1

term1 = sub(beta_c, c)    # β_c/c : 速度 / 速度 = 无量纲
term2 = sub(beta_ktaut, denom)  # β_{κτ}/(κc+τc) : T^-1 / T^-1 = 无量纲
P(same(term1, (0, 0, 0)) and same(term2, (0, 0, 0)), "BETA_G_DIMS",
  "β_G = G*(4β_c/c − β_{κτ}/(κc+τc)) : 两项均无量纲 => [β_G]=[G]=%s（合法）" % dim_str(G))

# 反向体检：若原稿分母 κ+τc 直接代入 β_G，第二项量纲
bad_term2 = sub(beta_ktaut, add(kappa, tauc))
P(not same(bad_term2, (0, 0, 0)), "BETA_G_RAW_ILLEGAL",
  "原稿 β_{κτ}/(κ+τc) : [%s] / [%s] = [%s] ≠ 无量纲 => 原 β_G 分母非法（须先修 D3）"
  % (dim_str(beta_ktaut), dim_str(add(kappa, tauc)), dim_str(bad_term2)))

n_pass = sum(1 for p in PR if p["pass"])
result = {
    "script": "TUFT_V34_RG_κ+τc_量纲合法化_R1_2026-10-07.py",
    "rating": "C/L1",
    "self_check": "%d/%d" % (n_pass, len(PR)),
    "checks": PR,
    "options": {
        "R1a": "κc+τc（两项 T^-1），零成本，仅给 κ 补既有 c",
        "R1b": "κ+τ（两项 L^-1），零成本，即 τc 除 c（=τ）",
        "R2": "声明 κ 为定值场并删 §5（结构性，未实现）",
        "R3": "走 ECSK ½g_ττ R（代价 +2 自由参数，违反 Ω5，未实现）",
    },
    "residual": "R1 仅使分母合法；β_c、β_{κτ} 量纲仍须显式声明（同 D4 性质），否则 β_G 数值不可信",
    "next": "待用户裁决 R1a / R1b / R2 / R3 后，方可把 β_G 写回修订稿",
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("SELF_CHECK %d/%d  EXIT_%s" % (n_pass, len(PR), "0" if n_pass == len(PR) else "1"))
sys.exit(0 if n_pass == len(PR) else 1)
