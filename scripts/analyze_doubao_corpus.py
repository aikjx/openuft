# -*- coding: utf-8 -*-
"""
豆包对话 · 全维分析整理 → 写入 openuft
========================================
解析 `code/豆包/自动化保存对话脚本/exports/doubao/<标题>/` 下所有已导出会话（优先 .jsonl，
含 role/content/created_at/exported_at 元数据；缺则回退 .md），按多维度做"全维分析整理"，
并把结构化结果写入 openuft 的专用卷 `91_豆包对话全维分析整理/`。

维度（对齐 openuft 卷结构）：
  D01 统一场方程与主方程       -> 07_统一场方程
  D02 TUFT/OpenUFT 体系与版本  -> 02_TUFT_来源
  D03 螺旋几何与拓扑本源       -> 01_独立体系
  D04 量子引力与标准模型统一   -> 06_统一体系层 / 07
  D05 参数拟合与精算审计       -> 04_公共成果/全维自洽与归一化
  D06 文献与全球研究路线       -> 05_全球研究
  D07 企业落地与产业应用       -> 01_独立体系 / 99_待整理资料
  D08 代码与工程实现           -> scripts / 实现方式
  D09 关系体系图与跨体系       -> 03_跨体系研究
  D10 数学基础与数论           -> 02_共享基础

可复跑：每次运行覆盖写出生目录，增量下载完成后再跑一遍即得"全维"覆盖。
用法：
  python analyze_doubao_corpus.py [--exports DIR] [--out DIR] [--limit N]
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# ----------------------------------------------------------------------------
# 路径默认值
# ----------------------------------------------------------------------------
DEFAULT_EXPORTS = r"D:\a10\aikjx\code\my_lib\code\豆包\自动化保存对话脚本\exports\doubao"
DEFAULT_OUT = r"D:\a10\aikjx\code\my_lib\openuft\91_豆包对话全维分析整理"

# ----------------------------------------------------------------------------
# 维度定义（关键词命中计分；中文无词边界，用子串计数，权重可调）
# ----------------------------------------------------------------------------
DIMENSIONS = [
    ("D01", "统一场方程与主方程", "07_统一场方程", [
        "统一场", "场方程", "主方程", "作用量", "拉格朗日", "变分", "诺特定理",
        "守恒律", "四力还原", "经典极限", "现象推导", "场元数据", "现象覆盖",
    ]),
    ("D02", "TUFT/OpenUFT 体系与版本", "02_TUFT_来源", [
        "TUFT", "OpenUFT", "UFT", "V4.", "V3.", "修正版", "谱系", "版本",
        "r9", "r97", "rNN", "全域力统一", "终极力的统一",
    ]),
    ("D03", "螺旋几何与拓扑本源", "01_独立体系", [
        "螺旋", "曲率", "挠率", "拓扑", "几何", "π螺旋", "超复数", "流形",
        "Frenet", "Darboux", "克莱因", "自旋",
    ]),
    ("D04", "量子引力与标准模型统一", "06_统一体系层", [
        "量子引力", "标准模型", "Warsaw", "Fierz", "β系数", "手征", "反常",
        "圈量子", "弦论", "全息", "规范耦合", "SMNF", "SM ", "Clifford", "旋量",
    ]),
    ("D05", "参数拟合与精算审计", "04_公共成果/全维自洽与归一化", [
        "参数拟合", "精算", "数值拟合", "审计", "判据", "边界", "量纲", "自洽",
        "归一化", "决议", "复核", "校验", "机器核账",
    ]),
    ("D06", "文献与全球研究路线", "05_全球研究", [
        "文献", "论文", "全球", "路线", "参考文", "arXiv", "期刊", "弦论",
        "圈量子引力", "因果集", "非交换几何", "全息对偶", "渐近安全",
    ]),
    ("D07", "企业落地与产业应用", "01_独立体系/99_待整理资料", [
        "企业", "落地", "产业", "应用", "加密", "区块链", "算力", "半导体",
        "工业", "金融", "航天", "医疗", "SDK", "商业", "市场",
    ]),
    ("D08", "代码与工程实现", "scripts/实现方式", [
        "代码", "实现", "python", "脚本", "算法", "程序", "函数", "调试",
        "编译", "API", "模块", "库", "class", "def ",
    ]),
    ("D09", "关系体系图与跨体系", "03_跨体系研究", [
        "关系", "图谱", "关图", "跨体系", "翻译表", "接口", "坐标系", "映射",
        "关联图", "关系体系",
    ]),
    ("D10", "数学基础与数论", "02_共享基础", [
        "数论", "素数", "代数", "群", "表示", "同调", "方程", "函数",
        "推导", "恒等式", "积分", "微分",
    ]),
]

# 实体/概念热度词典
ENTITIES = [
    "κ", "τ", "挠率", "曲率", "C²", "ℓ_P", "普朗克", "π", "守恒", "螺旋",
    "超复数", "量子", "引力", "统一场", "SM", "Warsaw", "Fierz", "β", "诺特",
    "参数", "判据", "审计", "文献", "代码", "版本", "TUFT", "OpenUFT", "加密",
    "区块链", "算力", "企业", "数论", "拓扑", "几何", "作用量",
]

# 与 openuft 卷/成果的交叉引用模式
OPENuft_REFS = [
    r"07_统一场方程", r"02_TUFT", r"判定_TUFT", r"全维审计", r"全维自洽",
    r"V4\d", r"V40", r"r9\d", r"卷", r"报告_", r"openuft", r"OpenUFT",
    r"关图", r"关系体系", r"跨体系",
]

ROLE_RE = re.compile(r"^##\s*\d+\.\s*(AI|用户|豆包|助手|你|我)\s*$", re.M)


def esc_link(t):
    """转义 markdown 链接目标中的 ( ) 空格 #，与 openuft refresh_catalog 约定一致，
    verify.py 侧 unquote 可原样还原。"""
    return t.replace('(', '%28').replace(')', '%29').replace(' ', '%20').replace('#', '%23')


def compile_dim_patterns():
    out = []
    for did, name, vol, kws in DIMENSIONS:
        pats = [(kw, re.compile(re.escape(kw), re.IGNORECASE)) for kw in kws]
        out.append((did, name, vol, pats))
    return out


def load_conversation(folder: Path):
    """返回 dict: title, cid, url, created_at, exported_at, n_msg, n_user, n_ai,
    char_user, char_ai, text(合并正文). 优先 jsonl。"""
    md_files = list(folder.glob("*.md"))
    jsonl_files = list(folder.glob("*.jsonl"))
    rec = {
        "title": folder.name, "cid": "", "url": "", "created_at": "",
        "exported_at": "", "n_msg": 0, "n_user": 0, "n_ai": 0,
        "char_user": 0, "char_ai": 0, "text": "",
    }
    if jsonl_files:
        rec["text"], meta = _read_jsonl(jsonl_files[0])
        rec.update(meta)
        return rec
    if md_files:
        rec["text"], meta = _read_md(md_files[0])
        rec.update(meta)
    return rec


def _read_jsonl(path: Path):
    text_parts = []
    n_user = n_ai = char_user = char_ai = 0
    meta = {"cid": "", "url": "", "created_at": "", "exported_at": "", "n_msg": 0}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                meta["cid"] = obj.get("conversation_id") or meta["cid"]
                meta["url"] = obj.get("conversation_url") or meta["url"]
                meta["created_at"] = obj.get("created_at") or meta["created_at"]
                meta["exported_at"] = obj.get("exported_at") or meta["exported_at"]
                role = (obj.get("role") or "").lower()
                content = obj.get("content") or ""
                meta["n_msg"] += 1
                text_parts.append(content)
                if role in ("user", "用户"):
                    n_user += 1
                    char_user += len(content)
                else:
                    n_ai += 1
                    char_ai += len(content)
    except Exception as e:
        print("  [warn] 读取 %s 失败: %s" % (path, e), file=sys.stderr)
    meta["n_user"] = n_user
    meta["n_ai"] = n_ai
    meta["char_user"] = char_user
    meta["char_ai"] = char_ai
    return "\n".join(text_parts), meta


def _read_md(path: Path):
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return "", {"n_msg": 0, "n_user": 0, "n_ai": 0,
                    "char_user": 0, "char_ai": 0}
    # 元信息
    m = re.search(r"会话 ID[:：]\s*(\S+)", text)
    cid = m.group(1) if m else ""
    m = re.search(r"来源[:：]\s*(\S+)", text)
    url = m.group(1) if m else ""
    m = re.search(r"消息数[:：]\s*(\d+)", text)
    n_msg = int(m.group(1)) if m else 0
    # 按角色分块
    parts = ROLE_RE.split(text)
    # parts[0] 为头部，其后每两块为 (role, content)
    n_user = n_ai = char_user = char_ai = 0
    for i in range(1, len(parts), 2):
        role = parts[i].strip()
        content = parts[i + 1] if i + 1 < len(parts) else ""
        if role in ("用户", "你", "我"):
            n_user += 1
            char_user += len(content)
        else:
            n_ai += 1
            char_ai += len(content)
    return text, {"cid": cid, "url": url, "created_at": "", "exported_at": "",
                  "n_msg": n_msg or (n_user + n_ai),
                  "n_user": n_user, "n_ai": n_ai,
                  "char_user": char_user, "char_ai": char_ai}


def score_dimensions(text, dim_patterns):
    scores = {}
    for did, name, vol, pats in dim_patterns:
        s = 0
        for kw, pat in pats:
            c = len(pat.findall(text))
            if c:
                # 长关键词权重更高；命中即至少计 1
                s += c * (2 if len(kw) >= 3 else 1)
        if s:
            scores[did] = s
    return scores


def count_entities(text):
    low = text.lower()
    hits = {}
    for e in ENTITIES:
        # 拉丁词用忽略大小写子串；中文直接用子串
        pat = re.compile(re.escape(e), re.IGNORECASE)
        c = len(pat.findall(low if e.isascii() else text))
        if c:
            hits[e] = c
    return hits


def find_openuft_refs(text):
    found = []
    for pat in OPENuft_REFS:
        c = len(re.findall(pat, text))
        if c:
            found.append((pat, c))
    return found


def month_of(iso):
    if not iso:
        return "未知"
    m = re.match(r"(\d{4}-\d{2})", iso)
    return m.group(1) if m else "未知"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exports", default=DEFAULT_EXPORTS)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--limit", type=int, default=0, help="0=全部")
    args = ap.parse_args()

    exports = Path(args.exports)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "维度索引").mkdir(parents=True, exist_ok=True)

    folders = sorted([p for p in exports.iterdir() if p.is_dir()])
    if args.limit:
        folders = folders[: args.limit]
    print("[info] 待分析会话文件夹: %d（来源 %s）" % (len(folders), exports))

    dim_patterns = compile_dim_patterns()
    records = []
    for idx, fol in enumerate(folders, 1):
        rec = load_conversation(fol)
        text = rec["text"]
        dim_scores = score_dimensions(text, dim_patterns)
        ents = count_entities(text)
        refs = find_openuft_refs(text)
        # 主维度 = 最高分；top3 维度
        ranked = sorted(dim_scores.items(), key=lambda x: -x[1])
        primary = ranked[0][0] if ranked else "D00"
        top3 = [d for d, _ in ranked[:3]]
        rec.update({
            "folder": fol.name,
            "rel_path": "code/豆包/自动化保存对话脚本/exports/doubao/%s" % fol.name,
            "dim_scores": dim_scores,
            "primary_dim": primary,
            "top3_dims": top3,
            "entities": dict(sorted(ents.items(), key=lambda x: -x[1])[:15]),
            "openuft_refs": [p for p, _ in refs],
            "month": month_of(rec["created_at"]),
            "chars": len(text),
        })
        records.append(rec)
        if idx % 100 == 0:
            print("  已处理 %d/%d" % (idx, len(folders)), flush=True)

    print("[info] 分析完成，共 %d 个会话" % len(records))

    # ---------------- 聚合 ----------------
    dim_names = {d[0]: d[1] for d in DIMENSIONS}
    dim_vols = {d[0]: d[2] for d in DIMENSIONS}
    dim_conv = defaultdict(list)
    for r in records:
        for d in r["top3_dims"]:
            dim_conv[d].append(r)

    total_msgs = sum(r["n_msg"] for r in records)
    total_chars = sum(r["chars"] for r in records)

    # 时间线
    timeline = defaultdict(lambda: [0, 0])
    for r in records:
        timeline[r["month"]][0] += 1
        timeline[r["month"]][1] += r["n_msg"]

    # 规模分布
    scale = Counter()
    for r in records:
        n = r["n_msg"]
        if n < 3:
            scale["空/极短(<3)"] += 1
        elif n < 10:
            scale["<10"] += 1
        elif n < 50:
            scale["10-49"] += 1
        elif n < 200:
            scale["50-199"] += 1
        elif n < 500:
            scale["200-499"] += 1
        else:
            scale["500+"] += 1

    # 实体热度
    ent_total = Counter()
    for r in records:
        for e, c in r["entities"].items():
            ent_total[e] += c

    # 覆盖矩阵：openuft 卷 -> 命中会话数
    vol_hits = Counter()
    for r in records:
        for d in r["top3_dims"]:
            vol_hits[dim_vols[d]] += 1

    # ---------------- 写 catalog.json ----------------
    catalog = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_exports": str(exports),
        "n_conversations": len(records),
        "total_messages": total_msgs,
        "total_chars": total_chars,
        "dimensions": [{"id": d[0], "name": d[1], "openuft_volume": d[2]}
                       for d in DIMENSIONS],
        "timeline": {k: {"convs": v[0], "msgs": v[1]}
                     for k, v in sorted(timeline.items())},
        "scale_distribution": dict(scale),
        "entity_heat": dict(ent_total.most_common(40)),
        "coverage_matrix": dict(vol_hits),
        "conversations": [
            {
                "folder": r["folder"], "title": r["title"], "cid": r["cid"],
                "url": r["url"], "created_at": r["created_at"],
                "n_msg": r["n_msg"], "n_user": r["n_user"], "n_ai": r["n_ai"],
                "chars": r["chars"], "month": r["month"],
                "primary_dim": r["primary_dim"], "top3_dims": r["top3_dims"],
                "dim_scores": r["dim_scores"], "entities": r["entities"],
                "openuft_refs": r["openuft_refs"],
                "rel_path": r["rel_path"],
            }
            for r in records
        ],
    }
    (out / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=1), encoding="utf-8")
    print("[info] 已写 catalog.json")

    # ---------------- 维度索引/<dim>.md ----------------
    for did, name, vol, _ in DIMENSIONS:
        convs = sorted(dim_conv.get(did, []),
                       key=lambda r: -r["n_msg"])
        lines = ["# %s · %s（→ openuft: %s）\n" % (did, name, vol)]
        lines.append("会话数：**%d**\n" % len(convs))
        lines.append("\n| # | 标题 | 会话ID | 消息数 | 创建月份 | 主要实体 | 交叉引用 | 路径 |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(convs, 1):
            ents = "、".join(list(r["entities"].keys())[:5]) or "-"
            refs = "、".join(r["openuft_refs"][:4]) or "-"
            lines.append("| %d | %s | %s | %d | %s | %s | %s | `%s` |" % (
                i, r["title"][:40], r["cid"], r["n_msg"], r["month"],
                ents, refs, r["rel_path"]))
        (out / "维度索引" / ("%s.md" % did)).write_text(
            "\n".join(lines), encoding="utf-8")
    print("[info] 已写维度索引 (%d 个维度)" % len(DIMENSIONS))

    # ---------------- 全维分析总览.md ----------------
    write_overview(out, records, catalog, dim_names, dim_vols,
                   total_msgs, total_chars, timeline, scale, ent_total, vol_hits)

    # ---------------- INDEX.md ----------------
    write_index(out, len(records), total_msgs, total_chars, dim_conv,
                dim_names, dim_vols)

    print("[done] 输出目录: %s" % out)


def write_overview(out, records, catalog, dim_names, dim_vols,
                   total_msgs, total_chars, timeline, scale, ent_total, vol_hits):
    L = []
    L.append("# 豆包对话 · 全维分析总览\n")
    L.append("> 生成时间：%s  \n> 数据源：`code/豆包/自动化保存对话脚本/exports/doubao/`"
             "（豆包桌面端原生登录态导出，.jsonl/.md 双格式）  \n"
             "  **数据范围说明**：本次分析覆盖**当前已下载**的 %d 个会话；豆包全量约 4810 个，"
             "后台导出仍在进行。本分析脚本可复跑——下载完成后重跑即得完整「全维」覆盖。"
             % (catalog["generated_at"], len(records)))
    L.append("\n## 一、执行摘要\n")
    L.append("- 已分析会话：**%d** 个" % len(records))
    L.append("- 累计消息：**%s** 条（用户 %s / AI %s）" % (
        total_msgs,
        sum(r["n_user"] for r in records),
        sum(r["n_ai"] for r in records)))
    L.append("- 累计正文：约 **%.1f MB** 文本" % (total_chars / 1e6))
    L.append("- 维度框架：10 个主题维度（对齐 openuft 卷结构）+ 时间/规模/角色/实体/映射 5 个辅助维度")
    L.append("- 落点：写入 `openuft/91_豆包对话全维分析整理/`")
    L.append("\n## 二、方法论\n")
    L.append("- 解析：每会话优先读 `.jsonl`（含 `role/content/created_at/exported_at`），"
             "缺则回退 `.md` 按 `## N. 角色` 分块。")
    L.append("- 主题维度：10 个维度各含关键词表，按子串命中计数加权计分；取命中维度 top3，"
             "最高分为该会话主维度。")
    L.append("- 实体热度：对 %d 个物理/工程概念做大小写不敏感计数。" % len(ENTITIES))
    L.append("- openuft 映射：正则捕获会话文本中对 openuft 卷/成果（如 `07_统一场方程`、`判定_TUFT`、"
             "`V4x`、`r9x`）的交叉引用，形成覆盖矩阵。")
    L.append("\n## 三、维度总览（主题维度 → openuft 卷）\n")
    L.append("| 维度 | 名称 | 映射 openuft 卷 | 会话数 | 累计消息 |")
    L.append("|---|---|---|---|---|")
    # 按会话数排序
    dim_order = sorted(dim_names.keys(),
                       key=lambda d: -sum(1 for r in records if d in r["top3_dims"]))
    for d in dim_order:
        convs = [r for r in records if d in r["top3_dims"]]
        msgs = sum(r["n_msg"] for r in convs)
        L.append("| %s | %s | %s | %d | %s |" % (
            d, dim_names[d], dim_vols[d], len(convs), msgs))
    L.append("\n## 四、时间线（按创建月份）\n")
    L.append("| 月份 | 会话数 | 消息数 |")
    L.append("|---|---|---|")
    for k in sorted(timeline.keys()):
        v = timeline[k]
        L.append("| %s | %d | %d |" % (k, v[0], v[1]))
    L.append("\n## 五、规模分布（每会话消息数）\n")
    L.append("| 区间 | 会话数 |")
    L.append("|---|---|")
    for k in ["<10", "10-49", "50-199", "200-499", "500+", "空/极短(<3)"]:
        L.append("| %s | %d |" % (k, scale.get(k, 0)))
    L.append("\n## 六、实体/概念热度（Top 25）\n")
    L.append("| 概念 | 命中会话提及次数 |")
    L.append("|---|---|")
    for e, c in ent_total.most_common(25):
        L.append("| %s | %d |" % (e, c))
    L.append("\n## 七、覆盖矩阵（openuft 卷 ← 命中会话数）\n")
    L.append("| openuft 卷/成果 | 关联会话数 | 建议整合动作 |")
    L.append("|---|---|---|")
    advice = {
        "07_统一场方程": "主方程、作用量、守恒律类对话直接归入本卷各章节",
        "02_TUFT_来源": "TUFT/OpenUFT 版本谱系、来源考据对话归入本卷",
        "01_独立体系": "螺旋几何、企业落地场景归入对应独立体系/应用卷",
        "06_统一体系层": "量子引力、SM 统一、Warsaw/Fierz 核验归入统一体系层",
        "04_公共成果/全维自洽与归一化": "参数拟合、精算审计、判据类对话并入本册",
        "05_全球研究": "文献、全球路线、弦论/圈量子等归入本卷",
        "03_跨体系研究": "关系图、跨体系映射对话归入本卷",
        "02_共享基础": "数论、代数基础归入共享基础",
        "scripts/实现方式": "代码与工程实现沉淀为可复用脚本/实现档案",
        "01_独立体系/99_待整理资料": "企业落地与应用先入待整理，再分流",
    }
    for vol, c in vol_hits.most_common():
        L.append("| %s | %d | %s |" % (vol, c, advice.get(vol, "按主题分流")))
    L.append("\n## 八、各维度重点会话（每维度 Top 15，按消息数）\n")
    for d in dim_order:
        convs = sorted([r for r in records if d in r["top3_dims"]],
                       key=lambda r: -r["n_msg"])[:15]
        if not convs:
            continue
        L.append("\n### %s %s（→ %s）\n" % (d, dim_names[d], dim_vols[d]))
        for i, r in enumerate(convs, 1):
            ents = "、".join(list(r["entities"].keys())[:4]) or "-"
            L.append("%d. **%s**（%d 条消息，%s）— 实体：%s  [路径](%s)"
                     % (i, r["title"][:50], r["n_msg"], r["month"], ents,
                        esc_link("../../code/豆包/自动化保存对话脚本/exports/doubao/%s" % r["folder"])))
    L.append("\n## 九、整合建议\n")
    L.append("1. **先归并高信号维度**：D01（统一场方程）、D05（参数拟合/精算审计）"
             "与 openuft `07_统一场方程`、`04_公共成果/全维自洽与归一化` 直接对应，优先人工审读并入。")
    L.append("2. **版本谱系入 `02_TUFT_来源`**：D02 中带 `V4x`/`r9x` 的对话按版本号归档。")
    L.append("3. **待整理缓冲**：D07 企业落地类先入 `99_待整理资料/豆包对话全维分析整理/` 或本卷，"
             "经人工提炼后再分流到独立体系/应用卷。")
    L.append("4. **复跑补齐**：后台导出完成后重跑本脚本，本卷所有文件将被覆盖刷新为完整语料视图。")
    L.append("\n---\n*本总览由 `openuft/scripts/analyze_doubao_corpus.py` 自动生成，可复跑。*")
    (out / "全维分析总览.md").write_text("\n".join(L), encoding="utf-8")
    print("[info] 已写 全维分析总览.md")


def write_index(out, n, total_msgs, total_chars, dim_conv, dim_names, dim_vols):
    L = []
    L.append("# 91 · 豆包对话全维分析整理\n")
    L.append("本卷存放**豆包（字节跳动 AI）全部对话**的「全维分析整理」结果，"
             "作为向 openuft 各研究卷整合的结构化入口。\n")
    L.append("## 内容\n")
    L.append("- `全维分析总览.md` — 多维度统计、覆盖矩阵与整合建议（**先看这份**）")
    L.append("- `catalog.json` — 机器可读的逐会话记录与聚合指标")
    L.append("- `维度索引/<Dxx>.md` — 每个主题维度的完整会话清单")
    L.append("\n## 规模速览\n")
    L.append("- 已分析会话：**%d** 个" % n)
    L.append("- 累计消息：**%s** 条" % total_msgs)
    L.append("- 累计正文：约 **%.1f MB**" % (total_chars / 1e6))
    L.append("\n## 维度导航\n")
    for did in sorted(dim_names.keys()):
        convs = dim_conv.get(did, [])
        L.append("- [%s %s](维度索引/%s.md) → openuft `%s`（%d 会话）"
                 % (did, dim_names[did], did, dim_vols[did], len(convs)))
    L.append("\n## 复跑方法\n")
    L.append("```powershell\n"
             "cd openuft\\scripts\n"
             "python analyze_doubao_corpus.py\n"
             "```\n"
             "下载完成后重跑，本卷所有文件覆盖刷新。\n")
    L.append("\n## 数据来源\n")
    L.append("`code/豆包/自动化保存对话脚本/exports/doubao/<标题>/`（.md + .jsonl 双格式）。")
    (out / "INDEX.md").write_text("\n".join(L), encoding="utf-8")
    print("[info] 已写 INDEX.md")


if __name__ == "__main__":
    main()
