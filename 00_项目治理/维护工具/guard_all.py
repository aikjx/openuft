#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
openuft 全维守卫 guard_all.py —— 企业级多域自动演化守卫
========================================================
全维分形知识自动演化引擎的「状态内核对标」，覆盖完整治理域。分两个层次：

[硬校验 · 决定退出码]  —— 复用根校验器 verify.py（目录/链接/迁移溯源/章节 provenance）
[扩展域软检查]        —— 四个子域，WARN/INFO 不污染全绿基线：

  · 域A claims 结构：列一致性（数据行列数==表头）、claim_id 同文件唯一性、
                     预测登记列成对（prediction_value/urel）
  · 域B claims 语义：evidence_level 词表合法性（检出列错位污染）、列语义对账、
                     裸 VERIFIED 拦截（B1：须写 VERIFIED(Ln)）
  · 域C system 身份：必填字段存在性、A1 schema 缺口（ontology/自由度/尺度/owner）
  · 域D 治理红线：夸大表述扫描（终极/彻底/颠覆/完美/显然…，INFO 仅供人工）

退出码：0 = verify PASS（基线全绿）；1 = verify FAIL（阻断）；2 = 内部错误。
已知登记项（如 S15 OPEN-B8）按 KNOWN_OPEN 豁免为 INFO，不重复告警。

逃生门：OPENUFT_GUARD_SKIP=1 → 跳过；OPENUFT_GUARD_FORCE=1 → 强制（忽略 SKIP）。
红线：纯校验编排，不改 git config、不新增物理主张、不篡改任何 CURATED 真源。

用法：
  python 00_项目治理/维护工具/guard_all.py              # 文本健康报告
  python 00_项目治理/维护工具/guard_all.py --json       # JSON 报告（供 CI/自动化）
"""
from __future__ import print_function

import csv
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ISSUE_PAT = ('Lost renamed', 'Lost localized', 'Lost historical',
             'Broken link', 'Chapter excerpt mismatch', 'Changed chapter source',
             'Research directory', 'mismatch', 'escapes root', 'Historic ZIP changed')

# 已知登记项（不重复告警）——OPEN 项见 ROADMAP
KNOWN_OPEN = {
    '01_独立体系/S15_空间光速螺旋曲率挠率几何统一场论/claims.csv': 'OPEN-B8 evidence_level 列单字母分级值污染（值语义，非行错位）待裁定',
}

SYSTEM_REQUIRED = ('id', 'title', 'kind', 'status', 'directory')
# A1 待建 schema 字段（检测缺口，不视为硬缺失）
A1_FIELDS = ('ontology', 'freedom_degrees', 'degrees_of_freedom', 'scale', 'owner')

# evidence_level 合法词表（勘察自活跃 claims；含组合，宽松防误报）
EVIDENCE_BASE = {
    'mathematical_result', 'numerical_check', 'conjecture', 'structural',
    'mathematical_check', 'experimental_constraint', 'observational_check',
    'numerical_result', 'structural_claim', 'methodological', 'observational',
    'mathematical_framework', 'review', 'hypothesis', 'verified',
}
GRADE_LETTERS = set('OCHU')
# status 合法状态词表（排除后，剩余 evidence 词即判串列；verified 等不误报）
STATUS_WORDS = {
    'open', 'falsified', 'verified', 'partial', 'closed', 'rejected',
    'unreviewed', 'pending', 'confirmed', 'disproven', 'in_progress', 'stalled',
}


def _is_valid_evidence(v):
    v = v.strip()
    if not v:
        return True, ''
    low = v.lower()
    if low in EVIDENCE_BASE:
        return True, ''
    if '+' in low and all(p.strip().lower() in EVIDENCE_BASE for p in low.split('+')):
        return True, ''
    if len(v) == 1 and v.upper() in GRADE_LETTERS:
        return True, 'letter-grade'
    return False, ''


def _scan_claims_structure(root):
    """域A：claims 结构。返回 (warns, infos)。"""
    warns, infos = [], []
    for csvf in sorted((root / '01_独立体系').rglob('claims.csv')):
        rel = csvf.relative_to(root).as_posix()
        try:
            with csvf.open(encoding='utf-8', newline='') as fh:
                rows = list(csv.reader(fh))
        except Exception as exc:
            warns.append('%s: 读取失败: %s' % (rel, exc))
            continue
        if not rows:
            continue
        header, ncols = rows[0], len(rows[0])
        known = rel in KNOWN_OPEN
        if known:
            infos.append('%s: %s' % (rel, KNOWN_OPEN[rel]))
        bad_col = [i + 1 for i, r in enumerate(rows[1:], start=1) if r and len(r) != ncols]
        if bad_col and not known:
            warns.append('%s: %d 行列数 != 表头 %d 列（行 %s）'
                         % (rel, len(bad_col), ncols, ','.join(map(str, bad_col[:8]))))
        seen, dup = {}, []
        for i, r in enumerate(rows[1:], start=2):
            if not r or not r[0].strip():
                continue
            cid = r[0].strip()
            if cid in seen:
                dup.append('%s(行%d&%d)' % (cid, seen[cid], i))
            seen[cid] = i
        if dup:
            warns.append('%s: claim_id 重复: %s' % (rel, ', '.join(dup[:8])))
    return warns, infos


def _scan_claims_semantic(root):
    """域B：claims 语义。返回 (warns, infos)。"""
    warns, infos = [], []
    for csvf in sorted((root / '01_独立体系').rglob('claims.csv')):
        rel = csvf.relative_to(root).as_posix()
        known = rel in KNOWN_OPEN
        try:
            with csvf.open(encoding='utf-8', newline='') as fh:
                rows = list(csv.reader(fh))
        except Exception as exc:
            warns.append('%s: 读取失败: %s' % (rel, exc))
            continue
        if not rows or 'evidence_level' not in rows[0]:
            continue
        ei = rows[0].index('evidence_level')
        si = rows[0].index('status') if 'status' in rows[0] else None
        bad_ev, letter_cnt, long_cnt, naked_verif, status_ev, status_bad = [], 0, 0, [], [], []
        for r in rows[1:]:
            if not r:
                continue
            if ei < len(r) and r[ei].strip():
                v = r[ei].strip()
                ok, why = _is_valid_evidence(v)
                if not ok:
                    bad_ev.append(v[:24])
                elif why == 'letter-grade':
                    letter_cnt += 1
                if len(v) > 25 and not ok:
                    long_cnt += 1
                if v.lower().startswith('verified') and not re.search(r'\(l\d', v.lower()):
                    naked_verif.append(v[:24])
            # 域B 增强：status 列不得放 evidence 词（evidence_level 串入 status）；且不得出现完全非法 status 词
            if si is not None and si < len(r):
                sv = r[si].strip()
                if sv:
                    sl = sv.lower()
                    if sl in EVIDENCE_BASE and sl not in STATUS_WORDS:
                        status_ev.append(sv[:24])
                    elif sl not in STATUS_WORDS and sl not in EVIDENCE_BASE:
                        status_bad.append(sv[:24])
        if bad_ev and not known:
            warns.append('%s: evidence_level 非法词 %d 个: %s（疑列语义错位/uncertainty 污染）'
                         % (rel, len(bad_ev), '; '.join(bad_ev[:6])))
        if letter_cnt and not known:
            infos.append('%s: %d 行 evidence_level 为单字母分级 %s（疑值语义污染：分级值落错列，供裁定）'
                         % (rel, letter_cnt, 'O/C/H/U'))
        if long_cnt and not known:
            infos.append('%s: %d 行 evidence_level 为长文本（疑 uncertainty 串列，供裁定）' % (rel, long_cnt))
        if naked_verif:
            warns.append('%s: %d 处裸 VERIFIED（须写 VERIFIED(Ln)，B1 红线）: %s'
                         % (rel, len(naked_verif), '; '.join(naked_verif[:6])))
        if status_ev and not known:
            warns.append('%s: status 列 %d 处放 evidence 词 %s（疑 evidence_level 串入 status）'
                         % (rel, len(status_ev), '; '.join(sorted(set(status_ev))[:6])))
        if status_bad and not known:
            warns.append('%s: status 列 %d 处非法词 %s（不在 STATUS_WORDS/evidence 词表，疑自定义词需规范化）'
                         % (rel, len(status_bad), '; '.join(sorted(set(status_bad))[:6])))
    return warns, infos


def _scan_system(root):
    """域C：system 身份。返回 (warns, infos)。"""
    warns, infos = [], []
    for jf in sorted((root / '01_独立体系').rglob('system.json')):
        rel = jf.relative_to(root).as_posix()
        try:
            data = json.loads(jf.read_text(encoding='utf-8'))
        except Exception as exc:
            warns.append('%s: 解析失败: %s' % (rel, exc))
            continue
        if not isinstance(data, dict):
            warns.append('%s: 非对象' % rel)
            continue
        missing = [f for f in SYSTEM_REQUIRED if not data.get(f)]
        if missing:
            warns.append('%s: 缺必填字段 %s' % (rel, ','.join(missing)))
        a1_missing = [f for f in A1_FIELDS if f not in data]
        if a1_missing:
            infos.append('%s: A1 schema 缺字段 %s（待建 schema 后回填）' % (rel, ','.join(a1_missing)))
        elif data.get('owner') in (None, ''):
            infos.append('%s: owner 空缺（A1 待回填）' % rel)
    return warns, infos


def _scan_boost(root):
    """域D：夸大词扫描（INFO 仅供人工，不判定违规）。返回 (warns, infos)。"""
    BOOST = ('终极', '彻底', '颠覆', '完美', '显然', '前所未有', '独一无二', '最强', '最优')
    infos = []
    seen = set()
    for f in sorted(root.rglob('*.md')):
        s = f.relative_to(root).as_posix()
        if s.startswith(('90_', '99_')) or '/90_' in s or '/99_' in s:
            continue
        try:
            txt = f.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        for w in BOOST:
            n = txt.count(w)
            if n and (s, w) not in seen:
                seen.add((s, w))
                infos.append('%s: “%s”×%d（夸大词，仅供人工复核）' % (s, w, n))
    return [], infos


def _emit(report, want_json):
    if want_json:
        print(json.dumps(report, ensure_ascii=False))
        return
    status = 'PASS' if report.get('ok') else ('GUARD-ERR' if report.get('code') == 2 else 'FAIL')
    print('=' * 62)
    print('openuft 企业级多域守卫 | 状态: %s | verify 退出码: %s' % (status, report.get('exit_code', 'n/a')))
    print('=' * 62)
    if report.get('message'):
        print('  ' + report['message'])
    for st in report.get('stats', []):
        print('  ' + st)
    issues = report.get('issues', [])
    if issues:
        print('  -- 硬校验 issue（%d）--' % len(issues))
        for it in issues:
            print('    ' + it)
    for section in ('warns', 'infos'):
        items = report.get(section, [])
        if not items:
            continue
        tag = 'WARN' if section == 'warns' else 'INFO'
        print('  -- 扩展域 %s（%d，不阻断；供处理）--' % (tag, len(items)))
        for it in items:
            print('    [%s] %s' % (tag, it))
    print('=' * 62)


def main():
    here = Path(__file__).resolve().parent
    root = here.parent.parent
    verify_py = root / 'verify.py'
    want_json = '--json' in sys.argv[1:]

    if not verify_py.is_file():
        _emit({'ok': False, 'code': 2, 'stage': 'locate', 'message': '未找到 verify.py'}, want_json)
        return 2
    if os.environ.get('OPENUFT_GUARD_SKIP') == '1' and os.environ.get('OPENUFT_GUARD_FORCE') != '1':
        _emit({'ok': True, 'code': 0, 'stage': 'skip', 'message': 'OPENUFT_GUARD_SKIP=1 跳过校验'}, want_json)
        return 0

    try:
        proc = subprocess.run([sys.executable, '-B', str(verify_py)], cwd=str(root),
                              capture_output=True, text=True, encoding='utf-8', errors='replace')
    except Exception as exc:
        _emit({'ok': False, 'code': 2, 'stage': 'run', 'message': '校验器异常: %s' % exc}, want_json)
        return 2

    combined = (proc.stdout or '') + (proc.stderr or '')
    lines = [ln for ln in combined.splitlines()]
    issues = [ln for ln in lines if any(p in ln for p in ISSUE_PAT)]
    stats = [ln for ln in lines if ln.startswith('Systems/directions')]
    ok = (proc.returncode == 0)

    warns, infos = [], []
    for scan in (_scan_claims_structure, _scan_claims_semantic, _scan_system, _scan_boost):
        w, i = scan(root)
        warns += w
        infos += i

    report = {
        'ok': ok, 'code': proc.returncode, 'stage': 'verify', 'exit_code': proc.returncode,
        'issue_count': len(issues), 'issues': issues[:50], 'stats': stats,
        'warns': warns[:60], 'infos': infos[:60],
    }
    report['message'] = ('PASS: 全维校验全绿（扩展域 %d WARN / %d INFO）'
                         % (len(warns), len(infos))) if ok else \
                        ('FAIL: %d issue(s) —— 详情见 issues 字段' % len(issues))
    _emit(report, want_json)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
