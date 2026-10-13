# -*- coding: utf-8 -*-
"""统一纲领·第一性审计守门工具（GATE-1 ｜ 2026-10-13）
把十二期四线 no-go 纪律固化为可复用守门判据：
  G1.重标度不变性检验（C108 教训）：经典方案若在联合重标度下形式不变 => 无绝对标度 => 自动 FAIL
  G2.L3 独立无量纲预言检验（C125 教训）：无 SM 之外独立无量纲预言 => 自动 FAIL
  G3.对称性定理检验（C121 教训）：单标量场方案 => CM/HLS/WW 自动 FAIL
  G4.实验能标检验（C117 教训）：预言偏差在 42μm/1e-15 已被排除的能标 => 自动 FAIL
输入：候选统一纲领参数（Lagrangian 齐次度 h、自由度类型、新无量纲预言数、偏差能标）
输出：PASS/FAIL 判定 + 证据行。mpmath 250 位。
"""
import mpmath as mp
mp.mp.dps = 250

class Gate:
    def __init__(self, name, h, dof, n_pred, scale, note=""):
        self.name = name
        self.h = h            # 经典 Lagrangian 齐次度（C108 检验点）
        self.dof = dof        # 场自由度类型（scalar/vector/spinor/...）
        self.n_pred = n_pred  # SM 之外独立无量纲预言数（L3 级）
        self.scale = mp.mpf(str(scale))  # 预言偏差特征能标/距离（m）
        self.note = note

    def run(self):
        ok = True
        lines = []
        # G1: 重标度检验——齐次度 h 意味着 L(lam phi)=lam^h L(phi)；h>0 且无 ℏ 引入即无绝对标度
        if self.dof == "scalar" and self.h > 0:
            lines.append("G1 FAIL: 经典标量场齐次度 h=%s>0 => 联合重标度不变 => 无 q0=f(G) 导出（C108 no-go）" % mp.nstr(self.h, 8))
            ok = False
        else:
            lines.append("G1 PASS: 非标量场或含 ℏ 量子化 => 存在内在标度（C108 不适用）")
        # G2: L3 预言检验
        if self.n_pred == 0:
            lines.append("G2 FAIL: 零个 SM 之外独立无量纲预言（L3=0）=> 数值自洽不等于第一性预言（C125）")
            ok = False
        else:
            lines.append("G2 PASS: 独立无量纲预言数=%d（L3 级）" % self.n_pred)
        # G3: 对称性定理
        if self.dof == "scalar":
            lines.append("G3 FAIL: 单标量场 => Coleman-Mandula/HLS/Weinberg-Witten 封死内部规范群/超对称/自旋2引力子（C121）")
            ok = False
        else:
            lines.append("G3 PASS: 非标量自由度 => 对称性定理适用面需个案审查")
        # G4: 实验能标
        eotwash = mp.mpf("42e-6")  # Eöt-Wash 第五力排除尺度（m）
        if self.scale < eotwash:
            lines.append("G4 FAIL: 偏差能标 %s m < 42μm => 第五力已被 Eöt-Wash 排除（C117）" % mp.nstr(self.scale, 8))
            ok = False
        else:
            lines.append("G4 PASS: 偏差能标 %s m >= 42μm（未被 Eöt-Wash 排除；仍需 MICROSCOPE η<=1e-15 复核）" % mp.nstr(self.scale, 8))
        verdict = "PASS" if ok else "FAIL"
        return verdict, lines

# ===== 示范用例 =====
cases = [
    Gate("TUFT（螺旋标量）", mp.mpf("1"), "scalar", 0, mp.mpf("1e-10"), "对照：十二期已终审 falsified"),
    Gate("SM×GR 基准", mp.mpf("0"), "vector+spinor", 2, mp.mpf("1e-3"), "对照：电弱统一已有 Weinberg-Salam 预言"),
    Gate("弦论候选", mp.mpf("0"), "string", 3, mp.mpf("1e-2"), "GUT 尺度质子衰变"),
]
print("===== GATE-1 统一纲领守门工具（250 位）=====")
for c in cases:
    v, ls = c.run()
    print("\n[%s] %s => %s" % (c.name, c.note, v))
    for l in ls:
        print("   " + l)

print("\n===== 结论 =====")
print("TUFT 四门全 FAIL（与十二期终审一致）；候选纲领需 G1-G4 全 PASS 方可进入数值建模。")
print("守门判据来源：C108（重标度）/ C125（L3）/ C121（对称性）/ C117（实验能标）——台账 127 条全定案。")
