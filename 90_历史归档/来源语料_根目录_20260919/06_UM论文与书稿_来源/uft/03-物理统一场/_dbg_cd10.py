import mpmath as mp, random

def conj(x):
    return [x[0]] + [-v for v in x[1:]]

def cd(a, b):
    n = len(a)
    if n == 1:
        return [a[0]*b[0]]
    m = n // 2
    a1, a2 = a[:m], a[m:]
    b1, b2 = b[:m], b[m:]
    # Wikipedia standard: (a,b)(c,d) = (a*c - d*conj(b), conj(a)*d + c*b)
    # here a=(a1,a2), (c,d)=(b1,b2)
    p1 = [u - v for u, v in zip(cd(a1, b1), cd(b2, conj(a2)))]
    p2 = [u + v for u, v in zip(cd(conj(a1), b2), cd(b1, a2))]
    return p1 + p2

nsq = lambda a: sum(v*v for v in a)
random.seed(2)
for n in [2, 4, 8, 16, 32]:
    mx = mp.mpf('0')
    for _ in range(5):
        x = [mp.mpf(random.randint(-3, 3)) for _ in range(n)]
        y = [mp.mpf(random.randint(-3, 3)) for _ in range(n)]
        d = nsq(cd(x, y)) - nsq(x) * nsq(y)
        mx = max(mx, abs(d))
    print('dim', n, 'max_abs_diff', mx)
