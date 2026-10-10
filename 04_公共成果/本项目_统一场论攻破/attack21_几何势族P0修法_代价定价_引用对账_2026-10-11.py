# -*- coding: utf-8 -*-
"""
attack21（攻破⑲）推进册引用对账门禁 —— 只读，不改任何被审文件

被审文档：推进_几何势族P0修法_attack21_2026-10-11.md
数值载体：attack21_几何势族P0修法_代价定价_2026-10-11_report.txt（本轮唯一的「面」）
第三方  ：../本项目_全维自洽与归一化/数据/TUFT-V41alpha自然单位势_全维审计_2026-10-10.md（r34 面，只读盘）

规则（每条都有牙，牙由变异体与正对照证明）：
  R1 数值逐字   文档每个数值 token（豁免外）必须整 token 出现在本轮面里（截前缀不算）。
  R2 十六进制   文档里 10+ 位 hex（md5 或其截形）必须逐字出现在本轮面里。
  R3 单文件命名 任何引「N B」尺寸或 hash 的行，必须且只能点名 1 个盘上存在的文件。
  R4 本册分布   「PASS×n ／ FAIL×n ／ THEOREM×n ／ BOUNDARY×n ／ INFO×n」每一处都须与面恒等。
  R5 guard     「N / N 通过」每一处须与面恒等。
  R6 豁免账     反引号跨度里不许藏带小数点/指数的测量值；豁免账不许全零（全零 = 尺没读到东西）。
  R7 三方核对   文档与本轮面里引的 r34 尺寸/md5/分布，必须等于**盘上那份 r34 面**的现读。
  CONTROL-A    以面为文档跑 R1/R2/R4/R5/R6（R3 关）——尺子在自证语料上必须无 R1/R2 违规。
  CONTROL-B    真盘必须全绿；不绿则本轮不得判 0。
  MUT-1..7     把文档逐条改坏（截短小数／伪造小数／删文件名／改一桶／改 guard／改 md5 一跳／
               改 r34 尺寸一跳）⇒ 对应规则必须红；任何一枚变异体没打破判据 = 本门禁无判决，红并退出码 1。
               覆盖表：R1/R2/R3/R4/R5/R7 各至少一枚，缺项即红（枚数由名单现算，不手钉）。

纯标准库，Python 3.8 可跑。退出码：0 = 全绿；1 = 有红；2 = 工具自身没跑成（零判决，不得引用）。
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
DOC = os.path.join(HERE, u"推进_几何势族P0修法_attack21_2026-10-11.md")
FACE = os.path.join(HERE, u"attack21_几何势族P0修法_代价定价_2026-10-11_report.txt")
GFACE = os.path.join(HERE, u"attack21_几何势族P0修法_代价定价_引用对账_2026-10-11.txt")
R34 = os.path.join(R34_DIR, u"数据", u"TUFT-V41alpha自然单位势_全维审计_2026-10-10.md")
# R3 点名文件的候选搜索根（面与文档同目录；r34 面在另一册的 数据/ 下）
CANDIDATE_DIRS = [HERE, os.path.join(R34_DIR, u"数据"), R34_DIR, os.path.join(HERE, u"数据")]

NUM = re.compile(u"(?<![0-9A-Za-z.])[+-]?[0-9]+(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]+)?(?![0-9A-Za-z.])")
# hash 尺的边界必须排除「小数的一部分」：0.82999999999999996 里的 17 位数字串不是 md5，
# 让它进 R2/R3 会把纯小数行判成「引 hash 却没点名文件」（本轮第一跑就踩过）。
HEX = re.compile(u"(?<![0-9A-Za-z.])[0-9a-f]{10,}(?![0-9A-Za-z])")
EXEMPT = [
    # 跨度大者先入账：反引号里的文件名天生含 ISO 日期，若日期先入账，
    # 反引号整类会因为「与已掩跨度重叠」被丢弃 ⇒ 豁免账自报 0（假账，判集塌缩）。
    (u"反引号跨度", re.compile(u"`[^`]*`")),
    (u"ISO日期", re.compile(u"\\d{4}-\\d{2}-\\d{2}")),
    (u"节号§", re.compile(u"§[0-9一二三四五六七八九十.]*")),
    (u"条目号", re.compile(u"\\b[A-Z]{1,2}[0-9]{1,3}[a-z]?\\b")),
    (u"册号rNN", re.compile(u"\\br[0-9]{1,3}\\b")),
    (u"版本号", re.compile(u"(?<![0-9A-Za-z.])[Vv][0-9]+(?:\\.[0-9]+)*(?![0-9A-Za-z])")),
]
# 每类豁免的「该不该非零」由文档里是否含该形状的字面字符现推，不手感钉
SHAPE_PROBE = {
    u"ISO日期": lambda t: bool(re.search(u"\\d{4}-\\d{2}-\\d{2}", t)),
    u"反引号跨度": lambda t: u"`" in t,
    u"节号§": lambda t: u"§" in t,
}
BUCKET_SELF = re.compile(u"PASS×([0-9]+)\\s*／\\s*FAIL×([0-9]+)\\s*／\\s*THEOREM×([0-9]+)"
                         u"\\s*／\\s*BOUNDARY×([0-9]+)\\s*／\\s*INFO×([0-9]+)")
BUCKET_R34 = re.compile(u"PASS=([0-9]+)\\s*/\\s*FAIL=([0-9]+)\\s*/\\s*MISMATCH=([0-9]+)"
                        u"\\s*/\\s*BOUNDARY=([0-9]+)\\s*/\\s*INFO=([0-9]+)")
GUARD = re.compile(u"([0-9]+) / ([0-9]+) 通过")
SIZE = re.compile(u"[+-]?[0-9]+(?:\\.[0-9]+)?\\s*B(?![a-zA-Z])")
FNAME = re.compile(u"[^\\s，。；、（）()`|]+\\.(?:md|py|json|txt)")

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
    """按位置建账：先命中的跨度不被后来者嵌套。返回 (掩蔽文本, 账本, 跨度)。"""
    ledger = {}
    spans = []
    buf = list(text)
    for name, rx in EXEMPT:
        hit = 0
        for m in rx.finditer(text):
            a, b = m.start(), m.end()
            if any(not (b <= x or a >= y) for x, y in spans):
                continue
            spans.append((a, b))
            for i in range(a, b):
                buf[i] = u"\u0001"
            hit += 1
        ledger[name] = hit
    return u"".join(buf), ledger, spans


def num_set(text):
    return set(m.group(0) for m in NUM.finditer(text))


def resolve(base):
    for d in CANDIDATE_DIRS:
        p = os.path.join(d, base)
        if os.path.isfile(p):
            return p
    return None


def check(text, face, r34_img, do_r3=True):
    errs = []
    masked, ledger, _spans = mask_exempt(text)
    fset = num_set(face)
    missed = []
    checked = 0
    for m in NUM.finditer(masked):
        t = m.group(0)
        checked += 1
        if t not in fset:
            missed.append(t)
    if missed:
        errs.append(u"R1 有 %d 枚数值不在面里（整 token 不匹配）：%s"
                    % (len(missed), u"／".join(sorted(set(missed)))))
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
    bs = BUCKET_SELF.findall(text)
    fb = BUCKET_SELF.findall(face)
    if not bs:
        errs.append(u"R4 文档没引到本册五桶分布行（推进册必须把分布挂在面上）")
    bad_b = [b for b in bs if fb and b != fb[0]]
    if bad_b:
        errs.append(u"R4 文档有 %d 处分布与面不合（面 = %s）：%s"
                    % (len(bad_b), fb[0] if fb else u"（面没印）", u"；".join(map(u"／".join, bad_b))))
    gg = GUARD.findall(text)
    fg = GUARD.findall(face)
    if not gg:
        errs.append(u"R5 文档没引到「N / N 通过」的 guard 读数")
    bad_g = [x for x in gg if fg and x != fg[0]]
    if bad_g:
        errs.append(u"R5 文档有 %d 处 guard 读数与面不合（面 = %s）：%s"
                    % (len(bad_g), fg[0] if fg else u"（面没印）",
                       u"；".join(u"%s / %s" % x for x in bad_g)))
    # R7 三方：文档与本轮面里引的 r34 尺寸/md5/分布，必须等于**盘上那份 r34 面**的现读。
    # 判据写成「两边都得印出盘上真值」——只比「相同」是空的：两处一起错也会相同。
    if r34_img is not None:
        disk_size = str(len(r34_img))
        disk_md5 = hashlib.md5(r34_img).hexdigest()
        dtext = r34_img.decode("utf-8", "replace")
        dB = BUCKET_R34.findall(dtext)
        dB = dB[0] if dB else None
        for nm, truth, hay in ((u"尺寸", disk_size, u"本轮面"), (u"尺寸", disk_size, u"文档"),
                               (u"md5", disk_md5, u"本轮面"), (u"md5", disk_md5, u"文档")):
            where = face if hay == u"本轮面" else text
            if truth not in where:
                errs.append(u"R7 r34 %s：盘上现读 %s 未出现在%s里（该处或已改，或根本没引盘）" % (nm, truth, hay))
        if dB is None:
            errs.append(u"R7 r34 分布：读不到盘上那份面的分布行 ⇒ 三方核对无对象")
        else:
            for b in BUCKET_R34.findall(text):
                if b != dB:
                    errs.append(u"R7 r34 分布：文档引 %s ≠ 盘上现读 %s" % (u"/".join(b), u"/".join(dB)))
            for b in BUCKET_R34.findall(face):
                if b != dB:
                    errs.append(u"R7 r34 分布：本轮面 T13 印 %s ≠ 盘上现读 %s" % (u"/".join(b), u"/".join(dB)))
            if not BUCKET_R34.findall(text):
                errs.append(u"R7 r34 分布：文档没引 r34 分布行（三方核对缺一路）")
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
    say(u"attack21（攻破⑲）推进册引用对账｜只读门禁｜2026-10-11")
    say(u"=" * 78)
    for p in (DOC, FACE):
        if not os.path.isfile(p):
            print(u"[零判决] 读不到被审对象或载体：%s ⇒ 拒跑，退出码 2" % os.path.basename(p))
            return 2
    d_img, f_img = rb(DOC), rb(FACE)
    r34_img = rb(R34) if os.path.isfile(R34) else None
    _d = d_img.decode("utf-8", "replace")
    _f = f_img.decode("utf-8", "replace")
    say(u"被审文档 %s｜盘上 %d B｜md5 %s｜CR %d／LF %d"
        % (os.path.basename(DOC), len(d_img), hashlib.md5(d_img).hexdigest(),
           d_img.count(b"\r"), d_img.count(b"\n")))
    say(u"数值载体 %s｜盘上 %d B｜md5 %s｜CR %d／LF %d（本轮面不能自量，尺寸由此 stat）"
        % (os.path.basename(FACE), len(f_img), hashlib.md5(f_img).hexdigest(),
           f_img.count(b"\r"), f_img.count(b"\n")))
    say(u"第三方 r34 面 %s"
        % (u"盘上 %d B｜md5 %s" % (len(r34_img), hashlib.md5(r34_img).hexdigest())
           if r34_img is not None else u"读不到 ⇒ R7 弃核（本条不得判绿）"))
    if r34_img is None:
        fault(u"R7", u"读不到 r34 面 ⇒ 三方核对没有对象，本门禁不得判绿")

    errs, checked, ledger = check(_d, _f, r34_img)
    for e in errs:
        fault(u"REAL", e)
    say(u"[R 实测] 文档数值 token 被检查 %d 枚（期望 > 100，否则尺没读到东西），违规 %d 条"
        % (checked, len(errs)))
    if checked <= 100:
        fault(u"R1", u"判集塌缩：只检查到 %d 枚数值 token ⇒ 「无违规」与「没在检查」同形" % checked)
    say(u"[R6 豁免账] " + u"／".join(u"%s=%d" % (k, ledger.get(k, 0)) for k, _ in EXEMPT))
    if all(ledger.get(k, 0) == 0 for k, _ in EXEMPT):
        fault(u"R6", u"豁免账全零：尺子没读到任何结构性形状，无法证明豁免按位置建过账")
    # 判集塌缩按形状逐类点名：文档里含该形状的字面字符，该类就不许读 0
    empty = [k for k, probe in SHAPE_PROBE.items() if probe(_d) and ledger.get(k, 0) == 0]
    if empty:
        fault(u"R6", u"豁免账里有 %d 类含形状却记 0（跨度被更先入账的类吃掉）：%s"
              % (len(empty), u"／".join(sorted(empty))))
    else:
        say(u"[R6 判集] 三类形状（%s）皆非零 ⇒ 豁免账不是空账" % u"／".join(sorted(SHAPE_PROBE)))

    say(u"")
    say(u"变异体（每枚把文档改坏一处，对应规则必须红；枚数由名单现算）：")
    muts = []
    _dec = [t for t in sorted(set(NUM.findall(_d)), key=len, reverse=True) if u"." in t]
    if not _dec:
        fault(u"MUT-1", u"文档里没有可截短的小数（变异位没落地）")
    else:
        v = _dec[0]
        # 截短 = 末位删掉一位，删完仍须是一枚合法 NUM token（删成 "-0." 会被尺当作没数，
        # 那是变异位落空不是判据有牙——本轮第一踩过一次，MUT-1 绿而全绿是假的）
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
    if not BUCKET_SELF.search(_d):
        fault(u"MUT-4", u"找不到本册五桶分布行（变异位没落地）")
    else:
        _b0 = BUCKET_SELF.search(_d).group(0)
        _b1 = _b0.replace(u"INFO×3", u"INFO×4", 1)
        if _b1 == _b0:
            fault(u"MUT-4", u"分布行改不动（变异位没落地）")
        else:
            muts.append((u"MUT-4 把 INFO 桶改一跳", _d.replace(_b0, _b1, 1), u"R4"))
    _g = GUARD.search(_d)
    if not _g:
        fault(u"MUT-5", u"找不到 guard 读数行（变异位没落地）")
    else:
        muts.append((u"MUT-5 把 guard 的分子减一", _d.replace(_g.group(0),
                     u"%d / %s 通过" % (int(_g.group(1)) - 1, _g.group(2)), 1), u"R5"))
    _h = [x for x in HEX.findall(_d)]
    if not _h:
        fault(u"MUT-6", u"文档里没有 10+ 位 hex（变异位没落地）")
    else:
        _hv = _h[0]
        muts.append((u"MUT-6 把 md5 改一跳", _d.replace(_hv, _hv[:-1] + (u"0" if _hv[-1] != u"0" else u"1"), 1),
                     u"R2"))
    if r34_img is not None:
        _ds = str(len(r34_img))
        if _ds not in _d:
            fault(u"MUT-7", u"文档里没有 r34 尺寸的现读值（变异位没落地）")
        else:
            _bad = str(int(_ds) + 1)
            if _bad in _d:
                fault(u"MUT-7", u"目标串 %s 已存在于文档，改一跳会撞车（变异位落地不明）" % _bad)
            else:
                muts.append((u"MUT-7 把 r34 尺寸改一跳 %s->%s" % (_ds, _bad),
                             _d.replace(_ds, _bad, 1), u"R7"))
    n_red = 0
    for nm, txt, rule in muts:
        got, _c, _l = check(txt, _f, r34_img)
        hit = [e for e in got if rule in e]
        ok = bool(hit)
        if ok:
            n_red += 1
        else:
            fault(rule, u"变异体未打破判据：" + nm)
        say(u"  %-40s 打向 %s ⇒ %s（%s）"
            % (nm, rule, u"红（合格）" if ok else u"绿（无牙，本门禁不得判绿）",
               (hit[0][:96] if hit else u"该规则无违规")))
    # 覆盖表由名单现算：每条数值规则至少一枚牙，缺项即红（不手钉「期望 6 枚」）
    _tgt = set(r for _, _, r in muts)
    _need = [r for r in (u"R1", u"R2", u"R3", u"R4", u"R5", u"R7") if r not in _tgt]
    if _need:
        fault(u"变异体", u"名单缺规则 %s 的牙（现算落地 %d 枚）：%s"
              % (u"／".join(_need), len(muts), u"／".join(sorted(set(r for _, _, r in muts)))))

    say(u"")
    say(u"对照：")
    self_errs, sc, _sl = check(_f, _f, r34_img, do_r3=False)
    hard = [e for e in self_errs if e.startswith(u"R1") or e.startswith(u"R2")]
    say(u"  CONTROL-A 面自反（以面为文档跑 R1/R2/R4/R5/R6，R3 关）：检查 %d 枚，R1/R2 违规 %d 条 ⇒ %s"
        % (sc, len(hard), u"合格" if not hard else u"不合格（尺在自证语料上就错）"))
    for e in hard:
        fault(u"CONTROL-A", e)
    neg_errs, _nc, _nl = check(_d, _f, r34_img)
    say(u"  CONTROL-B 真盘（未改动的文档 vs 面）：违规 %d 条 ⇒ %s"
        % (len(neg_errs), u"合格" if not neg_errs else u"不合格"))

    say(u"")
    say(u"=" * 78)
    if FAULTS:
        say(u"判决：红 %d 条 ⇒ 本册不得引用" % len(FAULTS))
        for x in FAULTS:
            say(u"  " + x)
        rc = 1
    else:
        say(u"判决：全绿（%d 枚数值逐字挂面；%d 枚变异体皆红；CONTROL-A/B 皆合格；R7 三方恒等）"
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
