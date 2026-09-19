import mpmath as mp, random, importlib.util
src = open('breakthrough_all.py', encoding='utf-8').read()
cut = src.index('SEP("B4')
ns = {}
exec(src[:cut], ns)
cd_mul = ns['cd_mul']
nsq = lambda a: sum(v * v for v in a)
random.seed(2)
for n in [8, 16, 32]:
    for _ in range(3):
        x = [mp.mpf(random.randint(-3, 3)) for _ in range(n)]
        y = [mp.mpf(random.randint(-3, 3)) for _ in range(n)]
        d = nsq(cd_mul(x, y)) - nsq(x) * nsq(y)
        print('n', n, 'diff', d)
        if d != 0:
            break
