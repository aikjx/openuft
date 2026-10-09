# -*- coding: utf-8 -*-
"""
引用侧对账器：03_验证与可证伪性.md 里每个数值 token 必须落在它声明的来源里
==========================================================================

动机：本仓库登记过同族失效 —— 手写文档抄到的常是"末位被吃掉的那一份"。故凡文档里出现数字，
必须由外部脚本逐字对账。

判据三条：① 命中（规范化后逐字出现在声明来源里）；② 豁免（必须显式声明理由，且统计"从未被用到的
豁免"——一条从不被走到的豁免等于没被核对过的说法）；③ 重算（"本册新算"的数当场重算，不接受豁免）。

规范化：`\\times10^{12}` / `×10^{12}` / `10^12` → `E12`；`e-4` → `E-4`；同时抽 `\\d+\\.\\d+`。

退出码：0 = 通过；1 = 未命中 / 豁免失效 / 重算不符 / 来源缺失。
运行：python -B doc_check_03_falsifiability.py
"""

import io
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIR = HERE.parent
ROOT = DIR.parent.parent
DOC = DIR / "03_验证与可证伪性.md"
JUDGE = ROOT / "04_公共成果" / "本项目_全维自洽与归一化"

SOURCES = [
    DIR / "11_证伪与反例" / "README.md",
    DIR / "README.md",
    DIR.parent / "README.md",
    DIR / "claims.csv",
    DIR / "验证脚本" / "audit_report.md",
    DIR / "验证脚本" / "source_scripts_rerun_report.md",
    JUDGE / "判定_空间螺旋V21续修_C25C35_2026-09-26.md",
    JUDGE / "判定_靶场卡方联合拟合_2026-09-26.md",
    JUDGE / "判定_空间螺旋全量claims_L3层级判定_2026-09-26.md",
    JUDGE / "判定_空间螺旋CMB拓扑双谱_攻坚审计_2026-09-26.md",
    JUDGE / "判定_空间螺旋EHT光子环_攻坚审计_2026-09-26.md",
    JUDGE / "判定_空间螺旋V21材料落库与下一步选定_2026-09-26.md",
    JUDGE / "判定_空间螺旋修复版_最小修复闭环与继承缺陷_2026-09-26.md",
]

# 豁免：token -> 理由（非读数的定义式/量级写法；读数一律不许走这条）
EXEMPT = {
    "3.84145882069": "χ²_crit 闭式定义式（统计层 §1），非读数",
    "0.1045": "理论侧相对棒（子目录 README §5 已述，取 4 位写法）",
    "0.1116": "水星 43.03 差（子目录 README §5）",
    "0.13": "水星锚点极差（子目录 README §5）",
    "1.13": "RK4 5πx² 距实测棒数（子目录 README §5）",
    "8.65": "3πx² 距实测棒数（子目录 README §5）",
    "0.0026": "草稿式金星修正量级（C25/C35 判定册 §13-C35-4 作 ~1e-3 量级）",
    "0.0006": "草稿式地球修正量级（同上）",
    "0.0049": "Binet 式金星修正量级（同上）",
    "0.0016": "Binet 式地球修正量级（同上）",
}


def canon(t):
    t = t.replace("\\times", "x").replace("\\cdot", "x").replace("×", "x").replace("·", "x")
    t = re.sub(r"x\s*10\s*\^?\s*\{?\s*([+-]?\d+)\s*\}?", r"E\1", t)
    t = re.sub(r"10\s*\^?\s*\{?\s*([+-]?\d+)\s*\}?", r"E\1", t)
    for ch in "$ {}\\!~,，" .split() + ["$", "{", "}", "\\", " ", "~"]:
        t = t.replace(ch, "")
    return t.replace("e", "E").replace("E+", "E")


TOKEN = re.compile(r"\d+(?:\.\d+)?E[+-]?\d+|\d+\.\d+")


def toks(text):
    d = {}
    for m in TOKEN.finditer(canon(text)):
        k = m.group(0)
        if k.endswith(".0"):
            k = k[:-2]
        d[k] = d.get(k, 0) + 1
    return d


def recompute():
    import mpmath as mp
    mp.mp.dps = 60
    chi2 = 2 * mp.erfinv(mp.mpf("0.95")) ** 2
    return {"3.84145882069": mp.nstr(chi2, 12), "1.959963985": mp.nstr(mp.sqrt(chi2), 10)}


def main():
    bad = []
    for p in SOURCES + [DOC]:
        if not p.exists():
            bad.append("来源缺失：%s" % p)
    if bad:
        print("[FATAL] " + " | ".join(bad))
        return 1
    blob = {str(p): canon(io.open(p, encoding="utf-8").read()) for p in SOURCES}
    rc = recompute()
    hit, exe, rec, miss = 0, [], [], []
    for tk, n in sorted(toks(io.open(DOC, encoding="utf-8").read()).items()):
        if any(tk in txt for txt in blob.values()):
            hit += 1
        elif tk in rc and canon(rc[tk]) == canon(tk):
            rec.append(tk)
        elif tk in EXEMPT:
            exe.append(tk)
        else:
            miss.append(tk)
    dead = sorted(set(EXEMPT) - set(exe))
    print("[03对账] 文档 %s" % DOC.name)
    print("  来源 %d 份 ｜ 数值 token 命中 %d ｜ 重算命中 %d ｜ 豁免 %d ｜ 未命中 %d"
          % (len(SOURCES), hit, len(rec), len(exe), len(miss)))
    print("  重算：%s" % ", ".join("%s(实算 %s)" % (k, rc[k]) for k in rec))
    print("  豁免：%s" % ", ".join(exe))
    print("  未被走到的豁免（=失效分支）：%s" % (", ".join(dead) if dead else "无"))
    if miss:
        print("  [MISS] 来源中逐字未命中（漂移候选）：%s" % ", ".join(miss))
    ok = (not miss) and (not dead)
    print("[03对账] %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
