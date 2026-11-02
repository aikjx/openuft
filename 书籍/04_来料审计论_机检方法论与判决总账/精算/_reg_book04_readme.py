# -*- coding: utf-8 -*-
"""《来料审计论：机检方法论与判决总账》在 openuft/书籍/README.md 的登记器。

模式：--land 首次写入（幂等、只增不删）｜--amend 就地更正已登记的行与块（其余行逐字不动）
      ｜--check 只读复核｜--selftest 变异体自证（对被登记面与被审卷零写盘，夹具只落临时目录）。
登记行里的每个聚合数都由同目录 _census_report.txt 现场解析，件数由盘上目录现扫；
脚本内零手打数字，现析失败 ⇒ 硬失败不写盘。
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)
BOOKS = os.path.dirname(BOOK)
README = os.path.join(BOOKS, "README.md")
BOOK_README = os.path.join(BOOK, "README.md")
REPORT = os.path.join(HERE, "_census_report.txt")
CENSUS = "audit_corpus_census.py"
CENSUS_FACE = "_census_report.txt"
CENSUS_JSON = "audit_corpus_census.json"

RE_DEN = re.compile(r"判定面分母 = (\d+) 份｜被三把尺之一取到 = (\d+) 份｜没提取到 = (\d+) 份")
RE_TOT = re.compile(r"合计：条目 Σ (\d+) ｜裁定 PASS (\d+) / FAIL (\d+) / BOUNDARY (\d+) / INFO (\d+)")
RE_CTRL = re.compile(r"对照 (\d+)/(\d+) 绿")
RE_NDEF = re.compile(r"闭合破坏面 (\d+) 份")
RE_DEFECT = re.compile(r"· 判定_TUFT-(r\d+)[^：]*：条目 (\d+) vs 四类之和 (\d+)")
RE_HONEST = re.compile(r"^\d+\. ", re.M)

ANCHOR_TABLE = "| 《全域双向分形统一场论》"
ANCHOR_TREE = "├── 大纲/"
ROW_PREFIX = "| 《来料审计论：机检方法论与判决总账》"
TREE_PREFIX = "├── 04_来料审计论_机检方法论与判决总账/"
TREE_CHILD = "│"

ROW_TMPL = (
    "| 《来料审计论：机检方法论与判决总账》 | 审计方法论的实证综述（**不提新理论、不做新计算、不新增判据**）："
    "把 ROOT 系列来料的每条主张转成可机读判据，再用具名变异体为每条判决的**判别力**定价；"
    "归纳四种零信息形状（双射⇒0 bit／坐标伪影⇒任意目标可造／自由除数⇒整数住在定义因子里／codim 状态条件⇒随机态命中 0）"
    "与两条准入线（自由度账 n_free ≤ n_obs−1、通过率定价） "
    "| `openuft/书籍/04_来料审计论_机检方法论与判决总账/README.md` "
    "| 成稿 v1.0（2026-11-02）：论文版 {n_paper} 件＋书稿 {n_chap} 件（卷首 {n_head}＋正文章 {n_body}＋附录 {n_apx}）"
    "＋精算 {n_num} 件（普查脚本／读数面／json／本登记器／其 stdout 凭据 {n_cred} 份），件数与 {n_honest} 条边界由盘上现扫（取自写盘前像）；"
    "聚合数唯一载体 `精算/_census_report.txt`，"
    "本行数字由该面现析——判定面 {den}／可解析 {got}／未提取 {miss} 份｜条目 Σ {items}"
    "（PASS {p}／FAIL {f}／BOUNDARY {b}／INFO {i}）｜对照 {ctrl_ok}/{ctrl_all} 绿"
    "｜★闭合破坏面 {ndef} 份（{defect}）；**全部为时点值，引用前重跑普查**；"
    "{n_honest} 条诚实边界见其 README §五（覆盖面由针的形状决定、PASS 高≠主张成立、不裁物理真、收录≠背书） |")


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


def scan_num(here):
    """精算/ 件数现扫 ⇒ (dict, None) 或 (None, 原因)。每个文件必须被登记行的名目点名一次。"""
    num = sorted(n for n in os.listdir(here)
                 if os.path.isfile(os.path.join(here, n)) and not n.startswith("__"))
    need = [CENSUS, CENSUS_FACE, CENSUS_JSON]
    reg = [n for n in num if n.startswith("_reg_") and n.endswith(".py")]
    missing = [n for n in need if n not in num] + ([] if reg else ["本登记器 _reg_*.py"])
    if missing:
        return None, "精算/ 缺必需件：%s ⇒ 拒判（不得把缺件报成更小的件数）" % "、".join(missing)
    cred = [n for n in num if n.startswith("_") and n.endswith(".txt") and n != CENSUS_FACE]
    named = set(need) | set(reg) | set(cred)
    other = sorted(set(num) - named)
    if other:
        return None, "精算/ 有 %d 件没被登记行名目覆盖：%s ⇒ 要么点名它，要么移出（不得虚报件数）" % (
            len(other), "、".join(other))
    return {"n_num": len(num), "n_cred": len(cred),
            "n_reg": len(reg), "n_other": len(other)}, None


def read_inventory(book=BOOK, here=HERE, book_readme=BOOK_README):
    """成稿件数现扫（论文版/书稿/精算/诚实边界）⇒ (dict, None)；任一类 0 或加和不闭合 ⇒ 拒判。"""
    d = {}
    d["n_paper"] = len([n for n in os.listdir(book)
                        if n.startswith("论文_") and n.endswith(".md") and os.path.isfile(os.path.join(book, n))])
    if not os.path.isdir(os.path.join(book, "书稿")):
        return None, "书稿/ 目录缺失"
    ch = sorted(n for n in os.listdir(os.path.join(book, "书稿")) if n.endswith(".md"))
    d["n_chap"] = len(ch)
    d["n_head"] = sum(1 for n in ch if "卷首" in n)
    d["n_apx"] = sum(1 for n in ch if "附录" in n)
    d["n_body"] = sum(1 for n in ch if re.search(r"第.{1,3}章", n))
    if min(d["n_paper"], d["n_chap"], d["n_head"], d["n_apx"], d["n_body"]) == 0:
        return None, "件数现扫出现 0 类：%s ⇒ 结构变了（针失效），不许把 0 写进登记表" % d
    if d["n_head"] + d["n_body"] + d["n_apx"] != d["n_chap"]:
        return None, "书稿闭合失败：卷首 %d＋章 %d＋附录 %d != %d ⇒ 有文件名不属这三类，拒判" % (
            d["n_head"], d["n_body"], d["n_apx"], d["n_chap"])
    s, err = scan_num(here)
    if err:
        return None, err
    d.update(s)
    if not os.path.exists(book_readme):
        return None, "本书 README 缺失 ⇒ 诚实边界条数无源"
    with open(book_readme, "rb") as f:
        bt = f.read().decode("utf-8", "replace").replace("\r\n", "\n")
    if "## 五、诚实边界" not in bt:
        return None, "本书 README §五 锚缺失 ⇒ 不许手打边界条数"
    d["n_honest"] = len(RE_HONEST.findall(bt.split("## 五、诚实边界")[1].split("## 六")[0]))
    if d["n_honest"] == 0:
        return None, "§五 现扫到 0 条边界 ⇒ 针失效，不许写 0"
    return d, None


def tree_block(d):
    return [
        TREE_PREFIX + "   # 《来料审计论》：审计方法论的实证综述（只读被审卷，不改其字节）",
        "│   ├── README.md            # 书目登记、数字对账表（每个数挂其载体）、与既有册关系、%d 条诚实边界" % d["n_honest"],
        "│   ├── 论文_来料主张的机检审计方法与判决总账.md   # 单文件论文版（摘要—方法—结果—讨论—局限—结论—文献，%d 件）" % d["n_paper"],
        "│   ├── 书稿/                # 卷首 %d＋第一章~第八章共 %d 章＋附录 %d（合计 %d 件）" % (
            d["n_head"], d["n_body"], d["n_apx"], d["n_chap"]),
        "│   └── 精算/                # %s（只读语料普查，聚合数唯一载体）+ %s + %s + 本登记器%s + 其 stdout 凭据 %d 份（合计 %d 件）" % (
            CENSUS, CENSUS_FACE, CENSUS_JSON, "" if d["n_reg"] == 1 else "×%d" % d["n_reg"], d["n_cred"], d["n_num"]),
    ]


def plan():
    """普查读数 + 盘上件数 ⇒ (dict, row, blk, None) 或 (None, None, None, 原因)。"""
    d, err = read_census()
    if err:
        return None, None, None, "普查面现析失败：%s" % err
    inv, err = read_inventory()
    if err:
        return None, None, None, "件数现扫失败：%s" % err
    d.update(inv)
    return d, ROW_TMPL.format(**d), tree_block(d), None


def line_hits(lines, prefix):
    return [i for i, L in enumerate(lines) if L.startswith(prefix)]


def land_lines(lines, row, blk):
    """内存插入 ⇒ (new_lines, err)。锚点非唯一／已登记／半登记／缺收尾换行一律拒写。"""
    tbl = line_hits(lines, ANCHOR_TABLE)
    rowh = line_hits(lines, ROW_PREFIX)
    tree = line_hits(lines, ANCHOR_TREE)
    blk0 = line_hits(lines, TREE_PREFIX)
    if lines and lines[-1] != "":
        return None, "面末行不是空行（缺收尾换行符）⇒ 拒写，否则首插会造出无换行的孤儿行"
    if len(tbl) != 1 or len(tree) != 1:
        return None, "锚点不唯一：登记表锚 %d 次／目录树锚 %d 次 ⇒ 拒写（不许挑第一处）" % (len(tbl), len(tree))
    if len(rowh) == 1 and len(blk0) == 1:
        return None, "ALREADY-LANDED"
    if len(rowh) == 0 and len(blk0) == 0:
        pass
    elif len(rowh) == len(blk0):
        return None, "本轮插入块出现 %d 份（>1）⇒ 重复登记，拒写" % len(rowh)
    else:
        return None, "半登记：行 %d 份／树 %d 份 ⇒ 状态不明，拒写" % (len(rowh), len(blk0))
    new = list(lines)
    for pos, block in sorted([(tree[0], blk), (tbl[0], [row])], key=lambda x: -x[0]):
        new[pos:pos] = block
    return new, None


def find_landed(lines):
    """结构定位已登记的那行与那棵树 ⇒ (row_idx, (i, k), None)；不恰一份 ⇒ (None, None, 原因)。"""
    rows = line_hits(lines, ROW_PREFIX)
    anchors = line_hits(lines, TREE_PREFIX)
    if len(rows) != 1 or len(anchors) != 1:
        return None, None, "登记行 %d 份／树锚 %d 份 ⇒ 不是一条可就地更正的登记" % (len(rows), len(anchors))
    i = anchors[0]
    k = i + 1
    while k < len(lines) and lines[k].startswith(TREE_CHILD):
        k += 1
    if k - i < 2:
        return None, None, "树锚第 %d 行下没挂子节点（只找到 %d 行）⇒ 结构不符，拒认" % (i, k - i)
    return rows[0], (i, k), None


def cut(lines, ri, span):
    """按索引剪掉已登记的行与块 ⇒ 其余行表（见证「只动了这一块」）。"""
    return [L for j, L in enumerate(lines) if j != ri and not (span[0] <= j < span[1])]


def amend_lines(lines, row, blk):
    """就地更正 ⇒ (new_lines, info, None)；info=None 表示盘上已是重建像（无需更正）。"""
    ri, span, err = find_landed(lines)
    if err:
        return None, None, err
    old_row = lines[ri]
    old_blk = lines[span[0]:span[1]]
    if len(old_blk) != len(blk):
        return None, None, "盘上树块 %d 行 vs 重建 %d 行 ⇒ 有人在块内加/删了行，须人工核对，不覆盖" % (
            len(old_blk), len(blk))
    if old_row == row and old_blk == blk:
        return None, None, None
    new = list(lines)
    for a, b, block in sorted([(ri, ri + 1, [row]), (span[0], span[1], blk)], key=lambda x: -x[0]):
        new[a:b] = block
    ri2, span2, err = find_landed(new)
    if err:
        return None, None, "更正后复核失败：" + err
    if cut(new, ri2, span2) != cut(lines, ri, span):
        return None, None, "更正后「其余行」与更正前不等 ⇒ 动了登记块以外的行，拒写"
    return new, {"old_row": old_row, "new_row": row, "old_blk": old_blk, "new_blk": blk,
                 "n_unchanged": len(cut(new, ri2, span2))}, None


def strip_inserted(lines, row, blk):
    """逐值删掉本轮插入的那几行 ⇒ (还原行表, 删掉数, 应删数)。"""
    kill = set(blk) | {row}
    out, removed = [], 0
    for L in lines:
        if L in kill:
            removed += 1
            continue
        out.append(L)
    return out, removed, len(kill)


def only_added(lines, row, blk, pre_text):
    """只增不删的见证：删回本轮插入行必须逐字等于写前像。"""
    back, removed, want = strip_inserted(lines, row, blk)
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


def _fmt(ok, out):
    return (out.decode("utf-8", "replace").strip() or "（无差异）") if ok == 0 else "git 不可用"


def numstat():
    """git 差异读数：worktree↔HEAD 是累计登记量，worktree↔index 只是本轮那一步。

    并发写入者会宽 `git add`（状态 `MM`），此时裸 `git diff` 只印本轮那一小步 ⇒ 不得当累计账引用。
    """
    a, oa = git("diff", "HEAD", "--numstat", "--", "README.md")
    b, ob = git("diff", "--numstat", "--", "README.md")
    c, oc = git("status", "--porcelain", "--", "README.md")
    return ("累计 worktree↔HEAD :: %s｜本轮 worktree↔index :: %s｜status :: %s（MM ⇒ 别人宽 add 过，索引非权威）"
            % (_fmt(a, oa), _fmt(b, ob), _fmt(c, oc) if c == 0 else "git 不可用"))


def cmd_land():
    raw, lines, err = load_readme()
    if err:
        print("FAIL ·", err)
        return 2
    d, row, blk, err = plan()
    if err:
        print("FAIL · %s ⇒ 不登记（不得把手打数写进登记表）" % err)
        return 2
    pre_text = "\n".join(lines)
    new, err = land_lines(lines, row, blk)
    if err == "ALREADY-LANDED":
        print("ALREADY-LANDED · 本轮零写盘（二跑 +0 字节）｜md5 %s｜%d B｜git diff --numstat（归一口径）：%s"
              % (md5s(raw), len(raw), numstat()))
        return cmd_check()
    if err:
        print("REFUSE ·", err)
        return 2
    good, removed, want = only_added(new, row, blk, pre_text)
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
    back, removed, want = strip_inserted(lines2, row, blk)
    c1 = lines2.count(row)
    c2 = sum(1 for L in lines2 if L in set(blk))
    c3 = md5s("\n".join(back).encode("utf-8")) == md5s(raw)
    print("LANDED · %d B → %d B（+%d）｜md5 %s → %s"
          % (len(raw), len(raw2), len(raw2) - len(raw), md5s(raw), md5s(raw2)))
    print("写后自证（吃盘上图像，期望由本轮插入集现算）")
    print("  C1 登记行逐字节命中恰 1 :: %d" % c1)
    print("  C2 目录树插入块在盘 :: %d/%d 行" % (c2, len(blk)))
    print("  C3 删回本轮 %d 行 == 写前像（只增不删）:: 实删 %d 行，像等=%s" % (want, removed, c3))
    print("  git --numstat（autocrlf 归一口径，只作当下观察）:: %s" % numstat())
    return 0 if (c1 == 1 and c2 == len(blk) and removed == want and c3) else 2


def cmd_amend():
    raw, lines, err = load_readme()
    if err:
        print("FAIL ·", err)
        return 2
    d, row, blk, err = plan()
    if err:
        print("FAIL · %s ⇒ 不更正" % err)
        return 2
    new, info, err = amend_lines(lines, row, blk)
    if err:
        print("REFUSE ·", err)
        return 2
    if info is None:
        print("NOTHING-TO-AMEND · 盘上登记行/块已逐字节等于重建像（%d B｜md5 %s）⇒ 零写盘" % (len(raw), md5s(raw)))
        return cmd_check()
    img = "\n".join(new).encode("utf-8").replace(b"\n", eol_of(raw)[0])
    with open(README, "wb") as f:
        f.write(img)
    raw2, lines2, err = load_readme()
    if err:
        print("AMEND-FAIL · 写后盘上图像不可读：", err)
        return 2
    ri, span, err2 = find_landed(lines2)
    ok_img = err2 is None and lines2[ri] == row and lines2[span[0]:span[1]] == blk
    print("AMENDED · %d B → %d B（%+d）｜md5 %s → %s｜登记块外 %d 行逐字未动"
          % (len(raw), len(raw2), len(raw2) - len(raw), md5s(raw), md5s(raw2), info["n_unchanged"]))
    print("更正披露（旧像逐行存档 ⇒ 新像，本凭证即更正记录）")
    if info["old_row"] != info["new_row"]:
        print("  A1 登记行 · 旧 :: %s" % info["old_row"])
        print("      登记行 · 新 :: %s" % info["new_row"])
    else:
        print("  A1 登记行 :: 未动")
    for i, (o, n) in enumerate(zip(info["old_blk"], info["new_blk"])):
        if o != n:
            print("  A2 树块第 %d 行 · 旧 :: %s" % (i + 1, o))
            print("      树块第 %d 行 · 新 :: %s" % (i + 1, n))
    print("  A3 写后盘上图像 == 重建像（行 + 块）:: %s" % ok_img)
    print("  A4 只动本轮登记块（守卫在 amend_lines 内，红则不写盘）:: 块外 %d 行等像 = True" % info["n_unchanged"])
    print("  git --numstat（autocrlf 归一口径，只作当下观察）:: %s" % numstat())
    return 0 if ok_img else 2


def doc_cells(book_readme=BOOK_README):
    """本书 README §三 对账表的 (行首格, 数值格) 对；行首格缺失 ⇒ 由调用方判红（不许当作「无需核对」）。"""
    with open(book_readme, "rb") as f:
        bt = f.read().decode("utf-8", "replace").replace("\r\n", "\n")
    cells = {}
    for L in bt.split("\n"):
        if not L.startswith("|"):
            continue
        c = [x.strip() for x in L.strip().strip("|").split("|")]
        if len(c) >= 2:
            cells.setdefault(c[0], c[1])
    return cells


def check_book_doc(d, here=HERE, book_readme=BOOK_README):
    """把「抄进文档的读数」逐条打回其载体面（普查面＋登记器自检面）⇒ 文档不是第二权威源，红了就是债。"""
    cs = doc_cells(book_readme)
    size = os.path.getsize(os.path.join(here, CENSUS_FACE))
    with open(os.path.join(here, CENSUS_FACE), "rb") as f:
        face_md5 = md5s(f.read())
    st_face = os.path.join(here, "_selftest_reg_book04.txt")
    if os.path.exists(st_face):
        with open(st_face, "rb") as f:
            m = RE_CTRL.search(f.read().decode("utf-8", "replace"))
        s_ok, s_all = (int(m.group(1)), int(m.group(2))) if m else (None, None)
    else:
        s_ok = s_all = None
    want = [("判定面分母／可解析／未提取", "%d／%d／%d" % (d["den"], d["got"], d["miss"])),
            ("条目 Σ／PASS／FAIL／BOUNDARY／INFO",
             "%d／%d／%d／%d／%d" % (d["items"], d["p"], d["f"], d["b"], d["i"])),
            ("头条闭合破坏面", "%d 份" % d["ndef"]),
            ("普查对照", "%d/%d 绿" % (d["ctrl_ok"], d["ctrl_all"])),
            ("普查对照", "%s B" % format(size, ",").replace(",", " ")),
            ("普查对照", "`%s`" % face_md5)]
    if s_ok is None:
        want = want + [("登记器变异体", "自检面缺失或没印「对照 n/n 绿」⇒ 无载体，不许引用文档值")]
    else:
        want = want + [("登记器变异体", "%d/%d 绿" % (s_ok, s_all))]
    want = want + [("登记表那一行的件数（论文版／书稿／精算／stdout 凭据／诚实边界）",
                    "%d／%d／%d／%d／%d" % (d["n_paper"], d["n_chap"], d["n_num"], d["n_cred"], d["n_honest"]))]
    out = []
    for label, needle in want:
        cell = cs.get(label)
        if cell is None:
            out.append((label, needle, "（§三 没这一行 ⇒ 针失效）", False))
        else:
            out.append((label, needle, cell if needle in cell else cell[:56], needle in cell))
    return out, face_md5, size


def cut_block(lines, row=None, blk=None):
    """剪掉本书登记块 ⇒ 与 HEAD 状态无关的「其余面」。

    优先按结构定位（find_landed）：块里的文本被本轮改写过也剪得掉；结构不符才退回按值删。
    """
    ri, span, err = find_landed(lines)
    if err is None:
        return cut(lines, ri, span), "结构（行 %d＋块 %d~%d）" % (ri, span[0], span[1])
    if row is None:
        return None, err
    back, removed, want = strip_inserted(lines, row, blk or [])
    return back, "按值（删 %d/%d）" % (removed, want)


def cmd_check():
    raw, lines, err = load_readme()
    if err:
        print("FAIL ·", err)
        return 2
    d, row, blk, err = plan()
    if err:
        print("FAIL · %s" % err)
        return 2
    ri, span, terr = find_landed(lines)
    hits_row = line_hits(lines, ROW_PREFIX)
    exact = sum(1 for L in lines if L == row)
    anchor_tree = len(line_hits(lines, ANCHOR_TREE))
    in_tree = sum(1 for L in lines if L in set(blk))
    back, removed, want = strip_inserted(lines, row, blk)
    rem_wt, how_wt = cut_block(lines, row, blk)
    okh, blob = git("show", "HEAD:书籍/README.md")
    head_lines = blob.decode("utf-8", "replace").replace("\r\n", "\n").split("\n") if okh == 0 else None
    rem_head, how_head = (cut_block(head_lines, row, blk) if head_lines is not None else (None, "HEAD 不可用"))
    eq_norm = rem_head is not None and rem_wt == rem_head
    eq_exact = okh == 0 and "\n".join(back).encode("utf-8") == blob
    print("CHECK · 只读复核（期望取自盘上图像 + 盘上件数现扫）")
    print("  C1 登记表那行在盘恰 1（按前缀）｜逐字等于现析重建的那一行 :: 前缀 %d｜逐字 %d" % (len(hits_row), exact))
    print("  C2 目录树那块在盘恰 1（按结构）｜树锚仍恰 1（未被挤掉）｜重建块逐字命中 :: %s｜%d｜%d/%d"
          % ("是" if terr is None else "否", anchor_tree, in_tree, len(blk)))
    print("  C3 本轮 %d 行整块删回 :: 实删 %d 行" % (want, removed))
    print("  C4 各自剪掉本书登记块后的「其余面」等像（工作树↔HEAD，与 HEAD 是否已含本书登记无关）:: %s（工作树 %d 行·口径 %s｜HEAD %s 行·口径 %s）｜含行尾的直接等像只作口径证据=%s（工作树 CRLF=%d↔blob CRLF=%d，autocrlf=true ⇒ 归一口径才是唯一可比；HEAD md5 %s）"
          % (eq_norm, len(rem_wt or []), how_wt,
             len(rem_head) if rem_head is not None else "不可用", how_head,
             eq_exact, raw.count(b"\r\n"), blob.count(b"\r\n") if okh == 0 else -1,
             md5s(blob) if okh == 0 else "不可用"))
    oks, oidx = git("show", ":书籍/README.md")
    head_has = okh == 0 and "《来料审计论：机检方法论与判决总账》" in blob.decode("utf-8", "replace")
    idx_has = oks == 0 and "《来料审计论：机检方法论与判决总账》" in oidx.decode("utf-8", "replace")
    print("  C5 本书登记在 git 各层的存在性（决定 numstat 该读哪一口径）:: HEAD=%s｜index=%s｜工作树=是（本面 %d 行）"
          % ("已含（有人提交过本书登记）" if head_has else "未含",
             "已含（有人 add 过）" if idx_has else "未含", len(lines)))
    red = []
    if os.path.exists(BOOK_README):
        rows, face_md5, face_size = check_book_doc(d)
        for label, needle, cell, good in rows:
            if not good:
                red.append((label, needle, cell))
        print("  C6 本书 README §三 抄录的读数逐条打回其载体面（普查面＋登记器自检面，%d 针）:: %s（面 %d B｜md5 %s）"
              % (len(rows), "全绿" if not red else "红 %d 条" % len(red), face_size, face_md5))
        for label, needle, cell in red:
            print("      [红] %s :: 面上重建=%s｜文档=%s" % (label, needle, cell))
    else:
        print("  C6 :: FAIL · 本书 README 缺失 ⇒ 抄录账无从核对")
        red.append(("本书 README", "存在", "缺失"))
    good = (len(hits_row) == 1 and exact == 1 and terr is None and span[1] - span[0] == len(blk)
            and in_tree == len(blk) and anchor_tree == 1 and removed == want and eq_norm and not red)
    print("VERDICT ·", "CHECK-GREEN（登记行逐字节等于普查面重建 ⇒ 无漂移）"
          if good else "CHECK-RED（漂移或未登记：重跑普查后用 --amend 就地更正，不得二插）")
    return 0 if good else 1


def cmd_selftest():
    """变异体在内存面上打；夹具只落临时目录，被登记面与被审卷零写盘。"""
    raw, lines, err = load_readme()
    if err:
        print("FAIL ·", err)
        return 2
    d, row, blk, err = plan()
    if err:
        print("FAIL · 现析失败（本轮靶面应可解析）：", err)
        return 2
    # 干净靶面：盘上若已登记，先按结构剪回登记块（否则变异体无「登记前」可打）
    ri, span, terr = find_landed(lines)
    base = cut(lines, ri, span) if terr is None else list(lines)
    pre_text = "\n".join(base)
    with open(REPORT, "rb") as f:
        rtxt = f.read().decode("utf-8", "replace").replace("\r\n", "\n")
    print("=== 登记器 · --selftest · 靶 %s ｜变异打在内存面，零写盘 ===" % README)
    print("盘上已登记：%s｜登记块外 %d 行｜重建：行 1 + 树 %d 行，件数现扫 论文 %d／书稿 %d／精算 %d（凭据 %d）／边界 %d"
          % ("是" if terr is None else "否", len(base), len(blk), d["n_paper"], d["n_chap"], d["n_num"],
             d["n_cred"], d["n_honest"]))
    res = []

    new, e = land_lines(base, row, blk)
    res.append(("L1 正对照·干净面可登记，且删回本轮插入行 == 写前像",
                new is not None and e is None and only_added(new, row, blk, pre_text)[0]))
    dup = list(base)
    k = line_hits(dup, ANCHOR_TABLE)[0]
    dup.insert(k, dup[k])
    _, e2 = land_lines(dup, row, blk)
    res.append(("N1 负对照·登记表锚点出现 2 次必须拒写（不许挑第一处）", e2 is not None and "锚点不唯一" in e2))
    half = [L for L in (new or []) if L != row]
    _, e3 = land_lines(half, row, blk)
    res.append(("N2 负对照·半登记（有树无行）必须拒写", e3 is not None and "半登记" in e3))
    cut_r = "\n".join(L for L in rtxt.split("\n") if not L.lstrip().startswith("合计：条目"))
    d2, e4 = read_census(cut_r)
    res.append(("N3 负对照·抹掉「合计」行 ⇒ 现析失败而不是给 0（不得用 0 去登记）",
                d2 is None and "RE_TOT" in (e4 or "")))
    d3, e5 = read_census(rtxt.replace("闭合破坏面 1 份", "闭合破坏面 0 份"))
    res.append(("N4 负对照·名数改 0 而名册那行还在 ⇒ 名数与名册矛盾，拒判", d3 is None and "矛盾" in (e5 or "")))
    edited = list(new or [])
    edited[edited.index(row)] = row.replace("条目 Σ %d" % d["items"], "条目 Σ %d" % (d["items"] + 1))
    res.append(("N5 负对照·登后手改登记行 1 个数 ⇒ 删回见证不认，且与现析重建不等",
                not only_added(edited, row, blk, pre_text)[0] and edited.count(row) == 0))
    d4 = dict(d)
    d4["items"] = d["items"] + 1
    res.append(("N6 负对照·漂移侦测有牙：普查数 +1 后重建行不再等于盘上那一行", ROW_TMPL.format(**d4) != row))
    wrong = [L if L != row else "| 《别的书》 | x | x | x |" for L in (new or [])]
    _, e6 = land_lines(wrong, row, blk)
    res.append(("N7 负对照·别的行冒充 ⇒ 已检测器不得认作本书已登记（须判半登记并拒写）",
                e6 is not None and "ALREADY" not in e6))
    noeof = [l for l in lines if l != ""]
    _, e7 = land_lines(noeof, row, blk)
    res.append(("N8 负对照·面末行缺收尾换行必须拒写（否则首插造孤儿行）", e7 is not None and "末行" in e7))
    res.append(("L2 正对照·已登记面二跑判定 ALREADY-LANDED（不重复插）",
                land_lines(new, row, blk)[1] == "ALREADY-LANDED" if new else False))
    am2, info2, err2 = amend_lines(new or [], row, blk)
    res.append(("L3 正对照·盘上已是重建像 ⇒ --amend 判 NOTHING-TO-AMEND（零写盘，不是第二次插）",
                new is not None and err2 is None and info2 is None))

    # —— 件数针：把已登记的行/块换成「手打的旧数」，--amend 必须抓回且只动那块 ——
    # 靶面 new 的索引由 find_landed(new) 现取（不许复用它处 lines 的索引 ⇒ 面长不同）
    ri_n, span_n, terr_n = find_landed(new or [])
    stale = list(new or [])
    stale_tree = list(blk)
    stale_tree[3] = "│   ├── 书稿/                # 卷首 + 第一章~第八章 + 附录（10 件）"
    stale_tree[4] = "│   └── 精算/                # audit_corpus_census.py + _census_report.txt + .json + 本登记器 + 其 stdout"
    if stale:
        stale[stale.index(row)] = row.replace("精算 %d 件" % d["n_num"], "精算 5 件")
        stale[span_n[0]:span_n[1]] = stale_tree
    am, ainfo, aerr = amend_lines(stale, row, blk) if new is not None else (None, None, "无面")
    ri_a, span_a, terr_a = find_landed(am or [])
    res.append(("N9 负对照·手打件数（盘上 %d 报成 5 且树块用旧措辞）⇒ --amend 换回重建像，块外 %d 行逐字未动、行数不变"
                % (d["n_num"], len(base)),
                am is not None and ainfo is not None and aerr is None and terr_a is None
                and am == new and "精算 5 件" in "\n".join(stale) and len(am) == len(stale)
                and cut(am, ri_a, span_a) == cut(stale, ri_n, span_n)))
    bb = list(new or [])
    if bb:
        bb.insert(span_n[1], "│   ├── 别人在块内新挂的一行.md   # 未知来路")
        _, _, e8 = amend_lines(bb, row, blk)
        res.append(("N10 负对照·盘上树块行数与重建不等（有人在块内加行）⇒ 拒覆盖，交人工核对",
                    e8 is not None and "人工核对" in e8))
        amb = list(new or [])
        amb.insert(amb.index(row), row)
        _, _, e9 = amend_lines(amb, row, blk)
        res.append(("N11 负对照·登记行出现 2 份 ⇒ 不猜哪条是本轮的，拒更正", e9 is not None and "一条可就地更正" in e9))
        stray = list(new or [])
        stray[ri_n] = stray[ri_n].replace("通过率定价", "通过率定价（别人补的字）")
        am3, i3, e13 = amend_lines(stray, row, blk)
        res.append(("N12 正对照·登记行被补字 ⇒ 更正是把该行换回重建像（块外行等像见证仍须成立，故可写）",
                    am3 is not None and i3 is not None and e13 is None and am3.count(row) == 1))
    # —— HEAD 口径针：见证必须与「HEAD 里那一版登记块」无关（并发提交会把旧像带进 HEAD）——
    head_stale = list(new or [])
    if head_stale:
        hri, hspan, h_err = find_landed(head_stale)
        head_stale[hri] = row.replace("精算 %d 件" % d["n_num"], "精算 5 件")
        head_stale[hspan[1] - 1] = "│   └── 精算/                # 旧措辞：+ 本登记器 + 其 stdout"
        rem_h, how_h = cut_block(head_stale, row, blk)
        rem_n, how_n = cut_block(new, row, blk)
        res.append(("L4 正对照·HEAD 里是本书登记的旧像 ⇒ 按结构剪块后与本轮面等像（据此判「别的行没人动」，与 HEAD 版本无关）",
                    h_err is None and how_h.startswith("结构") and rem_h == rem_n and head_stale != new))
        rem_v, how_v = cut_block(stale, row, blk)
        by_value = strip_inserted(stale, row, blk)[0]
        res.append(("N15 负对照·同一陈旧面按值删剪不掉旧措辞 ⇒ 会谎报「登记行被人改了」：按值口径留旧行、结构口径不留",
                    "精算 5 件" in "\n".join(by_value) and "精算 5 件" not in "\n".join(rem_v)
                    and how_v.startswith("结构")))
    tmp = tempfile.mkdtemp(prefix="reg04_fixture_")
    try:
        with open(BOOK_README, "rb") as f:
            doc0 = f.read()
        doc_dir = os.path.join(tmp, "doc")  # 放子目录：scan_num 只数 tmp 根下的文件，夹具不许互相污染（两针混因）
        os.makedirs(doc_dir)
        good_doc = os.path.join(doc_dir, "README_clean.md")
        bad_doc = os.path.join(doc_dir, "README_mutant.md")
        with open(good_doc, "wb") as f:
            f.write(doc0)
        mut_from = ("%d／%d／%d" % (d["den"], d["got"], d["miss"])).encode("utf-8")
        mut_to = ("%d／%d／%d" % (d["den"] - 1, d["got"], d["miss"])).encode("utf-8")
        with open(bad_doc, "wb") as f:
            f.write(doc0.replace(mut_from, mut_to))
        r_clean_all, _, _ = check_book_doc(d, book_readme=good_doc)
        r_bad_all, _, _ = check_book_doc(d, book_readme=bad_doc)
        # 「登记器变异体」那针读的是本脚本自己的 stdout —— --selftest 期间该面正被 shell 重定向截断
        # ⇒ 仪器看不见自己：那针只能由 --check 定价，这里剔除并注明，不许让「读不到」冒充「不绿=文档有债」
        excl = [x for x in r_clean_all if x[0] == "登记器变异体"]
        r_clean = [x for x in r_clean_all if x[0] != "登记器变异体"]
        r_bad = [x for x in r_bad_all if x[0] != "登记器变异体"]
        bad_labels = [x[0] for x in r_bad if not x[3]]
        res.append(("L6 正对照·C6 抄录账针在干净文档上全绿（%d 针，逐针取自载体面；恰 1 针因读自身 stdout 除名）" % len(r_clean),
                    all(x[3] for x in r_clean) and len(r_clean) >= 6 and len(excl) == 1
                    and len(r_clean_all) == len(r_clean) + 1))
        res.append(("N16 负对照·把文档里判定面分母改小 1 ⇒ C6 必须只点名那一针（不是恒绿，也不是全盘红）",
                    bad_labels == ["判定面分母／可解析／未提取"]))
        os.makedirs(os.path.join(tmp, "书稿"))
        for n in (CENSUS, CENSUS_FACE, CENSUS_JSON, "_reg_book04_readme.py", "_land_x.txt", "_check_x.txt"):
            open(os.path.join(tmp, n), "wb").write(b"x")
        f1, e10 = scan_num(tmp)
        os.remove(os.path.join(tmp, CENSUS_JSON))
        f2, e11 = scan_num(tmp)
        open(os.path.join(tmp, CENSUS_JSON), "wb").write(b"x")  # 先复原，否则 N14 打在 N13 的残局上（两针混成一因）
        open(os.path.join(tmp, "别的脚本.py"), "wb").write(b"x")
        f3, e12 = scan_num(tmp)
        res.append(("L5 正对照·完整夹具的件数闭合（精算 6＝点名 4＋凭据 2）",
                    f1 is not None and e10 is None and f1["n_num"] == 6 and f1["n_cred"] == 2))
        res.append(("N13 负对照·挪走 json 必需件 ⇒ 件数现扫硬失败（不得报成「精算 5 件」）",
                    f2 is None and "缺必需件" in (e11 or "")))
        res.append(("N14 负对照·精算里多一件没被名目覆盖 ⇒ 拒判并点名该件（件数不许只报总数）",
                    f3 is None and "没被登记行名目覆盖" in (e12 or "") and "别的脚本.py" in (e12 or "")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok = sum(1 for _, g in res if g)
    for name, good in res:
        print(("  [绿] " if good else "  [红] ") + name)
    n = len(res)
    print("对照 %d/%d 绿｜判集 %d 枚（非空=%s）" % (ok, n, n, n > 0))
    return 0 if (ok == n and n > 0) else 1


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode not in ("--land", "--amend", "--check", "--selftest"):
        print("用法：--land（首次写入）｜--amend（就地更正）｜--check（只读复核）｜--selftest（变异体自证）")
        sys.exit(2)
    if not os.path.exists(README) or not os.path.exists(REPORT):
        print("FAIL · 被写面或普查面缺失（README=%s REPORT=%s）⇒ 硬失败，不印 0"
              % (os.path.exists(README), os.path.exists(REPORT)))
        sys.exit(2)
    sys.exit({"--land": cmd_land, "--amend": cmd_amend, "--check": cmd_check,
              "--selftest": cmd_selftest}[mode]())
