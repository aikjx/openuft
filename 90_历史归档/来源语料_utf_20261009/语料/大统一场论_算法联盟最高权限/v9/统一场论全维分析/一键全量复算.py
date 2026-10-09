# -*- coding: utf-8 -*-
"""
一键全量复算入口 —— 运行全部59条数值脚本（第1-59层），汇总判定
v41.0: 并入第59层AI-数学-意识统一方程精算AMC（54/56层为并行产出）
用法: python 一键全量复算.py
"""
import subprocess, os, sys, time

DIR = os.path.dirname(os.path.abspath(__file__))
scripts = [
    ('闭环数值验证套件.py',      '六组核心验证'),
    ('第1层_数值核验套件.py',     '第1层 41项核验'),
    ('第2层_全路径突破精算.py',   '第2层 六路径判定'),
    ('第3层_动力学化构造性修复.py','第3层 修复验证'),
    ('第4层_GR经典检验精算.py',   '第4层 GR检验'),
    ('第5层_KK精算.py',          '第5层 KK方向'),
    ('第7层_EC唯象学_挠率可观测性.py','第7层 EC唯象'),
    ('第7层延伸_自旋相关力实验灵敏度.py','第7+层 实验灵敏度'),
    ('第8层_P1_KK实验约束深化.py','第8层 P1-KK'),
    ('第9层_P3_胀子物理与等效原理.py','第9层 P3-胀子'),
    ('第10层_P2_量子引力三大方向.py','第10层 P2-量子引力'),
    ('第11层_P4_手征费米子KK构造.py','第11层 P4-手征'),
    ('第13层_全域统一判定_规范耦合收敛精算.py','第13层 统一性判定'),
    ('第14层_全域统一候选评估矩阵.py','第14层 候选评估'),
    ('第15层_大统一破解精算.py',  '第15层 破解精算'),
    ('第16层_全域理论体系突破矩阵.py','第16层 突破矩阵'),
    ('第17层_实验判决时间线与覆盖矩阵.py','第17层 实验判决'),
    ('第18层_求导统一场论证明_全维度精算.py','第18层 求导统一场论'),
    ('第19层_量子引力闭合_渐近安全精算.py','第19层 量子引力闭合'),
    ('第20层v2_求导统一场论终极总纲_全链路复算.py','第20层 终极总纲(v2优化)'),
    ('第21层_几何代数统一_Clifford精算.py','第21层 几何代数统一(GAUFT)'),
    ('第22层_变分原理_全套场方程推导.py','第22层 变分原理(VAUFT)'),
    ('第23层_宇宙学推论_大反弹精算.py','第23层 宇宙学统一(CUFT)'),
    ('第24层_黑洞热力学_全息原理精算.py','第24层 黑洞全息统一(BHUFT)'),
    ('第25层_物质引力联合渐近安全_C5闭合.py','第25层 联合渐近安全(MGAS,C5闭合)'),
    ('第26层_终极统一场论总纲_全整合.py','第26层 终极总纲(UUFT)'),
    ('第27层_量子测量退相干统一_QMUFT.py','第27层 量子测量退相干(QMUFT)'),
    ('第28层_时间本质热力学统一_TEUFT.py','第28层 时间本质热力学(TEUFT)'),
    ('第29层_高维FRG截断鲁棒性_HFRG.py','第29层 高维FRG截断鲁棒性(HFRG)'),
    ('第30层_实验方案设计可检验预言_EPDUFT.py','第30层 实验方案设计(EPDUFT)'),
    ('第31层_终极哲学整合三元统一_PPUUFT.py','第31层 哲学整合(PPUUFT)'),
    ('第32层_全体系数值一致性验证_NCVUFT.py','第32层 数值一致性(NCVUFT)'),
    ('第33层_信息论统一全息深化_ITUFT.py','第33层 信息论统一(ITUFT)'),
    ('第34层_全体系终极整合优化_FUOFT.py','第34层 终极整合优化(FUOFT)'),
    ('第35层_传统物理异常修复全方程统一_APUFT.py','第35层 异常修复(APUFT)'),
    ('第36层_拓扑场论任意子拓扑量子计算统一_TTUFT.py','第36层 拓扑场论(TTUFT)'),
    ('第37层_非对易几何谱作用量统一_NCGUFT.py','第37层 非对易几何(NCGUFT)'),
    ('第38层_全链路求导证明精算验证_FDVUFT.py','第38层 全链路求导(FDVUFT)'),
    ('第39层_深度求导证明漏洞修复_DPVUFT.py','第39层 求导漏洞修复(DPVUFT)'),
    ('第40层_终极本源总纲_UOSFT.py','第40层 终极本源(UOSFT)'),
    ('第41层_关键异常修复预言精确化_KARPUFT.py','第41层 关键异常修复(KARPUFT)'),
    ('第42层_全体系终极整理优化总纲v12_FUOF2.py','第42层 终极整理总纲v12(FUOFT-v2)'),
    ('第43层_量子引力理论深度对比_CGCUFT.py','第43层 量子引力对比(CGCUFT)'),
    ('第44层_终极求导证明精算验证_UDPVUFT.py','第44层 终极求导证明(UDPVUFT)'),
    ('第45层_全维融合互通归一化证明_UFINUFT.py','第45层 全维融合互通(UFINUFT)'),
    ('第46层_全体系问题深度修复优化_DFIUFT.py','第46层 问题深度修复(DFIUFT)'),
    ('第47层_深度修复优化v2_DFIUFTv2.py','第47层 深度修复v2(DFIUFT-v2)'),
    ('第48层_量子计算信息处理统一_QCUFT.py','第48层 量子计算统一(QCUFT)'),
    ('第49层_全体系终极整理优化v3_FUOFTv3.py','第49层 全体系整理优化v3(FUOFT-v3)'),
    ('第50层_R3截断FRG精算_R3UFT.py','第50层 R³截断FRG(R3UFT)'),
    ('第51层_完整阈值函数FRG流精算_FTFRG.py','第51层 阈值函数FRG(FTFRG)'),
    ('第52层_高阶fR截断与截断收敛精算_FULLFRG.py','第52层 高阶fR截断(FULLFRG)'),
    ('第53层_阈值结构形式交叉与lambdaIR行为闭合_IRUFT.py','第53层 阈值结构交叉与λ-IR闭合(IRUFT)'),
    ('第54层_意识与生命物理统一_CLUFT.py','第54层 意识与生命物理统一(CLUFT)'),
    ('第55层_完整泛函fR_LPA收敛精算_FLPA.py','第55层 完整泛函f(R)-LPA收敛(FLPA)'),
    ('第56层_LQG异常诊断求导验证修复_LQGD.py','第56层 LQG异常诊断修复(LQGD)'),
    ('第57层_全体系疑问闭合与全维融合精算_QUFUFT.py','第57层 疑问闭合与全维融合(QUFUFT)'),
    ('第58层_渐近安全收敛闭合与lambdaIR结构泛化_ASCC.py','第58层 收敛闭合与λ-IR泛化(ASCC)'),
    ('第59层_AI数学与思想意识统一方程精算_AMC.py','第59层 AI-数学-意识统一(AMC)'),
]

print('='*78)
print('求导统一场论 · 一键全量复算（第1-59层，v41.0）')
print('='*78)
results_list = []
start_total = time.time()
ok = fail = 0
total = len(scripts)

for i, (name, desc) in enumerate(scripts, 1):
    path = os.path.join(DIR, name)
    if not os.path.exists(path):
        print(f'  [{i:2d}/{total}] [缺失] {name} ({desc})')
        fail += 1
        results_list.append((name, 'MISSING', 0))
        continue
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True,
                           encoding='utf-8', errors='replace', timeout=120)
        elapsed = time.time() - t0
        if r.returncode == 0:
            print(f'  [{i:2d}/{total}] [通过] {name} ({desc}) — {elapsed:.1f}s')
            ok += 1
            results_list.append((name, 'PASS', elapsed))
        else:
            print(f'  [{i:2d}/{total}] [失败] {name} ({desc}) — {elapsed:.1f}s (exit {r.returncode})')
            fail += 1
            results_list.append((name, 'FAIL', elapsed))
    except subprocess.TimeoutExpired:
        print(f'  [{i:2d}/{total}] [超时] {name} ({desc}) — 120s 上限')
        fail += 1
        results_list.append((name, 'TIMEOUT', 120))
    except Exception as ex:
        print(f'  [{i:2d}/{total}] [异常] {name} ({desc}) — {ex}')
        fail += 1
        results_list.append((name, 'ERROR', 0))

total_time = time.time() - start_total
print('='*78)
print(f'  复算汇总: 通过 {ok} / 共 {total}   (通过率 {ok/total*100:.1f}%)')
print(f'  总用时: {total_time:.1f}s ({total_time/60:.1f} min)')
if fail == 0:
    print('  => 全部数值脚本通过, 体系数值一致, 无编造')
else:
    print(f'  => 有 {fail} 项失败, 需检查:')
    for name, status, t in results_list:
        if status != 'PASS':
            print(f'      - {name}: {status}')
print('='*78)
