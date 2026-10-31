# -*- coding: utf-8 -*-
"""幂等注册 r273 于 README 四处（src/jud/cpt/full 四树），位于 r272 锚点之后。"""
import io
import os
import shutil

BASE = r"D:/a10/aikjx/code/my_lib/openuft/04_公共成果/本项目_全维自洽与归一化"
README = os.path.join(BASE, "README.md")
SCRATCH = os.path.join(BASE, "_scratch")
BACKUP = os.path.join(SCRATCH, "_README_before_r273_reg.md")
RID = "r273"

SLUG = ("TUFT-r273_四力本源参数精算层_统一势模板标准耦合重标定及qWqπ数值核验_"
        "精算与可视化_2026-10-31")
JUD = "判定_" + SLUG + ".md"

# 四树 r272 锚点前缀（精确，禁通用前缀）
ANCHORS = {
    "src": "│   ├── TUFT-r272_",
    "jud": "├── 判定_TUFT-r272_",
    "cpt": "- **r272（",
    "ful": "### r272 ·",
}

def build_entries():
    # src 树条目
    src = ("│   ├── %s.py  # 新增（**r273 · 2026-10-31**）：**四力本源参数精算层"
           "（V9.17 第二十三章）**—— 从 CODATA/PDG 常数第一性独立重算四力「本源参数」"
           "q_G/q_EM/q_W/q_π 与四力标度；审计书「本源参数全表数值化」声称。"
           "条目 8（PASS 8 / FAIL 0），**控制组 3/3**、**守卫 6/6**、rc=0。"
           "★承重：四力荷全高保真复现（q_G=7.685e-20、q_EM=0.08542、q_W=0.06512、"
           "q_π=0.02037；F_E=230.71 N / F_G=1.87e-34 N / F_W=1.637e7 N / F_π=4.516 N，"
           "与书 4e-3 内一致）。★结构判词：『本源参数全表数值化』= 已知 SM 耦合的改记，"
           "非第一性推导——q_W=√(G_F m_W²/4π√2)=g/√(32π)、q_π=√(f²(m_π/2m_p)²)，"
           "G_F/f²/α/m 全外输（B03 维持）⇒ 内生推导=0、判别性 0（与 r266 Yukawa 模板重包装 / "
           "r272 LW 重算同构）。★定价 2^8=256：SURVIVE 256 / SUICIDE 0 ⇒ "
           "**SURVIVE>0 ⇒ 不占度数**；候选 37 度但不计。") % SLUG
    # jud 树条目
    jud = ("├── %s  # 新增（**r273 · 2026-10-31**）：四力本源参数精算层判定册 —— "
           "§结论 · §逐条判定表（8 声称全 PASS）· §控制组 3/3（CG3 结构对照证判别力）· "
           "§守卫 6/6 · §结构判词（SM 耦合改记 / 判别性 0）· §定价（SURVIVE>0，不占度）。") % JUD
    # compact 树条目
    cpt = ("- **r273（2026-10-31）· 四力本源参数精算层：统一势模板匹配、q_G/q_EM/q_W/q_π "
           "与四力标度独立重算、判别性 0（★新层）**：审计第二十三章 V9.17 四力本源参数全表。"
           "条目 8（PASS 8 / FAIL 0），控制组 3/3，守卫 6/6，rc=0；源码 [`TUFT-r273_…py`](源码/%s.py)；"
           "判定册 [`…md`](数据/%s)；数据 [`…json`](数据/%s.json) / "
           "[`…_report.txt`](数据/%s_report.txt)。★★**四力荷全高保真复现**"
           "（q_G=7.685e-20、q_EM=0.08542、q_W=0.06512、q_π=0.02037；"
           "F_E=230.71 N / F_G=1.87e-34 N / F_W=1.637e7 N / F_π=4.516 N，与书 4e-3 内一致）。"
           "★★**结构判词：『本源参数全表数值化』= 已知 SM 耦合的改记，非第一性推导**——"
           "q_W=√(G_F m_W²/4π√2)=g/√(32π)、q_π=√(f²(m_π/2m_p)²)，G_F/f²/α/m 全外输（B03 维持）"
           "⇒ 内生推导=0、判别性 0（与 r266 Yukawa 模板重包装 / r272 LW 重算同构）。"
           "★定价 2^8=256：SURVIVE 256 / SUICIDE 0 ⇒ **SURVIVE>0 ⇒ 不占度数**；候选 37 度但不计。") % (
           SLUG, JUD, SLUG, SLUG)
    # full 树条目
    ful = ("### r273 · 2026-10-31 · 四力本源参数精算层：统一势模板标准耦合重标定及 "
           "q_W/q_π 数值核验（★新层）")
    return {"src": src, "jud": jud, "cpt": cpt, "ful": ful}

def main():
    text0 = io.open(README, "r", encoding="utf-8", newline="").read()
    if "TUFT-r273_" in text0:
        print("r273 已存在，跳过注册（幂等）。")
        return
    # 备份仅首次
    if not os.path.exists(BACKUP):
        shutil.copy2(README, BACKUP)
        print("备份:", BACKUP)
    # 保留行尾，逐行处理
    lines = text0.splitlines(keepends=True)
    ending = "\r\n" if lines[0].endswith("\r\n") else "\n"
    entries = build_entries()
    inserts = []  # (index, tree)
    for tree, anchor in ANCHORS.items():
        idx = None
        for i, ln in enumerate(lines):
            if ln.startswith(anchor):
                idx = i
        if idx is None:
            raise SystemExit("锚点未找到: " + anchor)
        inserts.append((idx, tree))
    # 从后往前插入，保持索引
    for idx, tree in sorted(inserts, reverse=True):
        lines.insert(idx + 1, entries[tree] + ending)
    out = "".join(lines)
    io.open(README, "w", encoding="utf-8", newline="").write(out)
    # 验证
    text1 = io.open(README, "r", encoding="utf-8", newline="").read()
    counts = {
        "src": text1.count("TUFT-r273_"),
        "jud": text1.count("判定_TUFT-r273_"),
        "cpt": text1.count("**r273（"),
        "ful": text1.count("### r273 ·"),
    }
    dead = text1.count("](判定/判定_TUFT-r273")
    print("注册后四树计数:", counts)
    print("疑似死链:", dead)
    ok = all(v >= 1 for v in counts.values()) and dead == 0
    print("注册结果:", "OK" if ok else "CHECK")

if __name__ == "__main__":
    main()
