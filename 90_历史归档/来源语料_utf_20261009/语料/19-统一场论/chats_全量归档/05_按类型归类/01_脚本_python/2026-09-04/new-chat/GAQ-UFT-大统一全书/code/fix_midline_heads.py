# -*- coding: utf-8 -*-
"""
第二阶段：拆分"行中间"粘连的标题（## X.Y / ### X.Y.Z / ### 例 N 出现在正文行中部）。
原理：对每个已知行中标题标记，定位其正文起始子串，把该行拆成：
  前一正文段 / 标题行 / 后续正文（可能继续含行中标题 → 递归）
标题文本取原文（标记与正文起始子串之间的内容），保证与作者原稿一致。
用法：python fix_midline_heads.py apply   （只支持 apply，执行前先 print 计划）
"""
import io, glob, os, re, sys

BASE = r'C:\Users\mo\Doubao\chats\2026-09-04\new-chat\GAQ-UFT-大统一全书'
MS = os.path.join(BASE, 'manuscript')

# {文件名: {行中标题标记: 正文起始子串}}
MID = {
    'ch00-序章.md': {'## 0.10': '序章确立了'},
    'ch01-总纲.md': {'## 1.11': '总纲给出了'},
    'ch02-第一公理与第二公理.md': {
        '## 2.4': '### 例 1',
        '### 例 1': '对 $\\mathbf r(t)',
        '## 2.9': '两条公理提供了',
    },
    'ch03-第三公理.md': {
        '## 3.5': '可见世界只有 4 维',
        '## 3.6': '### 3.6.1',
        '### 3.6.1': '$32=2^5$',
        '## 3.12': '第三公理把舞台',
    },
    'ch05-电磁力.md': {
        '## 5.4': '框架在对话历史中',
        '## 5.8': '本章反复出现',
        '## 5.11': '电磁力是理解',
    },
    'ch06-弱力与电弱统一.md': {'## 6.5': '中微子混合的最直接后果'},
    'ch08-引力.md': {
        '## 8.2': 'Einstein 场方程（1915）',
        '## 8.6': '为了给',
        '## 8.12': '引力是',
    },
    'ch09-精细结构常数.md': {
        '## 9.4': '框架的历史表述',
        '## 9.12': '本章把',
    },
    'ch11-全常数矩阵.md': {
        '## 11.5': '读者问',
        '## 11.9': '在常数问题里',
    },
    'ch12-宇宙演化.md': {
        '## 12.5': '- 标准宇宙学',
        '## 12.13': '标准宇宙学',
    },
    'ch13-暗物质与暗能量.md': {
        '## 13.4': '框架的历史主张',
        '## 13.13': '暗物质的存在',
    },
    'ch14-哈勃张力.md': {
        '## 14.5': '晚期宇宙测量',
        '## 14.12': '哈勃张力是',
    },
    'ch15-量子测量与观测者.md': {'## 15.4': '框架的历史主张'},
    'ch18-可证伪性清单.md': {
        '## 18.2': '| # | 框架主张',
        '## 18.5': '科学方法论有一条',
    },
    'ch19-诚实审计.md': {'## 19.11': '诚实审计总账给出'},
}

# 所有行中标题标记（按长度降序，避免 ## 2 误吞 ### 2.4 之类）
ALL_MARKERS = sorted({m for d in MID.values() for m in d}, key=len, reverse=True)

def find_marker_at(s, start=0):
    """在 s 中从 start 起找下一个行中标题标记，返回 (marker, pos)；pos 为标记起始。"""
    best = None
    for mk in ALL_MARKERS:
        i = s.find(mk, start)
        while i >= 0:
            # 前一字符不是 #（避免在 ### 内部匹配 ##）
            prev_ok = (i == 0 or s[i-1] != '#')
            # 标记后不是继续的小节号/点号（避免 ## 3.6 匹配 ## 3.6.2）
            end = i + len(mk)
            next_ok = (end >= len(s) or (s[end] not in '.0123456789'))
            if prev_ok and next_ok:
                if best is None or i < best[1]:
                    best = (mk, i)
                break
            i = s.find(mk, i + 1)
    return best

def split_segment(seg, chap, out):
    """处理一段可能含行中标题的文本，追加拆分后的行到 out。"""
    found = find_marker_at(seg, 0)
    if found is None:
        if seg.strip():
            out.append(seg.rstrip())
        return
    mk, pos = found
    # 标记前的正文
    if pos > 0:
        pre = seg[:pos].rstrip()
        if pre.strip():
            out.append(pre)
    # 标题标记之后的内容：标题文本 + 正文
    body_start = MID[chap][mk]
    rest = seg[pos + len(mk):].lstrip()
    idx = rest.find(body_start)
    if idx < 0:
        # 找不到正文起始：整个当标题行，并警告
        print(f'  [WARN] {chap} marker {mk} 未找到正文起始 "{body_start}"')
        out.append(mk + ' ' + rest)
        return
    heading = rest[:idx].rstrip()
    body = rest[idx:]
    # 保留原文间距：标记后原本是空格则用一个空格连接，否则直接相连
    after_mk = seg[pos + len(mk):pos + len(mk) + 1]
    sep = ' ' if after_mk == ' ' else ''
    out.append(mk + sep + heading)
    # 递归处理正文（可能含下一个行中标题）
    if body.strip():
        split_segment(body, chap, out)

def main():
    print('=== 第二阶段：行中标题拆分（计划）===')
    plan = {}
    for p in sorted(glob.glob(os.path.join(MS, 'ch*.md'))):
        chap = os.path.basename(p)
        with io.open(p, encoding='utf-8') as f:
            lines = f.read().split('\n')
        hits = 0
        for ln in lines:
            for mk in ALL_MARKERS:
                if mk in ln:
                    i = ln.find(mk)
                    if i == 0:
                        continue
                    hits += 1
                    print(f'  {chap[:6]} L: ...{ln[max(0,i-12):i]}||{mk} {ln[i+len(mk):][:30]}')
        plan[chap] = hits
    print('--- 命中行中标题总数:', sum(plan.values()))
    if 'apply' not in sys.argv:
        print('（未写入；加 apply 参数执行）')
        return
    # 执行
    for p in sorted(glob.glob(os.path.join(MS, 'ch*.md'))):
        chap = os.path.basename(p)
        if chap not in MID:
            continue
        with io.open(p, encoding='utf-8') as f:
            lines = f.read().split('\n')
        new_lines = []
        changed = 0
        for ln in lines:
            # 仅处理"行中间"含标题标记的行（标记不在行首）
            fm = find_marker_at(ln, 0)
            if fm is None or fm[1] == 0:
                new_lines.append(ln)
                continue
            buf = []
            split_segment(ln, chap, buf)
            new_lines.extend(buf)
            changed += 1
        if changed:
            with io.open(p, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            print(f'  已更新 {chap}（{changed} 行）')
    print('--- 完成')

if __name__ == '__main__':
    main()
