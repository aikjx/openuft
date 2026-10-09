# -*- coding: utf-8 -*-
"""按章输出两种口径字数：合并口径(merge_book 法，含表格)与严格口径(剔除表格)。"""
import io, re, glob, os

BASE = r'C:\Users\mo\Doubao\chats\2026-09-04\new-chat\GAQ-UFT-大统一全书'

def zh(s):
    return len(re.findall(r'[\u4e00-\u9fff]', s))

def merge_count(text):
    # 与 merge_book.py 完全一致：剔除代码块与公式后统计汉字
    body = re.sub(r'```.*?```', '', text, flags=re.S)
    body = re.sub(r'\$\$.*?\$\$', '', body, flags=re.S)
    body = re.sub(r'\$[^$\n]*\$', '', body)
    return zh(body)

def strict_count(text):
    body = re.sub(r'```.*?```', '', text, flags=re.S)
    body = re.sub(r'\$[^$]*\$', '', body)
    body = re.sub(r'^\s*\|.*\|$', '', body, flags=re.M)
    body = re.sub(r'^#{1,6}\s*', '', body, flags=re.M)
    return zh(body)

def main():
    files = sorted(glob.glob(os.path.join(BASE, 'manuscript', 'ch*.md')))
    cover = os.path.join(BASE, 'manuscript', '000-封面.md')
    tm = ts = 0
    for f in files:
        txt = io.open(f, encoding='utf-8').read()
        m, s = merge_count(txt), strict_count(txt)
        tm += m; ts += s
        print('| %s | %d | %d |' % (os.path.basename(f)[:6], m, s))
    txt = io.open(cover, encoding='utf-8').read()
    cm, cs = merge_count(txt), strict_count(txt)
    tm += cm; ts += cs
    print('| 封面 | %d | %d |' % (cm, cs))
    print('合计(合并口径) %d  合计(严格口径) %d' % (tm, ts))

if __name__ == '__main__':
    main()
