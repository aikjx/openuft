import mpmath as mp, importlib.util
src = open('breakthrough_all.py', encoding='utf-8').read()
cut = src.index('SEP("B4')
ns = {}
exec(src[:cut], ns)
cd_mul = ns['cd_mul']
nsq = lambda a: sum(v * v for v in a)
x = [mp.mpf('1'), mp.mpf('2'), mp.mpf('0'), mp.mpf('0')]
y = [mp.mpf('0'), mp.mpf('0'), mp.mpf('3'), mp.mpf('0')]
print('x*y =', cd_mul(x, y), 'expect [0,0,3,6]')
print('nsq(x*y)=', nsq(cd_mul(x, y)), 'nsq(x)*nsq(y)=', nsq(x) * nsq(y))
