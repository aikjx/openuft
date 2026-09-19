import mpmath as mp, importlib.util
src = open('breakthrough_all.py', encoding='utf-8').read()
cut = src.index('SEP("B4')
ns = {}
exec(src[:cut], ns)
cd_mul = ns['cd_mul']
def e(n, k):
    v = [mp.mpf('0')] * n
    v[k] = mp.mpf('1')
    return v
i = e(4, 1); j = e(4, 2); k = e(4, 3)
print('i*i =', cd_mul(i, i), '(expect [-1,0,0,0])')
print('j*j =', cd_mul(j, j), '(expect [-1,0,0,0])')
print('k*k =', cd_mul(k, k), '(expect [-1,0,0,0])')
print('i*j =', cd_mul(i, j), '(expect k=[0,0,0,1])')
print('j*i =', cd_mul(j, i), '(expect -k=[0,0,0,-1])')
print('j*k =', cd_mul(j, k), '(expect i=[0,1,0,0])')
print('k*i =', cd_mul(k, i), '(expect j=[0,0,1,0])')
