# -*- coding: utf-8 -*-
import io, json, os

base = r'D:\a10\aikjx\code\my_lib'
files = {
    '主册 TUFT_企业级归一化主册_v1.0.md': os.path.join(base, 'TUFT_企业级归一化主册_v1.0.md'),
    '台账 TUFT_归一化台账_v1.0.json': os.path.join(base, 'TUFT_归一化台账_v1.0.json'),
    '流程图 TUFT_全物理现象关系流程图.html': os.path.join(base, 'TUFT_全物理现象关系流程图.html'),
    'ch66 第66章_复谱GradeA_TUFT基频极点与两路互证.md': os.path.join(base, 'openuft', '书籍', 'v1_正文', '第十二编_动力学本征值路线_解锁UFT-3的真实尝试', '第66章_复谱GradeA_TUFT基频极点与两路互证.md'),
}

print('=== Python len() 实测（字符数；utf-8 解码后）===')
for name, path in files.items():
    s = io.open(path, encoding='utf-8').read()
    byte_len = os.path.getsize(path)
    print(f'{name}: len()={len(s)} chars ; on-disk bytes={byte_len}')

# ledger reload + structural checks
d = json.load(io.open(files['台账 TUFT_归一化台账_v1.0.json'], encoding='utf-8'))
print()
print('=== 台账结构校验 ===')
print('version', d['version'])
print('latest_round', d['latest_round'])
print('equation_range', d['equation_range'])
print('latest_erratum', d['latest_erratum'], 'erratum', d['erratum'])
print('four_state strict/conditional/definition/open =',
      d['four_state_counts_approx']['strict'],
      d['four_state_counts_approx']['conditional'],
      d['four_state_counts_approx']['definition'],
      d['four_state_counts_approx']['open'])
print('v53_amplitude_anchor_key_results present =', 'v53_amplitude_anchor_key_results' in d)
print('open_backlog len =', len(d['open_backlog']))
print('backlog[0] round tag =', d['open_backlog'][0][:12])

# master title check
ms = io.open(files['主册 TUFT_企业级归一化主册_v1.0.md'], encoding='utf-8').read()
print()
print('=== 主册校验 ===')
print('title line starts v6.5 =', ms.split(chr(10))[0].startswith('# TUFT 企业级归一化主册 v6.5'))
print('contains v6.5 block =', '★★ v6.5（v53 绝对振幅锚轮收口' in ms)
print('contains E503 =', 'E503' in ms)

# html checks
hs = io.open(files['流程图 TUFT_全物理现象关系流程图.html'], encoding='utf-8').read()
print()
print('=== HTML 校验 ===')
print('sub v6.5 =', 'SSOT v6.5 / E1–E503' in hs)
print('amplitude box =', 'v53 绝对振幅锚：ε 区间' in hs)
print('6.28x next-layer open =', '源激发能 e/f_π 升层项 OPEN' in hs)

# ch66 checks
cs = io.open(files['ch66 第66章_复谱GradeA_TUFT基频极点与两路互证.md'], encoding='utf-8').read()
print()
print('=== ch66 校验 ===')
print('contains 66.16 =', '## 66.16 v53 绝对振幅锚' in cs)
print('contains E503 =', 'E503' in cs)
print('contains 66.15 still =', '### 66.15.6 E502' in cs)
