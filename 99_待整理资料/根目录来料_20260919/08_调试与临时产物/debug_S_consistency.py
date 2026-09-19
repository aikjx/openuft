# -*- coding: utf-8 -*-
# 调试：E=10^6 与 10^7 处 S(E,√E) 与 H(E) 的一致性差异
import numpy as np, math

X = 10_000_000
sieve = np.ones(X + 1, dtype=bool)
sieve[0] = sieve[1] = False
for i in range(2, int(X ** 0.5) + 1):
    if sieve[i]:
        sieve[i * i::i] = False
primes = np.nonzero(sieve)[0]

def S_ok(E, z):
    lo = math.isqrt(E) + 1
    hi = E // 2
    ok = np.ones(E + 1, dtype=bool)
    for p in primes[primes <= z]:
        ok[p::p] = False
    ms = np.arange(lo, hi + 1)
    return int(np.sum(ok[ms] & ok[E - ms])), ok

def S_direct(E):
    lo = math.isqrt(E) + 1
    hi = E // 2
    cnt = 0
    first_bad = []
    for m in range(lo, hi + 1):
        if sieve[m] and sieve[E - m]:
            cnt += 1
    return cnt

for E in [10**6, 10**7]:
    z = math.isqrt(E)
    sok, ok = S_ok(E, z)
    sdir = S_direct(E)
    print(f"E={E}: S(ok方法)={sok}, S(直接sieve)={sdir}, 差={sdir-sok}")

# 找出 ok 方法漏掉的 m（m 与 E-m 都素数但 ok[ms]&ok[E-ms] 为 False）
E = 10**6
z = math.isqrt(E)
lo, hi = math.isqrt(E) + 1, E // 2
ok = np.ones(E + 1, dtype=bool)
for p in primes[primes <= z]:
    ok[p::p] = False
miss = []
for m in range(lo, hi + 1):
    if sieve[m] and sieve[E - m] and not (ok[m] and ok[E - m]):
        miss.append(m)
        if len(miss) >= 8:
            break
print(f"\nE={E} ok方法漏掉的 m（应全空）: {miss}")
if miss:
    m = miss[0]
    print(f"  首个漏掉的 m={m}: sieve[m]={sieve[m]}, sieve[E-m]={sieve[E-m]}, ok[m]={ok[m]}, ok[E-m]={ok[E-m]}")
    # ok[m] 为 False 的原因：m 的某个素因子 p<=z
    for p in primes[primes <= z]:
        if m % p == 0:
            print(f"    m 被 p={p} 筛掉 (m%p={m%p})"); break
    # ok[E-m] 为 False 的原因
    for p in primes[primes <= z]:
        if (E - m) % p == 0:
            print(f"    E-m 被 p={p} 筛掉 (E-m={E-m}, (E-m)%p={(E-m)%p})"); break
