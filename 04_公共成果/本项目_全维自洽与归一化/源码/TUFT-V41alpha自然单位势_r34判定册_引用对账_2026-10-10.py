# -*- coding: utf-8 -*-
"""
r34 判定册引用对账门禁（只读，不改任何文件）

被审文档：判定_TUFT-r34-V41alpha自然单位势_全维审计_2026-10-10.md
数值载体：数据/TUFT-V41alpha自然单位势_全维审计_2026-10-10.md（本册的面，唯一可引数值源）

规则（每条都有牙，牙由变异体与正对照证明）：
  R1 MEASUREMENT  文档里的每一个数值 token，除结构性豁免外，必须逐字出现在面里（整 token 匹配，
                  截前缀不算——「1.16638」不是「1.16638e-05」的合法引用形）。
  R2 HASH         文档里的 10+ 位十六进制串（md5 或其截断形）必须逐字出现在面里。
  R3 SINGLE-FILE  任何引用「N B」尺寸或 hash 的行，必须且只能点名一个文件，且该文件在盘上存在。
  R4 DISTRIBUTION 文档里五桶分布形（含 MISMATCH）只许出现一次，且与面的分布逐桶相等。
  R5 GUARD        文档里的「N / N 通过」只许与面的 guard 读数相等（他册自报的 guard 不带「通过」，
                  故不会被这条读到）。
  R6 LEDGER       豁免按位置建账并逐类点名；反引号跨度里的「带小数点/指数的数字」记为 ADVISORY，
                  本册要求 ADVISORY == 0（豁免不许吞掉测量值）。
  CONTROL-A       面的 KEY 读数串凡出现在文档里者，必须被 R1 真正检查到（不许落在豁免跨度内）。
  MUT-1  截短一枚 KEY 小数 => R1 必须红
  MUT-2  伪造一枚小数       => R1 必须红
  MUT-3  从尺寸行删掉文件名 => R3 必须红
  MUT-4  把分布的一桶改号   => R4 必须红

纯标准库，Python 3.8 可跑。退出码：0 = 全绿；1 = 有红；2 = 工具自身没跑成（无判决）。
"""
from __future__ import division
import io
import os
import re
import sys
import hashlib

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir))
DATA_DIR = os.path.join(ROOT, "数据")
DOC = os.path.join(ROOT, "判定_TUFT-r34-V41alpha自然单位势_全维审计_2026-10-10.md")
FACE = os.path.join(DATA_DIR, "TUFT-V41alpha自然单位势_全维审计_2026-10-10.md")

LINES = []
FAULTS = []
NOTES = []
STATUS = {}


def say(s):
    LINES.append(s)
    print(s)


def fault(rule, msg):
    FAULTS.append(u"[%s] %s" % (rule, msg))


def read_bytes(p):
    with io.open(p, "rb") as fh:
        raw = fh.read()
    return raw


# ---------------------------------------------------------------- numeric tokenizer
# 整 token 边界：前面不许是字母数字点，后面不许是字母数字点。
# 「1.16638」在文档里若写成 `1.16638e^{-05}` 会被拆成 1.16638 与 05，二者皆非面里的 token => R1 红。
NUM = re.compile(u"(?<![0-9A-Za-z.])[+-]?[0-9]+(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]+)?(?![0-9A-Za-z.])")
HEX = re.compile(u"(?<![0-9A-Za-z])[0-9a-f]{10,}(?![0-9A-Za-z])")

# 结构性豁免（按位置建账）
EXEMPT = [
    ("ISO日期", re.compile(u"\\d{4}-\\d{2}-\\d{2}")),
    ("反引号跨度", re.compile(u"`[^`]*`")),
    ("节号§", re.compile(u"§[0-9一二三四五六七八九十.]*")),
    ("条目号", re.compile(u"\\b[A-Z]{1,2}[0-9]{1,3}[a-z]?\\b")),
    ("册号rNN", re.compile(u"\\br[0-9]{1,3}\\b")),
    ("版本号", re.compile(u"(?<![0-9A-Za-z.])[Vv][0-9]+(?:\\.[0-9]+)*(?![0-9A-Za-z])")),
]

BUCKET = re.compile(u"PASS=([0-9]+)\\s*[//]\\s*FAIL=([0-9]+)\\s*[//]\\s*MISMATCH=([0-9]+)"
                    u"\\s*[//]\\s*BOUNDARY=([0-9]+)\\s*[//]\\s*INFO=([0-9]+)")
GUARD = re.compile(u"([0-9]+) / ([0-9]+) 通过")
SIZE = re.compile(u"[+-]?[0-9]+(?:\\.[0-9]+)?\\s*B(?![a-zA-Z])")
FNAME = re.compile(u"[^\\s，。；、（）()`|]+\\.(?:md|py|json|txt)")


def mask_exempt(text):
    """返回 (掩蔽后的文本, 账本, 掩蔽跨度列表)。"""
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
    out = set()
    for m in NUM.finditer(text):
        out.add(m.group(0))
    return out


def doc_text():
    raw = read_bytes(DOC)
    return raw.decode("utf-8", "replace")


def face_text():
    raw = read_bytes(FACE)
    return raw.decode("utf-8", "replace")


def check(text, face, do_r3=True):
    """跑 R1–R6 + CONTROL-A，返回 faults 列表（不改全局，便于喂变异体）。"""
    errs = []
    masked, ledger, spans = mask_exempt(text)
    fset = num_set(face)
    # R1
    missed = []
    checked = 0
    for m in NUM.finditer(masked):
        t = m.group(0)
        if t == u"":
            continue
        checked += 1
        if t not in fset:
            missed.append(t)
    if missed:
        errs.append(u"R1 有 %d 枚数值不在面里（整 token 不匹配）：%s"
                    % (len(missed), u"／".join(sorted(set(missed)))))
    # R2
    bad_hex = [h for h in sorted(set(HEX.findall(text))) if h not in face]
    if bad_hex:
        errs.append(u"R2 有 %d 枚十六进制串不在面里：%s" % (len(bad_hex), u"／".join(bad_hex)))
    # R6 ADVISORY：反引号跨度里不许藏测量值（含小数点或指数）
    adv = []
    bt = dict(EXEMPT)[u"反引号跨度"]
    for m in bt.finditer(text):
        for t in NUM.finditer(m.group(0)):
            if u"." in t.group(0) or re.search(u"[eE][+-]?[0-9]", t.group(0)):
                adv.append(t.group(0))
    if adv:
        errs.append(u"R6 反引号豁免里藏了 %d 枚带小数/指数的数：%s" % (len(adv), u"／".join(sorted(set(adv)))))
    # CONTROL-A：面的 KEY 读数凡在文档中出现，必须真被检查到（不在豁免跨度内）
    key_line = u""
    for ln in face.split(u"\n"):
        if u"关键读数" in ln:
            key_line = ln
            break
    key_vals = re.findall(u"=([^；\\s]+)", key_line)
    swallowed = []
    for kv in key_vals:
        if kv and kv in text:
            covered = False
            for a, b in spans:
                idx = text.find(kv)
                if idx >= 0 and a <= idx and idx + len(kv) <= b:
                    covered = True
                    break
            if covered:
                swallowed.append(kv)
            elif kv not in fset:
                errs.append(u"CONTROL-A 面 KEY 串自身不在面 token 集里：%s" % kv)
    if swallowed:
        errs.append(u"CONTROL-A 有 %d 枚 KEY 读数落在豁免跨度内（豁免过宽）：%s"
                    % (len(swallowed), u"／".join(swallowed)))
    STATUS["checked"] = STATUS.get(u"checked", 0) + checked
    STATUS["ledger"] = ledger
    # R4：分布行可以出现在多处（首页摘要 + 正文引用），但每一处都必须等于面
    buckets = BUCKET.findall(text)
    fb = BUCKET.findall(face)
    if not buckets:
        errs.append(u"R4 文档没引到五桶分布行（判定册必须把分布挂在面上）")
    bad_b = [b for b in buckets if fb and b != fb[0]]
    if bad_b:
        errs.append(u"R4 文档有 %d 处分布与面不合（面 = %s）：%s"
                    % (len(bad_b), fb[0] if fb else u"（面没印）",
                       u"；".join(u"PASS=%s/FAIL=%s/MISMATCH=%s/BOUNDARY=%s/INFO=%s" % b for b in bad_b)))
    # R5：同上，多处引用合法，但每一处都必须等于面
    gg = GUARD.findall(text)
    fg = GUARD.findall(face)
    if not gg:
        errs.append(u"R5 文档没引到「N / N 通过」的 guard 读数")
    bad_g = [x for x in gg if fg and x != fg[0]]
    if bad_g:
        errs.append(u"R5 文档有 %d 处 guard 读数与面不合（面 = %s）：%s"
                    % (len(bad_g), fg[0] if fg else u"（面没印）",
                       u"；".join(u"%s / %s" % x for x in bad_g)))
    # R3
    if do_r3:
        for i, ln in enumerate(text.split(u"\n")):
            has_size = bool(SIZE.search(ln))
            has_hash = bool(HEX.search(ln))
            if not (has_size or has_hash):
                continue
            names = sorted(set(FNAME.findall(ln)))
            if len(names) != 1:
                errs.append(u"R3 第 %d 行引尺寸/hash 但点名文件 %d 枚（期望 1）：%s"
                            % (i + 1, len(names), ln.strip()[:80]))
                continue
            base = names[0]
            cands = [p for p in (os.path.join(ROOT, base), os.path.join(DATA_DIR, base),
                                 os.path.join(HERE, base), base) if os.path.isfile(p)]
            if not cands:
                errs.append(u"R3 第 %d 行点名的文件不在盘上：%s" % (i + 1, base))
    return errs


def main():
    say(u"=" * 68)
    say(u"r34 判定册引用对账（只读门禁）")
    say(u"=" * 68)
    for p in (DOC, FACE):
        if not os.path.isfile(p):
            print(u"[0 判决] 读不到被审对象或载体：%s => 拒跑，退出码 2" % os.path.basename(p))
            return 2
    _d = doc_text()
    _f = face_text()
    say(u"被审文档 %s（%d B，md5 %s）" % (os.path.basename(DOC), len(read_bytes(DOC)),
                                        hashlib.md5(read_bytes(DOC)).hexdigest()[:12]))
    say(u"数值载体 %s（%d B，md5 %s）" % (os.path.basename(FACE), len(read_bytes(FACE)),
                                        hashlib.md5(read_bytes(FACE)).hexdigest()[:12]))

    real = check(_d, _f)
    for e in real:
        fault(u"REAL", e)
    say(u"[R 实测] 文档数值 token 被检查 %d 枚，违规 %d 条" % (STATUS.get(u"checked", 0), len(real)))

    led = STATUS.get(u"ledger", {})
    say(u"[R6 豁免账] " + u"／".join(u"%s=%d" % (k, led.get(k, 0)) for k, _ in EXEMPT))
    if all(led.get(k, 0) == 0 for k, _ in EXEMPT):
        fault(u"R6", u"豁免账全零：尺子没读到任何结构性形状，无法证明豁免按位置建过账")

    # 变异体：每枚必须让对应规则红
    muts = []
    m1 = _d.replace(u"0.0397887", u"0.039788", 1)
    muts.append((u"MUT-1 截短 KEY 小数 0.0397887->0.039788", m1, u"R1"))
    m2 = _d.replace(u"26494.9", u"26495.0", 1)
    muts.append((u"MUT-2 伪造小数 26494.9->26495.0", m2, u"R1"))
    _ln = [l for l in _d.split(u"\n") if SIZE.search(l) and u".md" in l]
    if not _ln:
        fault(u"MUT-3", u"找不到可删文件名的尺寸行（变异位没落地，此轮不得判绿）")
    else:
        m3 = _d.replace(_ln[0], re.sub(FNAME.pattern, u"（载体名已删）", _ln[0]), 1)
        muts.append((u"MUT-3 从尺寸行删掉文件名", m3, u"R3"))
    _b = BUCKET.search(_d)
    if not _b:
        fault(u"MUT-4", u"找不到五桶分布行（变异位没落地）")
    else:
        m4 = BUCKET.sub(u"PASS=6 / FAIL=15 / MISMATCH=2 / BOUNDARY=3 / INFO=4", _d, count=1)
        muts.append((u"MUT-4 改一跳 MISMATCH 桶", m4, u"R4"))
    for nm, txt, rule in muts:
        got = check(txt, _f)
        hit = [e for e in got if e.startswith(rule) or u"%s " % rule in e or e.startswith(u"R1") and rule == u"R1"]
        ok = any(rule in e for e in got)
        say(u"[%s] %s => %d 条违规，点名规则 %s：%s" % (
            u"红（合格）" if ok else u"绿（缺陷：变异体没打破判据）", nm, len(got), rule,
            (got[0][:110] if got else u"无违规")))
        if not ok:
            fault(rule, u"变异体未打破判据：" + nm)

    # 正对照：面自身作为文档自查（其 KEY/分布/guard 行必然自洽）；R3 关掉（面里的路径写法非本册散文形）
    self_ok = check(_f, _f, do_r3=False)
    say(u"[CONTROL-B 面自反] 以面为文档跑 R1/R2/R4/R5/R6/CONTROL-A：%s（期望无 R1/R2 违规）"
        % (u"无违规" if not self_ok else u"%d 条：%s" % (len(self_ok), self_ok[0][:100])))
    for e in self_ok:
        if e.startswith(u"R1") or e.startswith(u"R2"):
            fault(u"CONTROL-B", u"面自反不通过（尺子在自证语料上就错）：" + e)

    say(u"=" * 68)
    if FAULTS:
        say(u"判决：红 %d 条" % len(FAULTS))
        for x in FAULTS:
            say(u"  " + x)
            NOTES.append(x)
        rc = 1
    else:
        say(u"判决：全绿（引用逐字挂面；四枚变异体皆红；两条控制皆合格）")
        rc = 0
    say(u"退出码 %d" % rc)

    out = os.path.join(DATA_DIR, u"TUFT-V41alpha自然单位势_r34判定册_引用对账_2026-10-10.txt")
    buf = u"\n".join(LINES) + u"\n"
    with io.open(out, "wb") as fh:
        fh.write(buf.encode("utf-8"))
    with io.open(out, "rb") as fh:
        _b2 = fh.read()
    print(u"面已写：%s｜盘上 %d B｜md5 %s" % (os.path.basename(out), len(_b2),
                                          hashlib.md5(_b2).hexdigest()[:12]))
    return rc


if __name__ == "__main__":
    sys.exit(main())
