# -*- coding: utf-8 -*-
"""
================================================================================
TUFT g-2 / EDM 多口径对照表铸面器（2026-09-30）
================================================================================

它做一件此前从未做成的事：把 `04_理论推导/TUFT_双分量干涉屏蔽因子_g-2与EDM联合约束_审计.md`
行 297（§八 第 9 条）要求的「统一 OPEN5 的 α/(8π)、OPEN5b 的 2τ/κ 与 V3.2 的两尺度磁矩
映射，禁止多口径择优」那张对照表**铸出来**，并顺手登记两枚新主张、把 05_一致性检查/README.md
里那句「当前尚无本阶段独立产物」换成指针。

三条硬规矩（本件自己执行，失败即还原）：
  [R1] 版面里的每一个 MEASUREMENT 小数都不许由我复述：必须由本件从普查面
       `tuft_g2_EDM_口径普查_20260930_report.txt` 正则现读，或由现读值算出并在表内明写「派生」。
       写出之前先跑一次无源小数扫描（--mutant 会篡改一枚小数，扫描必须拒绝，否则 exit 4）。
  [R2] 落盘是原子的：三份文件任一失败 ⇒ 三份全部还原为写前图像（内存里存前像）。
  [R3] 本件不写自己的行数与字节数，也不写主册尺寸；被量产物不是引用来源。

用法：
  python tuft_g2_EDM_对照表铸面_20260930.py            # 铸面 + 追加 claims + 改 README
  python tuft_g2_EDM_对照表铸面_20260930.py --check     # 只与盘上版面比字节，不写
  python tuft_g2_EDM_对照表铸面_20260930.py --mutant    # 篡改一枚小数，验证 R1 有牙
退出码：0 成功 / 2 普查面读数缺失 / 3 版面含无源小数 / 4 变异体未被拒绝 / 5 版面表列数不齐
        6 claims 表头或 id 链不符 / 7 写后形状复核失败（EOL、行数、还原）
"""
import csv
import io
import os
import re
import sys

import mpmath as mp

mp.mp.dps = 32

HERE = os.path.dirname(os.path.abspath(__file__))
S14 = os.path.abspath(os.path.join(HERE, "..", ".."))
CARRIER = os.path.join(HERE, "tuft_g2_EDM_口径普查_20260930_report.txt")
DOC = os.path.join(S14, "05_一致性检查", "TUFT_g2与EDM_多口径对照与防串号_20260930.md")
CLAIMS = os.path.join(S14, "claims.csv")
README = os.path.join(S14, "05_一致性检查", "README.md")
AUDIT_MD = "04_理论推导/TUFT_双分量干涉屏蔽因子_g-2与EDM联合约束_审计.md"
CARRIER_REL = "07_计算复现/源码/tuft_g2_EDM_口径普查_20260930_report.txt"
MINT_REL = "07_计算复现/源码/tuft_g2_EDM_对照表铸面_20260930.py"

MEAS_RE = re.compile(r"\d+\.\d+(?:e[+-]?\d+)?")
# STRUCTURAL 豁免：版本号（V3.2）、日期。豁免表按位置建，逐条打印，不放宽正则。
STRUCT_OK = {"3.2"}


def read_lf(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    return raw.decode("utf-8", "replace").replace("\r\n", "\n"), raw


def one(pattern, text, flags=0):
    m = re.findall(pattern, text, flags)
    if len(m) != 1:
        print("EXIT 2  普查面读数 %r 命中 %d 次（应为 1）" % (pattern[:40], len(m)))
        raise SystemExit(2)
    return m[0] if not isinstance(m[0], tuple) else m[0]


def parse_carrier(text):
    R = {}
    n, bad, selfx = one(r"\[实测分母\] 被扫描文件数 = (\d+)   其中不可读 = (\d+)   本件自有产物被排除 = (\d+)", text)
    R["scanned"], R["unreadable"], R["excluded_self"] = n, bad, selfx
    lines = text.split("\n")
    census, firsts = [], []
    key_re = re.compile(r"^  ((?:g2|edm)@[\w.\-]+)\s+命中行\s+(\d+)\s+载体文件\s+(\d+)\s+\((.*)\)$")
    hit_re = re.compile(r"^        (\S+?):(\d+)  \[(.*)\]$")
    for i, l in enumerate(lines):
        m = key_re.match(l)
        if not m:
            continue
        h = hit_re.match(lines[i + 1]) if i + 1 < len(lines) else None
        if h is None:
            print("EXIT 2  口径 %s 的下一行不是载体行（无载体？）" % m.group(1))
            raise SystemExit(2)
        census.append(m.groups())
        firsts.append(h.groups())
    if len(census) != 7:
        print("EXIT 2  普查面口径行数 = %d（声明集为 7 枚）" % len(census))
        raise SystemExit(2)
    R["census"], R["firsts"] = census, firsts
    a, va, b, vb = one(r"A_E_EXP 读自 OPEN5\.py:(\d+)（类型 Constant，值 ([0-9.]+)）；tau_over_kappa 读自 OPEN5b\.py:(\d+) = ([0-9.]+)", text)
    R["open5_ae_line"], R["a_e_exp"], R["open5b_rat_line"], R["r0"] = a, va, b, vb
    R["a8pi"], R["ae_vs"], R["dev_low"] = one(r"α/\(8π\) = ([0-9.]+)  vs a_e\(exp\) = ([0-9.]+)  偏差\(低侧\) = ([0-9.]+) %", text)
    R["a2pi"], R["a2pi_gap"] = one(r"α/\(2π\) = ([0-9.]+)  （QED 主导项，与 a_e 差 ([0-9.]+) %）", text)
    R["api"], R["two_ae"], R["api_ratio"] = one(r"α/π    = ([0-9.]+)  vs 2a_e = ([0-9.]+)  比值 = ([0-9.]+)", text)
    R["two_rk"], R["dev_high"] = one(r"2τ/κ   = ([0-9.]+) （[^）]*）偏差\(高侧\) = ([0-9.]+) %", text)
    R["coll_lo"], R["coll_hi"], R["coll_pp"] = one(r"\[反向碰撞\] 两个偏差 ([0-9.]+)% 与 ([0-9.]+)%，只差 ([0-9.]+) 个百分点", text)
    R["fg"], R["fd"], R["split"], R["logsplit"] = one(
        r"F_g 需 = ([0-9.eE+-]+)\s+F_d 需 = ([0-9.eE+-]+)\s+分裂比 = ([0-9.eE+-]+) （log10 = ([0-9.]+)）", text)
    R["de_cm"], R["dself"], R["d_open6"], R["d_open5b"] = one(
        r"单位换算自洽：([0-9.eE+-]+) C·m -> ([0-9.eE+-]+) e·cm；档案另印 ([0-9.eE+-]+)（OPEN6）与 ([0-9.eE+-]+)（OPEN5b）", text)
    R["acme"], R["jila"], R["limit_ratio"], R["ex_acme"], R["ex_jila"] = one(
        r"上限口径差：ACME2018 ([0-9.eE+-]+) / JILA2023 ([0-9.eE+-]+) 相差 ([0-9.]+) 倍；同一 d_e 分别超限 ([0-9.eE+-]+) 与 ([0-9.eE+-]+) 倍", text)
    ok = re.findall(r"^\s+\[OK\s*\] (.*?)\s+ carrier=(\S+) 本件=(\S+) 相对差=(\S+)$", text, re.M)
    if len(ok) != 5:
        print("EXIT 2  逐位比对行数 = %d（应为 5）" % len(ok))
        raise SystemExit(2)
    R["ok"] = ok
    R["g2_line"], R["g2_val"] = one(r"G2_TUFT @行(\d+) 右侧类型=Constant 值=([0-9.]+)", text)
    R["closure"] = one(r"tau/kappa 与 G2_TUFT/2 之差 = ([0-9.eE+-]+)", text)
    if "[C3 判定] CIRCULAR" not in text:
        print("EXIT 2  普查面未印 CIRCULAR 判定")
        raise SystemExit(2)
    R["retract_line"] = one(r"出现的行 = \[(\d+)\]", text)
    return R


def derived(R):
    """由现读值算出的量；每个都在版面里标「派生」，并列进 allow 供无源扫描放行。"""
    d, allow = {}, set()

    def k(name, s):
        # 派生量必须长得像一个十进制 token，否则它会绕过无源扫描（没有小数点的数不被针读到）。
        if not re.search(r"\d+\.\d", s):
            print("EXIT 2  派生量 %s=%r 不含小数，会绕过无源扫描" % (name, s))
            raise SystemExit(2)
        allow.add(s)
        d[name] = s
        return s

    dev_lo, dev_hi = mp.mpf(R["dev_low"]), mp.mpf(R["dev_high"])
    k("d_pp", mp.nstr(dev_lo - dev_hi, 4))
    k("ratio_hi", mp.nstr(mp.mpf(R["two_rk"]) / mp.mpf(R["two_ae"]), 6))
    k("ratio_lo", mp.nstr(mp.mpf(R["a8pi"]) / mp.mpf(R["ae_vs"]), 6))
    k("ratio_pi", mp.nstr(mp.mpf(R["two_ae"]) / mp.mpf(R["api"]), 6))
    # 分裂比对 F_g 幅度的灵敏度：F_g 只要在 [1e-2,1e2] 内摆动，log10 分裂比仍在 15.866 ± 2
    ls = mp.mpf(R["logsplit"])
    k("band_lo", mp.nstr(ls - 2, 8))
    k("band_hi", mp.nstr(ls + 2, 8))
    k("wp_vs_acme", mp.nstr(mp.mpf(R["acme"]) / mp.mpf("8.7e-34"), 7))
    k("open6_vs_self", mp.nstr((mp.mpf(R["d_open6"]) - mp.mpf(R["dself"])) / mp.mpf(R["dself"]), 3))
    k("limit_check", mp.nstr(mp.mpf(R["ex_jila"]) / mp.mpf(R["ex_acme"]), 4))
    return d, allow


def check_tables(lines):
    """逐表校列数：同一块 | 行里管道符数必须相同，且第 2 行必须是分隔行。"""
    blocks, cur = [], []
    for i, l in enumerate(lines, 1):
        if l.startswith("|"):
            cur.append((i, l))
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    bad = []
    for b in blocks:
        if len(b) < 2 or "---" not in b[1][1]:
            bad.append("表块首行 %d 缺分隔行" % b[0][0])
        widths = {l.count("|") for _, l in b}
        if len(widths) != 1:
            bad.append("表块首行 %d 列数不齐：%s" % (b[0][0], sorted(widths)))
    return bad, len(blocks)



def build_doc(R, D, tamper=None, nxt=("", "")):
    L = []
    a = L.append
    a("# TUFT g−2 / EDM 多口径对照与防串号检查（2026-09-30）")
    a("")
    a("所属独立体系：[挠率统一场论TUFT](../README.md)。阶段目录：05_一致性检查。")
    a("")
    a("读数载体（下文称「普查面」）：`" + CARRIER_REL + "`；铸面器：`" + MINT_REL + "`。")
    a("本件回答 " + AUDIT_MD + " 行 " + "297" + "（§八 第 9 条）那条要求：三套磁矩映射必须统一、禁止多口径择优。")
    a("该要求此前只有要求、没有对照表；本轮把表铸出来，并登记两条由表读出的后果。")
    a("")
    a("红线：不构造新物理、不改写任何映射公式、不改写历史 report；只回答「每句话挂在哪份文件上、")
    a("数字能否复算、口径之间能不能互换」。判定用词：**载体**＝印出该读数的文件；**派生**＝由现读值算出、")
    a("表内明写；本件不复述任何未挂载体的数。")
    a("")
    a("## 一、覆盖面：这台普查走了多少文件、声明的口径有没有载体")
    a("")
    a("| 口径 | 命中行 | 载体文件 | 普查面给出的首枚载体（path:line，原样） |")
    a("|---|---:|---:|---|")
    for i, (key, hit, files, label) in enumerate(R["census"]):
        p, ln, tok = R["firsts"][i]
        a("| `%s` (%s) | %s | %s | `%s`:%s 命中 `%s` |" % (key, label, hit, files, p.replace("\\", "/"), ln, tok))
    a("")
    a("分母现读自普查面：被扫描文件 " + R["scanned"] + " 个，不可读 " + R["unreadable"] +
      " 个，本件自有产物被排除 " + R["excluded_self"] + " 个。")
    a("排除自有产物的原因：覆盖面就是把「声明这枚口径的那几行」算成载体的那种自证——声明不是证据。")
    a("因此「" + AUDIT_MD.split('/')[-1] + "」这类档案文件出现在载体列里是**被普查读到的既有行**，")
    a("不是本件写入的：本件只写下面这份版面与两枚主张行。")
    a("")
    a("## 二、五口径对照表（数值全部现读自普查面 C2，逐位回到三份历史 report）")
    a("")
    a("| 口径 | 现算值 | 对照对象 | 方向 | 比值/偏差 | 载体 |")
    a("|---|---:|---|---|---|---|")
    a("| OPEN5：α/(8π) | " + R["a8pi"] + " | a_e = " + R["ae_vs"] + " | 偏低 | 偏差 " + R["dev_low"] +
      " %（值为其 " + D["ratio_lo"] + "） | OPEN5 report |")
    a("| OPEN5b：2τ/κ | " + R["two_rk"] + " | 2a_e = " + R["two_ae"] + " | 偏高 | 偏差 " + R["dev_high"] +
      " %（值为其 " + D["ratio_hi"] + "） | OPEN5b report（该值来源见 §四） |")
    a("| 参照：α/(2π)（QED 主导项） | " + R["a2pi"] + " | a_e | 偏高 | 与 a_e 差 " + R["a2pi_gap"] +
      " % | 普查面 C2（标准 QED，非 TUFT 产出） |")
    a("| 参照：α/π（无挠率） | " + R["api"] + " | 2a_e | 偏高 | 比值 " + R["api_ratio"] +
      "（2a_e 为其 " + D["ratio_pi"] + "） | 普查面 C2 |")
    a("| V3.2：两尺度磁矩 | 未复算 | 2.002319 | — | 只登记载体计数（上表 " + R["census"][2][1] +
      " 行 / " + R["census"][2][2] + " 文件） | 普查面 C1 |")
    a("")
    a("逐位比对（普查面 C2 的 5 行，格式 `载体印的 → 本件现算的（相对差）`）：")
    a("")
    for label, carrier_v, mine_v, rel in R["ok"]:
        a("- " + label + "：`" + carrier_v + "` ↔ `" + mine_v + "`，相对差 " + rel)
    a("")
    a("## 三、两处会串号的地方")
    a("")
    a("### 串号一：反向碰撞——档案里有两个看起来互相抵消的「75%」")
    a("")
    a("同一份普查面上，α/(8π) 的偏差是 **" + R["coll_lo"] + " %（偏低）**，2τ/κ 的偏差是 **" +
      R["coll_hi"] + " %（偏高）**，两者只差 **" + D["d_pp"] + " 个百分点**，")
    a("而对照对象还分别是 a_e 与 2a_e（差一个因子 2）。结论：**「TUFT 的 g−2 偏差约 75%」这句话在不点名口径时")
    a("无法判定该往哪边修**——一个口径要求把预言放大，另一个要求把它缩小。")
    a("这条不是新的物理主张，是把 " + AUDIT_MD.split('/')[-1] + " §一 已记名的「方向相反」补上价格。")
    a("")
    a("### 串号二：α/π 是假朋友")
    a("")
    a("不含任何挠率的 α/π = " + R["api"] + " 与 2a_e = " + R["two_ae"] + " 的比值已达 " + R["api_ratio"] +
      "（差 " + R["a2pi_gap"] + " % 量级）。")
    a("所以「g−2 量级对得上」不能当 TUFT 的证据：一个几何映射只要落在 α 的某个整数分母附近就能撞过量级。")
    a("任何后续声称必须给出**与 α/π 不同的、由挠率决定的结构因子**，否则该声称被这条参照线直接吃掉。")
    a("")
    a("## 四、" + R["g2_val"] + " 这个基线从哪来：循环定价，且判定带牙")
    a("")
    a("普查面 C3 用 ast 读源码结构（不读文案）得到：")
    a("")
    a("- OPEN5b.py 行 " + R["g2_line"] + "：`G2_TUFT` 右侧类型 = `Constant`，值 = " + R["g2_val"] + " —— 字面常量，不是算出来的。")
    a("- OPEN5b.py 行 " + R["open5b_rat_line"] + "：`tau_over_kappa = Rational` → " + R["r0"] + "，注释自称「由 g-2_TUFT=" +
      R["g2_val"] + " 反解」。")
    a("- 闭式检验：" + R["r0"] + " 与 " + R["g2_val"] + "/2 之差 = " + R["closure"] + "（同一赋值链的两个成员；判定阈写死在普查件源码 C3 分支里，本件不复述其位数）。")
    a("- 判定：**CIRCULAR**。")
    a("- 独立见证（不同目录、另一条弧，与本件不共享代码）："
      "`04_公共成果/本项目_全维自洽与归一化/数据/v_eq_c_TUFT_V2_双分量孤子_可证伪性审计.md` 行 32 的 B-05 "
      "判语把同一件事记为「来料把 g-2_0=2r 当作起点，全文无推导 ⇒ 属映射层注入」，其行 55 另引 V1 的同一个 " +
      R["g2_val"] + " 作对照。")

    a("- 而同一份档案里那句「τ/κ 被孤子自洽锁死」已由 OPEN5c.py 行 " + R["retract_line"] +
      " 撤回为「由额外孤子解选定」。")
    a("")
    a("后果：以 2τ/κ 口径算出的 " + R["dev_high"] + " % 偏差**不是与实验值的偏差，而是与自身输入之偏差**。")
    a("把它当预言的失败证据、或当预言的成功证据，都不成立——它没有被产出。要让它成为可判定的量，")
    a("必须有一次不含 g−2 数据的动力学产出（同一个 " + R["g2_val"] + " 由场方程与边界条件给出）。")
    a("")
    a("## 五、哪些结论在这个缺陷下仍然存活")
    a("")
    a("| 结论 | 为什么活 | 现读依据 |")
    a("|---|---|---|")
    a("| EDM 侧 " + R["de_cm"] + " C·m 超上限 " + R["ex_acme"] + " 倍（ACME " + R["acme"] + "） | 该倍数的分子来自 OPEN6 现算的 d_e，不经 " +
      R["g2_val"] + " | 普查面 C2 |")
    a("| F_g 与 F_d 分裂 " + R["split"] + " 倍（log10 = " + R["logsplit"] + "）的数量级 | 分裂由 F_d = " + R["fd"] +
      " 一侧定价；F_g 即便摆动两个数量级，log10 仍在 " + D["band_lo"] + "–" + D["band_hi"] + "（派生） | 普查面 C2 |")
    a("| α/(8π) 口径 " + R["dev_low"] + " % 偏低 | 分子是 CODATA 复算，不依赖 2τ/κ | 普查面 C2 |")
    a("| 「屏蔽因子 f(κ,τ) 能同时修 g−2 与 EDM」 | 被上述分裂否证：一个几何因子不可能同时是 " + R["fg"] +
      " 与 " + R["fd"] + " | 普查面 C2 |")
    a("| 以 2τ/κ 基线做的任何「偏差」陈述 | **不活**：见 §四，它是自比 | 普查面 C3 |")
    a("")
    a("## 六、EDM 上限的三套口径与第 4 位数字")
    a("")
    a("- 档案并存 ACME2018 " + R["acme"] + " 与 JILA2023 " + R["jila"] + " e·cm，相差 " + R["limit_ratio"] +
      " 倍；同一 d_e 分别超限 " + R["ex_acme"] + " 与 " + R["ex_jila"] + " 倍（后者/前者 = " + D["limit_check"] +
      "，与上限之比同值 ⇒ 两个口径差全在这一枚上限上，派生自洽）。")
    a("- 白皮书口径引用的是 " + "8.7e-34" + " C·m，比 ACME 严 " + D["wp_vs_acme"] + " 倍（派生）。")
    a("- 单位换算链在第 4 位分叉：" + R["de_cm"] + " C·m 自洽化为 " + R["dself"] + " e·cm；OPEN5b 印 " +
      R["d_open5b"] + "（与自洽值同），OPEN6 印 " + R["d_open6"] + "（相对偏 " + D["open6_vs_self"] + "，派生）。")
    a("- 规矩：引用「超限 N 个量级」必须同句点名上限口径与单位换算链；否则这句话在语料里至少对应三个不同数值。")
    a("")
    a("## 七、判定：本轮没有突破，推进的是口径的可判定性")
    a("")
    a("1. **未发现新的理论体系公式。**本轮所有产出是对既有口径的对照与定价；未提出任何新映射、未改任何既有公式。")
    a("2. g−2 侧当前**不可判定**：唯一被当作 TUFT 预言的 " + R["two_rk"] + " 是字面常量反解（§四），"
      )
    a("   而 α/π 参照线（§三 串号二）表明「量级对上」不构成证据。")
    a("3. EDM 侧超限 " + R["ex_acme"] + " 倍那笔冲突**仍存活**（§五），且它不依赖 §四 的缺陷——这是档案里唯一一把不靠循环输入的否证。")
    a("4. 准入门槛（要谈突破必须同时满足，逐条可查）：")
    a("   (a) 唯一化磁矩口径：从三套映射中由同一电磁流算符选定一套，另两套降级为参照；")
    a("   (b) " + R["g2_val"] + " 由不含 g−2 数据的动力学产出，闭合差 " + R["closure"] + " 那种自比必须消失；")
    a("   (c) 给出与 α/π 不同的挠率结构因子；")
    a("   (d) EDM 的 γ 定出量纲与数值（此前「最有利修复」的结论挂在 " + AUDIT_MD.split('/')[-1] +
      " §四 与 claims S14-C0062 上，本件不复制其读数）。")
    a("5. 「双分量干涉屏蔽因子」那条 V2 路线的准入条件在 " + AUDIT_MD.split('/')[-1] + " §八，本轮未推进其任一条。")
    a("")
    a("## 八、仪器账与产物索引")
    a("")
    a("- 普查件（只读，本轮新增）：`" + CARRIER_REL + "` 与 `tuft_g2_EDM_口径普查_20260930_mutant_report.txt`；")
    a("  源码 `tuft_g2_EDM_口径普查_20260930.py`。退出码 2/3/4/5/6/7 分别对应：口径无载体 / 复算与载体逐位不符 /")
    a("  变异体未改口 / 基线未判 CIRCULAR / 扫描根推错 / 结构读失败。")
    a("- 本版面由 `" + MINT_REL + "` 铸出：写前先跑无源小数扫描，`--mutant` 会篡改 " + D["d_pp"] +
      " 这枚小数并要求扫描拒绝。")
    a("- 登记：claims.csv 追加 " + nxt[0] + "（循环定价与反向碰撞的价格）、" + nxt[1] +
      "（EDM 上限口径与第 4 位分叉），")
    a("  id 由本铸面器在写盘前现读表尾取得（取号行由铸面器打印，不由本段复述）；")
    a("  05_一致性检查/README.md 的「尚无本阶段独立产物」改为指向本文件。")
    a("- 本段故意不写行数与字节数：本件是被量产物，尺寸只活在量它的那份日志里。")
    a("")
    a("红线复述：数学自洽不等于物理实证；能反解实验值不等于预言；口径对照表不产出新物理，")
    a("本件只做对照与定价：口径表不产出预言，它只让「哪句话可以被判红」变得可查——TUFT 的核心声称仍未被证明。")
    if tamper:
        txt = "\n".join(L)
        if txt.count(tamper[0]) < 1:
            print("EXIT 2  变异体锚点未在版面里出现：%s" % tamper[0])
            raise SystemExit(2)
        L = [x.replace(tamper[0], tamper[1]) for x in L]
    return "\r\n".join(L) + "\r\n", L


def scan_unsourced(md, carrier_text, allow):
    """版面里的每个小数都必须出现在普查面里，或在派生 allow 表里。
    唯一的 STRUCTURAL 豁免按位置建：token 必须紧跟在 V/v 之后（版本号），且本身在豁免表里。
    测量小数永远不会长成「V 后面」的样子，所以这条豁免不给无源数留通道。"""
    stray, exempt = [], []
    for m in MEAS_RE.finditer(md):
        tok = m.group(0)
        prev = md[max(0, m.start() - 1):m.start()]
        line = md[:m.start()].count("\n") + 1
        if tok in STRUCT_OK and prev in ("V", "v"):
            exempt.append((line, tok, "版本号前缀 V"))
            continue
        if tok in carrier_text or tok in allow:
            continue
        stray.append((line, tok))
    return stray, exempt



def build_claims(R, D, existing_rows):
    hdr = existing_rows[0]
    if hdr[0] != "claim_id" or len(hdr) != 14:
        print("EXIT 6  claims 表头不符：%s / %d 字段" % (hdr[0], len(hdr)))
        raise SystemExit(6)
    ids = [r[0] for r in existing_rows[1:] if r]
    nums, odd = [], []
    for i in ids:
        m = re.match(r"^S14-C(\d+)$", i)
        (nums if m else odd).append(int(m.group(1)) if m else i)
    if odd:
        print("  [注意] 表尾 id 链里有 %d 枚不符 S14-C\\d+ 形式：%s（未参与取号）" % (len(odd), odd[:5]))
    if not nums:
        print("EXIT 6  没有任何可取号的 id")
        raise SystemExit(6)
    tail = max(nums)
    nxt = ["S14-C%04d" % (tail + 1), "S14-C%04d" % (tail + 2)]
    print("  [现读取号] 表尾最大号 %d → 本件取 %s, %s（在册 id %d 枚）" % (tail, nxt[0], nxt[1], len(ids)))

    c1 = ("『2τ/κ=" + R["g2_val"] + " 是孤子自洽锁死给出的 TUFT g−2 预言』——已否证："
          "OPEN5b.py 行 %s 的 G2_TUFT 右侧类型为 Constant=%s（字面常量），行 %s 的 tau_over_kappa=%s "
          "注释自称由它反解（闭式差 %s），而同档案 OPEN5c.py 行 %s 已把「τ/κ 被孤子自洽锁死」撤回为"
          "「由额外孤子解选定」。故以该口径算出的 %s%% 偏差是与自身输入之比、不是与实验之比，既不能当成功证据"
          "也不能当失败证据。附带定价：α/(8π) 口径的偏差 %s%% 方向相反，两者仅差 %s 个百分点，"
          "且对照对象分别为 a_e 与 2a_e，故不点名口径的「75%% 偏差」无法指示修复方向"
          % (R["g2_line"], R["g2_val"], R["open5b_rat_line"], R["r0"], R["closure"],
             R["retract_line"], R["dev_high"], R["dev_low"], D["d_pp"]))
    c2 = ("EDM 上限在档案里以三套口径并存：ACME2018 %s、JILA2023 %s e·cm（相差 %s 倍），"
          "白皮书引用 8.7e-34 C·m；同一 d_e=%s C·m 分别超限 %s 与 %s 倍。"
          "单位换算另在第 4 位分叉：%s C·m 自洽化为 %s e·cm，OPEN5b 印 %s 而 OPEN6 印 %s。"
          "故引用「超限 N 个量级」必须同句点名上限口径与单位换算链"
          % (R["acme"], R["jila"], R["limit_ratio"], R["de_cm"], R["ex_acme"], R["ex_jila"],
             R["de_cm"], R["dself"], R["d_open5b"], R["d_open6"]))
    rows = []
    for cid, stmt, ev, st in ((nxt[0], c1, "structural", "falsified"),
                              (nxt[1], c2, "structural", "open")):
        rec = {k: "" for k in hdr}
        rec["claim_id"] = cid
        rec["hypothesis_revision"] = "tuft-census-20260930"
        rec["statement"] = stmt
        rec["assumptions"] = "S14-A1"
        rec["derivation"] = CARRIER_REL + "#C3" if st == "falsified" else CARRIER_REL + "#C2"
        rec["run_id"] = "07_计算复现/运行记录/run_template.json"
        rec["uncertainty"] = ("ast 结构读 + 闭式检验，判定由变异体改口作证"
                             if st == "falsified" else "两把上限口径的现读比值与自洽单位换算")
        rec["evidence_level"] = ev
        rec["status"] = st
        buf = io.StringIO()
        csv.writer(buf, lineterminator="\n").writerow([rec[k] for k in hdr])
        rows.append(buf.getvalue().rstrip("\n"))
    return nxt, rows


def patch_readme(text):
    old = "当前尚无本阶段独立产物；不因目录存在而标记完成。"
    if text.count(old) != 1:
        print("EXIT 7  README 那句占位符命中 %d 次（应为 1）" % text.count(old))
        raise SystemExit(7)
    new = ("本阶段独立产物：[TUFT g−2 / EDM 多口径对照与防串号检查（2026-09-30）]"
           "(TUFT_g2与EDM_多口径对照与防串号_20260930.md) —— 该文件只对照既有口径并给每枚读数点名载体，"
           "不产出新映射；目录存在本身仍不标记完成。")
    return text.replace(old, new)


def main():
    mode = "write"
    if "--check" in sys.argv:
        mode = "check"
    if "--mutant" in sys.argv:
        mode = "mutant"
    carrier_text, _ = read_lf(CARRIER)
    R = parse_carrier(carrier_text)
    D, allow = derived(R)

    # 取号必须在铸面之前：版面要印它自己登记的那两枚 id（写盘后再改就是第二权威源）
    with open(CLAIMS, "rb") as fh:
        claims_raw = fh.read()
    claims_text = claims_raw.decode("utf-8").replace("\r\n", "\n")
    rows = [r for r in csv.reader(io.StringIO(claims_text)) if r and any(x.strip() for x in r)]
    nxt, new_rows = build_claims(R, D, rows)

    tamper = None
    if mode == "mutant":
        tamper = (D["d_pp"], "0.7721")
    if mode == "check" and os.path.isfile(DOC):
        # 版面一旦落盘，它印的就是当时实际取到的号；复跑必须拿盘上的号来比，
        # 否则 --check 会因为自己把表尾推高了而判不匹配（工具不许钉不住自己的取号）。
        disk = open(DOC, "rb").read().decode("utf-8", "replace").replace("\r\n", "\n")
        found = re.findall(r"追加 (S14-C\d{4})（循环定价与反向碰撞的价格）、(S14-C\d{4})（EDM 上限口径与第 4 位分叉）", disk)
        if len(found) != 1:
            print("EXIT 6  盘上版面里的取号句命中 %d 次，--check 无法复算" % len(found))
            raise SystemExit(6)
        in_claims = all(x in [r[0] for r in rows[1:] if r] for x in found[0])
        print("  [--check 取号] 版面点名 %s / %s；两枚均已在册 = %s" % (found[0][0], found[0][1], in_claims))
        nxt = list(found[0])
    md, lines = build_doc(R, D, tamper, nxt)

    # 表列数复核（逐表，不全局：三张表列数本来就不同）
    bad, nblocks = check_tables(md.replace("\r\n", "\n").split("\n"))
    if bad:
        for x in bad:
            print("  表格缺陷：" + x)
        print("EXIT 5  版面有 %d 张表、其中 %d 张列数不齐，拒绝写盘" % (nblocks, len(bad)))
        return 5
    stray, exempt = scan_unsourced(md, carrier_text, allow)
    print("[扫描] STRUCTURAL 豁免 %d 枚（逐条：位置＋串）：%s" % (len(exempt), exempt))
    if mode == "mutant":
        if stray:
            print("[MUTANT] 无源小数扫描拒绝被篡改的 %s：%s ⇒ 扫描有牙" % (tamper[1], stray))
            print("EXIT 0  变异体已按预期失败")
            return 0
        print("EXIT 4  变异体未被拒绝：篡改 %s→%s 后扫描仍通过 ⇒ 无源小数扫描是装饰" % (tamper[0], tamper[1]))
        return 4
    if stray:
        for ln, tok in stray:
            print("  无源小数：行 %d  %s" % (ln, tok))
        print("EXIT 3  版面含 %d 枚未挂载体的小数，拒绝写盘" % len(stray))
        return 3

    with open(README, "rb") as fh:
        readme_raw = fh.read()
    readme_text = readme_raw.decode("utf-8").replace("\r\n", "\n")
    if "当前尚无本阶段独立产物" in readme_text:
        readme_new = patch_readme(readme_text)
    elif mode == "check":
        # --check 是复跑：占位符已被本件换成指针，此时不该再要求占位符存在
        print("  [--check] README 占位符已替换为指针（复跑模式视为满足）")
        readme_new = readme_text
    else:
        readme_new = patch_readme(readme_text)


    claims_new = claims_text
    for r_ in new_rows:
        claims_new = claims_new + "\n" + r_ + "\n"

    if mode == "check":
        ok_doc = os.path.isfile(DOC) and open(DOC, "rb").read().decode("utf-8", "replace").replace("\r\n", "\n") == md.replace("\r\n", "\n")
        ok_cl = nxt[0] in claims_text and nxt[1] in claims_text
        print("[CHECK] 版面字节与盘面相同 = %s；%s/%s 已在册 = %s" % (ok_doc, nxt[0], nxt[1], ok_cl))
        return 0 if (ok_doc and ok_cl) else 1

    before = {DOC: open(DOC, "rb").read() if os.path.isfile(DOC) else None,
              CLAIMS: claims_raw, README: readme_raw}
    try:
        with open(DOC, "wb") as fh:
            fh.write(md.encode("utf-8"))
        with open(CLAIMS, "wb") as fh:
            fh.write(claims_new.encode("utf-8"))
        with open(README, "wb") as fh:
            fh.write(readme_new.replace("\n", "\r\n").encode("utf-8"))
    except Exception as e:
        for p, b in before.items():
            if b is None:
                if os.path.isfile(p):
                    os.remove(p)
            else:
                with open(p, "wb") as fh:
                    fh.write(b)
        print("EXIT 7  写入失败，三份文件已还原：%s" % e)
        return 7

    # 写后复核：EOL 形状、claims 行数、id 唯一
    errs = []
    db = open(DOC, "rb").read()
    rows_md = len(db.split(b"\r\n")) - 1
    if db.count(b"\r") != db.count(b"\r\n"):
        errs.append("版面含游离 CR（非纯 CRLF）")
    if db.decode("utf-8", "replace").replace("\r\n", "\n") != md.replace("\r\n", "\n"):
        errs.append("版面读回与铸出内容不一致")
    if rows_md < 60:
        errs.append("版面行数 %d 异常偏低" % rows_md)
    cb = open(CLAIMS, "rb").read()
    ct = cb.decode("utf-8").replace("\r\n", "\n")
    rid = [r[0] for r in csv.reader(io.StringIO(ct)) if r and r[0] != "claim_id" and any(x.strip() for x in r)]
    if len(rid) != len(set(rid)):
        errs.append("claims id 重复")
    if nxt[0] not in rid or nxt[1] not in rid:
        errs.append("claims 新行未落地")
    rb = open(README, "rb").read()
    if rb.count(b"\r") != rb.count(b"\r\n"):
        errs.append("README EOL 被改形")
    if "当前尚无本阶段独立产物" in rb.decode("utf-8"):
        errs.append("README 占位符未替换")
    if errs:
        for p, b in before.items():
            if b is None:
                os.remove(p)
            else:
                with open(p, "wb") as fh:
                    fh.write(b)
        for x in errs:
            print("  写后复核失败：" + x)
        print("EXIT 7  复核失败，三份文件已还原")
        return 7
    print("WROTE  版面 rows(CRLF)=%d bytes=%d ｜ claims +%s +%s（现共 %d 条数据行）｜ README 占位符已替换"
          % (db.count(b"\r\n"), len(db), nxt[0], nxt[1], len(rid)))
    print("EXIT 0  无源小数扫描通过（放行依据：普查面 %d 枚读数 + 派生表 %d 枚）"
          % (len(carrier_text), len(allow)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
