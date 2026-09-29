# -*- coding: utf-8 -*-
"""
================================================================================
TUFT 卷十四 · 主线 A：CMB 拓扑跃迁模型 后验收敛诊断与贝叶斯因子计算
================================================================================

设计稿 / 规划骨架。依赖：numpyro + arviz + jax（仓库既有环境为 numpy + sympy，
新增贝叶斯采样依赖，运行前须确保已安装）。

收敛判据（嵌套采样标准诊断）：
  1) Rhat < 1.05
  2) N_eff (bulk) > 1000
  3) trace plot 无漂移/分层
  4) |logZ 误差| < 0.5

贝叶斯因子 B10 = exp(logZ1 - logZ0)，仅对比现象学 f_NL 阶跃模型，
不是 TUFT 本体公理的证伪。

TODO（未实现占位）：
  - lcdm_cmb_model 依赖 fnl_lcdm / fnl_model（CMB f_NL 预言映射，待落地）
  - reconstruct_rg_trajectory 依赖 integrate_rg（RG 流 ODE，待落地）
================================================================================
"""
from __future__ import print_function

import numpyro
import numpyro.distributions as dist
from numpyro.infer import NestedSampler
import jax.numpy as jnp

try:
    import arviz as az
    HAVE_ARVIZ = True
except Exception:
    HAVE_ARVIZ = False


def diagnostics(ns):
    """承接 numpyro NestedSampler 结果，输出收敛诊断与对数证据。"""
    if not HAVE_ARVIZ:
        raise RuntimeError("arviz 未安装，无法做 Rhat / ESS 诊断")
    idata = az.from_numpyro(ns)
    rhat = az.rhat(idata)
    neff = az.ess_bulk(idata)
    print("Rhat:\n", rhat)
    print("Effective sample size:\n", neff)
    az.plot_trace(idata, compact=True)
    az.plot_posterior(idata)
    logZ = ns.get_log_marginal_likelihood()
    logZ_err = ns.get_log_marginal_likelihood_error()
    print(f"logZ = {logZ:.3f} +/- {logZ_err:.3f}")
    return idata, logZ, logZ_err


def lcdm_cmb_model(obs_l, obs_fnl, obs_sigma=None):
    """ΛCDM 基线模型 M0：无拓扑跳变，仅固定 f_NL。

    TODO: fnl_lcdm / fnl_model 为占位，须先实现 CMB f_NL 预言映射。
    """
    fnl_model = fnl_lcdm  # TODO: 实现
    with numpyro.plate("obs", len(obs_l)):
        numpyro.sample("obs_fnl", dist.Normal(fnl_model, obs_sigma), obs=obs_fnl)


def reconstruct_rg_trajectory(samples):
    """从 t_c 后验样本重建 RG 流轨迹（主线 A.3）。

    TODO: integrate_rg 为占位，须先实现 RG 流 ODE 数值积分。
    """
    t_c_samples = samples["t_c"]
    traj_set = []
    for tc in t_c_samples:
        t_arr, sol = integrate_rg(p=(tc, 0.01, -0.02))  # TODO: 实现
        traj_set.append(sol)
    return t_arr, jnp.array(traj_set)


def bayes_factor(logZ1, logZ0):
    """B10 = exp(logZ1 - logZ0)。"""
    return float(jnp.exp(jnp.asarray(logZ1 - logZ0)))


# ---------------------------------------------------------------------------
# 占位函数（设计稿，运行前必须实现）
# ---------------------------------------------------------------------------
def fnl_lcdm(*args, **kwargs):
    raise NotImplementedError("fnl_lcdm 待实现：CMB f_NL 预言映射")


def integrate_rg(p):
    raise NotImplementedError("integrate_rg 待实现：RG 流 ODE 数值积分")
