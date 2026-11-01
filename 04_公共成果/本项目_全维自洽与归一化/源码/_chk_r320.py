# -*- coding: utf-8 -*-
"""r320 收口只读复核 v6（零写入 · 期望全部从落盘面现推 · 每条判据各配一枚内存变异体证明有牙）。

纪律：
1. 本脚本不写任何文件、不重跑引擎（重跑会写盘）。自身源码里出现写模式即判红（W0 + M01）。
2. 所有期望值从盘上的面本身现推（json / 数据册 md / report / 判定册 / 正本 / README / HTML / runner），
   不从上一轮叙述抄来；解析不出东西 = 判 False（与「没有缺陷」不同形）。
3. 每条判据抽成纯函数 chk_wN(Wv)，Wv = 「世界字典」（盘面文本 + 解析结果）。变异体只改世界副本的一个字段，
   两趟制：①正对照（未变异世界必须 True，否则尺与盘面口径不符 = PRE-CONTROL-RED）；②变异（必须 False）。
   任一趟抛异常 = CRASH = 零判决 = 本判决 INVALID（rc=1）。
4. 他卷面（r308/r317/r321）与 README 只做 md5/尺寸比对，证明本脚本运行期间没人动过（W12）。
"""
import copy
import glob
import hashlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import _r320_selfbugs as SB  # noqa: E402  自抓块的唯一派生（与登记/同步驱动同一支尺）
DATA = os.path.join(ROOT, "数据")
JUDG = os.path.join(ROOT, "判定")
README = os.path.join(ROOT, "README.md")
VERD = ("PASS", "FAIL", "BOUNDARY", "INFO")
BS = chr(92)
STUB_HEX = "0123456789ab"

JF = glob.glob(os.path.join(DATA, "TUFT-r320_*.json"))
MF = glob.glob(os.path.join(DATA, "TUFT-r320_*_精算与可视化_2026-11-01.md"))
RF = glob.glob(os.path.join(DATA, "TUFT-r320_*_report.txt"))
ZF = glob.glob(os.path.join(DATA, "TUFT-r320_*_来料原件_ROOT_V24.0_用户附件逐字_2026-11-01.md"))
JUF = glob.glob(os.path.join(JUDG, "判定_TUFT-r320_*.md"))
HF = glob.glob(os.path.join(ROOT, "四力统一方程_ROOTV24图表层*_r320*.html"))
EF = glob.glob(os.path.join(HERE, "TUFT-r320_*.py"))
RUN = glob.glob(os.path.join(HERE, "_run_r320.py"))


def one(xs, name):
    if len(xs) != 1:
        print("FACE-COUNT %s = %d -> 判集不唯一，拒绝判决" % (name, len(xs)))
        sys.exit(2)
    return xs[0]


P_JSON, P_MD, P_REP = one(JF, "json"), one(MF, "datamd"), one(RF, "report")
P_ZH, P_JU, P_H = one(ZF, "zheng"), one(JUF, "judgment"), one(HF, "html")
P_E, P_RUN = one(EF, "engine"), one(RUN, "runner")
OURS = [P_JSON, P_MD, P_REP, P_ZH, P_JU, P_H, P_E, P_RUN]
OTHER = sorted(glob.glob(os.path.join(DATA, "TUFT-r317_*")) + glob.glob(os.path.join(DATA, "TUFT-r321_*"))
               + glob.glob(os.path.join(DATA, "TUFT-r308_*.md")))


def rd(p):
    return io.open(p, encoding="utf-8", newline="").read()


def st(p):
    b = open(p, "rb").read()
    return len(b), hashlib.md5(b).hexdigest()


D0 = json.loads(rd(P_JSON))
W = {
    "D": D0,
    "D_RAW": rd(P_JSON),
    "ITEMS": dict((it["id"], it) for it in D0["items"]),
    "MD_TXT": rd(P_MD), "REP_TXT": rd(P_REP), "JU_TXT": rd(P_JU), "ZH_TXT": rd(P_ZH),
    "H_TXT": rd(P_H), "ENG_TXT": rd(P_E), "RUN_TXT": rd(P_RUN),
    "README_TXT": open(README, "rb").read().decode("utf-8"),
    "ST": dict((p, st(p)) for p in OURS + [README]),
    "CHK_SRC": rd(os.path.abspath(__file__)),
}
W["BEFORE_MAP"] = dict((p, st(p)) for p in OURS + [README] + OTHER)
W["AFTER_MAP"] = dict(W["BEFORE_MAP"])


def ids_of(Wv, layer):
    return sorted(i for i in Wv["ITEMS"] if Wv["ITEMS"][i]["layer"] == layer)


# ---------------------------------------------------------------- 解析器（全部从世界文本现推）
def parse_report(txt):
    return dict(re.findall(r"^\[(\S+?)\s*\]\s+(%s)" % "|".join(VERD), txt, re.M))


def parse_md(txt):
    return dict(re.findall(r"^### (\S+) · (%s) · " % "|".join(VERD), txt, re.M))


def parse_ju(txt):
    return dict((m.group(1), m.group(3)) for m in
                re.finditer(r"^\| (\S+) \| (主|控制组|守卫) \| (%s) \|" % "|".join(VERD), txt, re.M))


def printed_anchors(Wv):
    return ([r[0] for r in Wv["ITEMS"]["V11"]["kv"]["rows"]]
            + re.findall(r'ulp_case\("([0-9][0-9.]*)"', Wv["ENG_TXT"]))


def html_anchors(Wv):
    it = Wv["ITEMS"]
    return {"worst_ratio": str(it["V11"]["kv"]["worst_ratio"]),
            "maxrel": str(it["V11"]["kv"]["maxrel"]),
            "H1[:12]": str(it["V13"]["kv"]["H1"])[:12],
            "spread_inv": str(it["V12"]["kv"]["spread_inv"]),
            "S*_dec": str(it["V8"]["kv"]["S_zero_curvature_dec"])}


def readme_section(Wv):
    rt = Wv["README_TXT"]
    i = rt.index("### r320 ·")
    j = rt.find("\n### ", i + 5)
    return rt[i:j if j > 0 else len(rt)]


def face_decl(Wv):
    return dict(re.findall(r"^FACE\s+(\S+)\s+md5=([0-9a-f]{12,})", Wv["REP_TXT"], re.M))


# ---------------------------------------------------------------- 判据
def chk_w0(Wv):
    modes = re.findall(r'''op(?:en|\.open)\([^()]*?,\s*['"]([^'"]*)['"]''', Wv["CHK_SRC"])
    bad = [m for m in modes if m and (m[0] in "wax" or "+" in m)]
    return len(bad) == 0, ("打开模式全名单 %s，写模式 %s 枚。重跑引擎被禁止（引擎会写盘），故幂等性只由 W12/W13 的结构判据复核。"
                           % (sorted(set(modes)), bad))


def chk_w1(Wv):
    rid = {"json": str(Wv["D"]["rid"]),
           "datamd": (re.findall(r"^\| rid \| (\S+) \|", Wv["MD_TXT"], re.M) or ["-"])[0],
           "judgment": (re.findall(r"r3\d\d", Wv["JU_TXT"].split("\n")[0]) or ["-"])[0],
           "report": (re.findall(r"r3\d\d", Wv["REP_TXT"].split("\n")[0]) or ["-"])[0],
           "html": "r320" if "r320" in Wv["H_TXT"] else "-"}
    return all(v == "r320" for v in rid.values()), "实收 %s" % rid


def chk_w2(Wv):
    it = Wv["ITEMS"]
    rr, mm, jj = parse_report(Wv["REP_TXT"]), parse_md(Wv["MD_TXT"]), parse_ju(Wv["JU_TXT"])
    n = len(it)
    n_ids = set(it) == (set(rr) | set(mm) | set(jj))
    counts_ok = n > 0 and n == len(rr) == len(mm) == len(jj)
    hdr = dict(re.findall(r"^\| (条目总数|主条目|PASS|FAIL|BOUNDARY|INFO) \| (\d+) \|", Wv["MD_TXT"], re.M))
    tally = {}
    for i in it:
        tally[it[i]["verdict"]] = tally.get(it[i]["verdict"], 0) + 1
    hdr_ok = (int(hdr.get("条目总数", -1)) == n and int(hdr.get("主条目", -1)) == len(ids_of(Wv, "主"))
              and all(int(hdr.get(k, -1)) == tally.get(k, 0) for k in VERD))
    return counts_ok and n_ids and hdr_ok, (
        "四面条目数 json=%d / report=%d / 数据册段=%d / 判定册表=%d；名册同一=%s；表头 %s vs 现数 %s；主 %d / 控制 %d / 守卫 %d"
        % (n, len(rr), len(mm), len(jj), n_ids, hdr, tally,
           len(ids_of(Wv, "主")), len(ids_of(Wv, "控制组")), len(ids_of(Wv, "守卫"))))


def chk_w3(Wv):
    it = Wv["ITEMS"]
    rr, mm, jj = parse_report(Wv["REP_TXT"]), parse_md(Wv["MD_TXT"]), parse_ju(Wv["JU_TXT"])
    disagree = [i for i in it if not (rr.get(i) == mm.get(i) == jj.get(i) == it[i]["verdict"])]
    return len(disagree) == 0 and len(rr) == len(it), "不一致名单 %s；report 行数 %d vs 条目 %d" % (disagree, len(rr), len(it))


def chk_w4(Wv):
    decl = sorted(re.findall(r'"(V\d+)"', re.findall(r'DESIGN_FAIL\s*=\s*\(([^)]*)\)', Wv["ENG_TXT"])[0]))
    fail_now = sorted(i for i in Wv["ITEMS"] if Wv["ITEMS"][i]["verdict"] == "FAIL")
    sec3 = sorted(set(re.findall(r"\*\*(V\d+)\*\* ★", Wv["JU_TXT"])))
    return (fail_now == decl == sec3 and len(decl) > 0), (
        "实收 %s；引擎预注册 %s；判定册 §三 %s" % (fail_now, decl, sec3))


def chk_w5(Wv):
    zb, zm = Wv["ST"][P_ZH]
    zp = Wv["D"]["zheng"]
    pa = printed_anchors(Wv)
    miss = [t for t in pa if t not in Wv["ZH_TXT"]]
    return (zb == zp["bytes"] and zm == zp["md5"] and not miss and len(pa) >= 12), (
        "正本 %d B / md5 %s（面自报 %d B / %s）；印刷锚 %d 枚（V11 表印刷列 + 引擎 ulp_case 字面量），缺位 %s"
        % (zb, zm[:12], zp["bytes"], zp["md5"][:12], len(pa), miss))


def chk_w6(Wv):
    rows = Wv["ITEMS"]["V11"]["kv"]["rows"]
    bad, ratios = [], []
    for r in rows:
        diff = abs(float(r[1]) - float(r[0]))
        ratios.append(float(r[4]))
        if not (diff <= float(r[3]) and abs(diff - float(r[2])) <= 1e-12 and float(r[4]) < 1.0):
            bad.append(r[0])
    return (not bad and len(ratios) == len(rows) and max(ratios) < 1.0), (
        "复算违反 %s；命中 %d/%d；最紧 %.6f；上界取自面内列 3（印刷字段口径），非本脚本手打"
        % (bad, len(ratios), len(rows), max(ratios)))


def v16_triplet(Wv):
    """kv 分桶 / 判定册行 / 题面 —— 全部转成整数，不许 str≠int 造出假红。"""
    kv = Wv["ITEMS"]["V16"]["kv"]
    bucket = [int(kv["有载体"]), int(kv["部分载体"]), int(kv["无载体"]), int(kv["自认红"])]
    g = re.findall(r"^- V16 §六 九行审计表逐行挂载体（有 (\d+) / 部分 (\d+) / 无 (\d+) / 自认红 (\d+)）",
                   Wv["JU_TXT"], re.M)
    ju = [int(x) for x in g[0]] if g else None
    title = [int(x) for x in re.findall(r"(\d+)", Wv["ITEMS"]["V16"]["title"])]
    return bucket, ju, title, int(kv["n_rows"])


def chk_w7(Wv):
    bucket, ju, title, n_rows = v16_triplet(Wv)
    rows_shape = len(Wv["ITEMS"]["V16"]["kv"]["rows"])
    ok = (sum(bucket) == n_rows == rows_shape == 9 and ju is not None and ju == bucket and title[:4] == bucket)
    return ok, ("kv 分桶 %s 求和 %d；rows 列举 %d 行；判定册行 %s；题面 %s（回归：题面曾硬编码「有载体 6」，且并列和 10≠9）"
                % (bucket, sum(bucket), rows_shape, ju, title[:4]))


def chk_w8(Wv):
    g11 = Wv["ITEMS"]["G11"]["kv"]
    kv = [int(g11[k]) for k in ("n_main", "n_starred", "n_ledger", "n_inter")]
    add = (kv[1] + kv[2] - kv[3] == kv[0] == len(ids_of(Wv, "主")))
    zero = int(g11["n_undeclared"]) == 0 and int(g11["n_ghost"]) == 0
    hit = re.findall(r"主条目 (\d+) = 带★（净增量）(\d+) ∪ 账内点名 (\d+)（交集 (\d+)）", Wv["JU_TXT"])
    prose = [int(x) for x in hit[0]] if hit else None
    ok = add and zero and prose == kv
    return ok, ("G11 kv（主/带★/账内/交集）%s；判定册文字现推 %s；账外=%s 虚挂=%s"
                % (kv, prose, g11["n_undeclared"], g11["n_ghost"]))


def ctl_types(Wv):
    t = {}
    for i in ids_of(Wv, "控制组"):
        k = Wv["ITEMS"][i].get("型") or "-"
        t[k] = t.get(k, 0) + 1
    return t


def chk_w9(Wv):
    t = ctl_types(Wv)
    rej, pos = int(t.get("拒绝型", 0)), int(t.get("正对照", 0))
    all_pass = all(Wv["ITEMS"][i]["verdict"] == "PASS" for i in ids_of(Wv, "控制组"))
    g7_title = (re.findall(r"^### G7 · PASS · (.*)$", Wv["MD_TXT"], re.M) or [""])[0]
    g7_nums = [int(x) for x in re.findall(r"(\d+)", g7_title)]
    ok = (all_pass and len(ids_of(Wv, "控制组")) == 7 and rej == 4 and pos == 3
          and Wv["ITEMS"]["G7"]["verdict"] == "PASS" and g7_nums[:3] == [rej, pos, rej + pos])
    return ok, ("类型现数 %s；G7 verdict=%s；G7 题面数字 %s vs 现数 %s（题面不许硬编码期望值，必须与现数同）"
                % (t, Wv["ITEMS"]["G7"]["verdict"], g7_nums[:3], [rej, pos, rej + pos]))


def chk_w10(Wv):
    h = Wv["H_TXT"]
    keys = re.findall(r'"(%[A-Z0-9_]+%)"', Wv["ENG_TXT"])
    unfilled = sorted({k for k in keys if k in h} | set(re.findall(r"%[A-Z][A-Z0-9_]*%", h)))
    anchors = html_anchors(Wv)
    miss = {k: v for k, v in anchors.items() if v not in h}
    levs = re.findall(r'"%LEV\d%": "%.4f" % \(([0-9.]+)\)', Wv["ENG_TXT"])
    src = {"0.0192353209": str(Wv["ITEMS"]["V13"]["kv"]["H1"]),
           "0.01816": str(Wv["ITEMS"]["V12"]["kv"]["spread_inv"])}
    stale = [l for l in levs if l in src and round(float(src[l]), 4) != round(float(l), 4)]
    disp_miss = [l for l in levs if ("%.4f" % float(l)) not in h]
    ok = (not unfilled and not miss and len(anchors) == 5 and sorted(levs) == sorted(src)
          and not stale and not disp_miss and len(h) > 1000)
    return ok, ("引擎占位键 %d 枚，未填充 %s；招牌锚 %d 枚缺位 %s；硬打展示值 %s（词表脱钩 %s / 舍入脱钩 %s / 显示缺位 %s）；HTML %d 字符"
                % (len(keys), unfilled, len(anchors), miss, levs,
                   [l for l in levs if l not in src], stale, disp_miss, len(h)))


def bug_count(Wv):
    """本卷自抓仪器缺陷枚数：从判定册「五之二」小节的 bullet 现数（不是题面那句自报数字）。"""
    ju = Wv["JU_TXT"]
    i = ju.index("五之二")
    blk = ju[i:]
    blk = blk[:blk.index("\n## ")]
    return len([l for l in blk.splitlines() if l.startswith("- ")])


def chk_w11(Wv):
    rt = Wv["README_TXT"]
    if rt.count("### r320 ·") != 1:
        return False, "键「### r320 ·」实收 %d 枚（必须恰 1）" % rt.count("### r320 ·")
    sec, it = readme_section(Wv), Wv["ITEMS"]
    links = re.findall(r"\]\(([^)\s]+)\)", sec)
    miss_l = [t for t in links if not os.path.exists(os.path.normpath(os.path.join(ROOT, t)))]
    anchors = ["条目 **%d**" % len(it), "主 **%d**" % len(ids_of(Wv, "主")),
               "控制组 **%d/%d**" % (len(ids_of(Wv, "控制组")), len(ids_of(Wv, "控制组"))),
               "守卫 **%d/%d**" % (len(ids_of(Wv, "守卫")), len(ids_of(Wv, "守卫"))),
               "R1–R6 = **%s**" % it["V19"]["kv"]["score"]]
    miss_a = [a for a in anchors if a not in sec]
    n_bug = bug_count(Wv)
    # 只判「登记锚」两处（标题 + 块首），块内 ⑩ 引用的旧字面量不参与：
    # 把全部出现都当成锚会禁掉缺陷自己的引文（本轮实测：块里有一句故意引用「自抓 7 枚」）。
    anchors_bug = (re.findall(r"本卷自抓 (\d+) 枚仪器坑）", sec)
                   + re.findall(r"本卷自抓 (\d+) 枚仪器坑（判定册", sec))
    quoted = [x for x in re.findall(r"自抓 (\d+) 枚仪器坑", sec) if x not in anchors_bug]
    if sorted(set(anchors_bug)) != [str(n_bug)]:
        miss_a = miss_a + ["自抓 N 枚仪器坑（判定册现数 %d，登记锚印 %s；引文不参与 %s）"
                           % (n_bug, anchors_bug, sorted(set(quoted)))]
    return (not miss_l and not miss_a and len(links) >= 5 and len(sec) > 500), (
        "键 1 枚；链接 %d/%d 在盘上（缺 %s）；登记行 %d 枚数字锚缺 %s；自抓锚 %s vs 面 %d（块内引文 %s 不判）；"
        "小节 %d 行（区间已截到下一个 ### 键，不再吃后续卷节）"
        % (len(links) - len(miss_l), len(links), miss_l, len(anchors) + 1, miss_a,
           anchors_bug, n_bug, sorted(set(quoted)), sec.count("\n")))


def chk_w17(Wv):
    """README 的自抓块必须逐字等于由判定册 §五之二 现推的那一行（第三个消费者 = 本复核器）。"""
    try:
        face, n_face, line = SB.block_from_face(ROOT)
    except SB.SelfBugError as e:
        return False, "面侧派生失败：%s" % e
    sec = readme_section(Wv)
    m = SB.BLOCK_RE.search(sec)
    if not m:
        return False, "README 没有自抓块（或块首字样不是「- **★本卷自抓」）"
    disk = re.sub(r"\r\n|\r|\n", "\n", m.group(0)).rstrip("\n")
    cont = disk.count("\n")
    same = disk == line
    # 形状针：断句由组合器负责 ⇒ 块内不该出现「。；」或「。。」。
    # 逐字等式两边同出一把尺，尺子漏剥句号时等式照样绿，所以这一枚只能独立于等式存在（见 M26）。
    # 计数豁免行内代码引文：块里 ⑫ 就在引用这两个形状，裸子串会把缺陷的说明判成缺陷（SB.shape_glue）。
    glue, n_glue, n_span, n_naked = SB.shape_glue(disk)
    diff = None if same else next((i for i in range(min(len(disk), len(line)))
                                  if disk[i] != line[i]), min(len(disk), len(line)))
    return same and not glue, (
        "面 %s §五之二 = %d 枚；README 块 %d 字符（续行 %d 枚，应为 0）、逐字同=%s、"
        "叠句「。；」+「。。」= %d 处 %s（行内代码引文豁免 %d 段，豁免后 %d 字符）%s"
        % (face[:24] + "…", n_face, len(disk), cont, same, n_glue, glue, n_span, n_naked,
           "" if same else "（首个分叉在第 %d 字符：盘 %r vs 面 %r）"
           % (diff, disk[diff - 6:diff + 8], line[diff - 6:diff + 8])))


def chk_w12(Wv):
    before, after = Wv["BEFORE_MAP"], Wv["AFTER_MAP"]
    changed = [p for p in before if after.get(p) != before[p]]
    return (not changed and len(before) >= 10), (
        "看盘对象 %d 个（本卷 8 面 + README + 他卷 r308/r317/r321 面 %d 张），复核期间被改动 %d 个 %s；写入操作 0 次"
        % (len(before), len(OTHER), len(changed), [os.path.basename(c) for c in changed]))


def chk_w13(Wv):
    me = Wv["ST"][P_REP][1]
    self_hit = me in Wv["REP_TXT"]
    reverse = [os.path.basename(p) for p in (P_JSON, P_MD, P_JU, P_H) if me in rd(p)]
    decl = face_decl(Wv)
    bad_face = sorted(os.path.basename(p) for p, hh in decl.items() if hh != st(p)[1])
    ok = (not self_hit and not reverse and len(decl) == 4 and not bad_face)
    return ok, ("自身 md5 %s 在报告面内=%s；其它面引用报告面 md5 %s（无反向环才能三趟收敛）；FACE 行声明 %d 张，与盘不符 %s"
                % (me[:12], self_hit, reverse, len(decl), bad_face))


def chk_w14(Wv):
    """跨卷引用普查：面里钉的每一个「字节/md5」串，按卷分两类。
    (a) 他卷的引用必须逐字带「只作当下观察」限定词（写盘时无法证明他卷会停笔）；
    (b) 本卷面名册与正本的引用只许是「写盘时」的，且此刻必须与盘一致（否则是死账）。"""
    reg = dict((st(p)[1][:12], p) for p in OURS + OTHER + [P_ZH])
    txt = Wv["D_RAW"]
    pins = re.findall(r"\d+ B / md5 ([0-9a-f]{12})(｜[^\"'，。)]*)?", txt)
    ours_b = "r320"
    xv = [h for h, _ in pins if h in reg and ours_b not in os.path.basename(reg[h])]
    bare_xv = sorted(set(os.path.basename(reg[h]) for (h, q) in pins
                         if h in xv and "只作当下观察" not in q))
    stale = sorted(set(h for (h, q) in pins if h not in reg and "只作当下观察" not in q))
    own_pin = len([h for h, _ in pins if h in reg and ours_b in os.path.basename(reg[h])])
    zheng = [h for h, _ in pins if h == st(P_ZH)[1][:12]]
    disclose = ("不可后引" in Wv["JU_TXT"]) and ("当下读数" in Wv["JU_TXT"])
    ok = (bool(xv) and not bare_xv and not stale and bool(zheng) and own_pin > 0 and disclose)
    return ok, ("跨卷钉 %d 枚（缺「只作当下观察」%d 枚 %s）；本卷面钉 %d 枚；"
                "死账钉（盘上已无此面且未声明当下观察）%d 枚 %s；"
                "正本钉 %d 枚；判定册同时披露「当下读数」+「不可后引」=%s"
                % (len(xv), len(bare_xv), bare_xv, own_pin, len(stale), stale,
                   len(zheng), disclose))


def chk_w15(Wv):
    try:
        Wv["RUN_TXT"].encode("ascii")
        ascii_ok = True
    except UnicodeEncodeError:
        ascii_ok = False
    ok = (ascii_ok and "glob" in Wv["RUN_TXT"] and "subprocess" in Wv["RUN_TXT"] and (BS + "u") not in Wv["RUN_TXT"])
    return ok, ("字节 %d；ASCII=%s / glob=%s / subprocess=%s / 含 %su 字面=%s"
                % (Wv["ST"][P_RUN][0], ascii_ok, "glob" in Wv["RUN_TXT"], "subprocess" in Wv["RUN_TXT"],
                   BS, (BS + "u") in Wv["RUN_TXT"]))


def chk_w16(Wv):
    it, md = Wv["ITEMS"], Wv["MD_TXT"]
    sig = {"1/v* = 150 − k": ("150 − k" in md) or ("150−k" in md),
           "S* 分数": str(it["V8"]["kv"]["S_zero_curvature"]) in md,
           "H(1) 闭式": str(it["V13"]["kv"]["H1_closed"]).replace(" ", "") in md.replace(" ", ""),
           "t* 数值": str(it["V6"]["kv"]["t_star"]) in md,
           "λ± 载体": str(it["V9"]["kv"]["eigs"][0]) in md,
           "σ 定价": str(it["V4"]["kv"]["sigma_inv"]) in md}
    return all(sig.values()), "在场 %d/%d；缺位 %s" % (sum(sig.values()), len(sig),
                                                    [k for k, v in sig.items() if not v])


CHECKS = {"W0": chk_w0, "W1": chk_w1, "W2": chk_w2, "W3": chk_w3, "W4": chk_w4, "W5": chk_w5,
          "W6": chk_w6, "W7": chk_w7, "W8": chk_w8, "W9": chk_w9, "W10": chk_w10, "W11": chk_w11,
          "W12": chk_w12, "W13": chk_w13, "W14": chk_w14, "W15": chk_w15, "W16": chk_w16,
          "W17": chk_w17}

TITLES = {
    "W0": "本复核器自身零写入（扫自身源码的打开模式）",
    "W1": "五张面的 rid 通道逐张现读 = r320（不靠文件名）",
    "W2": "条目数四面闭合 + 数据册自报计数由逐条现数复核",
    "W3": "逐条 verdict 四面同口径",
    "W4": "FAIL 主条目 = 引擎预注册 DESIGN_FAIL = 判定册 §三 点名",
    "W5": "正本字节/md5 = JSON 自报 + 印刷读数逐字住在正本里",
    "W6": "§三 半 ulp 独立复算（容差取自印刷字段口径）",
    "W7": "九行审计表：分桶求和 = 行数 = rows 列举，且判定册行/题面/kv 三处同数",
    "W8": "分工账可加性 + 判定册文字与 G11 kv 同数",
    "W9": "控制组 7/7 全绿且类型字段驱动，G7 题面数字由现数复核",
    "W10": "可视化面零未填 %TOKEN% + 招牌锚与 kv 同源 + 硬打展示值不脱钩",
    "W11": "README 登记：键恰 1 枚、链接全在盘、数字锚与面现数一致",
    "W12": "零写入见证：看盘对象复核前后逐字节相同",
    "W13": "报告面不含自身 md5、无反向引用环，FACE 行声明与盘一致",
    "W14": "跨卷钉普查：他卷引用必带「只作当下观察」，本卷钉与正本钉须与盘一致",
    "W15": "runner 纯 ASCII、按前缀 glob、无 %su 字面" % BS,
    "W16": "六枚招牌恒等式/读数在数据册逐字在场",
    "W17": "README 自抓块逐字 = 判定册 §五之二 现推的那一行（无续行、无手打）+ 断句由组合器负责（叠句「。；」「。。」计数豁免行内代码引文，豁免段数现印）",
}

# ---------------------------------------------------------------- 变异体（只改世界副本，绝不落盘）
MUT = []


def mutant(name, tid, field, transform):
    live_ok, _ = CHECKS[tid](W)
    if not live_ok:
        MUT.append((name, "PRE-CONTROL-RED(%s)" % tid))
        return
    base = W[field]
    try:
        new = transform(copy.deepcopy(base) if isinstance(base, (dict, list)) else base)
    except Exception as e:
        MUT.append((name, "CRASH-TRANSFORM(%s:%s)" % (type(e).__name__, e)))
        return
    if new == base:
        MUT.append((name, "NO-OP(%s)" % tid))
        return
    mutated = dict(W)
    mutated[field] = new
    try:
        ok, _ = CHECKS[tid](mutated)
    except Exception as e:
        MUT.append((name, "CRASH-MUT(%s:%s)" % (type(e).__name__, e)))
        return
    MUT.append((name, ("RED(%s)" % tid) if ok is False else "NOT REACHED(%s)" % tid))


def m_bytes_plus1(d):
    d["zheng"] = dict(d["zheng"], bytes=d["zheng"]["bytes"] + 1)
    return d


def m_zero_bound(it):
    it["V11"]["kv"]["rows"] = [[r[0], r[1], r[2], "0", r[4]] for r in it["V11"]["kv"]["rows"]]
    return it


def m_unfill(h):
    return h.replace(html_anchors(W)["worst_ratio"], "%RATIO%", 1)


def m_readme_anchor(t):
    i = t.index("### r320 ·")
    j = t.find("\n### ", i + 5)
    return t[:i] + t[i:j].replace("条目 **41**", "条目 **42**", 1) + t[j:]


def m_face_hex(t):
    d = face_decl(W)
    p, hh = sorted(d.items())[0]
    flipped = hh[:6] + ("0" if hh[6] != "0" else "1") + hh[7:]
    return t.replace("md5=" + hh, "md5=" + flipped, 1)


def m_after_map(am):
    k = sorted(am)[0]
    am[k] = (am[k][0] + 1, am[k][1])
    return am


def m_strip_live(t):
    return re.sub(r"｜[^\"'，。)]*只作当下观察，不可后引", "", t)


def m_orphan_pin(t):
    # 伪造一枚「盘上无人认领、又不声明自己是当下读数」的钉：正是本轮 r321 面移动后留下的死账形状
    return t.replace('"rid": "r320"', '"ghost_face": "9999 B / md5 %s", "rid": "r320"' % (STUB_HEX), 1)


mutant("M01 植入写模式（模式串现场拼，免得尺读到自己的字面量）", "W0", "CHK_SRC",
       lambda t: t + '\nopen(P_JSON, "%s" + "%s")\n' % ("w", "b"))
mutant("M02 数据册 rid 改 r319", "W1", "MD_TXT", lambda t: t.replace("| rid | r320 |", "| rid | r319 |"))
mutant("M03 report 删 V15 整行（判集塌陷）", "W2", "REP_TXT",
       lambda t: re.sub(r"^\[V15[^\n]*\n", "", t, count=1, flags=re.M))
mutant("M04 数据册表头条目总数 41→42", "W2", "MD_TXT",
       lambda t: t.replace("| 条目总数 | 41 |", "| 条目总数 | 42 |"))
mutant("M05 report 里 V1 的 verdict 改 FAIL", "W3", "REP_TXT",
       lambda t: re.sub(r"^\[V1\s*\]\s+PASS", "[V1] FAIL", t, count=1, flags=re.M))
mutant("M06 判定册 §三 名册丢掉 V17 的★", "W4", "JU_TXT", lambda t: t.replace("**V17** ★", "**V17** ○"))
mutant("M07 正本字节数 +1（尺寸引用脱钩）", "W5", "D", m_bytes_plus1)
mutant("M08 正本丢弃一枚印刷读数", "W5", "ZH_TXT", lambda t: t.replace(printed_anchors(W)[0], "【删】"))
mutant("M09 半 ulp 上界全改 0（容差不再是印刷字段口径）", "W6", "ITEMS", m_zero_bound)
mutant("M10 判定册分桶行改回硬编码「有 6」（本轮修好的那枚回归）", "W7", "JU_TXT",
       lambda t: t.replace("（有 5 / 部分 2 / 无 1 / 自认红 1）", "（有 6 / 部分 2 / 无 1 / 自认红 1）"))
mutant("M11 重叠账交集 6→5（可加性破）", "W8", "JU_TXT", lambda t: t.replace("（交集 6）", "（交集 5）"))
mutant("M12 G7 题面拒绝型 4→5、总数 7→8", "W9", "MD_TXT",
       lambda t: t.replace("拒绝型 4 + 正对照 3 = 7", "拒绝型 5 + 正对照 3 = 8"))
mutant("M13 可视化面把最紧比值退回未填占位", "W10", "H_TXT", m_unfill)
mutant("M14 可视化面改掉残余历史读数", "W10", "H_TXT", lambda t: t.replace("0.018159972", "0.018999999"))
def m_readme_stale_bugcount(t):
    i = t.index("### r320 ·")
    j = t.find("\n### ", i + 5)
    n = bug_count(W)
    return t[:i] + t[i:j].replace("本卷自抓 %d 枚仪器坑" % n, "本卷自抓 %d 枚仪器坑" % (n - 3)) + t[j:]


def m_readme_hand_append(t):
    """复现本轮修掉的那一型：块里再手打一个续行（并打错趟→趛）。枚数不变 ⇒ W11 仍绿，只有 W17 能抓。
    必须在本卷小节内定位：`- **★本卷自抓` 在别的卷小节里也存在（首轮就插错了人家卷里 ⇒ NOT REACHED）。"""
    i = t.index("- **\u2605\u672c\u5377\u81ea\u6293", t.index("### r320 ·"))
    j = t.find("\n", i)
    # 插在行尾之后而不是替换掉那个换行：直接塞 "CR LF" 会和前一个 CR 拼成 CR CR LF，
    # 续行正则读不到 ⇒ 变异体假性不达标（本轮实测踩过一次 NOT REACHED）。
    return t[:j] + "\n    \u2469 \u624b\u6253\u7eed\u884c\uff08\u7b2c\u4e00\u8d9b\u843d\u76d8\uff09\n" + t[j:]


mutant("M15 README 登记行条目 41→42（只改 r320 小节内）", "W11", "README_TXT", m_readme_anchor)
mutant("M16 模拟在飞：看盘名单里任一对象尺寸 +1", "W12", "AFTER_MAP", m_after_map)
mutant("M17 报告面写进自身 md5（递归自哈希复活）", "W13", "REP_TXT",
       lambda t: t + "\n[SELF-HASH] " + W["ST"][P_REP][1] + "\n")
mutant("M18 FACE 行声明的某张面 md5 改一个十六进制位", "W13", "REP_TXT", m_face_hex)
mutant("M19 判定册把「不可后引」披露改成「可后引」", "W14", "JU_TXT", lambda t: t.replace("不可后引", "可后引"))
mutant("M22 剥掉跨卷钉的当下观察限定词（死账复活的形状）", "W14", "D_RAW", m_strip_live)
mutant("M23 钉一张盘上不存在的他卷面且不声明当下观察", "W14", "D_RAW", m_orphan_pin)
mutant("M24 README 的自抓枚数退回面数 -3（判定册现数由面驱动，不手打）", "W11", "README_TXT", m_readme_stale_bugcount)
mutant("M25 README 自抓块被手打出一个续行（枚数不动，只有 W17 能抓）", "W17", "README_TXT", m_readme_hand_append)
mutant("M20 runner 里植入一个中文字", "W15", "RUN_TXT", lambda t: t + "\n# 中文\n")
mutant("M21 数据册把 S* 分数改一位", "W16", "MD_TXT", lambda t: t.replace("-506250000/2571353", "-506250000/2571354"))

# M26 双面变异：把组合器退回「不剥句号」，同时把 README 的块换成退回后的那一行。
# 盘与面同出一把尺 ⇒ 枚数（W11）与逐字等式（W17 第一枚）都还绿，只有形状针会红。
# 没有这一枚，「尺子自己漏剥句号」就是零判决面上的自由变异——形状针也就没被定价。
def _retro_compose(n, items):
    return "- **%s %d 枚仪器坑（判定册 §五之二逐条登记，全部就地修）**：%s" % (
        SB.LABEL, n, "；".join("%s %s" % (SB.CIRC[i], b) for i, b in enumerate(items)) + "。")


M26 = "M26 组合器与 README 同步退回叠句（枚数与逐字等式仍绿，只有形状针红）"
_ok17_live, _ = CHECKS["W17"](W)
if not _ok17_live:
    MUT.append((M26, "PRE-CONTROL-RED(W17)"))
else:
    _compose_orig = SB.compose_readme_line
    SB.compose_readme_line = _retro_compose
    try:
        _rt = W["README_TXT"]
        _i26 = _rt.index("### r320 ·")
        _j26 = _rt.find("\n### ", _i26 + 5)
        _j26 = _j26 if _j26 > 0 else len(_rt)
        _m26 = SB.BLOCK_RE.search(_rt[_i26:_j26])
        if not _m26:
            MUT.append((M26, "CRASH-TRANSFORM(BLOCK-NOT-FOUND)"))
        else:
            _, _n26, _line26 = SB.block_from_face(ROOT)
            _sec26 = _rt[_i26:_j26]
            _newsec = _sec26[: _m26.start()] + _line26 + _sec26[_m26.end():]
            _disk26 = re.sub(r"\r\n|\r|\n", "\n", SB.BLOCK_RE.search(_newsec).group(0)).rstrip("\n")
            _g26_hits, _g26, _sp26, _ = SB.shape_glue(_disk26)
            _W26 = dict(W)
            _W26["README_TXT"] = _rt[:_i26] + _newsec + _rt[_j26:]
            _ok26, _ = CHECKS["W17"](_W26)
            if _ok26 is not False:
                MUT.append((M26, "NOT REACHED(W17)"))
            elif _disk26 != _line26:
                # 等式两边没同形变 ⇒ 这一枚抓到的是等式不是形状，等于没给它定价
                MUT.append((M26, "NOT-UNIQUE(W17)"))
            elif _g26 == 0:
                MUT.append((M26, "NO-OP(W17)"))
            else:
                MUT.append((M26, "RED(W17) \u9010\u5b57\u7b49\u5f0f\u7eff\u3001\u53e0\u53e5 %d \u5904 %s\uff08\u8c41\u514d %d \u6bb5\uff09"
                            % (_g26, _g26_hits, _sp26)))
    finally:
        SB.compose_readme_line = _compose_orig

# ---------------------------------------------------------------- 判决
JUD = []
for tid in sorted(CHECKS, key=lambda x: int(x[1:])):
    ok, msg = CHECKS[tid](W)
    JUD.append([tid, ok, msg])
# W12 的真值只有收尾才可得：重测看盘名单后覆盖
W["AFTER_MAP"] = dict((p, st(p)) for p in W["BEFORE_MAP"])
ok12, msg12 = chk_w12(W)
for row in JUD:
    if row[0] == "W12":
        row[1], row[2] = ok12, msg12

cov = sorted({re.search(r"\((W\d+)\)", v).group(1) for _, v in MUT if re.search(r"\((W\d+)\)", v)})
uncovered = sorted(set(CHECKS) - set(cov), key=lambda x: int(x[1:]))
n_break = len([m for m in MUT if m[1].startswith("RED")])
red_ids = [tid for tid, ok, _ in JUD if not ok]

print("=" * 98)
print("TUFT-r320 · 收口只读复核 v6（零写入，期望全部从落盘面现推）")
print("判据 %d 条；变异体 %d 枚覆盖 %d 条判据" % (len(JUD), len(MUT), len(cov)))
print("-" * 98)
for tid, ok, msg in JUD:
    print("[%s] %-6s %s" % (tid, "PASS" if ok else "FAIL", TITLES[tid]))
    print("        %s" % msg)
print("-" * 98)
for name, verdict in MUT:
    print("[MUT] %-26s %s" % (verdict, name))
print("-" * 98)
print("变异体打破 %d/%d；判据红 %d 条 %s" % (n_break, len(MUT), len(red_ids), red_ids))
print("变异体覆盖判据 %d/%d；未覆盖 %s" % (len(cov), len(CHECKS), uncovered))
CHK = "CHK-OK" if (not red_ids and n_break == len(MUT) and not uncovered) else "CHK-INVALID"
print("%s %d/%d 判据 · 变异体 %d/%d 打破 · 覆盖判据 %d/%d"
      % (CHK, len(JUD) - len(red_ids), len(JUD), n_break, len(MUT), len(cov), len(CHECKS)))
sys.exit(0 if CHK == "CHK-OK" else 1)
