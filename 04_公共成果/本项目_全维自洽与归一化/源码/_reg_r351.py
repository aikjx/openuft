# -*- coding: utf-8 -*-
"""r351 README 双锚点登记（幂等 / 零删除 / 写后读回验证）。

r351 是**热区回补**：正本 2026-11-01 已由别的会话落盘，源码本轮才落 ⇒ 本卷**不占新号**。

纪律：
  · 锚点串含本卷 RID（`│   ├── TUFT-r351_` / `├── 判定_TUFT-r351_`），先判存在再分流（幂等）；
  · 源码树插在 `│   ├── TUFT-r350_` 之**后**（按卷序贴近邻居，不追加链尾）；判定列表**追加末尾**；
  · README 现为**纯 LF、无尾换行**（r375 登记时实测 CRLF=0）⇒ newline="\n" 读写是字节安全的；
    末尾追加会把「无尾换行」变成「有尾换行」，判法用 `t.count(备份末行) == 1`（伪删除探针），不看 diff；
  · 每个数字都点名印出它的那份面（`源码/_out_r351.txt`／判定册 §九／§一），不许凭本轮写作记忆生成。
"""
import io, os, re, shutil, sys

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(ROOT, "README.md")
BAK = os.path.join(ROOT, "scratch", "_bak_README_pre_r351.md")
OUT_R351 = os.path.join(ROOT, "源码", "_out_r351.txt")

SRC_ANCHOR = "│   ├── TUFT-r350_"
SRC_KEY = "│   ├── TUFT-r351_"
JUD_ANCHOR = "├── 判定_TUFT-r351_"

def scan_max_rounds():

    """登记那一刻的只读现扫：源码树 / 判定面的最大卷号（并发写者在飞，故不许手写）。"""
    import glob, re
    def mx(d, pat):
        v = [int(m.group(1)) for f in os.listdir(d)
             for m in [re.search(pat, f)] if m]
        assert v, ("扫描集为空" % d)
        return max(v), len(v)
    src = mx(os.path.join(ROOT, "源码"), r"^TUFT-r(\d+)_")
    jud = mx(os.path.join(ROOT, "判定"), r"^判定_(?:判定_)?TUFT-r(\d+)_")
    return src, jud


MX_SRC, MX_JUD = scan_max_rounds()

def read_scan_count():
    """从 `源码/_out_r351.txt` 的 G9 行现读扫面份数；该数随并发卷落盘增长 ⇒ 不许手写。"""
    txt = io.open(OUT_R351, encoding="utf-8", newline="").read()
    m = re.search("扫面 (\d+) 份", txt)
    assert m, "G9 行未印扫面份数 ⇒ 读数载体缺席"
    n = int(m.group(1))
    assert n >= 20, ("判集塌缩：扫面 %d 份" % n)
    return n


SCAN_N = read_scan_count()
SCAN_TXT = "扫面 **%d** 份（登记时刻现读 G9，随并发卷落盘增长 ⇒ 只作当下观察）" % SCAN_N


SCAN_SENT = ("登记那一刻只读现扫：源码树最大号 **r%d**（共 %d 份源码面）、"
             "判定面最大号 r%d（共 %d 份判定面）"
             % (MX_SRC[0], MX_SRC[1], MX_JUD[0], MX_JUD[1]))



FN = ("TUFT-r351_ROOTV27双层光速螺旋洛伦兹自洽与曲率挠率比观察者依赖与内禀频率"
      "半角动量与Dirac磁矩审计_精算与可视化_2026-11-02.py")

SRC_LINE = (
    "│   ├── " + FN + "  # 新增（**r351 · 2026-11-02 热区回补**）："
    "**审计 ROOT V27（双层光速螺旋：洛伦兹自洽 / 曲率挠率比的观察者依赖 / 内禀频率 / 半角动量 / Dirac 磁矩）**"
    "（条目 **64**＝A 精确代数 14 / B 高精度复现 11 / G 判决 9 / C 对照 10 / E 自捕 15 / P 定价 2 / O 3；"
    "判决类 **44/44** 由具名变异体定价；收口闸门 **12/12 PASS**、退出码 0、"
    "二跑五件产物逐字节同值 ⇒ 幂等。读数载体：`源码/_out_r351.txt` 与判定册 §九）。"
    "★**取号**：**不占新号**——正本文件名 r351 于 11-01 已落、源码未落（README 的 r354 行正因「r351 来料已落、源码未落 ⇒ 热区」而改取冷号），"
    "本轮把该热区回补到底；登记那一刻现扫（由 scan_max_rounds() 算，不手写）＝" + SCAN_SENT +
    "；并发卷在飞 ⇒ 只作当下观察，引用前须重扫。"
    "★**去重尺先自证有牙**：同一把尺打在确住在这本账上的老词必须全亮 ⇒ 正对照 `['固定点','曲率','挠率','判别力','自由度']` **5/5** 命中、去重尺现读 @@SCAN@@（C07）；"
    "邻居让渡账现扫＝点名 r351 的次数 `[('r354',3),('r360',1)]`（C08），故本卷的磁矩/观察者依赖条目是**接管让渡项**而非抢账。"
    "★★**判决一 G01（0 bit）**：把 κ/|τ₃| 反解成 β 是 **(0,1)→(0,∞) 的严格单调双射**——3999 点网格严格递减 **3998/3998** 档、"
    "端点 (∞,0)、往返符号残差 **0**、六档（含 α、0.75、1e±6、1e30）最大相对残差 **1.5093e-65** 且逐档 ≤ 3×「往返自身条件数×算术底」"
    "⇒ 把 α 换成 0.75 或 10³⁰ 同样「得到」一个 β_match，该匹配是双射的后果而不是对 α 的择选；来料 §三 自陈「事后选择了观察者速度」在此升级为可算判决。"
    "★★**判决二 G02（不是舍入）**：来料印的 γ_match = **137.039647804709** = 闭式 √(1+α²)/α，而 α⁻¹ = **137.035999177**，"
    "差 **0.00364863**（= 7.2972554e+9 个 γ 字段半 ulp）＝展开式的 **α/2 = 0.0036486763** 前导项 ⇒「该参考系洛伦兹因子就是 137」被自家数字否证；"
    "把它说成舍入需要 γ_match 只有 8 位，而它印了 15 位。"
    "★★★**判决三 G03（一钮两靶）**：§四 的「半径对了」与 §五 的「磁矩差 2 倍」是**同一个 η=1 选择的两次计价**——"
    "两靶同时命中的唯一解 (η,ξ) = **(1, 2.0023193043609)**，需 2.0023 倍电子电荷回转（违反来料自家 ξ=1「全部电荷沿圆周旋转」）；"
    "强制 ξ=1 ⇒ η = 0.4994208455 ⇒ **L = 0.2497104228·ħ**（把 §四 的 ħ/2 打回约 ħ/4），实测 μ(ξ=1)/μ_B = 0.499999999323（残差 6.773e-10）。"
    "★**判决四 G04**：树级 g=2 的全部来源是 **[πx,πy] = iħqB** 这一叉（置 0 ⇒ μ=(q/2m)L 即 g=1；留着 ⇒ g=2）"
    "⇒ 经典环结构上给不出 2，而 G03 的 ξ\*=2(1+a_e) 与它是同一条事实的两种说法。"
    "★★★**判决五 G05（模型内硬冲突）**：|a| = c²/(Rγ²) 有限（β=0 时两条 SI 路 4.6548e+29 m/s²、相对差 2.764e-76），"
    "但提供它的横向力 F = γ_v·m·a 而模型把内部速度钉在 c ⇒ lim_{v→c⁻} γ_v^{-3} = **0**、v=1−10⁻¹⁵ 处 γ_v³ = **1.11803e+22**（15 档严格递增）⇒ **所需约束力发散**；"
    "变异体把 γ³ 挪进分母后同一套网格判据即为假（递减、末值 8.94427e-23）⇒ 承重实在「γ_v³ 在横向力关系里的位置」；"
    "**口径声明**：本条不用 sympy 的有符号左极限当判据——它把该极限印成 -oo（分支伪影，E10）。"
    "★**判决六 G06**：|μ_e|/μ_ring = **2.00231930436092** 不是测量比，是恒等式 g_e ≡ 2(1+a_e) 换分母（候选集 5 项：(1+a_e)、1/(1+a_e)、2、2*(1+a_e)、2/(1+a_e) 里恰 **1** 命中 = 2*(1+a_e)；μ_ring=½μ_B 贡献精确因子 2）。"
    "★**判决七 G07（本卷唯一 G-PASS）**：§四 四行只有 **1** 个独立数（R_Z·Ω_Z=c 是别名、f_Z=2×康普顿精确、R_Z=λ̄_C/2），"
    "且常数版本**可归因**：命中图 {2018:[F,F,F], 2022:[T,T,T]}，反解 m_e = **9.109383713882014e-31**（相对差 −1.9745e-12 < 字段分辨率 2.5896e-12，"
    "两版本差 = 分辨率的 **525.65** 倍 ⇒ 归因由位数定价，C05 反向对照把 R_Z 截到 5 位后归因立即失效）。"
    "★**判决八 G08**：L = ħ/k，k 是**自由整数**——逐 k 实测 L/ħ = 1 / 0.5 / 0.333333 / 0.25 / 0.166667（k=1,2,3,4,6）"
    "⇒「半」住在 Ω_Z = 2m_ec²/ħ 的因子 2 上，不是自旋 ½ 的来由（表示论那条路未被触碰）。"
    "★**G09 不裁定**：§七 的「50,000 组随机 boost 全通过」无 seed、「最大归一化浮点残差 6.66e-16」无分母定义 ⇒ 只印口径对照："
    "6.66e-16 = float64 eps 的 **2.999** 倍，而本卷 75 位在 1999 点网格残差 **7.07475e-74** ⇒ 该步算术底是 float64，不是它自称的 75 位精算（C09）。"
    "★★**定价 0/5 不占度**（S1 无参数预言 α / S2 观察者无关内禀比 / S3 自旋½来由 / S4 磁矩达实测 / S5 有限圆周约束——五槽全不满足，逐槽点名证据条目）；"
    "**供给 0 条**入池。**分层铁律**：64 条只覆盖 V27 一份来料，不可与 r354/r360/r365/r368/r374/r375 相加。"
    "★★**仪器自捕 15 枚（E01–E15，均已修复、未带病落盘；分层闭合 Σ=64==len(ITEMS) 由闸门 G5 现推）**，六枚值得单列："
    "E10＝拿 sympy 有符号 ±∞ 当判据 ⇒ 变异体 `F_lim != sp.oo` 为真、闸门 G2 抓到「判决未定价」；"
    "E11＝待印代码样例放进与它同种引号的定界符里 ⇒ import 期 SyntaxError＝**零判决**（比假红更坏）；"
    "E12＝act 串留了裸占位符没代入实参 ⇒ 占位符原样印进读数格＝「读数缺失被当成读数」，"
    "现升级成闸门 **G11**（对 ITEMS 五个文本字段＋判定册/数据表两张**盘面图像**现扫，命中即 RED；该闸门自身的题面第一跑也被自己判红 ⇒ 题面不得含违例形状）；E13＝G06 的候选集拿斜杠当列举分隔符，而候选者名字本身含除号（1/(1+a_e)、2/(1+a_e)）⇒ 5 项名册印到盘面上读成一个连分式，**本轮写 README 登记行时真的把它误读成 4 项**（同一缺陷在第二个读者身上复现，故不是假想）⇒ 分隔符换全角分号、名册与命中数由 B06 的 cand 现推。教训＝列举分隔符必须与元素内部字符不相交，题面的「几项」要由 len() 现推；E14＝登记器首跑把 len(str) 的**字符数**印成 bytes（标称 427695→432573，同一次写的真字节 800713→809985、+9272，中文 3 字节/字）⇒ 标签单位与取值方式脱钩，抄进台账就是假账；改＝old/new 都对编码后字节取 len，chars／bytes 各标自己的单位，幂等三跑 +0 bytes；**E15＝修 E14 时我自己造了个假数**：登记条写「真实字节 805107→809985」，而 805107 = 809985 − 4878 是拿**字符差去减字节终点**（单位混用的第二次发作，且发生在专门记录单位混用的那条里）⇒ 现测备份面 scratch/_bak_README_pre_r351.md = 800713 字节 / 427695 字符 / md5 14d5ffed…，条内数字全部改成 stat 直读。教训＝凡改一处账，新数要重新测得；由旧口径差值反推的端点＝第三个权威源，且必带旧口径的错。"
    "★**只读与越界写守卫**：正本 **11377 B / md5 729deeb1** 起点=终点（G4）；写盘白名单只含五件产物，"
    "故意向源码树临时件写一次必须被 PermissionError 拒绝且本轮真写出=False（G10）；判定册声明字节 = 盘上实测（不动点迭代收敛，G7）。"
    "★**收口只读复核另落 `源码/_out_r351_closing.txt`**（只新增该件、不覆盖，正本/README/判定册的字节在该件里写了落盘前后两行同值）："
    "这把尺不比字符串，而是**每张面的每个数由该面自己的形状正则现取、再只比值**——README 两行、`_out`、判定册各一张取数表"
    "（判定册那张按小节结构现扫：§二 表体按首格 ID、§九 按闸门名、§〇 层表按单字母行；§三/§四/§五 是 ### 与项目符号而非表格，"
    "故不能按表体行数核），**槽数与跨面格数一律由该件自己在 §2/§4/§5 印出**——登记条不手写这类计数（本把它初稿手写过一处"
    "「`_out` 15 槽」，而那张表实测 14 个键，故现改成不印），跨面格全部同值；"
    "且**针自己被打过**：1 发正对照（原文 0 红）+ 10 发单点负对照（每发只改一个数，红在该当格；其中一发在内存里伪造"
    "「字符==字节」的盘面，专打那条只读盘上的尺）⇒「绿」分不清账净还是针瞎，这一型才算定价。"
    "同轮第一把尺拿字面串（「Sigma 64」「E 15」「五槽 0/5」）在三张面之间找同一本账，于是把「这张面没用这个形状印」读成「三面不同值」"
    "⇒ 三条假红（缺陷与教训记在该件头部「缺陷自陈」段）；该条**不回写进引擎台账**——引擎与五件产物已 md5 幂等定稿，"
    "再往里加一条 E 会移动判定册的自指字节、README 两行的分层计数与全部分母，由见证件单独持有比追加更便宜、且不造第二个权威源。"
    "★**OPEN**：`X-R351-1`（非对易项 (σ·π)² 能否在纯几何、不引 q/ħ 下生成 g=2——来料 §八 自己的路线把 q、ħ 当**输入**，故该问法被前置条件消化）/ "
    "`X-R351-2`（G05 的约束力发散能否被挠率/自旋联络吸收成有限实现——来料引入 τ₃ 却未把它用到动力学上）/ "
    "`X-R351-3`（§七 补齐 seed 与归一化分母后可升级为独立复核）。"
    "**判词** `V27-SPIRAL-NULL-CONDITION-DEPENDS-ON-BOXED-ASSUMPTION--RATIO-IS-BIJECTION-ZERO-DISCRIMINATION--GAMMA-MATCH-NOT-ALPHA-INV--"
    "ONE-KNOB-TWO-TARGETS--CONSTRAINT-FORCE-DIVERGES--RATIO-IS-G-FACTOR-REBASED--SIX-ROWS-ONE-DEGREE-OF-FREEDOM--SPIN-HALF-IS-FREE-DIVISOR--SEC7-NOT-RECONSTRUCTIBLE`。"
)

JUD_FN = ("判定_TUFT-r351_ROOTV27双层光速螺旋观察者依赖与半角动量旋钮_"
          "磁矩一钮两靶与约束力发散判决_2026-11-02.md")

JUD_LINE = (
    "├── " + JUD_FN + "  # 新增（**r351 · 2026-11-02 热区回补**）：ROOT V27 判定册 —— "
    "§〇 分层声明（64 条：A14/B11/G9/C10/E15/P2/O3，**条目不可相加**）· §一 取号、分工与让渡账"
    "（不占新号；老账名册 N1–N8 逐主题点名邻居卷；去重尺正对照 5/5 + @@SCAN@@）· §二 主册 64 行（逐条含变异体名）· "
    "§三 **9 条判决明细**（G01 双射 0 bit / G02 γ_match≠α⁻¹ 差 α/2 / G03 一钮两靶 ξ\*=2.0023 / G04 g=2 来自非对易叉 / "
    "G05 约束力发散 / G06 比值=g 因子换分母 / G07 四行 1 独立数且可归因 CODATA2022 / G08 半角动量是自由除数 / G09 §七 不裁定）· "
    "§四 对照与守卫 C01–C10（每条形如「尺若不响则该判决作废」）· §五 仪器自捕 15 枚 · §六 定价与供给（五槽 **0/5 ⇒ 不占度**、入池 0 条）· "
    "§七 不裁定与 OPEN X-R351-1/2/3 · §八 终审判词与诚实边界 · §九 收口闸门 **12/12**（分母全部由 ITEMS 现推：变异体覆盖 44/44、"
    "MUT_FAILS 空、主册行数回读 64==64、正本 md5 起终同值、分层闭合 Σ=64、六件在盘非空、判定册自指尺寸不动点、登记层无红、"
    "去重尺有牙、写盘白名单有牙、无裸格式符、OPEN 必须自陈未算）· §十 产物真链接（字节数为写盘实测，本文件自身用不动点迭代自洽）。"
    "**终态** `SELF-CHECK 12/12 闸门 PASS；判决类条目 44 条全部由具名变异体定价；零带病落盘`。"
    "**治理**：靶只读、未改 `verify.py`、未 git。"
)


def main():
    s = io.open(README, encoding="utf-8", newline="").read()
    old_len = len(s.encode("utf-8"))
    old_chars = len(s)          # 写前图像自己的字符数；写后的数只能和它比，不许拿写后的 s 当「前」
    last_line = s.rstrip("\n").split("\n")[-1][:40]
    assert "\r\n" not in s, "README 出现 CRLF，登记前的 LF 假设失效"

    if not os.path.exists(BAK):
        os.makedirs(os.path.dirname(BAK), exist_ok=True)
        shutil.copy2(README, BAK)
        print("BACKUP created:", os.path.basename(BAK))
    else:
        print("BACKUP exists, keep:", os.path.basename(BAK))

    # ---- upsert：键已在 ⇒ 就地整行替换并逐行对账；键不在 ⇒ 插锚点后 / 追加末尾 ----
    lines = s.split("\n")
    pre = list(lines)
    touched = []
    changed = []      # 真正动过的登记项（NOCHANGE 不进）⇒ 用它反证「幂等跑必须 +0 字节」

    def upsert(key, anchor, text, tag, at_eof=False):
        hit = [k for k, L in enumerate(lines) if L.startswith(key)]
        if len(hit) == 1:
            k = hit[0]
            if lines[k] == text:
                print("NOCHANGE %s @line %d（文本已同步，幂等）" % (tag, k + 1))
                return
            lines[k] = text
            touched.append(k)
            changed.append(tag)
            print("UPDATE %s in place @line %d" % (tag, k + 1))
            return
        assert not hit, ("%s 键命中多行" % tag, hit)
        if at_eof:
            k = len(lines) - 1 if lines[-1] == "" else len(lines)
            lines.insert(k, text)
            changed.append(tag)
            print("APPEND %s at line %d" % (tag, k + 1))
        else:
            a = [k for k, L in enumerate(lines) if L.startswith(anchor)]
            assert len(a) == 1, ("%s anchor 命中数 != 1" % tag, a)
            lines.insert(a[0] + 1, text)
            changed.append(tag)
            print("INSERT %s after line %d" % (tag, a[0] + 1))

    upsert(SRC_KEY, SRC_ANCHOR, SRC_LINE, "src")
    upsert(JUD_ANCHOR, None, JUD_LINE, "jud", at_eof=True)

    if touched:
        assert len(lines) == len(pre), ("就地替换却改了行数", len(lines), len(pre))
        diff = [k for k, (x, y) in enumerate(zip(pre, lines)) if x != y]
        assert diff == sorted(set(touched)), ("逐行对账：变化行 != 登记行" % (), diff, touched)
    else:
        assert len(lines) - len(pre) in (0, 1, 2), (len(lines), len(pre))
    s = "\n".join(lines)

    io.open(README, "w", encoding="utf-8", newline="\n").write(s)

    # ---- 写后读回验证 ----
    t = io.open(README, encoding="utf-8", newline="").read()
    c_src = t.count(SRC_KEY)
    c_jud = t.count(JUD_ANCHOR)
    new_len = len(t.encode("utf-8"))
    new_chars = len(t)
    d_b, d_c = new_len - old_len, new_chars - old_chars
    print("bytes %d -> %d (+%d)" % (old_len, new_len, d_b))
    print("chars %d -> %d (+%d)" % (old_chars, new_chars, d_c))
    print("changed 项 = %s" % (changed or "无（两项均 NOCHANGE）"))
    if not changed:
        assert (d_b, d_c) == (0, 0), ("幂等跑却有位移", d_b, d_c)
    assert (d_b > 0) == (d_c > 0) or (d_b == d_c == 0), ("字节与字符位移方向不一致", d_b, d_c)
    assert abs(d_b) >= abs(d_c), ("|字节增量| < |字符增量| ⇒ 单位口径不成立（中文 3 字节/字）", d_b, d_c)
    print("src anchor count = %d (expect 1)" % c_src)
    print("jud anchor count = %d (expect 1)" % c_jud)
    print("prev last line kept exactly once =", t.count(last_line) == 1)
    print("touched in-place lines =", touched)
    print("no trailing blank   =", not t.endswith("\n\n"))
    print("CRLF count =", t.count("\r\n"))
    assert c_src == 1 and c_jud == 1, (c_src, c_jud)
    assert (t.count(last_line) == 1) or (len(lines) - 1 in touched), "备份末行被破坏 ⇒ 触发了伪删除"
    assert "\r\n" not in t
    return 0


SRC_LINE = SRC_LINE.replace("@@SCAN@@", SCAN_TXT)
JUD_LINE = JUD_LINE.replace("@@SCAN@@", SCAN_TXT)
assert "@@SCAN@@" not in SRC_LINE and "@@SCAN@@" not in JUD_LINE, "记号未被替换"


if __name__ == "__main__":
    sys.exit(main())
