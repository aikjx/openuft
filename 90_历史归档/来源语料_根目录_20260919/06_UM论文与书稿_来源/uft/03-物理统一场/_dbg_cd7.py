import mpmath as mp, importlib.util
src = open('breakthrough_all.py', encoding='utf-8').read()
cut = src.index('SEP("B4')
ns = {}
exec(src[:cut], ns)
cd_mul = ns['cd_mul']
i = [mp.mpf('0'), mp.mpf('1'), mp.mpf('0'), mp.mpf('0')]
j = [mp.mpf('0'), mp.mpf('0'), mp.mpf('1'), mp.mpf('0')]
print('i*j direct =', cd_mul(i, j))
