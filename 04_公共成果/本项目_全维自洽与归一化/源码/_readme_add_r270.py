# -*- coding: utf-8 -*-
"""
r270 README 注册（幂等 · 每次重新读盘 · 落盘后读回验证）

★铁律（r264 事故而来，本脚本严格遵守）
--------------------------------------
1. **锚点串必须含本卷 RID**：判定「本卷条目是否已存在」一律用 `TUFT-r270_` /
   `判定_TUFT-r270_` / `- **r270（` / `### r270 ·` / `· r270 卷）**`，
   禁止用他人也可能写的通用前缀做 replace_first。
2. **先判定存在再分流**：已存在 ⇒ 原地刷新；不存在 ⇒ 插入。**禁止把插入与刷新混成一步。**
3. **不得回溯改写他人卷**：绝不触碰任何含他人 RID 的行（不刷新他人「下轮」指针）。
4. **落盘后再从磁盘读回验证一次**（共享 README 是并行会话竞态文件）。
5. 判定册链接一律写 `数据/`（不写 `判定/`，否则死链）。
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
README = os.path.join(ROOT, "README.md")

RID = "r270"
STEM = ("可机检验收规范层_统一场论验收器十二条必要条件与正负对照"
        "及GR_SM_TUFT三对象实跑_精算与可视化_2026-10-31")
PY = "TUFT-r270_" + STEM + ".py"
HTML = "TUFT-r270_" + STEM + ".html"
VERDICT = "判定_TUFT-r270_" + STEM + ".md"
DJ = "TUFT-r270_" + STEM + ".json"
DM = "TUFT-r270_" + STEM + ".md"
DR = "TUFT-r270_" + STEM + "_report.txt"

# ---------------- 待插入内容（拼接而非 % 格式化，彻底避开字面 % 坑） ----------------
LINE_SRC = (
    "│   ├── " + PY + "  # 新增（**r270 · 2026-10-31**）：**可机检验收规范层首卷（★新层 · "
    "本线「立」轴）—— 不重复做跨卷总账，而是把 r243–r269 的教训凝成一台「统一场论验收器」**："
    "12 条可机检必要条件（量纲封闭 / 单位不变 / 非定义恒等式 / 内部一致 / 数值可复现 / "
    "自由度匹配 / 选择定则自洽 / 非零比特 / 低能极限纯度 / 参数预算 / 符号单调 / 实验相容），"
    "每条配**正对照**（GR·SM 必须通过）与**负对照**（本库已判死声称必须失败），"
    "再对 GR / SM / TUFT 实跑（条目 **31**：PASS 26 / FAIL 1 / INFO 4；"
    "**控制组 24/24**、**守卫 13/13**、退出码 0）。"
    "★三条承重：①**判据有牙齿**——正负对照 12/12 齐备，缺一即判 INFO 不计分；"
    "②**不针对 TUFT**——GR 11/12（1 INFO）、SM 12/12、TUFT 0/12；"
    "③**自杀集与可修订集分离**——可修订 5 条 {G2,G4,G5,G7,G11}、改即自杀 7 条 "
    "{G1,G3,G6,G8,G9,G10,G12}。★修复定价双档：严格 EMPTY 4095 / SUICIDE 1 / SURVIVE 0；"
    "宽松 EMPTY 3968 / SUICIDE 127 / SURVIVE 1 ⇒ 按 r262/r265 先例**不占度数**，候选 37 只登记。"
    "★对靶有利 8 条单列（F1–F8）。★背景：真机读回前卷判定册 **27 册**（r243–r269），"
    "只做名录与指针（条目不可相加）。"
)

LINE_VER = (
    "├── " + VERDICT + "  # 新增（**r270 · 2026-10-31**）：可机检验收规范层判定册 —— "
    "§一句话判词 · §三条承重（判据有牙齿 / 不针对 TUFT / 自杀集与可修订集分离）· "
    "§对靶有利 F1–F8 · §结算（条目 31 = PASS 26 / FAIL 1 / INFO 4；控制组 24/24；守卫 13/13；"
    "rc=0）· §取号（**连改三次**：r266 被两个并行会话抢占 ⇒ r267 亦被抢占 ⇒ "
    "r268/r269 亦已被占 ⇒ 取 r270。**下轮从 r271 复查起**）· §性质界定（空 ≠ 错；规范卷非新指控）"
)

LINE_ITEM = (
    "- **r270（2026-10-31）· 可机检验收规范层：统一场论验收器 12 条必要条件与正负对照，"
    "GR / SM / TUFT 三对象实跑（★新层首卷 · 本线「立」轴）**：把 r243–r269 的教训凝成一台"
    "**验收器**——12 条可机检必要条件，每条配正对照（GR·SM 必须通过）与负对照"
    "（本库已判死声称必须失败）。条目 **31**（**PASS 26 / FAIL 1 / INFO 4**），"
    "**控制组 24/24**，**守卫 13/13**，rc=0；源码 [`TUFT-r270_…py`](源码/" + PY + ")；"
    "判定册 [`…md`](数据/" + VERDICT + ")；数据 [`…json`](数据/" + DJ + ") / "
    "[`…_report.txt`](数据/" + DR + ")；**交互可视化** [`…html`](源码/" + HTML + ")。"
    "★★**判据有牙齿**：正负对照 12/12 齐备，缺一即零判别力。★★**不针对 TUFT**："
    "GR 11/12（1 INFO）、SM 12/12、TUFT **0/12**。★★**自杀集 vs 可修订集**：可修订 5 条、"
    "改即自杀 7 条 ⇒ 严格档 SURVIVE 0、宽松档 SURVIVE 1 ⇒ **不占度数**。"
    "★**真机读回前卷判定册 27 册**，只做名录与指针，**条目不可与 r142–r269 相加**。"
)

LINE_DISAMBIG = (
    "> **编号消歧（2026-10-31 撞号第 11 次 · r270 卷）**：本卷**连改三次**——"
    "16:11 实测 r266/r267/r268 三树全空 ⇒ 拟取 r266；16:19 复查发现 "
    "**r266 已被两个并行会话抢占**（16:19:34 落齐四件套《力的大统一方程层》；"
    "16:19:50 另一会话正在起草《统一场论完成度终局验收层》）⇒ 第一次改号 r266→r267；"
    "16:33 复查发现 **r267 亦被抢占**（同一会话 16:33:37 落齐四件套）⇒ 第二次改号 r267→r268；"
    "16:34 复查发现 **r268（ROOT-V5.0 融合审计）、r269（候选比例多元性定理）亦均已被占**，"
    "实测 r270/r271/r272 三树全空 ⇒ 第三次改号 **r268→r270**。未改写他人任何字节"
    "（误落在 r267 树内的本卷草稿已移入 `源码/_scratch_dead/`）。"
    "**下轮从 r271 复查起**（★「起草时为空」≠「落盘时仍为空」，且度数须经守卫机读核定）。"
)

SEC_TITLE = ("### r270 · 2026-10-31 · 可机检验收规范层：统一场论验收器十二条必要条件、"
             "正负对照与 GR·SM·TUFT 三对象实跑（★新层首卷 · 本线「立」轴）")


def rd(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def has(lines, needle):
    return any(needle in l for l in lines)


def idx_of(lines, pred):
    for i, l in enumerate(lines):
        if pred(l):
            return i
    return -1


def main():
    txt = rd(README)
    lines = txt.split("\n")
    print("README lines (fresh) = %d" % len(lines))

    changed = False

    # ---- 1) 源码树：插到「最近一条 源码树 TUFT-r2xx_…py」之前 ----
    if has(lines, "TUFT-r270_" + STEM + ".py"):
        print("[1] 源码树：已存在，跳过")
    else:
        k = idx_of(lines, lambda l: l.startswith("│   ├── TUFT-r2") and ".py" in l)
        if k < 0:
            print("[1] 源码树：FAIL 找不到插入点")
            return 2
        lines.insert(k, LINE_SRC)
        changed = True
        print("[1] 源码树：插入到 L%d 之前" % (k + 1))

    # ---- 2) 判定树 ----
    if has(lines, "判定_TUFT-r270_" + STEM + ".md"):
        print("[2] 判定树：已存在，跳过")
    else:
        k = idx_of(lines, lambda l: l.startswith("├── 判定_TUFT-r2"))
        if k < 0:
            print("[2] 判定树：FAIL 找不到插入点")
            return 2
        lines.insert(k, LINE_VER)
        changed = True
        print("[2] 判定树：插入到 L%d 之前" % (k + 1))

    # ---- 3) 编号消歧（锚点含本卷 RID，绝不通用前缀） ----
    if has(lines, "· r270 卷）**"):
        print("[3] 编号消歧：已存在，跳过")
    else:
        k = idx_of(lines, lambda l: l.startswith("> **编号消歧（"))
        if k < 0:
            print("[3] 编号消歧：FAIL 找不到插入点")
            return 2
        lines.insert(k, LINE_DISAMBIG)
        changed = True
        print("[3] 编号消歧：插入到 L%d 之前" % (k + 1))

    # ---- 4) 增量章条目 ----
    if has(lines, "- **r270（2026-10-31）"):
        print("[4] 增量章条目：已存在，跳过")
    else:
        k = idx_of(lines, lambda l: l.startswith("- **r2") and "（2026-10-31）" in l)
        if k < 0:
            print("[4] 增量章条目：FAIL 找不到插入点")
            return 2
        lines.insert(k, LINE_ITEM)
        changed = True
        print("[4] 增量章条目：插入到 L%d 之前" % (k + 1))

    # ---- 5) 增量章详节 ----
    if has(lines, "### r270 · 2026-10-31 · 可机检验收规范层"):
        print("[5] 详节：已存在，跳过")
    else:
        k = idx_of(lines, lambda l: l.startswith("### r2") and "· 2026-10-31" in l)
        if k < 0:
            print("[5] 详节：FAIL 找不到插入点")
            return 2
        block = [
            SEC_TITLE,
            "",
            "- **产物**：源码 [`TUFT-r270_…py`](源码/" + PY + ") / [`…html`](源码/" + HTML + ")；"
            "数据 [`…json`](数据/" + DJ + ") / [`…md`](数据/" + DM + ") / [`…_report.txt`](数据/" + DR + ")；"
            "判定册 [`判定_…md`](数据/" + VERDICT + ")；runner `源码/_run_r270.py` → `源码/_out_r270.txt`",
            "- **复现**：`python -X utf8 源码\\_run_r270.py` ⇒ **rc=0**，条目 **31**"
            "（**PASS 26 / FAIL 1 / INFO 4**），**控制组 24/24**，**守卫 13/13**",
            "- **★★ 承重①：判据有牙齿（正负对照 12/12 齐备）**：每条判据同时给出"
            "「已确立理论必须通过」与「本库已判死声称必须失败」两个端点；缺任一端即零判别力，"
            "本卷判 INFO 不计分。正对照一律**独立机算**（不转抄教科书）："
            "Einstein 场方程量纲元组、c/ℓ_P 三单位扫描、水星/金星/地球三星进动、"
            "λ̄_C 双路径（ℏ/m_ec ↔ α·a₀）、α 由 CODATA 重算（rel 1e-10 量级）、"
            "SU(3) 8↔8、sphaleron 不动点模拟、PPN γ 偏折、Schwarzschild 弱场数值求导、"
            "Schwinger α/(2π)、α_s 单调性、水星进动 z 值。",
            "- **★★ 承重②：不针对 TUFT**：同一台验收器上 **GR 11/12（1 INFO）**、"
            "**SM 12/12**、**TUFT 0/12**。TUFT 的 12 条 FAIL 每条标注来源卷"
            "（r248/r264/r258/r250/r245/r262/r265/r249/r243），不许无据指控。",
            "- **★★ 承重③：自杀集与可修订集分离**：可修订 5 条 {G2,G4,G5,G7,G11}"
            "（改单位口径、统一内部陈述、修正表格、改正选择定则、纠正符号）；"
            "「改即自杀」7 条 {G1,G3,G6,G8,G9,G10,G12}（改主方程 / 需新物理 / 改几何结构 / "
            "需真预言 / 改低能极限 / 需内生出新数 / 与实验和解 ⇒ 等于放弃原主张）。",
            "- **★ 双档修复定价**：严格档（须满足全部 12 条）EMPTY 4095 / SUICIDE 1 / "
            "SURVIVE 0；宽松档（只修 5 条可修订项）EMPTY 3968 / SUICIDE 127 / SURVIVE 1。"
            "按 r262/r265 先例（SURVIVE>0 ⇒ 判「靶未达成」、不占度数链），"
            "**本卷不占度数**，候选 37 仅登记不占位。",
            "- **★ 对靶有利八条（F1–F8，如实登记不抵消）**：λ 列 8/8 与 ħc/m 相符 · "
            "b=αρ 与 τ=ακ 8/8 成立 · 电子行 ω²=c²(κ²+τ²) 精确成立 · 主动承认 m=ħω/c² 是定义式 · "
            "B=(28/79)(B−L) 群论系数完全正确 · η_B 与 Planck 2018 相符 0.327% · "
            "V9.41 主动修正跨量纲伪失配 · r261 靶《全维分析》8/8 零 FAIL。",
            "- **★ 背景名录**：真机读回前卷判定册 **27 册**（r243–r269），逐册取 sha256 前 12 位、"
            "层名、条目/控制组/守卫、判词首句；**只并列、不相加**（守卫 G7 机检："
            "各册条目数之和不得泄漏进任何条目文本）。",
            "- **★ 性质界定**：本卷是「规范」不是「新指控」——12 条均为任何统一场论必须满足的"
            "必要条件；GR/SM 全过证明判据不是定罪工具。**空 ≠ 错**：GR 的 G7 判 INFO 而非 FAIL。",
            "- **★ 分层（不可相加）**：本卷为**可机检验收规范层**，与 r243–r269 任何一卷"
            "都不是同一层；**条目不可与 r142–r269 相加**。",
            "- **取号（撞号第 11 次 · 连改三次）**：r266→r267→r268→**r270**"
            "（r266/r267/r268/r269 均被并行会话抢占）。"
            "**下轮从 r271 复查起**（★落盘前必须再实测一次，且度数须经守卫机读 README 核定）。",
            "- **开发期自抓 4 处**：`calc_g2` 漏返回 `ok_pos/ok_neg` 致判据 G2 误判 FAIL · "
            "G9 数值求导参照值符号写反（应为径向向内 −GM/r²）· "
            "「对靶有利」条目 id 与破组 A1–A3 撞号（改 F1–F8 并新增守卫 G12 查 id 唯一）· "
            "HTML 模板内 CSS `width:100%` 与 `%` 格式化冲突（改占位符 `@@…@@` 替换）。",
            "- **治理**：本卷为规范卷（无独立来料靶，sha256 不适用）；未改 `verify.py`；"
            "未跑 `refresh_catalog.py`；**条目不可与 r142–r269 相加**。",
            "",
            "",
        ]
        lines[k:k] = block
        changed = True
        print("[5] 详节：插入到 L%d 之前（%d 行）" % (k + 1, len(block)))

    if not changed:
        print("\nNo write needed (all anchors already present).")
        return 0

    wr(README, "\n".join(lines))

    # ---- 落盘后从磁盘读回验证 ----
    print("\n==== POST-WRITE VERIFY (fresh read) ====")
    L2 = rd(README).split("\n")
    print("lines after write = %d" % len(L2))
    checks = [
        ("源码树 计数==1", sum(1 for l in L2 if l.startswith("│   ├── TUFT-r270_") and ".py  # 新增" in l) == 1),
        ("判定树 计数==1", sum(1 for l in L2 if l.startswith("├── 判定_TUFT-r270_")) == 1),
        ("编号消歧 计数==1", sum(1 for l in L2 if "· r270 卷）**" in l) == 1),
        ("增量章条目 计数==1", sum(1 for l in L2 if l.startswith("- **r270（2026-10-31）")) == 1),
        ("详节标题 计数==1", sum(1 for l in L2 if l.startswith("### r270 · 2026-10-31 · 可机检验收规范层")) == 1),
        ("数据链接写 数据/（无死链）", sum(1 for l in L2 if "](判定/判定_TUFT-r270" in l) == 0),
        ("未污染他人 r267/r268/r269 详节",
         sum(1 for l in L2 if l.startswith("### r267 · ")) == 1 and
         sum(1 for l in L2 if l.startswith("### r268 · ")) == 1 and
         sum(1 for l in L2 if l.startswith("### r269 · ")) == 1),
    ]
    allok = True
    for name, v in checks:
        print("  [%s] %s" % ("OK " if v else "BAD", name))
        allok &= v
    print("\nRESULT = %s" % ("ALL OK" if allok else "PROBLEM"))
    print("(提示：并行会话可能整篇覆盖，收口前请再跑一次本脚本确认)")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
