# -*- coding: utf-8 -*-
"""r165 污染修复：截断旧版残留，重建 report_and_write 尾部（自抓节 + 红线 + 落盘）。"""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

P = (r'd:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化'
     r'\源码\TUFT-r165_D5四力闭合层_单粒子运动学量与源依赖冲突_2026-10-24.py')

with io.open(P, encoding='utf-8', newline='') as f:
    s = f.read()
NL = '\r\n' if '\r\n' in s else '\n'
L = s.split(NL)

MARK = u'    b("   ' + u'\u300c' + u'short write_to_file'
cut = -1
for i, ln in enumerate(L):
    if u'def det3(a, b, c):' in ln and i > 600:
        cut = i
        break
print('cut =', cut, 'prev =', repr(L[cut - 1][:70]) if cut > 0 else None)
if cut < 0:
    print('ABORT: pollution mark not found')
    sys.exit(1)

TAIL = [
    u'    b("   ' + u'\u300c' + u'short write_to_file ' + u'\u5efa' + u' ' + u'\u542b' + u' `# __NEXT__` ' + u'\u54e8' + u' ' + u'\u5175' + u' + ' + u'\u591a' + u' ' + u'\u6b21' + u' replace_in_file ' + u'\u586b' + u' ' + u'\u5145' + u'\u300d' + u'")',
    u'    b("2. **group_f ' + u'\u91cf' + u' ' + u'\u7eb2' + u' ' + u'\u6307' + u' ' + u'\u6570' + u' ' + u'\u9996' + u' ' + u'\u7248' + u' ' + u'\u5199' + u' ' + u'\u9519' + u'")',
]

# 上面仅用于定位校验；真正尾部用下方 raw 文本
TAIL_RAW = u'''    b("   \u300cshort write_to_file \u5efa\u542b `# __NEXT__` \u54e8\u5175 + \u591a\u6b21 replace_in_file \u586b\u5145\u300d")
    b("2. **group_f \u91cf\u7eb2\u6307\u6570\u9996\u7248\u5199\u9519**\uff08\u628a M \u5206\u91cf\u5199\u6210\u591a\u91cf\u4e4b\u548c\uff09\u21d2 \u5df2\u6539\u4e3a")
    b("   M=a5\u3001L=\u2212a0\u2212a1+a3+a4\u3001T=\u2212a2\u2212a3\u2212a4\u3001Q=a6\uff0c\u5e76\u4e0e\u63a7\u5236\u7ec4 C1 \u4e92\u9501\u3002")
    b("3. **disc_res \u521d\u7248\u6b8b\u7559\u4e00\u884c\u65e0\u6548\u7b97\u5f0f**\uff08\u5148\u7b97 0.25 \u518d\u8986\u76d6 0.75\uff09\u21d2 \u5df2\u6e05\u7406\u4e3a\u5355\u4e00\u8d4b\u503c\u3002")
    b("4. \u2605**\u624b\u5199\u300c\u89e3\u6790\u5f0f \u03c1/r = 1 \u2212 e\u00b7cos\u03c6\u300d\u662f\u9519\u7684**\uff08\u5b88\u536b G4/G5 \u5f53\u573a\u5224 BAD\uff1a")
    b("   \u673a\u8bfb\u8de8\u5ea6 4.044952 \u800c\u6211\u9884\u671f 4.0\u3001\u673a\u8bfb\u4e0e\u624b\u5199\u5f0f\u504f\u5dee 0.75\uff09\u21d2 \u5df2\u7531")
    b("   \u03ba = u\u00b3(u+u'')/(u\u00b2+u'\u00b2)^{3/2} \u4e0e u+u''\u22611/p **\u91cd\u65b0\u63a8\u51fa\u6b63\u786e\u95ed\u5f0f**")
    b("   \u03c1/r = p(u\u00b2+u'\u00b2)^{3/2}/u\u00b2\uff08u=(1+e cos\u03c6)/p\u3001u'=\u2212e sin\u03c6/p\uff09\uff0c")
    b("   \u4e94\u76f8\u4f4d\u9010\u4f4d\u4e00\u81f4\u3002**\u672c\u5e93\u300c\u624b\u7b97\u89e3\u6790\u5f0f\u5fc5\u9519\u3001\u5fc5\u987b\u673a\u5668\u515c\u5e95\u300d\u7eaa\u5f8b\u53c8\u4e00\u5b9e\u8bc1**\uff1a")
    b("   \u82e5\u5f53\u65f6\u628a\u5b88\u536b\u9608\u503c\u653e\u5bbd\u5230\u300c\u5dee\u4e0d\u591a\u300d\uff0c\u5c31\u4f1a\u628a\u4e00\u6761\u5047\u6052\u7b49\u5f0f\u5199\u8fdb\u7ed3\u8bba\u3002")
    b("")
    b("## 07. \u7ea2\u7ebf")
    b("")
    b("- \u6570\u5b66\u81ea\u6d3b \u2260 \u5b9e\u9a8c\u8bc1\u5b9e\uff1b**\u6052\u7b49\u5f0f\u6210\u7acb \u2260 \u6709\u65b0\u5185\u5bb9**\uff1b**\u6210\u7acb \u2260 \u5ba3\u79f0\u57df\u65e0\u8fb9\u754c**\u3002")
    b("- **\u9776\u81ea\u627f\u4f18\u5148**\uff1a\u672c\u5377\u4e0d\u628a\u9776\u5df2\u81ea\u627f\u7684\u300c\u672a\u505a\u56db\u529b\u7edf\u4e00\u300d\u5f53\u4f5c\u53d1\u73b0\u3002")
    b("- \u9632\u8fc7\u5ea6\u6307\u63a7\u4e0e\u9632\u6f0f\u5224\u7b49\u540c\u91cd\u8981\uff1aF1/F2 \u56e0\u9775\u672a\u5ba3\u79f0 r\u207b\u00b2 \u800c\u964d INFO/BOUNDARY\u3002")
    b("")
'''

new = L[:cut] + TAIL_RAW.split(u'\n')
if new and new[-1].strip() == u'':
    new.pop()
with io.open(P, 'w', encoding='utf-8', newline='') as f:
    f.write(NL.join(new) + NL)
print('written, lines =', len(new) + 1)
