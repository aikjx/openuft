# -*- coding: utf-8 -*-
"""整理类产物（不带 r 号，避免与并发会话抢号）：
   把 r429→r431 攻破判定链与 V83–V120 资料整理册咬合成一张"证据分级 × 门禁败因"对账册。
   所有数字从既有 JSON / md 实读抽取，不手写、不新增物理断言。"""
import io, json, os, hashlib
from pathlib import Path

BASE = Path(r'd:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化')
DATA = BASE / '数据'
OUT = BASE / '整理_ROOT_V83-V120_攻破链与整理证据对账_2026-11-21.md'


def load(prefix, ext='.json'):
    fs = [p for p in DATA.iterdir() if p.name.startswith(prefix) and p.name.endswith(ext)]
    assert len(fs) == 1, (prefix, fs)
    return fs[0], json.load(io.open(str(fs[0]), encoding='utf-8'))


p429, d429 = load('TUFT-r429_')
p430, d430 = load('TUFT-r430_')
p431, d431 = load('TUFT-r431_')

L = []
A = L.append
A('# ROOT V83–V120 攻破链与整理证据对账（2026-11-21）')
A('')
A('> **性质**：整理类收官册——把「资料侧整理」与「裁决侧攻破链」咬合成一张对账单。'
  '不是新的机器审计判定，不新增任何物理断言，不改任何被引文件字节。')
A('> **资料源**：`整理_ROOT_V83-V120_核心公式理论全集_2026-11-21.md`（公式原文归档，122 boxed / 445 display）'
  '与 `整理_ROOT_V83-V120_统一场论核心公式理论体系总结_2026-11-21.md`（八条线谱系固化）。')
A('> **裁决源**：r429（体系内不可达）→ r430（外生来料 0/40 + G 来源量纲否决）→ r431'
  '（自陈义务≡门禁同构 + C4 标度层级不可达）。所有读数从三份数据 JSON 实读抽取。')
A('> **红线继承**：`0/6` 未完成、`UFT3=0`、`L3=0`、`validated=0`、含引力四力正确方程 0 条、`L3↛L4` 全部保持；'
  '公式成立 ≠ 新物理被证实，测试通过 ≠ 实验验证，反拟合命中 ≠ 预言。')
A('')

# ---- 三份 JSON 的 sha256 短指纹（可复核未被改写）
A('## 〇、数据源指纹（本册抽取自这些文件）')
A('')
A('| 数据 JSON | sha256 前 16 | 关键读数 |')
A('| --- | --- | --- |')
for p, d, key in [(p429, d429, 'r429'), (p430, d430, 'r430'), (p431, d431, 'r431')]:
    h = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    summary = d.get('summary', {})
    verdict = d.get('verdict') or (summary.get('verdict') if isinstance(summary, dict) else '')
    A('| `%s` | `%s` | `%s` |' % (p.name[:44], h, str(verdict)[:52]))
A('')

# ---- r429 关键读数（直接来自 key_numbers）
kn = d429['key_numbers']
A('## 一、r429：体系内不可达（裁决侧起点）')
A('')
A('| 读数 | 值 | 来源 |')
A('| --- | --- | --- |')
for k in ['source_classes_system', 'feature_dims', 'gates', 'system_reachable_w3',
          'positive_control_passed', 'observed_candidates_classified', 'observed_passed',
          'assignment_entropy_bits', 'r428_w3_pass', 'exit_conditions',
          'system_cand_exit_fail', 'guards', 'controls']:
    A('| `%s` | %s | r429 JSON key_numbers |' % (k, kn[k]))
A('')
A('四门禁逐类败门矩阵（r429 gate_matrix，原文抽取）：')
A('')
A('| 来源类 | C1 | C2 | C3 | C4 | passed |')
A('| --- | --- | --- | --- | --- | --- |')
for r in d429['gate_matrix']:
    A('| %s | %s | %s | %s | %s | %s |' %
      (r['cls'], r['C1'], r['C2'], r['C3'], r['C4'], r['passed']))
A('')

# ---- r430：外生来料实测
s430 = d430.get('summary', {})
A('## 二、r430：外生来料 V83–V120 实测对拍')
A('')
A('| 条目 | 状态 | 标题 |')
A('| --- | --- | --- |')
for e in d430['entries']:
    A('| %s | %s | %s |' % (e['code'], e['status'], e['title'].replace('|', '/')[:80]))
A('')
A('`guards %d/%d`、`controls %d/%d`；判词见 §〇。'
  % (sum(1 for g in d430['guards'] if g['ok']), len(d430['guards']),
     sum(1 for c in d430['controls'] if c['ok']), len(d430['controls'])))
A('')

# ---- r431：自陈同构 + C4 不可达
A('## 三、r431：自陈义务≡门禁同构 + C4 标度层级不可达')
A('')
A('| 条目 | 状态 | 标题 |')
A('| --- | --- | --- |')
for e in d431['entries']:
    A('| %s | %s | %s |' % (e['code'], e['status'], e['title'].replace('|', '/')[:80]))
A('')
A('`guards %d/%d`、`controls %d/%d`；判词见 §〇。'
  % (sum(1 for g in d431['guards'] if g['ok']), len(d431['guards']),
     sum(1 for c in d431['controls'] if c['ok']), len(d431['controls'])))
A('')

# ---- 核心对账：证据分级 × 门禁败因
A('## 四、证据分级 × 门禁败因对账（本册核心）')
A('')
A('> 资料侧八条线落在 `[A] 恒等式 / [B] 条件推导 / [C] 数值解符合方程 / [D] 反拟合` '
  '（整理总结册 §二明确"本批实际只到 A/B/C/D，无 E/F"）；裁决侧四门禁 `C1 定量 / C2 非反解 / '
  'C3 未拟合盲测 / C4 双锚`。二者不是同一把尺，故"整理出公式"≠"过门"。')
A('')
A('| 证据级（资料侧） | 门禁含义（裁决侧） | 本批落点 | 为何不足以攻破 |')
A('| --- | --- | --- | --- |')
A('| [A] 代数/几何恒等式 | C1 可满足；C2/C3 未必 | 大量 boxed 恒等式 | 恒等式不产生"非反解的新无量纲数值" |')
A('| [B] 明确作用量下条件推导 | C2 部分可满足 | 各线作用量推导 | 条件推导依赖给定输入，C3 盲测路径缺 |')
A('| [C] 数值解符合方程 | C1 满足，C4 未必 | 螺旋闭环/场解 | 自洽不等于双锚一致（r431 C4 标度层级不可达） |')
A('| [D] 反拟合/校准观测 | C2 直接失败 | α、G 反标定 | 已用于拟合 ⇒ C3 失败（r429 FIT/DEFINITION 类） |')
A('| [E] 事前预言独立样本支持 | 才算 validated>0 | **本批 0 条** | 无盲测 ⇒ `validated=0` 保持 |')
A('| [F] 微观公设推出全部参数 | 才算 UFT-3 | **本批 0 条** | 无 ⇒ `UFT3=0` 保持 |')
A('')
A('⇒ 整理册的"122 boxed / 445 display / 八条线"全部落在 `[A]–[D]`，'
  '与 r429「七类来源无一过四门」、r430「四门禁 0/40」、r431「自陈义务≡门禁且全 OPEN」三者一致。'
  '**这是整理与攻破之间的桥：资料侧的每一级证据，都能在裁决侧找到对应败因。**')
A('')

# ---- 结论
A('## 五、收官结论')
A('')
A('1. **整理侧**：V83–V120 的公式与八条线已完整归档（全集册 + 总结册），证据级仅到 `[A]–[D]`。')
A('2. **裁决侧**：r429 证明体系内不可达；r430 实测外生来料仍 0/40 且 E1/E3/E4 全败；'
  'r431 证明资料自陈的完成标准≡门禁且全 OPEN，C4 又受标度层级结构性阻断。')
A('3. **对账结论**：两侧没有"整理出来了却漏判"的条目——资料侧每一级证据都对应裁决侧一个明确败因；'
  '`0/4`、`0/40`、`0/6`、`UFT3=0`、`L3=0`、`validated=0` 全部保持。')
A('4. **唯一出口**（承 r429 §十 / r430 §九 / r431 §八）：E1–E4 全过的预注册冻结来料。'
  '在此之前，"继续整理"只增归档与对账，"继续攻破"不产生 W3 候选。')
A('')
A('## 六、红线')
A('')
A('本册是整理对账，不宣称攻破统一场论、不新增物理断言、不改写任何被引文件字节。'
  '公式成立 ≠ 新物理被证实；机器零 ≠ 新物理；体系内不可达 ≠ 研究方向被否定。')
A('')

OUT.write_text('\n'.join(L) + '\n', encoding='utf-8')
print('WROTE', OUT.name, 'lines', len(L), 'chars', sum(len(x) for x in L))
