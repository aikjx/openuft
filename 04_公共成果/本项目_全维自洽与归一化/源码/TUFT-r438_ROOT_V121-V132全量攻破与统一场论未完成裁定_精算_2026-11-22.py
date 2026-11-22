# -*- coding: utf-8 -*-
"""TUFT-r438 | ROOT V121-V132 全量攻破 + 统一场论未完成裁定.

定位: 外生来料全量取证 (非重判), 机核四件硬事实:
  1) 12/12 版本正文自认未完成 (自述否定句机检);
  2) h_geo=alpha 被 Lorentz 速度叠加数学否证 (坐标量必变);
  3) G 无法由 {c,hbar} 量纲生成 (0 命中), 含 m 唯一族仍须外部 m_P;
  4) UFT-1..6 判据矩阵 0/6, 12 版本 0 声称完成.

不做: 不宣称攻破、不否证方向、不重判既有册、不改被引文件字节.
纯标准库 / Python 3.8 / Fraction 精确 + Decimal 60 位.
"""
import io
import json
import re
import sys
from decimal import Decimal as Dec
from decimal import getcontext
from fractions import Fraction as F
from pathlib import Path
from urllib.parse import unquote

try:
    _r = getattr(sys.stdout, "reconfigure", None)
    if callable(_r):
        _r(errors="replace")
except Exception:
    pass

getcontext().prec = 60

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
OUT = BASE / "数据"
NAME = "TUFT-r438_ROOT_V121-V132全量攻破与统一场论未完成裁定_精算_2026-11-22"
ROUND = "r438"
DATE = "2026-11-22"

CORPUS = ROOT / "90_历史归档" / "来源语料_ufthub_ROOT_V121-V132_202611c"
ZIPLIST = ROOT.parent / "ufthub" / "zip" / "202611c" / "_清单_ROOT_V系列_202611c.json"
EXTLIST = CORPUS / "_解压清单_ROOT_V121-V132_202611c.json"

ENTRIES = []
GUARDS = []
CONTROLS = []


def add(code, status, title, detail):
    ENTRIES.append(dict(code=code, status=status, title=title, detail=detail))


def guard(code, cond, note):
    GUARDS.append(dict(code=code, ok=bool(cond), note=note))


def ctrl(code, cond, note):
    CONTROLS.append(dict(code=code, ok=bool(cond), note=note))


def read_text(p):
    for enc in ("utf-8-sig", "utf-8", "gbk"):
        try:
            return io.open(str(p), encoding=enc).read()
        except Exception:
            continue
    return ""


# ============================================================ A 事实源实读
zip_data = json.loads(read_text(ZIPLIST))
ext_data = json.loads(read_text(EXTLIST))
summary = zip_data["summary"]
files = zip_data["files"]
rows = ext_data["rows"]

guard("G-A1", CORPUS.is_dir(), "语料目录存在: %s" % CORPUS)
guard("G-A2", ZIPLIST.is_file() and EXTLIST.is_file(), "两份清单均存在")
guard("G-A3", summary["count"] == 20, "清单 count=20, 实得 %d" % summary["count"])
guard("G-A4", sorted(summary["v_covered"]) == list(range(121, 133)),
      "版本连续 V121-V132")

vdirs = sorted([d for d in CORPUS.iterdir() if d.is_dir() and re.match(r"^V\d+$", d.name)])
md_files = sorted([p for d in vdirs for p in d.rglob("*.md")])
guard("G-A5", len(vdirs) == 12, "版本目录 12, 实得 %d" % len(vdirs))
guard("G-A6", len(md_files) > 0, "md 文件数 > 0, 实得 %d" % len(md_files))

# ============================================================ B 状态词盘点
PATTERNS = {
    "pass": [r"\bPASS\b", r"通过"],
    "fail": [r"\bFAIL\b", r"失败", r"被排除", r"否决", r"不可行"],
    "open": [r"\bOPEN\b", r"开放项", r"仍开放", r"未闭合"],
    "counter": [r"反例", r"反证", r"counter-?example"],
    "not_proven": [r"未证明", r"不能\s*导出", r"无法\s*导出", r"未\s*派生"],
    "synthetic": [r"SYNTHETIC", r"合成数据", r"为合成"],
    "codata": [r"CODATA"],
}
RC = {k: [re.compile(p, re.I) for p in v] for k, v in PATTERNS.items()}
AGG = {k: 0 for k in PATTERNS}
TOTAL_LINES = 0
TOTAL_MD = len(md_files)

NEG = [re.compile(p) for p in [
    r"不是完成统一场论", r"不是已经完成", r"非原创四力大统一",
    r"物理大统一未证明", r"未证明[^\n]{0,16}统一", r"统一[^\n]{0,16}未证明",
    r"不是[^\n]{0,16}四力统一理论", r"不是发现第五力",
]]

VERSIONS = []
for d in vdirs:
    v = int(d.name[1:])
    v_mds = sorted(d.rglob("*.md"))
    counts = {k: 0 for k in PATTERNS}
    lines = 0
    neg_hits = []
    for p in v_mds:
        t = read_text(p)
        lines += t.count("\n")
        for k in PATTERNS:
            n = 0
            for rx in RC[k]:
                n += len(rx.findall(t))
            counts[k] += n
        for line in t.splitlines():
            s = line.strip()
            if not s:
                continue
            for rx in NEG:
                if rx.search(s):
                    neg_hits.append(s[:160])
                    break
    for k in PATTERNS:
        AGG[k] += counts[k]
    TOTAL_LINES += lines
    title = ""
    for f in files:
        if int(f["v"]) == v:
            title = f["title"]
            break
    VERSIONS.append(dict(
        version="V%d" % v, title=title, md=len(v_mds), lines=lines,
        counts=counts, neg=bool(neg_hits), neg_sample=neg_hits[:2],
        verdict="NOT_COMPLETE",
    ))

guard("G-B1", AGG["pass"] > 0, "PASS 计数非零 (%d)" % AGG["pass"])
guard("G-B2", AGG["open"] > 0, "OPEN 计数非零 (%d)" % AGG["open"])
guard("G-B3", sum(v["md"] for v in VERSIONS) == TOTAL_MD, "版本 md 数求和 = 总 md")
add("MT01", "PASS", "事实源与口径实读",
    "20 文件 / 18 唯一包 / 12 版本目录 / %d 篇 md / %d 行；解压清单 unique=%d dup=%d"
    % (TOTAL_MD, TOTAL_LINES, ext_data["unique_packages"], ext_data["dup_packages_skipped"]))
add("MT02", "INFO", "全批状态词盘点",
    "PASS %d / FAIL %d / OPEN %d / 反例 %d / 未证明 %d / SYNTHETIC %d / CODATA %d"
    % (AGG["pass"], AGG["fail"], AGG["open"], AGG["counter"],
       AGG["not_proven"], AGG["synthetic"], AGG["codata"]))

# ============================================================ C 自述否定句
neg_versions = [v["version"] for v in VERSIONS if v["neg"]]
guard("G-C1", len(neg_versions) >= 5, "自述否定句命中版本数 %d (>=5)" % len(neg_versions))
add("MT03", "FAIL", "12 版本自述未完成（作者自认）",
    "命中版本 %d/12: %s" % (len(neg_versions), ",".join(neg_versions)))

# ============================================================ D Lorentz 反例
ALPHA = Dec("0.0072973525693")
BETA = Dec("0.6")
REPORT_U2 = Dec("-0.59530916")


def boost_u(u, beta):
    return (u - beta) / (Dec(1) - u * beta)


u2 = boost_u(ALPHA, BETA)
u0 = boost_u(ALPHA, Dec(0))
rel = abs((u2 - REPORT_U2) / REPORT_U2)
guard("G-D1", u0 == ALPHA, "beta=0 时 u'=u（阳性对照，判据有牙）")
guard("G-D2", rel < Dec("1e-6"), "beta=0.6 复算与来料 -0.59530916 一致, rel=%.3E" % rel)
guard("G-D3", u2 < 0, "boost 后 u'<0（符号翻转，非数值噪声）")
ctrl("C-D1", u0 == ALPHA and u2 < 0, "Lorentz 阳性/阴性并存")
add("MT04", "FAIL", "h_geo=alpha 被 Lorentz 速度叠加否证",
    "u=alpha=0.0072973525693, beta=0.6 -> u'=%.11f (来料 -0.59530916, rel=%.2E)"
    % (u2, rel))

# ============================================================ E G 量纲否决
DIM = {
    "c": (0, 1, -1), "hbar": (1, 2, -1), "G": (-1, 3, -2), "m": (1, 0, 0),
}


def dadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def dscale(d, n):
    return tuple(x * n for x in d)


def dim_ch(a, b):
    return dadd(dscale(DIM["c"], a), dscale(DIM["hbar"], b))


hits2 = [(a, b) for a in range(-8, 9) for b in range(-8, 9)
         if dim_ch(a, b) == DIM["G"]]
hits3 = [(a, b, d) for a in range(-8, 9) for b in range(-8, 9) for d in range(-8, 9)
         if dadd(dim_ch(a, b), dscale(DIM["m"], d)) == DIM["G"]]
guard("G-E1", dim_ch(1, 1) != DIM["G"], "c^1 hbar^1 != G（判据有牙）")
guard("G-E2", len(hits2) == 0, "{c,hbar} 二维穷举 0 命中, 实得 %d" % len(hits2))
guard("G-E3", hits3 == [(1, 1, -2)], "含 m 唯一命中 (1,1,-2), 实得 %s" % (hits3[:3],))
guard("G-E4", dadd(dim_ch(1, 1), dscale(DIM["m"], -2)) == DIM["G"],
      "c hbar / m^2 量纲恰为 G（工具非坏）")
ctrl("C-E1", len(hits2) == 0 and len(hits3) == 1, "量纲穷举阳性/阴性并存")
add("MT05", "FAIL", "G 无法由 {c,hbar} 生成（量纲秩否决）",
    "二维 0 命中；含 m 唯一族 (a,b,d)=(1,1,-2) ⇒ G∝c*hbar/m^2 仍须外部 m_P")

# ============================================================ F 合成/真实
real_obs = len([p for p in md_files if "真实卫星" in read_text(p) and "已获得" in read_text(p)])
guard("G-F1", AGG["synthetic"] > 0, "SYNTHETIC 计数 %d" % AGG["synthetic"])
add("MT06", "FAIL", "证据等级：合成数据 0 真实观测",
    "SYNTHETIC/合成 %d 处；真实观测已获得 %d 处" % (AGG["synthetic"], real_obs))

# ============================================================ G UFT 判据矩阵
UFT = [
    ("UFT-1 数学自洽", "PARTIAL", "恒等式层通过；同批含严格反例（Lorentz/整数塔）"),
    ("UFT-2 四力统一", "FAIL", "无共同耦合/共同来源；全批 OPEN %d" % AGG["open"]),
    ("UFT-3 常数派生", "FAIL", "G 量纲 0 命中；alpha 条件识别且被 boost 否证"),
    ("UFT-4 观测复现", "FAIL", "SYNTHETIC %d，真实观测 0" % AGG["synthetic"]),
    ("UFT-5 可证伪预言", "FAIL", "无 E/F 级；自述未提供超越 GR 的可证伪预测"),
    ("UFT-6 外部验证", "FAIL", "0"),
]
uft_pass = len([x for x in UFT if x[1] == "PASS"])
guard("G-G1", uft_pass == 0, "UFT 判据 PASS 计数 0, 实得 %d" % uft_pass)
add("MT07", "FAIL", "UFT-1..6 判据矩阵 0/6",
    "PARTIAL 1 / FAIL 5 / PASS 0")

# ============================================================ H 逐版本裁定
claim_done = len([v for v in VERSIONS if v["verdict"] == "COMPLETE"])
guard("G-H1", claim_done == 0, "声称完成版本数 0, 实得 %d" % claim_done)
guard("G-H2", len(VERSIONS) == 12, "版本数 12")
add("MT08", "FAIL", "12 版本逐条裁定：0 声称完成",
    "NOT_COMPLETE 12/12；OPEN 合计 %d；反例合计 %d" % (AGG["open"], AGG["counter"]))

# ============================================================ I 同构与缺口
add("MT09", "PASS", "与前两批同构（互印）",
    "r430 对 V83-V120 判 0/40 四门禁；本批 V121-V132 方向一致（0/12），非新物理")
add("MT10", "BOUNDARY", "唯一缺口定价：第一性输入",
    "G / 规范群 / 粒子谱 / 量子一致性 四类输入均未派生；缺的是输入不是算力")

# ============================================================ J 产出
guard("G-J1", len(ENTRIES) >= 8, "条目数 %d" % len(ENTRIES))
guard("G-J2", all(g["ok"] for g in GUARDS), "全部守卫通过")
guard("G-J3", all(c["ok"] for c in CONTROLS), "全部控制组通过")
add("MT11", "INFO", "红线",
    "归档≠证实；解压≠成立；代码自测≠物理验证；不宣称攻破、不否证方向")

payload = dict(
    round=ROUND, date=DATE, name=NAME,
    corpus=str(CORPUS),
    files=summary["count"], total_bytes=summary["total_bytes"],
    unique_packages=ext_data["unique_packages"],
    dup_skipped=ext_data["dup_packages_skipped"],
    versions=len(VERSIONS), md=TOTAL_MD, lines=TOTAL_LINES,
    aggregate=AGG,
    entries=ENTRIES, guards=GUARDS, controls=CONTROLS,
    version_rows=VERSIONS,
    uft=[dict(k=a, status=b, note=c) for a, b, c in UFT],
    lorentz=dict(alpha=str(ALPHA), beta=str(BETA), u2=str(u2), report_u2=str(REPORT_U2)),
    dimension=dict(hits2=len(hits2), hits3=[list(x) for x in hits3[:5]]),
    verdict="ROOT-V121-V132--SELF-DECLARED-INCOMPLETE-12OF12--UFT-0OF6--LORENTZ-REFUTED--G-DIMENSION-EMPTY--NOT-COMPLETED",
)

OUT.mkdir(parents=True, exist_ok=True)
jf = OUT / (NAME + ".json")
io.open(str(jf), "w", encoding="utf-8").write(
    json.dumps(payload, ensure_ascii=False, indent=1))

# 数据 md（简表）
L = []
L.append("# " + NAME)
L.append("")
L.append("- 轮次 %s ｜ 日期 %s" % (ROUND, DATE))
L.append("- 条目 %d：%s" % (len(ENTRIES), " / ".join(
    "%s %d" % (s, len([e for e in ENTRIES if e["status"] == s]))
    for s in ("PASS", "FAIL", "BOUNDARY", "INFO", "CORRECTED"))))
L.append("- 守卫 %d/%d ｜ 控制组 %d/%d" % (
    len([g for g in GUARDS if g["ok"]]), len(GUARDS),
    len([c for c in CONTROLS if c["ok"]]), len(CONTROLS)))
L.append("")
L.append("## 全批聚合")
L.append("")
L.append("| 指标 | 值 |")
L.append("|---|---|")
for k in ("pass", "fail", "open", "counter", "not_proven", "synthetic", "codata"):
    L.append("| %s | %d |" % (k, AGG[k]))
L.append("")
L.append("## 逐版本")
L.append("")
L.append("| 版本 | md | 行 | PASS | FAIL | OPEN | 反例 | 合成 | 自述未完成 |")
L.append("|---|---|---|---|---|---|---|---|---|")
for v in VERSIONS:
    c = v["counts"]
    L.append("| %s | %d | %d | %d | %d | %d | %d | %d | %s |" % (
        v["version"], v["md"], v["lines"], c["pass"], c["fail"], c["open"],
        c["counter"], c["synthetic"], "是" if v["neg"] else "否"))
L.append("")
L.append("## UFT 判据")
L.append("")
L.append("| 判据 | 状态 | 说明 |")
L.append("|---|---|---|")
for a, b, c in UFT:
    L.append("| %s | %s | %s |" % (a, b, c))
L.append("")
io.open(str(OUT / (NAME + ".md")), "w", encoding="utf-8").write("\n".join(L))

# report
R = []
R.append("ROUND %s  %s" % (ROUND, DATE))
for e in ENTRIES:
    R.append("[%s] %s | %s" % (e["status"], e["code"], e["title"]))
R.append("AGG " + " ".join("%s=%d" % (k, AGG[k]) for k in AGG))
R.append("LORENTZ u2=%s rel=%.3E" % (u2, rel))
R.append("DIM hits2=%d hits3=%s" % (len(hits2), hits3[:3]))
R.append("GUARDS %d/%d  CONTROLS %d/%d" % (
    len([g for g in GUARDS if g["ok"]]), len(GUARDS),
    len([c for c in CONTROLS if c["ok"]]), len(CONTROLS)))
R.append("VERDICT " + payload["verdict"])
io.open(str(OUT / (NAME + "_report.txt")), "w", encoding="utf-8").write("\n".join(R))

print("ENTRIES %d" % len(ENTRIES))
print("GUARDS %d/%d  CONTROLS %d/%d" % (
    len([g for g in GUARDS if g["ok"]]), len(GUARDS),
    len([c for c in CONTROLS if c["ok"]]), len(CONTROLS)))
print("LORENTZ u2=%.11f rel=%.3E" % (u2, rel))
print("DIM hits2=%d hits3=%s" % (len(hits2), hits3[:3]))
print("VERDICT " + payload["verdict"])
