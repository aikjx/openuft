# -*- coding: utf-8 -*-
r"""`so10_errorbar_propagation.py` 的牙齿检验：每个变异体必须把**点名**的判据打红。

规矩（本目录红线）
----------------
* "全绿"不是证据。误差棒这类判据有两种假绿：协方差矩阵被降级成对角、或传播根本没接在
  引擎的解上。本驱动对每条判据种一个缺陷，要求它按名字变红。
* 解析判决行的正则**不许凭格式记忆写**：这里 import 被测模块、调用它自己的 `ok()` 铸一枚
  金丝雀，要求解析器原样吐回该名字；吐不回即 INVALID（退出码 2）。2026-09-26 同一批仪器里
  有一条驱动就因为把 `[%-8s]` 猜成 `[FAIL]` 而把 11 枚真捕获全报成 MISSED。
* 未变异基线必须打印判决行且 rc=0，否则整轮 INVALID。
* 变异体写在临时目录，**不改归档**；版面 JSON 也只落在临时目录。

运行：`python -B so10_errorbar_teeth.py`
退出码：0 = 全部 CAUGHT/CLEAN；1 = 有 MISSED/CRASH；2 = 驱动本身无效。
"""
import os
import re
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, 'so10_errorbar_propagation.py')
SUM = re.compile(r'PASS (\d+) / FAIL (\d+)')
GATE = re.compile(r'\[\s*PASS\s*\]\s+(\S+)')
FAILG = re.compile(r'\[\s*FAIL\s*\]\s+(\S+)')

# (名称, 原文, 变异后, 必须变红的判据)
# 首跑（2026-09-26）对表时有两枚"预期"是我写错的，已按实测改成它们真正指向的门：
#   * 原 m2 把 Σ_A 整个降级成"只留对角"，但 J⁻¹ 仍会在传播后重新造出非对角元 ⇒ E4 按构造
#     测的是**传播后**的交叉项，它不该为输入侧去相关负责；改成只剥掉 SA 的非对角元（方差
#     逐项保持），E4 不再被期待，红点归给专门管交叉项的 cov2 变异体。
#   * 原 m9 是"预期全绿的阳性对照"（σ 全部翻倍），可 E3 的比值 18.2 倍在 σ×2 后掉到 9.1
#     倍、**低于它自己的 10 倍门槛**而变红。这不是门禁失效：它证明传播带确实由声明的输入 σ
#     驱动（不是写死的），于是把它登记成打破者并记下"10 倍门槛只剩 1.8 倍余量"这条读数。
MUTANTS = [
    ('m1_inverse_not_transposed',
     "            c[j][i] = ((-1.0) ** (i + j)) * (mm[0][0] * mm[1][1] - mm[0][1] * mm[1][0]) / d",
     "            c[i][j] = ((-1.0) ** (i + j)) * (mm[0][0] * mm[1][1] - mm[0][1] * mm[1][0]) / d",
     {'E2'}),
    ('m2_input_correlation_stripped',
     "    SA = simat(JA, Sx)\n    corr12",
     "    SA = simat(JA, Sx)\n    for _i in range(3):\n        for _j in range(3):\n"
     "            if _i != _j:\n                SA[_i][_j] = 0.0\n    corr12",
     {'E1'}),
    ('m3_cross_covariance_dropped_in_tau_bar',
     "        cov2 = [[SU[ptg][ptg], SU[ptg][pag]], [SU[pag][ptg], SU[pag][pag]]]",
     "        cov2 = [[SU[ptg][ptg], 0.0], [0.0, SU[pag][pag]]]",
     {'E4'}),
    ('m4_elasticity_column_zeroed',
     "        col = matvec(Jinv, e)",
     "        col = [0.0, 0.0, 0.0]",
     {'E6'}),
    ('m5_hadronic_inflation_removed',
     "        s_tot = math.sqrt(r['sigma_ln_tau_full'] ** 2 + LN_HAD ** 2)",
     "        s_tot = r['sigma_ln_tau_full']",
     {'E8'}),
    ('m6_print_uses_precision_r',
     "    return repr(v)",
     "    return '%.10r' % v",
     {'E8b'}),
    ('m7_spread_quoted_as_the_bar',
     "    spread = math.log(max(mg_all) / min(mg_all)) if len(mg_all) > 1 else 0.0",
     "    spread = max(r['sigma_ln_MGUT'] for r in rows)",
     {'E3'}),
    ('m8_zero_input_control_not_zeroed',
     "    SA0 = [[0.0] * 3 for _ in range(3)]",
     "    SA0 = [[1e-3 if i == j else 0.0 for j in range(3)] for i in range(3)]",
     {'E5'}),
    ('m9_z_counter_decorative',
     "        r['ln_tau_over_SK'] = math.log(r['tau_p_yr']) - sk",
     "        r['ln_tau_over_SK'] = 0.0",
     {'E7'}),
    ('m10_sigma_doubling_moves_the_bar',
     "    sig = [s for _, _, s, _ in INPUTS]",
     "    sig = [2.0 * s for _, _, s, _ in INPUTS]",
     {'E3'}),
    # E9 钉的是"协方差按 σ 的**平方**走、带按 σ 的一次方走"这件事：把 λ² 写成 λ 是一个
    # 会算错齐次阶数的真实缺陷（bar2 = √λ·bar ≠ λ·bar，偏差 0.293），不是把门槛放松。
    ('m11_homogeneity_trial_uses_linear_scaling',
     "        SUx = simat(Jinvx, [[LAM * LAM * SA[i][j] for j in range(3)] for i in range(3)])",
     "        SUx = simat(Jinvx, [[LAM * SA[i][j] for j in range(3)] for i in range(3)])",
     {'E9'}),
]


def run(path):
    # 变异体落在临时目录：ROOT（版面落点）跟着副本走，而引擎 `so10_chain` 必须仍从归档目录
    # 解析，否则"崩在 import"会被记成一次捕获。PYTHONPATH 排在脚本目录之后，正好只用它兜底。
    env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONPATH=HERE)
    p = subprocess.run([sys.executable, path, '--strict'], capture_output=True,
                       text=True, encoding='utf-8', errors='replace', env=env,
                       cwd=os.path.dirname(path))
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def check_parser():
    """把解析器钉在生产者自己的打印上：借它的 ok() 铸一枚金丝雀。"""
    sys.path.insert(0, HERE)
    import so10_errorbar_propagation as M
    out = []
    real = sys.stdout

    class Cap(object):
        def write(self, s):
            out.append(s)

        def flush(self):
            pass
    sys.stdout = Cap()
    try:
        M.ok('CANARY9', '金丝雀', True, 'detail')
    finally:
        sys.stdout = real
    txt = ''.join(out)
    got = {m.group(1) for m in GATE.finditer(txt)} | {m.group(1) for m in FAILG.finditer(txt)}
    return 'CANARY9' in got, txt.strip()[:60]


def check_mint():
    r"""引用令牌铸造器 `s()` 的两枚样例：**该红的红**（同键铸成两串 ⇒ 抛）＋**该绿的绿**（同键同串 ⇒ 静默复用）。

    `s()` 是"判据行印出来的串 == 版面 `citable` 里的串"这条唯一数据源保证的实现方。尺子只在
    文档侧（`so10_errorbar_doc_check.py`）量结果、不钉实现，于是给它补一对样例：删掉冲突检查
    则红样例失效，把它改成无条件抛则绿样例失效。
    """
    sys.path.insert(0, HERE)
    import so10_errorbar_propagation as M
    M.CIT['TEETH_MINT'] = '1.0000'
    red = False
    try:
        M.s('TEETH_MINT', '%.3f', 1.0)          # '1.000' ≠ '1.0000' ⇒ 必须抛
    except AssertionError:
        red = True
    green = True
    try:
        green = (M.s('TEETH_MINT', '%.4f', 1.0) == '1.0000')   # 同串 ⇒ 必须静默复用
    except AssertionError:
        green = False
    M.CIT.pop('TEETH_MINT', None)
    return red, green


def main():
    src = open(TARGET, encoding='utf-8').read()
    pinned, sample = check_parser()
    if not pinned:
        print('INVALID: 解析器没有从生产者自己的 ok() 打印里取回金丝雀名（样例=%s）' % sample)
        return 2
    print('解析器已钉在生产者的 ok() 上（金丝雀 CANARY9 原样取回；样例：%s）' % sample)
    mint_red, mint_green = check_mint()
    if not (mint_red and mint_green):
        print('INVALID: 引用令牌铸造器 s() 的样例没过（该红的红=%s／该绿的绿=%s）⇒'
              ' "判据行与版面 citable 同源"这条保证无人守着' % (mint_red, mint_green))
        return 2
    print('令牌铸造器已验（冲突必抛 = %s，同串静默复用 = %s）' % (mint_red, mint_green))
    tmp = tempfile.mkdtemp(prefix='ebteeth_')
    base = os.path.join(tmp, 'baseline.py')
    with open(base, 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    rc, out = run(base)
    mm = SUM.search(out)
    if not mm or rc != 0:
        print('INVALID: 未变异基线没有判决行或 rc=%d（判决行是本轮的引用资格）' % rc)
        print(out[-1200:])
        return 2
    print('基线：PASS %s / FAIL %s rc=%d' % (mm.group(1), mm.group(2), rc))
    n_caught = n_missed = n_crash = 0
    red_all = set()
    for i, (name, old, new, expect) in enumerate(MUTANTS):
        c = src.count(old)
        if c != 1:
            print('INVALID: %s 的锚点命中 %d 次（期望 1）' % (name, c))
            return 2
        p = os.path.join(tmp, 'mut%d.py' % i)
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write(src.replace(old, new, 1))
        rc, out = run(p)
        r = {m.group(1) for m in FAILG.finditer(out)}
        red_all |= r
        mm = SUM.search(out)
        tally = ('PASS %s/FAIL %s' % (mm.group(1), mm.group(2))) if mm else '无判决行'
        if not mm:
            n_crash += 1
            state = 'CRASH'
        elif not expect and rc == 0:
            n_caught += 1
            state = 'CLEAN(阳性对照)'
        elif not expect and rc != 0:
            n_missed += 1
            state = 'MISSED(对照却红了 %s)' % sorted(r)
        elif expect <= r:
            n_caught += 1
            state = 'CAUGHT'
        else:
            n_missed += 1
            state = 'MISSED(缺 %s)' % sorted(expect - r)
        print('  %-38s %-22s rc=%d %-16s 红=%s' % (name, state, rc, tally,
                                                   sorted(r) if r else '[]'))
    covered = {'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E8b', 'E9'}
    print('\n牙齿检验：%d CAUGHT/CLEAN / %d MISSED / %d CRASH（共 %d 个变异体）'
          % (n_caught, n_missed, n_crash, len(MUTANTS)))
    print('判据覆盖：%d/%d（被点名红过 = %s；未覆盖 = %s）'
          % (len(covered & red_all), len(covered), sorted(covered & red_all),
             sorted(covered - red_all) or '无'))
    return 0 if (n_missed == 0 and n_crash == 0 and covered <= red_all) else 1


if __name__ == '__main__':
    sys.exit(main())
