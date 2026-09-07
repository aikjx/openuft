# -*- coding: utf-8 -*-
from pathlib import Path
import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "02_shared" / "computation" / "src").is_dir())
sys.path.insert(0, str(ROOT / "02_shared" / "computation" / "src"))
import math
import physics_constants as physics

def zhang_unified_force(v_frac=0.6):
    """张祥前统一力框架核心关系：
        P = m(c - v)        （统一动量）
        dP/dt = F           （统一力 = 动量变化率）
    由此导出的电/磁力比 F_e/F_m = c/v，以及电磁波关系 E = c B。
    本函数：
      (1) 计算在 v = v_frac * c 下的力比 c/v；
      (2) 数值校验真空电磁波 E = c B（由 Maxwell 已证，见 maxwell_wave_relation）。
    诚实边界：这是几何-运动学统一框架的力分解，非实验新预言。
    """
    c = physics.SPEED_OF_LIGHT
    v = v_frac * c
    force_ratio = c / v  # F_e / F_m
    # 电磁波 E = c B 校验
    eps0 = physics.VACUUM_PERMITTIVITY
    mu0 = physics.VACUUM_PERMEABILITY
    c_em = 1.0 / math.sqrt(eps0 * mu0)
    return {
        "v": v, "force_ratio_c_over_v": force_ratio,
        "c_from_em": c_em, "rel_err_c": abs(c_em - c) / c,
    }
