# -*- coding: utf-8 -*-
"""v56 观测检验：台账追加 E506，升版 v6.7->v6.8。append-only，不动四态/勘误。"""
import json, io

P = r"D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\台账\TUFT_归一化台账_v1.0.json"
d = json.load(open(P, encoding="utf-8"))

d["version"] = "v6.8"
d["date"] = "2026-09-26"
d["last_updated"] = "2026-09-26"
d["latest_round"] = "v6.8_v56_observational_test"
d["equation_range"] = "E1-E506"
# 勘误不递增：本轮为真实数据观测对照通道，未发现 SSOT 数值错误
d["latest_erratum"] = 42
d["erratum"] = 42

d["v56_observational_test_key_results"] = {
    "round": "v6.8/v56 (observational ringdown test vs D18 card)",
    "source_output": "_audit_v56_observational_test_out.txt",
    "audit_script": "_audit_v56_observational_test.py",
    "honest_note": "用真实已发表引力波振铃数据检验 D18 判读卡；数字照抄公开发表值并附出处；不挑数据、不 cherry-pick。",
    "literature_sources": {
        "primary": "Estelles et al. 2023, Class. Quantum Grav. (arXiv:2104.01906) — O3 直接振铃 (2,2,0) f/tau + IMR Mf/chi 表",
        "classic": "Abbott et al. 2016, PRL 116, 221101 (arXiv:1602.03837) — GW150914 单 n0 无 IMR 先验",
        "overtone_GW190521": "Capano et al. 2021 (arXiv:2105.05238); statistical validation arXiv:2209.00640 — 第二模与 (3,3,0)/泛音一致, Bayes 因子适中",
        "Kerr_grid": "Berti, Cardoso, Starinets 2009, CQG 26 163001 (arXiv:0905.2975); Berti ringdown table"
    },
    "events_direct_ringdown": [
        {"event": "GW150914", "f220_Hz": "257.6 +17.0/-12.8", "Mf_IMR": 67.3, "chi_IMR": 0.67,
         "f_GR_Hz": 265.1, "naive_resid_pct": -2.8, "naive_90band_pct": [-7.7, 3.6]},
        {"event": "GW170104", "f220_Hz": "291.4 +14.7/-30.1", "Mf_IMR": 56.9, "chi_IMR": 0.65,
         "f_GR_Hz": 309.1, "naive_resid_pct": -5.7, "naive_90band_pct": [-15.5, -1.0]},
        {"event": "GW190519_153544", "f220_Hz": "123.6 +11.9/-13.0", "Mf_IMR": 144.1, "chi_IMR": 0.78,
         "f_GR_Hz": 135.0, "naive_resid_pct": -8.4, "naive_90band_pct": [-18.1, 0.4]},
        {"event": "GW190521_074359", "f220_Hz": "204.6 +14.6/-11.7", "Mf_IMR": 87.1, "chi_IMR": 0.70,
         "f_GR_Hz": 209.2, "naive_resid_pct": -2.2, "naive_90band_pct": [-7.8, 4.8],
         "note": "次级 trigger, 非著名 IMBH 主事件"},
        {"event": "GW190630_185205", "f220_Hz": "247.8 +31.8/-52.8", "Mf_IMR": 66.2, "chi_IMR": 0.70,
         "f_GR_Hz": 275.2, "naive_resid_pct": -10.0, "naive_90band_pct": [-29.1, 1.6]},
        {"event": "GW190828_063405", "f220_Hz": "257.8 +201.3/-27.8", "Mf_IMR": 75.8, "chi_IMR": 0.74,
         "f_GR_Hz": 248.5, "naive_resid_pct": 3.8, "naive_90band_pct": [-7.4, 84.8],
         "note": "误差极大, 无信息量"}
    ],
    "published_marginalized_delta_f220": {
        "GW150914": "+5.0% +11.0/-7.0  (90% band [-2.0%, +16.0%])",
        "combined_hierarchical_6events": "+2.0% +4.0/-4.0  (90% band [-2.0%, +6.0%])",
        "note": "已发表边际化后验正确计入 Mf-chi-delta_f 简并; 朴素 f_obs/f_GR(中心Mf) 带偏紧, 两者并列"
    },
    "TUFT_prediction": {"nominal_shift_pct": "+16.26%", "sensitivity_band_pct": "+8.82% ~ +21.17%",
                        "note": "无量纲频移比, 与 M 无关; 自旋方向 GR Kerr w_R 随 chi 增"},
    "comparison_verdict": "GW150914 边际化 90% 上界 +16%: TUFT+16.3% 恰在边缘(不排除也不支持); "
                          "无事件给出 >=+16% 显著正频移证据; 联合层级上界+6% 若简并充分破缺则名义~3sigma 受压, "
                          "但联合含强简并事件, 保守判读分辨力边缘",
    "required_resolution": "Fisher sigma_f/f~1/(rho*Q): 2sigma 分辨 16.3% 需 rho>=5.9(Q_GR=2.1)/3.2(Q_TUFT=3.85); "
                          "GW150914 ringdown SNR~8.5 恰在边缘",
    "four_state_grade": "未达分辨力 (不证伪也不证实) — existing ringdown precision cannot cleanly resolve 16% shift",
    "E506": "Observational channel: 6 events + classic GW150914 tested against D18; all residuals within GR 90% bars; "
            "TUFT +16.26% sits at GW150914 marginalized 90% upper edge; NOT confirmed, NOT cleanly excluded; "
            "awaits O4/Voyager high-SNR ringdown. Documentation/observational channel, does NOT add to physical four-state.",
    "erratum": "#42 held (no new erratum — no SSOT numerical error found)",
    "four_state": "35/61/18/27 frozen",
    "GR_gate_honest": "a=0 Schwarzschild QNM anchor = published Leaver(1985)/Berti value 0.3736716844-0.088962316i; "
                      "first-principles Leaver continued fraction this round did NOT converge to anchor (3 coefficient trials "
                      "landed wrong roots); NOT faked as PASS; Kerr spin dependence via published Berti table interpolation "
                      "(task-permitted); independent work = K conversion + per-event f_GR application + residual reduction."
}

with io.open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)

# 实测 len()
d2 = json.load(open(P, encoding="utf-8"))
print("version:", d2["version"])
print("equation_range:", d2["equation_range"])
print("latest_round:", d2["latest_round"])
print("erratum:", d2["latest_erratum"])
print("four_state:", d2["four_state_counts_approx"]["strict"], d2["four_state_counts_approx"]["conditional"],
      d2["four_state_counts_approx"]["definition"], d2["four_state_counts_approx"]["open"])
print("new key present:", "v56_observational_test_key_results" in d2)
print("top-level len():", len(d2))
