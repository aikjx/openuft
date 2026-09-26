# -*- coding: utf-8 -*-
"""`spiral_c25_alpha_n_scan.py` 的牙齿检验：每个变异体必须把**点名**的判据打红。

为什么需要它（本目录红线）
------------------------
"全绿"本身不是证据。扫描脚本的 11 条判据里有几条是**容差型**的
（残差 <= 2× 先验地板、实测 == 闭式 <= 地板、Richardson 自身误差 <= (2/15)x^2），
这种判据有两种假绿：地板写大了（什么都放过）、或判据根本没接在被测函数上。
本驱动对每一条判据种一个缺陷，要求它按名字变红；另外三个变异体是**预期全绿**的
阳性对照（把 α 换成 1/137 口径、把螺旋半径翻倍、把动能系数翻倍），
用来证明这些判据不是"见谁红"。

规矩
----
* 未变异基线必须打印判决行且 rc=0；否则整轮 INVALID（退出码 2）。
* 崩溃只有发生在被测守卫的报错上才算捕获；这里单独计 CRASH 并算失败。
* 变异体写在临时目录，**不改归档**；产物 JSON 也只落在临时目录
  （扫描脚本的版面钉在"脚本自己旁边"，复制品旁边就是临时目录）。

运行：python spiral_c25_scan_teeth.py
退出码：0 = 全部 CAUGHT/CLEAN；1 = 有 MISSED 或 CRASH；2 = 驱动本身无效。
"""
import os
import re
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

TARGET = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      'spiral_c25_alpha_n_scan.py')
SUM = re.compile(r'PASS (\d+) / FAIL (\d+)')

# (名称, 原文整行, 变异后整行, 必须变红的判据 ID 集合；空集 = 预期全绿的阳性对照)
MUTANTS = [
    ('m1_bias_minus1_dropped',
     '    return (math.sin(x) / x) ** 2 - 1.0',
     '    return (math.sin(x) / x) ** 2',
     {'S2a', 'S2b', 'S2c'}),
    ('m2_fd_wrong_angle',
     '    return (2.0 / (h * h)) * (1.0 - math.cos(2.0 * math.pi * n / N))',
     '    return (2.0 / (h * h)) * (1.0 - math.cos(2.0 * math.pi * n / (2 * N)))',
     {'S1-N32', 'S2a', 'S3-N32'}),
    ('m3_richardson_div2',
     '    return ((k2 - k1) / 3.0 / kc, (k1 - kc) / kc, (k2 - kc) / kc)',
     '    return ((k2 - k1) / 2.0 / kc, (k1 - kc) / kc, (k2 - kc) / kc)',
     {'S2c'}),
    ('m4_series_coef_halved',
     '    RIC_C = 2.0 / 15.0',
     '    RIC_C = 1.0 / 15.0',
     {'S2c'}),
    ('m5_noise_floor_zeroed',
     '    return EPS / (2.0 * s * s) + 4.0 * EPS',
     '    return 0.0',
     {'S2a', 'S2b'}),
    ('m6_kin_scale_x2_GREEN',
     'KIN = HBAR ** 2 / (2.0 * ME)',
     'KIN = HBAR ** 2 / ME',
     set()),
    ('m7_nstar_inverted',
     '    nstar = math.sqrt(ALPHA / g1)',
     '    nstar = math.sqrt(g1 / ALPHA)',
     {'S4a'}),
    ('m8_nsquare_law_as_n3',
     "          abs((KIN * 1 / (ALPHA / 1)) / (KIN * 4 / ALPHA) - 0.25) < 1e-12,",
     "          abs((KIN * 1 / (ALPHA / 1)) / (KIN * 3 / ALPHA) - 0.25) < 1e-12,",
     {'S4b'}),
    ('m9_offset_comparable_scale',
     'OFFSET = E_SCALE * V0',
     'OFFSET = 1.0e-9',
     {'S2d'}),
    ('m10_alpha_137_GREEN',
     'ALPHA = 7.2973525693e-3',
     'ALPHA = 1.0 / 137.0',
     set()),
    ('m11_geometry_x2_GREEN',
     'A_M = 1e-15',
     'A_M = 2e-15',
     set()),
]


def run(path):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    p = subprocess.run([sys.executable, path, '--strict', '--nmax', '40'],
                       capture_output=True, text=True, encoding='utf-8',
                       errors='replace', env=env, cwd=os.path.dirname(path))
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def red_ids(out):
    return {m.group(1) for m in re.finditer(r'\[FAIL\]\s+(\S+)', out)}


def main():
    src = open(TARGET, encoding='utf-8').read()
    tmp = tempfile.mkdtemp(prefix='c25teeth_')
    base = os.path.join(tmp, 'baseline.py')
    with open(base, 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    rc, out = run(base)
    mm = SUM.search(out)
    if not mm or rc != 0:
        print('INVALID: 未变异基线没有判决行或 rc=%d（判决行是本轮的引用资格）' % rc)
        print(out[-1500:])
        return 2
    print('基线：%s rc=%d（--strict，任何内部判据 FAIL 都会把退出码打到 1）'
          % ('PASS %s / FAIL %s' % (mm.group(1), mm.group(2)), rc))
    n_caught = n_missed = n_crash = 0
    for i, (name, old, new, expect) in enumerate(MUTANTS):
        c = src.count(old)
        if c != 1:
            print('INVALID: %s 的锚点命中 %d 次（期望 1）' % (name, c))
            return 2
        p = os.path.join(tmp, 'mut%d.py' % i)
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write(src.replace(old, new, 1))
        rc, out = run(p)
        r = red_ids(out)
        mm = SUM.search(out)
        tally = ('PASS %s/FAIL %s' % (mm.group(1), mm.group(2))) if mm else '无判决行'
        if not mm:
            n_crash += 1
            state = 'CRASH'
        elif not expect and not r:
            n_caught += 1
            state = 'CLEAN(阳性对照)'
        elif expect <= r:
            n_caught += 1
            state = 'CAUGHT'
        else:
            n_missed += 1
            state = 'MISSED(缺 %s)' % sorted(expect - r)
        extra = sorted(r - expect)
        print('  %-34s %-16s rc=%d %-18s 红=%s%s'
              % (name, state, rc, tally, sorted(r) if r else '[]',
                 ('  连带红=%s' % extra) if (state == 'CAUGHT' and extra) else ''))
    print('\n牙齿检验：%d CAUGHT/CLEAN / %d MISSED / %d CRASH（共 %d 个变异体，'
          '其中 %d 个预期全绿的阳性对照）'
          % (n_caught, n_missed, n_crash, len(MUTANTS),
             sum(1 for m in MUTANTS if not m[3])))
    return 0 if (n_missed == 0 and n_crash == 0) else 1


if __name__ == '__main__':
    sys.exit(main())
