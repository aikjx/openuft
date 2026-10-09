import os, json
d = r'd:\a10\aikjx\code\my_lib\utf'
fn = [f for f in os.listdir(d) if 'full_valid' in f][0]
fp = os.path.join(d, fn)
print('FILE:', fp)
with open(fp, 'r', encoding='utf-8') as f:
    L = f.readlines()
print('LINES:', len(L))
r = {}
for i, l in enumerate(L):
    if 'VIII.可证伪' in l and 'm1a' not in r:
        r['m1a'] = i
        print('m1a L'+str(i+1)+':', l.rstrip()[:60])
    if 'm1a' in r and 'm1b' not in r and '========' in l[:60]:
        r['m1b'] = i
        print('m1b L'+str(i+1)+':', l.rstrip()[:60])
    if i>100 and l.strip()=='# 主程序' and '========' in L[i-1][:60]:
        r['m2s'] = i-1
        r['m2m'] = i
        print('m2s L'+str(i)+':', L[i-1].rstrip()[:60])
        print('m2m L'+str(i+1)+':', l.rstrip()[:60])
    if '"VIII", validate_module_viii' in l:
        r['m3v'] = i
        print('m3v L'+str(i+1)+':', l.rstrip()[:60])
        for j in range(i+1, i+6):
            if L[j].strip() == ']':
                r['m3c'] = j
                print('m3c L'+str(j+1)+':', L[j].rstrip()[:60])
                break
    if 'm4a' not in r and '模块VIII' in l and ('OK' in l or '\u2705' in l):
        r['m4a'] = i
        print('m4a L'+str(i+1)+':', l.rstrip()[:60])
    if '8大模块' in l:
        r['m4b'] = i
        print('m4b L'+str(i+1)+':', l.rstrip()[:60])
if 'm4a' not in r:
    print('SEARCH m4a:')
    for i, l in enumerate(L):
        if '模块VIII' in l:
            print(' cand L'+str(i+1)+':', repr(l[:90]))
print('RESULT_JSON:', json.dumps({k:v+1 for k,v in r.items()}, ensure_ascii=False))
