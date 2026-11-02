# -*- coding: utf-8 -*-
"""《来料审计论：机检方法论与判决总账》在 openuft/书籍/README.md 的登记器。

模式：--land 写入（幂等、只增不删）｜--check 只读复核（期望取自盘上图像）｜--selftest 变异体自证（零写盘）。
登记行里的每个聚合数都由同目录 _census_report.txt 现场解析；脚本内零手打数字，现析失败 ⇒ 硬失败不写盘。
"""
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)
BOOKS = os.path.dirname(BOOK)
README = os.path.join(BOOKS, "README.md")
REPORT = os.path.join(HERE, "_census_report.txt")

RE_DEN = re.compile(r"判定面分母 = (\d+) 份｜被三把尺之一取到 = (\d+) 份｜没提取到 = (\d+) 份")
RE_TOT = re.compile(r"合计：条目 Σ (\d+) ｜裁定 PASS (\d+) / FAIL (\d+) / BOUNDARY (\d+) / INFO (\d+)")
RE_CTRL = re.compile(r"对照 (\d+)/(\d+) 绿")
RE_NDEF = re.compile(r"闭合破坏面 (\d+) 份")
RE_DEFECT = re.compile(r"· 判定_TUFT-(r\d+)[^：]*：条目 (\d+) vs 四类之和 (\d+)")

ANCHOR_TABLE = "| 《全域双向分形统一场论》"
ANCHOR_TREE = "├── 大纲/"
ROW_PREFIX = "| 《来料审计论：机检方法论与判决总账》"
TREE_PREFIX = "├── 04_来料审计论_机检方法论与判决总账/"

TREE_BLOCK = [
    "├── 04_来料审计论_机检方法论与判决总账/   # 《来料审计论》：审计方法论的实证综述（只读被审卷，不改其字节）",
    "│   ├── README.md            # 书目登记、数字对账表（每个数挂其载体）、与既有册关系、6 条诚实边界",
    "│   ├── 论文_来料主张的机检审计方法与判决总账.md   # 单文件论文版（摘要—方法—结果—讨论—局限—结论—文献）",
    "│   ├── 书稿/                # 卷首 + 第一章~第八章 + 附录（10 件）",
    "│   └── 精算/                # audit_corpus_census.py（只读语料普查，聚合数唯一载体）+ _census_report.txt + .json + 本登记器 + 其 stdout",
]

ROW_TMPL = (
    "| 《来料审计论：机检方法论与判决总账》 | 审计方法论的实证综述（**不提新理论、不做新计算、不新增判据**）："
    "把 ROOT 系列来料的每条主张转成可机读判据，再用具名变异体为每条判决的**判别力**定价；"
    "归纳四种零信息形状（双射⇒0 bit／坐标伪影⇒任意目标可造／自由除数⇒整数住在定义因子里／codim 状态条件⇒随机态命中 0）"
    "与两条准入线（自由度账 n_free ≤ n_obs−1、通过率定价） "
    "| `openuft/书籍/04_来料审计论_机检方法论与判决总账/README.md` "
    "| 成稿 v1.0（2026-11-02）：论文版 1 件＋书稿 10 件＋精算 5 件；聚合数唯一载体 `精算/_census_report.txt`，"
    "本行数字由该面现析——判定面 {den}／可解析 {got}／未提取 {miss} 份｜条目 Σ {items}"
    "（PASS {p}／FAIL {f}／BOUNDARY {b}／INFO {i}）｜对照 {ctrl_ok}/{ctrl_all} 绿"
    "｜★闭合破坏面 {ndef} 份（{defect}）；**全部为时点值，引用前重跑普查**；"
    "6 条诚实边界见其 README §五（覆盖面由针的形状决定、PASS 高≠主张成立、不裁物理真、收录≠背书） |")


def md5s(b):
    return hashlib.md5(b).hexdigest()[:8]


def read_census(txt=None):
    """现析普查面 ⇒ (dict, None)；任一针没提取到 ⇒ (None, 原因)。缺数不得当 0 用。"""
    if txt is None:
        with open(REPORT, "rb") as f:
            txt = f.read().decode("utf-8", "replace").replace("\r\n", "\n")
    d = {}
    for name, rx, keys in (("RE_DEN", RE_DEN, ("den", "got", "miss")),
                           ("RE_TOT", RE_TOT, ("items", "p", "f", "b", "i")),
                           ("RE_CTRL", RE_CTRL, ("ctrl_ok", "ctrl_all"))):
        m = rx.search(txt)
        if not m:
            return None, "%s 没提取到" % name
        for k, v in zip(keys, m.groups()):
            d[k] = int(v)
    m = RE_NDEF.search(txt)
    if not m:
        return None, "RE_NDEF 没提取到"
    d["ndef"] = int(m.group(1))
    hit = RE_DEFECT.search(txt)
    if d["ndef"] == 0:
        if hit:
            return None, "名册仍点名了 %s ⇒ 与「闭合破坏面 0 份」矛盾，拒判" % hit.group(1)
        d["defect"] = "无（本轮普查未抓到头条闭合破坏面）"
        return d, None
    if not hit:
        return None, "报出 %d 份闭合破坏面，但名册那行没提取到 ⇒ 拒判（名数与名册必须同向）" % d["ndef"]
    d["defect"] = "%s：条目 %s vs 四类之和 %s" % hit.groups()
    return d, None


def build_row(d):
    return ROW_TMPL.format(**d)


def line_hits(lines, prefix):
    return [i for i, L in enumerate(lines) if L.startswith(prefix)]


def land_lines(lines, row):
    """内存插入 ⇒ (new_lines, err)。锚点非唯一／已登记／半登记／缺收尾换行一律拒写。"""
    tbl = line_hits(lines, ANCHOR_TABLE)
    rowh = line_hits(lines, ROW_PREFIX)
    tree = line_hits(lines, ANCHOR_TREE)
    blk = line_hits(lines, TREE_PREFIX)
    if lines and lines[-1] != "":
        return None, "面末行不是空行（缺收尾换行符）⇒ 拒写，否则首插会造出无换行的孤儿行"
    if len(tbl) != 1 or len(tree) != 1:
        return None, "锚点不唯一：登记表锚 %d 次／目录树锚 %d 次 ⇒ 拒写（不许挑第一处）" % (len(tbl), len(tree))
    if len(rowh) == 1 and len(blk) == 1:
        return None, "ALREADY-LANDED"
    if len(rowh) == 0 and len(blk) == 0:
        pass
    elif len(rowh) == len(blk):
        return None, "本轮插入块出现 %d 份（>1）⇒ 重复登记，拒写" % len(rowh)
    else:
        return None, "半登记：行 %d 份／树 %d 份 ⇒ 状态不明，拒写" % (len(rowh), len(blk))
    new = list(lines)
    for pos, block in sorted([(tree[0], TREE_BLOCK), (tbl[0], [row])], key=lambda x: -x[0]):
        new[pos:pos] = block
    return new, None


def strip_inserted(lines, row):
    """逐值删掉本轮插入的那 6 行 ⇒ (还原行表, 删掉数, 应删数)。"""
    kill = set(TREE_BLOCK) | {row}
    out, removed = [], 0
    for L in lines:
        if L in kill:
            removed += 1
            continue
        out.append(L)
    return out, removed, len(kill)


def only_added(lines, row, pre_text):
    """只增不删的见证：删回本轮 6 行必须逐字等于写前像。"""
    back, removed, want = strip_inserted(lines, row)
    return removed == want and "\n".join(back) == pre_text, removed, want


def eol_of(raw):
    """面级行尾判定：单一行尾 ⇒ (eol, None)；混杂 ⇒ (None, 原因)。"""
    crlf, lf = raw.count(b"\r\n"), raw.count(b"\n")
    if crlf == lf:
        return (b"\r\n" if crlf else b"\n"), None
    return None, "行尾混杂：CRLF %d／LF %d ⇒ 只认单一行尾的面，拒动" % (crlf, lf)


def load_readme():
    with open(README, "rb") as f:
        raw = f.read()
    _, err = eol_of(raw)
    if err:
        return None, None, err
    return raw, raw.decode("utf-8").replace("\r\n", "\n").split("\n"), None


def git(*args):
    p = subprocess.run(["git", "-C", BOOKS] + list(args), capture_output=True)
    return p.returncode, p.stdout


def cmd_land():
    raw, lines, err = load_readme()
    if err:
        print("FAIL ·", err)
        return 2
    d, err = read_census()
    if err:
        print("FAIL · 普查面现析失败：%s ⇒ 不登记（不得把手打数写进登记表）" % err)
        return 2
    row = build_row(d)
    pre_text = "\n".join(lines)
    new, err = land_lines(lines, row)
    if err == "ALREADY-LANDED":
        ok, out = git("diff", "--numstat", "--", "README.md")
        print("ALREADY-LANDED · 本轮零写盘（二跑 +0 字节）｜md5 %s｜%d B｜git diff --numstat（归一口径）：%s"
              % (md5s(raw), len(raw),
                 out.decode("utf-8", "replace").strip() if ok == 0 else "git 不可用"))
        return cmd_check()
    if err:
        print("REFUSE ·", err)
        return 2
    good, removed, want = only_added(new, row, pre_text)
    if not good:
        print("REFUSE · 只增不删守卫失败（删回 %d/%d 行）" % (removed, want))
        return 2
    img = "\n".join(new).encode("utf-8").replace(b"\n", eol_of(raw)[0])
    with open(README, "wb") as f:
        f.write(img)
    raw2, lines2, err = load_readme()
    if err:
        print("LAND-FAIL · 写后盘上图像不可读：", err)
        return 2
    back, removed, want = strip_inserted(lines2, row)
    c1 = lines2.count(row)
    c2 = sum(1 for L in lines2 if L in set(TREE_BLOCK))
    c3 = md5s("\n".join(back).encode("utf-8")) == md5s(raw)
    print("LANDED · %d B → %d B（+%d）｜md5 %s → %s"
          % (len(raw), len(raw2), len(raw2) - len(raw), md5s(raw), md5s(raw2)))
    print("写后自证（吃盘上图像，期望由本轮插入集现算）")
    print("  C1 登记行逐字节命中恰 1 :: %d" % c1)
    print("  C2 目录树插入块在盘 :: %d/%d 行" % (c2, len(TREE_BLOCK)))
    print("  C3 删回本轮 %d 行 == 写前像（只增不删）:: 实删 %d 行，像等=%s" % (want, removed, c3))
    ok, out = git("diff", "--numstat", "--", "README.md")
    print("  git --numstat（autocrlf 归一口径，只作当下观察）:: %s"
          % (out.decode("utf-8", "replace").strip() if ok == 0 else "git 不可用"))
    return 0 if (c1 == 1 and c2 == len(TREE_BLOCK) and removed == want and c3) else 2


def cmd_check():
    raw, lines, err = load_readme()
    if err:
        print("FAIL ·", err)
        return 2
    d, err = read_census()
    if err:
        print("FAIL · 普查面现析失败：", err)
        return 2
    row = build_row(d)
    hits_row = line_hits(lines, ROW_PREFIX)
    exact = sum(1 for L in lines if L == row)
    hits_tree = line_hits(lines, TREE_PREFIX)
    anchor_tree = len(line_hits(lines, ANCHOR_TREE))
    in_tree = sum(1 for L in lines if L in set(TREE_BLOCK))
    back, removed, want = strip_inserted(lines, row)
    okh, blob = git("show", "HEAD:书籍/README.md")
    wt = "\n".join(back).encode("utf-8")
    eq_exact = okh == 0 and wt == blob
    eq_norm = okh == 0 and wt.replace(b"\r\n", b"\n") == blob.replace(b"\r\n", b"\n")
    print("CHECK · 只读复核（期望取自盘上图像）")
    print("  C1 登记表那行在盘恰 1（按前缀）｜逐字等于现析重建的那一行 :: 前缀 %d｜逐字 %d" % (len(hits_row), exact))
    print("  C2 目录树那块在盘恰 1（按前缀）｜树锚仍恰 1（未被挤掉）｜本轮插入块行数 :: %d｜%d｜%d/%d"
          % (len(hits_tree), anchor_tree, in_tree, len(TREE_BLOCK)))
    print("  C3 本轮 %d 行整块删回 :: 实删 %d 行" % (want, removed))
    print("  C4 删回后与 git HEAD 那份 :: 直接等像=%s｜行尾归一后等像=%s（worktree CRLF=%d，blob CRLF=%d｜autocrlf=true ⇒ 见证走归一口径，%s 只作当下观察）"
          % (eq_exact, eq_norm, raw.count(b"\r\n"), blob.count(b"\r\n") if okh == 0 else -1,
             md5s(blob) if okh == 0 else "HEAD 不可用"))
    good = len(hits_row) == 1 and exact == 1 and len(hits_tree) == 1 and in_tree == len(TREE_BLOCK) \
        and anchor_tree == 1 and removed == want and eq_norm
    print("VERDICT ·", "CHECK-GREEN（两处已登记，登记行逐字节等于普查面重建 ⇒ 无漂移）"
          if good else "CHECK-RED（漂移或未登记：须重跑普查后就地更正，不得二插）")
    return 0 if good else 1


def cmd_selftest():
    """变异体在内存面上打，零写盘；每条判据的期望从前一步的现算值来。"""
    raw, lines, err = load_readme()
    if err:
        print("FAIL ·", err)
        return 2
    d, err = read_census()
    if err:
        print("FAIL · 现析失败（本轮靶面应可解析）：", err)
        return 2
    row = build_row(d)
    # 干净靶面：盘上若已登记，先剪回本轮 6 行（否则变异体无「登记前」可打）
    landed = [L for L in lines if L == row or L in set(TREE_BLOCK)]
    base = [L for L in lines if not (L == row or L in set(TREE_BLOCK))] if len(landed) == 6 else list(lines)
    pre_text = "\n".join(base)
    with open(REPORT, "rb") as f:
        rtxt = f.read().decode("utf-8", "replace").replace("\r\n", "\n")
    print("=== 登记器 · --selftest · 靶 %s ｜变异打在内存面，零写盘 ===" % README)
    res = []

    new, e = land_lines(base, row)
    res.append(("L1 正对照·干净面可登记，且删回本轮 6 行 == 写前像",
                new is not None and e is None and only_added(new, row, pre_text)[0]))
    dup = list(base)
    k = line_hits(dup, ANCHOR_TABLE)[0]
    dup.insert(k, dup[k])
    _, e2 = land_lines(dup, row)
    res.append(("N1 负对照·登记表锚点出现 2 次必须拒写（不许挑第一处）", e2 is not None and "锚点不唯一" in e2))
    half = [L for L in (new or []) if L != row]
    _, e3 = land_lines(half, row)
    res.append(("N2 负对照·半登记（有树无行）必须拒写", e3 is not None and "半登记" in e3))
    cut = "\n".join(L for L in rtxt.split("\n") if not L.lstrip().startswith("合计：条目"))
    d2, e4 = read_census(cut)
    res.append(("N3 负对照·抹掉「合计」行 ⇒ 现析失败而不是给 0（不得用 0 去登记）",
                d2 is None and "RE_TOT" in (e4 or "")))
    d3, e5 = read_census(rtxt.replace("闭合破坏面 1 份", "闭合破坏面 0 份"))
    res.append(("N4 负对照·名数改 0 而名册那行还在 ⇒ 名数与名册矛盾，拒判", d3 is None and "矛盾" in (e5 or "")))
    edited = list(new or [])
    edited[edited.index(row)] = row.replace("条目 Σ %d" % d["items"], "条目 Σ %d" % (d["items"] + 1))
    res.append(("N5 负对照·登后手改登记行 1 个数 ⇒ 删回见证不认，且与现析重建不等",
                not only_added(edited, row, pre_text)[0] and edited.count(row) == 0))
    d4 = dict(d)
    d4["items"] = d["items"] + 1
    res.append(("N6 负对照·漂移侦测有牙：普查数 +1 后重建行不再等于盘上那一行", build_row(d4) != row))
    wrong = [L if L != row else "| 《别的书》 | x | x | x |" for L in (new or [])]
    _, e6 = land_lines(wrong, row)
    res.append(("N7 负对照·别的行冒充 ⇒ 已检测器不得认作本书已登记（须判半登记并拒写）",
                e6 is not None and "ALREADY" not in e6))
    noeof = [l for l in lines if l != ""]
    _, e7 = land_lines(noeof, row)
    res.append(("N8 负对照·面末行缺收尾换行必须拒写（否则首插造孤儿行）", e7 is not None and "末行" in e7))
    res.append(("L2 正对照·已登记面二跑判定 ALREADY-LANDED（不重复插）",
                land_lines(new, row)[1] == "ALREADY-LANDED" if new else False))
    ok = sum(1 for _, g in res if g)
    for name, good in res:
        print(("  [绿] " if good else "  [红] ") + name)
    n = len(res)
    print("对照 %d/%d 绿｜判集 %d 枚（非空=%s）" % (ok, n, n, n > 0))
    return 0 if (ok == n and n > 0) else 1


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode not in ("--land", "--check", "--selftest"):
        print("用法：--land（写入）｜--check（只读复核）｜--selftest（变异体自证）")
        sys.exit(2)
    if not os.path.exists(README) or not os.path.exists(REPORT):
        print("FAIL · 被写面或普查面缺失（README=%s REPORT=%s）⇒ 硬失败，不印 0"
              % (os.path.exists(README), os.path.exists(REPORT)))
        sys.exit(2)
    sys.exit({"--land": cmd_land, "--check": cmd_check, "--selftest": cmd_selftest}[mode]())
