# -*- coding: utf-8 -*-
import io, re

P = 'D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_统一场论攻破/布局_物理Top100难题攻破清单_2026-10-21.md'

new_status = {
    2:  '✅ C0148（本轮）：P15 结构性负面——黑洞熵/霍金温度精算，需幺正 QG+全息对偶，几何供给 0，撞 C1/C7',
    4:  '✅ C0145（本轮）：P05 结构性负面——Λ=1.31e-52 m⁻²、w=−1 0.875σ，几何供给 0，撞 C2/C3',
    12: '✅ C0144（本轮）：P09 结构性负面——慢滚参数精算，inflaton 需 3 新输入，撞 C1/C2/C3',
    17: '✅ C0147（本轮）：P08 结构性负面——sin²θ_W=3/8、τ_p 两难（4.60e31/2.87e36 yr），撞 C1/C2',
    22: '✅ C0142：P11 结构性负面——代民主差 2.3–203 倍，几何供给 0',
    23: '✅ C0142（含于 T022）',
    24: '✅ C0143（本轮）：P06 结构性负面——seesaw 反解 M_R≈1.22e15 GeV，撞 C1/C2',
    25: '✅ C0146（本轮）：P07 结构性负面——E_sph=7.12–12.81 TeV、双重否决，撞 C1/C2',
    27: '✅ C0151（本轮）：结构性负面——反常不锁 N_g=3，撞 C1/C2',
    37: '✅ C0150（本轮）：结构性负面——σ=4.847，需新物理，几何供给 0，撞 C2/C5',
    91: '✅ C0149（本轮）：P16 结构性负面——无单点预言，撞 C5/C6',
}

txt = io.open(P, encoding='utf-8').read()
lines = txt.split('\n')
changed = 0
for i, line in enumerate(lines):
    m = re.match(r'^\| (T\d{3}) \|', line)
    if not m:
        continue
    tid = int(m.group(1)[1:])
    if tid in new_status:
        fields = line.split('|')
        # fields: ['', ' Txxx ', ' 难题 ', ' 所需机制 ', ' 撞 C ', ' 状态 ', '']
        fields[5] = ' ' + new_status[tid] + ' '
        lines[i] = '|'.join(fields)
        changed += 1

io.open(P, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('updated rows =', changed)
