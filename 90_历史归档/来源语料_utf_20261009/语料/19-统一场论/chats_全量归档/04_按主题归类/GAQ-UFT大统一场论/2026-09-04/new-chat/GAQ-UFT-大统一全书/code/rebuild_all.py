# -*- coding: utf-8 -*-
"""rebuild_all.py：从备份恢复 → 全修复管线 → 校验 → 合并 → 双口径字数。
每步都在同一进程内读盘验证，杜绝命令间状态疑云。"""
import io, os, re, glob, shutil, subprocess, sys

ROOT = r'C:\Users\mo\Doubao\chats\2026-09-04\new-chat\GAQ-UFT-大统一全书'
CODE = os.path.join(ROOT, 'code')
MS = os.path.join(ROOT, 'manuscript')
BAK = os.path.join(ROOT, '_backup_pre_fix', 'manuscript')
OUT = os.path.join(ROOT, 'deliverables', 'final.md')

def run(script, *args):
    r = subprocess.run([sys.executable, os.path.join(CODE, script), *args],
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(script + ' failed:\n' + r.stderr.decode('utf-8', 'replace'))
    return r.stdout.decode('utf-8', 'replace')

def long_head_lines():
    """行首 ## / ### 且总长>105 的行数（含超长标题诊断）"""
    n = 0
    for p in sorted(glob.glob(os.path.join(MS, 'ch*.md'))):
        with io.open(p, encoding='utf-8') as f:
            lines = f.read().split('\n')
        for ln in lines:
            if ln.startswith('##') and len(ln) > 105:
                n += 1
    return n

def mid_line_heads():
    """行中标题计数：行内出现 '## X.Y' 或 '### X.Y' 且前面还有正文"""
    n = 0
    pat = re.compile(r'.+\S(##|###) \d+\.\d+')
    for p in sorted(glob.glob(os.path.join(MS, 'ch*.md'))):
        with io.open(p, encoding='utf-8') as f:
            lines = f.read().split('\n')
        for ln in lines:
            if pat.search(ln):
                n += 1
    return n

def norm_glued():
    """检查是否存在 '## X.Y 标题正文粘连'（标题行含正文、下一行非空且紧跟）"""
    n = 0
    pat = re.compile(r'^## \d+\.\d+ ')
    for p in sorted(glob.glob(os.path.join(MS, 'ch*.md'))):
        with io.open(p, encoding='utf-8') as f:
            lines = f.read().split('\n')
        for i, ln in enumerate(lines):
            m = pat.match(ln)
            if m and len(ln) > 60 and i + 1 < len(lines) and lines[i+1].strip():
                n += 1
    return n

def head_counts():
    """每章顶层 ## 标题编号是否连续 1..N"""
    out = []
    for p in sorted(glob.glob(os.path.join(MS, 'ch*.md'))):
        with io.open(p, encoding='utf-8') as f:
            lines = f.read().split('\n')
        nums = []
        pat = re.compile(r'^## (\d+)\.(\d+) ')
        for ln in lines:
            m = pat.match(ln)
            if m:
                nums.append((int(m.group(1)), int(m.group(2))))
        if not nums:
            out.append((os.path.basename(p)[:6], 'no-head'))
            continue
        chapter = nums[0][0]
        ok = all(b == i + 1 for (a, b), i in zip(nums, range(len(nums)))) and all(a == chapter for a, _ in nums)
        out.append((os.path.basename(p)[:6], 'OK' if ok else 'BAD'))
    return out

# 1) 恢复备份（干净原始稿）
n = 0
for src in sorted(glob.glob(os.path.join(BAK, 'ch*.md'))):
    shutil.copy2(src, os.path.join(MS, os.path.basename(src)))
    n += 1
print('1. 恢复章节数:', n)

# 2) pass-1
print('2. pass-1:\n', run('fix_glued_heads.py', 'apply').strip().split('\n')[-1])
print('   行首超长标题:', long_head_lines())

# 3) midline
print('3. midline:\n   ' + run('fix_midline_heads.py', 'apply').strip().split('\n')[-1])
print('   行中标题:', mid_line_heads())

# 4) fix_one
print('4. fix_one:', run('fix_one.py').strip())
print('   行首超长标题:', long_head_lines())

# 5) normalize（已修复换行 bug）
print('5. normalize（含换行修复）:')
print(run('normalize_heads.py').strip())
print('   行首超长标题:', long_head_lines())
print('   行中标题:', mid_line_heads())
print('   标题正文粘连(>60字+下行非空):', norm_glued())

# 6) 章节编号连续性
print('6. 章节编号:', head_counts())

# 7) merge
print('7. merge:\n' + run('merge_book.py').strip())

# 8) 字数
print('8. dual_count:')
print(run('dual_count.py').strip())

# 9) final.md 校验
print('9. check_final:')
print(run('check_final.py').strip())
