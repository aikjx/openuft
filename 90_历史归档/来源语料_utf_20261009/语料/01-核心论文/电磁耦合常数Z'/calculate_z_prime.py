#!/usr/bin/env python3
# 计算Z'常数的精确值

# CODATA 2018常数
c = 299792458  # 光速，单位：m/s
epsilon0 = 8.8541878128e-12  # 真空介电常数，单位：F/m
import math

# 计算8π
pi8 = 8 * math.pi
print(f"8π = {pi8}")

# 计算Z' = c/(8πε₀)
Z_prime = c / (pi8 * epsilon0)
print(f"Z' = c/(8πε₀) = {Z_prime}")
print(f"Z'（科学计数法） = {Z_prime:.11e}")

# 计算更精确的Z'值
pi8_precise = 8 * 3.14159265358979323846
Z_prime_precise = c / (pi8_precise * epsilon0)
print(f"\n使用更精确的π值:")
print(f"8π（精确） = {pi8_precise}")
print(f"Z'（精确） = {Z_prime_precise}")
print(f"Z'（精确，科学计数法） = {Z_prime_precise:.11e}")
