"""Preserve V106 issue descriptions; append V107 tasks without overwriting closed/open semantics."""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parent.parent
BASE=Path('/mnt/data/ROOT_V106_单相位无曲率与规范耦合审计_20261120/ledger')
# Independent ZIP runtime must not depend on BASE; CSV copies shipped under input_history/
BASE_LOCAL=ROOT/'ledger'/'input_history'

def generate():
    a=BASE_LOCAL/'ALL_369_AUDITED_BASELINE.csv'
    b=BASE_LOCAL/'V106_15_tasks.csv'
    with a.open(encoding='utf-8-sig',newline='') as f: hist=list(csv.DictReader(f))
    with b.open(encoding='utf-8-sig',newline='') as f: v106=list(csv.DictReader(f))
    tasks=[
        ('U107-01','无右手中微子时超荷比例条件唯一','给出混合/立方异常和Yukawa的完整代数证明','MATH_CONDITIONAL_COMPLETE'),
        ('U107-02','加入右手中微子后的B-L连续歧义','构造连续一参数反例；说明Majorana条件','MATH_CONDITIONAL_COMPLETE'),
        ('U107-03','完整SU5多重态单圈beta贡献相等','Dirac 5+5bar 的三个精确群系数','MATH_CONDITIONAL_COMPLETE'),
        ('U107-04','单组分裂5+5bar的临界质量比','给定测量输入/区间/匹配方案下证明必要不等式','MODEL_CONDITIONAL_NOGO'),
        ('U107-05','两组分裂多重态的一圈交点','独立根查找、阈值次序及高精度残差','MODEL_CONSTRUCTED_NOT_VALIDATED'),
        ('U107-06','匹配能标和质子衰变限制','明确X,Y玻色子质量、寿命、置信区间','OPEN_EMPIRICAL'),
        ('U107-07','完整两圈RGE和规范阈值','有质量谱/ Yukawa 的两圈稳定分析','OPEN_THEORY'),
        ('U107-08','内部相位秩对局部Pontryagin密度的限制','证明k<=3局部tr(F∧F)=0且k=4反例','MATH_CONDITIONAL_COMPLETE'),
        ('U107-09','非零全局二陈数的束拓扑','构造紧致四流形上的正规化联络并算整数拓扑荷','OPEN_TOPOLOGY'),
        ('U107-10','内空间无自由输入推出标准模型全部谱','从独立原理产生群、手征表示、异常抵消','OPEN_FOUNDATIONAL'),
        ('U107-11','第一性独立求G','不得输入G或其派生的Planck尺度，且满足观测','OPEN_FOUNDATIONAL'),
        ('U107-12','产生可证伪的独立实验预测','含实验可行性、误差模型及外部重复观测','OPEN_EMPIRICAL'),
    ]
    rows=[]
    for x in hist:
        rows.append({'canonical_id':x['canonical_id'],'issue':x['issue'],'source':x['source_version'],
                     'prior_status':x['legacy_status'],'evidence_state':x['new_evidence_class'],
                     'acceptance':x['effective_acceptance_criterion'],'note':x['independent_audit_note']})
    for x in v106:
        rows.append({'canonical_id':x['id'],'issue':x['issue'],'source':'V106',
                     'prior_status':x['status'],'evidence_state':'INHERITED_STATUS_NOT_REASSESSED',
                     'acceptance':x['acceptance'],'note':'V106原始研究状态保留'})
    for cid,issue,acceptance,state in tasks:
        rows.append({'canonical_id':cid,'issue':issue,'source':'V107',
                     'prior_status':'NEW','evidence_state':state,'acceptance':acceptance,
                     'note':'条件模型数学完成不等于四力统一；开放项不得关闭'})
    ids=[r['canonical_id'] for r in rows]
    assert len(hist)==369 and len(v106)==15 and len(tasks)==12
    assert len(rows)==396 and len(set(ids))==396,(len(rows),len(set(ids)))
    with (ROOT/'ledger'/'ALL_396_UNIQUE_ISSUES.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
    summary={'V106_baseline':len(hist),'V106_new_tasks':len(v106),'V107_new_tasks':len(tasks),
             'total_unique_canonical_ids':len(set(ids)),'user_goal_full_unification_solved':False}
    (ROOT/'ledger'/'LEDGER_VALIDATION.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return summary

if __name__=='__main__':print(generate())
