# -*- coding: utf-8 -*-
# V9.35/36 单方程 vs SM 拉氏量逐项对照（Windows 主全书复算版）
import json, math

out = {}

A = {
    "L_SM 六项": {
        "A1 规范动能": "-1/4 F^a F^a（SU(3)xSU(2)xU(1)：8+3+1=12 规范玻色子）",
        "A2 费米子动能+耦合": "i psi_bar gamma^mu D_mu psi（3 代 x 15 Weyl=90 实分量）",
        "A3 Higgs 动能": "|D_mu H|^2（4 实分量）",
        "A4 Higgs 势": "V(H)=mu^2|H|^2+lambda|H|^4（SSB v=246 GeV）",
        "A5 Yukawa": "y_f psi_bar psi H",
        "A6 规范质量+混合": "m_W=g2 v/2、m_Z=m_W/cos(theta_W)、sin^2W=g1^2/(g1^2+g2^2)",
    },
    "TUFT 对应物": "无规范场/无旋量/无 Higgs/质量全外输/无混合角（1 标量势+参数表）",
    "A_verdict": "SM 场内容 106+EC24+度规10=140 实分量 vs TUFT 1 标量势+参数表。",
}
out["A"] = A

alpha = 0.0072973525693
sin2W = 0.22337
cos2W = 1-sin2W
e = math.sqrt(4*math.pi*alpha)
g2 = e/math.sqrt(sin2W)
g1 = e/math.sqrt(cos2W)
v = 246.22
mW = g2*v/2.0
mZ = mW/math.sqrt(cos2W)
alpha_e = g2*g2*sin2W/(4*math.pi)
yt = math.sqrt(2.0)*172.69/v
B = {
    "SM 内生量": {
        "g1": "%.4f" % g1, "g2": "%.4f" % g2,
        "m_W (tree)": "%.2f GeV" % mW, "m_Z (tree)": "%.2f GeV" % mZ,
        "m_W/m_Z = cos(theta_W)": "%.4f vs PDG 0.8814（偏差 %.2f%%）" % (mW/mZ, abs(mW/mZ-0.8814)/0.8814*100),
        "alpha_e 回代": "%.6f (=PDG 恒等)" % alpha_e,
        "y_t": "%.3f" % yt,
    },
    "TUFT 外输": "m_W/alpha/m_f/sin^2W 全部输入（B02/B03）",
    "B_verdict": "SM 以 alpha/sin^2W/v 导出 m_W/m_Z（tree 级，辐射修正 δr≈1.9% 后 pole 80.377/91.19；比值偏差 0.02%）；TUFT 全外输。",
}
out["B"] = B

C = {
    "八维矩阵": {
        "场内容": "140 vs 1（SM 多 139）",
        "对称性": "局域 SU(3)xSU(2)xU(1) vs 全局旋转",
        "力机制": "规范玻色子交换（V-A/自旋/手征）vs 标量 Yukawa（仅径向）",
        "力程来源": "Higgs 内生（g*v/2）vs lambda=hbar/mc 外输",
        "力强来源": "g1,g2,g3 跑动 vs q_i 外输",
        "质量谱": "Yukawa 内生 vs 全外输",
        "混合角": "sin^2W 内生 vs 无",
        "判别性预言": "有 vs 0 类（V9.33）",
    },
    "约化路径": "SM 单玻色子交换树图+静态源+非相对论极限 = Yukawa/库仑势（TUFT 单方程）",
    "C_verdict": "TUFT 单方程 = SM 低能极限势形层严格子集；SM 拥有 TUFT 缺失的规范-旋量-Higgs 层。",
}
out["C"] = C

D = {
    "子集关系": "PASS：TUFT 单方程 ⊆ SM 低能静态源极限势形层",
    "缺失层": "FAIL：SM 规范-旋量-Higgs 内生层 TUFT 全缺失（与 V9.31 F2-F5 FAIL 一致）",
    "新预言": "0（V9.33）",
    "D_verdict": "单方程封闭式是 SM 低能势形层的参数化投影：形式统一成立，TUFT 只能作 SM 低能极限参数字典（V9.22）。",
}
out["D"] = D

out["summary"] = ("V9.35/36 SM 对照：SM 六项 140 实分量 vs TUFT 1 标量势；SM 以 alpha/sin^2W/v 导出 m_W/m_Z（比值偏差 0.02%）、"
                  "TUFT 全外输；八维矩阵全列差异；约化路径=SM 单玻色子交换树图极限=Yukawa 势。判定：子集 PASS；SM 内生层缺失 FAIL；新预言 0。")

with open(r"D:\a10\aikjx\code\my_lib\tuft_v113_sm_lagrangian_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("g1=%.4f g2=%.4f mW=%.2f mZ=%.2f ratio=%.4f yt=%.3f" % (g1, g2, mW, mZ, mW/mZ, yt))
print("saved json ok")
