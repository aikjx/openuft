# -*- coding: utf-8 -*-
"""ROOT 本源核心公式 3D 可视化「片段级」来料审计。

来料只给到 <head> 与 header 样式，没有正文、公式与 3D 实现；
因此本引擎只做可机判的片段事实与标题宣称对账，不虚构公式、不重做 ROOT V128 链。

门族：
  G AST 前置；
  F1 片段不完整检测；F2 标题层四力统一宣称检测；F3 MathJax 已载但无公式正文；
  F4 红线锚点仍在；F5 无内联 3D 实现；
  N 注入闭合标签/假公式必须翻红。
不占 RID、不登记 README、不与 r403/r410/r413/r437 或 ROOT V128 八册链相加。
"""
import ast
import glob
import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def one(pattern):
    hits = glob.glob(pattern)
    assert len(hits) == 1, (pattern, hits)
    return hits[0]


FRAG = one(os.path.join(HERE, "*来料片段*.html"))
R403 = one(os.path.join(BASE, "04_*", "本项目_*", "数据", "TUFT-r403_*.json"))
R437 = one(os.path.join(BASE, "04_*", "本项目_*", "判定", "判定_TUFT-r437_*.md"))
R413 = one(os.path.join(BASE, "04_*", "算法联盟_*", "判定_TUFT-r413-*.md"))
OUT_JSON = os.path.join(HERE, "_root_fragment_meta.json")
REPORT_PATH = os.path.join(HERE, "_root_fragment_meta_report.txt")

with open(FRAG, encoding="utf-8") as f:
    src = f.read()
md5 = hashlib.md5(src.encode("utf-8")).hexdigest()
nbytes = len(src.encode("utf-8"))

gates = []


def add(gid, kind, exp, act, ok, note=""):
    gates.append({"id": gid, "kind": kind, "exp": str(exp), "act": str(act),
                  "ok": bool(ok), "note": note})


tree = ast.parse(open(os.path.abspath(__file__), encoding="utf-8").read())
bad_import = []
bad_call = []
hardcoded_ok = []
for node in ast.walk(tree):
    if isinstance(node, ast.Import) and any(a.name in ("numpy", "sympy") for a in node.names):
        bad_import.extend(a.name for a in node.names if a.name in ("numpy", "sympy"))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
        bad_call.append(node.func.id)
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id == "add" and len(node.args) >= 5):
        v = node.args[4]
        if isinstance(v, ast.Constant) and isinstance(v.value, bool):
            hardcoded_ok.append(getattr(node.args[0], "value", "?"))
add("G00-ast", "gate", "AST 前置：无禁库、无 eval/exec、ok 不写死",
    "bad_import=%s bad_call=%s hardcoded_ok=%s" % (bad_import, bad_call, hardcoded_ok),
    (not bad_import and not bad_call and not hardcoded_ok),
    "守卫自身可翻红")

# F1 片段完整性
has_doctype = src.lstrip().startswith("<!DOCTYPE html>")
has_close = "</html>" in src and "</head>" in src
incomplete = has_doctype and not has_close
add("F1-fragment-incomplete", "gate", "检测到来料为不完整片段：有 DOCTYPE、无 </head></html>",
    "doctype=%s close=%s incomplete=%s bytes=%d" % (has_doctype, has_close, incomplete, nbytes),
    incomplete,
    "这是片段事实门，不是来料错误；正文公式未到场，禁止公式级复算")

# F2 标题层宣称
m = re.search(r"<title>(.*?)</title>", src)
title = m.group(1) if m else ""
overclaim = ("四力统一" in title) and ("ROOT本源核心公式" in title)
add("F2-title-overclaim", "gate", "标题层出现四力统一 + ROOT 本源核心公式的完成式宣称",
    "title=%s overclaim=%s" % (title, overclaim),
    overclaim,
    "只报标题层事实；不把可视化标题当物理证据")

# F3 MathJax 已载但无公式正文
tex_markers = [t for t in ("$$", "\\[", "\\(", "\\frac", "\\begin{") if t in src]
mathjax_loaded = "mathjax" in src.lower()
no_formula = mathjax_loaded and not tex_markers
add("F3-no-formula-body", "gate", "已载入 MathJax 但片段内没有任何 TeX 公式正文",
    "mathjax=%s tex_markers=%s no_formula=%s" % (mathjax_loaded, tex_markers, no_formula),
    no_formula,
    "MathJax 脚本标签不是公式；不能据 CDN 引用推断核心公式内容")

# F4 红线锚点
with open(R403, encoding="utf-8") as f:
    r403_txt = f.read()
with open(R437, encoding="utf-8") as f:
    r437_txt = f.read()
with open(R413, encoding="utf-8") as f:
    r413_txt = f.read()
anchors = {
    "r403_no_four_force_gut": "NO-CORRECT-FOUR-FORCE-GUT" in r403_txt,
    "r413_pseudo_plus1": "PLUS-ONE-IS-PSEUDO-COST" in r413_txt,
    "r437_unique_exit": "UNIQUE-EXIT-9FOLD-REAFFIRMED" in r437_txt,
}
add("F4-redline-anchors", "gate", "最新判负链锚点仍在：r403/r413/r437 未被本片段改写",
    "anchors=%s" % anchors,
    all(anchors.values()),
    "按纪律取最新重定价；本片段不销任何既有债务")

# F5 无内联 3D 实现
inline = [s for s in re.findall(r"<script(?:\s[^>]*)?>([\s\S]*?)</script>", src) if s.strip()]
add("F5-no-inline-3d", "gate", "片段只有外链脚本，没有内联 3D 实现代码",
    "inline_blocks=%d" % len(inline),
    len(inline) == 0,
    "three.js 与 MathJax 只是 CDN 引用；3D 场景与公式绑定尚未到场")

# 反噬：注入闭合标签使 F1 翻红
patched_close = src + "\n</head>\n<body></body>\n</html>\n"
incomplete_patched = patched_close.lstrip().startswith("<!DOCTYPE html>") and not (
    "</html>" in patched_close and "</head>" in patched_close)
add("N1-inject-close-neg", "neg", "注入 </head></html> 后片段不完整检测必须翻红",
    "before=%s after=%s" % (incomplete, incomplete_patched),
    incomplete and not incomplete_patched,
    "反噬：若补上闭合仍判片段，则完整性检测无判别力")

# 反噬：注入假公式使 F3 翻红
patched_tex = src + "\n$$E = m c^2$$\n"
tex_patched = [t for t in ("$$", "\\[", "\\(", "\\frac", "\\begin{") if t in patched_tex]
no_formula_patched = mathjax_loaded and not tex_patched
add("N2-inject-formula-neg", "neg", "注入假 TeX 公式后无公式正文检测必须翻红",
    "before=%s after=%s tex_after=%s" % (no_formula, no_formula_patched, tex_patched),
    no_formula and not no_formula_patched,
    "反噬：若注入公式仍判无公式，则 F3 是恒绿装饰")

repair = {
    "suggested_title": "ROOT 本源核心公式 3D 可视化（宣称级演示 · 四力统一未证实）",
    "suggested_banner": "本页为可视化演示，不构成四力统一已被实验证实的证据；独立实验预言 0。判负链见 r403 / r410 / r413 / r437。",
    "required_before_upgrade": [
        "完整 HTML 正文与 3D 实现源码",
        "核心公式逐字文本、锚点文件与机器可读版本",
        "可翻覆判据及正负对照",
        "外部一手实验读数（含双侧误差棒）",
    ],
}

n_gate = sum(1 for g in gates if g["kind"] == "gate")
n_neg = sum(1 for g in gates if g["kind"] == "neg")
n_identity = sum(1 for g in gates if g["kind"] == "identity")
failed = [g["id"] for g in gates if not g["ok"]]
if failed:
    verdict = "ROOT-FRAGMENT-AUDIT-FAIL--" + "-".join(failed)
else:
    verdict = ("ROOT-FRAGMENT--INCOMPLETE-CONFIRMED--TITLE-OVERCLAIM-DETECTED--"
               "NO-FORMULA-BODY--NO-INLINE-3D--REDLINE-ANCHORS-OK--"
               "NO-UPGRADE--NO-INDEPENDENT-PREDICTION--NO-UFT-CLAIM")

result = {
    "subject": "ROOT 本源核心公式 3D 可视化片段级来料审计",
    "fragment": {"path": os.path.basename(FRAG), "md5": md5, "bytes": nbytes,
                 "title": title, "incomplete": incomplete},
    "verdict": verdict,
    "counts": {"gate": n_gate, "neg": n_neg, "identity": n_identity, "failed": len(failed)},
    "independent_prediction_count": 0,
    "redline_anchors": anchors,
    "repair_suggestions": repair,
    "gates": gates,
}
with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, ensure_ascii=False, indent=2, default=str)

lines = [
    "ROOT 本源核心公式 3D 可视化 · 片段级来料审计",
    "=" * 72,
    "判词: " + verdict,
    "门数: gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(failed)),
    "片段: %s | md5=%s | bytes=%d" % (os.path.basename(FRAG), md5, nbytes),
    "独立预言计数: 0",
    "-" * 72,
]
for g in gates:
    lines.append("[%s] %-28s %-8s exp=%s | act=%s // %s" % (
        "PASS" if g["ok"] else "FAIL", g["id"], g["kind"],
        g["exp"], g["act"], g["note"]))
lines.extend([
    "-" * 72,
    "修复标题: " + repair["suggested_title"],
    "建议横幅: " + repair["suggested_banner"],
    "红线锚点: " + json.dumps(anchors, ensure_ascii=False),
    "-" * 72,
    "纯标准库 ; 全确定性 ; 不占RID ; 不与UFT链或ROOT V128八册链相加",
])
with open(REPORT_PATH, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines) + "\n")

print(verdict)
print("gate=%d neg=%d identity=%d failed=%d" % (n_gate, n_neg, n_identity, len(failed)))
for g in gates:
    if not g["ok"]:
        print("FAIL:", g["id"], g["exp"], g["act"])
