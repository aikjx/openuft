"""从全球研究登记生成中文路线导航、文献登记和覆盖矩阵。"""
import argparse
import csv
import io
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]

def csv_text(header, rows):
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue()

def views(root):
    base = root / '05_全球研究'
    data = json.loads((base / '全球研究登记.json').read_text(encoding='utf-8'))
    rows = data['路线']
    ids, directories = set(), set()
    outputs = {}
    intro = '# 全球研究路线\n\n**AI科技星 · [aikjx.com](https://aikjx.com)**\n\n[返回全球研究](../README.md) · [覆盖矩阵](覆盖矩阵.csv)\n\n首批代表性研究路线。目录均为中文，来源保留实际作者；入口核对不等于全文评审、实验验证或全球完整覆盖。\n\n| 编号 | 路线 | 研究对象 |\n|---|---|---|\n'
    for row in rows:
        rid, directory = row['编号'], row['目录']
        if rid in ids or directory in directories or not directory or '/' in directory or '\\' in directory or directory in {'.', '..'}:
            raise ValueError('重复编号或无效目录: ' + directory)
        if urlparse(row['原始链接']).scheme != 'https':
            raise ValueError('来源需提供 HTTPS 原始链接: ' + rid)
        ids.add(rid); directories.add(directory)
        intro += '| {} | [{}]({}/README.md) | {} |\n'.format(rid, row['名称'], directory, row['研究对象'])
        text = '# {}\n\n[全球路线总表](../README.md) · [文献来源](../../01_文献来源/README.md)\n\n{}\n\n## 体系边界\n\n{}\n\n## 来源入口\n\n- 来源编号：{}\n- 原作者：{}\n- 原文：[{}]({})\n- 年份：{}\n- 核实日期：{}\n- 核实范围：{}\n\n## 后续研究放置\n\n本路线的中文阅读笔记放在此目录，以来源编号命名；推导比较进入“跨体系研究”，形成独立公设后才在“独立体系”登记。下一步需明确自由度、作用量、适用域、可观测量和尚未解决的问题。\n'.format(row['名称'],row['研究对象'],row['体系边界'],row['来源编号'],row['原作者'],row['原题名'],row['原始链接'],row['年份'],row['核实日期'],row['核实范围'])
        outputs[base / '02_全球路线' / directory / 'README.md'] = text
    outputs[base / '02_全球路线/README.md'] = intro
    outputs[base / '02_全球路线/覆盖矩阵.csv'] = csv_text(['路线编号','研究路线','来源编号','覆盖状态','核实日期','仍需完成'], [[x['编号'],x['名称'],x['来源编号'],x['覆盖状态'],x['核实日期'],'全文精读；最新进展补充；适用域与预测审查'] for x in rows])
    outputs[base / '01_文献来源/文献登记.csv'] = csv_text(['来源编号','原作者','原题名','年份','原始链接','路线编号','核实日期','核实范围'],[[x['来源编号'],x['原作者'],x['原题名'],x['年份'],x['原始链接'],x['编号'],x['核实日期'],x['核实范围']] for x in rows])
    return outputs

def check(root):
    try:
        outputs = views(root)
    except (ValueError, KeyError, OSError) as exc:
        return ['全球研究登记无效: ' + str(exc)]
    return ['全球研究导航需刷新: ' + p.relative_to(root).as_posix() for p, text in outputs.items() if not p.is_file() or p.read_text(encoding='utf-8') != text]

def refresh(root):
    outputs = views(root)
    for path, text in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check','refresh'])
    args = parser.parse_args()
    if args.command == 'refresh': refresh(ROOT)
    errors = check(ROOT)
    for error in errors: print(error)
    print('FAIL' if errors else 'PASS: 全球研究中文导航与登记一致')
    raise SystemExit(bool(errors))
