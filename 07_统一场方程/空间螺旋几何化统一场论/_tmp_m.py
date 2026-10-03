# -*- coding: utf-8 -*-
import sympy as sp

a = [sp.zeros(4, 4) for _ in range(4)]
print("distinct?", [a[i] is a[j] for i in range(4) for j in range(4) if i < j])
a[1][1, 1] = 99
print("after a[1][1,1]=99 -> a[3][1,1] =", a[3][1, 1])
b = [sp.zeros(2, 2) for _ in range(3)]
print("2x2 distinct?", b[0] is b[1], b[1] is b[2])
