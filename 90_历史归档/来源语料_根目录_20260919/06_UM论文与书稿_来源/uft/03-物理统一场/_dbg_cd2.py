import mpmath as mp, random, importlib.util
src = open('breakthrough_all.py', encoding='utf-8').read()
cut = src.index('SEP("B4')
ns = {}
exec(src[:cut], ns)
cd_mul = ns['cd_mul']
cd_conj = ns['cd_conj']
nsq = lambda a: sum(v * v for v in a)

def e(n, k):
    v = [mp.mpf('0')] * n
    v[k] = mp.mpf('1')
    return v

# test quaternion: i,j,k
i = e(4, 1); j = e(4, 2); k = e(4, 3)
print('i*j ==', cd_mul(i, j), 'expect k or -k')
print('nsq(i*j)', nsq(cd_mul(i, j)))
# random quaternions
random.seed(3)
for _ in range(3):
    x = [mp.mpf(random.randint(-3, 3)) for _ in range(4)]
    y = [mp.mpf(random.randint(-3, 3)) for _ in range(4)]
    d = nsq(cd_mul(x, y)) - nsq(x) * nsq(y)
    print('4d diff', d)
