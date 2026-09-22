import mpmath as mp, random, importlib.util
spec = importlib.util.spec_from_file_location('bt', 'breakthrough_all.py')
src = open('breakthrough_all.py', encoding='utf-8').read()
cut = src.index('SEP("B4')
head = src[:cut]
ns = {}
exec(head, ns)
cd_mul = ns['cd_mul']
nsq = lambda a: sum(v * v for v in a)
random.seed(7)
for n in [2, 4, 8, 16, 32]:
    mx = mp.mpf('0')
    for _ in range(3):
        x = [mp.mpf(random.randint(-3, 3)) for _ in range(n)]
        y = [mp.mpf(random.randint(-3, 3)) for _ in range(n)]
        d = abs(nsq(cd_mul(x, y)) - nsq(x) * nsq(y))
        mx = max(mx, d)
    print('dim', n, 'max_norm_diff', mx)
