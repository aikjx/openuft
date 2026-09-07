# -*- coding: utf-8 -*-
from pathlib import Path
import csv
import hashlib
import json
import os

root = Path(__file__).resolve().parent / 'openuft'
def write(rel, body):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body.rstrip() + '\n', encoding='utf-8')
def replace(rel, old, new):
    p = root / rel
    write(rel, p.read_text(encoding='utf-8').replace(old, new))
replace('.github/PULL_REQUEST_TEMPLATE.md', '../../CONTRIBUTING.md', '../00_governance/CONTRIBUTING.md')
replace('02_shared/references/README.md', '(OPEN_PROBLEMS.md)', '(../protocols/audit_methodology/A4_诚实声明OpenProblems/开放问题清单_L0-L2.md)')
write('00_governance/catalog/README.md', '# 研究目录与历史总表\n\n[当前全量索引](material_catalog.md) · [机器可读清单](structure_manifest.json) · [历史定理谱系](定理谱系总表.md)\n\n在 openuft 根目录执行 `python 00_governance/tools/refresh_catalog.py` 更新当前索引。历史总表和研究报告保留原有主张，科学状态以各模型证据登记和实际审查为准。')
write('00_governance/README.md', '# 项目治理\n\n[全生命周期流程](WORKFLOW.md) · [目录索引](catalog/README.md) · [迁移说明](MIGRATION_GUIDE.md) · [迁移验证](VALIDATION.md) · [贡献约定](CONTRIBUTING.md) · [规划](ROADMAP.md)\n\nlayout.json 是结构校验依据；研究结论由各模型证据登记管理。')
write('02_shared/README.md', '# 共享研究基础\n\n[研究协议](protocols/README.md) · [数学与文献](references/README.md) · [计算工具](computation/README.md)\n\n只共享确实可复用的定义、方法与实现。任何带理论前提的工具须注明适用模型和版本。')
write('00_governance/CONTRIBUTING.md', '# 研究贡献约定\n\n1. 按原始假设选择 01_models 下的模型；归属不明则进入 99_inbox。\n2. 明确 model.json 中的假设版本、定义与适用边界；混合模型显式登记依赖。\n3. 在 claims.csv 登记命题，链接推导、预测、代码、数据、误差和负结果。\n4. 模型专属源码、图表、论文与评审记录放入本模型对应阶段；共享材料仅保留一个主版本。\n5. 提交前运行 `python verify.py`，涉及计算时执行相应复算；目录调整后运行 `python 00_governance/tools/refresh_catalog.py`。\n6. 在评审记录中注明具体审查人、版本、发现和处置；未经审查的历史标签不能作为结论认证。\n\n[详细流程](WORKFLOW.md)')
write('00_governance/ROADMAP.md', '# 后续研究规划\n\n- 已完成：按六条假设路线建立全生命周期布局、迁移快照、路径映射、目录校验和复算入口修复。\n- 待开展：逐模型填写本体、公设、尺度、自由度和负责人；当前未审定字段保持空值。\n- 待审查：历史 GAQ 系列、综合论文与关键词资料关联的真实理论归属。\n- 待验证：逐命题核对证明条件、独立预测、数据独立性、不确定度和负结果。\n- 待发布：按真实审查结果建立论文、复现包与长期保存版本。\n\n以上为研究待办，不预设物理结论成立。')
write('00_governance/FAQ.md', '# 常见问题\n\n## 从哪里进入？\n\n从 [六条理论路线](../01_models/README.md) 进入，与本体假设最接近的路线是主归属。\n\n## 目录齐全是否意味着研究完成？\n\n不是。目录和模板仅代表组织能力；model.json 的空值与未审查状态需要由真实研究填充。\n\n## 跨体系材料放哪里？\n\n共享方法放 02_shared，比较放 03_comparative，综合报告放 04_publications，无法确认的输入放 99_inbox。只设一个主文件，通过链接引用。\n\n## 历史文件能恢复吗？\n\n见 [迁移说明](MIGRATION_GUIDE.md)。迁移前 193 个文件保存在 ZIP 中，并有逐文件 SHA-256；恢复时先解压到独立目录核对。')
write('00_governance/VALIDATION.md', '# 本次目录迁移验证\n\n范围：组织结构、文件保存、链接和运行路径。未进行理论成立性审查。\n\n- 完整快照：193 个迁移前文件，逐文件 SHA-256 校验；包含当时磁盘上的未提交内容。\n- 模型结构：6 条路线及 1 套模板，每套 17 个生命周期目录。\n- 内部 Markdown 文件路径：由根目录 verify.py 自动检查；历史归档保留旧文本，不检查其旧链接。校验不覆盖 Markdown 锚点、外部网址或任意正文内的路径字符串。\n- 实际运行：共享 `triad_uft.verify`、H01 的 D5 与 V2、H04 的 D0 四个入口均退出码 0。\n- 运行环境：本机 Python 3.8.8；现有 numpy、sympy、mpmath 可用。\n\n四个入口运行成功仅表示迁移后能够执行；其中 STRICT / VERIFIED 等标签来自历史代码，不能作为本次科学认证。')
for model in (root / '01_models').iterdir():
    if not model.is_dir(): continue
    meta = json.loads((model / 'model.json').read_text(encoding='utf-8'))
    if model.name in ['h01_space_motion', 'h04_geometry_action']:
        meta['cross_model_dependencies'] = [{'path': '../../02_shared/computation/src/triad_uft', 'role': 'historical reproduction engine; assumptions require review'}]
        write(model.relative_to(root).as_posix() + '/model.json', json.dumps(meta, ensure_ascii=False, indent=2))
    # Preserve the old README verbatim in before.zip; current entry has no unreviewed certification.
    p = model / 'README.md'
    body = p.read_text(encoding='utf-8')
    start = body.find('状态：')
    end = body.find('\n', start)
    if start >= 0: body = body[:start] + '状态：研究资料待审；模型公设与证据登记尚待完善。' + body[end:]
    p.write_text(body, encoding='utf-8')
with (root / '03_comparative/comparison_matrix.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['comparison_id','observable','baseline','model_id','hypothesis_revision','free_parameters','data_ids','prediction','uncertainty','metric','run_id','status'])
    for m in sorted((root / '01_models').glob('h*')): writer.writerow(['','','',m.name,'','','','','','','','not_tested'])
for name in ['restructure_openuft_layout.py', 'finish_openuft_layout.py']:
    src = root.parent / name
    dst = root / '90_archive/migrations/20260907_full_layout' / name
    assert str(src.resolve()).startswith(str(root.parent.resolve()) + os.sep)
    assert str(dst.resolve()).startswith(str(root.resolve()) + os.sep)
    src.rename(dst)
manifest_path = root / '90_archive/migrations/20260907_full_layout/manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
for row in manifest['files']:
    row['sha256_after'] = hashlib.sha256((root / row['new']).read_bytes()).hexdigest()
manifest['after_hash_note'] = 'Hashes recorded during migration; generated catalogs may subsequently refresh. Snapshot before hashes are immutable.'
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print('Finalized navigation, governance and migration records')
