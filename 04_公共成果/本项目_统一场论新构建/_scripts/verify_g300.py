# -*- coding: utf-8 -*-
"""本源演绎推导工程 · G 全套实数核对脚本
扫描 10-13 卷，验证 (1) G001-G300 连续无缺无重 (2) 每卷条数符合号段分配
      (3) 五要素（推导链/公式/量纲核验/现象锚定/诚实标界）逐条齐全。
复跑：python verify_g300.py
"""
import re, os, sys

BASE = r'D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论新构建'
FILES = [
    ('10_本源推导_宇宙属性元数据全谱_2026-10-21.md', 1, 80),
    ('11_本源推导_所有力与所有运动_2026-10-21.md', 81, 180),
    ('12_核心公式理论体系总成_2026-10-21.md', 181, 260),
    ('13_宇宙模拟总纲_2026-10-21.md', 261, 300),
]
ELEMENTS = ['**推导链**', '**公式**', '**量纲核验**', '**现象锚定**', '**诚实标界**']

def main():
    all_nums, per_file, total_elems = [], {}, {}
    for f, lo, hi in FILES:
        p = os.path.join(BASE, f)
        if not os.path.exists(p):
            print(f'[缺失文件] {p}'); sys.exit(1)
        txt = open(p, encoding='utf-8').read()
        nums = [int(m) for m in re.findall(r'^### G(\d{3})\b', txt, re.M)]
        ok_range = all(lo <= n <= hi for n in nums)
        per_file[f] = dict(count=len(nums), lo=min(nums), hi=max(nums),
                           range_ok=ok_range, ordered=sorted(nums) == nums,
                           unique=len(set(nums)) == len(nums),
                           expect=(hi - lo + 1))
        all_nums.extend(nums)
        for k in ELEMENTS:
            total_elems[k] = total_elems.get(k, 0) + txt.count(k)
    print('== 每卷实数计数 ==')
    for f, d in per_file.items():
        mark = 'OK' if (d['count'] == d['expect'] and d['range_ok'] and d['ordered'] and d['unique']) else 'FAIL'
        print(f"  {f}: count={d['count']}/{d['expect']} 范围={d['lo']}-{d['hi']} 号段内={d['range_ok']} 有序={d['ordered']} 唯一={d['unique']} [{mark}]")
    print(f"  合计条目数 = {len(all_nums)}  (目标 300)")
    exp = set(range(1, 301))
    missing = sorted(exp - set(all_nums))
    dup = sorted({n for n in all_nums if all_nums.count(n) > 1})
    extra = sorted(set(all_nums) - exp)
    print(f"  缺号数 = {len(missing)}  缺号列表 = {missing[:30]}")
    print(f"  重复数 = {len(dup)}  重复列表 = {dup[:30]}")
    print(f"  越界(非G001-G300) = {len(extra)}  {extra[:30]}")
    print('== 五要素全卷计数（目标≥300，每条一次）==')
    ok = True
    for k in ELEMENTS:
        print(f"  {k}: {total_elems[k]}")
        if total_elems[k] < 300:
            ok = False
    print('== 结论 ==')
    if len(all_nums) == 300 and not missing and not dup and not extra and ok:
        print('PASS: G001-G300 实数核对通过，连续无缺无重，五要素逐条齐全。')
    else:
        print('FAIL: 存在缺号/重复/越界/要素缺失，需修正。')

if __name__ == '__main__':
    main()
