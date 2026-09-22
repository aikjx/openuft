"""中文默认的国际参与入口、地区机构与开放资源视图。"""
import json
import os
import re
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse


def entry_for(config, language=None):
    """未指定或不支持的语言均返回中文入口，不按访问地区猜测语言。"""
    if config['默认语言'] != 'zh-Hans' or config['回退语言'] != 'zh-Hans' or config['自动按地区切换'] is not False:
        raise ValueError('默认与回退语言必须是简体中文，关闭地区自动切换')
    entries = {}
    for row in config['语言版本']:
        code, path = row['语言代码'], row['入口']
        if code in entries or not path or '\\' in path or ':' in path or PurePosixPath(path).is_absolute() or '..' in PurePosixPath(path).parts:
            raise ValueError('重复语言或无效入口')
        entries[code] = path
    if entries.get('zh-Hans') != 'README.md':
        raise ValueError('中文主入口必须是 README.md')
    return entries.get(language, entries[config['回退语言']])


def views(root, data):
    base = root / '05_全球研究'
    config = json.loads((root / '00_项目治理/国际化配置.json').read_text(encoding='utf-8'))
    entry_for(config)
    outputs = {}
    text = '# 语言入口\n\n默认语言：**简体中文**。未指定语言或对应译文不可用时，返回中文。所有语言版本的目录仍使用中文名称。\n\n'
    for row in config['语言版本']:
        target = os.path.relpath(root / entry_for(config, row['语言代码']), base / '03_多语种协作').replace('\\','/')
        text += '- [{}]({})：{}。\n'.format(row['显示名称'],target,row['范围'])
    text += '\n英语与日语提供项目参与摘要，研究正文不自动标为已翻译。原始论文保留原题名、作者及版本。\n'
    outputs[base / '03_多语种协作/语言入口.md'] = text
    outputs[base / '03_多语种协作/英语/项目介绍.md'] = '''# OpenUFT — Global research, Chinese by default

**AI科技星 · [aikjx.com](https://aikjx.com)**

[简体中文（默认）](../../../README.md) · [日本語](../日语/项目介绍.md) · [Language entries](../语言入口.md)

This is an optional English participation summary. The default entry and research directories are Chinese. It is not a translation of the full repository.

OpenUFT organizes independent research modules, external theoretical approaches, reproducible computations and source records. Inclusion is not endorsement or experimental confirmation. Original authors and bibliographic titles are preserved.

The physical research label is “space light-speed helix”; an author's name identifies a bibliographic source, not a separate theory category. See the shared [reference list](../../../02_共享基础/参考资料/BIBLIOGRAPHY.md), including reference ZXQ2024.

Browse [theory routes](../../02_全球路线/README.md), [regional research institutions](../../05_地区与机构/README.md), or [open research resources](../../06_开放资源/README.md). These are public-resource directories, not partnership claims. Most linked local descriptions are Chinese.

Contribute primary-source checks, mathematical reviews, reproducible computations, negative results or translations. Identify the system and assumption revision, record commands and inputs, and separate language review from scientific review. See the [contribution guide](../../../CONTRIBUTING.md).

Translation scope: summary of the Chinese participation guide; editorial draft, awaiting independent language review.
'''
    outputs[base / '03_多语种协作/日语/项目介绍.md'] = '''# OpenUFT — 統一場理論の公開研究

**AI科技星 · [aikjx.com](https://aikjx.com)**

[简体中文](../../../README.md) · [English](../英语/项目介绍.md) · [言語一覧](../语言入口.md)

このページは日本語のプロジェクト概要です。既定の言語と研究用ディレクトリ名は中国語です。研究本文全体の翻訳ではありません。

OpenUFT は、異なる基礎仮定を持つ研究体系を独立して管理します。数学的証明、数値計算、観測との比較を区別し、仮定、導出、コード、データ、反例、論文を追跡できるように整理しています。

体系名には研究対象や仮定を用います。「空間の光速螺旋」は研究上の名称であり、著者名は出典として記載します。資料の収録は、その理論が実験的に確立されたことを意味しません。

[独立した研究体系](../../../01_独立体系/README.md) · [世界の研究アプローチ](../../02_全球路线/README.md) · [参考文献](../../../02_共享基础/参考资料/BIBLIOGRAPHY.md)

原著の確認、数学的検討、再現可能な計算、否定的結果の記録、翻訳を歓迎します。対象の体系と仮定の版を明記し、翻訳の確認と科学的内容の審査を分けてください。[参加案内](../../../CONTRIBUTING.md)を参照してください。

翻訳範囲：中国語の参加案内に基づく要約。独立した日本語校閲は未実施です。
'''
    regions = ['亚洲','欧洲','北美洲','南美洲','非洲','大洋洲']
    intro = '# 地区与研究机构\n\n[全球研究](../README.md) · [全球理论路线](../02_全球路线/README.md)\n\n六个地区的首批研究入口，当前每个地区一条代表性记录，远非机构全集。所有条目均是公开资料收录，不表示已建立合作，也不表示该机构支持本项目候选理论。\n\n| 地区 | 收录机构数 |\n|---|---:|\n'
    for region in regions:
        rows = [x for x in data['地区机构'] if x['地区'] == region]
        intro += '| [{}]({}/README.md) | {} |\n'.format(region,region,len(rows))
        page = '# {}研究入口\n\n[地区总表](../README.md)\n\n'.format(region)
        for row in rows:
            if urlparse(row['来源']).scheme != 'https': raise ValueError('机构来源必须为 HTTPS')
            page += '## {}\n\n- 所在地：{}\n- 研究入口用途：{}\n- [官方来源]({})\n- 核实日期：{}\n- 核实范围：{}\n- 与本项目关系：公开资料收录，未登记合作关系。\n\n'.format(row['机构'],row['所在地'],row['用途'],row['来源'],row['核实日期'],row['核实范围'])
        outputs[base / '05_地区与机构' / region / 'README.md'] = page
    if any(x['地区'] not in regions for x in data['地区机构']): raise ValueError('未定义地区')
    outputs[base / '05_地区与机构/README.md'] = intro
    resources = '# 全球开放资源\n\n[全球研究](../README.md)\n\n以下链接指向公开服务，说明使用中文。尚未下载具体数据或建立本项目镜像；引用与复现应指向具体记录及版本。\n\n'
    seen = set()
    for row in data['开放资源']:
        if row['编号'] in seen: raise ValueError('开放资源编号重复')
        seen.add(row['编号'])
        if any(urlparse(row[key]).scheme != 'https' for key in ['入口','说明来源']): raise ValueError('资源需提供 HTTPS 来源')
        resources += '## {}\n\n{}\n\n[访问入口]({}) · [官方说明]({})\n\n'.format(row['名称'],row['用途'],row['入口'],row['说明来源'])
    outputs[base / '06_开放资源/README.md'] = resources
    return outputs
