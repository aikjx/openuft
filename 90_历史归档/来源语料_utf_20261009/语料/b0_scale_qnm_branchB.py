import math
alpha = 1/137.035999084
mP   = 2.176434e-8        # Planck mass (kg)
me   = 9.1093837015e-31
mp   = 1.67262192369e-27
Msun = 1.98892e30

print("alpha              = %.12f" % alpha)
print("theta (2*pi*alpha) = %.9f rad = %.4f deg" % (2*math.pi*alpha, math.degrees(2*math.pi*alpha)))
th_b = math.atan(alpha)
print("theta (arctan al)  = %.9f rad = %.4f deg" % (th_b, math.degrees(th_b)))
print("两条定义之比        = %.6f  (应恰为 2pi=%.6f)" % (2*math.pi*alpha/th_b, 2*math.pi))

ae = 1.15965218128e-3
for name, th in (("2pi*alpha", 2*math.pi*alpha), ("arctan(alpha)", th_b)):
    print("2tan(theta=%-14s) = %.6e  |  比 a_e=%.6e  偏差 = %.3f x" % (name, 2*math.tan(th), 2*ae, 2*math.tan(th)/(2*ae)))

print("\n--- No-Go VI 激活判据 Q(m)=alpha/(1+alpha^2)*(m/mP)^2 ---")
pref = alpha/(1+alpha**2)
print("前因子 alpha/(1+alpha^2) = %.6e" % pref)
print("Q=1 阈值 m*/mP = %.4f  (卷二十五:21 记 11.7)" % math.sqrt(1/pref))
for label, m in (("electron", me), ("proton", mp), ("10 Msun PBH", 10*Msun),
                 ("GW150914 30 Msun", 30*Msun), ("Sgr A* 4.3e6 Msun", 4.3e6*Msun)):
    q = pref*(m/mP)**2
    print("  Q(%-20s) = %.3e" % (label, q))
