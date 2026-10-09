# -*- coding: utf-8 -*-
"""按章统计汉字数（与 merge_book 同口径）并输出 Markdown 台账行。"""
import io, re, glob, os

BASE = r'C:\Users\mo\Doubao\chats\2026-09-04\new-chat\GAQ-UFT-大统一全书'

def zh_count(text):
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    text = re.sub(r'\$[^$]*\$', '', text)
    text = re.sub(r'^\s*\|.*\|$', '', text, flags=re.M)
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.M)
    text = re.sub(r'[^\u4e00-\u9fff]', '', text)
    return len(text)

def main():
    files = sorted(glob.glob(os.path.join(BASE, 'manuscript', 'ch*.md')))
    total = 0
    rows = []
    for f in files:
        n = zh_count(io.open(f, encoding='utf-8').read())
        total += n
        name = os.path.basename(f)[:6]
        rows.append((name, n))
    # 封面单独计
    cover = os.path.join(BASE, 'manuscript', '000-封面.md')
    cn = zh_count(io.open(cover, encoding='utf-8').read()) if os.path.exists(cover) else 0
    for name, n in rows:
        print('| %s | - | - | %d | 已复核 |' % (name, n))
    print('| 封面 | - | - | %d | 已复核 |' % cn)
    print('正文合计(含封面):', total + cn)

if __name__ == '__main__':
    main()
