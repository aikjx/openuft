import mpmath as mp, random

def cd_rev(a, b):
    n = len(a)
    if n == 1:
        return [a[0] * b[0]]
    m = n // 2
    # 变体: 用 reversed 实现共轭效果
    return [u - v for u, v in zip(cd_rev(a[:m], b[:m]),
                                  cd_rev(a[m:], list(reversed(b[m:]))))] + \
           [u + v for u, v in zip(cd_rev(list(reversed(a[:m])), b[m:]),
                                  cd_rev(a[m:], b[:m]))]

nsq = lambda a: sum(v * v for v in a)
random.seed(2)
for n in [2, 4, 8, 16, 32]:
    mx = mp.mpf('0')
    for _ in range(5):
        x = [mp.mpf(random.randint(-3, 3)) for _ in range(n)]
        y = [mp.mpf(random.randint(-3, 3)) for _ in range(n)]
        d = nsq(cd_rev(x, y)) - nsq(x) * nsq(y)
        mx = max(mx, abs(d))
    print('dim', n, 'max_abs_diff', mx)
