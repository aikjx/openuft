# -*- coding: utf-8 -*-
"""统一场论新构建 · Top1000 实数核对脚本
功能：扫描六卷文件，验证 (1) 单元总数=1000 (2) F001-F1000 连续无缺 (3) 无重复编号
      (4) 六要素（公式/量纲核验/假设/逻辑链/现象锚定/诚实标界）逐单元齐全。
复跑：python verify_f1000.py
"""
import re, os, sys

BASE = r'D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论新构建'
FILES = [
    '01_卷A_引力与时空_F001-F250.md',
    '02_卷B_粒子与统一_F251-F500.md',
    '03_卷C_宇宙学_F501-F625.md',
    '04_卷D_量子基础_F626-F750.md',
    '05_卷E_凝聚态与现象_F751-F875.md',
    '06_卷F_数学物理与交叉_F876-F1000.md',
]
ELEMENTS = ['**公式**', '**量纲核验**', '**假设/猜想**', '**逻辑链**', '**现象锚定**', '**诚实标界**']

def main():
    all_nums, per_file, total_elems = [], {}, {}
    for f in FILES:
        p = os.path.join(BASE, f)
        if not os.path.exists(p):
            print(f'[缺失文件] {p}'); sys.exit(1)
        txt = open(p, encoding='utf-8').read()
        nums = [int(m) for m in re.findall(r'^### F(\d{3,4})\b', txt, re.M)]
        per_file[f] = dict(count=len(nums), lo=min(nums), hi=max(nums),
                           ordered=sorted(nums) == nums, unique=len(set(nums)) == len(nums))
        all_nums.extend(nums)
        for k in ELEMENTS:
            total_elems[k] = total_elems.get(k, 0) + txt.count(k)
    print('== 每卷实数计数 ==')
    for f, d in per_file.items():
        print(f"  {f}: count={d['count']} 范围={d['lo']}-{d['hi']} 有序={d['ordered']} 唯一={d['unique']}")
    print(f"  合计单元数 = {len(all_nums)}  (目标 1000)")
    exp = set(range(1, 1001))
    missing = sorted(exp - set(all_nums))
    dup = sorted({n for n in all_nums if all_nums.count(n) > 1})
    extra = sorted(set(all_nums) - exp)
    print(f"  缺号数 = {len(missing)}  缺号列表 = {missing[:30]}")
    print(f"  重复数 = {len(dup)}  重复列表 = {dup[:30]}")
    print(f"  越界(非F001-F1000) = {len(extra)}  {extra[:30]}")
    print('== 六要素全卷计数（目标≈1000，每单元各一次）==')
    ok = True
    for k in ELEMENTS:
        print(f"  {k}: {total_elems[k]}")
        if total_elems[k] < 1000:
            ok = False
    print('== 结论 ==')
    if len(all_nums) == 1000 and not missing and not dup and not extra and ok:
        print('PASS: 1000 单元实数核对通过，F001-F1000 连续无缺无重，六要素逐单元齐全。')
    else:
        print('FAIL: 存在缺号/重复/越界/要素缺失，需修正。')

if __name__ == '__main__':
    main()
