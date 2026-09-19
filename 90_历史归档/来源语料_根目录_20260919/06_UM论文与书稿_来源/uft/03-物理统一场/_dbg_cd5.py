import mpmath as mp, random, importlib.util
src = open('breakthrough_all.py', encoding='utf-8').read()
cut = src.index('SEP("B4')
ns = {}
exec(src[:cut], ns)
cd_mul = ns['cd_mul']
nsq = lambda a: sum(v * v for v in a)

def quat_mul(q, r):
    # (a,b,c,d) standard Hamilton
    a,b,c,d = q
    e,f,g,h = r
    return [
        a*e - b*f - c*g - d*h,
        a*f + b*e + c*h - d*g,
        a*g - b*h + c*e + d*f,
        a*h + b*g - c*f + d*e,
    ]

random.seed(3)
x = [mp.mpf(random.randint(-3, 3)) for _ in range(4)]
y = [mp.mpf(random.randint(-3, 3)) for _ in range(4)]
print('x=', x)
print('y=', y)
print('cd_mul  =', cd_mul(x, y), 'nsq', nsq(cd_mul(x, y)))
print('quat_mul=', quat_mul(x, y), 'nsq', nsq(quat_mul(x, y)))
print('nsq(x)*nsq(y)=', nsq(x) * nsq(y))
