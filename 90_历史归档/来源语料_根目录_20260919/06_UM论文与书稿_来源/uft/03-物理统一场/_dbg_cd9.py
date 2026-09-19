import mpmath as mp, importlib.util
src = open('breakthrough_all.py', encoding='utf-8').read()
cut = src.index('SEP("B4')
ns = {}
exec(src[:cut], ns)
cd_mul = ns['cd_mul']
nsq = lambda a: sum(v * v for v in a)
def e(n, k):
    v = [mp.mpf('0')] * n
    v[k] = mp.mpf('1')
    return v
for n in [16]:
    for k in [1, 2, 3, 4, 5, 6, 7, 8]:
        sq = cd_mul(e(n, k), e(n, k))
        print('e%d^2 =' % k, sq, 'nsq', nsq(sq))
    # e1 * e2
    p = cd_mul(e(n, 1), e(n, 2))
    print('e1*e2 =', p, 'nsq', nsq(p))
    p2 = cd_mul(e(n, 2), e(n, 1))
    print('e2*e1 =', p2, 'nsq', nsq(p2))
