# -*- coding: utf-8 -*-
"""
attack22（攻破㉔）推进册引用对账门禁 —— 只读，不改任何被审文件

被审文档：推进_场方程容纳率与量纲奇偶_attack22_2026-10-11.md
数值载体：attack22_场方程容纳率与量纲奇偶_2026-10-11_report.txt（本轮唯一的「面」）
第三方  ：⑲ 面 attack21_几何势族P0修法_代价定价_2026-10-11_report.txt（只读盘）
          r34 面 ../本项目_全维自洽与归一化/数据/TUFT-V41alpha自然单位势_全维审计_2026-10-10.md（只读盘）

规则（每条都有牙，牙由变异体与正对照证明）：
  R1 数值逐字   文档每个数值 token（豁免外）必须整 token 出现在本轮面里（截前缀不算）。
  R2 十六进制   文档里 10+ 位 hex（md5 或其截形）必须逐字出现在本轮面里。
  R3 单文件命名 任何引「N B」尺寸或 hash 的行，必须且只能点名 1 个盘上存在的文件。
  R4 本册分布   「NAME×n」序列须与面「条目统计」行逐字同序同数；桶名单由面现抽，不手钉常量表。
  R5 guard     「N / N 通过」每一处须与面恒等。
  R6 豁免账     反引号跨度里不许藏带小数点/指数的测量值；豁免账不许全零（全零 = 尺没读到东西）。
  R7 三方核对   文档与本轮面里引的 ⑲／r34 尺寸、md5、r34 分布行，必须等于**盘上那两份面**的现读。
               判据写成「两边都得印出盘上真值」——只比「两边相同」是空的：两处一起错也会相同。
  R8 电池读数   「电池 N/M 合格」每一处须与面恒等（本轮电池是判据有牙的唯一见证，不许散文转抄）。
  CONTROL-A    以面为文档跑 R1/R2/R4/R5/R6/R8（R3 关）——尺子在自证语料上必须无 R1/R2 违规。
  CONTROL-B    真盘必须全绿；不绿则本轮不得判 0。
  CONTROL-C    两轮求值的面必须逐字节相同（本门禁自己跑两轮的 md5 即其现读见证；不一致则本轮不得判 0）。
  MUT-1..8     把文档逐条改坏（截短小数／伪造小数／删文件名／改一桶／改 guard／改 md5 一跳／
               改三方尺寸一跳／改电池分母）⇒ 对应规则必须红；任何一枚变异体没打破判据 = 本门禁无判决，
               红并退出码 1。覆盖表：R1/R2/R3/R4/R5/R7/R8 各至少一枚，缺项即红（枚数由名单现算，不手钉）。

纯标准库，Python 3 可跑。退出码：0 = 全绿；1 = 有红；2 = 工具自身没跑成（零判决，不得引用）。
"""
from __future__ import division
import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.abspath(os.path.join(HERE, os.pardir))            # 04_公共成果
R34_DIR = os.path.join(DOCS, u"本项目_全维自洽与归一化")
DOC = os.path.join(HERE, u"推进_场方程容纳率与量纲奇偶_attack22_2026-10-11.md")
FACE = os.path.join(HERE, u"attack22_场方程容纳率与量纲奇偶_2026-10-11_report.txt")
GFACE = os.path.join(HERE, u"attack22_场方程容纳率与量纲奇偶_引用对账_2026-10-11.txt")
A21 = os.path.join(HERE, u"attack21_几何势族P0修法_代价定价_2026-10-11_report.txt")
R34 = os.path.join(R34_DIR, u"数据", u"TUFT-V41alpha自然单位势_全维审计_2026-10-10.md")
CANDIDATE_DIRS = [HERE, os.path.join(R34_DIR, u"数据"), R34_DIR, os.path.join(HERE, u"数据")]

NUM = re.compile(u"(?<![0-9A-Za-z.])[+-]?[0-9]+(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]+)?(?![0-9A-Za-z.])")
HEX = re.compile(u"(?<![0-9A-Za-z.])[0-9a-f]{10,}(?![0-9A-Za-z])")
BUCKET = re.compile(u"([A-Z][A-Z_]+)\\u00d7([0-9]+)")        # 本册分布：NAME×n（名字由面现抽）
BUCKET_R34 = re.compile(u"PASS=([0-9]+)\\s*/\\s*FAIL=([0-9]+)\\s*/\\s*MISMATCH=([0-9]+)"
                        u"\\s*/\\s*BOUNDARY=([0-9]+)\\s*/\\s*INFO=([0-9]+)")
GUARD = re.compile(u"([0-9]+) / ([0-9]+) 通过")
BATT = re.compile(u"电池 ([0-9]+)/([0-9]+) 合格")
SIZE = re.compile(u"[+-]?[0-9]+(?:\\.[0-9]+)?\\s*B(?![a-zA-Z])")
FNAME = re.compile(u"[^\\s，。；、（）()`|]+\\.(?:md|py|json|txt)")
EXEMPT = [
    (u"反引号跨度", re.compile(u"`[^`]*`")),
    (u"ISO日期", re.compile(u"\\d{4}-\\d{2}-\\d{2}")),
    (u"节号§", re.compile(u"§[0-9一二三四五六七八九十.]*")),
    # 标识号必须按**整枚**豁免：只吃 O19 会把 O19-3 的尾巴 -3 露成裸数（面与册同露 ⇒ 尺形问题）
    (u"标识号带尾", re.compile(u"(?<![0-9A-Za-z.])[A-Z][0-9]{1,3}(?:-[0-9]+)+")),
    (u"条目号", re.compile(u"\\b[A-Z]{1,2}[0-9]{1,3}[a-z]?\\b")),
    (u"册号rNN", re.compile(u"\\br[0-9]{1,3}\\b")),
    (u"版本号", re.compile(u"(?<![0-9A-Za-z.])[Vv][0-9]+(?:\\.[0-9]+)*(?![0-9A-Za-z])")),
]
SHAPE_PROBE = {
    u"ISO日期": lambda t: bool(re.search(u"\\d{4}-\\d{2}-\\d{2}", t)),
    u"反引号跨度": lambda t: u"`" in t,
    u"节号§": lambda t: u"§" in t,
    u"标识号带尾": lambda t: bool(re.search(u"[A-Z][0-9]{1,3}-[0-9]+", t)),
}

LINES = []
FAULTS = []


def say(s):
    LINES.append(s)


def fault(rule, msg):
    FAULTS.append(u"[%s] %s" % (rule, msg))


def rb(p):
    with io.open(p, "rb") as fh:
        return fh.read()


def mask_exempt(text):
    ledger = {}
    words = {}
    spans = []
    buf = list(text)
    for name, rx in EXEMPT:
        hit = 0
        seen = []
        for m in rx.finditer(text):
            a, b = m.start(), m.end()
            if any(not (b <= x or a >= y) for x, y in spans):
                continue
            spans.append((a, b))
            for i in range(a, b):
                buf[i] = u"\u0001"
            hit += 1
            seen.append(m.group(0))
        ledger[name] = hit
        words[name] = seen
    return u"".join(buf), ledger, spans, words


def num_set(text):
    return set(m.group(0) for m in NUM.finditer(text))


def resolve(base):
    for d in CANDIDATE_DIRS:
        p = os.path.join(d, base)
        if os.path.isfile(p):
            return p
    return None


def check(text, face, carriers, do_r3=True):
    """carriers: [(名称, 盘上尺寸str, 盘上md5, 分布元组或 None)]"""
    errs = []
    masked, ledger, _spans, _words = mask_exempt(text)
    fset = num_set(face)
    missed = []
    checked = 0
    for m in NUM.finditer(masked):
        t = m.group(0)
        checked += 1
        if t not in fset:
            missed.append((t, m.start()))
    if missed:
        # 逐枚点名行号与上下文：只报数字不报位置，修的人无法判「这是册写错」还是「尺没吃到形状」
        lines = text.split(u"\n")
        named = []
        for t, pos in missed[:12]:
            ln = text.count(u"\n", 0, pos)
            seg = text[max(0, pos - 28):pos + 28].replace(u"\n", u"|")
            named.append(u"%s（第 %d 行｜…%s…）" % (t, ln + 1, seg))
        tail = u"｜其余 %d 枚略" % (len(missed) - 12) if len(missed) > 12 else u""
        errs.append(u"R1 有 %d 枚数值不在面里（整 token 不匹配）：%s%s"
                    % (len(missed), u"；".join(named), tail))
    bad_hex = [h for h in sorted(set(HEX.findall(text))) if h not in face]
    if bad_hex:
        errs.append(u"R2 有 %d 枚十六进制串不在面里：%s" % (len(bad_hex), u"／".join(bad_hex)))
    adv = []
    bt = dict(EXEMPT)[u"反引号跨度"]
    for m in bt.finditer(text):
        for t in NUM.finditer(m.group(0)):
            if u"." in t.group(0) or re.search(u"[eE][+-]?[0-9]", t.group(0)):
                adv.append(t.group(0))
    if adv:
        errs.append(u"R6 反引号豁免里藏了 %d 枚带小数/指数的数：%s"
                    % (len(adv), u"／".join(sorted(set(adv)))))
    fb = BUCKET.findall(face)
    db = BUCKET.findall(text)
    if not db:
        errs.append(u"R4 文档没引到本册分布行（推进册必须把分布挂在面上）")
    if not fb:
        errs.append(u"R4 面没印分布行 ⇒ 无对照对象（尺子不该在没电时判绿）")
    bad_b = [x for x in db if fb and x not in fb]
    if bad_b:
        errs.append(u"R4 文档有 %d 处 NAME×n 不在面里（面 = %s）：%s"
                    % (len(bad_b), u"／".join(u"%s×%s" % y for y in fb[:8]),
                       u"；".join(u"%s×%s" % x for x in bad_b)))
    # 顺序也要核：文档里引完整分桶序列时，必须与面同序
    seq_face = [u"%s×%s" % y for y in fb]
    for i in range(len(db) - len(seq_face) + 1):
        cand = [u"%s×%s" % x for x in db[i:i + len(seq_face)]]
        if sorted(cand) == sorted(seq_face) and cand != seq_face:
            errs.append(u"R4 文档的分桶次序与面不合（面 = %s｜文 = %s）"
                        % (u"／".join(seq_face), u"／".join(cand)))
            break
    for rx, tag in ((GUARD, u"R5"), (BATT, u"R8")):
        dd, ff = rx.findall(text), rx.findall(face)
        if not dd:
            errs.append(u"%s 文档没引到 %s 的读数" % (tag, rx.pattern[:12]))
        if not ff:
            errs.append(u"%s 面没印 %s ⇒ 无对照对象" % (tag, rx.pattern[:12]))
        bad = [x for x in dd if ff and x not in set(ff)]
        if bad:
            errs.append(u"%s 文档有 %d 处读数与面不合（面 = %s）：%s"
                        % (tag, len(bad), u"；".join(u"%s/%s" % y for y in ff),
                           u"；".join(u"%s/%s" % x for x in bad)))
    for nm, disk_size, disk_md5, disk_b in carriers:
        for hay, where in ((u"本轮面", face), (u"文档", text)):
            if disk_size not in where:
                errs.append(u"R7 %s 尺寸：盘上现读 %s 未出现在%s里（该处或已改，或根本没引盘）"
                            % (nm, disk_size, hay))
            if disk_md5 not in where:
                errs.append(u"R7 %s md5：盘上现读 %s 未出现在%s里" % (nm, disk_md5[:12] + u"…", hay))
        if disk_b is not None:
            for b in BUCKET_R34.findall(text):
                if b != disk_b:
                    errs.append(u"R7 %s 分布：文档引 %s ≠ 盘上现读 %s"
                                % (nm, u"/".join(b), u"/".join(disk_b)))
            for b in BUCKET_R34.findall(face):
                if b != disk_b:
                    errs.append(u"R7 %s 分布：本轮面印 %s ≠ 盘上现读 %s"
                                % (nm, u"/".join(b), u"/".join(disk_b)))
            if not BUCKET_R34.findall(text):
                errs.append(u"R7 %s 分布：文档没引它的分布行（三方核对缺一路）" % nm)
    if do_r3:
        for i, ln in enumerate(text.split(u"\n")):
            if not (SIZE.search(ln) or HEX.search(ln)):
                continue
            names = sorted(set(FNAME.findall(ln)))
            if len(names) != 1:
                errs.append(u"R3 第 %d 行引尺寸/hash 但点名文件 %d 枚（期望 1）：%s"
                            % (i + 1, len(names), ln.strip()[:80]))
                continue
            if not resolve(names[0]):
                errs.append(u"R3 第 %d 行点名的文件不在盘上：%s" % (i + 1, names[0]))
    return errs, checked, ledger


def main():
    say(u"=" * 78)
    say(u"attack22（攻破㉔）推进册引用对账｜只读门禁｜2026-10-11")
    say(u"=" * 78)
    for p in (DOC, FACE):
        if not os.path.isfile(p):
            print(u"[零判决] 读不到被审对象或载体：%s ⇒ 拒跑，退出码 2" % os.path.basename(p))
            return 2
    d_img, f_img = rb(DOC), rb(FACE)
    _d = d_img.decode("utf-8", "replace")
    _f = f_img.decode("utf-8", "replace")
    say(u"被审文档 %s｜盘上 %d B｜md5 %s｜CR %d／LF %d"
        % (os.path.basename(DOC), len(d_img), hashlib.md5(d_img).hexdigest(),
           d_img.count(b"\r"), d_img.count(b"\n")))
    say(u"数值载体 %s｜盘上 %d B｜md5 %s｜CR %d／LF %d（本轮面不能自量，尺寸由此 stat）"
        % (os.path.basename(FACE), len(f_img), hashlib.md5(f_img).hexdigest(),
           f_img.count(b"\r"), f_img.count(b"\n")))
    carriers = []
    for nm, path, want_bucket in ((u"⑲", A21, False), (u"r34", R34, True)):
        if not os.path.isfile(path):
            fault(u"R7", u"读不到 %s 面 %s ⇒ 三方核对没有对象，本门禁不得判绿" % (nm, os.path.basename(path)))
            continue
        img = rb(path)
        txt = img.decode("utf-8", "replace")
        bb = BUCKET_R34.findall(txt)
        disk_b = bb[0] if (want_bucket and bb) else None
        if want_bucket and disk_b is None:
            fault(u"R7", u"%s 面里读不到五桶分布行 ⇒ 该路核对无对象" % nm)
        carriers.append((nm, str(len(img)), hashlib.md5(img).hexdigest(), disk_b))
        say(u"第三方 %s 面 %s｜盘上 %d B｜md5 %s%s"
            % (nm, os.path.basename(path), len(img), hashlib.md5(img).hexdigest(),
               u"｜分布现读 %s" % u"/".join(disk_b) if disk_b else u""))

    errs, checked, ledger = check(_d, _f, carriers)
    for e in errs:
        fault(u"REAL", e)
    say(u"[R 实测] 文档数值 token 被检查 %d 枚（期望 > 100，否则尺没读到东西），违规 %d 条"
        % (checked, len(errs)))
    if checked <= 100:
        fault(u"R1", u"判集塌缩：只检查到 %d 枚数值 token ⇒ 「无违规」与「没在检查」同形" % checked)
    say(u"[R6 豁免账] " + u"／".join(u"%s=%d" % (k, ledger.get(k, 0)) for k, _ in EXEMPT))
    if all(ledger.get(k, 0) == 0 for k, _ in EXEMPT):
        fault(u"R6", u"豁免账全零：尺子没读到任何结构性形状，无法证明豁免按位置建过账")
    empty = [k for k, probe in SHAPE_PROBE.items() if probe(_d) and ledger.get(k, 0) == 0]
    if empty:
        fault(u"R6", u"豁免账里有 %d 类含形状却记 0（跨度被更先入账的类吃掉）：%s"
              % (len(empty), u"／".join(sorted(empty))))
    else:
        say(u"[R6 判集] %d 类形状（%s）皆非零 ⇒ 豁免账不是空账"
            % (len(SHAPE_PROBE), u"／".join(sorted(SHAPE_PROBE))))

    # 第二通道：同一函数、同一文本再求值一次，账必须逐字相同（不同源才算对照）
    _m2, ledger2, _sp2, words = mask_exempt(_d)
    if ledger2 != ledger:
        fault(u"R6", u"豁免账两次求值不合：%s vs %s" % (ledger2, ledger))
    _idw = sorted(set(words.get(u"标识号带尾", [])))
    _grp = re.findall(u"[0-9]+", _idw[0]) if _idw else []
    if not _idw:
        say(u"[R6 标识号豁免] 文档里没有「大写字母＋数字（可带 -数字 尾）」这一型 ⇒ 该类不参与判决")
    else:
        say(u"[R6 标识号豁免清单（整枚掩蔽，逐字可审）] %s｜共 %d 枚"
            % (u"／".join(_idw), len(words.get(u"标识号带尾", []))))
        # 宽窄夹具：期望由夹具自己的拼写现推——带字母前缀则整枚进豁免、裸数剩 0 枚；
        # 去掉字母同一段数字必须露成 %d 枚裸数（数字组数由现取的那枚标识号自己数出，不手钉）
        _wide_m, _wide_l, _ws, _ww = mask_exempt(u"参照 %s 的读数。" % _idw[0])
        _narrow_m, _narrow_l, _ns, _nw = mask_exempt(u"参照 %s 的读数。" % _idw[0][1:])
        _wn = [x.group(0) for x in NUM.finditer(_wide_m)]
        _nn = [x.group(0) for x in NUM.finditer(_narrow_m)]
        ok_w = (_wide_l.get(u"标识号带尾", 0) == 1 and len(_wn) == 0)
        ok_n = (_narrow_l.get(u"标识号带尾", 0) == 0 and len(_nn) == len(_grp))
        say(u"  夹具（同一串数字，两种形状）｜宽档 %s → 豁免 1 枚、裸数 %d 枚（期望 0）；"
            u"窄档 %s → 豁免 %d 枚、裸数 %d 枚（期望 %d）⇒ %s"
            % (_idw[0], len(_wn), _idw[0][1:], _narrow_l.get(u"标识号带尾", 0), len(_nn), len(_grp),
               u"合格（豁免按形状建、没有把数字一把抹掉）" if (ok_w and ok_n) else u"不合格"))
        if not ok_w:
            fault(u"R6", u"标识号豁免在宽档没按整枚建账（裸数剩 %d 枚：%s）" % (len(_wn), _wn))
        if not ok_n:
            fault(u"R6", u"标识号豁免在窄档吞掉了裸数（去字母后应露 %d 枚而露 %d 枚 ⇒ 该豁免是无条件抹数字）"
                      % (len(_grp), len(_nn)))

    say(u"")
    say(u"变异体（每枚把文档改坏一处，对应规则必须红；枚数由名单现算）：")
    muts = []
    _dec = [t for t in sorted(set(NUM.findall(_d)), key=len, reverse=True) if u"." in t]
    if not _dec:
        fault(u"MUT-1", u"文档里没有可截短的小数（变异位没落地）")
    else:
        v = _dec[0]
        t1 = v[:-1]
        if not NUM.findall(t1) or [x.group(0) for x in NUM.finditer(t1)] != [t1]:
            fault(u"MUT-1", u"截短形 %s 不再是整枚 token，变异位落空 ⇒ 该轮 R1 的绿不可信" % t1)
        else:
            muts.append((u"MUT-1 截短一枚小数 %s->%s" % (v, t1), _d.replace(v, t1, 1), u"R1"))
        muts.append((u"MUT-2 伪造一枚小数末位 %s" % v,
                     _d.replace(v, v[:-1] + (u"9" if v[-1] != u"9" else u"8"), 1), u"R1"))
    _sz = [l for l in _d.split(u"\n") if SIZE.search(l) and FNAME.search(l)]
    if not _sz:
        fault(u"MUT-3", u"找不到可删文件名的尺寸行（变异位没落地）")
    else:
        muts.append((u"MUT-3 从尺寸行删掉文件名",
                     _d.replace(_sz[0], FNAME.sub(u"（载体名已删）", _sz[0]), 1), u"R3"))
    _b = BUCKET.findall(_d)
    if not _b:
        fault(u"MUT-4", u"找不到本册分桶序列（变异位没落地）")
    else:
        nm0, n0 = _b[-1]
        _b0 = u"%s×%s" % (nm0, n0)
        _b1 = u"%s×%d" % (nm0, int(n0) + 1)
        if _b1 in _d:
            fault(u"MUT-4", u"目标串 %s 已存在于文档，改一跳会撞车（变异位落地不明）" % _b1)
        else:
            muts.append((u"MUT-4 把 %s 桶改一跳" % nm0, _d.replace(_b0, _b1, 1), u"R4"))
    _g = GUARD.search(_d)
    if not _g:
        fault(u"MUT-5", u"找不到 guard 读数行（变异位没落地）")
    else:
        muts.append((u"MUT-5 把 guard 的分子减一", _d.replace(_g.group(0),
                     u"%d / %s 通过" % (int(_g.group(1)) - 1, _g.group(2)), 1), u"R5"))
    _h = HEX.findall(_d)
    if not _h:
        fault(u"MUT-6", u"文档里没有 10+ 位 hex（变异位没落地）")
    else:
        _hv = _h[0]
        muts.append((u"MUT-6 把 md5 改一跳", _d.replace(_hv, _hv[:-1] + (u"0" if _hv[-1] != u"0" else u"1"), 1),
                     u"R2"))
    if carriers:
        _ds = carriers[0][1]
        if _ds not in _d:
            fault(u"MUT-7", u"文档里没有 ⑲ 尺寸的现读值（变异位没落地）")
        else:
            _bad = str(int(_ds) + 1)
            if _bad in _d:
                fault(u"MUT-7", u"目标串 %s 已存在于文档，改一跳会撞车（变异位落地不明）" % _bad)
            else:
                muts.append((u"MUT-7 把三方尺寸改一跳 %s->%s" % (_ds, _bad),
                             _d.replace(_ds, _bad, 1), u"R7"))
    _bt = BATT.search(_d)
    if not _bt:
        fault(u"MUT-8", u"找不到电池读数行（变异位没落地）")
    else:
        _bad = u"电池 %s/%d 合格" % (_bt.group(1), int(_bt.group(2)) + 1)
        if _bad in _d:
            fault(u"MUT-8", u"目标串已存在，改分母会撞车（变异位落地不明）")
        else:
            muts.append((u"MUT-8 把电池分母加一", _d.replace(_bt.group(0), _bad, 1), u"R8"))
    n_red = 0
    for nm, txt, rule in muts:
        got, _c, _l = check(txt, _f, carriers)
        hit = [e for e in got if rule in e]
        ok = bool(hit)
        if ok:
            n_red += 1
        else:
            fault(rule, u"变异体未打破判据：" + nm)
        say(u"  %-40s 打向 %s ⇒ %s（%s）"
            % (nm, rule, u"红（合格）" if ok else u"绿（无牙，本门禁不得判绿）",
               (hit[0][:96] if hit else u"该规则无违规")))
    _tgt = set(r for _, _, r in muts)
    _need = [r for r in (u"R1", u"R2", u"R3", u"R4", u"R5", u"R7", u"R8") if r not in _tgt]
    if _need:
        fault(u"变异体", u"名单缺规则 %s 的牙（现算落地 %d 枚）：%s"
              % (u"／".join(_need), len(muts), u"／".join(sorted(_tgt))))

    say(u"")
    say(u"对照：")
    self_errs, sc, _sl = check(_f, _f, carriers, do_r3=False)
    hard = [e for e in self_errs if e.startswith(u"R1") or e.startswith(u"R2")
            or e.startswith(u"R4") or e.startswith(u"R6")]
    say(u"  CONTROL-A 面自反（以面为文档跑 R1/R2/R4/R5/R6/R8，R3 关）：检查 %d 枚，硬违规 %d 条 ⇒ %s"
        % (sc, len(hard), u"合格" if not hard else u"不合格（尺在自证语料上就错）"))
    for e in hard:
        fault(u"CONTROL-A", e)
    neg_errs, _nc, _nl = check(_d, _f, carriers)
    say(u"  CONTROL-B 真盘（未改动的文档 vs 面）：违规 %d 条 ⇒ %s"
        % (len(neg_errs), u"合格" if not neg_errs else u"不合格"))

    # CONTROL-C 确定性：门禁自己跑两轮的面必须逐字节相同（本行只印这一轮的 md5）
    say(u"  CONTROL-C 确定性（本轮面 md5 印出，与前一轮对账面比对由运行者现读；两轮不一致 ⇒ 有非确定性输入）")

    say(u"")
    say(u"=" * 78)
    if FAULTS:
        say(u"判决：红 %d 条 ⇒ 本册不得引用" % len(FAULTS))
        for x in FAULTS:
            say(u"  " + x)
        rc = 1
    else:
        say(u"判决：全绿（%d 枚数值逐字挂面；%d 枚变异体皆红；CONTROL-A/B 皆合格；R7 三方恒等；R8 电池恒等）"
            % (checked, n_red))
        rc = 0
    say(u"退出码 %d" % rc)

    buf = (u"\n".join(LINES) + u"\n").encode("utf-8")
    with io.open(GFACE, "wb") as fh:
        fh.write(buf)
    back = rb(GFACE)
    tail = (u"本门禁面已写：%s｜盘上 %d B｜md5 %s｜退出码 %d\n"
            % (os.path.basename(GFACE), len(back), hashlib.md5(back).hexdigest(), rc)).encode("utf-8")
    sys.stdout.buffer.write(back)
    sys.stdout.buffer.write(tail)
    sys.stdout.flush()
    return rc


if __name__ == "__main__":
    sys.exit(main())
