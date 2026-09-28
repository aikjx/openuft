# -*- coding: utf-8 -*-
"""v48 收口：主册升版 v5.7->v5.8。全部替换带计数断言，不匹配即报错。"""
p = r'D:\a10\aikjx\code\my_lib\openuft\01_独立体系\S16_TUFT归一化主册\13_论文与成果\主册\TUFT_归一化主册_v1.0.md'
top_p = r'D:\a10\aikjx\code\my_lib\_v48_topblock.txt'
chrono_p = r'D:\a10\aikjx\code\my_lib\_v48_chrono.txt'
s = open(p, encoding='utf-8').read()
topblock = open(top_p, encoding='utf-8').read().rstrip('\n')
chrono = open(chrono_p, encoding='utf-8').read().rstrip('\n')

def rep(old, new, cnt=1):
    global s
    c = s.count(old)
    assert c == cnt, 'anchor count=%d (want %d) for: %r' % (c, cnt, old[:60])
    s = s.replace(old, new)

# 1) 标题行（line 1）
old_title = '# TUFT 归一化主册 v5.7（v47 A4 SNR 精算轮：真实 PSD（O4=aLIGOZeroDetHighPower／Voyager=LIGO-T1800043 设计曲线）loudness 积分＋天线投影精算、GR 极限 PASS、绝对振幅 OPEN[E497]；E1–E497；当前勘误 #42【本轮无新勘误】；物理四态 35/61/18/27 冻结）'
new_title = '# TUFT 归一化主册 v5.8（v48 旋转 QNM Beyn 扩展轮：Beyn 围道向小旋转 a 推广、局域帧拖曳对角嵌入、GR 门 A PASS（n₀ ~12 位）/门 B FAIL（缺 Teukolsky O(a) 虚部交叉项）、a<0.10 条件墙上限[E498]；E1–E498；当前勘误 #42【本轮无新勘误】；物理四态 35/61/18/27 冻结）'
rep(old_title, new_title)

# 2) line 6 机器可读镜像版本
rep('机器可读镜像见《TUFT_归一化台账_v1.0.json》（内部 version=v5.7）。',
    '机器可读镜像见《TUFT_归一化台账_v1.0.json》（内部 version=v5.8）。')

# 3) 顶部块：v5.7 降版 + 插入 v5.8 新块（实际前缀为 空格+>+空格+**）
old_v57_head = ' > **★★★ 最新（v5.7，2026-09-24；v47 A4 SNR 精算轮收口'
new_v57_head = ' > **★★★（前版，已由 v5.8 接管；v5.7，2026-09-24；v47 A4 SNR 精算轮收口'
rep(old_v57_head, new_v57_head)
# 在降版后的 v5.7 块行之前插入新 v5.8 块
anchor = ' > **★★★（前版，已由 v5.8 接管；v5.7，2026-09-24；v47 A4 SNR 精算轮收口'
rep(anchor, topblock + '\n' + anchor)

# 4) line 26 权威口径行（用后续"（#41 为 v42 轮 held"锚定，与 line402 编年历史条目的 v5.7 戳区分）
rep('**version=v5.7 / latest_round=v5.7_v47_a4_snr_psd_actuarial / E1–E497 / 勘误 #42**（#41 为 v42 轮 held',
    '**version=v5.8 / latest_round=v5.8_v48_rotating_qnm_beyn / E1–E498 / 勘误 #42**（#41 为 v42 轮 held')
# 在 E497 登记句后追加 E498，并把"六者"改"七者"
old_e497 = 'E497＝v47 A4 SNR 精算（真实 PSD loudness 积分＋天线投影精算、GR 极限 PASS、绝对振幅 OPEN）登记；六者**不进物理四态**'
new_e497 = ('E497＝v47 A4 SNR 精算（真实 PSD loudness 积分＋天线投影精算、GR 极限 PASS、绝对振幅 OPEN）登记；'
            'E498＝v48 旋转 QNM Beyn 扩展（Beyn 围道向小旋转 a 推广、局域拖曳对角嵌入、GR 门 A PASS n₀~12 位／门 B FAIL 缺 Teukolsky O(a) 虚部交叉项、a<0.10 条件墙上限）登记；'
            '七者**不进物理四态**')
rep(old_e497, new_e497)

# 5) 编年列表：在 v5.7 条目（line 402）之前插入 v5.8 条目
old_chrono_anchor = '- **v5.7【v47 A4 SNR 精算轮收口，E497；'
rep(old_chrono_anchor, chrono + '\n' + old_chrono_anchor)

# 6) T01 告诫（line 797 区）追加 v5.8 更新块
old_tail = '本轮系对既有 E443/A9 墙的严格否定确认，不闭合新物理 E-number。）**'
new_tail = ('本轮系对既有 E443/A9 墙的严格否定确认，不闭合新物理 E-number。）**'
            '**（v5.8 E498 更新：v48 把 Beyn 围道机器向小旋转 a 推广——局域拖曳 Ω_F=2a/r³ 折成 O(aω) 局域对角势 −4amω/r³，GR Jansen 紧化 pencil Q1←Q1+diag(−4am/r³)；GR 门 A PASS（n₀@a=0 |err|=2.470e-13 ~12 位、N spread=3.45e-11），但 GR 门 B FAIL（Rayleigh split/a=0.0962 vs 靶 0.25153、延拓 max|Im drift|=1.54e-2>5e-3）：裸对角拖曳嵌入复现实部符号但缺 Teukolsky O(a) 虚部交叉项 4i(r−1)K/Δ，须经完整 Chandrasekhar 变换才能嵌进 Jansen 紧化 pencil，不硬凑 4 位。TUFT 侧门 B 未过不宣告物理读数（静态再锚 |d|=4.5e-9；旋转极原始 split/a@0.10=0.1045/@0.20=−0.343 符号翻转=非物理，与 v44 一阶 0.09832 的 a=0.10 吻合系不稳定算符下巧合）；条件墙 σ_min(L)=7.7e-12、可信 a<0.10；根因＝O(a) 算符未补全、非 Beyn 围道本身失败。完整旋转混合 BVP 求解器仍 OPEN——下一步＝补全 Teukolsky–Chandrasekhar O(a) 嵌入后重过门 B、再切 TUFT 反射壁报 m 频裂。）**')
rep(old_tail, new_tail)

open(p, 'w', encoding='utf-8', newline='').write(s)
print('OK main register updated; new len()=', len(s))
