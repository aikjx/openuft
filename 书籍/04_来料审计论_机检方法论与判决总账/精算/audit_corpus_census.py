# -*- coding: utf-8 -*-
"""判定册三本账 · 只读普查（本书所有聚合数字的唯一载体）。

审计对象（只读，不改任何被审册字节）：
  账一 判定/判定_TUFT-r*.md            —— 判决面本体（条目数、裁定分布、控制组/守卫、rc）
  账二 数据/*来料原件* + 态势盘点册      —— 来料正本与 ROOT 版本谱
  账三 openuft/07_统一场方程/*_第N轮_*  —— J 线（力统一正面建设）卷数与最新轮

家族感知：判决面模板跨代不同形，故用三把尺 F1/F2/F3 依序试打；
一把面只归入第一个命中的家族，全部未命中的面**逐名点出**（「没提取到」≠「值为 0」）。

对照（尺必须有牙）：
  正对照 P1 合成一张符合 F2 形状的内存面，必须被解析且闭合成立
  负对照 N1 把合成面的 FAIL 0→1（条目数不动）⇒ 闭合断言必须转红
  负对照 N2 把合成面的条目数 24→25 ⇒ 提取值必须随之改变（针不是恒 0）
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)                      # .../书籍/04_来料审计论_...
OPENUFT = os.path.dirname(os.path.dirname(BOOK))  # .../openuft
VOL = os.path.join(OPENUFT, "04_公共成果", "本项目_全维自洽与归一化")
JLINE = os.path.join(OPENUFT, "07_统一场方程")
INVENTORY = os.path.join(VOL, "整理_攻破态势盘点与偏差更正_ROOT版本谱与号段占用_2026-11-02.md")

CHECKS = []
FAILS = []


def ctl(name, ok, detail):
    CHECKS.append((name, ok, detail))
    if not ok:
        FAILS.append("%s :: %s" % (name, detail))
    print("  [%s] %s :: %s" % ("绿" if ok else "红", name, detail))


def read_text(path):
    with io.open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().replace("\r\n", "\n").replace("\r", "\n")


def stat(path):
    b = os.stat(path)
    return b.st_size


# ---------------------------------------------------------------- 账一
RE_F2 = re.compile(
    r"\*\*条目\*\*：(\d+)（主\s*(\d+)）\s*\*\*PASS\s*(\d+)\s*/\s*FAIL\s*(\d+)\s*/"
    r"\s*BOUNDARY\s*(\d+)\s*/\s*INFO\s*(\d+)\*\*\s*\*\*控制组\s*(\d+)/(\d+)\*\*"
    r"\s*\*\*守卫\s*(\d+)/(\d+)\*\*\s*\*\*rc=(\d+)\*\*")

RE_F3 = re.compile(r"条目\s*(\d+)（PASS\s*(\d+)\s*/\s*INFO\s*(\d+)\s*/\s*FAIL\s*(\d+)）")

RE_F1_ROW = re.compile(r"^\|\s*([ABCGEPO])\s*\|\s*[^|]*\|\s*(\d+)\s*\|\s*$", re.M)
RE_F1_TOTAL = re.compile(r"^\|\s*合计\s*\|\s*—\s*\|\s*(\d+)\s*\|\s*$", re.M)
RE_F1_ITEM = re.compile(r"^\|\s*[ABCGEPO]\d\d\s*\|")


def parse_f1(text):
    """r351 型：§〇 分层声明表 + §二 主册行。裁定只从 §二 表体数，不扫全文（防同词多面计数）。"""
    if "## §〇" not in text or "## §二" not in text:
        return None
    body = text.split("## §〇", 1)[1].split("\n## ", 1)[0]
    rows = RE_F1_ROW.findall(body)
    tot = RE_F1_TOTAL.search(body)
    if not rows or not tot:
        return None
    layer = {}
    for k, v in rows:
        layer[k] = layer.get(k, 0) + int(v)
    total = int(tot.group(1))
    mj = text.split("## §二", 1)[1].split("\n## ", 1)[0]
    item_rows = [L for L in mj.split("\n") if RE_F1_ITEM.match(L)]
    verd = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    mut = judge = jmut = 0
    for L in item_rows:
        m = re.search(r"\*\*(PASS|FAIL|BOUNDARY|INFO)/", L)
        if m:
            verd[m.group(1)] += 1
        cells = [c.strip() for c in L.strip().strip("|").split("|")]
        has_mut = bool(len(cells) >= 7 and cells[-1] and cells[-1] != "—")
        mut += 1 if has_mut else 0
        if cells and cells[0][:1] in "ABGC":          # 判决类 = 有裁定的四层（E/P/O 属登记与边界）
            judge += 1
            jmut += 1 if has_mut else 0
    return {
        "family": "F1 分层表",
        "items": total,
        "layer": layer,
        "layer_sum": sum(layer.values()),
        "main_rows": len(item_rows),
        "verd": verd,
        "verd_sum": sum(verd.values()),
        "judge_rows": judge,
        "judge_mut": jmut,
        "ctrl": None,
        "guard": None,
        "rc": None,
        "mut": mut,
    }


def parse_f2(text):
    m = RE_F2.search(text)
    if not m:
        return None
    g = [int(x) for x in m.groups()]
    return {
        "family": "F2 头条行",
        "items": g[0],
        "main": g[1],
        "verd": {"PASS": g[2], "FAIL": g[3], "BOUNDARY": g[4], "INFO": g[5]},
        "ctrl": (g[6], g[7]),
        "guard": (g[8], g[9]),
        "rc": g[10],
        "mut": None,
    }


def parse_f3(text):
    m = RE_F3.search(text)
    if not m:
        return None
    g = [int(x) for x in m.groups()]
    return {
        "family": "F3 裁定行",
        "items": g[0],
        "verd": {"PASS": g[1], "FAIL": g[3], "BOUNDARY": 0, "INFO": g[2]},
        "ctrl": None,
        "guard": None,
        "rc": None,
        "mut": None,
    }


def parse_face(text):
    for fn in (parse_f2, parse_f1, parse_f3):
        r = fn(text)
        if r:
            return r
    return None


def synth_face():
    """正/负对照用的合成面：形状取自盘上真实头条行，数值自定。"""
    return (
        "# 判定_TUFT-r9999 · 合成面\n"
        "- **日期**：2026-11-02　- **靶**：合成\n"
        "- **条目**：24（主 10）　**PASS 22 / FAIL 0 / BOUNDARY 0 / INFO 2**　"
        "**控制组 4/4**　**守卫 10/10**　**rc=0**\n"
    )


def closure(rec):
    v = rec["verd"]
    return v["PASS"] + v["FAIL"] + v["BOUNDARY"] + v["INFO"]


# ---------------------------------------------------------------- 账二
def census_provenance():
    faces = sorted(glob_proper(os.path.join(VOL, "数据"), "*来料原件*"))
    rows = []
    for p in faces:
        with io.open(p, "rb") as fh:
            raw = fh.read()
        rows.append({
            "name": os.path.basename(p),
            "bytes": len(raw),
            "date": (re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(p)) or [None, "?"])[1],
        })
    return rows


def glob_proper(d, pat):
    return [os.path.join(d, n) for n in sorted(os.listdir(d))
            if os.path.isfile(os.path.join(d, n)) and pat.strip("*") in n]


def census_root谱():
    if not os.path.exists(INVENTORY):
        return None, None
    text = read_text(INVENTORY)
    sec = text.split("## 二、ROOT 版本谱", 1)
    if len(sec) < 2:
        return None, None
    body = sec[1].split("##", 1)[0]
    rows = []
    for L in body.split("\n"):
        if not L.startswith("|"):
            continue
        cells = [c.strip() for c in L.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] in ("版本", "") or set(cells[0]) <= set("-: "):
            continue
        rows.append({"version": cells[0].replace("**", ""), "carriers": cells[1], "date": cells[2]})
    vers = set()
    for r in rows:
        for v in re.findall(r"V\d+(?:\.\d+)?", r["version"]):
            vers.add(v)
    return rows, sorted(vers)


# ---------------------------------------------------------------- 账三
def census_jline():
    files = [n for n in sorted(os.listdir(JLINE)) if re.match(r"\d+_第\d+轮_", n)]
    vols = [int(re.match(r"(\d+)_", n).group(1)) for n in files]
    rounds = [int(re.match(r"\d+_第(\d+)轮_", n).group(1)) for n in files]
    latest = max(files, key=lambda n: (int(re.match(r"(\d+)_", n).group(1)),
                                       int(re.match(r"\d+_第(\d+)轮_", n).group(1)))) if files else None
    return {
        "round_named_files": len(files),
        "max_volume_no": max(vols) if vols else 0,
        "max_round_no": max(rounds) if rounds else 0,
        "latest_file": latest,
        "total_md_in_dir": len([n for n in os.listdir(JLINE) if n.endswith(".md")]),
    }


def main():
    for p in (os.path.join(VOL, "判定"), os.path.join(VOL, "数据"), JLINE, INVENTORY):
        if not os.path.exists(p):
            print("被审对象路径缺失：%s ⇒ 硬失败（不印 0，不印空表）" % p)
            return 2
    print("=" * 78)
    print("判定册三本账 · 只读普查（脚本 %s）" % os.path.relpath(__file__, OPENUFT))
    print("=" * 78)

    # ---- 对照先行：针有牙才允许引用下面的数
    print("\n【对照】合成面三发（两负一正）")
    s = synth_face()
    base = parse_face(s)
    ctl("P1 正对照·合成 F2 面被解析且闭合",
        base is not None and closure(base) == base["items"],
        "提取 %s，PASS+FAIL+BOUND+INFO=%s == 条目 %s" % (base["items"], closure(base), base["items"]))
    bad = parse_face(s.replace("FAIL 0", "FAIL 1"))
    ctl("N1 负对照·FAIL 0→1 必须破坏闭合",
        bad is not None and closure(bad) == base["items"] + 1,
        "闭合和由 %s 变 %s（条目仍 %s）⇒ 闭合断言有牙" % (closure(base), closure(bad), bad["items"]))
    off = parse_face(s.replace("**条目**：24", "**条目**：25"))
    ctl("N2 负对照·条目 24→25 必须被读到",
        off is not None and off["items"] == 25,
        "提取值 %s → %s（不是恒 0 的针）" % (base["items"], off["items"]))
    clean = parse_face(s.replace("PASS 22 / FAIL 0 / BOUNDARY 0 / INFO 2",
                                 "PASS 21 / FAIL 1 / BOUNDARY 0 / INFO 2"))
    ctl("N2b 正对照·头条自洽的面不得被报成缺陷",
        clean is not None and closure(clean) == clean["items"],
        "FAIL 0→1 且条目不动（四类之和 %s == 条目 %s）⇒ 缺陷报告器不误伤干净面"
        % (closure(clean), clean["items"]))
    f1_synth = (
        "## §〇 分层声明（条目不可相加）\n\n| 层 | 含义 | 条数 |\n| --- | --- | --- |\n"
        "| A | x | 14 |\n| G | y | 9 |\n| 合计 | — | 23 |\n\n"
        "## §二 主册\n\n| ID | 层 | 条目 | 期望 | 实测 | 裁定 | 变异体 |\n| --- | --- | --- | --- | --- | --- | --- |\n"
        "| A01 | A | 项 | e | m | **PASS/成立** | 改坏后必须为假 |\n"
        "| G01 | G | 项 | e | m | **FAIL/不成立** | 改坏后必须消失 |\n"
        "| E01 | E | 项 | e | m | **INFO/登记** | — |\n\n"
        "## §三 下一节\n"
    )
    r1 = parse_f1(f1_synth)
    ctl("N3 负对照·F1 尺在合成面上取到层表 23／主册 3 行／判决类 2 行带变异体 2",
        r1 is not None and r1["layer"] == {"A": 14, "G": 9} and r1["layer_sum"] == 23
        and r1["main_rows"] == 3 and r1["judge_rows"] == 2 and r1["judge_mut"] == 2,
        "layer=%s 层和=%s 主册行=%s 判决类=%s 带变异体=%s ⇒ §〇+§二 两把尺可复现（非只对一个盘上面有效）"
        % (r1["layer"], r1["layer_sum"], r1["main_rows"], r1["judge_rows"], r1["judge_mut"]))
    r1b = parse_f1(f1_synth.replace("| G01 | G | 项 | e | m | **FAIL/不成立** | 改坏后必须消失 |",
                                    "| G01 | G | 项 | e | m | **FAIL/不成立** | — |"))
    ctl("N4 负对照·把判决类某行变异体改成破折号，带变异体计数必须从 2 降到 1",
        r1b is not None and r1b["judge_mut"] == 1,
        "judge_mut %s → %s（覆盖针不是恒满格）" % (r1["judge_mut"], r1b["judge_mut"]))
    if FAILS:
        print("对照未全绿 ⇒ 后面的一切聚合数不得引用")
        return 2

    # ---- 账一
    print("\n【账一】判定面普查（分母＝盘上判定_TUFT-r*.md 全名册）")
    face_dir = os.path.join(VOL, "判定")
    names = [n for n in sorted(os.listdir(face_dir)) if re.match(r"判定_TUFT-r.*\.md$", n)]
    recs, missing = [], []
    for n in names:
        p = os.path.join(face_dir, n)
        rec = parse_face(read_text(p))
        if rec is None:
            missing.append(n)
        else:
            rec["file"] = n
            rec["bytes"] = stat(p)
            recs.append(rec)
    by_fam = {}
    for r in recs:
        by_fam.setdefault(r["family"], []).append(r)
    print("判定面分母 = %d 份｜被三把尺之一取到 = %d 份｜没提取到 = %d 份"
          % (len(names), len(recs), len(missing)))
    for fam in sorted(by_fam):
        rs = by_fam[fam]
        agg = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
        for r in rs:
            for k in agg:
                agg[k] += r["verd"][k]
        print("  %-10s 面 %3d ｜条目 Σ %5d ｜裁定 PASS %4d / FAIL %3d / BOUNDARY %3d / INFO %3d"
              % (fam, len(rs), sum(r["items"] for r in rs), agg["PASS"], agg["FAIL"],
                 agg["BOUNDARY"], agg["INFO"]))
        if all(closure(r) == r["items"] for r in rs):
            print("             闭合：每面 4 类裁定之和 == 该面条目数（%d/%d 面成立）" % (len(rs), len(rs)))
        else:
            badf = [r["file"] for r in rs if closure(r) != r["items"]]
            print("             闭合破坏面 %d 份：%s" % (len(badf), badf[:6]))
    tot_items = sum(r["items"] for r in recs)
    tot_verd = {"PASS": 0, "FAIL": 0, "BOUNDARY": 0, "INFO": 0}
    for r in recs:
        for k in tot_verd:
            tot_verd[k] += r["verd"][k]
    vsum = sum(tot_verd.values())
    rel = "==" if vsum == tot_items else ("!=" if vsum < tot_items else ">")
    print("  合计：条目 Σ %d ｜裁定 PASS %d / FAIL %d / BOUNDARY %d / INFO %d ｜四类之和 %d（%s 条目 Σ）"
          % (tot_items, tot_verd["PASS"], tot_verd["FAIL"], tot_verd["BOUNDARY"],
             tot_verd["INFO"], vsum, rel))
    broken = [r for r in recs if closure(r) != r["items"]]
    if broken:
        print("  ★账面缺陷（本普查现扫到的，逐名点出）：这些面的头条自报数与其四类裁定之和不符 ⇒ 差 %d 条"
              % (tot_items - vsum))
        for r in broken:
            print("     · %s：条目 %s vs 四类之和 %s（层表/主册未与头条同行核对）"
                  % (r["file"], r["items"], closure(r)))
    else:
        print("  闭合破坏面 0 份")
    f2 = by_fam.get("F2 头条行", [])
    if f2:
        rc0 = sum(1 for r in f2 if r["rc"] == 0)
        cg = [(r["ctrl"][0], r["ctrl"][1]) for r in f2 if r["ctrl"]]
        gg = [(r["guard"][0], r["guard"][1]) for r in f2 if r["guard"]]
        print("  F2 子集：%d 面里 rc=0 者 %d；控制组满格 %d/%d；守卫满格 %d/%d"
              % (len(f2), rc0, sum(1 for a, b in cg if a == b), len(cg),
                 sum(1 for a, b in gg if a == b), len(gg)))
    print("\n【账一·附】三面互认（判定册 §〇/§二 ↔ 引擎 stdout）：靶 r351")
    r351 = [r for r in recs if r.get("family") == "F1 分层表"]
    out_p = os.path.join(VOL, "源码", "_out_r351.txt")
    if r351 and os.path.exists(out_p):
        rec = r351[0]
        ot = read_text(out_p)
        mo = re.search(r"条目\s*(\d+)（判决类\s*(\d+)，带变异体\s*(\d+)）", ot)
        if mo:
            o_items, o_judge, o_mut = [int(x) for x in mo.groups()]
            ctl("X1 面 §〇 合计 == stdout 条目数", rec["items"] == o_items,
                "面 §〇=%s vs stdout=%s" % (rec["items"], o_items))
            ctl("X2 面 §二 判决类行数 == stdout 判决类数", rec["judge_rows"] == o_judge,
                "面 §二 A/B/G/C 行=%s vs stdout=%s" % (rec["judge_rows"], o_judge))
            ctl("X3 面 §二 判决类带变异体 == stdout 带变异体", rec["judge_mut"] == o_mut,
                "面=%s vs stdout=%s（另 %s 行 INFO 类也填了变异体列，属口径宽一档，已在书稿注明）"
                % (rec["judge_mut"], o_mut, rec["mut"] - rec["judge_mut"]))
            ctl("X4 面 §二 行数 == §〇 合计（行数不靠手打）", rec["main_rows"] == rec["items"],
                "§二 现扫 %s 行 vs §〇 合计 %s" % (rec["main_rows"], rec["items"]))
        else:
            ctl("X0 stdout 摘要行提取", False, "_out_r351.txt 里没提取到「条目 N（判决类 M，带变异体 K）」行")
    else:
        print("  三面互认：没提取到（F1 面或 stdout 缺席 ⇒ 不引用）")
    print("  没提取到的面（逐名点出，不计入任何分母）：")
    for n in missing[:12]:
        print("     ·", n)
    if len(missing) > 12:
        print("     · …另 %d 份（全名册见 json）" % (len(missing) - 12))

    # ---- 账二
    print("\n【账二】来料正本与 ROOT 版本谱")
    prov = census_provenance()
    print("正本（数据/*来料原件*）= %d 件，合计 %d 字节"
          % (len(prov), sum(p["bytes"] for p in prov)))
    for p in prov[-6:]:
        print("   %9d B  %s" % (p["bytes"], p["name"][:96]))
    rows, vers = census_root谱()
    if rows:
        print("版本谱（态势盘点册 §二 表体，按首格现扫）= %d 行；提及的版本号 %d 个：%s"
              % (len(rows), len(vers), " ".join(vers)))
        print("承载册去重 r 号 = %d 个" % len(set(re.findall(r"r(\d+)", " ".join(r["carriers"] for r in rows)))))
    else:
        print("版本谱：没提取到（该册小节形状变了 ⇒ 不引用任何版本计数）")

    # ---- 账三
    print("\n【账三】J 线（07_统一场方程 · 第 N 轮）")
    j = census_jline()
    print("轮名文件 %d 份｜最大卷号 %d｜最大轮号 %d｜目录内 md 共 %d 份"
          % (j["round_named_files"], j["max_volume_no"], j["max_round_no"], j["total_md_in_dir"]))
    print("最新一册：", j["latest_file"])

    # ---- 产物
    out = {
        "faces_total": len(names),
        "faces_parsed": len(recs),
        "faces_not_extracted": missing,
        "by_family": {f: {"faces": len(v), "items": sum(x["items"] for x in v),
                          "verdicts": {k: sum(x["verd"][k] for x in v) for k in
                                       ("PASS", "FAIL", "BOUNDARY", "INFO")}}
                      for f, v in by_fam.items()},
        "items_total": tot_items,
        "verdicts_total": tot_verd,
        "closure_gap": tot_items - sum(tot_verd.values()),
        "closure_broken": [r["file"] for r in broken],
        "faces": recs,
        "provenance_files": prov,
        "root_version_rows": rows,
        "jline": j,
        "controls": [{"name": c[0], "ok": c[1]} for c in CHECKS],
    }
    jp = os.path.join(HERE, "audit_corpus_census.json")
    with io.open(jp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(out, ensure_ascii=False, indent=1))
    print("\n产物：json %d B（%s）" % (stat(jp), os.path.relpath(jp, OPENUFT)))
    n_pass = sum(1 for c in CHECKS if c[1])
    print("对照 %d/%d 绿；未提取面 %d 份（已逐名点出，不计入分母）" % (n_pass, len(CHECKS), len(missing)))
    if FAILS:
        print("CENSUS-RED")
        return 1
    print("CENSUS-GREEN：三本账读数由盘面现取，闭合与对照同轮成立")
    return 0


if __name__ == "__main__":
    sys.exit(main())
