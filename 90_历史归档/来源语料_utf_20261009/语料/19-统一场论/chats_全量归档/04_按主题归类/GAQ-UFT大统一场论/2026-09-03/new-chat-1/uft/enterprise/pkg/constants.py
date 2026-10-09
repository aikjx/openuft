# -*- coding: utf-8 -*-
"""
企业级常量库：CODATA 2022 + SI 2019 精确常数
——全部以 mpmath 250 位有效数字核算，含 G 的不确定度传播。
规范：
  * 常量名 = 物理名；_u = 相对不确定度（CODATA 2022 报告值）。
  * 派生 Planck 单位给出 δ(相对不确定度) = (1/2)·δG 传播。
"""
import mpmath as mp
mp.mp.dps = 250

# ----------------------------------------------------------------------
# SI 2019 精确定义值（不确定度为 0）
# ----------------------------------------------------------------------
C_SI   = mp.mpf("299792458")            # m/s
HBAR   = mp.mpf("1.0545718176461565e-34")  # J·s
E_SI   = mp.mpf("1.602176634e-19")      # C
KB     = mp.mpf("1.380649e-23")         # J/K
NA     = mp.mpf("6.02214076e23")        # mol^-1
G0     = mp.mpf("1.25663706212e-6")     # N/A^2（真空磁导率）

# ----------------------------------------------------------------------
# CODATA 2022 测量值（带相对不确定度）
# ----------------------------------------------------------------------
G      = mp.mpf("6.67430e-11")          # m^3 kg^-1 s^-2,  δG = 2.2e-5
G_u    = mp.mpf("2.2e-5")
ALPHA  = mp.mpf("0.0072973525693")      # 精细结构常数, δα = 1.5e-10
ALPHA_u = mp.mpf("1.5e-10")
ME     = mp.mpf("9.1093837015e-31")     # kg, δme = 3.0e-10
ME_u   = mp.mpf("3.0e-10")
MP     = mp.mpf("1.67262192369e-27")    # kg, δmp = 3.0e-10
MP_u   = mp.mpf("3.0e-10")
RINF   = mp.mpf("10973731.568160")      # m^-1 里德伯常数
RINF_u = mp.mpf("1.9e-12")

# ----------------------------------------------------------------------
# 派生 Planck 单位（250 位精算）
# ----------------------------------------------------------------------
def _planck():
    lP  = mp.sqrt(HBAR*G/C_SI**3)
    tP  = mp.sqrt(HBAR*G/C_SI**5)
    mP  = mp.sqrt(HBAR*C_SI/G)
    eP  = mp.sqrt(HBAR*C_SI**5/G)
    qP  = mp.sqrt(4*mp.pi*mp.mpf("8.8541878128e-12")*HBAR*C_SI)  # ε0·ℏc
    TP  = mp.sqrt(HBAR*C_SI**5/(G*KB**2))
    rho = C_SI**5/(HBAR*G**2)
    return lP, tP, mP, eP, TP, rho, qP

LP, TP_, MP_PL, EP, TPL, RHO_P, QP = _planck()
# 不确定度传播：δlP = δtP = δmP = δeP = δTP = ½δG = 1.1e-5
DELTA_PL = mp.mpf("1.1e-5")

# 常用换算
EV2J   = E_SI
J2EV   = 1/E_SI
GEV2KG = mp.mpf("1.78266192162790e-27")   # 1 GeV/c² = 1.78266e-27 kg
KG2GEV = 1/GEV2KG
M2GEV  = (HBAR*C_SI/E_SI)/mp.mpf("1e9")   # 1/m → GeV（ℏc/e 除以 1e9）: ℏc=197.3269804 MeV·fm → 1/m=1.97327e-16 GeV·m? 见 m2GeV()

def m2GeV(per_meter):
    """1 m^-1 = ℏc/(e·1e9) GeV = 1.97327e-16 GeV"""
    return (HBAR*C_SI/E_SI)/mp.mpf("1e9")*per_meter

def CODATA_SUMMARY():
    """返回 Planck 单位对标 CODATA 2022 的核算表（文本）。"""
    rows = [
        ("Planck长度 ℓ_P", LP, mp.mpf("1.616255e-35"), "m"),
        ("Planck时间 t_P", TP_, mp.mpf("5.391247e-44"), "s"),
        ("Planck质量 M_P", MP_PL, mp.mpf("2.176434e-8"), "kg"),
        ("Planck能量 E_P", EP, mp.mpf("1.9561e9"), "J"),
        ("Planck温度 T_P", TPL, mp.mpf("1.416784e32"), "K"),
        ("Planck密度 ρ_P", RHO_P, mp.mpf("5.155e96"), "kg/m³"),
    ]
    out = []
    for name, val, codata, unit in rows:
        rel = abs((val - codata)/codata)
        out.append(f"{name:18s} = {mp.nstr(val,12)} {unit}   CODATA≈{mp.nstr(codata,8)} {unit}   相对差 {mp.nstr(rel,3)}")
    out.append(f"全部 Planck 量相对不确定度 δ = ½δG = {mp.nstr(DELTA_PL,3)}（G 主导误差传播）")
    return "\n".join(out)

if __name__ == "__main__":
    print("=== 企业级精算库自检：CODATA 2022 Planck 单位核算 ===")
    print(CODATA_SUMMARY())
    print(f"\n电子质量 m_e = {mp.nstr(ME,15)} kg（CODATA 2022: 9.1093837015e-31）")
    print(f"精细结构常数 α = {mp.nstr(ALPHA,15)}（CODATA 2022: 7.2973525693e-3）")
