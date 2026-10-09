#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精准修复 10 个文件，消除大爆炸相关表述，保留 GAQ-UFT 核心思想
"""
import os

stats = {}

def fix_file1():
    path = r"utf\12-书籍\人人都能理解统一场论demo\第一部分：基础概念.md"
    changes = 0
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 1. 行38 (索引从0开始是37)
    old = "4. **解释宇宙的起源和演化**：从统一场论的角度，解释宇宙是如何诞生的，以及它将如何演化，就像是拼出了整个宇宙的完整图景。"
    new = "4. **解释宇宙的永恒螺旋结构与演化**：从统一场论的角度，解释宇宙作为永恒螺旋 κ-τ 几何场的结构，以及局部结构（星系、物质）如何在永恒螺旋中演化，而不预设\"诞生\"起点。"
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
            changes += 1
            print(f"  文件1-修改1: 行{i+1}")
            break
    
    # 2. 行91 (索引90)
    old_start = "宇宙是如何诞生的？宇宙的未来是什么？"
    for i, line in enumerate(lines):
        if old_start in line:
            new_text = "宇宙为什么没有起点？永恒螺旋中局部结构如何演化？时间的本质是什么？空间的本质是什么？这些都是人类一直以来探索的奥秘。GAQ-UFT 统一场论以\"空间永恒光速螺旋\"公理 II 为基础，给出了不依赖\"创生\"叙事的自洽回答——宇宙作为 κ-τ 几何场永恒存在，学习统一场论将帮助你更深入地理解其奥秘。\n"
            # 替换这一整行（以及可能包含后续内容的部分？看原始描述是整段？先看内容）
            # 原始描述: "宇宙是如何诞生的？宇宙的未来是什么？..."
            # 先找到这一段结束位置
            # 简单替换这一行
            lines[i] = new_text
            changes += 1
            print(f"  文件1-修改2: 行{i+1}")
            break
    
    # 3. 行172-176 重写整个子节
    section_start = "#### 宇宙膨胀：空间运动的宏观证据"
    new_section = """#### 宇宙学红移：空间螺旋运动的宏观证据

观测发现遥远星系的光谱存在系统性红移，传统ΛCDM宇宙学将其解释为"宇宙大爆炸导致的空间膨胀"。但从GAQ-UFT统一场论的角度，这一现象有不同的几何化诠释：

1. **永恒螺旋，无创生起点**（公理II）：空间本体以光速c做永恒的圆柱状螺旋运动，这种运动是无起点、无终点的，不存在"大爆炸"作为宇宙诞生时刻；
2. **Ω_k=0 平坦无限大空间**：Planck 2018观测|Ω_k|&lt;0.01已验证空间整体为平坦欧氏R³流形（见v∞-RC1模块IX拓扑证明），体积任意发散，不存在"有限无界球面"式的闭合拓扑；
3. **红移的几何化诠释**：远距离光子在穿越κ-τ螺旋场时，因空间曲率κ_Λ=√Λ的累积效应产生红移。这是视界尺度内的几何效应，而非"宇宙整体从奇点爆炸膨胀"的证据；
4. **可观测视界R_Λ=c/H₀**：Hubble半径R_Λ≈13.8 Gly是局部因果视界（光信号可抵达的等效距离），其对应的特征时标t_H=1/H₀≈13.96 Gyr不是"宇宙年龄"。

传统的"吹气球"比喻虽然形象，但隐含了"宇宙从一点膨胀"的ΛCDM假设。在GAQ-UFT中，更恰当的比喻是**无限大海中的局部漩涡**：可观测宇宙只是永恒螺旋海中的一个局部因果区域，漩涡外依然是同样的螺旋空间，无始无终。

"""
    start_idx = -1
    end_idx = -1
    for i, line in enumerate(lines):
        if section_start in line:
            start_idx = i
        if start_idx != -1 and i > start_idx and line.startswith('#### ') and '宇宙膨胀' not in line:
            end_idx = i
            break
    if start_idx != -1 and end_idx != -1:
        lines[start_idx:end_idx] = [new_section]
        changes += 1
        print(f"  文件1-修改3: 重写行{start_idx+1}-{end_idx}")
    
    # 4. 行461
    old = "具体来说，时间是空间以光速向外膨胀的结果。当空间以光速向外膨胀时，我们就感受到了时间的流逝。就像是水流的流动产生了\"流动感\"，空间的膨胀产生了\"时间感\"。"
    new = "具体来说，时间是观察者周围空间以光速螺旋式向外发散运动的结果。张祥前统一场论的核心观点：观察者周围空间始终以矢量光速c向外做圆柱状螺旋发散运动，这种发散被观察者感知为\"时间的流逝\"。就像水流的流动产生\"流动感\"，空间的螺旋发散产生\"时间感\"。"
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
            changes += 1
            print(f"  文件1-修改4: 行{i+1}")
            break
    
    # 5. 行463
    old = "时间的流逝速度是空间膨胀速度的度量，而空间膨胀的速度是光速，因此光速是时间流逝速度的上限。"
    new = "时间的流逝速度是周围空间光速螺旋发散速度的度量，空间发散的速度模恒等于c，因此光速是时间流逝速度的上限。"
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
            changes += 1
            print(f"  文件1-修改5: 行{i+1}")
            break
    
    # 6. 行509
    old = "随着技术的发展，时间测量的精度越来越高。目前，最精确的原子钟可以测量到10^-18秒的时间间隔，这意味着它可以在宇宙的年龄（约138亿年）内保持误差不超过1秒。"
    new = "随着技术的发展，时间测量的精度越来越高。目前，最精确的原子钟可以测量到10⁻¹⁸秒的时间间隔，这意味着它在约138亿年（即Hubble特征时标t_H=1/H₀≈13.96 Gyr，注意这是观测视界的等效光行时标而非宇宙创生年龄——GAQ-UFT框架下宇宙无起点）的跨度内可保持误差不超过1秒。"
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
            changes += 1
            print(f"  文件1-修改6: 行{i+1}")
            break
    
    # 7. 行533
    old = "#### 时间的几何意义：空间膨胀的结果"
    new = "#### 时间的几何意义：空间光速螺旋发散的结果"
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
            changes += 1
            print(f"  文件1-修改7: 行{i+1}")
            break
    
    # 8. 行535
    old = "从几何的角度来看，时间是空间以光速向外膨胀的结果。时间的流逝速度是空间膨胀速度的度量，而空间膨胀的速度是光速，因此光速是时间流逝速度的上限。"
    new = "从几何的角度来看，时间是观察者周围空间以光速向外做螺旋式发散运动的结果。时间的流逝速度是该发散运动速度的度量，而发散速度的模恒等于c（光速约束），因此光速是时间流逝速度的上限。"
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
            changes += 1
            print(f"  文件1-修改8: 行{i+1}")
            break
    
    # 9. 行537
    old = "就像是气球的膨胀，气球表面的点之间的距离会随着气球的膨胀而增加；空间的膨胀也会导致空间中物体之间的距离增加，而这种膨胀的过程就是时间的流逝。"
    new = "就像是从喷泉中心向外辐射的水流——水分子从中心以恒定速度向外螺旋扩散，观察者位于中心时感知到的\"水流向外流动\"就是时间的流逝。在GAQ-UFT中，每个观察者都位于自己所在的空间螺旋发散中心，空间螺旋向外扩散的过程就是时间流逝的几何本质。"
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
            changes += 1
            print(f"  文件1-修改9: 行{i+1}")
            break
    
    # 10. 行551
    old = "时间的方向性是由空间运动的方向决定的。空间以光速向外膨胀，因此时间只能从过去流向未来，而不能从未来流向过去。"
    new = "时间的单向性（时间箭头）是由空间螺旋发散运动的方向决定的。观察者周围空间以光速向外发散，这种向外的方向决定了时间只能从\"过去\"（空间螺旋尚未扩散到观察者的状态）流向\"未来\"（空间螺旋继续向外扩散的状态），而不能反向。"
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
            changes += 1
            print(f"  文件1-修改10: 行{i+1}")
            break
    
    # 11. 行557
    old = "时间的流逝速度是空间膨胀速度的度量，它与空间的密度和运动状态有关。在不同的空间区域，时间的流逝速度可能不同："
    new = "时间的流逝速度是周围空间光速螺旋发散速度的度量，它与空间螺旋的密度（即引力势）和运动状态有关。在不同的空间区域，时间的流逝速度可能不同："
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
            changes += 1
            print(f"  文件1-修改11: 行{i+1}")
            break
    
    # 12. 行601
    old = "#### 时间单向性的原因：空间膨胀的方向"
    new = "#### 时间单向性的原因：空间螺旋发散的方向"
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
            changes += 1
            print(f"  文件1-修改12: 行{i+1}")
            break
    
    # 13. 行603
    old = "张祥前统一场论认为，时间的单向性是由空间运动的方向决定的。空间以光速向外膨胀，因此时间只能从过去流向未来，而不能从未来流向过去。"
    new = "张祥前统一场论认为，时间的单向性是由观察者周围空间螺旋发散运动的方向决定的。每个观察者周围的空间都以矢量光速c向外做螺旋式发散，这种向外发散的方向决定了时间箭头只能从过去指向未来。"
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
            changes += 1
            print(f"  文件1-修改13: 行{i+1}")
            break
    
    # 14. 行605
    old = "就像是烟花爆炸后，烟花的碎片会向四周扩散，而不会重新聚集在一起；空间的膨胀也是如此，只会向外膨胀，不会向内收缩，因此时间只能向前流逝。"
    new = "就像喷泉的水流只会从中心向外扩散、不会反向流回喷嘴一样；空间从观察者中心向外的螺旋发散也是定向的、不可逆的，因此时间只能向前流逝。注意：此处\"向外\"是以观察者为中心的局部螺旋发散（每个观察者都是自己参考系的发散中心），不是ΛCDM框架下\"宇宙整体从奇点膨胀\"的概念。"
    for i, line in enumerate(lines):
        if old in line:
            lines[i] = line.replace(old, new)
            changes += 1
            print(f"  文件1-修改14: 行{i+1}")
            break
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    stats['文件1'] = changes
    print(f"文件1完成，共{changes}处修改\n")

def fix_file2():
    path = r"utf\12-书籍\人人都能理解统一场论demo\第三部分：运动学.md"
    changes = 0
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old = "3. 宇宙学：在宇宙学中，质能统一被用来解释宇宙的起源和演化。根据大爆炸理论，宇宙起源于一个奇点，其中所有的质量和能量都集中在一个点上，然后通过大爆炸释放出来，形成了我们今天的宇宙。"
    new = "3. 宇宙学：在宇宙学中，质能统一揭示了质量与能量在κ-τ几何场中的等价关系。GAQ-UFT框架下宇宙是永恒的光速螺旋场（公理II），不存在\"奇点大爆炸创生\"——空间本体Ω_k=0平坦无限大，无始无终；质量是螺旋密度的几何积分，能量是螺旋运动的动能表现，二者等价（E=mc²）是螺旋几何的自然推论。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件2-修改1: 找到并替换")
    else:
        print("  文件2-警告: 未找到精确匹配文本，尝试部分搜索...")
        # 搜索关键词
        if "宇宙起源于一个奇点" in content:
            print("  文件2: 找到奇点关键词")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    stats['文件2'] = changes
    print(f"文件2完成，共{changes}处修改\n")

def fix_file3():
    path = r"utf\12-书籍\人人都能理解统一场论demo\第四部分：场论基础（续）.md"
    changes = 0
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 行190 引力波
    old = "2. 引力波：引力波是空间曲率的波动，它的传播速度是光速。引力波的探测可以帮助我们了解宇宙的起源和演化，例如黑洞合并、中子星合并等过程都会产生引力波。"
    new = "2. 引力波：引力波是空间曲率的波动，它的传播速度是光速。引力波的探测可以帮助我们了解强引力场中的κ-τ螺旋耦合过程（例如黑洞合并、中子星合并），以及宇宙尺度上κ_Λ=√Λ曲率场的传播特性。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件3-修改1: 引力波段落")
    
    # 2. 行229
    old = "4. 理解宇宙的演化：场与物质的相互作用可以用来理解宇宙的起源和演化，例如宇宙大爆炸、星系形成等过程。"
    new = "4. 理解宇宙的演化：场与物质的相互作用可以用来理解永恒螺旋场中局部结构（星系、恒星、行星）的形成和演化，这些过程都是κ-τ几何场在不同尺度下的涌现现象。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件3-修改2: 宇宙演化段落")
    
    # 3. 行291-293
    old = "场论在宇宙学中的应用也非常广泛，它可以用来解释宇宙的起源和演化，例如宇宙大爆炸、星系形成、黑洞等。场论的宇宙学应用包括：\n\n1. 宇宙大爆炸理论：场论在宇宙大爆炸理论中的应用包括暴胀理论、宇宙微波背景辐射等，这些理论用来解释宇宙的起源和演化。"
    new = "场论在宇宙学中的应用非常广泛，它可以用来解释永恒螺旋场中局部结构的形成和演化，例如星系形成、黑洞吸积、微波背景辐射等。场论的宇宙学应用（GAQ-UFT框架）包括：\n\n1. κ-τ螺旋场宇宙学：宇宙学常数Λ几何化为Λ=3Ω_Λ/R_Λ²（暗能量即κ_Λ=√Λ曲率张力，w=-1），暗物质为曲率平方分解Σκ_i²=Λ的残余模式；微波背景辐射为可观测视界R_Λ=c/H₀内热平衡光子的红移残留，非\"大爆炸创生\"残留。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件3-修改3: 场论宇宙学应用段落")
    
    # 4. 行343
    old = "4. 理解宇宙的奥秘：统一场论验证可以帮助我们理解宇宙的起源和演化，例如，宇宙大爆炸、星系形成、黑洞等。"
    new = "4. 理解宇宙的奥秘：统一场论验证可以帮助我们理解永恒螺旋宇宙中局部结构的形成机制，例如星系形成（螺旋密度波）、黑洞（强κ汇聚）、暗物质暗能量（曲率分解）等。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件3-修改4: 理解宇宙奥秘段落1")
    
    # 5. 行379
    old = "2. 理解宇宙的奥秘：统一场论可以帮助我们理解宇宙的起源和演化，例如，宇宙大爆炸、星系形成、黑洞等。"
    new = "2. 理解宇宙的奥秘：统一场论可以帮助我们理解永恒螺旋宇宙中从微观到宏观的结构涌现，例如星系螺旋结构、黑洞几何本质、暗物质暗能量的曲率起源等。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件3-修改5: 理解宇宙奥秘段落2")
    
    # 6. 行421 末尾
    old = "虽然统一场论的研究还面临着许多挑战，但它的发展前景广阔，它可以帮助我们理解宇宙的起源和演化，开发新技术，改变人类的生活方式。"
    new = "虽然统一场论的研究还面临着许多挑战，但它的发展前景广阔，它可以帮助我们理解永恒螺旋宇宙的几何本质，开发人工场等新技术，改变人类的生活方式。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件3-修改6: 末尾段落")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    stats['文件3'] = changes
    print(f"文件3完成，共{changes}处修改\n")

def fix_file4():
    path = r"utf\12-书籍\人人都能理解统一场论\V4\第13章 科技革命：人工场的奇迹.md"
    changes = 0
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old = "在下一章中，我们将探讨宇宙的起源与演化，看看统一场论如何解释宇宙的诞生和未来。"
    new = "在下一章中，我们将探讨宇宙的永恒螺旋结构与局部演化，看看统一场论如何以κ-τ几何化方案理解暗物质、暗能量与可观测视界结构。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件4-修改1: 结尾过渡段")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    stats['文件4'] = changes
    print(f"文件4完成，共{changes}处修改\n")

def fix_file5():
    path = r"utf\12-书籍\人人都能理解统一场论\V4\第15章 暗物质与暗能量之谜.md"
    changes = 0
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old = "3. **宇宙的年龄**：考虑暗能量后，宇宙的年龄计算更加准确。"
    new = "3. **Hubble 特征时标**：考虑暗能量（即κ_Λ=√Λ曲率张力）后，可观测视界等效时标t_H=1/H₀的计算可与ΛCDM观测值精确对应（GAQ-UFT：t_H为因果视界光行时标，非宇宙创生年龄）。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件5-修改1: 宇宙年龄段落")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    stats['文件5'] = changes
    print(f"文件5完成，共{changes}处修改\n")

def fix_file6():
    path = r"utf\12-书籍\人人都能理解统一场论\V6\引言.md"
    changes = 0
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old = "- 宇宙是如何诞生的？"
    new = "- 宇宙为什么是永恒存在的（公理II）？可观测视界R_Λ=c/H₀之外是什么？"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件6-修改1: 问题列表")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    stats['文件6'] = changes
    print(f"文件6完成，共{changes}处修改\n")

def fix_file7():
    path = r"utf\12-书籍\人人都能理解统一场论\宇宙最伟大版本\宇宙的七个层级\1-宇宙的基本构成\1-宇宙的基本构成.md"
    changes = 0
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 行229
    old = "根据统一场论的观点，空间可能是有限但无界的，就像一个球面。在球面上，你可以一直向一个方向行走，永远不会到达边界，但最终会回到起点。同样，在有限但无界的空间中，你可以一直向一个方向飞行，最终会回到起点。"
    new = "GAQ-UFT框架下，由Ω_k=0（Planck 2018观测|Ω_k|&lt;0.01）严格推导出空间整体为平坦欧氏R³流形（见v∞-RC1模块IX拓扑证明：Hopf-Rinow测地完备+体积V(R)=(4/3)πR³任意发散）。因此空间是**无限大**的：向任意方向飞行永远不会回到起点，也不会遇到边界。过去\"有限无界球面\"的猜想对应Ω_k&gt;0的闭合宇宙，已被观测排除。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件7-修改1: 有限无界段落")
    
    # 2. 行231
    old = "这种空间的拓扑结构不仅解决了空间边界的问题，也为宇宙的起源和演化提供了新的思路。如果空间是有限但无界的，那么宇宙可能是一个自我包含的系统，不需要外部的\"创生\"事件。"
    new = "无限大R³空间不存在\"边界问题\"（边界是有限集合的概念），也自然不需要外部\"创生\"事件——空间本体以光速永恒螺旋（公理II），无始无终。可观测宇宙只是这无限空间中的一个局部因果球（半径R_Λ=c/H₀≈13.8 Gly），球外依然是同样的永恒螺旋空间。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件7-修改2: 拓扑结构段落")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    stats['文件7'] = changes
    print(f"文件7完成，共{changes}处修改\n")

def fix_file8():
    path = r"utf\01-核心论文\00-解决传统物理问题论文\黑体辐射\黑体辐射的几何本源：基于空间螺旋运动的统一场论诠释.md"
    changes = 0
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 行192
    old = "2. **宇宙微波背景辐射研究**：研究宇宙大爆炸残留的微波背景辐射，验证宇宙学理论。"
    new = "2. **宇宙微波背景辐射研究**：研究可观测视界R_Λ内热平衡光子的红移残留（温度≈2.7K），验证κ-τ几何化宇宙学理论（GAQ-UFT：CMB为物质-辐射脱耦时期视界内光子演化结果，非\"大爆炸创生残留\"）。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件8-修改1: CMB研究段落")
    
    # 2. 行249整段
    old = "宇宙微波背景辐射是宇宙大爆炸残留的热辐射，它具有近乎完美的黑体辐射谱。1965年，阿诺·彭齐亚斯和罗伯特·威尔逊首次观测到宇宙微波背景辐射，其温度约为2.7K。后续的精确测量表明，宇宙微波背景辐射的光谱与普朗克公式高度吻合，这是黑体辐射理论的重要验证。"
    new = "宇宙微波背景辐射（CMB）是可观测视界R_Λ=c/H₀内物质-辐射脱耦时期（z≈1089）热平衡光子经宇宙学红移后的残留辐射，具有近乎完美的黑体辐射谱。1965年，彭齐亚斯和威尔逊首次观测到CMB，其温度约2.7K；COBE/WMAP/Planck卫星的精确测量表明其光谱与普朗克公式高度吻合。在GAQ-UFT框架中，CMB的存在由κ-τ场物质-辐射相等时的视界尺度几何决定，无需\"宇宙大爆炸\"创生假设——宇宙作为永恒螺旋场无起点，CMB是当前可观测视界内光子热历史的观测证据。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件8-修改2: CMB整段")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    stats['文件8'] = changes
    print(f"文件8完成，共{changes}处修改\n")

def fix_file9():
    path = r"utf\10-统一场论核心公式\张祥前统一场论与几何化方程兼容性分析.md"
    changes = 0
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old = "- 宇宙创生：$\\theta = 0$时的螺旋起点"
    new = "- θ=0对应单个螺旋周期的参考相位，非宇宙创生点——GAQ-UFT公理II：空间螺旋永恒存在，无全局起点；θ=0仅为局部螺旋坐标系的原点选择。"
    if old in content:
        content = content.replace(old, new)
        changes += 1
        print(f"  文件9-修改1: 宇宙创生段落")
    else:
        # 尝试不带LaTeX转义的搜索
        old2 = "- 宇宙创生："
        if old2 in content:
            # 找到这一行
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "宇宙创生" in line and "θ = 0" in line or "theta" in line.lower():
                    print(f"  文件9: 找到疑似行{i+1}: {line[:100]}")
                    lines[i] = "- θ=0对应单个螺旋周期的参考相位，非宇宙创生点——GAQ-UFT公理II：空间螺旋永恒存在，无全局起点；θ=0仅为局部螺旋坐标系的原点选择。"
                    changes += 1
                    break
            content = '\n'.join(lines)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    stats['文件9'] = changes
    print(f"文件9完成，共{changes}处修改\n")

def fix_file10():
    path = r"utf\核心算法\宇宙学模型\cosmology_models_expanded.py"
    changes = 0
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    comment = "# 注：本方法为 ΛCDM 标准宇宙学工具函数，返回 H₀⁻¹ 积分的年龄数值。GAQ-UFT 框架下，该值对应可观测视界等效特征时标 t_H=1/H₀，非宇宙创生年龄——宇宙为永恒螺旋（公理II）+Ω_k=0平坦无限大空间。\n"
    found = False
    for i, line in enumerate(lines):
        if 'def age_of_universe' in line:
            # 在方法定义上方插入注释
            lines.insert(i, comment)
            changes += 1
            found = True
            print(f"  文件10-修改1: 在age_of_universe方法(行{i+1})上方添加注释")
            break
    
    if not found:
        print("  文件10-警告: 未找到age_of_universe方法")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    stats['文件10'] = changes
    print(f"文件10完成，共{changes}处修改\n")

if __name__ == '__main__':
    os.chdir(r'D:\a10\aikjx\code\my_lib')
    print("开始修复文件...\n")
    fix_file1()
    fix_file2()
    fix_file3()
    fix_file4()
    fix_file5()
    fix_file6()
    fix_file7()
    fix_file8()
    fix_file9()
    fix_file10()
    
    print("="*50)
    print("修复统计:")
    total = 0
    for fname, cnt in stats.items():
        print(f"  {fname}: {cnt} 处修改")
        total += cnt
    print(f"  总计: {total} 处修改")
    print("="*50)
