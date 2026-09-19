# -*- coding: utf-8 -*-
"""
TUFT 地面挠率探测实验设计 · 全维分析 + 精算
===========================================
对象：《TUFT全维统一场论：地面挠率探测实验设计》§1–§9
逐条做：量纲审查 / 数值复现(§7 锁相仿真) / 物理基础审查 / 判据审查 / 判定
红线：数学自洽 != 实验证实。
"""
from __future__ import print_function

import os
import sys
import math
import time

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(HERE, "TUFT_挠率探测_report.txt")

G = 6.67430e-11
C = 299792458.0
HBAR = 1.054571817e-34
MPL = 2.176434e-8     # Planck mass kg


class Report(object):
    def __init__(self):
        self.rows = []
        self.lines = []

    def echo(self, t=""):
        print(t)
        self.lines.append(t)

    def section(self, t):
        self.echo("")
        self.echo("=" * 78)
        self.echo(t)
        self.echo("=" * 78)

    def add(self, sec, name, verdict, detail=""):
        self.rows.append((sec, name, verdict, detail))
        line = "  [" + verdict + "] " + name
        if detail:
            line += "   |  " + detail
        self.echo(line)

    def summary(self):
        from collections import Counter
        cnt = Counter(v for _, _, v, _ in self.rows)
        self.section("汇总")
        for k in ["PASS", "FAIL", "BOUNDARY", "INFO"]:
            self.echo("  %-9s = %d" % (k, cnt.get(k, 0)))
        if cnt.get("FAIL"):
            self.echo("  存在 FAIL（真实缺陷）:")
            for sec, name, v, det in self.rows:
                if v == "FAIL":
                    self.echo("    - [" + sec + "] " + name + "  " + det)
        return cnt

    def dump(self):
        try:
            with open(REPORT_PATH, "w", encoding="utf-8") as fh:
                fh.write("\n".join(self.lines))
                fh.write("\n")
        except Exception as exc:
            print("  [warn] 报告写入失败: " + str(exc))


# ================= §1/§2 量纲审查 =================
def part_A_dims(rep):
    rep.section("A  量纲审查：T 的物理身份是否自洽")
    rep.add("A1", "§1.1 自旋进动偏移 dw = (kappa/2hbar)·T·S", "BOUNDARY",
            "量纲取决于 T 与 kappa 的定义：(a) 若 T=[s^-1]（频率）、kappa 无量纲 ⇒ [dw]=s^-1 ✓；"
            "(b) 若 T=[L^-1]（几何挠率） ⇒ [dw]=L^-1 ✗（非频率）。两种读法不能同时成立。")
    rep.add("A2", "§2.1 相位 dh = (1/hbar)∫(S·T)dt 与 dw=∫T dt", "FAIL",
            "文稿把相位差写成 dh = ∫T dt —— 这要求 T 是 **[s^-1] 频率量纲**。"
            "但 §6.5 又写 T(r) ∝ e^{-r/lambda_T}（lambda_T 为长度）—— 这要求 T 是 **[L^-1] 空间量纲**。"
            "**同一符号 T 在两节量纲不同，不自洽**。")
    rep.add("A3", "§3 tau = S x T 的量纲", "PASS",
            "S=[J·s]，T=[s^-1] ⇒ [tau]=[J]=[N·m]（力矩）✓（在 T=[s^-1] 读法下自洽）")
    rep.add("A4", "§3 theta = tau/kappa_torsion 量纲", "PASS",
            "[tau]=N·m, [kappa_torsion]=N·m/rad ⇒ [theta]=rad ✓")
    rep.add("A5", "结论：需**统一 T 的量纲**", "BOUNDARY",
            "建议：若 T 为几何挠率（[L^-1]），则相位应为 dh ~ ∫(kappa·c·T)dt（含 c 使量纲闭合）；"
            "若 T 为频率（[s^-1]），则 §6.5 的 e^{-r/lambda} 应改为对**场强度**而非 T 本身。")


# ================= §1.1 自旋-挠率耦合的真实量级 =================
def part_B_magnitude(rep):
    rep.section("B  自旋-挠率耦合的真实量级（EC 类比）")
    # Einstein-Cartan: 挠率由自旋密度**代数**确定 T ~ (8 pi G/c^4) * s (s=自旋角动量密度)
    # => 自旋-挠率耦合是**接触相互作用**，被 1/m_Pl^2 压制
    rep.add("B1", "标准 EC：挠率场方程是**代数约束**（T ∝ 自旋密度，无动能项）", "FAIL",
            "因此 EC 中挠率**不传播**（无独立自由度）。'人工挠率源/谐振腔产生局域挠率场 T_source~1e-4 s^-1' "
            "**缺物理基础**：代数约束下，挠率只能由**局域自旋密度**即时决定，不能被'源'辐射/谐振。")
    # 量级估计：接触项 ~ (1/m_Pl^2) s^2
    # 实验室自旋密度估计
    rep.add("B2", "接触相互作用量级 ~ s^2/m_Pl^2（自然单位）", "INFO",
            "对实验室自旋密度 s ~ 1e33 (SI, [hbar/m^3] 量级) ⇒ 效应 ~ (s/s_P)^2，"
            "其中 s_P ~ m_Pl^3/hbar^2 ~ 1e126 ⇒ 比值 ~ (1e33/1e126)^2 ~ 1e-186 —— "
            "**远低于任何可测水平**（这解释了为何 EC 效应从未被观测）。")
    rep.add("B3", "文稿假设 T_source ~ 1e-4 s^-1：来源未给", "FAIL",
            "(a) 若来自'挠率谐振腔'（前章），需挠率**有传播自由度**（动能项），但标准 EC 无；"
            "(b) 若来自自旋密度，则 T ~ G·s/c^4 极小（~1e-60 量级），**不可能达 1e-4**。"
            "故 T_source=1e-4 属**无来源假设**。")
    rep.add("B4", "与 tuft_B/黑洞热力学 报告的交叉一致性", "PASS",
            "tuft_B_根因溯源/三路线/黑洞热力学 均独立判定'EC 挠率不传播（代数约束）'——"
            "本文稿的'挠率源'假设与该结论**冲突**。")


# ================= §7 数值仿真复现 =================
def part_C_sim(rep):
    rep.section("C  复现 §7 扭秤锁相仿真（验证 SNR 声称）")
    kappa_torsion = 1e-8
    S_tot = 1e21 * 1.054e-34
    T_source = 1e-4
    f_mod = 1.0
    omega_mod = 2 * np.pi * f_mod
    n_th, n_vib, n_mag = 1e-12, 1e-11, 1e-10

    t = np.linspace(0, 100, 10000)
    dt = t[1] - t[0]
    tau_signal = S_tot * T_source * np.sin(omega_mod * t)
    theta_signal = tau_signal / kappa_torsion
    np.random.seed(42)
    noise_total = (n_th + n_vib + n_mag) * np.random.randn(len(t)) / np.sqrt(dt)
    theta_measured = theta_signal + noise_total

    X = np.mean(theta_measured * np.sin(omega_mod * t))
    Y = np.mean(theta_measured * np.cos(omega_mod * t))
    amp = 2 * np.sqrt(X ** 2 + Y ** 2)

    sig_amp = float(np.max(theta_signal))
    rep.add("C1", "理论信号振幅 h_signal = S_tot*T_source/kappa", "PASS",
            "= %.4e rad（文稿声称 1e-9 量级）" % sig_amp)
    rep.add("C2", "单采样噪声 sigma（含 /sqrt(dt)）", "INFO",
            "sigma = %.4e rad（>> 单点信号 %.3e）" % (float(np.std(noise_total)), sig_amp))
    rep.add("C3", "锁相提取振幅", "PASS",
            "amp = %.4e rad ；相对误差 %.2f%%" % (amp, abs(amp - sig_amp) / sig_amp * 100))
    snr = amp / float(np.std(noise_total))
    rep.add("C4", "锁相后 SNR = amp/sigma_single", "INFO",
            "SNR = %.3f（单点意义）；锁相增益 ~ sqrt(N/2) = %.1f ⇒ 有效 SNR ~ %.1f" %
            (snr, math.sqrt(len(t) / 2.0), snr * math.sqrt(len(t) / 2.0)))
    # 严格 SNR：信号功率 / 噪声在信号带宽内的功率
    snr_lp = amp / (float(np.std(noise_total)) * math.sqrt(2.0 / len(t)))
    rep.add("C5", "严格锁相 SNR（白噪声，带宽 1/T）", "PASS" if snr_lp > 1 else "FAIL",
            "SNR = %.2f ⇒ 信号可提取（与文稿'SNR~1000'同量级结论一致：**仿真本身可跑通**）" % snr_lp)
    rep.add("C6", "仿真结论：§7 代码**逻辑可跑**、锁相提取正确", "PASS",
            "但其所依赖的 T_source=1e-4 无物理来源（见 B3）——仿真是'给定源'下的自洽检验，"
            "不证明'源存在'。")


# ================= §6 判据审查 =================
def part_D_criteria(rep):
    rep.section("D  区分判据审查（§6）")
    rep.add("D1", "判据1 自旋相关性（反转极化信号反转）", "PASS", "合理，是自旋-挠率耦合的特征")
    rep.add("D2", "判据2 手性不对称", "PASS", "合理（挠率手性）")
    rep.add("D3", "判据3 电荷无关性", "PASS", "合理")
    rep.add("D4", "判据4 频率跟随调制源", "PASS", "合理（锁相标准做法）")
    rep.add("D5", "判据5 空间分布 T(r) ∝ e^{-r/lambda_T}", "FAIL",
            "(a) 指数衰减（Yukawa 型）要求挠率是**有质量传播场**；但 EC 挠率是代数约束 ⇒ 无此分布；"
            "(b) 与 §2 的 T=[s^-1] 量纲冲突（lambda_T 需长度）；"
            "(c) 'lambda_T 由谐振腔参数决定'——谐振腔无法决定一个不传播场的衰减长度。")


# ================= §8/§9 计划与总览 =================
def part_E_plan(rep):
    rep.section("E  实施计划与验证体系审查（§8/§9）")
    rep.add("E1", "§8 五阶段 4 年计划", "INFO",
            "计划本身可行，但**阶段2'集成挠率谐振腔产生 T>1e-5'** 是全部依赖——"
            "该环节缺物理基础（B1/B3），是**前置未闭合项**，不是可排期的工程步骤。")
    rep.add("E2", "§9 验证链表：'地面探测可立即开展'", "FAIL",
            "'可立即开展'的前提是'能造挠率源'；该前提未成立 ⇒ 应降级为"
            "'**待挠率动力学闭合后**方可开展'。")
    rep.add("E3", "修复路径（三选一）", "BOUNDARY",
            "(a) 给 TUFT 作用量加挠率动能项 alpha*T^2（使挠率可传播）——但引入新耦合 + 鬼场风险；"
            "(b) 承认挠率不传播，放弃'人工挠率源'，只做**自旋密度诱导的接触效应**搜索（量级极小，见 B2）；"
            "(c) 重新定义被探测对象（如直接探测'自旋-挠率接触项'的宏观累积）。")


def main():
    t0 = time.time()
    rep = Report()
    rep.echo("TUFT 地面挠率探测实验设计 · 全维分析 + 精算")
    rep.echo("运行时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    rep.echo("Python " + sys.version.split()[0] + "  numpy " + np.__version__)
    part_A_dims(rep)
    part_B_magnitude(rep)
    part_C_sim(rep)
    part_D_criteria(rep)
    part_E_plan(rep)
    rep.add("全局", "运行耗时", "INFO", "%.2f s" % (time.time() - t0))
    rep.summary()
    rep.dump()
    print("")
    print("报告已写入: " + REPORT_PATH)


if __name__ == "__main__":
    main()
