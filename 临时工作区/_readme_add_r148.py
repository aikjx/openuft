# -*- coding: utf-8 -*-
"""README 四处登记 r148（外科式插入，按锚点定位，不整体重写）。"""
import os
import io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "README.md")

with io.open(README, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

SRC_ANCHOR = "\u2502   \u2514\u2500\u2500 TUFT-r147_\u4fee\u590d\u7a7a\u95f4\u7684\u673a\u5668\u751f\u6210\u4e0e\u95ed\u5305\u5b9a\u4ef7_2026-10-22.py"
JUDGE_ANCHOR = "\u251c\u2500\u2500 \u5224\u5b9a_TUFT-r147_\u4fee\u590d\u7a7a\u95f4\u7684\u673a\u5668\u751f\u6210\u4e0e\u95ed\u5305\u5b9a\u4ef7_2026-10-22.md"
DATA_ANCHOR = "    \u251c\u2500\u2500 TUFT-r147_\u4fee\u590d\u7a7a\u95f4\u7684\u673a\u5668\u751f\u6210\u4e0e\u95ed\u5305\u5b9a\u4ef7_2026-10-22.json"

SRC_LINE = (
    "\u2502   \u2514\u2500\u2500 TUFT-r148_D5\u5927\u7edf\u4e00\u529b\u65b9\u7a0b\u9996\u653b\u4e0e\u4fee\u590d\u5b9a\u4ef7_2026-10-22.py  # \u65b0\u589e\uff08**r148 \u00b7 2026-10-22**\uff1a"
    "**D5\u300a\u5927\u7edf\u4e00\u529b\u65b9\u7a0b\u300b\u9996\u653b** \u2014\u2014 \u9776\u4e3a"
    "`01_\u72ec\u7acb\u4f53\u7cfb/S02_\u7a7a\u95f4\u5149\u901f\u87ba\u65cb\u7edf\u4e00\u529b/04_\u7406\u8bba\u63a8\u5bfc/D5_\u5927\u7edf\u4e00\u529b\u65b9\u7a0b/`\uff08\u5f20\u7965\u524d\u4f53\u7cfb"
    "**\u539f\u59cb\u516c\u8bbe\u5c42**\uff1a\u7edf\u4e00\u52a8\u91cf `P=m(c-v)` / \u7edf\u4e00\u529b `F=dP/dt` / "
    "\u7535\u78c1\u529b\u6bd4 `F_e/F_m=c/v` / \u7535\u78c1\u6ce2 `E=cB` / \u57fa\u77f3 `\u03ba\u00b2+\u03c4\u00b2=(\u03c9/v)\u00b2`\uff09\uff0c"
    "**\u5e93\u5185\u4ece\u672a\u88ab\u653b\u7834**\uff08\u4ec5\u5728\u300a\u65b9\u6cd5\u5168\u8c31\u300b\u6e05\u70b9\u4e2d\u88ab\u63d0\u53ca\u4e00\u6b21\uff09\u3002"
    "\uff08**\u6761\u76ee 15\uff1aPASS 0 / FAIL 9 / INFO 4 / BOUNDARY 2**\uff1b**\u63a7\u5236\u7ec4 5/5**\u3001**\u5b88\u536b 11/11**\u3001\u9000\u51fa\u7801 0\uff09\u3002"
    "**\u2605\u5206\u5c42\uff08\u4e0e\u65e2\u6709\u518c\u4e0d\u53ef\u76f8\u52a0\uff09**\uff1aS02 \u7684 \u00a718 \u505a\u6807\u51c6\u7269\u7406 Yukawa/Proca \u56db\u529b\u5f62\u5f0f\u7edf\u4e00\uff08\u6709\u6548\u7406\u8bba\u5c42\uff09\u3001"
    "\u00a719 \u505a\u8026\u5408\u8dd1\u52a8\u4e0e GUT \u80fd\u6807\u3001r146 \u5360\u4f4d\u505a\u56db\u529b\u7edf\u4e00\u53ef\u884c\u6027\u8de8\u518c\u5f52\u603b\uff1b**\u672c\u5377\u653b D5 \u672c\u8eab**\u3002"
    "**\u2605\u56db\u6761\u786c\u4f24**\uff1a"
    "\u2460**A1 \u7c7b\u578b\u4e24\u96be**\u2014\u2014 `c` \u4e3a\u6807\u91cf\u5219\u300c\u6807\u91cf\u51cf\u77e2\u91cf\u300d\u65e0\u5b9a\u4e49\uff1b\u53d6\u901f\u7387\u5219 P \u9000\u5316\u4e3a\u6807\u91cf\u3001\u627f\u4e0d\u4e86\u529b\u7684\u65b9\u5411\uff1b"
    "\u53d6\u5411\u91cf `C`\uff08\u7a7a\u95f4\u5149\u901f\u87ba\u65cb\u516c\u8bbe\uff09\u5219\u5f15\u51fa\u4e0b\u9762\u4e09\u6761 **\u4e09\u79cd\u8bfb\u6cd5\u5fc5\u5c45\u5176\u4e00\u3001\u6ca1\u6709\u4e00\u79cd\u5e72\u51c0**\uff1b"
    "\u2461**A2 \u9759\u6b62\u6781\u9650**\u2014\u2014 `P(v=0)=mC`\uff0c\u6a21\u957f **2.997925e+08 kg\u00b7m/s**\uff08m=1 kg\uff09\uff0c\u800c\u725b\u987f/\u76f8\u5bf9\u8bba\u5747\u4e3a **0** \u21d2 \u52a8\u91cf\u96f6\u70b9\u88ab\u6574\u4f53\u5e73\u79fb\uff1b"
    "\u2462**A3 \u5149\u901f\u6781\u9650**\u2014\u2014 `v\u2192c` \u65f6 `P\u21920` \u21d2 **\u5149\u5b50\u80fd\u91cf\u4e3a\u96f6**\uff1b\u673a\u8bfb\u7535\u5b50\u5728 \u03b2=1\u22121e\u22129 \u5904"
    "E_D5=**8.187106e\u221223 J** vs \u76f8\u5bf9\u8bba **1.830693e\u221209 J**\uff0c\u5dee **2.236068e+13 \u500d**\uff0c**\u5355\u8c03\u6027\u4e0e\u76f8\u5bf9\u8bba\u5b8c\u5168\u76f8\u53cd**\uff1b"
    "\u2463**B1 \u7b26\u53f7\u53cd\u53f7**\u2014\u2014 `F=dP/dt=m(dC/dt\u2212dv/dt)=\u2212ma`\uff0c\u4e0e `F=+ma` **\u5904\u5904\u53cd\u53f7**\uff1b\u5f39\u7c27\uff08k/m=1, x\u2080=1\uff09\u79ef\u5206\u5230 t=10\uff1a"
    "\u6807\u51c6 `cos10=\u22120.839072`\uff08\u6709\u754c\u632f\u8361\uff09vs \u6765\u6599 `cosh10=**11013.2329**`\uff08**\u6307\u6570\u53d1\u6563**\uff09\uff0c\u6bd4\u503c **1.3125e+04**\u3002"
    "**\u2605B2 \u51e0\u4f55\u529b**\uff1a\u82e5 `C` \u8d70\u87ba\u65cb\uff08\u516c\u8bbe\uff09\u5219\u9759\u6b62\u7269\u4f53\u53d7 `F_geo=m c\u00b2/R`\uff1b\u7535\u5b50\u6309 S02 \u53d6\u53c2 R=\u03bb_C/2\u03c0=**6.145916e\u221214 m** \u21d2 "
    "a=**1.462362e+30 m/s\u00b2**\u3001F=**1.332121e+00 N**\uff08\u91cd\u529b\u4ec5 8.93e\u221230 N\uff0c\u5dee **1.4912e+29 \u500d**\uff09\u3002"
    "**\u2605C \u7ec4\u65b0\u589e\u6027\u5b9a\u4ef7**\uff1a\u2460`\u03ba\u00b2+\u03c4\u00b2=(\u03c9/v)\u00b2` \u5728\u5300\u901f\u87ba\u65cb\u4e0b**\u5bf9\u4f46\u96f6\u65b0\u589e**\uff08\u673a\u8bfb\u6b8b\u5dee **1.110e\u221216**\uff09\u21d2 INFO\uff1b"
    "\u2461\u6765\u6599\u628a\u9002\u7528\u8303\u56f4\u5199\u6210\u300c\u5300\u901f\u87ba\u65cb / **\u68af\u5ea6\u78c1\u573a**\u300d\u662f**\u8d8a\u754c**\u2014\u2014\u78c1\u955c\u6548\u5e94\u4f7f `dv_\u2225/dt=\u2212v_\u2225\u2080\u00b2\u03b5/2` \u6301\u7eed\u975e\u96f6\uff0c"
    "\u8fd0\u52a8\u4e0d\u518d\u662f\u5300\u901f\u87ba\u65cb\uff0c\u6b8b\u5dee\u5355\u8c03\u5347\u81f3 **2.044e\u221201**\uff08\u6700\u574f\uff09\uff0c\u8fbe 1% \u6b8b\u5dee\u4ec5\u9700 **147 \u4e2a\u56de\u65cb\u5468\u671f**\uff1b\u4e14\u68af\u5ea6\u78c1\u573a\u4e0b `B` \u968f\u4f4d\u7f6e\u53d8\uff0c"
    "`\u03c9=qB/(\u03b3m)` **\u7528\u54ea\u4e00\u70b9\u7684 B \u672a\u58f0\u660e** \u21d2 **\u53e3\u5f84\u672a\u5b9a**\uff1b\u2462`F_e/F_m=c/v` \u662f\u6807\u51c6\u6d1b\u4f26\u5179\u529b\u590d\u8ff0\uff08\u6b8b\u5dee 1.481e\u221216\uff09\u21d2 INFO\uff1b"
    "\u2463`E=cB` \u88ab\u5199\u6210\u666e\u904d\u5173\u7cfb\uff0c\u5b9e\u9645**\u4ec5\u5bf9\u8f90\u5c04\u573a\u6210\u7acb**\uff08\u9759\u7535\u573a\u53cd\u4f8b\uff1a\u7535\u5b50\u7535\u8377 r=1 nm \u5904 E=**1.4400e+09 V/m** \u800c B=0 \u21d2 \u6bd4\u503c\u53d1\u6563\uff09\u3002"
    "**\u2605D1 \u540d\u5b9e\u4e4b\u8fa8\uff08\u4e09\u5c42\u673a\u8bfb\uff09**\uff1a\u53eb\u300c\u5927\u7edf\u4e00\u529b\u65b9\u7a0b\u300d\uff0c\u4f46"
    "\u3010\u65b9\u7a0b\u5c42\u3011\u975e\u7535\u78c1\u8026\u5408\u7b26\u53f7\uff08G / g_w\u00b7G_F\u00b7M_W / g_s\u00b7\u03b1_s\u00b7\u039b_QCD\uff09\u547d\u4e2d **0**\uff1b"
    "\u3010\u5168\u6587\u5c42\u3011\u5f15\u529b 2 \u6b21\u3001\u5f31\u529b 0\u3001\u5f3a\u529b 0\uff0c\u4e14\u5f15\u529b **\u53ea\u51fa\u73b0\u5728\u81ea\u627f\u5426\u5b9a\u53e5\u4e2d**\uff08\u300c\u4e0d\u89e3\u91ca\u5f15\u529b\u3001\u4e0d\u751f\u6210\u5e38\u6570\u3001\u4e0d\u5b8c\u6210\u56db\u529b\u7edf\u4e00\u300d\uff09\uff1b"
    "\u3010\u7535\u78c1\u4fa7\u301121 \u6b21 \u21d2 **\u53ea\u8986\u76d6\u7535\u78c1\u4e00\u79cd\u529b**\uff0c\u300c\u5927\u7edf\u4e00\u300d\u662f\u6807\u7b7e\u4e0d\u662f\u5185\u5bb9\uff08\u5df2\u767b\u8bb0\u9776\u81ea\u627f\uff0c\u9632\u8fc7\u5ea6\u6307\u63a7\uff09\u3002"
    "**\u2605D2 \u91cf\u7eb2\u95e8\u7981\u96f6\u5224\u522b\u529b**\uff1a`P=m(c-v)` \u4e0e\u6807\u51c6\u52a8\u91cf**\u5b8c\u5168\u9f50\u6b21**\uff08\u5747\u4e3a M\u00b7L\u00b7T\u207b\u00b9\uff09\u21d2 \u91cf\u7eb2\u5ba1\u8ba1\u653e\u4e0d\u51fa A2/A3/B1 \u4efb\u4f55\u4e00\u6761\uff1b"
    "\u672c\u5e93\u300c**\u91cf\u7eb2\u81ea\u6d3d \u2260 \u6210\u7acb**\u300d\u53c8\u4e00\u5b9e\u8bc1\uff1a\u9519\u5728\u7269\u7406\u89d2\u8272\u4e0e\u6781\u9650\u884c\u4e3a\uff0c\u4e0d\u5728\u91cf\u7eb2\u3002"
    "**\u2605\u2605E \u7ec4\u4fee\u590d\u5b9a\u4ef7\uff08\u5ef6\u7eed r147 \u673a\u5668\u751f\u6210\u53e3\u5f84\uff09**\uff1a\u5bf9 `P=m(C-v)` \u7684\u4e24\u4e2a\u52a0\u9879\u7edf\u4e00\u65bd\u52a0 {KEEP, FLIP, DEL}\uff0c"
    "\u5168\u679a\u4e3e 3\u00b2=**9** \u4e2a\u7ec4\u5408\uff1b\u5173\u95ed\u6761\u4ef6\u5168\u90e8\u673a\u8bfb\uff08A2 \u9759\u6b62\u52a8\u91cf=0 / A3 \u5149\u901f\u6781\u9650\u975e\u96f6 / B1 \u9700 v \u9879\u7cfb\u6570 +1 / B2 \u9700 C \u9879\u7cfb\u6570 0\uff09"
    "\u21d2 **\u5b58\u6d3b\u89e3\u6070 1 \u4e2a\uff1a`P = m v`**\uff0c**\u5373\u6807\u51c6\u725b\u987f\u52a8\u91cf**\u3002"
    "**\u2605\u603b\u88c1\u5b9a UNIFIED-FORCE-EQUATION-INCONSISTENT-AND-REPAIR-EQUALS-NEWTON**\uff1a\u65bd\u52a0\u552f\u4e00\u5b58\u6d3b\u89e3\u540e\uff0c"
    "`P=m(C-v)`\u2192\u725b\u987f\u52a8\u91cf\u3001`F=dP/dt`\u2192\u725b\u987f\u7b2c\u4e8c\u5b9a\u5f8b\u5b9a\u4e49\u5f0f\u3001`F_e/F_m=c/v`\u2192\u6d1b\u4f26\u5179\u529b\u590d\u8ff0\u3001`\u03ba\u00b2+\u03c4\u00b2`\u2192\u6807\u51c6 Frenet \u63a8\u8bba\u3001`E=cB`\u2192\u8f90\u5c04\u573a\u7279\u4f8b\u3001"
    "\u300c\u5927\u7edf\u4e00\u300d\u6807\u7b7e\u88ab\u8bc1\u4f2a \u21d2 **\u5269\u4f59\u975e\u5df2\u77e5\u7269\u7406\u9879 = 0**\u3002**\u6765\u6599\u76f8\u5bf9\u6807\u51c6\u7269\u7406\u7684\u5168\u90e8\u589e\u91cf\uff08\u90a3\u4e2a m\u00b7C \u9879\uff09\u6b63\u662f\u5168\u90e8\u9519\u8bef\u7684\u6765\u6e90**\u3002"
    "**\u2605\u81ea\u6293 3 \u5904**\uff1a\u2460\u7b26\u53f7\u6e05\u70b9\u6f0f\u8ba1\u8fde\u5199\uff08`qB` \u88ab\u8fb9\u754c\u6b63\u5219\u6f0f\u6389\uff09\u21d2 \u6539\u4e3a\u4e09\u5c42\u6e05\u70b9\uff08\u65b9\u7a0b\u5c42 / \u5168\u6587\u5c42 / \u7535\u78c1\u4fa7\uff09\uff1b"
    "\u2461\u9759\u7535\u573a\u53cd\u4f8b\u521d\u53d6 r=1 m \u592a\u5f31\uff08E=1.44e\u22129 V/m\uff09\u21d2 \u6539\u539f\u5b50\u5c3a\u5ea6 r=1 nm\uff08E=1.44e+09 V/m\uff09\uff1b"
    "\u2462B3 \u672a\u6ce8\u660e\u8d28\u91cf\u53e3\u5f84\u21d2 \u8865\u4e0a\u300c\u53d6\u7535\u5b50\u300d\u3002"
    "**\u2605\u2605\u65b9\u6cd5\u4fa7\u65b0\u6212\u5f8b\uff08\u5df2\u5199\u5165 MEMORY\uff09**\uff1a"
    "**\u521d\u59cb\u6761\u4ef6\u9000\u5316\u9677\u9631**\u2014\u2014\u5224\u636e\u51fd\u6570\u82e5\u53ea\u5728\u5355\u4e2a\u53c2\u6570\u70b9\u91c7\u6837\uff0c\u4f1a\u88ab\u300c\u53c2\u6570\u9000\u5316\u300d\u9a97\u8fc7"
    "\uff08r147 \u7684 \u03c1=r\u03c9/c\u21920 \u4f7f\u87ba\u65cb\u53d8\u76f4\u7ebf\uff1b\u672c\u5377\u7684\u5300\u901f\u87ba\u65cb `A=0` \u662f\u9178\u6027\u5f0f\u7684\u96f6\u6d4b\u70b9\uff09\uff1b"
    "**\u5fc5\u987b\u5728\u53c2\u6570\u7f51\u683c\u4e0a\u626b\u63cf\u5e76\u8981\u6c42\u5355\u8c03**\uff08\u672c\u5377\u626b A/v_\u2225 \u4e94\u6863\uff0c\u6b8b\u5dee 1.1e\u221216 \u2192 2.0e\u221201 \u5355\u8c03\uff09\u3002"
    "\u7eaf\u6807\u51c6\u5e93\uff08RK4 2 \u4e07\u6b65 / \u89e3\u6790\u5bfc\u6570 Frenet \u907f\u4e09\u9636\u6570\u503c\u5dee\u5206 / \u91cf\u7eb2\u56db\u5143\u7ec4 / \u6b63\u5219\u6e05\u70b9\uff09\uff0c\u65e0\u7b2c\u4e09\u65b9\u4f9d\u8d56\u3002"
)

JUDGE_LINE = (
    "\u251c\u2500\u2500 \u5224\u5b9a_TUFT-r148_D5\u5927\u7edf\u4e00\u529b\u65b9\u7a0b\u9996\u653b\u4e0e\u4fee\u590d\u5b9a\u4ef7_2026-10-22.md  # \u65b0\u589e\uff08**r148 \u00b7 2026-10-22**\uff1a"
    "**D5 \u5927\u7edf\u4e00\u529b\u65b9\u7a0b\u5224\u5b9a\u518c**\uff08\u4e5d\u8282\uff1a\u5377\u53f7\u4e0e\u5206\u5de5\u58f0\u660e\uff08**\u4e0e S02 \u00a718/\u00a719 \u53ca r146 \u4e25\u683c\u5206\u5c42\u3001\u6761\u76ee\u4e0d\u53ef\u76f8\u52a0**\uff09/ \u5224\u5b9a / "
    "\u65b9\u6cd5\u4e0e\u63a7\u5236\u7ec4 5 \u9879 / \u6761\u76ee\u603b\u8868 15 \u6761 / \u9010\u6761\u88c1\u5b9a / "
    "**\u2605\u4fee\u590d\u5b9a\u4ef7\uff1a\u552f\u4e00\u5b58\u6d3b\u89e3\u5c31\u662f\u725b\u987f\u52a8\u91cf** / \u5b88\u536b 11 \u6761 / "
    "\u4ecd\u672a\u95ed\u5408\u9879 5 \u6761 / \u7ea2\u7ebf 4 \u6761 / Glossary\uff09\u3002"
    "**\u63a7\u5236\u7ec4 5/5**\uff1a\u6807\u51c6\u76f8\u5bf9\u8bba\u52a8\u91cf p=\u03b3mv \u5728 v=0 \u7ed9 0\u3001\u5728 \u03b2=0.9 \u7ed9 5.638653e\u221222 kg\u00b7m/s\uff08A2/A3 \u5224\u636e\u5bf9\u5176\u4e0d\u89e6\u53d1\uff09\uff1b"
    "\u6807\u51c6 F=+ma \u5f39\u7c27\u6709\u754c\uff08|x|\u22641\uff09\uff08B1 \u5224\u636e\u5bf9\u5176\u4e0d\u89e6\u53d1\uff09\uff1b"
    "Frenet \u5de5\u5177\u5728\u6807\u51c6\u5300\u901f\u87ba\u65cb\u4e0a\u6b8b\u5dee 1.110e\u221216\uff08\u8bc1 C2 \u6b8b\u5dee\u6765\u81ea\u7269\u7406\u800c\u975e\u5de5\u5177\uff09\uff1b"
    "\u91cf\u7eb2\u5de5\u5177\u81ea\u68c0 p=mv / E=mc\u00b2 / F=ma \u5747\u9f50\u6b21\uff1b\u6807\u51c6\u6d1b\u4f26\u5179\u529b\u5728\u5e73\u9762\u6ce2\u4e0b\u590d\u73b0 c/v\uff08\u6b8b\u5dee <1e\u221212\uff09\u3002"
)

DATA_LINE = (
    "    \u251c\u2500\u2500 TUFT-r148_D5\u5927\u7edf\u4e00\u529b\u65b9\u7a0b\u9996\u653b\u4e0e\u4fee\u590d\u5b9a\u4ef7_2026-10-22.json / .md / _report.txt  # \u65b0\u589e\uff08**r148 \u00b7 2026-10-22**\uff09"
    "D5 \u9996\u653b\u673a\u68c0\u4ea7\u7269\uff0815 \u6761\u5224\u5b9a + **11 \u6761 guard** + \u63a7\u5236\u7ec4 5 \u9879 + metrics \u539f\u59cb\u673a\u8bfb\u91cf\uff1b"
    "key_numbers\uff1a\u9759\u6b62\u52a8\u91cf **2.997925e+08 kg\u00b7m/s**\uff08\u6807\u51c6 0\uff09\u3001"
    "\u03b2=1\u22121e\u22129 \u5904 E_D5=**8.187106e\u221223 J** vs \u76f8\u5bf9\u8bba **1.830693e\u221209 J**\uff08\u5dee **2.236068e+13**\uff09\u3001"
    "\u5149\u5b50\u6781\u9650 P_D5=**0** vs \u6807\u51c6 **1.105110e\u221227 kg\u00b7m/s / 2.0678 eV**\u3001"
    "\u5f39\u7c27\u53cd\u53f7 cosh10/cos10=**1.3125e+04**\uff08\u6570\u503c\u8bef\u5dee 4.37e\u221215\uff09\u3001"
    "\u7535\u5b50\u51e0\u4f55\u529b **1.332121e+00 N**\uff08\u91cd\u529b 8.93e\u221230 N\uff0c**1.4912e+29 \u500d**\uff09\u3001"
    "\u5300\u901f\u87ba\u65cb\u6052\u7b49\u5f0f\u6b8b\u5dee **1.110e\u221216** vs \u53d8\u901f\u6700\u574f **2.044e\u221201**\uff08\u5355\u8c03\uff0c\u78c1\u955c\u8fbe 1% \u9700 **146.9 \u5468\u671f**\uff09\u3001"
    "F_e/F_m \u590d\u73b0\u6b8b\u5dee **1.481e\u221216**\u3001\u9759\u7535\u573a E=**1.4400e+09 V/m**\uff08r=1 nm\uff09\u3001"
    "\u540d\u5b9e\u6e05\u70b9 \u975e\u7535\u78c1\u8026\u5408\u7b26\u53f7 **0** / \u7535\u78c1\u4fa7 **21**\uff1b"
    "**\u4f4e\u9636\u7b97\u5b50\u679a\u4e3e 3\u00b2=9 \u7ec4\u5408\uff0c\u5b58\u6d3b\u89e3 1 \u4e2a = `P=mv`\uff08\u725b\u987f\u52a8\u91cf\uff09**\uff09"
)

CHAPTER = """
## 增量登记（2026-10-22 · r148）：D5《大统一力方程》首攻与修复定价

- **命题**：用户点名「**力的大统一方程**」。库内对应的原始来料是
  `01_独立体系/S02_空间光速螺旋统一力/04_理论推导/D5_大统一力方程/`（README.md + D5_大统一力方程.py），
  即张祥前体系的**原始公设层方程**：`P=m(c-v)`、`F=dP/dt`、`F_e/F_m=c/v`、`E=cB`、
  基石 `kappa^2+tau^2=(omega/v)^2`。该靶**从未被攻破**（全库仅在《方法全谱》清点中被提及一次）。
- **★分层（与既有册不可相加）**：S02 的 §18 做**标准物理 Yukawa/Proca 四力形式统一**（有效理论层，
  且自认只攻「形式统一+极限正确」，不攻「参数物理化+QCD 禁闭」）；§19 做**耦合跑动与 GUT 能标**；
  r146 占位做**四力统一可行性跨册归总**。**本卷攻 D5 本身**，不在同一层。
- **产物**：`源码/TUFT-r148_D5大统一力方程首攻与修复定价_2026-10-22.py`（纯标准库）+ `源码/_run_r148.py`
  + `数据/同名.{json,md,_report.txt}` + `数据/判定_TUFT-r148_D5大统一力方程首攻与修复定价_2026-10-22.md`。
  复现 `python 源码/_run_r148.py`（`-W error::SyntaxWarning`），**退出码 0**。
- **★条目与裁定**：**条目 15（PASS 0 / FAIL 9 / INFO 4 / BOUNDARY 2）**、**控制组 5/5**、**守卫 11/11**、退出码 0；
  总裁定 **UNIFIED-FORCE-EQUATION-INCONSISTENT-AND-REPAIR-EQUALS-NEWTON**。
  **PASS=0 是结论不是判据失效**：凡「正确但与已知物理逐字相同」一律降 INFO（C1/C3），分辨力由控制组 5/5 背书。
- **★四条硬伤（机读）**：
  ①**A1 类型两难** —— `P=m(c-v)` 三种读法必居其一：c 为标量则「标量减矢量」无定义；v 取速率则 P 退化为标量、
  承载不了力的方向；c 取矢量 C（空间光速螺旋公设）则引出 ② ③ ④。**没有一种读法是干净的。**
  ②**A2 静止极限** —— `P(v=0)=mC`，模长 **2.997925e+08 kg·m/s**（m=1 kg），而牛顿与相对论均为 **0** ⇒ 动量零点被整体平移。
  ③**A3 光速极限** —— `v→c` 时 `P→0` ⇒ **光子能量为零**；电子在 β=1−1e−9 处 E_D5=**8.187106e−23 J**
  vs 相对论 **1.830693e−09 J**，差 **2.236068e+13 倍**，且**单调性与相对论完全相反**（相对论发散、来料趋零）。
  ④**B1 符号反号** —— `F=dP/dt=m(dC/dt−dv/dt)=−ma`，与 `F=+ma` 处处反号；弹簧（k/m=1, x₀=1）积分到 t=10：
  标准 `cos10=−0.839072`（有界振荡）vs 来料 `cosh10=**11013.2329**`（指数发散），比值 **1.3125e+04**。
  ⇒ 一切束缚势变反束缚：行星轨道、弹簧、单摆全部指数飞散。
- **★B2 几何力**：若 C 走螺旋（公设），静止物体受 `F_geo=m c²/R`；电子按 S02 取参 R=λ_C/2π=**6.145916e−14 m**
  ⇒ a=**1.462362e+30 m/s²**、F=**1.332121e+00 N**（重力仅 8.93e−30 N，**1.4912e+29 倍**）。
- **★C 组新增性定价**：①`kappa²+tau²=(omega/v)²` 在匀速螺旋下**对但零新增**（残差 **1.110e−16**）⇒ INFO；
  ②来料把适用范围写成「匀速螺旋 / **梯度磁场**」是**越界** —— 磁镜效应使 `dv_∥/dt=−v_⊥0²ε/2` 持续非零，
  运动不再是匀速螺旋，残差单调升至 **2.044e−01**，**达 1% 残差仅需 146.9 个回旋周期**；
  且梯度磁场下 B 随位置变，`omega=qB/(γm)` **用哪一点的 B 未声明** ⇒ **口径未定**；
  ③`F_e/F_m=c/v` 是标准洛伦兹力复述（残差 1.481e−16）⇒ INFO；④`E=cB` 只对辐射场成立
  （静电场反例：电子电荷 r=1 nm 处 E=**1.4400e+09 V/m** 而 B=0 ⇒ 比值发散）。
- **★D1 名实之辩（三层机读）**：叫「大统一力方程」，但【方程层】非电磁耦合符号（G / g_w·G_F·M_W / g_s·α_s·Λ_QCD）
  命中 **0**；【全文层】引力 2 次、弱力 0、强力 0，且引力**只出现在自承否定句**里
  （「不解释引力、不生成常数、不完成四力统一」）；【电磁侧】21 次。⇒ **只覆盖电磁一种力**，
  「大统一」是标签不是内容。**已登记靶自承**（attack16 判据④），不是过度指控。
- **★D2 量纲门禁零判别力**：`P=m(c-v)` 与标准动量**完全齐次**（均 M·L·T⁻¹），A2/A3/B1 **全部量纲自洽**
  ⇒ 量纲审计一条都拦不住。本库「**量纲自洽 ≠ 成立**」又一处实证：错在物理角色与极限行为，不在量纲。
- **★★E 组修复定价（延续 r147 的机器生成口径）**：对 `P=m(C−v)` 的两个加项统一施加 {KEEP, FLIP, DEL}，
  全枚举 3²=**9** 个组合，关闭条件全部机读（A2 静止动量=0 / A3 光速极限非零 / B1 需 v 项系数 +1 / B2 需 C 项系数 0）
  ⇒ **存活解恰 1 个：`P = m v`，即标准牛顿动量**。
  施加后：`P=m(C−v)`→牛顿动量、`F=dP/dt`→牛顿第二定律定义式、`F_e/F_m=c/v`→洛伦兹力复述、
  `kappa²+tau²`→标准 Frenet 推论、`E=cB`→辐射场特例、「大统一」标签被证伪
  ⇒ **剩余非已知物理项 = 0**。
  **★最强的一句**：来料相对标准物理的全部增量（那个 `m·C` 项）**正是全部错误的来源** ——
  删掉它物理就对了，但也就什么都不剩了。这与 r142（S17）的「修复即自杀」同型，是**第三次**复发。
- **★自抓 3 处**：①符号清点漏计连写（`qB` 被边界正则漏掉）⇒ 改为三层清点（方程层 / 全文层 / 电磁侧）；
  ②静电场反例初取 r=1 m 太弱（E=1.44e−09 V/m）⇒ 改原子尺度 r=1 nm（E=1.44e+09 V/m）；
  ③B3 未注明质量口径 ⇒ 补「取电子」。
- **★方法侧新戒律（已写入 MEMORY）**：**初始条件退化陷阱** —— 判据函数若只在单个参数点采样会被「参数退化」骗过：
  r147 的 ρ=rω/c→0 使螺旋退化为直线；本卷的「匀速螺旋 A=0」是恒等式的**测度零**成立点。
  **必须在参数网格上扫描并要求单调性**（本卷扫 A/v_∥ 五档，残差 1.1e−16 → 2.0e−01 单调）。
- **仍未闭合项（未做即未证）**：①C2 用的是**运动学反例**（螺距变化 + 磁镜绝热不变量），
  **未做**真实梯度磁场的洛伦兹力数值积分，也**未用**三阶数值差分直接测 τ（该通道地板 ~1e−7，不可靠）；
  ②梯度磁场下 ω 的口径未代选；③修复空间仍是**低阶算子**，高阶算子（改函数形式 / 改向量结构 / 改假设 / 新增内容）未枚举；
  ④B2 的 R 取 S02 口径，若来料另取 R 则数值变但「静止受力非零且巨大」的**定性结论不变**（F_geo ∝ 1/R）；
  ⑤未检索实验文献。
- **不自推**：不代来料补方程；不重判 §18 / §19 / r140 / r142 / r147；不修改任何既有产物字节。
- **红线**：数学自洽 ≠ 实验证实；**修复可行 ≠ 修复后仍有内容**；**低阶空间完备 ≠ 全空间完备**；靶自承优先登记。
- **治理**：**未跑** `refresh_catalog.py`（并发会话活跃，整体重生成会回退他人更大版本，待批准）；
  **未改** `verify.py`；**未做** git 操作；**未触碰**他人产物字节。
  已完成四处 README 登记（源码树 / 判定册树 / 数据树 / 本增量登记章）。**下轮从 r149 起。**
"""

out = []
hit = {"src": 0, "judge": 0, "data": 0}
for ln in lines:
    out.append(ln)
    s = ln.strip()
    if hit["src"] == 0 and s.startswith(SRC_ANCHOR):
        out.append(SRC_LINE)
        hit["src"] = 1
    elif hit["judge"] == 0 and s.startswith(JUDGE_ANCHOR):
        out.append(JUDGE_LINE)
        hit["judge"] = 1
    elif hit["data"] == 0 and s.startswith(DATA_ANCHOR):
        out.append(DATA_LINE)
        hit["data"] = 1

txt = "\n".join(out)
if not txt.endswith("\n"):
    txt += "\n"
txt += CHAPTER

with io.open(README, "w", encoding="utf-8", newline="\n") as f:
    f.write(txt)

print("hits:", hit)
print("lines:", len(lines), "->", len(txt.split("\n")))
