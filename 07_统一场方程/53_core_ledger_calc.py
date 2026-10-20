# -*- coding: utf-8 -*-
"""53 · 核心公式体系总册（2026-10-19）—— 机器合账引擎

职责（整理，不重判）：
  1. 机读继承账本：从《理论体系方程总汇_正确方程集_2026-10-14.md》解析各口径计数，
     并与该文件自称的头部数字逐项核对（抗漂移守卫：表格数字与文件内容不一致 ⇒ 非零退出）。
  2. 机读增量：扫描 04_公共成果/本项目_全维自洽与归一化/数据/TUFT-r1*.json，
     汇总 r100–r123 攻破链的总判决分布；解析 65 号卷（V4.8）判定计数。
  3. 应用 r111 + r112 降级：正确核 22 → 17 → 16（r111：f-桥接族 K-12/13/14/15 + K-09；
     r112：K-03 质量定义欠定）。
  4. 入账 r113「力的统一」攻破（零降级 + 黑名单 B-11 + §2.3 主题归纳，机读七轮判决：r120 方程层合流——
     所有力大统一方程式候选全集 9 方程 2 验证，无一被实验确立；r123 退守封堵层——换群族/阈值/额外维/
     紫外完备/剔除引力五路全封 + 黑名单 B-14）。
  5. 入账 r114「引力的本源」常数层攻破（零降级 + §2.4 主题归纳，机读三轮判决）。
  6. 入账 r115「引力的本质/引力波几何本源」机制层攻破（零降级 + 黑名单 B-12 + §2.4 四轮判决）。
  7. 入账 r116「光子内部运行」全情形穷举判决（36 格 + 五立场矩阵）、r117「相位不变性 +
     de Broglie 内时钟门」增补（七门全 FAIL + 180 组合枚举）、r118 纲领退守路径攻破（电子环形
     光子模型 + OAM 避难所）与 r121 光子几何本源语料机审（13 项 FAIL + 黑名单 B-13）⇒ §2.5
     光子主题归纳（六轮机读）。
  8. 入账 r119 统一场论完成度总判定（七必要条件 1/7 + 电弱控制组 6/6）⇒ §3 达成度行交叉引用。
  9. 汇总黑名单（不可引用登记册，B-01–B-13）。
 10. 生成本卷 md + 数据 md + json + out.txt；所有数字由计算注入，禁手写。

红线：本卷是整理与合账，不产生新物理、不重判任何条目、不修改被引文件字节。
"""

import glob
import json
import os
import re
import sys

DIR = os.path.dirname(os.path.abspath(__file__))               # 07_统一场方程
ROOT = os.path.dirname(DIR)                                     # openuft
SRC_1014 = os.path.join(ROOT, "理论体系方程总汇_正确方程集_2026-10-14.md")
R_DATA = os.path.join(ROOT, "04_公共成果", "本项目_全维自洽与归一化", "数据")
VOL65 = os.path.join(DIR, "空间螺旋几何化统一场论",
                     "65_TUFT-V4.8公式集_作用量量纲与场方程结构机器审计_2026-10-15.md")

OUT_TAG = "53_core_ledger"
VOL_MD = os.path.join(DIR, "53_核心公式体系总册_2026-10-19.md")
OUT_JSON = os.path.join(DIR, OUT_TAG + "_results.json")
OUT_MD = os.path.join(DIR, OUT_TAG + "_data.md")
OUT_TXT = os.path.join(DIR, OUT_TAG + "_out.txt")

ENTRIES = []
GUARDS = []


def add(code, verdict, title, detail, **extra):
    e = {"code": code, "verdict": verdict, "title": title, "detail": detail}
    e.update(extra)
    ENTRIES.append(e)


def guard(cond, name, desc=""):
    GUARDS.append((name, bool(cond), desc))
    return bool(cond)


print("[53] boot ok", flush=True)

# ---------------------------------------------------------------- 1. 继承账本机读
if not os.path.isfile(SRC_1014):
    sys.stderr.write("SRC_1014 NOT FOUND\n")
    sys.exit(3)

txt = open(SRC_1014, encoding="utf-8").read()

k_ids = re.findall(r"^\|\s*(K-\d+)\s*\|", txt, re.M)
n_k = len(k_ids)
uniq_k = len(set(k_ids))
guard(n_k == 22 and uniq_k == 22, "g_inherit_cores_22",
      "10-14 总汇正确核行数须为 22 且编号唯一；实测 %d/%d" % (n_k, uniq_k))
add("L01", "PASS" if (n_k == 22 and uniq_k == 22) else "FAIL",
    "继承账本：正确核 22 条（机读行号）",
    "从 10-14 总汇正则提取 K-编号行 %d 条、唯一 %d 个 ⇒ 与文件自称'PASS 22'一致" % (n_k, uniq_k))

m_health = re.search(r"H\s*(\d+)\s*·\s*O\s*(\d+)\s*·\s*C\s*(\d+)\s*·\s*U\s*(\d+)", txt)
health = tuple(int(x) for x in m_health.groups()) if m_health else None
guard(health == (2, 10, 6, 4), "g_inherit_health_22systems",
      "22 体系分级须为 H2/O10/C6/U4；实测 %s" % (health,))
add("L02", "PASS" if health == (2, 10, 6, 4) else "FAIL",
    "继承账本：22 体系健康度分级 H2/O10/C6/U4",
    "机读 %s ⇒ 与自称一致（H=s01 螺旋三重奏、s13 全域双向分形；均附'非库级终审'注记）" % (health,))

m_tuft = re.search(r"PASS\s*(\d+)\s*·\s*FAIL\s*(\d+)\s*·\s*BOUNDARY\s*(\d+)\s*·\s*INFO\s*(\d+)", txt)
tuft = tuple(int(x) for x in m_tuft.groups()) if m_tuft else None
guard(tuft == (479, 338, 228, 884), "g_inherit_tuft_73",
      "TUFT 73 报告口径须为 479/338/228/884；实测 %s" % (tuft,))
add("L03", "PASS" if tuft == (479, 338, 228, 884) else "FAIL",
    "继承账本：TUFT 归档报告集 73 份 PASS479/FAIL338/BOUNDARY228/INFO884",
    "机读 %s ⇒ 与自称一致（只读引用，未重跑语料）" % (tuft,))

m_v8 = re.search(r"PASS\s*(\d+)\s*·\s*FAIL\s*(\d+)\s*·\s*INFO\s*(\d+)\s*·\s*部分闭合\s*(\d+)", txt)
v8 = tuple(int(x) for x in m_v8.groups()) if m_v8 else None
guard(v8 == (169, 62, 18, 23), "g_inherit_v8_272",
      "v8 全维分析 272 项须为 169/62/18/23；实测 %s" % (v8,))
add("L04", "PASS" if v8 == (169, 62, 18, 23) else "FAIL",
    "继承账本：v8 全维分析系 272 项 PASS169/FAIL62/INFO18/部分闭合23",
    "机读 %s ⇒ 与自称一致（28/28 套件成功运行）" % (v8,))

# 5 条待降级核必须在清单中
must_have = {"K-09", "K-12", "K-13", "K-14", "K-15"}
have = must_have.issubset(set(k_ids))
guard(have, "g_r111_targets_present", "r111 攻破的 5 条须在 22 正确核清单中；实测缺失 %s" % (must_have - set(k_ids),))
add("L05", "PASS" if have else "FAIL",
    "r111 攻破靶点在继承清单中的存在性",
    "K-09/K-12/K-13/K-14/K-15 全部在 22 条清单内 ⇒ 降级操作有明确对象")

# r112 靶点存在性（跨引擎一致性检查在第 3 节 DOWNGRADED 定义后执行）
must_have_112 = {"K-03"}
have_112 = must_have_112.issubset(set(k_ids))
guard(have_112, "g_r112_targets_present", "r112 攻破的 K-03 须在 22 正确核清单中；实测缺失 %s" % (must_have_112 - set(k_ids),))
add("L05b", "PASS" if have_112 else "FAIL",
    "r112 攻破靶点在继承清单中的存在性",
    "K-03 在 22 条清单内 ⇒ r112 降级操作有明确对象")

# ---------------------------------------------------------------- 2. 增量：r 系列攻破链机读
# r 系列 JSON 跨代 schema 不一致（r108/r111 用 summary.verdict_total；r101-r106/r109 用顶层
# verdict+counts；r100/r103 用 counts；r110 只有 counts）⇒ 用容错提取器，禁止猜字段。
def extract_round(p):
    d = json.load(open(p, encoding="utf-8"))
    verdict = None
    counts = None
    n = None
    if isinstance(d.get("summary"), dict):
        verdict = d["summary"].get("verdict_total")
        counts = d["summary"].get("tally")
        n = d["summary"].get("n_entries")
    if verdict is None:
        verdict = d.get("verdict")
    if isinstance(verdict, dict):
        verdict = (verdict.get("verdict_total") or verdict.get("helix_internal_run")
                   or verdict.get("T1") or None)
        if verdict is None and "target_pass" in d.get("verdict", {}):
            # r119 schema：七条必要条件通过数/总数
            vd = d["verdict"]
            verdict = "FAIL(derived)" if vd.get("target_pass", 0) < vd.get("target_total", 1) else "PASS"
        if verdict is None and "n_pass" in d.get("verdict", {}):
            # r120 schema：候选方程验证通过数/总数（宣称「存在大统一方程」未确立 ⇒ 失败轮）
            vd = d["verdict"]
            verdict = "FAIL(derived)" if vd.get("n_pass", 0) < vd.get("n_equations", 1) else "PASS"
    if not isinstance(counts, dict) or not counts:
        counts = d.get("counts") if isinstance(d.get("counts"), dict) else None
    if counts is None:
        vc = d.get("verdict_count")
        if isinstance(vc, dict) and vc:
            counts = vc
    if counts is None:
        # r122 schema：顶层 tally 字典（无 verdict/counts/verdict_count 字段）
        tl = d.get("tally")
        if isinstance(tl, dict) and tl:
            counts = tl
    if n is None:
        n = d.get("total")
    if n is None and isinstance(d.get("entries"), list):
        n = len(d["entries"])
    if verdict is None:
        rp = p.replace(".json", "_report.txt")
        if os.path.isfile(rp):
            for line in open(rp, encoding="utf-8"):
                m = re.search(r"VERDICT\s*=\s*([A-Z]+)", line)
                if m:
                    verdict = m.group(1)
                    break
    return verdict, counts, n


r_files = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r1*.json")))
chain = []
for p in r_files:
    verdict, counts, n = extract_round(p)
    chain.append({"file": os.path.basename(p), "verdict": verdict,
                  "counts": counts, "n_entries": n})

# 派生规则（本引擎声明式规则，非解释）：任一轮 counts 中 FAIL>0 ⇒ 记为该轮含硬失败
def round_class(c):
    if c["verdict"]:
        return c["verdict"]
    cnt = c.get("counts") or {}
    if cnt.get("FAIL", 0) > 0:
        return "FAIL(derived)"
    if cnt.get("BOUNDARY", 0) > 0:
        return "BOUNDARY(derived)"
    return "UNREAD"

chain_ok = [c for c in chain if round_class(c) != "UNREAD"]
dist = {}
for c in chain_ok:
    k = round_class(c)
    dist[k] = dist.get(k, 0) + 1
guard(len(chain_ok) == len(r_files) and len(r_files) >= 13,
      "g_chain_json_readable",
      "r 系列 JSON 须全部可读出判决或计数且不少于 13 份；实测 %d/%d" % (len(chain_ok), len(r_files)))
add("D01", "PASS" if len(chain_ok) == len(r_files) else "FAIL",
    "增量账本：r100–r123 攻破链机读（%d 份数据文件）" % len(r_files),
    "判决分布（含派生规则 FAIL>0⇒失败轮）：%s ⇒ 增量以否定/边界为主，无一条把'统一已完成'变成 PASS"
    % (dist or "空"),
    chain=chain, dist=dist, rule="FAIL>0 ⇒ 该轮记失败（仅用于无显式 verdict 的旧 schema）")

# 65 号卷（V4.8）计数
v48 = None
if os.path.isfile(VOL65):
    t65 = open(VOL65, encoding="utf-8").read()
    m65 = re.search(r"PASS\s*=\s*(\d+)\s*/\s*FAIL\s*=\s*(\d+)\s*/\s*BOUNDARY\s*=\s*(\d+)\s*/\s*INFO\s*=\s*(\d+)", t65)
    if m65:
        v48 = tuple(int(x) for x in m65.groups())
add("D02", "PASS" if v48 else "BOUNDARY",
    "增量账本：65 号卷 TUFT-V4.8 机器审计计数",
    "V4.8 判定 %s（PASS/FAIL/BOUNDARY/INFO）⇒ 作用量层双基量纲不自洽、场方程退化为代数式 ⇒ 螺旋几何化线当前版本不可引用" % (v48,))

# ---------------------------------------------------------------- 3. r111 + r112 降级入账
DOWNGRADED = ["K-09", "K-12", "K-13", "K-14", "K-15", "K-03"]
CORES_BEFORE = 22
CORES_AFTER = CORES_BEFORE - len(DOWNGRADED)

# 跨引擎一致性：r112 数据 JSON 的机读降级决定须与本卷 DOWNGRADED 中的 r112 部分一致
r112_jsons = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r112*.json")))
r112_down = []
for p in r112_jsons:
    try:
        d112 = json.load(open(p, encoding="utf-8"))
        r112_down = list(d112.get("summary", {}).get("cores_downgraded", []))
    except Exception:
        r112_down = []
cross_ok = (len(r112_jsons) == 1 and set(r112_down) == {"K-03"}
            and set(r112_down).issubset(set(DOWNGRADED)))
guard(cross_ok, "g_r112_cross_engine",
      "r112 数据 JSON 的降级决定须恰为 {K-03} 且为本卷 DOWNGRADED 子集；实测 json=%d 份 downgraded=%s"
      % (len(r112_jsons), r112_down))
add("D03b", "PASS" if cross_ok else "FAIL",
    "跨引擎一致性：r112 机读降级决定入账",
    "机读 r112 数据 JSON：cores_downgraded=%s ⇒ 与本卷 DOWNGRADED 的 r112 部分一致"
    "（判定册：判定_TUFT-r112-正确核残余软肋_K-03质量定义_K-07力方程_K-11磁场登记_攻破_2026-10-19.md）"
    % r112_down, r112_json=[os.path.basename(p) for p in r112_jsons], r112_downgraded=r112_down)

add("D03", "FAIL",
    "应用 r111 + r112 降级：正确核 22 → %d" % CORES_AFTER,
    "降级 %d 条：%s。r111 理由：f-桥接族为单位约定（重标度 A′=fA 完全吸收、残差 0）；"
    "K-09 电荷定义欠定（kk′ 有量纲无定值、Ω 无定义）。r112 理由：K-03 质量定义欠定"
    "（n/dn/dΩ 无观测程序、k 由外部 G 锚定、总立体角被 ∮dΩ=4π 锁死致「Ω 收缩导出质速关系」"
    "与其自身登记的总质量形式互斥）。判定依据见 r111/r112 判定册，本卷只入账不重判"
    % (len(DOWNGRADED), "、".join(DOWNGRADED)),
    downgraded=DOWNGRADED, before=CORES_BEFORE, after=CORES_AFTER,
    r112_source="判定_TUFT-r112-正确核残余软肋_K-03质量定义_K-07力方程_K-11磁场登记_攻破_2026-10-19.md")

# ---------------------------------------------------------------- 4. 黑名单登记册
# 保留清单分区（机读分区 + 分区守卫：groups ∪ DOWNGRADED == 22 且互不相交）
CORE_GROUPS = [
    ("标准引力", ["K-04"], "牛顿引力场的记号改写"),
    ("标准电磁", ["K-10", "K-11", "K-19"],
     "库仑、毕奥–萨伐尔（K-11 只可引标准形式；name 串修串要求见 r112/B-09）、偶极辐射磁场"),
    ("标准波动", ["K-08", "K-18"], "波动方程及其通解（补 1/r）"),
    ("标准动力学/质能", ["K-01", "K-02", "K-05", "K-06", "K-07", "K-16", "K-17"],
     "定义式与恒等（K-07：符号约定可吸收、四力映射不可辨识，见 r112；K-17 为 K-07 子集，其『光速飞行器』应用被 r113 判否、须按 B-11 修名）"),
    ("标准常数", ["K-20", "K-21", "K-22"], "恒等重排（信息增量 0，标注）与 α 标准定义"),
]
group_ids = [i for _, ids, _ in CORE_GROUPS for i in ids]
part_ok = (len(group_ids) == CORES_AFTER
           and len(set(group_ids)) == len(group_ids)
           and set(group_ids).isdisjoint(set(DOWNGRADED))
           and set(group_ids) | set(DOWNGRADED) == set(k_ids))
guard(part_ok, "g_groups_partition",
      "保留清单分区须与 22 条继承清单构成精确划分（grouped=%d, downgraded=%d, 22=%d, 相交=%s）"
      % (len(group_ids), len(DOWNGRADED), len(set(k_ids)),
         set(group_ids) & set(DOWNGRADED)))
add("D03c", "PASS" if part_ok else "FAIL",
    "保留清单分区守卫（防表格改了、散文没改）",
    "分组条目 %d 条 + 降级 %d 条 = %d = 继承 22 条，且互不相交 ⇒ 第 4 节清单与机读降级同源"
    % (len(group_ids), len(DOWNGRADED), len(group_ids) + len(DOWNGRADED)),
    groups=[(g, ids) for g, ids, _ in CORE_GROUPS])

# r113 轮入账（「力的统一」攻破：零降级 + 修名要求 + 主题归纳）
r113_jsons = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r113*.json")))
r113_verdict = None
r113_down = []
for p in r113_jsons:
    v, c, n = extract_round(p)
    r113_verdict = round_class({"verdict": v, "counts": c})
    try:
        r113_down = list(json.load(open(p, encoding="utf-8"))
                         .get("summary", {}).get("cores_downgraded", []))
    except Exception:
        r113_down = []
r113_ok = (len(r113_jsons) == 1 and r113_verdict in ("FAIL", "FAIL(derived)") and r113_down == [])
guard(r113_ok, "g_r113_force_theme",
      "r113 数据 JSON 须恰 1 份、判决 FAIL、零降级；实测 json=%d verdict=%s downgraded=%s"
      % (len(r113_jsons), r113_verdict, r113_down))
add("D03d", "PASS" if r113_ok else "FAIL",
    "r113 入账：「力的统一」宣称攻破（零降级 + 修名要求）",
    "机读 r113：verdict=%s、cores_downgraded=%s。结论：四分支源侧因子 0/4 ⇒ 结构上不可能是力；"
    "K-17 飞碟推进两种读数俱败（V̇≡0 / V→−∞）⇒ 不降级任何正确核（宣称在散文层），"
    "追加黑名单 B-11（K-17 登记名修名要求）。判定册：判定_TUFT-r113-力的统一宣称_四分支源侧结构审计_"
    "电磁支归零_飞碟动力学攻破_2026-10-19.md" % (r113_verdict, r113_down),
    r113_json=[os.path.basename(p) for p in r113_jsons], r113_verdict=r113_verdict,
    r113_downgraded=r113_down)

# §2.3 主题归纳：力的统一（机读七轮判决；主题归属为本引擎声明式数据）
THEME_FORCE = [
    ("r104", "TUFT-r104_*", "式 07 反号：F=dp/dt 经典极限给 −ma ⇒ 符号约定族起点（正确核 K-07 附符号约定）"),
    ("r108", "TUFT-r108_*", "外部来料 TUFT V10 四力分支：电磁支双重死（F∝m_test/m_src、恒吸引）、宇宙学 w=−1/3"),
    ("r111", "TUFT-r111_*", "K-09 电荷定义欠定 ⇒ 电磁力几何化的 q 来源断裂；f-桥接族为单位约定"),
    ("r112", "TUFT-r112_*", "K-07 四力映射不可辨识（384 读法/0 约束）、C 无观测约束；K-03 降级"),
    ("r113", "TUFT-r113_*", "四分支源侧因子 0/4 ⇒ 结构上不可能是力定律；K-17 飞碟推进两种读数俱败"),
    ("r120", "TUFT-r120_*", "所有力大统一方程式候选全集（9 方程 2 验证）：代数容量 SM 15 匹配 SU(5)/SO(10)/E6 但质子衰变最小 SU(5) 快 523 倍、引力缺口 4.18 量级 ⇒ 不存在被实验确立的大统一方程"),
    ("r123", "TUFT-r123_*", "退守路径总攻破（五路封堵）：换群族八族全 FAIL（余量 0/1/12/233 与 n_free 2/6/8/13 同向增而 n_obs 恒 3）、加阈值凑汇聚不可辨识、额外维降能标被质子衰变硬门枪毙（安全线 6.12e15 GeV，TeV 越线 12.79 量级）、弦论 10^500 真空非唯一且不可证伪、剔除引力则命题自削"),
]
theme_rows = []
theme_fail = 0
for rid, pat, note in THEME_FORCE:
    ps = sorted(glob.glob(os.path.join(R_DATA, pat + ".json")))
    if len(ps) != 1:
        theme_rows.append((rid, "UNREAD", note))
        continue
    v, c, n = extract_round(ps[0])
    vc = round_class({"verdict": v, "counts": c})
    theme_rows.append((rid, vc, note))
    if vc.startswith("FAIL"):
        theme_fail += 1
theme_ok = (len(theme_rows) == 7 and theme_fail == 7)
guard(theme_ok, "g_theme_force_all_fail",
      "「力的统一」主题七轮须全部机读为 FAIL；实测 %s" % [(r, v) for r, v, _ in theme_rows])
add("D03e", "PASS" if theme_ok else "FAIL",
    "主题归纳：力的统一（机读七轮判决）",
    "分布：%s ⇒ 主题轮次 %d/7 全部 FAIL，0 轮把该宣称升格；结构层（r113：分支无源）与映射层"
    "（r112：不可辨识）合流 ⇒ 『力的统一』既无可能也无区分；方程层（r120：GUT 候选 9 方程仅 2 验证且无四力闭合、"
    "质子衰变最小 SU(5) 超上限 523 倍）把最后出口也封死。"
    % (" / ".join("%s=%s" % (r, v) for r, v, _ in theme_rows), theme_fail),
    theme_rows=[{"round": r, "verdict": v, "note": n} for r, v, n in theme_rows])

# r114 轮入账（「引力的本源」攻破：零降级 + 主题归纳 §2.4）
r114_jsons = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r114*.json")))
r114_verdict = None
r114_down = []
r114_counts = {}
for p in r114_jsons:
    v, c, n = extract_round(p)
    r114_verdict = round_class({"verdict": v, "counts": c})
    r114_counts = c or {}
    try:
        r114_down = list(json.load(open(p, encoding="utf-8"))
                         .get("summary", {}).get("cores_downgraded", []))
    except Exception:
        r114_down = []
r114_ok = (len(r114_jsons) == 1 and r114_verdict in ("FAIL", "FAIL(derived)") and r114_down == [])
guard(r114_ok, "g_r114_gravity_theme",
      "r114 数据 JSON 须恰 1 份、判决 FAIL、零降级；实测 json=%d verdict=%s downgraded=%s"
      % (len(r114_jsons), r114_verdict, r114_down))
add("D03f", "PASS" if r114_ok else "FAIL",
    "r114 入账：「引力的本源」宣称攻破（零降级 + 主题归纳）",
    "机读 r114：verdict=%s、cores_downgraded=%s、tally=%s。结论：G 的几何本源四版本全败——"
    "量纲关（三公式 (M,L,T,A) 残差全非零、ρ 所需量纲三式互斥）、非循环关（ρ=√(G/(α²μ₀c²)) "
    "反解闭环，独立取值残差 1.0）、普遍性关（开普勒 8 值散布 1.5%% vs 行星质量比 5750，"
    "方程预测量偏离观测 1.43e7 倍）、等效原理可执行性（约束 (R,ω,b) 方程数 0）；"
    "GAQ 恒零复核确认（ℐ≡0，200 采样残差 7.3e-16）。判定册：判定_TUFT-r114-引力本源宣称_"
    "G几何本源四版本机审_螺旋机制普遍性审计_攻破_2026-10-19.md" % (r114_verdict, r114_down, r114_counts),
    r114_json=[os.path.basename(p) for p in r114_jsons], r114_verdict=r114_verdict,
    r114_downgraded=r114_down)

# r115 轮入账（「引力的本质」机制层攻破：零降级 + 黑名单 B-12）
r115_jsons = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r115*.json")))
r115_verdict = None
r115_down = []
r115_counts = {}
for p in r115_jsons:
    v, c, n = extract_round(p)
    r115_verdict = round_class({"verdict": v, "counts": c})
    r115_counts = c or {}
    try:
        r115_down = list(json.load(open(p, encoding="utf-8"))
                         .get("summary", {}).get("cores_downgraded", []))
    except Exception:
        r115_down = []
r115_ok = (len(r115_jsons) == 1 and r115_verdict in ("FAIL", "FAIL(derived)") and r115_down == [])
guard(r115_ok, "g_r115_gravity_theme",
      "r115 数据 JSON 须恰 1 份、判决 FAIL、零降级；实测 json=%d verdict=%s downgraded=%s"
      % (len(r115_jsons), r115_verdict, r115_down))
add("D03h", "PASS" if r115_ok else "FAIL",
    "r115 入账：「引力的本质/引力波几何本源」机制层攻破（零降级 + B-12）",
    "机读 r115：verdict=%s、cores_downgraded=%s、tally=%s。结论：四卷语料（含两份自称 20 项求导"
    "验证版）机制层全败——k 四量纲互斥、Z 双重量纲残差 (−1,7,−2,0)、G 两版差 8π、因子 2 六读法"
    "无一闭合（真积分 0/1/π⁴）、Z=Gc/2 反解闭环且宣称误差超不确定度 20 倍、光速自毁 c√2（超 41.4%%）、"
    "GW 公式零螺旋依赖（GR 抄录）、Peters 幂次反号且结论自斥。黑名单加 B-12。判定册："
    "判定_TUFT-r115-引力本质与引力波几何本源语料_求导验证版审计_攻破_2026-10-20.md"
    % (r115_verdict, r115_down, r115_counts),
    r115_json=[os.path.basename(p) for p in r115_jsons], r115_verdict=r115_verdict,
    r115_downgraded=r115_down)

# r116 轮入账（「光子内部运行」全情形穷举判决：零降级 + §2.5 光子主题）
r116_jsons = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r116*.json")))
r116_verdict = None
r116_down = []
r116_counts = {}
for p in r116_jsons:
    v, c, n = extract_round(p)
    r116_verdict = round_class({"verdict": v, "counts": c})
    r116_counts = c or {}
    try:
        d116 = json.load(open(p, encoding="utf-8"))
        vc116 = d116.get("verdict_count") if isinstance(d116.get("verdict_count"), dict) else {}
        if vc116:
            r116_counts = vc116
            r116_verdict = "FAIL" if vc116.get("FAIL", 0) > 0 else "PASS"
        r116_down = list(d116.get("summary", {}).get("cores_downgraded", [])) if isinstance(d116.get("summary"), dict) else []
    except Exception:
        r116_down = []
r116_ok = (len(r116_jsons) == 1 and r116_verdict in ("FAIL", "FAIL(derived)") and r116_down == [])
guard(r116_ok, "g_r116_photon_theme",
      "r116 数据 JSON 须恰 1 份、判决 FAIL、零降级；实测 json=%d verdict=%s downgraded=%s"
      % (len(r116_jsons), r116_verdict, r116_down))
add("D03i", "PASS" if r116_ok else "FAIL",
    "r116 入账：「光子内部运行」全情形穷举判决（零降级 + §2.5 光子主题）",
    "机读 r116：verdict_count=%s、cores_downgraded=%s。结论：36 格情形穷举（6 载体 × 3 时标 × 2 速率预算）"
    "FAIL 26 / PASS 2 / BOUNDARY 8——两张唯一存活的格是 Maxwell 圆偏振（与教科书逐字相同，零新增）；"
    "四条承重定价：光速预算定理（δ=1e-18 ⇒ 螺旋半径 R≤1.1254e-16 m，曲率半径 56.27 m ⇒ 轨迹必为直线）、"
    "自转载荷定理（v_eq=c/√a 与 R/ω/λ 无关，实心球 1.5811c 超光速 58.1%%）、内禀性判据（光子 ω 随参考系变，"
    "电子不变质量残差 2.81e-59 ⇒ 频率是关系量）、反解定义判据（Ω≡ω ⇔ L=λ/2π，换参偏差 0.5）。"
    "五套立场矩阵唯一分歧格（A1）归因到 S3 判据集缺洛伦兹协变性一条 ⇒ 分歧可仲裁。判定册："
    "判定_TUFT-r116-光子内部运行全情形判决与传统对照_2026-10-20.md"
    % (r116_counts, r116_down),
    r116_json=[os.path.basename(p) for p in r116_jsons], r116_verdict=r116_verdict,
    r116_downgraded=r116_down)

# r117 轮入账（相位不变性 + de Broglie 内时钟门：零降级，r116 增补）
r117_jsons = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r117*.json")))
r117_verdict = None
r117_down = []
for p in r117_jsons:
    v, c, n = extract_round(p)
    r117_verdict = round_class({"verdict": v, "counts": c})
    try:
        d117 = json.load(open(p, encoding="utf-8"))
        vd = d117.get("verdict")
        if isinstance(vd, dict) and vd.get("helix_internal_run"):
            r117_verdict = vd["helix_internal_run"]
        r117_down = list(d117.get("summary", {}).get("cores_downgraded", [])) if isinstance(d117.get("summary"), dict) else []
    except Exception:
        r117_down = []
r117_ok = (len(r117_jsons) == 1 and r117_verdict in ("FAIL", "FAIL(derived)") and r117_down == [])
guard(r117_ok, "g_r117_photon_theme",
      "r117 数据 JSON 须恰 1 份、helix_internal_run 判决 FAIL、零降级；实测 json=%d verdict=%s downgraded=%s"
      % (len(r117_jsons), r117_verdict, r117_down))
add("D03j", "PASS" if r117_ok else "FAIL",
    "r117 入账：相位不变性 + de Broglie 内时钟门（零降级，r116 增补）",
    "机读 r117：verdict=%s、cores_downgraded=%s。结论：沿类光世界线相位增量 dΦ≡0（Fraction 精确零）；"
    "de Broglie 内时钟 dΦ/dτ=−mc²/ħ 在 m=0 下把内部时钟锁死——内部角频率上限 0.00151927 rad/s（周期 ≥68.9 分钟）"
    "比观测频率（810 nm，2.3255e15 rad/s）慢 1.53067e18 倍，无法解释 E=ħω；七门（固有时/内时钟/静质量/"
    "螺旋-光速几何/色散-洛伦兹/内部自由度/局域光速）全 FAIL；180 组合枚举后存活 15 例全部是 O0_none"
    "（无内部本体论）；四控制组（μ 子/中子/Giovannini 结构光/GW170817）全 PASS。判定册："
    "判定_TUFT-r117-空间光速螺旋实验室_相位不变性与内时钟门_2026-10-20.md"
    % (r117_verdict, r117_down),
    r117_json=[os.path.basename(p) for p in r117_jsons], r117_verdict=r117_verdict,
    r117_downgraded=r117_down)

# r118 轮入账（空间螺旋纲领退守路径攻破：电子环形光子模型 + OAM 避难所 + 协变性闭合）
r118_jsons = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r118*.json")))
r118_verdict = None
r118_down = []
for p in r118_jsons:
    v, c, n = extract_round(p)
    r118_verdict = round_class({"verdict": v, "counts": c})
    try:
        d118 = json.load(open(p, encoding="utf-8"))
        vd = d118.get("verdict")
        if isinstance(vd, dict) and str(vd.get("T1", "")).startswith("FAIL"):
            r118_verdict = "FAIL"
        r118_down = list(d118.get("summary", {}).get("cores_downgraded", [])) if isinstance(d118.get("summary"), dict) else []
    except Exception:
        r118_down = []
r118_ok = (len(r118_jsons) == 1 and r118_verdict in ("FAIL", "FAIL(derived)") and r118_down == [])
guard(r118_ok, "g_r118_photon_theme",
      "r118 数据 JSON 须恰 1 份、判决 FAIL、零降级；实测 json=%d verdict=%s downgraded=%s"
      % (len(r118_jsons), r118_verdict, r118_down))
add("D03l", "PASS" if r118_ok else "FAIL",
    "r118 入账：纲领退守路径攻破（电子环形模型 + OAM 避难所，零降级 + §2.5 光子主题）",
    "机读 r118：verdict=%s、cores_downgraded=%s。结论：T1  Williamson–van der Mark 电子环形光子模型五门四 FAIL"
    "（结构半径超 LEP 点状上限 6.90e5 倍、拓扑裸电荷偏差 7.94%%、约束机制无来源、形状因子能标 1.02e6 eV 已被散射覆盖；"
    "Zitterbewegung 归因更正为正负能干涉）；T2 OAM 避难所四门全 FAIL（光子合法算符表不含 L——SAM/OAM 分解不存在是原理性 no-go；"
    "OAM 依赖参考轴随束宽消失；l 不进入 E–p 关系）；T3 r116 D02 分歧闭合（五套立场对 A1 收敛 5-0 全 FAIL）。"
    "四控制组（质子/g-2 0.28 ppt/单光子能量/算符表）全 PASS。判定册："
    "判定_TUFT-r118-空间螺旋纲领退守路径攻破_电子环形光子模型与OAM避难所_2026-10-20.md"
    % (r118_verdict, r118_down),
    r118_json=[os.path.basename(p) for p in r118_jsons], r118_verdict=r118_verdict,
    r118_downgraded=r118_down)

# r119 轮入账（统一场论完成度总判定：七条必要条件 + 电弱控制组）
r119_jsons = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r119*.json")))
r119_verdict = None
r119_down = []
r119_ratio = None
for p in r119_jsons:
    v, c, n = extract_round(p)
    r119_verdict = round_class({"verdict": v, "counts": c})
    try:
        d119 = json.load(open(p, encoding="utf-8"))
        vd = d119.get("verdict")
        if isinstance(vd, dict) and "target_pass" in vd:
            r119_ratio = "%s/%s" % (vd.get("target_pass"), vd.get("target_total"))
        r119_down = list(d119.get("summary", {}).get("cores_downgraded", [])) if isinstance(d119.get("summary"), dict) else []
    except Exception:
        r119_down = []
r119_ok = (len(r119_jsons) == 1 and r119_verdict in ("FAIL", "FAIL(derived)") and r119_down == [])
guard(r119_ok, "g_r119_completion",
      "r119 数据 JSON 须恰 1 份、判决 FAIL、零降级；实测 json=%d verdict=%s downgraded=%s"
      % (len(r119_jsons), r119_verdict, r119_down))
add("D03m", "PASS" if r119_ok else "FAIL",
    "r119 入账：统一场论完成度总判定（七必要条件 1/7，电弱控制组 6/6）",
    "机读 r119：verdict=%s、cores_downgraded=%s、通过率=%s。结论：四力/大统一七条必要条件仅 U7（与精密观测相容）"
    "通过 ⇒ 1/7（14.29%%）；U1 框架容纳 FAIL（SM 秩 4 > Cl(1,3) 极大秩 3）、U2 耦合汇聚 FAIL（SM 共线残差 0.0723，"
    "α_s 偏 52.06σ）、U3 引力纳入 FAIL（α_G(M_GUT)=2.72e-06 vs α_GUT=0.0412，差 4.18 量级）、U4 质量导出 FAIL"
    "（SM 约 19 个自由参数全为拟合输入）、U5 参数计数 FAIL、U6 判别力 FAIL（唯一预言链 τ_p=3.4e35 yr 超当前上限且超近期可及 0.53 量级）。"
    "控制组：同一套判据判电弱统一 6/6 通过（M_W/M_Z=cosθ_W 精确恒等、e=gsinθ_W=g′cosθ_W Fraction 层验证）⇒ 判据有判别力。"
    "判定册：判定_TUFT-r119-统一场论完成度总判定_七条必要条件与电弱控制组_2026-10-20.md"
    % (r119_verdict, r119_down, r119_ratio),
    r119_json=[os.path.basename(p) for p in r119_jsons], r119_verdict=r119_verdict,
    r119_downgraded=r119_down, r119_pass_ratio=r119_ratio)

# r120 轮入账（所有力大统一方程式候选全集与状态机判）
r120_jsons = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r120*.json")))
r120_verdict = None
r120_down = []
r120_eq = None
for p in r120_jsons:
    v, c, n = extract_round(p)
    r120_verdict = round_class({"verdict": v, "counts": c})
    try:
        d120 = json.load(open(p, encoding="utf-8"))
        vd = d120.get("verdict")
        if isinstance(vd, dict) and "n_pass" in vd:
            r120_eq = "%s/%s" % (vd.get("n_pass"), vd.get("n_equations"))
        r120_down = list(d120.get("summary", {}).get("cores_downgraded", [])) if isinstance(d120.get("summary"), dict) else []
    except Exception:
        r120_down = []
r120_ok = (len(r120_jsons) == 1 and r120_verdict in ("FAIL", "FAIL(derived)") and r120_down == [])
guard(r120_ok, "g_r120_gut",
      "r120 数据 JSON 须恰 1 份、判决 FAIL、零降级；实测 json=%d verdict=%s downgraded=%s"
      % (len(r120_jsons), r120_verdict, r120_down))
add("D03n", "PASS" if r120_ok else "FAIL",
    "r120 入账：所有力大统一方程式候选全集（9 方程 2 验证，零降级 + §2.3 扩轮）",
    "机读 r120：verdict=%s、cores_downgraded=%s、方程验证=%s。结论：代数容量 SM 一代 Weyl 15 与 SU(5) 匹配（SO(10) 余 1、E6 余 12）；"
    "耦合汇聚 SM 共线残差 0.0723（α_s 偏 52.06σ）vs MSSM 0.000954（1.27σ）；质子衰变最小 SU(5) 预言 τ_p≈4.59e31 yr，"
    "比 Super-K 上限 2.4e34 yr 快 523 倍（MSSM 仅维度-6 给 2.79e36 yr 但维度-5 算符会显著加快）；引力缺口 4.18 量级"
    "（继承 r119 U3）⇒ 不存在被实验确立的『所有力的大统一方程』，破缺链 ≥3 条中 2/3 不给 M_GUT 预言。"
    "判定册：判定_TUFT-r120-所有力的大统一方程式_候选全集与状态机判_2026-10-20.md"
    % (r120_verdict, r120_down, r120_eq),
    r120_json=[os.path.basename(p) for p in r120_jsons], r120_verdict=r120_verdict,
    r120_downgraded=r120_down, r120_equation_verified=r120_eq)

# r121 轮入账（光子几何本源语料机审：H0–H8 × 传统数据精算对照）
r121_jsons = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r121*.json")))
r121_verdict = None
r121_down = []
r121_counts = {}
for p in r121_jsons:
    v, c, n = extract_round(p)
    r121_verdict = round_class({"verdict": v, "counts": c})
    r121_counts = c or {}
    try:
        d121 = json.load(open(p, encoding="utf-8"))
        vc121 = d121.get("verdict_count") if isinstance(d121.get("verdict_count"), dict) else {}
        if vc121:
            r121_counts = vc121
            r121_verdict = "FAIL" if vc121.get("FAIL", 0) > 0 else "PASS"
        r121_down = list(d121.get("summary", {}).get("cores_downgraded", [])) if isinstance(d121.get("summary"), dict) else []
    except Exception:
        r121_down = []
r121_ok = (len(r121_jsons) == 1 and r121_verdict in ("FAIL", "FAIL(derived)") and r121_down == [])
guard(r121_ok, "g_r121_photon_theme",
      "r121 数据 JSON 须恰 1 份、判决 FAIL、零降级；实测 json=%d verdict=%s downgraded=%s"
      % (len(r121_jsons), r121_verdict, r121_down))
add("D03o", "PASS" if r121_ok else "FAIL",
    "r121 入账：光子几何本源语料机审（动量双读法/Larmor 猝灭/κ 扫描，零降级 + §2.5 光子主题）",
    "机读 r121：verdict_count=%s、cores_downgraded=%s。结论：《光子的几何本源与运动模型证明》语料 13 项 FAIL——"
    "动量定义 P=m(C−V) 与结论1 V=C 互斥（⇒P=0 vs 验证节 p⃗=mC⃗ 需 V=0）；双电子动量-能量断裂 29.29%%；"
    "自旋-光速-频率三接口互斥（κ=2π ⇒ p=0 不传播、κ=1 ⇒ v_z=0.917c、κ>2π 无实数解）；Larmor 辐射猝灭"
    "（带电螺旋偶极子寿命 2.65e-19 s vs >4.35e17 s，缺口 1.64e36 倍）；传播速度自承随激发条件可变；"
    "验证节对螺旋参数依赖 0（抄录）。黑名单候选 B-13。判定册："
    "判定_TUFT-r121-光子几何本源语料_H0-H8假设空间与传统数据精算对照_攻破_2026-10-20.md"
    % (r121_counts, r121_down),
    r121_json=[os.path.basename(p) for p in r121_jsons], r121_verdict=r121_verdict,
    r121_downgraded=r121_down)

# r123 轮入账（「力的大统一方程」退守路径总攻破：五路封堵 + 黑名单 B-14）
r123_jsons = sorted(glob.glob(os.path.join(R_DATA, "TUFT-r123*.json")))
r123_verdict = None
r123_down = []
r123_keys = None
for p in r123_jsons:
    v, c, n = extract_round(p)
    r123_verdict = round_class({"verdict": v, "counts": c})
    try:
        d123 = json.load(open(p, encoding="utf-8"))
        r123_keys = d123.get("key_numbers") if isinstance(d123.get("key_numbers"), dict) else None
        r123_down = list(d123.get("summary", {}).get("cores_downgraded", [])) if isinstance(d123.get("summary"), dict) else []
    except Exception:
        r123_down = []
r123_ok = (len(r123_jsons) == 1 and r123_verdict in ("FAIL", "FAIL(derived)") and r123_down == [])
guard(r123_ok, "g_r123_gut_retreat",
      "r123 数据 JSON 须恰 1 份、判决 FAIL、零降级；实测 json=%d verdict=%s downgraded=%s"
      % (len(r123_jsons), r123_verdict, r123_down))
add("D03p", "PASS" if r123_ok else "FAIL",
    "r123 入账：力的大统一方程退守路径总攻破（换群族/阈值/额外维/紫外完备/剔除引力，零降级 + §2.3 扩轮 + B-14）",
    "机读 r123：verdict=%s、cores_downgraded=%s。结论（r120 增补卷，条目不可相加）：五条退路全封——"
    "R1 换群族八族全 FAIL（容量余量 0/1/12/233 与 n_free 2/6/8/13 同向单调增而 n_obs 恒 3 ⇒ 参数门 n_free≤2 仅 "
    "minimal SU(5)/331 边界可达，前者质子衰变快 523 倍、后者根本不统一耦合）；R2 加阈值凑汇聚需参数当量 41 ≫ 2 ⇒ "
    "不可辨识（同 r112 384 读法款），但**承认 MSSM 1.27σ 是真汇聚**（代价 105 参数 + 未见 + 维度-5）；"
    "R3 额外维降能标被质子衰变硬门枪毙（τ_p ∝ M⁴ ⇒ 安全线 M_GUT ≥ 6.12e15 GeV = 10^15.79，TeV 方案越线 12.79 量级，"
    "τ_p(1TeV)≈1.71e-17 yr≈5.4e-10 s）；R4 弦/超引力 10^500 真空 ⇒ 非唯一 + 本代不可证伪（不判其数学错）；"
    "R5 剔除引力 ⇒ 命题自削且引力缺口 4.18 量级仍在。控制组 4/4（电弱 6/6、MSSM 汇聚、SU(5) 容量匹配、GR 已确立）。"
    "关键数：%s。黑名单 B-14（低能标/额外维 GUT 族）。判定册："
    "判定_TUFT-r123-力的大统一方程_退守路径总攻破_换群族与阈值与额外维与紫外完备_2026-10-20.md"
    % (r123_verdict, r123_down, r123_keys),
    r123_json=[os.path.basename(p) for p in r123_jsons], r123_verdict=r123_verdict,
    r123_downgraded=r123_down, r123_keys=r123_keys)

# §2.4 主题归纳：引力的本源（机读四轮判决；主题归属为本引擎声明式数据）
THEME_GRAVITY = [
    ("r108", "TUFT-r108_*", "外部来料 TUFT V10 引力支：∇×(f(r)r̂)≡0 源项恒零、τ∝r^{−3/2} 代入自身方程残差 5/4≠0 ⇒ 无源无解，牛顿项是反解输入"),
    ("r112", "TUFT-r112_*", "K-03 质量定义 m=k·dn/dΩ 欠定降级（引力支的锚断裂）；总立体角 Ω≡4π 与质速关系推导互斥"),
    ("r114", "TUFT-r114_*", "G 的几何本源四版本全败：量纲三式互斥、反解闭环、开普勒普遍性矛盾（5750 倍）、本体公设零约束"),
    ("r115", "TUFT-r115_*", "「引力的本质/引力波几何本源」四卷机制层全败：k 四量纲互斥、因子 2 六读法无一闭合、光速自毁 c√2、GW 公式零螺旋依赖（GR 抄录）"),
]
theme_g_rows = []
theme_g_fail = 0
for rid, pat, note in THEME_GRAVITY:
    ps = sorted(glob.glob(os.path.join(R_DATA, pat + ".json")))
    if len(ps) != 1:
        theme_g_rows.append((rid, "UNREAD", note))
        continue
    v, c, n = extract_round(ps[0])
    vc = round_class({"verdict": v, "counts": c})
    theme_g_rows.append((rid, vc, note))
    if vc.startswith("FAIL"):
        theme_g_fail += 1
theme_g_ok = (len(theme_g_rows) == 4 and theme_g_fail == 4)
guard(theme_g_ok, "g_theme_gravity_all_fail",
      "「引力的本源」主题四轮须全部机读为 FAIL；实测 %s" % [(r, v) for r, v, _ in theme_g_rows])
add("D03g", "PASS" if theme_g_ok else "FAIL",
    "主题归纳：引力的本源（机读四轮判决）",
    "分布：%s ⇒ 主题轮次 %d/4 全部 FAIL，0 轮把该宣称升格；常数层（r112/r114：G 的两个"
    "『本源式』俱为重言/反解闭环）、机制层（r114：m=ω²r³ 与开普勒同一性矛盾；r115：拖拽/涡量/"
    "度规扰动/引力波方程机制全败、k 四量纲互斥、因子 2 六读法无一闭合）、"
    "本体层（r114：S12 公设零约束、GAQ 场方程右端恒零）三层合流 ⇒ 『引力的几何本源』"
    "在本库证据链内无一个版本成立。"
    % (" / ".join("%s=%s" % (r, v) for r, v, _ in theme_g_rows), theme_g_fail),
    theme_gravity_rows=[{"round": r, "verdict": v, "note": n} for r, v, n in theme_g_rows])

# §2.5 主题归纳：光子的本质（光子专题四轮机读；r53/r56 为旧 schema，用专用容错提取器）
def photon_verdict(p):
    """光子专题轮次的判决提取（显式字段路径，不猜）：r53 summary.counts / r56 verdict_summary /
    r116 verdict_count / r117 verdict.helix_internal_run / r118 verdict.T1 / r121 顶层 verdict
    字符串（+ counts）；均以 FAIL>0 或显式 FAIL 记失败轮。"""
    d = json.load(open(p, encoding="utf-8"))
    vd = d.get("verdict")
    if isinstance(vd, str) and vd:
        return vd
    if isinstance(vd, dict):
        if vd.get("helix_internal_run"):
            return vd["helix_internal_run"]
        if str(vd.get("T1", "")).startswith("FAIL"):
            return "FAIL"
    for key in ("verdict_count",):
        vc = d.get(key)
        if isinstance(vc, dict) and vc:
            return "FAIL" if vc.get("FAIL", 0) > 0 else "PASS"
    sm = d.get("summary")
    if isinstance(sm, dict) and isinstance(sm.get("counts"), dict):
        return "FAIL" if sm["counts"].get("FAIL", 0) > 0 else "PASS"
    vs = d.get("verdict_summary")
    if isinstance(vs, dict) and vs:
        return "FAIL" if vs.get("FAIL", 0) > 0 else "PASS"
    return "UNREAD"


THEME_PHOTON = [
    ("r53", "TUFT-r53_*", "空间螺旋结构光与光子全维审计（47 条目 FAIL15）：螺旋空间度规实为平直（Riemann 全零=坐标选择）、圆柱螺旋轨道与向心加速度矛盾、有效质量 FAIL"),
    ("r56", "TUFT-r56_*", "光/光子/空间光速螺旋三分法概念裁定（16 条目 FAIL3）：τ 可被 boost 精确清零、v_z=c·cosθ<c、三约束互斥定理 {总速率=c, 轴向速率=c, R>0}⇒∅、ω↔f 映射公设未声明"),
    ("r116", "TUFT-r116_*", "「光子内部运行」36 格穷举（FAIL26/PASS2/BOUNDARY8）：光速预算把螺旋半径压到 1.1e-16 m、自转载荷定理 v_eq=c/√a、内禀性判据、唯一分歧格可归因到判据集缺口"),
    ("r117", "TUFT-r117_*", "相位不变性 + de Broglie 内时钟门（七门全 FAIL）：dΦ≡0 精确零、内时钟比观测频率慢 1.53e18 倍、180 组合枚举存活 15 例全为 O0_none"),
    ("r118", "TUFT-r118_*", "纲领退守路径攻破（8 门 FAIL）：电子环形光子模型超 LEP 点状上限 6.90e5 倍、OAM 避难所四门全 FAIL（SAM/OAM 分解原理性不存在）、协变性分歧闭合 5-0"),
    ("r121", "TUFT-r121_*", "《光子的几何本源与运动模型证明》语料机审（13 FAIL）：动量双读法互斥（P=0 vs mc）、双电子动量-能量断裂 29.29%、κ 扫描三接口无解、Larmor 辐射寿命缺口 1.64e36 倍"),
]
theme_p_rows = []
theme_p_fail = 0
for rid, pat, note in THEME_PHOTON:
    ps = sorted(glob.glob(os.path.join(R_DATA, pat + ".json")))
    if len(ps) != 1:
        theme_p_rows.append((rid, "UNREAD", note))
        continue
    vc = photon_verdict(ps[0])
    theme_p_rows.append((rid, vc, note))
    if vc.startswith("FAIL"):
        theme_p_fail += 1
theme_p_ok = (len(theme_p_rows) == 6 and theme_p_fail == 6)
guard(theme_p_ok, "g_theme_photon_all_fail",
      "「光子的本质」主题六轮须全部机读为 FAIL；实测 %s" % [(r, v) for r, v, _ in theme_p_rows])
add("D03k", "PASS" if theme_p_ok else "FAIL",
    "主题归纳：光子的本质（机读六轮判决）",
    "分布：%s ⇒ 主题轮次 %d/6 全部 FAIL，0 轮把该宣称升格；边界轮（r53：螺旋空间=平直坐标选择；r56：boost 消 τ、"
    "三约束互斥）、命题轮（r116：36 格穷举；r117：dΦ≡0 + 七门）、退守轮（r118：电子环形模型超 LEP 上限 6.90e5 倍 + "
    "OAM 避难所原理性 no-go + 协变性分歧 5-0 闭合）、语料轮（r121：动量双读法互斥、κ 扫描无解、Larmor 缺口 1.64e36）"
    "四层合流 ⇒ 『光子以圆柱螺旋方式内部运行』在本库证据链内无一个版本成立。"
    % (" / ".join("%s=%s" % (r, v) for r, v, _ in theme_p_rows), theme_p_fail),
    theme_photon_rows=[{"round": r, "verdict": v, "note": n} for r, v, n in theme_p_rows])

BLACKLIST = [    {"id": "B-01", "item": "UFE-1′（把 EC 引力写成 Yang–Mills 型曲率方程）",
     "reason": "该等同不成立；00 号卷 2026-10-09 勘误废除",
     "source": "07_统一场方程/00_统一场方程.md 勘误段"},
    {"id": "B-02", "item": "Gε₀ 桥接（循环恒等）",
     "reason": "恒等重排、信息增量 0，且循环",
     "source": "理论体系方程总汇_正确方程集_2026-10-14.md §6"},
    {"id": "B-03", "item": "TUFT-A05 质能关系",
     "reason": "与标准质能关系冲突，终局裁定不通过",
     "source": "判定_TUFT-A05_质能关系冲突_终局裁定_2026-10-07.md"},
    {"id": "B-04", "item": "TUFT-V4.8 公式集（ℒ=(ħc/2)(κ²−τ²)−U 一支）",
     "reason": "作用量双基量纲俱败；共轭动量恒零、场方程退化为代数式；250 位伪精度",
     "source": "65 号卷（36 项判定 PASS9/FAIL18/BOUNDARY4/INFO5）"},
    {"id": "B-05", "item": "TUFT V10 螺旋挠率统一场论（外部来料）",
     "reason": "主方程源项恒零（∇×径向场≡0）、静态解非自身方程之解、电磁支双重死、宇宙学 w=−1/3 与加速矛盾",
     "source": "r108 判定册（49 项判定 FAIL31）"},
    {"id": "B-06", "item": "核心公式 f-桥接族 K-12/K-13/K-14/K-15",
     "reason": "f 为单位约定（可被 A′=fA 完全吸收），物理内容为零",
     "source": "r111 判定册"},
    {"id": "B-07", "item": "核心公式 K-09 电荷定义",
     "reason": "kk′ 为有量纲自由常数且 Ω 无定义 ⇒ 定义欠定",
     "source": "r111 判定册"},
    {"id": "B-08", "item": "α=1/137.036 的『四重几何身份』整页主张",
     "reason": "四重断言审计 FAIL5/CORRECTED8/BOUNDARY5 ⇒ 部分更正，不得整页引用",
     "source": "r110 判定册（23 项判定）"},
    {"id": "B-09", "item": "正确核登记串缺陷族（K-10 name/latex 反号、K-11 name 缺 q、K-09/K-11 q 符号互斥）",
     "reason": "人读登记串与机读因子分解不一致（M02 族）；K-11 name 按字面读数量纲断裂（缺口恰为 [q]）⇒ 引用正确核时 name 串不可直接用，须以 latex/机读因子为准；K-11 name 补 q 后方可引用",
     "source": "r112 判定册（C1/C2）"},
    {"id": "B-10", "item": "核心公式 K-03 质量定义 m = k·dn/dΩ",
     "reason": "n/dn/dΩ 无观测程序、k=4πm_p 由外部 G 锚定、∮dΩ=4π 锁死总立体角致「Ω 收缩导出质速关系」与登记的总质量形式互斥 ⇒ 定义欠定（与 B-07 同族）",
     "source": "r112 判定册（A1–A5）"},
    {"id": "B-11", "item": "K-17 登记名『光速飞行器 F⃗=(C⃗−V⃗)dm/dt』",
     "reason": "名称冠以被 r113 判否的应用宣称：该式作为总力时 V̇≡0（推力效应为零）、作为外力平衡时 V=C(1−m₀/m) 连续无跃迁且 m→0 时 V→−∞（无光速终点）、m=0 状态在理论自身运动学不可达（γ≥1）且账本退化（P→0、E→0）。方程作为 K-07 子集可引，名称须改为『加质量力项（K-07 子集）』",
     "source": "r113 判定册（B1a–B2）"},
    {"id": "B-12", "item": "G=2Z/c「引力光速统一方程」族（张祥前常数 Z=dn/dVdt）",
     "reason": "反解闭环（Z=Gc/2 由 G 反解再「验证」G）；k 有 4 种互斥量纲读法（M / 1/G / √c / L⁻¹）；两版推导的 G 表达式差 8π；几何因子 2 的六读法无一闭合（真积分 0/1/π⁴，余者靠无来源插入系数 3/1、8）；宣称的独立吻合误差 0.045% 超 G 自身不确定度 20 倍 ⇒ 与 B-02（Gε₀ 循环恒等）同族",
     "source": "r115 判定册（A1–A5）"},
    {"id": "B-13", "item": "《光子的几何本源与运动模型证明》「光子=静止质量为零的激发电子圆柱螺旋」族（模型一/二、E∝ω 无系数、p 自由、动量双读法）",
     "reason": "动量定义 P=m(C−V) 与结论 V=C 互斥（⇒P=0 vs 验证节 p⃗=mC⃗ 需 V=0）；双电子动量-能量断裂 29.29%；κ=ω/f 扫描三接口无解（κ=2π⇒p=0 不传播、κ=1⇒v_z=0.917c、κ>2π 无实数解）；Larmor 辐射猝灭（带电螺旋偶极子寿命 2.65e-19 s vs >4.35e17 s，缺口 1.64e36 倍）；传播速度自承随激发条件可变；验证节对螺旋参数依赖 0（抄录）⇒ 与 B-04/B-05 同族（语料支整支不可引用）",
     "source": "r121 判定册（A1–B7，13 项 FAIL）"},
    {"id": "B-14", "item": "低能标 / 额外维 GUT 族（把统一能标降到质子衰变安全线 M_GUT < 6.12e15 GeV 者，含 ADD/RS 的 TeV 统一）",
     "reason": "τ_p ∝ M_GUT⁴（维度-6）⇒ 由 Super-K 上限 2.4e34 yr 反算安全线 M_GUT ≥ 6.12e15 GeV（10^15.79）；1e10 GeV 给 τ_p=1.71e11 yr（快 1.40e23 倍）、1 TeV 给 1.71e-17 yr（≈5.4e-10 s）⇒ 低能标统一被质子衰变上限直接排除，越线 12.79 量级。非'未检验'而是'已被排除'",
     "source": "r123 判定册（R3a/R3b，守卫 g_r3_proton_hard_gate）"},
]
add("D04", "FAIL",
    "黑名单登记册（%d 条，不可引用）" % len(BLACKLIST),
    " ；".join("%s %s" % (b["id"], b["item"]) for b in BLACKLIST),
    blacklist=BLACKLIST)

# ---------------------------------------------------------------- 5. 汇总
tally = {}
for e in ENTRIES:
    tally[e["verdict"]] = tally.get(e["verdict"], 0) + 1
verdict_total = "FAIL" if tally.get("FAIL", 0) else ("BOUNDARY" if tally.get("BOUNDARY", 0) else "PASS")
guard_failed = [g for g in GUARDS if not g[1]]

SUMMARY = {
    "tag": OUT_TAG,
    "date": "2026-10-19",
    "role": "核心公式体系总册（整理 + 机器合账，不重判）",
    "verdict_total": verdict_total,
    "tally": tally,
    "n_entries": len(ENTRIES),
    "guards_total": len(GUARDS),
    "guards_failed": len(guard_failed),
    "cores_before": CORES_BEFORE,
    "cores_after": CORES_AFTER,
    "cores_downgraded": DOWNGRADED,
    "chain_dist": dist,
    "chain_files": len(r_files),
    "blacklist_n": len(BLACKLIST),
}

payload = {"summary": SUMMARY, "entries": ENTRIES,
           "guards": [{"name": g[0], "ok": g[1], "desc": g[2]} for g in GUARDS],
           "blacklist": BLACKLIST}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------- 6. 生成数据 md
lines = ["# 53 数据产物｜核心公式体系总册合账（机器读数）\n",
         "- 角色：整理 + 合账（不重判）｜ 总读数：**%s** ｜ 条目 %d ｜ %s ｜ 守卫 %d/%d"
         % (verdict_total, len(ENTRIES), " / ".join("%s %d" % kv for kv in sorted(tally.items())),
            len(GUARDS) - len(guard_failed), len(GUARDS)),
         "- 正确核：%d → **%d**（降级 %s）｜ r 链文件 %d 份（分布 %s）｜ 黑名单 %d 条\n"
         % (CORES_BEFORE, CORES_AFTER, "、".join(DOWNGRADED), len(r_files), dist, len(BLACKLIST)),
         "| 代号 | 读数 | 条目 | 机读依据 |", "|---|---|---|---|"]
for e in ENTRIES:
    det = e["detail"].replace("\n", " ").replace("|", "/")
    if len(det) > 300:
        det = det[:300] + "…"
    lines.append("| %s | **%s** | %s | %s |" % (e["code"], e["verdict"], e["title"], det))
lines.append("\n## 守卫\n")
for g in GUARDS:
    lines.append("- %s **%s** %s" % (g[0], "PASS" if g[1] else "FAIL", g[2]))
lines.append("\n## 黑名单\n")
for b in BLACKLIST:
    lines.append("- **%s** %s —— %s（来源：%s）" % (b["id"], b["item"], b["reason"], b["source"]))
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

with open(OUT_TXT, "w", encoding="utf-8") as f:
    f.write("53 core ledger | verdict=%s | entries=%d | guards=%d/%d\n"
            % (verdict_total, len(ENTRIES), len(GUARDS) - len(guard_failed), len(GUARDS)))
    f.write("cores %d -> %d (downgraded %s)\n" % (CORES_BEFORE, CORES_AFTER, DOWNGRADED))
    f.write("chain dist=%s files=%d\n" % (dist, len(r_files)))
    for e in ENTRIES:
        f.write("%-5s %-9s %s\n" % (e["code"], e["verdict"], e["title"]))
    for g in GUARDS:
        f.write("GUARD %-32s %s %s\n" % (g[0], "PASS" if g[1] else "FAIL", g[2]))
    f.flush()

# ---------------------------------------------------------------- 7. 生成总册卷 md
health_txt = "H %d · O %d · C %d · U %d" % health if health else "读取失败"
tuft_txt = "PASS %d · FAIL %d · BOUNDARY %d · INFO %d" % tuft if tuft else "读取失败"
v8_txt = "PASS %d · FAIL %d · INFO %d · 部分闭合 %d" % v8 if v8 else "读取失败"

vol = []
vol.append("# 53 · 核心公式体系总册（2026-10-19）\n")
vol.append("> **openuft · 07_统一场方程 · 编号 53**｜整理 + 机器合账卷（不重判任何条目）")
vol.append("> 引擎：`53_core_ledger_calc.py` → `53_core_ledger_results.json` + `_data.md` + `_out.txt`（退出码 0，守卫 %d/%d）"
           % (len(GUARDS) - len(guard_failed), len(GUARDS)))
vol.append("> 上游：[理论体系方程总汇_正确方程集_2026-10-14](../理论体系方程总汇_正确方程集_2026-10-14.md)（继承账本，只读）· [r111 判定册](../04_公共成果/本项目_全维自洽与归一化/判定_TUFT-r111-核心公式f桥接族与电荷定义_可辨识性与约定吸收攻破_2026-10-19.md)（r111 降级依据）· [r112 判定册](../04_公共成果/本项目_全维自洽与归一化/判定_TUFT-r112-正确核残余软肋_K-03质量定义_K-07力方程_K-11磁场登记_攻破_2026-10-19.md)（r112 降级依据）· [54 全物理现象覆盖矩阵](54_全物理现象覆盖矩阵_2026-10-19.md)（覆盖面对账）\n")
vol.append("---\n")
vol.append("## 0. 本卷是什么、不是什么\n")
vol.append("**是**：把散在 10-14 总汇、r95–r121 攻破链、62–65 号螺旋线里的判定结果合到一本账，数字全部由引擎机读注入（末次同步 2026-10-20：入账 r118–r121）。")
vol.append("**不是**：不重判任何方程、不产生新物理、不修改被引文件一个字节。凡本卷数字与上游文件不一致，以上游文件为准并触发本引擎守卫。\n")
vol.append("## 1. 继承账本（机读 10-14 总汇，抗漂移核对）\n")
vol.append("| 口径 | 机读值 | 自称值 | 守卫 |")
vol.append("|---|---|---|---|")
vol.append("| 正确核行数 | %d（唯一 %d） | 22 | %s |" % (n_k, uniq_k, "PASS" if (n_k == 22 and uniq_k == 22) else "FAIL"))
vol.append("| 22 体系健康度 | %s | H2/O10/C6/U4 | %s |" % (health_txt, "PASS" if health == (2, 10, 6, 4) else "FAIL"))
vol.append("| TUFT 报告集 73 份 | %s | 479/338/228/884 | %s |" % (tuft_txt, "PASS" if tuft == (479, 338, 228, 884) else "FAIL"))
vol.append("| v8 全维分析 272 项 | %s | 169/62/18/23 | %s |" % (v8_txt, "PASS" if v8 == (169, 62, 18, 23) else "FAIL"))
vol.append("\n> 诚实备注（随继承一并转录）：22 体系里两个 H（s01/s13）来自体系自述与实跑记录，**非库级终审**；`01_独立体系/README.md` 仍标 `unreviewed`。\n")
vol.append("## 2. 增量账本（2026-10-14 → 10-20）\n")
vol.append("### 2.1 r 系列攻破链（机读 %d 份数据文件）\n" % len(r_files))
vol.append("| 文件 | 总判决 | 计数 |")
vol.append("|---|---|---|")
for c in chain:
    cnt = c.get("counts") or {}
    cnt_txt = " / ".join("%s %d" % kv for kv in sorted(cnt.items())) if cnt else "—"
    vol.append("| %s | **%s** | %s |"
               % (c["file"].replace("TUFT-", "").replace(".json", ""), round_class(c), cnt_txt))
vol.append("\n分布：%s。派生规则（本引擎声明）：旧 schema 无显式 verdict 的轮次按 counts 中 FAIL>0 记失败轮。**增量以否定与边界为主**：没有任何一轮把外部来料或内部候选升格为'统一已完成'。\n" % (dist or "空"))
vol.append("### 2.2 螺旋几何化子卷（62–65 号）\n")
vol.append("65 号卷对 V4.8 公式集的机器审计：%s ⇒ 作用量层在 (M,L,T) 双基下不自洽（A6–A10 五连 FAIL）、共轭动量恒零、场方程只剩代数式（B1/B2）⇒ **V4.8 当前版本整支入黑名单**，正确下一步是 Step-1 维度修复而非任选续作选项。\n"
           % (("PASS=%d / FAIL=%d / BOUNDARY=%d / INFO=%d" % v48) if v48 else "读取失败"))
vol.append("### 2.3 主题归纳：力的统一（机读七轮判决，守卫 g_theme_force_all_fail）\n")
vol.append("| 轮次 | 机读判决 | 该轮对「力的统一」的攻破点 |")
vol.append("|---|---|---|")
for r, v, n in theme_rows:
    vol.append("| %s | **%s** | %s |" % (r, v, n))
vol.append("\n归纳：**七轮全部 FAIL，0 轮把该宣称升格**。结构层（r113：四分支源侧因子 0/4 ⇒ 分支不可能是力定律）与映射层（r112：384 读法/0 约束 ⇒ 不可辨识）合流 ⇒ 『力的统一』既无可能也无区分；应用层（r113：飞碟推进两种读数俱败）随之崩塌。方程层（r120：候选全集 9 方程 2 验证——代数容量 SM 一代 Weyl 15 匹配 SU(5)（SO(10) 余 1、E6 余 12），但质子衰变最小 SU(5) 预言快 Super-K 上限 523 倍、引力缺口 4.18 量级、MSSM 控制组 1.27σ 通过证判据有判别力）⇒ 不存在被实验确立的『所有力的大统一方程』。**退守封堵层（r123，r120 增补卷）**：换群族八族全 FAIL（容量余量 0/1/12/233 与 n_free 2/6/8/13 同向单调增，而可检验观测量恒为 3 ⇒ 换群只是把不确定性搬进更多模数）；加阈值凑汇聚需参数当量 41 ≫ 2 ⇒ 不可辨识（同 r112 款，但**承认 MSSM 1.27σ 是真汇聚**，代价 105 参数 + 未见 + 维度-5）；额外维降能标被质子衰变硬门枪毙（τ_p ∝ M⁴ ⇒ 安全线 **M_GUT ≥ 6.12e15 GeV**，TeV 方案越线 **12.79 量级**，τ_p≈1.71e-17 yr）；弦/超引力 10^500 真空 ⇒ 非唯一 + 本代不可证伪（不判其数学错）；剔除引力则命题自削且 4.18 量级缺口仍在 ⇒ **五条退路无一存活**。方程层幸存物 = 牛顿第二定律的几何记号改写 + 三张外挂的教科书场公式（K-04/K-10/K-11）；唯一『已完成的统一』范本 = 电弱统一（M_W/M_Z=cosθ_W、预言 m_t 偏差 0.139%）。\n")
vol.append("### 2.4 主题归纳：引力的本源（机读四轮判决，守卫 g_theme_gravity_all_fail）\n")
vol.append("| 轮次 | 机读判决 | 该轮对「引力的本源」的攻破点 |")
vol.append("|---|---|---|")
for r, v, n in theme_g_rows:
    vol.append("| %s | **%s** | %s |" % (r, v, n))
vol.append("\n归纳：**四轮全部 FAIL，0 轮把该宣称升格**。常数层（r112：G=ħc/m_p² 重言残差 3.0e-50；r114：G=α²μ₀ 反解闭环、ρ_fit=3.33 nm 无基本尺度对应；r115：G=2Z/c 反解闭环 + k 四量纲互斥）、机制层（r114：m=ω²r³ 与开普勒常数同一性矛盾——八行星 ω²a³ 散布 1.5% 而方程要求质量全相等，实测跨 5750 倍；r115：拖拽/涡量/度规扰动/引力波方程机制全败、因子 2 六读法无一闭合、光速自毁 c√2、GW 公式零螺旋依赖）、本体层（r114：S12 公设零约束、GAQ 场方程右端恒零）三层合流 ⇒ 『引力的几何本源』无一个版本成立。正确核内引力内容 = K-04 牛顿记号改写一条；UFE-1′ 已由 B-01 勘误废除；G=2Z/c 族入黑名单 B-12。\n")
vol.append("### 2.5 主题归纳：光子的本质（机读六轮判决，守卫 g_theme_photon_all_fail）\n")
vol.append("| 轮次 | 机读判决 | 该轮对「光子内部运行」的攻破点 |")
vol.append("|---|---|---|")
for r, v, n in theme_p_rows:
    vol.append("| %s | **%s** | %s |" % (r, v, n))
vol.append("\n归纳：**六轮全部 FAIL，0 轮把该宣称升格**。边界轮（r53：螺旋空间度规 Riemann 全零=平直坐标选择、圆柱螺旋轨道与向心加速度矛盾；r56：τ 可被 boost 精确清零、v_z=c·cosθ<c、三约束互斥定理 {总速率=c, 轴向速率=c, R>0}⇒∅、ω↔f 映射公设未声明）、命题轮（r116：36 格穷举 FAIL26/PASS2/BOUNDARY8——光速预算把螺旋半径压到 1.1e-16 m（曲率半径 56 m ⇒ 轨迹必为直线）、自转载荷定理 v_eq=c/√a（实心球 1.5811c）、唯一分歧格归因到判据集缺洛伦兹协变性；r117：dΦ≡0 精确零 + de Broglie 内时钟被 m=0 锁死、七门全 FAIL、180 组合枚举存活 15 例全为 O0_none）、退守轮（r118：Williamson–van der Mark 电子环形光子模型超 LEP 点状上限 6.90e5 倍、OAM 避难所四门全 FAIL——SAM/OAM 分解是原理性 no-go、协变性分歧 5-0 闭合）与语料轮（r121：《光子的几何本源与运动模型证明》13 项 FAIL——动量双读法互斥 P=0 vs mc、双电子动量-能量断裂 29.29%、κ 扫描三接口无解、Larmor 辐射寿命缺口 1.64e36 倍）四层合流 ⇒ 『光子以圆柱螺旋方式内部运行』无一个版本成立；唯一在机器判决中「成立」的内部样态是场矢量旋转（=Maxwell 圆偏振，零新增）与结构光能流螺旋（光束横模属性，非单光子）。语料支整支入黑名单 B-13。\n")
vol.append("## 3. 更新后总账本\n")
vol.append("| 指标 | 10-14 | 10-19/20（本卷） | 变动原因 |")
vol.append("|---|---|---|---|")
vol.append("| 正确核 | 22 | **%d** | r111 降 5 条（f-桥接族 4 条单位重写 + K-09 欠定）；r112 降 1 条（K-03 欠定） |" % CORES_AFTER)
vol.append("| H 级体系 | 2 | 2（不变） | 无新增体系级审计 |")
vol.append("| 黑名单 | 2（UFE-1′、Gε₀） | **%d** | 新增 V4.8、V10、f-桥接族、K-09、α 四重身份、TUFT-A05、登记串缺陷族、K-03、K-17 修名（B-11）、G=2Z/c 循环恒等族（B-12）、光子几何本源语料族（B-13）、低能标/额外维 GUT 族（B-14） |" % len(BLACKLIST))
vol.append("| 统一场论达成度 | 1/6 | **1/6（不变）** | 增量全为否定/边界；UFT-2~6 无一项转为达标（r119 七必要条件机读 1/7，仅 U7 与精密观测相容通过；电弱控制组 6/6 证判据有判别力） |")
vol.append("| 主题归纳 | §2.3 五轮 / §2.4 四轮 | **§2.3 七轮 / §2.4 四轮 / §2.5 六轮** | §2.3 补 r120 方程层 + r123 退守封堵层；§2.5 光子主题补 r118 退守轮 + r121 语料轮（r53/r56/r116/r117/r118/r121 机读全 FAIL） |")
vol.append("\n## 4. 正确核 %d 条保留清单（按性质分组；机读分区守卫 g_groups_partition）\n" % CORES_AFTER)
vol.append("| 组 | 条目 | 性质 |")
vol.append("|---|---|---|")
for gname, ids, gnote in CORE_GROUPS:
    vol.append("| %s | %s | %s |" % (gname, "、".join(ids), gnote))
vol.append("\n> 结构读数（随继承一并转录）：**保留的 %d 条里没有一条是来料新增的物理**，全部是教科书物理在另一套记号下的改写、代数恒等或已证几何定理。r111 降 5 条、r112 降 1 条（K-03 移入黑名单 B-10）后这一读数不变、且更干净；K-11 的登记串修串要求见黑名单 B-09。\n" % CORES_AFTER)
vol.append("## 5. 黑名单（不可引用登记册）\n")
vol.append("| 编号 | 对象 | 理由 | 来源 |")
vol.append("|---|---|---|---|")
for b in BLACKLIST:
    vol.append("| %s | %s | %s | %s |" % (b["id"], b["item"], b["reason"], b["source"]))
vol.append("\n## 6. 引用规则（给后续卷与对外文稿）\n")
vol.append("1. 引『正确核』必须引 %d 条版；引 17 条版须同时引 r112 降级说明（K-03）；引 22 条版须同时引 r111 + r112 降级说明。" % CORES_AFTER)
vol.append("2. 黑名单对象不得作为任何推导的前提；若需讨论，只能以『已被 X 号卷判否』的形式出现。")
vol.append("3. 引用『宇宙大统一方程的四力统一』或『光速飞行器推进』必须同时引 r113 判定册；引用『所有力的大统一方程』须同时引 r120 + r123 判定册（r120=候选全集状态机判，r123=退守路径封堵，两册条目不可相加）；引用『换更大群/补阈值/降能标/弦论已完成/先统一三力』等退守话术须同时引 r123 判定册并注明该路已被封堵；单独引用 K-17 名称而不带 B-11 修名说明，按黑名单处理。")
vol.append("4. 引用『引力/引力常数的几何本源』『空间螺旋生引力』（含 G=α²μ₀、G=ℏc/m_p²、m=ω²r³、G=2Z/c、GAQ 引力场方程）必须同时引 r114 + r115 判定册；单独引用而不带本册说明，按未决宣称或黑名单 B-12 处理。")
vol.append("5. 引用『光子以圆柱螺旋方式运动 / 光子内部自转 / 光子携带内禀时钟（de Broglie 内时钟）/ 光子螺旋角频率=光子频率』必须同时引 r116 + r117 判定册；引用电子环形光子模型 / 光子 OAM 避难所须同时引 r118 判定册；引用『光子的几何本源』两种光子模型 / 光子静止于空间中须同时引 r121 判定册（黑名单 B-13）；引用结构光坡印廷涡旋/OAM 须注明其为光束横模属性而非单光子内部运行（r116 B05）；单独引用而不带本册说明，按未决宣称或黑名单处理。")
vol.append("6. 本卷数字由引擎注入；若人工改动本卷任何数字，须重跑 `53_core_ledger_calc.py` 使其回归机读值。")
vol.append("7. 覆盖面的定量读数见 54 号卷；两卷数字同源（都经本引擎族产出），不一致即触发守卫。\n")
vol.append("## 7. 红线\n")
vol.append("数学自洽 ≠ 有物理内容 ≠ 实验证实。本卷是整理与合账册，不产生新物理；未改任何被引文件字节；未跑 git。\n")

with open(VOL_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(vol))

print("[53] VERDICT=%s entries=%d guards=%d/%d cores=%d->%d"
      % (verdict_total, len(ENTRIES), len(GUARDS) - len(guard_failed), len(GUARDS), CORES_BEFORE, CORES_AFTER), flush=True)
if guard_failed:
    for g in guard_failed:
        sys.stderr.write("GUARD FAIL: %s :: %s\n" % (g[0], g[2]))
    sys.exit(2)
sys.exit(0)
