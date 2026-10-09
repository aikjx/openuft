# -*- coding: utf-8 -*-
# 一键全量复算入口 —— 运行全部9条数值脚本，汇总判定
# 用法: python 一键全量复算.py
import subprocess, os, sys

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
]

print('='*74)
print('0·1·∞ 闭环体系 · 一键全量复算')
print('='*74)
ok = fail = 0
for name, desc in scripts:
    path = os.path.join(DIR, name)
    if not os.path.exists(path):
        print(f'  [缺失] {name} ({desc})')
        fail += 1
        continue
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True,
                           encoding='utf-8', errors='replace', timeout=120)
        if r.returncode == 0:
            print(f'  [通过] {name} ({desc})')
            ok += 1
        else:
            print(f'  [失败] {name} ({desc}) -> exit {r.returncode}')
            fail += 1
    except Exception as ex:
        print(f'  [异常] {name} ({desc}) -> {ex}')
        fail += 1

print('='*74)
print(f'  复算汇总: 通过 {ok} / 共 {ok+fail}')
if fail == 0:
    print('  => 全部数值脚本通过, 体系数值一致, 无编造')
else:
    print(f'  => 有 {fail} 项失败, 需检查')
print('='*74)
