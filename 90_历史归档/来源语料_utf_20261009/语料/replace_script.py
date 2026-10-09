#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""精准文本替换脚本 - 保持UTF-8编码，局部精准替换"""

import os
import re

BASE_DIR = r"d:\a10\aikjx\code\my_lib\utf"

def read_file(filepath):
    """读取UTF-8文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """写入UTF-8文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def count_lines(content):
    return content.count('\n') + 1

def replace_text(content, old, new, is_regex=False, flags=0):
    """执行替换并返回 (new_content, count)"""
    if is_regex:
        matches = list(re.finditer(old, content, flags=flags))
        count = len(matches)
        if count > 0:
            new_content = re.sub(old, new, content, flags=flags)
            return new_content, count
        return content, 0
    else:
        count = content.count(old)
        if count > 0:
            return content.replace(old, new), count
        return content, 0

def process_file(rel_path, task_list):
    """
    处理单个文件
    task_list: list of dict with keys: old, new, is_regex, flags(optional), desc
    """
    full_path = os.path.join(BASE_DIR, rel_path)
    if not os.path.exists(full_path):
        print(f"\n[跳过] 文件不存在: {rel_path}")
        return None

    content = read_file(full_path)
    orig_content = content
    orig_lines = count_lines(content)
    results = []
    total_count = 0

    for idx, task in enumerate(task_list):
        old = task['old']
        new = task['new']
        is_regex = task.get('is_regex', False)
        flags = task.get('flags', 0)
        desc = task.get('desc', f'替换{idx+1}')

        content, count = replace_text(content, old, new, is_regex, flags)
        total_count += count
        if count > 0:
            results.append(f"  ✓ 替换{idx+1} [{desc}]: {count}处")
        else:
            results.append(f"  ✗ 替换{idx+1} [{desc}]: 未找到匹配")

    new_lines = count_lines(content)
    line_diff = new_lines - orig_lines

    if content != orig_content:
        write_file(full_path, content)
        print(f"\n[修改成功] {rel_path}")
        print(f"  行数变化: {line_diff:+d}行 (原{orig_lines} → 新{new_lines})")
        print(f"  总替换数: {total_count}处")
    else:
        print(f"\n[未修改] {rel_path} (无匹配)")
    
    for r in results:
        print(r)
    
    return {
        'path': rel_path,
        'modified': content != orig_content,
        'line_diff': line_diff,
        'total_replacements': total_count,
        'results': results,
    }

def main():
    print("=" * 70)
    print("精准文本替换脚本开始执行")
    print(f"基础目录: {BASE_DIR}")
    print("=" * 70)

    summary = []

    # ============================================================
    # 目标1：角速度论文1（3处替换）
    # ============================================================
    f1 = r"01-核心论文\角速度\v1\验证\算法联盟视角下：抛弃β因子，以光速螺旋为宇宙统一本源——角速度普适公式全维度求导、严格证明与跨尺度验证.md"
    t1 = [
        {
            # 替换1: 兼容中英文引号（""、''、""、''）
            'old': r'理论与宇宙演化的绝对起点，是["\u201c\u201d\u300c\u300d\u300e\u300f\'\u2018\u2019]物体["\u201c\u201d\u300c\u300d\u300e\u300f\'\u2018\u2019]的几何本质',
            'new': '每个物理对象（"物体"）的几何本质',
            'is_regex': True,
            'flags': 0,
            'desc': '理论绝对起点→物理对象几何本质（多引号兼容）',
        },
        {
            # 替换2: 精确文本
            'old': '仅为几何意义上的奇点（坐标原点），是光速螺旋运动的汇聚中心与载体',
            'new': '仅为几何意义上的坐标原点，是该对象周围光速螺旋运动的局部汇聚中心与载体',
            'is_regex': False,
            'desc': '奇点坐标原点→局部汇聚中心',
        },
        {
            # 替换3: 从"。零维奇点的几何属性"到行末（MULTILINE模式）
            'old': r'。零维奇点的几何属性.*$',
            'new': '。零维几何点的属性（无尺度、无方向，仅为汇聚点），决定了光速螺旋运动的汇聚方向，是引力场几何化、质量几何化的核心基础，其本身无任何冗余参数，完全契合算法联盟"去冗余"的诉求。**澄清**：此处 r=0 为质量定义的局部几何中心，非时空创生意义上的宇宙学奇点；GAQ-UFT 公理 II 声明螺旋运动永恒存在，宇宙作为整体无"演化绝对起点"。',
            'is_regex': True,
            'flags': re.MULTILINE,
            'desc': '零维奇点属性→零维几何点+澄清说明（行末替换）',
        },
    ]
    summary.append(process_file(f1, t1))

    # ============================================================
    # 目标2：角速度论文3（1处替换）
    # ============================================================
    f2 = r"01-核心论文\角速度\v1\验证\时空几何的本征规律：基于光速螺旋运动第一性原理的角速度普适公式全维度求导、严格证明与跨尺度验证.md"
    t2 = [
        {
            # 整行替换（MULTILINE模式）
            'old': r'^（1）零维几何奇点：理论的绝对起点.*$',
            'new': '（1）零维几何点：即每个"物体"的局部几何本质——不具备体积、质量等物理属性，仅为几何意义上的坐标原点，是该物体周围时空运动的载体。**澄清**：此处为物体的质量定义中心（r=0），非整个宇宙时空创生的"理论绝对起点"；GAQ-UFT 公理 II：空间螺旋运动永恒存在，宇宙作为 κ-τ 几何场无绝对创生时刻。',
            'is_regex': True,
            'flags': re.MULTILINE,
            'desc': '零维几何奇点整行→零维几何点+澄清',
        },
    ]
    summary.append(process_file(f2, t2))

    # ============================================================
    # 目标3：附录.md（2处词条替换）
    # ============================================================
    f3 = r"12-书籍\人人都能理解统一场论demo\附录.md"
    t3 = [
        {
            'old': r'^.*\*\*奇点\*\*：宇宙大爆炸的起点.*$',
            'new': '**奇点**：物体质量几何化定义中的局部坐标原点（r=0），是该物体周围空间光速螺旋运动的汇聚中心。在 GAQ-UFT 框架中不存在"宇宙大爆炸起点"意义上的宇宙学奇点——空间螺旋运动永恒存在（公理 II），Ω_k=0 对应平坦无限大的 R³ 空间。',
            'is_regex': True,
            'flags': re.MULTILINE,
            'desc': '奇点词条重写',
        },
        {
            'old': r'^.*\*\*微波背景辐射\*\*：宇宙大爆炸遗留下来的辐射.*$',
            'new': '**微波背景辐射**：可观测视界（R_Λ=c/H₀）内热平衡态光子的红移残留，温度约 2.7K。在 GAQ-UFT 框架中，它是 κ-τ 场物质-辐射相等时期（z_eq≈5766）的视界内光子演化结果，并非"宇宙大爆炸"的创生残留——宇宙无创生起点。',
            'is_regex': True,
            'flags': re.MULTILINE,
            'desc': '微波背景辐射词条重写',
        },
    ]
    summary.append(process_file(f3, t3))

    # ============================================================
    # 目标4：第五部分.md - 重写18.1节（整节替换）
    # ============================================================
    f4 = r"12-书籍\人人都能理解统一场论\最终版\第五部分.md"

    new_section_18_1 = '''### 18.1 宇宙的永恒螺旋：从"大爆炸"叙事到 κ-τ 几何化的范式转变

宇宙的起源是人类最感兴趣的问题之一。ΛCDM 标准宇宙学给出了"大爆炸"叙事——宇宙起源于约 138 亿年前的一次爆炸，从一个奇点膨胀至今。但 GAQ-UFT 框架（基于空间以光速 c 永恒螺旋运动的公理 II）给出了完全不同的几何化图景，彻底改写了"起源"的含义。

#### 标准 ΛCDM 叙事：一种有效的视界内近似

ΛCDM 的"大爆炸"模型在描述可观测视界（R_Λ=c/H₀≈13.8 Gly）内的结构演化、元素核合成、CMB 各向异性等方面取得了巨大成功。但必须明确：
- H₀⁻¹≈13.96 Gyr 是 Hubble **特征时标**（R_Λ 对应的光行尺度），不是"宇宙的年龄"；
- CMB 红移 z≈1089 对应物质-辐射脱耦时期的观测**视界内**光子，不是"创生火球"的直接残留；
- 奇点定理在 GAQ-UFT 中被消除：质量的"奇点"只是每个物体的局部几何汇聚中心（r=0），并非全宇宙的时空创生起点。

#### GAQ-UFT 的几何化宇宙观（Ω_k=0 → 平坦无限大）

GAQ-UFT 以第一性原理重新诠释宇宙学，消除了"创生"这一外部叙事：
1. **永恒螺旋**（公理 II）：空间本体以光速 c 做永恒的圆柱状螺旋运动——无起点，无终点，不存在"诞生"时刻；
2. **平坦无限大空间**（Ω_k=0，Planck 2018 验证 |Ω_k|<0.01）：空间整体几何为欧氏 R³ 流形，测地完备且非紧，意味着体积向任意方向无限延伸，不存在边界；
3. **R_Λ=c/H₀ 为因果视界**：可观测宇宙只是无限大空间中的一个局部因果球（半径由 Hubble 特征曲率 κ_Λ=√Λ 决定），球外依然是同样的永恒螺旋空间；
4. **Λ 的几何化**：Λ=3Ω_Λ/R_Λ² 是宇宙尺度的曲率特征量，暗能量本质即 κ_Λ=√Λ 的曲率张力（w=-1，Friedmann 方程严格证明），无需"真空零点能"或自由参数。

#### 统一场论的关键洞察：宇宙不需要"诞生"，只需要"被理解"

当宇宙作为 κ-τ 永恒螺旋几何场被理解时，"它从哪里来"的伪问题自然消解——几何本体是自存的、永恒的。而真正有物理意义的问题是：
- 局部质量结构如何从 κ-τ 场的曲率平方分解（Σκ_i²=Λ）中涌现？→ 暗物质即残余曲率模式；
- 三代费米子质量比如何通过 SO(3) 投影与 π₃(SU(3)) 拓扑导出？→ v7 质量谱几何化；
- 为什么可观测视界 R_Λ 恰好是今天这个尺度？→ 与 C_Λ=3Ω_Λ≈2.0658 这一几何不变量相关。

因此，GAQ-UFT 的宇宙观将"大爆炸创生"替换为"永恒螺旋的视界内演化"，宇宙不需要第一推动，它就是螺旋本身。'''

    # 手工处理目标4
    full_path4 = os.path.join(BASE_DIR, f4)
    content4 = read_file(full_path4)
    orig_content4 = content4
    orig_lines4 = count_lines(content4)
    start_title = "### 18.1 宇宙大爆炸：它真的发生过吗？：宇宙的诞生之谜"
    start_idx = content4.find(start_title)

    if start_idx >= 0:
        # 找下一个同级标题
        rest = content4[start_idx + len(start_title):]
        next_match = re.search(r'\n### \d', rest)
        if next_match:
            end_idx = start_idx + len(start_title) + next_match.start()
            old_section = content4[start_idx:end_idx]
            trailing = '\n\n' if old_section.endswith('\n\n') else ('\n' if old_section.endswith('\n') else '')
            content4 = content4[:start_idx] + new_section_18_1 + trailing + content4[end_idx:]
            new_lines4 = count_lines(content4)
            line_diff4 = new_lines4 - orig_lines4
            write_file(full_path4, content4)
            print(f"\n[修改成功] {f4}")
            print(f"  行数变化: {line_diff4:+d}行 (原{orig_lines4} → 新{new_lines4})")
            print(f"  总替换数: 1处")
            print(f"  ✓ 替换1 [重写18.1整节]: 1处 (范围: '{start_title[:30]}...' → 下一个###之前)")
            summary.append({
                'path': f4, 'modified': True, 'line_diff': line_diff4,
                'total_replacements': 1, 'results': ['整节替换1处']
            })
        else:
            print(f"\n[部分失败] {f4}: 找到18.1标题但未找到下一个###标记")
            summary.append({'path': f4, 'modified': False, 'total_replacements': 0})
    else:
        # 尝试模糊匹配
        fuzzy = re.search(r'### 18\.1.*宇宙大爆炸', content4)
        if fuzzy:
            print(f"[调试] 找到模糊匹配: {fuzzy.group()[:50]}")
        print(f"\n[未修改] {f4}: 未找到18.1节标题")
        summary.append({'path': f4, 'modified': False, 'total_replacements': 0})

    # ============================================================
    # 目标5：V4第14章（2处）
    # ============================================================
    f5 = r"12-书籍\人人都能理解统一场论\V4\第14章 宇宙的起源与演化.md"
    t5 = [
        {
            'old': '1. **目前的估计**：根据宇宙膨胀的速率，宇宙的年龄约为138亿年。',
            'new': '1. **Hubble 特征时标**：R_Λ=c/H₀≈13.8 Gly，其对应的光行时标 t_H=1/H₀≈13.96 Gyr。GAQ-UFT 框架下这不是"宇宙年龄"（空间永恒螺旋无起点），而是可观测视界的几何尺度量。',
            'is_regex': False,
            'desc': '目前估计→Hubble特征时标',
        },
        {
            'old': '2. **年龄的意义**：宇宙的年龄告诉我们宇宙从开始到现在的时间跨度。',
            'new': '2. **t_H 的几何意义**：t_H 反映了暗能量特征曲率 κ_Λ=√Λ 对应的倒数尺度，是观测视界 R_Λ 的定量等价描述，不代表宇宙有"开始"。',
            'is_regex': False,
            'desc': '年龄意义→t_H几何意义',
        },
    ]
    summary.append(process_file(f5, t5))

    # ============================================================
    # 目标6：V4第3章时间之谜（1处整段替换）
    # ============================================================
    f6 = r"12-书籍\人人都能理解统一场论\V4\第3章 时间之谜.md"
    t6 = [
        {
            # 匹配包含目标子串的整行（MULTILINE）
            'old': r'^.*宇宙学时间箭头是由宇宙的膨胀决定的。根据宇宙大爆炸理论，宇宙从一个奇点开始，不断膨胀至今。.*$',
            'new': '宇宙学时间箭头由 κ-τ 场的局部熵增方向与视界尺度演化共同决定。GAQ-UFT 框架下没有"宇宙从奇点开始膨胀"的创生叙事——空间永恒螺旋（公理 II），Ω_k=0 对应平坦无限大空间，局部观测到的膨胀是视界内曲率模式的统计表现。',
            'is_regex': True,
            'flags': re.MULTILINE,
            'desc': '宇宙学时间箭头段落重写',
        },
    ]
    summary.append(process_file(f6, t6))

    # ============================================================
    # 目标7：知识图谱 T_obs 标注（2处）
    # ============================================================
    f7 = r"20-所有知识图谱关联关系整理\知识图谱完整整理.md"
    t7 = [
        {
            'old': 'T_obs（标准宇宙学时间≈138亿年）',
            'new': 'T_obs = 1/H₀（Hubble 特征时标≈13.96 Gyr，GAQ-UFT：非创生年龄，仅为可观测视界的几何尺度等效时标）',
            'is_regex': False,
            'desc': '第一处T_obs括号注释修正',
        },
        {
            'old': r'^\| 标准观测时间 \| T_obs \| ≈138亿年 \| ΛCDM宇宙学时间 \|.*$',
            'new': '| Hubble 特征时标 | T_obs = 1/H₀ | ≈13.96 Gyr | GAQ-UFT：观测视界 R_Λ 的等效时标，非宇宙创生年龄；Ω_k=0 下空间永恒且无限大 |',
            'is_regex': True,
            'flags': re.MULTILINE,
            'desc': '第二处T_obs表格行修正',
        },
    ]
    summary.append(process_file(f7, t7))

    # ============================================================
    # 最终汇总
    # ============================================================
    print("\n" + "=" * 70)
    print("执行汇总")
    print("=" * 70)
    for s in summary:
        if s is None:
            continue
        status = "✓已修改" if s.get('modified') else "-未修改"
        ld = s.get('line_diff', 0)
        tr = s.get('total_replacements', 0)
        print(f"  {status} | {s['path'][:60]:60s} | 行数{ld:+3d} | 替换{tr}处")

    total_modified = sum(1 for s in summary if s and s.get('modified'))
    total_replacements = sum(s.get('total_replacements', 0) for s in summary if s)
    print("\n" + "=" * 70)
    print(f"总计: 修改文件 {total_modified} 个 | 累计替换点 {total_replacements} 个")
    print("=" * 70)

if __name__ == "__main__":
    main()
