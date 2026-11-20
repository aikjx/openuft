"""One-to-one preserving audit of all 396 ROOT V107 issues.
No pre-existing OPEN state is silently marked solved.
"""
from __future__ import annotations
import csv, pathlib, collections, json

INPUT=pathlib.Path(__file__).resolve().parent.parent/'ledger'/'V107_ALL_396_original.csv'
OUTPUT=pathlib.Path(__file__).resolve().parent.parent/'ledger'/'V108_ALL_396_AUDITED.csv'

SPECIAL={
'U107-05':('ONE_LOOP_FIT_NOT_PREDICTION','阈值参数的完整反演存在一维零空间；拟合交点不能代替独立预测','results/mathematical_audit.json'),
'U107-06':('CONDITIONALLY_RULED_OUT_SIMPLE_GUT','若MX=交点且常规dim-6质子衰变未抑制，示范寿命低于观测界；其它GUT形式未排除','results/mathematical_audit.json'),
'U107-09':('BPST_MATH_EXAMPLE_DONE_ROOT_ORIGIN_OPEN','BPST SU2 在S4给非零二陈数示例；螺旋内部相位未独立产生该丛','research/02_证明与反例.md'),
'U107-10':('OPEN_GAUGE_ORIGIN','平坦相位环面平移对称U(1)^k不足以单独推出SU3×SU2×U1','research/02_证明与反例.md'),
'U107-11':('OPEN_G_ORIGIN','单靠c、ħ无法确定G；引入独立曲率尺度仍需动力学确定','research/02_证明与反例.md'),
'U107-12':('OPEN_EMPIRICAL','候选模型必须产生非调参新预测，并给统计、系统误差与独立复现','research/01_总论.md'),
'U107-07':('OPEN_TWO_LOOP_AND_MATCHING','未完成两圈+阈值全量匹配，单圈交点不能视为GUT成功','research/01_总论.md'),
'U107-08':('MATH_CONDITIONAL_COMPLETE','局部四形式秩障碍保留；全局拓扑不能从它直接推出','research/02_证明与反例.md'),
}

def classify(row):
    id=row['canonical_id'];state=row['evidence_state']
    if id in SPECIAL: return SPECIAL[id]
    if state in ('OPEN_RESEARCH','OPEN_FOUNDATIONAL','OPEN_EMPIRICAL','OPEN_THEORY','OPEN_TOPOLOGY'):
        return ('GOAL_OPEN','需要新的独立动力学、完整数学证明或真实测量；不得因相关子定理成立而关闭','ledger/V108_ALL_396_AUDITED.csv')
    if state=='INHERITED_STATUS_NOT_REASSESSED':
        return ('INHERITED_NEEDS_EVIDENCE_AUDIT','继承状态，不臆断V108独立完成','ledger/V108_ALL_396_AUDITED.csv')
    if state=='REQUIRES_REAL_EXPERIMENT':
        return ('EXPERIMENT_REQUIRED','必须有仪器定义、真实数据、置信区间及独立复现','ledger/V108_ALL_396_AUDITED.csv')
    if state=='DIAGNOSTIC_CLOSED_GOAL_OPEN':
        return ('DIAGNOSTIC_CLOSED_GOAL_OPEN','否定错误旧式不等于完成原科学目标','ledger/V108_ALL_396_AUDITED.csv')
    if state in ('CONDITIONAL_RESULT_ONLY','MATH_CONDITIONAL_COMPLETE','CONDITIONAL_THEOREM','MODEL_CONDITIONAL_NOGO'):
        return ('CONDITIONAL_ONLY','数学在声明假设下成立；原高层目标未自动关闭','ledger/V108_ALL_396_AUDITED.csv')
    if state in ('MODEL_OR_SOFTWARE_ONLY','MODEL_CONSTRUCTED_NOT_VALIDATED'):
        return ('MODEL_ONLY','软件测试/模型拟合不可当作实验确认','ledger/V108_ALL_396_AUDITED.csv')
    if state=='KNOWN_BASELINE':return ('KNOWN_BASELINE','已有基准不是ROOT发现的新定律','ledger/V108_ALL_396_AUDITED.csv')
    raise ValueError(f'Unknown original state: {state}')

def build():
    with INPUT.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    assert len(rows)==396
    ids=[r['canonical_id'] for r in rows]
    assert len(set(ids))==len(ids)
    assert all(r['acceptance'].strip() for r in rows)
    columns=list(rows[0])+['v108_status','v108_finding','v108_evidence_path','v108_original_goal_closed']
    for row in rows:
        outcome,note,evidence=classify(row)
        row.update(v108_status=outcome,v108_finding=note,v108_evidence_path=evidence,
                   v108_original_goal_closed='NO' if ('OPEN' in outcome or outcome not in ('KNOWN_BASELINE',)) else 'NOT_A_NEW_GOAL')
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    with OUTPUT.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)
    return {'total':len(rows),'unique_ids':len(set(ids)),
            'v107_evidence_states':dict(sorted(collections.Counter(r['evidence_state'] for r in rows).items())),
            'v108_dispositions':dict(sorted(collections.Counter(r['v108_status'] for r in rows).items())),
            'focused_ids':sorted(SPECIAL),
            'note':'Only some model-level/mathematical subtasks were completed. No claim of 396 solved physics problems.'}
if __name__=='__main__':print(json.dumps(build(),ensure_ascii=False,indent=2))
