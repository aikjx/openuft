# -*- coding: utf-8 -*-
"""零螺距闭设定理引擎的变异体自检：每枚针必须被一具 named 变异体打破。

为什么要有这个文件
------------------
本轮的承重结论是「非零螺距 ∧ 严格传播 ∧ 量子化 = 空集」。这种「恒为空」的断言
最容易被写成一枚看不见东西的针：判据塌空、对照塌空、通道抄成同源，都会让面全绿
而结论已死。故本文件把引擎的源码当作被试对象，逐枚注入语义破坏，要求：
  1) 未变异的基线在临时目录里 rc=0（证明变异跑没有偷走仓库写盘）；
  2) 每枚变异体 rc!=0，且红的正是它在登记表里指定的那枚守卫；
  3) 变异跑全程 OUTDIR 重定向到临时目录，仓库三件套 md5 逐字节不变。
仓库零污染；所有临时产物由 tempfile 自己清理。
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE / '磁场闭环螺旋_零螺距闭设定理与最小修法代价_攻破_2026-10-18.py'
ROUND = HERE.parent
DATA = ROUND / '数据'
STEM = '磁场闭环螺旋_零螺距闭设定理与最小修法代价_攻破_2026-10-18'
SRC = ENGINE.read_bytes()

# 变异体表：名字 -> (被替换的源码片段, 替换后的片段, 指定必须变红的守卫号)
MUTANTS = {
    'M1_strip_quantization': (
        "            q = is_int(j)\n",
        "            q = True\n",
        'G2-1'),
    'M2_arm2_always_zero_pitch': (
        "            _b = Fr(_m - 1, 1) / _k\n",
        "            _b = Fr(0, 1) / _k\n",
        'G2-5'),
    'M3_pifree_D_sign': (
        "    return -(j * j * a * a + (j * j - 1) * b * b) / (b * b * (a * a + b * b))\n",
        "    return -(j * j * a * a + (j * j + 1) * b * b) / (b * b * (a * a + b * b))\n",
        'G1-4'),
    'M4_control_blinded': (
        "                if pr:\n                    arm1['notquant_prop'] += 1\n"
        "                    if _b > 0:\n                        arm1['notquant_prop_bpos'] += 1\n",
        "                if pr:\n                    arm1['notquant_prop'] += 1\n"
        "                    if False:\n                        arm1['notquant_prop_bpos'] += 1\n",
        'G3-1'),
    'M5_famA_wrong_quantum': (
        "            ve = kappa2_pifree(_a, _b, Fr(_n))\n",
        "            ve = kappa2_pifree(_a, _b, Fr(0))\n",
        'G6-1'),
    'M6_phase_from_unoverridden_b': (
        "            d03_rows.append(dict(n=_n, m=_m, b=b_used, kn=kn, phase=_m - kn * b_used, k2=k2))\n",
        "            d03_rows.append(dict(n=_n, m=_m, b=b_used, kn=kn, phase=_m - kn * float(code_b), k2=k2))\n",
        'G7-2'),
    'M7_integrality_needle_dead': (
        "    return ceil_lo <= floor_hi, ceil_lo, floor_hi\n",
        "    return False, ceil_lo, floor_hi\n",
        'G8-0'),
    'M8_cost_channel_self_copy': (
        "        chan_a[f] = len(re.findall(comb, t))\n",
        "        chan_a[f] = raw_sum[f]\n",
        'G9-2'),
    'M9_duplicate_guard_code': (
        "guard('G4-5', nt_ratio_set == {Fr(1)},\n",
        "guard('G4-4', nt_ratio_set == {Fr(1)},\n",
        'G11-1'),
}


def run_engine(source, workdir):
    """把（可能被变异的）源码写进临时目录跑；OUTDIR 一律指向临时目录。"""
    script = Path(workdir) / 'engine_under_test.py'
    script.write_bytes(source)
    env = dict(os.environ)
    env['UFT_ZEROPITCH_OUTDIR'] = str(Path(workdir) / 'out')
    proc = subprocess.Popen([sys.executable, str(script)], cwd=str(workdir),
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    out = proc.communicate()[0].decode('utf-8', 'replace')
    return proc.returncode, out


CRLF = b'\r\n' in SRC


def anchor(text):
    """锚点按引擎自身的行尾类型归一（行尾判据属于对象，不属于我的习惯）。"""
    b = text.encode('utf-8')
    return b.replace(b'\n', b'\r\n') if CRLF else b


def guard_codes_in_source():
    """引擎里注册的针号 = 字面 guard('X' + 代价台账循环的派生号（G9-<digit>[b]）。
    派生号不许手打，由 FIXES 表的 ('P<n>', …) 行现读——针名单必须覆盖全部要红的号。
    拼接写法 guard('G9-' + code[1]) 被字面正则截成 'G9-'，那不是号，是前缀：
    必须按源码自己的拼接证据剔掉，展开由派生通道负责（留着它＝一个假号混进名单）。"""
    lit = set(x.decode() for x in re.findall(rb"guard\('([0-9A-Za-z\-]+)'", SRC))
    prefixes = set(x.decode() for x in re.findall(rb"guard\('([0-9A-Za-z\-]+)'\s*\+", SRC))
    codes = lit - prefixes
    derived = set()
    for mm in re.finditer(rb"^    \('(P[0-9])',", SRC, re.M):
        base = 'G9-' + mm.group(1)[1:].decode()
        codes.add(base)
        codes.add(base + 'b')
        derived.add(base)
        derived.add(base + 'b')
    assert prefixes, '源码里没有拼接型 guard，派生通道却还在跑（展开器已失去对象）'
    assert derived, '派生针名单塌空：台账循环的 (' + "'Pn'" + ',) 行形变了，8 枚针会安静消失'
    for d in derived:
        assert d.startswith(tuple(prefixes)), '派生号 %r 不是任何拼接前缀铸出来的' % d
    return codes


def md5_of_products():
    got = {}
    for suffix in ('.json', '.md', '_report.txt'):
        p = DATA / (STEM + suffix)
        got[p.name] = hashlib.md5(p.read_bytes()).hexdigest() if p.exists() else '<absent>'
    return got


class MutantBattery(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='zeropitch_mutants_')
        self.addCleanup(self.temp.cleanup)
        self.assertTrue(SRC, '引擎源码必须非空')

    def test_engine_exists_and_registers_every_named_mutant(self):
        """被试对象必须是本轮那份引擎；每枚变异体指定的守卫号必须真是引擎里注册过的针。"""
        self.assertEqual(ENGINE.name, STEM + '.py')
        self.assertGreater(len(SRC), 20000, '引擎源码只有 %d 字节，不可能是完整件' % len(SRC))
        codes = guard_codes_in_source()
        self.assertGreaterEqual(len(codes), 40, '引擎里解析到的守卫号太少（解析器或写法坏了）：%d' % len(codes))
        for name, (old, new, want) in sorted(MUTANTS.items()):
            self.assertIn(want, codes, '%s 指定的守卫 %s 不在引擎的针名单里' % (name, want))

    def test_baseline_runs_clean_in_temp(self):
        rc, out = run_engine(SRC, self.temp.name)
        self.assertEqual(0, rc, '基线（未变异）应 rc=0，实得 %d：%s' % (rc, out[-1500:]))
        self.assertIn('EXIT 0', out)
        man = [l for l in out.splitlines() if l.startswith('守卫 ')]
        self.assertEqual(1, len(man), '面必须自报守卫数：%r' % (man,))
        n = int(re.search(r'守卫 (\d+)/', man[0]).group(1))
        self.assertEqual(n, len(guard_codes_in_source()),
                         '面自报的守卫数须等于源码里注册的针数（自报与实数分家即第 109 类）：%d vs %d'
                         % (n, len(guard_codes_in_source())))

    def test_every_mutant_is_caught_by_its_named_guard(self):
        for name, (old, new, want_guard) in sorted(MUTANTS.items()):
            a = anchor(old)
            b = anchor(new)
            self.assertEqual(1, SRC.count(a), '%s 的锚点在源码里出现次数不是 1' % name)
            mutated = SRC.replace(a, b)
            self.assertNotEqual(SRC, mutated, '%s 的替换没落地（锚点写错＝恒绿假证据）' % name)
            rc, out = run_engine(mutated, self.temp.name)
            self.assertNotEqual(0, rc, '%s 未被任何守卫抓住（rc=0）——该结论没有牙齿：%s'
                                % (name, out[-800:]))
            red = [l for l in out.splitlines() if l.startswith('GUARD FAILED:')]
            self.assertEqual(1, len(red), '%s 应当恰好红在一枚守卫上，实得 %r' % (name, red))
            self.assertEqual(want_guard, red[0].split()[2],
                             '%s 指定红 %s，实得 %r' % (name, want_guard, red[0]))

    def test_mutants_never_touch_the_repo_products(self):
        before = md5_of_products()
        for name, (old, new, _g) in sorted(MUTANTS.items()):
            run_engine(SRC.replace(anchor(old), anchor(new)), self.temp.name)
        self.assertEqual(before, md5_of_products(), '变异跑动了仓库三件套：%r -> %r' % (before, md5_of_products()))

    def test_pin_list_has_no_reused_code(self):
        """G11-1 的第二通道：盘上的针名单必须逐号唯一。
        复用编号时「恰红一枚」的归因失效，而 size 对账会被两处错互相抵消而假绿。"""
        jpath = DATA / (STEM + '.json')
        if not jpath.exists():
            self.skipTest('本轮面尚未落盘（正式跑之后再跑这条）')
        face = json.loads(jpath.read_bytes().decode('utf-8'))
        rows = [g['code'] for g in face['guards']]
        self.assertEqual(len(rows), len(set(rows)),
                         '盘上守卫名单有复用编号：%r' % sorted(set(c for c in rows if rows.count(c) > 1)))
        self.assertEqual(set(rows), guard_codes_in_source(),
                         '盘上针名单与源码解析出的名单必须同集（差集即漏针或假号）')

    def test_needle_is_necessary_counterfactual(self):
        """反证 G11-1 不是装饰：撤掉这根针、把编号复用回去，引擎必须 rc=0 并把重复号印到盘上。
        若撤针后仍然红，说明红来自别处，这根针本身看不见任何东西。"""
        needle = ("guard('G11-1', _dups == [],\n"
                  "      '守卫编号必须互不相同（本引擎现扫 %d 条守卫，重复 %d 个）：%r' % (len(_codes), len(_dups), _dups))\n")
        self.assertEqual(1, SRC.count(anchor(needle)), '撤针锚点出现次数不是 1')
        no_needle = SRC.replace(anchor(needle), b'')
        self.assertNotEqual(SRC, no_needle, '撤针替换没落地')
        rc0, out0 = run_engine(no_needle, self.temp.name)
        self.assertEqual(0, rc0, '撤针但未复用时须 rc=0（针没有误伤），实得 %d：%s' % (rc0, out0[-500:]))
        dup_src = no_needle.replace(anchor("guard('G4-5', nt_ratio_set == {Fr(1)},\n"),
                                    anchor("guard('G4-4', nt_ratio_set == {Fr(1)},\n"))
        self.assertNotEqual(no_needle, dup_src, 'M9 的锚点没落地')
        rc1, out1 = run_engine(dup_src, self.temp.name)
        self.assertEqual(0, rc1, '撤针后复用编号必须能安静落盘（红说明另有针在管，G11-1 是装饰）：%d：%s'
                         % (rc1, out1[-500:]))
        tj = Path(self.temp.name) / 'out' / '数据' / (STEM + '.json')
        self.assertTrue(tj.exists(), '反证跑没写出临时面：%s' % tj)
        trows = [g['code'] for g in json.loads(tj.read_bytes().decode('utf-8'))['guards']]
        dups = sorted(set(c for c in trows if trows.count(c) > 1))
        self.assertEqual(['G4-4'], dups, '临时面须带着那枚复用编号：%r' % dups)

    def test_theorem_face_is_non_vacuous_on_disk(self):
        """读基线面（若存在）：定理的空桶必须由非空对照托住，且跨轮 pin 逐字对账。"""
        jpath = DATA / (STEM + '.json')
        if not jpath.exists():
            self.skipTest('本轮面尚未落盘（正式跑之后再跑这条）')
        face = json.loads(jpath.read_bytes().decode('utf-8'))
        th = face['theorem']
        self.assertEqual(0, th['arm1']['quant_prop_bpos'])
        self.assertGreater(th['arm1']['notquant_prop_bpos'], 0, '阳性对照塌空')
        self.assertEqual(0, th['arm2']['prop_bpos'])
        self.assertGreater(th['arm2']['prop'], 0)
        self.assertEqual([1], th['arm2']['prop_m'])
        self.assertEqual(th['arm1']['quant_prop_bzero'], th['budget_table'][0]['points'])
        self.assertEqual(0, face['family_b_modes']['integer_j'])
        pins = face['cross_round_pins']
        prev = json.loads((DATA / '磁场闭环螺旋光速运动_HTML语料全维审计与整理_2026-10-18.json')
                          .read_bytes().decode('utf-8'))['key_numbers']
        self.assertEqual(prev['c01_grid_neg'], pins['famA_neg_exact'])
        self.assertEqual(prev['c04_n_max'], pins['nmax_paper'])
        self.assertEqual(prev['d03_solutions'], pins['d03_total'])
        self.assertLess(pins['phase_abs_diff'], 1e-15)


if __name__ == '__main__':
    unittest.main(verbosity=2)
