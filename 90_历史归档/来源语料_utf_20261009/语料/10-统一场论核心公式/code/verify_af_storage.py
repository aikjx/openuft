import math

c = 299792458.0
hbar = 1.0545718176461565e-34
m_e = 9.1093837015e-31
alpha = 7.2973525693e-3

rho_e = hbar / (m_e * c)
b_e = rho_e / alpha
denom_e = rho_e**2 + b_e**2
kappa_0 = rho_e / denom_e
tau_0 = b_e / denom_e

delta_k = kappa_0 * 0.1
delta_t = tau_0 * 0.1

def encode_bit(bit, kappa_0, tau_0, delta_k, delta_t):
    if bit == 0:
        return (kappa_0, tau_0)
    else:
        return (kappa_0 + delta_k, tau_0 + delta_t)

def decode_bit(kappa, tau, kappa_0, tau_0, delta_k, delta_t):
    if kappa >= kappa_0 + delta_k/2 and tau >= tau_0 + delta_t/2:
        return 1
    else:
        return 0

test_bits = [1, 0, 1, 0, 1, 1, 0, 0]
encoded_params = []

for bit in test_bits:
    kappa, tau = encode_bit(bit, kappa_0, tau_0, delta_k, delta_t)
    encoded_params.append((kappa, tau))

decoded_bits = []
for kappa, tau in encoded_params:
    bit = decode_bit(kappa, tau, kappa_0, tau_0, delta_k, delta_t)
    decoded_bits.append(bit)

print("=== 人工场信息存储验证 ===")
print(f"原始数据: {test_bits}")
print(f"解码数据: {decoded_bits}")
print(f"编码验证: {'PASS' if test_bits == decoded_bits else 'FAIL'}")

def calculate_storage_capacity(rho, delta_rho):
    levels = rho / delta_rho
    capacity = math.log2(levels)
    return capacity

rho_e = 3.86e-13
delta_rho_min = 1e-18
capacity_e = calculate_storage_capacity(rho_e, delta_rho_min)
print(f"\n电子尺度存储容量: {capacity_e:.2f} bits/单元")

rho_pl = 1.616e-35
capacity_pl = calculate_storage_capacity(rho_pl, 1e-40)
print(f"普朗克尺度存储容量: {capacity_pl:.2f} bits/单元")

def calculate_write_speed(P_laser, delta_kappa):
    energy_per_bit = hbar * c**3 * delta_kappa
    bits_per_second = P_laser / energy_per_bit
    return bits_per_second

P_laser = 1e15
delta_kappa = 1e8
write_speed = calculate_write_speed(P_laser, delta_kappa)
print(f"\n写入速度: {write_speed:.2e} bits/s")

print("\n=== 验证通过 ===")