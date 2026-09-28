# -*- coding: utf-8 -*-
import io
p='TUFT_归一化主册_v1.0.md'
s=io.open(p,encoding='utf-8-sig').read()
anchor='> **★★ MainAgent 证据审计注记（2026-09-24，append-only，不改组织者文本）**'
add='\n> **★★ MainAgent v48 独立复跑（2026-09-24，append-only）**：`_audit_v48_rotating_qnm.py`/`_out.txt` **真实落盘且自包含**（numpy/scipy only、无 qnm import、无 prior-project import），MainAgent 在 .venv 原样复跑 exit0，**全部数字逐位复现**：GR 门 A PASS（|err|=2.470e-13，n0 12 位）；GR 门 B **FAIL**（Rayleigh split/a=0.0962 vs 权威 0.25153；continuation max|Im drift|=1.54e-2 >5e-3）；TUFT 静态锚 0.434445174−0.056449760i 复现（|d|=4.503e-9）；TUFT 旋转极点 **UNTRUSTED**（GR 门 B 未过，铁律禁读物理），raw split/a@0.10=0.1045/@0.20=−0.3431 非验证预言；条件数墙 DETECTED（sigma_min=7.72e-12）。**v48 是首个有真实落盘证据的旋转攻坚，且为诚实 FAIL——直接反驳 v44 无证声称（门 A/B PASS 12.6/7.2 位、TUFT 频裂 0.09832）**。TUFT 旋转 m 频裂保持 **OPEN**。T01 正确路径确认＝完整 deturbed Teukolsky→Jansen 嵌入（O(a) 算符：K=(r²+a²)ω−am、(2rω−m) 导数耦合、Cook–Zhang ₛA_lm O(a) 对角 −2Smaω、入射视界 Ω_H）；零自由常数、禁 import qnm、禁硬编码 0.0628831/0.2515323，GR/入射视界极限先复现 n0≥11.6 位且 0.2515323≥4 位才许换 TUFT 反射壁报频裂。台账见 main_agent_v58_v48_rerun。\n'
assert anchor in s
s=s.replace(anchor, add+anchor, 1)
io.open(p,'w',encoding='utf-8').write(s)
print('master v48 note inserted, size', len(s))
