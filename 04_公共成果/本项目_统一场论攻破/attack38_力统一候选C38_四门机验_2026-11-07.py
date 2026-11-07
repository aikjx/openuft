# -*- coding: utf-8 -*-
# attack38 / 攻破㉚ —— 力统一构造性候选 C38 的 four-gate 机验（一个真预言、四道门、诚实负判）
# 承接 attack20 留下的「常数统一 OPEN」债：把「秩=时空维＋手征二分」判据提升为公设（候选 C38），
# 要求三规范耦合一圈无自由阈值汇合，交出无自由参数的可证伪预言 sin²θ_W(M_Z)，过 Ω5/K4/K5/M1 四门。
# 数值内核独立重推 attack28 的真预测闭式（S0 控制组逐位核对），新内容在候选 framing＋四门审计＋原创裁定。
# 红线：教科书级 RGE 复算＋一个未公理化的提升公设 ⇒ 原创第一性供给=0；C38 作为「攻破」判负；0/22、UFT-3=0 不变。
import os, sys, json
from mpmath import mp, mpf, pi, log, e
mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
ENTRIES = []
def add(uid, claim, verdict, reading):
    ENTRIES.append({"id": uid, "claim": claim, "verdict": verdict, "reading": reading})
    print("[%-9s] %s | %s" % (verdict, uid, claim))
    print("            读数: %s" % reading)
def ns(x, n=10): return mp.nstr(x, n)
print("== attack38 攻破㉚·力统一候选 C38 四门机验 ==")

# ---------- 登记输入（外部 PDG 口径，与 attack28 同）----------
MZ = mpf('91.1876'); MSUSY = mpf('1000')           # M_SUSY 是 MSSM 支的自由输入（Ω5 计数）
alpha_em = mpf(1)/mpf('127.916'); alpha_s = mpf('0.1184')
SW_OBS = mpf('0.23122')                            # 仅最后比对，不进入求解
A_SM = (mpf(41)/10, -mpf(19)/6, mpf(-7))           # SM 一圈 β（GUT 归一化 b1）
B_MSSM = (mpf(33)/5, mpf(1), mpf(-3))              # MSSM 一圈 β
print("-- 候选 C38 公设：规范群秩=时空维 4 ＋ 手征双态⊕单态（attack20 判据提升为公设）＋三耦合一圈汇合 --")
print("-- 输入：alpha_em^-1=127.916, alpha_s=0.1184, M_Z=91.1876；sin²θ_W=0.23122 仅比对 --")

def predict(A, Bm, L1v, a_em=alpha_em, a_s=alpha_s, gut_norm=mpf(5)/3):
    # 两段跑动：M_Z --(A,L1)--> M_SUSY --(Bm,L2)--> M_GUT；sin²θ_W 为未知量
    b1, b2, b3 = A
    B1, B2, B3 = Bm
    # 消去 x 的组合 C=(a2^-1-a3^-1)+(5/3)(a1^-1-a3^-1)：C(M_Z)=1/a_em-(1+gut_norm)/a_s，C(M_GUT)=0
    coef_L1 = (b2-b3) + gut_norm*(b1-b3)
    coef_L2 = (B2-B3) + gut_norm*(B1-B3)
    rhs = 1 - (1+gut_norm)*a_em/a_s                # gut_norm=5/3 ⇒ 1-(8/3)alpha_em/alpha_s
    L2 = ((2*pi/a_em)*rhs - coef_L1*L1v)/coef_L2
    x = a_em*(1/a_s + ((b2-b3)*L1v + (B2-B3)*L2)/(2*pi))
    return x, L2

# ---------- S0 控制组：独立重推须逐位复现 attack28 登记值 ----------
L1 = log(MSUSY/MZ)
x_sm, L2_sm = predict(A_SM, A_SM, mpf(0))
x_mssm, L2_m = predict(A_SM, B_MSSM, L1)
mgut_sm = MZ*e**L2_sm; mgut_mssm = MSUSY*e**L2_m
dev_sm = abs(x_sm-SW_OBS)/SW_OBS*100; dev_mssm = abs(x_mssm-SW_OBS)/SW_OBS*100
REF_SM = mpf('0.20744763'); REF_MSSM = mpf('0.2289256')   # attack28 report 逐字
s0 = (abs(x_sm-REF_SM) < mpf('1e-7')) and (abs(x_mssm-REF_MSSM) < mpf('1e-6'))
add("S0","控制组：独立重推闭式逐位复现 attack28 登记预测（SM 0.20744763 / MSSM 0.2289256）","PASS" if s0 else "FAIL",
    "SM x=%s（Δ vs attack28=%.2e）；MSSM x=%s（Δ=%.2e）；M_GUT SM=%s MSSM=%s GeV"%(ns(x_sm),abs(x_sm-REF_SM),ns(x_mssm),abs(x_mssm-REF_MSSM),ns(mgut_sm,8),ns(mgut_mssm,8)))

# ---------- S1 / K4：低能预言对实验 ----------
add("S1a","K4·SM 支：无自由参数预言 sin²θ_W 对实验 0.23122","FAIL" if dev_sm>5 else "PASS",
    "SM 预言 x=%s，偏差 %.4f%%（>5%% ⇒ 被排除；教科书标准结论）"%(ns(x_sm),dev_sm))
add("S1b","K4·MSSM 支：预言 sin²θ_W 对实验（但 M_SUSY=1000 为自由输入）","BOUNDARY" if dev_mssm<5 else "FAIL",
    "MSSM 预言 x=%s，偏差 %.4f%%（<5%% 相容；但相容性依赖自由 M_SUSY，见 S2）"%(ns(x_mssm),dev_mssm))

# ---------- S2 / Ω5：参数计数门 n_free ≤ n_obs−1 ----------
# SM 支作为预言：n_free=0（alpha_em,alpha_s 为测量输入非旋钮；群由公设固定），n_obs=1（sin²θ_W）=> 0<=0 PASS（但 K4 错）
# MSSM 支：n_free=1（M_SUSY），n_obs=1 => 1<=0 FAIL
# 提升公设「秩=时空维」本身：未被更深原理导出，计 +1 自由公设（M1 计）
nfree_sm, nobs = 0, 1
nfree_mssm = 1
gate_sm = nfree_sm <= nobs-1
gate_mssm = nfree_mssm <= nobs-1
add("S2","Ω5 参数计数门 n_free≤n_obs−1（n_obs=1 sin²θ_W）","FAIL" if not gate_mssm else "PASS",
    "SM 支 n_free=%d≤%d PASS（但 K4 错）；MSSM 支 n_free=%d（M_SUSY）≤%d ⇒ %s；提升公设另计 +1 自由公设（未导出）"%(nfree_sm,nobs-1,nfree_mssm,nobs-1,"PASS" if gate_mssm else "FAIL"))

# ---------- S3 / K5：可证伪性（预言随输入变化，非恒等/非往返）----------
sens = []
for f in ['0.95','1.0','1.05']:
    xs,_ = predict(A_SM, B_MSSM, L1, a_s=alpha_s*mpf(f))
    sens.append((f, xs))
spread = max(s[1] for s in sens)-min(s[1] for s in sens)
s3 = spread > mpf('1e-4')
add("S3","K5 可证伪：α_s±5% 时预言移动（非恒等、非输入往返）","PASS" if s3 else "FAIL",
    "α_s×{0.95,1.0,1.05} → x={%s}；跨度 %s（>1e-4 ⇒ 有判别力；与 attack28 P3 同族）"%(", ".join(ns(s[1],8) for s in sens), ns(spread,6)))

# ---------- S4 / M1：原创第一性供给 ----------
# C38 公设 = attack20 判据（已登记）的提升；数值预言 = 1981 教科书 RGE。两者均非新第一性原理。
add("S4","M1 原创门：C38 是否给出新的第一性唯一选择原理","FAIL",
    "公设=attack20『秩=时空维＋手征二分』判据的未公理化提升（『为何秩=4』仍无出处）；预言=教科书一圈 RGE（attack28 已登记）⇒ 原创第一性供给=0")

# ---------- 守卫（仪器有牙）----------
print("-- 守卫 --")
# G10 翻 b1 符号 → SM 预言必须移动（读的是 β 不是常数）；SM 单段预言读高能段 B1，故翻 Bm 的 b1
x_g10,_ = predict(A_SM, (-A_SM[0], A_SM[1], A_SM[2]), mpf(0))
g10 = abs(x_g10-x_sm) > mpf('1e-3')
print("[%s] G10 翻 b1 符号：SM 预言 %s → %s（移动 %.2e >1e-3 ⇒ 读 β）"%("OK" if g10 else "BAD", ns(x_sm,8), ns(x_g10,8), abs(x_g10-x_sm)))
# G11 撤 GUT 归一化 5/3→1 → 预言必须移动（读的是归一化）
x_g11,_ = predict(A_SM, A_SM, mpf(0), gut_norm=mpf(1))
g11 = abs(x_g11-x_sm) > mpf('1e-3')
print("[%s] G11 撤 5/3 归一化：SM 预言 %s → %s（移动 %.2e >1e-3 ⇒ 读归一化）"%("OK" if g11 else "BAD", ns(x_sm,8), ns(x_g11,8), abs(x_g11-x_sm)))
# G12 扫 M_SUSY → MSSM 预言必须随自由旋钮变化（坐实 M_SUSY 是自由参数非导出）
xs_ms = []
for ms in ['200','1000','5000']:
    L1v = log(mpf(ms)/MZ); xv,_ = predict(A_SM, B_MSSM, L1v); xs_ms.append(xv)
spread_ms = max(xs_ms)-min(xs_ms)
g12 = spread_ms > mpf('1e-4')
print("[%s] G12 扫 M_SUSY∈{200,1000,5000}：MSSM 预言跨度 %s（>1e-4 ⇒ M_SUSY 是自由旋钮，Ω5 计数成立）"%("OK" if g12 else "BAD", ns(spread_ms,6)))
guards_ok = bool(g10 and g11 and g12)

# ---------- 候选总裁定 ----------
candidate_verdict = "FAIL"   # K4(SM 错) + Ω5/M1(MSSM 自由参数＋ borrowed) ⇒ 不构成攻破
from collections import Counter
cnt = Counter(x["verdict"] for x in ENTRIES)
print("== 汇总：条目 %d；%s；守卫 %d/3 ==" % (len(ENTRIES), " / ".join("%s %d"%(k,v) for k,v in sorted(cnt.items())), sum([g10,g11,g12])))
print("== 候选 C38 总裁定：%s（作为『攻破力的统一场论』）==" % candidate_verdict)
print("   理由：SM 支无自由参数但预言错（K4 偏 %.2f%%）；MSSM 支相容但 M_SUSY 自由（Ω5 FAIL）＋公设未公理化（M1 FAIL）。" % dev_sm)
print("   净增量：把 attack20『常数统一 OPEN』债以精确负读数闭合——提升判据为公设并不带来一个被验证的无参数力预言。")
print("红线：教科书 RGE 复算＋未导出公设 ⇒ 原创第一性供给=0；PASS（S0/S3）是仪器有效，不迁移为物理成立、不计攻破数；0/22、UFT-3=0、L3=0 不变。")
out = {"round":"attack38_攻破㉚力统一候选C38四门机验","date":"2026-11-07","entries":ENTRIES,"summary":dict(cnt),
       "candidate":"C38","candidate_verdict":candidate_verdict,
       "guards":{"G10_flipb1":bool(g10),"G11_dropnorm":bool(g11),"G12_scanMSUSY":bool(g12)},
       "readings":{"x_sm":str(x_sm),"x_mssm":str(x_mssm),"dev_sm_pct":str(dev_sm),"dev_mssm_pct":str(dev_mssm),
                   "mgut_sm":str(mgut_sm),"mgut_mssm":str(mgut_mssm),"S3_spread":str(spread),"G12_spread":str(spread_ms)},
       "exit":0 if (guards_ok and s0) else 2}
json.dump(out, open(os.path.join(HERE,"attack38_力统一候选C38_四门机验_2026-11-07.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
sys.exit(out["exit"])