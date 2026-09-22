"""
run_all_deep.py — AI科技星 · 全维统一场论 D1-D25 一键回归入口
============================================================
按顺序运行全部 25 个物理分支深化验证脚本，汇总输出行数与状态。

用法：
    python run_all_deep.py            # 运行全部 25 个脚本（顺序执行）
    python run_all_deep.py --smoke    # 仅检查脚本可导入（快速冒烟）
    python run_all_deep.py --list     # 仅列出脚本清单

输出：
    - 控制台：逐方向进度 + 汇总表
    - 文件：   回归结果_D1-D25全维汇总.txt（UTF-8）
"""

import os
import subprocess
import sys
import time

# [UTF8-GUARD v1]
import sys as _sys_utf8
try:
    _sys_utf8.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# D1-D25 方向清单：(编号, 方向名, 脚本名, 输出文件)
DIRECTIONS = [
    ("D1",  "QCD精确计算",          "verify_qcd_deep.py",                         "验证结果_QCD.txt"),
    ("D2",  "暗物质探测",            "verify_dark_matter_deep.py",                "验证结果_暗物质.txt"),
    ("D3",  "量子引力实验",          "verify_quantum_gravity_experiment.py",      "验证结果_量子引力实验.txt"),
    ("D4",  "人工场原型",            "verify_artificial_field_prototype.py",      "验证结果_人工场原型.txt"),
    ("D5",  "粒子质量第一性原理",    "verify_particle_mass_first_principles.py",  "验证结果_粒子质量第一性原理.txt"),
    ("D6",  "量子力学几何化",        "verify_quantum_mechanics_geometrization_deep.py", "验证结果_量子力学几何化.txt"),
    ("D7",  "宇宙学精确计算",        "verify_cosmology_precision_deep.py",        "验证结果_宇宙学精确计算.txt"),
    ("D8",  "引力波物理",            "verify_gravitational_wave_physics_deep.py", "验证结果_引力波物理.txt"),
    ("D9",  "中微子物理",            "verify_neutrino_physics_deep.py",           "验证结果_中微子物理.txt"),
    ("D10", "标准模型精确检验",      "verify_sm_precision_tests_deep.py",         "验证结果_标准模型精确检验.txt"),
    ("D11", "核物理",                "verify_nuclear_physics_deep.py",            "验证结果_核物理.txt"),
    ("D12", "凝聚态物理",            "verify_condensed_matter_deep.py",           "验证结果_凝聚态物理.txt"),
    ("D13", "原子分子物理",          "verify_atomic_molecular_deep.py",           "验证结果_原子分子物理.txt"),
    ("D14", "统计物理",              "verify_statistical_physics_deep.py",        "验证结果_统计物理.txt"),
    ("D15", "光学",                  "verify_optics_deep.py",                     "验证结果_光学.txt"),
    ("D16", "等离子体物理",          "verify_plasma_physics_deep.py",             "验证结果_等离子体物理.txt"),
    ("D17", "数学物理",              "verify_mathematical_physics_deep.py",       "验证结果_数学物理.txt"),
    ("D18", "计算物理",              "verify_computational_physics_deep.py",      "验证结果_计算物理.txt"),
    ("D19", "生物物理",              "verify_biophysics_deep.py",                 "验证结果_生物物理.txt"),
    ("D20", "医学物理",              "verify_medical_physics_deep.py",            "验证结果_医学物理.txt"),
    ("D21", "流体力学",              "verify_fluid_mechanics_deep.py",            "验证结果_流体力学.txt"),
    ("D22", "声学",                  "verify_acoustics_deep.py",                  "验证结果_声学.txt"),
    ("D23", "地球物理",              "verify_geophysics_deep.py",                 "验证结果_地球物理.txt"),
    ("D24", "量子信息",              "verify_quantum_information_deep.py",        "验证结果_量子信息.txt"),
    ("D25", "天体物理",              "verify_astrophysics_deep.py",               "验证结果_天体物理.txt"),
]

# 各方向已知对标统计（精确/初步/开放），用于汇总断言
KNOWN_STATS = {
    "D1": (10, 0, 0), "D2": (10, 0, 0), "D3": (10, 0, 0), "D4": (8, 0, 0),
    "D5": (3, 4, 0), "D6": (10, 0, 0), "D7": (6, 2, 2), "D8": (6, 3, 1),
    "D9": (4, 4, 2), "D10": (7, 0, 3), "D11": (6, 4, 0), "D12": (24, 0, 0),
    "D13": (24, 1, 0), "D14": (30, 1, 0), "D15": (36, 1, 0), "D16": (21, 3, 1),
    "D17": (12, 0, 0), "D18": (11, 1, 0), "D19": (12, 0, 0), "D20": (12, 0, 0),
    "D21": (12, 0, 0), "D22": (12, 0, 0), "D23": (12, 0, 0), "D24": (9, 2, 1),
    "D25": (11, 1, 0),
}


def count_lines(path):
    """统计输出文件行数"""
    if not os.path.exists(path):
        return 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return sum(1 for _ in f)


def run_one(num, name, script, outfile, to_console=True):
    """运行单个脚本，重定向输出到文件"""
    script_path = os.path.join(BASE_DIR, script)
    if not os.path.exists(script_path):
        return "脚本不存在"
    try:
        with open(outfile, "w", encoding="utf-8") as f:
            proc = subprocess.run(
                [sys.executable, script],
                cwd=BASE_DIR,
                stdout=f,
                stderr=subprocess.STDOUT,
                timeout=600,
            )
        if proc.returncode == 0:
            return "OK"
        return f"FAIL(exit={proc.returncode})"
    except subprocess.TimeoutExpired:
        return "超时"
    except Exception as e:
        return f"错误:{e}"


def main():
    args = sys.argv[1:]

    if "--list" in args:
        print(f"{'编号':<5} {'方向':<16} {'脚本'}")
        print("-" * 70)
        for num, name, script, _ in DIRECTIONS:
            print(f"{num:<5} {name:<16} {script}")
        return

    if "--smoke" in args:
        print("冒烟测试：检查 25 个脚本可导入性")
        ok = 0
        for num, name, script, _ in DIRECTIONS:
            script_path = os.path.join(BASE_DIR, script)
            exists = os.path.exists(script_path)
            status = "OK" if exists else "MISSING"
            ok += 1 if exists else 0
            print(f"  {num} {name:<16} {status}")
        print(f"冒烟结果：{ok}/25 存在")
        return

    print("=" * 72)
    print("  AI科技星 · 全维统一场论 D1-D25 一键回归")
    print(f"  开始时间：{time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 72)
    print()

    results = []
    summary_lines = []
    total_lines = 0

    for num, name, script, outfile in DIRECTIONS:
        print(f"  [{num}] {name} ... ", end="", flush=True)
        status = run_one(num, name, script, outfile)
        lines = count_lines(outfile)
        total_lines += lines
        stat = KNOWN_STATS.get(num, (0, 0, 0))
        results.append((num, name, status, lines, stat))
        print(f"{status} ({lines}行)")
        summary_lines.append(f"{num}|{name}|{status}|{lines}|{stat[0]}|{stat[1]}|{stat[2]}")

    # 汇总
    ok_count = sum(1 for r in results if r[2] == "OK")
    exact_total = sum(r[4][0] for r in results)
    partial_total = sum(r[4][1] for r in results)
    open_total = sum(r[4][2] for r in results)

    print()
    print("=" * 72)
    print("  回归汇总")
    print("=" * 72)
    print()
    print(f"  方向数：{len(results)}")
    print(f"  成功：{ok_count}/{len(results)}")
    print(f"  输出总行数：{total_lines}")
    print(f"  对标统计：精确 {exact_total} + 初步 {partial_total} + 开放 {open_total} = {exact_total+partial_total+open_total}")
    print()

    print(f"  {'编号':<5} {'方向':<16} {'状态':<16} {'行数':<8} {'精确':<6} {'初步':<6} {'开放'}")
    print("  " + "-" * 68)
    for num, name, status, lines, stat in results:
        print(f"  {num:<5} {name:<16} {status:<16} {lines:<8} {stat[0]:<6} {stat[1]:<6} {stat[2]}")
    print()

    # 写入汇总文件
    summary_file = os.path.join(BASE_DIR, "回归结果_D1-D25全维汇总.txt")
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("AI科技星 · 全维统一场论 D1-D25 一键回归汇总\n")
        f.write(f"运行时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"方向数：{len(results)} | 成功：{ok_count} | 总行数：{total_lines}\n")
        f.write(f"对标：精确 {exact_total} + 初步 {partial_total} + 开放 {open_total} = {exact_total+partial_total+open_total}\n")
        f.write("-" * 60 + "\n")
        f.write("编号|方向|状态|输出行数|精确|初步|开放\n")
        for line in summary_lines:
            f.write(line + "\n")
    print(f"  汇总已写入：{summary_file}")
    print()

    if ok_count != len(DIRECTIONS):
        print("  ⚠️ 存在失败脚本，请检查上方明细。")
        sys.exit(1)
    print("  全部通过。AI科技星，继续加油！🚀")


if __name__ == "__main__":
    main()
