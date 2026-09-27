# -*- coding: utf-8 -*-
"""`spiral_c35_beta_universality.py` 的牙齿检验：每个变异体必须把**点名**的判据打红。

为什么需要它（本目录红线）
------------------------
"13 条判据全绿"本身不是证据。C35 里最容易假绿的有三类：
①容差型 [Q3]/[Q3c]——容差写大了什么都放过，或者根本没接在 RK4 的输出上；
②不变量型 [Q4]——断言的是"比值不随 λ 动"，若比值压根没把 λ 乘到两端，这条也恒绿；
③误差棒型 [Q8a]/[Q8b]——把字面书写精度传成棒，如果传播路是死的（返回 0），判据只会更绿。
本驱动对每一条判据种一个真实缺陷（改公式、改符号、改本底减法、改书写精度口径、
改标定靶），要求它按名字变红；另外四个变异体是**预期全绿**的阳性对照
（换 coarse 网格、换"零信号"用的 eps、换 λ 名单、换 φ 的算式），
用来证明这些判据不是"见谁红"。

这一轮驱动**自己也被咬过一次**，两条教训写死在下面：
* 解析器不能猜版式。第一版按 C25 的 `[FAIL]` 找红名单，而 C35 的 rec() 用
  `[%-8s]` 补空格 ⇒ 红集合恒空，变异体照样 rc=1，覆盖表 0/13 才暴露它。
  现在 `check_parser()` 直接 import 被测脚本、用它的 rec() 生成一行 FAIL，
  读不回那个名字就整轮 INVALID——解析器被钉在产生者的代码上，而不是我的猜测上。
* 阳性对照不能只验"没红"。`[Q3]` 头注里"φ 用乘式还是累加式"这句话是个**数值断言**，
  所以 pc4 要求它的 [3] 段与基线**逐字节相同**（实测确实相同：本底相减把公共模
  误差对消掉了），而不是只要求它不红。

规矩（与 spiral_c25_scan_teeth.py 同）
------------------------------------
* 未变异基线必须打印判决行且 rc=0；否则整轮 INVALID（退出码 2）。
* 崩溃/无判决行单独计 CRASH 并算失败——只有被测守卫报错才算捕获，容差不构成捕获。
* 变异体写在临时目录，**不改归档**；版面 JSON 也只落在临时目录
  （扫描脚本的版面钉在"脚本自己旁边"，复制品旁边就是临时目录）。
* 最后还要**覆盖率**：基线里每一条 PASS 判据都必须至少被一个变异体点名，
  否则该轮不算收口（退出码 1）。

运行：python spiral_c35_beta_teeth.py
退出码：0 = 全部 CAUGHT/CLEAN 且判据全覆盖；1 = 有 MISSED / CRASH / DRIFT / 漏覆盖；
        2 = 驱动本身无效。
"""
import importlib.util
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
                      'spiral_c35_beta_universality.py')
# 判决行版式的产生者是 spiral_c35_beta_universality.py 的 rec()（`[%-8s] %-9s`），
# 与 C25 那台的 `[%s]` 不同。两边不一致时 check_parser() 会直接判 INVALID。
SUM = re.compile(r'PASS (\d+) / FAIL (\d+)')
GATE = re.compile(r'\[\s*PASS\s*\]\s+(\S+)')
FAIL = re.compile(r'\[\s*FAIL\s*\]\s+(\S+)')
SEC3 = re.compile(r'\n\[3\].*?(?=\n\[\d)', re.S)

# (名称, 锚点(源码里必须恰好命中 1 次), 变异后, 必须变红的判据 ID 集合,
#  是否要求 [3] 段与基线逐字节相同)
# 第 5 条注释写的是**这个缺陷为什么会让点名的判据变红**，不是"跑出来是什么就是什么"。
MUTANTS = [
    # [Q1] 断言双精度复算 == 仓库 250 位版面。逐行星动版面值 ⇒ 只有对账那条腿该红。
    ('m1_gr250_venus_tampered',
     '8.624863899085765', '8.624864899085765', {'Q1-金星'}, False),
    ('m2_gr250_mercury_tampered',
     '42.98203636043861', '42.98203736043861', {'Q1-水星'}, False),
    ('m3_gr250_earth_tampered',
     '3.8388229840403927', '3.8388239840403927', {'Q1-地球'}, False),
    # [Q2] 用开普勒第三定律独立复算周期。把 a 的幂改半格 ⇒ 独立路失效。
    ('m4_kepler_power_off',
     'math.sqrt(a ** 3 / GM)', 'math.sqrt(a ** 3.5 / GM)', {'Q2'}, False),
    # [Q3] 的被测对象是 RK4 右端项。扰动力反号 ⇒ 数值进动变负，残差 ≈ 2×闭式。
    # 实测**不**连带 [Q3c]：二阶系数 B 是 eps 的偶函数（B∝x²），反号看不见，
    # 这条边界记在 [Q3c] 自己的语义里（它只钉 x² 项的大小，不钉符号）。
    ('m5_rk4_perturbation_sign',
     'A + eps_loc * u * u - u', 'A - eps_loc * u * u - u', {'Q3'}, False),
    # [Q3c] 的语义就是"系数被独立复现"。把推导值退回漏掉圆半径位移的 3πx²
    # ⇒ 与实测 B 差 8.6 个棒，dev5<4 必红（[Q3] 的容差仍够宽，不连带）。
    ('m6_second_order_3pi',
     'return 5.0 * math.pi * x * x', 'return 3.0 * math.pi * x * x', {'Q3c'}, False),
    # [Q3]/[Q3c] 接的是"减去 eps=0 本底"这条通路。去掉减法 ⇒ 可观测量回到 2π 本身：
    # 残差 ≈ 2π（[Q3] 红），反解出的 B 变成 −2π·15/240 = −0.3927（[Q3c] 红）。
    # [Q3b] 实测不红——本底只是变大（极差 8.4e-9），不是转成截断支配。
    ('m7_baseline_subtraction_removed',
     'return (phi_grav - phi_flat)', 'return phi_grav', {'Q3', 'Q3c'}, False),
    # [Q3b] 是示警判据：它断言"当前网格族上，细化没有按 h⁴ 收敛"。把默认网格
    # 从 5e-4 抬到 2e-3（≈ 4 千步/圈）⇒ 相邻两级之差在某一档恰好为 0 ⇒ q=0 红。
    ('m8_default_grid_raised',
     '    h = 5e-4', '    h = 2e-3', {'Q3b'}, False),
    # [Q4] 的载荷是"λ 乘到了比值两端"。只乘分子（分母固定用标定 β）⇒
    # 比值随 λ 走 0.4/1/1.7/10 倍，漂移从 2.7e-16 跳到 O(1)，本条必红。
    ('m9_lambda_applied_to_one_side',
     'per_century_of(law_binet, lam * beta_binet, a0, e0, T0))',
     'per_century_of(law_binet, beta_binet, a0, e0, T0))', {'Q4'}, False),
    # 反向探针（**预期 [Q4] 仍绿**的缺陷）：把草稿式改成 β² 。约掉的条件只是
    # "两端共用同一个 β"，与幂次无关 ⇒ [Q4] 结构上看不见这种缺陷，红的是
    # [Q5]（结构比）与 [Q7]（信号大小）。这一条不是牙齿，是把 [Q4] 的**负空间**
    # 钉进版面：它证明 [Q4] 绿只说明 β 不区分行星，不说明 β 是一次。
    ('m10_draft_beta_squared_Q4_blind',
     '3.0 * math.pi * beta * GM / (C * C * a ** 3',
     '3.0 * math.pi * beta * beta * GM / (C * C * a ** 3', {'Q5', 'Q7'}, False),
    # [Q5] 断言 草稿/Binet == a_水星/a_行星（两式只差一个 1/a）。把 Binet 的 p
    # 指数从 2 改成 1.5 ⇒ 结构比不成立；[Q3] 第二例的闭式直接调 law_binet ⇒ 连带红。
    ('m11_lawbinet_exponent',
     'beta / semilatus(a, e) ** 2', 'beta / semilatus(a, e) ** 1.5', {'Q3', 'Q5'}, False),
    # [Q6] 判"金星参考值是否独立观测"。把 8.62 换成与预言差 7% 的数 ⇒
    # 参考值看起来像观测了，循环性守卫必须变红。
    ('m12_venus_ref_looks_observed',
     '0.615197, 8.62),', '0.615197, 8.0),', {'Q6'}, False),
    # [Q7] 判决力 = 两式之差 / 水星锚点极差。标定靶 43.03→43.55 ⇒ 两式之差按
    # 几何项线性放大约 11 倍，越过 0.1 这条线（其余判据用的是同一个几何项的
    # 比值或棒，故不连带）。
    ('m13_calibration_target_raised',
     '43.03 - gr_pc[', '43.55 - gr_pc[', {'Q7'}, False),
    # [Q8a] 把轨道元字面末位当 ±0.5 末位传播。"小数位"口径整体放宽 100 倍
    # ⇒ 轨道元这条腿自己就超过 1e-4，合成棒也破 [Q8b] 的 1/10 线。
    ('m14_written_precision_inflated',
     '    return 0.5 * 10.0 ** (-decimals)', '    return 0.5 * 10.0 ** (2.0 - decimals)',
     {'Q8a', 'Q8b'}, False),
    # [Q8b] 的主导腿是标定靶末位。只把它放大 100 倍（轨道元腿不动）⇒ 只有
    # [Q8b] 该红，证明"主导腿 = 标定靶末位"这条结论接在真实数值上。
    ('m15_anchor_leg_only_inflated',
     '    d_anchor = abs_ulp_dec(', '    d_anchor = 100.0 * abs_ulp_dec(', {'Q8b'}, False),
    # ---- 阳性对照：预期一条都不红 ----
    # 极差本底跨 4 档网格，coarse 这一点选 0.02 还是 0.05 不该改变任何判决
    # （否则"本底"其实是被网格选择钉出来的假量）。反向实测也有信息：把这条的
    # same 打开成 True 时驱动报 DRIFT ⇒ **判决**不动但 [3] 的极差/容差数值会动，
    # 所以引用任何一条容差都要连 H_COARSE 一起报（该披露记在常量定义处）。
    ('pc1_coarse_grid_GREEN', 'H_COARSE = 0.02', 'H_COARSE = 0.05', set(), False),
    # EPS_NULL 只喂给打印用的反面教材，明确**不是**判据；换成 1e-14 必须全绿。
    ('pc2_null_eps_GREEN', 'EPS_NULL = 1.0e-12', 'EPS_NULL = 1.0e-14', set(), False),
    # β 约掉与 λ 取值无关：把 λ 名单换成跨 4 个数量级的另一组，判据必须不动。
    ('pc3_lambda_list_GREEN', 'for lam in (0.4, 1.0, 1.7, 10.0):',
     'for lam in (0.1, 1.0, 3.3, 700.0):', set(), False),
    # [Q3] 头注里"φ 用乘式还是累加式"是一个**数值断言**（公共模误差被本底减法
    # 对消），所以这里不止要求不红，还要求 [3] 段与基线逐字节相同。
    ('pc4_phi_accumulation_identical',
     '            phin = (step + 1) * h_loc', '            phin = phi + h_loc',
     set(), True),
]


def run(path):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    p = subprocess.run([sys.executable, path, '--strict'],
                       capture_output=True, text=True, encoding='utf-8',
                       errors='replace', env=env, cwd=os.path.dirname(path))
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def red_ids(out):
    return {m.group(1) for m in FAIL.finditer(out)}


def sec3(out):
    m = SEC3.search(out)
    return m.group(0) if m else None


def check_parser():
    """驱动的自杀式守卫：判据名的解析必须由**产生者自己的打印**来验。

    这一发是真打过人的：驱动第一版把版式猜成 `[FAIL]`，而 C35 的 rec() 用
    `[%-8s]` 补空格 ⇒ 红集合恒为空，变异体照样 rc=1，看起来"全打红了"，
    其实一条名字都没读到（覆盖表 0/13 才暴露它）。
    """
    import contextlib
    import io
    spec = importlib.util.spec_from_file_location('_c35_under_test', TARGET)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # 只执行到定义，main 有 __main__ 守卫
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod.rec('CANARY', '驱动版式探针', 'FAIL', '这一行不是物理结论，只验版式')
    got = red_ids(buf.getvalue())
    if got != {'CANARY'}:
        print('INVALID: 解析器读不到产生者打印的判据名（读到 %s）'
              % (sorted(got) if got else '空集合'))
        return False
    return True


def main():
    if not check_parser():
        return 2
    src = open(TARGET, encoding='utf-8').read()
    tmp = tempfile.mkdtemp(prefix='c35teeth_')
    base = os.path.join(tmp, 'baseline.py')
    with open(base, 'w', encoding='utf-8', newline='\n') as f:
        f.write(src)
    rc, out = run(base)
    mm = SUM.search(out)
    if not mm or rc != 0:
        print('INVALID: 未变异基线没有判决行或 rc=%d（判决行是本轮的引用资格）' % rc)
        print(out[-1500:])
        return 2
    gates = set(GATE.findall(out))
    base_sec3 = sec3(out)
    if base_sec3 is None:
        print('INVALID: 基线里定位不到 [3] 段，pc4 的"逐字节相同"没法判')
        return 2
    print('基线：%s rc=%d，%d 条 PASS 判据待覆盖：%s'
          % ('PASS %s / FAIL %s' % (mm.group(1), mm.group(2)), rc, len(gates), sorted(gates)))
    n_caught = n_missed = n_crash = n_drift = 0
    covered = set()
    for i, (name, old, new, expect, same) in enumerate(MUTANTS):
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
        drift = same and (sec3(out) != base_sec3)
        if not mm:
            n_crash += 1
            state = 'CRASH'
        elif expect <= r and not drift:
            n_caught += 1
            state = 'CAUGHT' if expect else 'CLEAN(阳性对照)'
            covered |= expect
        elif drift:
            n_drift += 1
            state = 'DRIFT([3] 段与基线不同)'
        else:
            n_missed += 1
            state = 'MISSED(缺 %s)' % sorted(expect - r)
            covered |= (expect & r)
        extra = sorted(r - expect)
        print('  %-36s %-24s rc=%d %-18s 红=%s%s'
              % (name, state, rc, tally, sorted(r) if r else '[]',
                 ('  连带红=%s' % extra) if (state == 'CAUGHT' and extra) else ''))
    print('\n牙齿检验：%d CAUGHT/CLEAN / %d MISSED / %d CRASH / %d DRIFT'
          '（共 %d 个变异体，其中 %d 个预期全绿的阳性对照）'
          % (n_caught, n_missed, n_crash, n_drift, len(MUTANTS),
             sum(1 for m in MUTANTS if not m[3])))
    uncovered = sorted(gates - covered)
    print('判据覆盖：%d/%d 条 PASS 判据被点名%s'
          % (len(gates) - len(uncovered), len(gates),
             '' if not uncovered else '，漏：%s' % uncovered))
    return 0 if (n_missed == 0 and n_crash == 0 and n_drift == 0 and not uncovered) else 1


if __name__ == '__main__':
    sys.exit(main())
