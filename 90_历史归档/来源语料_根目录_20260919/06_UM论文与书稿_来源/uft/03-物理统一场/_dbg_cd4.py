import mpmath as mp, random, importlib.util
src = open('breakthrough_all.py', encoding='utf-8').read()
cut = src.index('SEP("B4')
ns = {}
exec(src[:cut], ns)
cd_mul = ns['cd_mul']
nsq = lambda a: sum(v * v for v in a)
random.seed(3)
x = [mp.mpf(random.randint(-3, 3)) for _ in range(4)]
y = [mp.mpf(random.randint(-3, 3)) for _ in range(4)]
print('x=', x)
print('y=', y)
print('x*y=', cd_mul(x, y))
print('nsq(x*y)=', nsq(cd_mul(x, y)))
print('nsq(x)*nsq(y)=', nsq(x) * nsq(y))
print('diff=', nsq(cd_mul(x, y)) - nsq(x) * nsq(y))
