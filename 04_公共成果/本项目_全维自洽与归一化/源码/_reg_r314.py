# -*- coding: utf-8 -*-
"""_reg_r314.py · 把 r314 卷级条目幂等登记进 README（四处链接齐备：源码/数据/判定册/可视化+runner+正本）。

纪律：
  1) 全部数字从**已落盘**的 r314 数据面（JSON summary + items）现读，登记行不引用登记之后才产生的读数；
  2) 引用的每个文件路径必须此刻在盘上，缺一个即拒写（不是写完再红）；
  3) 二进制读 + 二进制写，行尾形状（CRLF）由文件自己决定，不许文本模式混进 LF；
  4) 零删除对账：写前图像的每一行必须按原顺序出现在写后图像里；
  5) 幂等：已含「### r314 ·」则 SKIP，并且核验其恰出现一次。
"""
import io
import json
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))          # .../本项目_全维自洽与归一化/源码
BASE = os.path.dirname(ROOT)                              # .../本项目_全维自洽与归一化
README = os.path.join(BASE, "README.md")
RID = "r314"
STAMP = "2026-11-01"


def rel(p):
    return os.path.relpath(p, BASE).replace(os.sep, "/")


def face(d, name):
    p = os.path.join(BASE, d, name)
    return p


# ---- 本卷五张面 + 正本 + runner + 输出（路径必须现读存在）----
SRC = face("源码", "TUFT-r314_ROOTV21固定点机制独立复核与截断自等价定理与f0可证伪窗口与记忆擦除律与格点基准率与六格门禁_精算与可视化_2026-11-01.py")
DATA_JSON = face("数据", "TUFT-r314_ROOTV21固定点机制独立复核与截断自等价定理与f0可证伪窗口与记忆擦除律与格点基准率与六格门禁_精算与可视化_2026-11-01.json")
DATA_MD = face("数据", "TUFT-r314_ROOTV21固定点机制独立复核与截断自等价定理与f0可证伪窗口与记忆擦除律与格点基准率与六格门禁_精算与可视化_2026-11-01.md")
DATA_REP = face("数据", "TUFT-r314_ROOTV21固定点机制独立复核与截断自等价定理与f0可证伪窗口与记忆擦除律与格点基准率与六格门禁_精算与可视化_2026-11-01_report.txt")
DATA_LIA = face("数据", "TUFT-r314_ROOTV21固定点机制独立复核与截断自等价定理与f0可证伪窗口与记忆擦除律与格点基准率与六格门禁_精算与可视化_2026-11-01_来料原件_ROOT_V21.0_用户附件逐字_2026-11-01.md")
JUD = face("判定", "判定_TUFT-r314_ROOTV21固定点机制独立复核与截断自等价定理与f0可证伪窗口与记忆擦除律与格点基准率与六格门禁_精算与可视化_2026-11-01.md")
HTML = os.path.join(BASE, "四力统一方程_ROOTV21耦合固定点机制审计_r314可视化_2026-11-01.html")
RUNNER = face("源码", "_run_r314.py")
OUTF = face("源码", "_out_r314.txt")

PATHS = [("源码", SRC), ("数据 json", DATA_JSON), ("数据 md", DATA_MD), ("数据 report", DATA_REP),
         ("来料正本", DATA_LIA), ("判定册", JUD), ("可视化", HTML), ("runner", RUNNER), ("stdout", OUTF)]


def kv(item_id):
    for it in SUM["__items__"]:
        if it["id"] == item_id:
            return it["kv"]
    raise KeyError(item_id)


missing = [(n, rel(p)) for n, p in PATHS if not os.path.isfile(p)]
if missing:
    print("REFUSE：以下被引用路径不在盘上：%s" % missing)
    sys.exit(2)

raw = io.open(DATA_JSON, "rb").read()
doc = json.loads(raw.decode("utf-8"))
SUM = doc["summary"]
SUM["__items__"] = doc["items"]

main = [i for i in doc["items"] if i["layer"] not in ("控制组", "守卫")]
ctl = [i for i in doc["items"] if i["layer"] == "控制组"]
grd = [i for i in doc["items"] if i["layer"] == "守卫"]
m_pass = sum(1 for i in main if i["verdict"] == "PASS")
m_fail = sum(1 for i in main if i["verdict"] == "FAIL")
m_bnd = sum(1 for i in main if i["verdict"] == "BOUNDARY")
m_inf = sum(1 for i in main if i["verdict"] == "INFO")
fail_ids = sorted(i["id"] for i in main if i["verdict"] == "FAIL")
assert len(main) + len(ctl) + len(grd) == SUM["条目总数"], "分账与总账不平"

v7 = kv("V7")
v10 = kv("V10")
v14 = kv("V14")
v3 = kv("V3")
n_neg = sum(1 for i in ctl if i["kv"].get("型") == "负对照")
n_pos = sum(1 for i in ctl if i["kv"].get("型") == "正对照")

# ---- 载体绑定：README 里每一个数字都从**已落盘**的读数面取回，不带手写值 ----
MD_TEXT = io.open(DATA_MD, "rb").read().decode("utf-8")
BY_ID = {i["id"]: i for i in doc["items"]}


def grab(item_id, pattern, label):
    """①该条目的 detail/kv 里必须按正则命中；②命中的 token 必须逐字出现在已落盘的 md 面上。
    任一不中 ⇒ 当场拒写（rc=2）：登记面不许出现没有载体可核对的数字。"""
    it = BY_ID.get(item_id)
    if it is None:
        print("REFUSE：数据面没有条目 %s（要取 %s）" % (item_id, label))
        sys.exit(2)
    hay = it["detail"] + "\n" + json.dumps(it["kv"], ensure_ascii=False)
    m = re.search(pattern, hay)
    if not m:
        print("REFUSE：%s 面上取不到 %r（%s）" % (item_id, pattern, label))
        sys.exit(2)
    tok = m.group(1) if m.groups() else m.group(0)
    if tok not in MD_TEXT:
        print("REFUSE：token %r（%s）逐字不在 md 面上 ⇒ 无载体" % (tok, label))
        sys.exit(2)
    return tok


def vf(item_id, key):
    """kv 里的值必须**逐字**出现在 md 面上才许进 README：不截断、不四舍五入、不改写。"""
    v = str(BY_ID[item_id]["kv"][key])
    if v not in MD_TEXT:
        print("REFUSE：%s.kv[%s]=%r 逐字不在 md 面上 ⇒ 它不是面上印出的读数" % (item_id, key, v))
        sys.exit(2)
    return v


G = {
    "v7_rate": grab("V7", r"斜率 = 17/\(3π\) = ([\d.]+)", "V7 链斜率"),
    "v7_mu10": grab("V7", r"M_U=([\d.e+]+) GeV", "V7 f0=10 反演能标"),
    "n_anchor": grab("C1", r"锚点命中 (\d+)/", "C1 打印锚点数"),
    "n_mut": grab("C2", r"共 4×10=(\d+) 枚", "C2 变异体枚数"),
    "v6_ratio": grab("V6", r"数值核对 (\[[^\]]*\])", "V6 带号比三值"),
    "v7_bij": grab("V7", r"往返残差 ≤\s*([\de.e+-]+)（双射）", "V7 双射往返残差"),
    "v8_avail": grab("V8", r">可达 (\d+\.\d+)", "V8 可达十进距"),
    "v8_n1": grab("V8", r"N=(1\.9998\d*)", "V8 ε=1 行擦除预算"),
    "v8_n2": grab("V8", r"N=(28\.06\d*)", "V8 ε=0.1 行擦除预算"),
    "v8_n44": grab("V8", r"⇒ N≥(\d+) >", "V8 微扰区下界"),
    "v9_hits": grab("V9", r"候选有 (\d+) 个", "V9 零偏差命中数"),
    "v9_gap": grab("V9", r"格距 ([\d.]+) ppm", "V9 相邻格距 ppm"),
    "v9_half": grab("V9", r"半格 ([\d.]+)", "V9 半格 ppm"),
    "v9_tol": grab("V9", r"距目标 ≤([\d.]+) ppm 的先验", "V9 实测容差 ppm"),
    "v9_rate": grab("V9", r"先验比例 = ([\d.]+)", "V9 基准率"),
    "v9_grid": grab("V9", r"ε∈\(0,1\] 的 (\d+) 点网格", "V9 第二口径网格"),
    "v9_1ppm": grab("V9", r"降到 ([\d.]+)", "V9 tol=1ppm 基准率"),
    "v9_023": grab("V9", r"占比 = ([\d.]+)", "V9 第二口径占比"),
    "v6_8of8": grab("V6", r"精确断言，([\d/]+) 通过", "V6 闭式逐整数通过数"),
    "v14_refgap": grab("V14", r"（差 ([\d.eE+-]+)）", "V14 85 位对 140 位裁判差"),
    "v14_rows": grab("V14", r"BZ 全表 (\d+) 行中有", "V14 第二口径分母"),
    "v14_print": grab("V14", r"r313 印 ([0-9.]+)，距裁判", "V14 r313 面读数"),
    "c5_ratio": grab("C5", r"比值 ([\d.]+)", "C5 两容差比值"),
    "c3_live": grab("C3", r"f0=(\d+) → 预测", "C3 存活示例 f0"),
    "c3_rej": grab("C3", r"存活；f0=(\d+) →", "C3 拒绝示例 f0"),
    "c3_excl": grab("C3", r"排除集=(\[[^\]]*\])", "C3 排除集"),
    "codata": grab("V11", r"(137\.035999177\(21\))", "CODATA 2022 锚点"),
    "v11_val": grab("V11", r"数值一致：([\d.]+) ", "V11 锚点数值"),
    "lia_bytes": grab("C1", r"字节=(\d+)", "来料正本字节数"),
    "v14_rows2": grab("V14", r"字节=(\d+)、mtime", "r313 面字节数"),
}

# ---- stdout 面（runner 捕获）：rc、五张面指纹、FAIL 名单都从它现读 ----
OUT_TEXT = io.open(OUTF, "rb").read().decode("utf-8", errors="replace")


def outgrab(pattern, label):
    m = re.search(pattern, OUT_TEXT)
    if not m:
        print("REFUSE：stdout 面取不到 %r（%s）" % (pattern, label))
        sys.exit(2)
    return m.group(1) if m.groups() else m.group(0)


RC_RUN = outgrab(r"RC = (\d+)", "runner 退出码")
MD5S = re.findall(r"md5=([0-9a-f]{32})", OUT_TEXT)
assert len(MD5S) == 5, "stdout 面指纹不是五张（实收 %d）⇒ 面名册变了，先对齐再登记" % len(MD5S)
FACE_ORDER = ["数据 json", "数据 md", "数据 report", "判定册", "可视化 html"]
m_fail_out = re.search(r"FAIL 主条目.*?\[(.*?)\]", OUT_TEXT)
fail_out = sorted(re.findall(r"'([^']*)'", m_fail_out.group(1))) if m_fail_out else None
assert fail_out == fail_ids, "stdout 的 FAIL 名单 %s ≠ 数据面 %s" % (fail_out, fail_ids)



live_md5 = {"数据 json": DATA_JSON, "数据 md": DATA_MD, "数据 report": DATA_REP,
            "判定册": JUD, "可视化 html": HTML}
for _n, _h in zip(FACE_ORDER, MD5S):
    now = hashlib.md5(io.open(live_md5[_n], "rb").read()).hexdigest()
    if now != _h:
        print("REFUSE：%s 盘上 md5=%s ≠ stdout 面指纹 %s ⇒ 面在跑完后又被改过" % (_n, now, _h))
        sys.exit(2)

TITLE = ("### %s · %s · ROOT V21 同来料第二把尺：截断自等价定理 / f0 可证伪窗口 / 记忆擦除律 / "
         "格点基准率 / 六格门禁（★外部来料审计层 · 承 r304/r308/r313 判词链 · ★让号 r308→r314 "
         "· ★本卷自抓三处仪器坑）" % (RID, STAMP))

L = []
A = L.append
A(TITLE)
A("")
A("- **产物**：源码 [`TUFT-r314_…py`](%s)；数据 [`…json`](%s) / [`…md`](%s) / "
  "[`…_report.txt`](%s)；判定册 [`判定_TUFT-r314_…md`](%s)；runner `源码\\_run_r314.py` → "
  "`源码\\_out_r314.txt`；交互可视化 [`四力统一方程_ROOTV21耦合固定点机制审计_r314可视化_"
  "%s.html`](%s)；来料正本 [`…_来料原件_ROOT_V21.0_用户附件逐字.md`](%s)。"
  % (rel(SRC), rel(DATA_JSON), rel(DATA_MD), rel(DATA_REP), rel(JUD), STAMP, rel(HTML), rel(DATA_LIA)))
A("- **复现**：`python -X utf8 源码\\_run_r314.py` ⇒ **rc=%s**（由 stdout 面 `RC =` 行现读），条目 **%d**"
  "（主 **%d**：**PASS %d / FAIL %d / BOUNDARY %d / INFO %d**），**控制组 %d/%d**（拒绝型负对照 %d 枚 + "
  "正对照 %d 枚），**守卫 %d/%d**，mpmath %s 位 + sympy 符号精确，耗时 %s s。★**两条 FAIL（%s）"
  "是判给「路线解释力」的设计性 FAIL，不否来料算术**——来料每个可计算数字全部复现为真"
  "（V1–V5 逐位、V6 闭式 %s、V12 %s 行审计表逐行挂载体；stdout 面的 FAIL 名单与数据面的 FAIL 名单"
  "在写入前逐字对过）。"
  % (RC_RUN, SUM["条目总数"], len(main), m_pass, m_fail, m_bnd, m_inf,
     len([i for i in ctl if i["verdict"] == "PASS"]), len(ctl), n_neg, n_pos,
     len([i for i in grd if i["verdict"] == "PASS"]), len(grd), SUM["精度位"], SUM["耗时秒"],
     "、".join(fail_ids), G["v6_8of8"], kv("V12")["总行数"]))
A("- **面指纹（登记时现算，与 stdout 面逐张对上）**：%s。" % "；".join(
    "%s md5=%s" % (n, h) for n, h in zip(FACE_ORDER, MD5S)))
A("- **命题与分工（★让号如实登记）**：同一份 ROOT V21.0 来料已由并行卷 **r313** 落库并注册；本卷起草时"
  "占 **r308**，实测 r308 已被并行《ROOT V22》卷齐套占用、随后 r313 又占了同来料的 V21 号 ⇒ 按"
  "「先占四件套者为权威、后到者整体改号、不删不改他人文件」让号 **r308→r314**（RID/BASE/引擎文件名/"
  "runner/数据/判定/HTML 联动，正本 %s B 逐字未动）。本卷**不重复** r313 的路线互消与搬家定理，"
  "两卷**不可相加**；对同一事实取较严者。" % G["lia_bytes"])
A("- **V1–V5 · 来料算术全真**：4D QED 一圈固定点集 {0}、4−ε 的 α*=3πε/(2N_f) 与 β'(α*)=ε、"
  "N_f^{req}=%s → 646、α*(646)=%s、偏差 %s ppm（来料 360.79）、SU(3) 两圈四值与 α_s*(16)=2π/151、"
  "谱几何 f(0)=10/20/40 三值与 sin²θ_W=3/8 ⇒ 正本 %s 条打印锚点全部在半 ulp 内复现（C1），"
  "%s 枚 ±1/±2 ulp 变异体全红（C2）。"
  % (vf("V3", "Nf_star"), vf("V3", "a646"), vf("V3", "abs_ppm"),
     G["n_anchor"], G["n_mut"]))
A("- **★V6 截断自等价定理（新增，符号）**：任何两项截断 β 在其固定点处「末项/首项」**带号恒等 = −1**"
  "（BZ 与 4−ε 两族各自 SymPy 精确，N_f=12/15/16 数值核对 %s）⇒ α*≤0.15 的「微扰可用」"
  "不等于级数自洽，固定点位置不是可收敛级数的读数；BZ 闭式 α*(N_f)=2π(33−2N_f)/(19N_f−153) 全表 "
  "N_f=9..16、单调性 dα*/dN_f=−642π/(19N_f−153)²、整数正根 {9..16} 由 N_f=1..40 扫描现推。"
  % G["v6_ratio"])
A("- **★V7 f(0) 从自由参数压成可证伪窗口（新增）**：SM 一圈链 1/α(0)=64f0/(3π)+阈值和+斜率·ln(M_U/M_Z)"
  "（阈值和 %s、斜率 %s 全由锚现推）＋M_U∈[M_Z,M_Pl] ⇒ f0∈[%s, %s]，来料三个示例值恰排除 %s、"
  "存活 %s；f0↔M_U 双射往返残差 ≤%s，f0=10 ⇔ M_U=%s GeV。**正面回答 r313 的 X-R313-4**："
  "「像覆盖 (0,∞) ⇒ 零判别力」是树级口径的产物，带跑动与区间后集合可证伪。"
  % (vf("V7", "thr"), G["v7_rate"], vf("V7", "f0_min"), vf("V7", "f0_max"),
     vf("V7", "excluded"), vf("V7", "survived"), G["v7_bij"], G["v7_mu10"]))
A("- **★V8 记忆擦除律（新增）**：T(ρ)=∂lnα/∂lnα0 闭式与精确反演两口径同号；统一阈值 η=1%% ⇒ "
  "4−ε 族仅 ε=1 行来得及擦除（N=%s ≪ 可达 log10(M_Pl/M_Z)=%s），ε=0.1 行 N=%s 超时；"
  "BZ 线性读法 N=1/θ 与恒等式 β'=α*(33−2N_f)/(6π) ⇒ **微扰可用（N_f≥15）的 BZ 固定点必有 N≥%s**，"
  "微扰性与擦除速度不相容。★方向本身是新结果：唯一来得及擦除初值记忆的那一行，恰是唯一非微扰的那一行。"
  % (G["v8_n1"], G["v8_avail"], G["v8_n2"], G["v8_n44"]))
A("- **★V9（设计红）格点基准率**：ε 自由时 **%s 个零偏差命中**（「命中 α」在整数格上是常态）；"
  "ε=1 时相邻 N_f 的 ppm 间隔 ≈%s ⇒ 半格 ≈%s ppm，实测 %s ppm 的先验比例 ≈%s"
  "（%s 点 float64 第二口径占比 %s 同向），而 tol=1 ppm 时 ≈%s ⇒ 「近失」必须由基准率定价，"
  "不由印象定价；另机判圈参数恒等式 (2N_f/3π)·α*≡ε ⇒ 来料的「拟合」不含一位新信息。"
  % (G["v9_hits"], G["v9_gap"], G["v9_half"], G["v9_tol"], G["v9_rate"],
     G["v9_grid"], G["v9_023"], G["v9_1ppm"]))
A("- **★V10（设计红）六格门禁矩阵**：s1 存在性/s2 稳定性/s3 微扰一致性/s4 无自由参数/s5 四维 U(1)_em/"
  "s6 低能唯一映射——四条真实路线最高 **%s/6**，且机判二分定理 **¬(s2∧s5)**（凡有红外吸引子者必失 "
  "s3/s5）；合成理想路线 6/6（C6）⇒ 缺口不是「再算一次」，是**需要一个四维电磁耦合自身的吸引子**。"
  % vf("V10", "最高分"))
A("- **★V14 对表并发卷 r313（只读引用，未触字节）**：从 r313 精算面（%s B，md5 见 V14）正则取出 %s 个"
  "打印读数，本卷独立复算后 **%s/%s 逐位一致、%s 枚面上取不到**，并现场印出该面 md5=%s 作为引用锚；"
  "第二口径：BZ 全表 %s 行中有 %s 行的本卷 10 位读数同现于其面。相消比同口径（本卷带号恒等 ≡ %s）；"
  "r313 的 G6/G7 两枚恒等式守卫在其面上印 FAIL，本卷独立复算这两条恒等式为真 ⇒ 只登记为「恒等式级"
  "守卫被路线级判决捆住」的仪器型态观察（X-R314-7），**不裁定他卷、不改他字节**。"
  % (G["v14_rows2"], vf("V14", "锚数"), vf("V14", "命中"), vf("V14", "锚数"),
     vf("V14", "取不到"), vf("V14", "面md5"), G["v14_rows"], vf("V14", "第二口径同现行"),
     vf("V14", "同口径相消比")))
A("- **★本卷自抓三处仪器坑（对表把自己也照了一遍，全部留在面上）**：①**X-R314-9 假精度**——"
  "`sp.N(sympify(mp.mpf),28)` 名义 28 位、实为 float64 的 16 位，首版据此把 r313 的正确读数判成"
  "「矛盾」；现算裁判：闭式反解 N_f* 在 85 位=%s 与 140 位=%s 差 %s，r313 印 %s 距裁判 "
  "%s 个 ulp64（double 口径内正确），本卷 SymPy 路距 %s 个 ulp64 ⇒ 跨库传常数必须先证明目标库吃得到"
  "那个位数。②**X-R314-10 假零**——子串探测器吃下已被 `mp.nstr` 转成带引号字符串的读数 ⇒ 误印"
  "「0 行同现」；现配正/负对照自测（在场 token 必亮、缺席 token 必灭），旧写法的带引号前缀缺席做成"
  "现场见证。③**X-R314-11 假阳**——守卫 G7 原按「题面含『负对照』字样」数牙齿，措辞一改就红；"
  "改由登记时声明的 `kv[\"型\"]` 计数（拒绝型 %d 枚 + 正对照 %d 枚）。"
  % (vf("V14", "BZ反解_85位"), vf("V14", "BZ反解_140位裁判"), G["v14_refgap"],
     G["v14_print"], vf("V14", "r313_距裁判ulp64"),
     vf("V14", "BZ反解_SymPy路距裁判ulp64"), n_neg, n_pos))
A("- **控制组（%d/%d，正负双对照）**：C1 来料正本 %s 个打印锚点在盘上逐字命中（正）｜C2 %s 枚 ±1/±2 ulp "
  "变异体全红（牙）｜C3 f0 排除恰 %s 且 %s 活/%s 拒（牙）｜C4 擦除判据双向有效（牙）｜"
  "C5 基准率把 tol=%s ppm（先验 %s）与 tol=1 ppm（先验 %s）分开 %s 倍（牙）｜"
  "C6 合成理想路线 6/6（正，证明门禁可达非空判）｜C7 精确解回代残差=0 而指数改 ε/2 残差≠0（牙）。"
  % (len([i for i in ctl if i["verdict"] == "PASS"]), len(ctl),
     G["n_anchor"], G["n_mut"], G["c3_excl"], G["c3_live"], G["c3_rej"],
     G["v9_tol"], G["v9_rate"], G["v9_1ppm"], G["c5_ratio"]))
A("- **判据集 R1–R6**：%s（V13，与 r311/r313 同族不可相加）。**判词**：%s"
  % (SUM["判据集"], SUM["判词"]))
A("- **诚实边界**：①α⁻¹(0)=%s 的**现行版本**只由二手来源支撑（NIST 常数页直取失败，"
  "X-R314-1，V11 判 BOUNDARY），引用本卷 ppm/σ 时须一并读出；②谱几何系数 f(0)/(2π²)·(1/4) 未独立推导（X-R314-2）；"
  "③4−ε 与 BZ 的两圈及以上系数为文献口径（X-R314-3）；④f0 窗口是**一圈**口径，阈值修正或 M_U 越过 "
  "M_Pl 会重新放大窗口（X-R314-4/8）；⑤M_U=%s GeV 与本库 r303 无阈值统一排除的张力未清算"
  "（X-R314-5）；⑥V6 的 ≡−1 恒等只约束微扰截断，不约束非微扰严格解（X-R314-6）。"
  % (G["codata"], G["v7_mu10"]))
A("- **治理**：未改 `verify.py`；未跑 `refresh_catalog.py`（并发活跃，整体重生成会回退他人更大版本）；"
  "未触碰任何既有卷字节——对 r313/r308(ROOT V22) 全为只读，引用其数字时连同 V14 现场印出的 md5 一起读；"
  "守卫 G12（仅写本卷路径）逐路径核验、G13（五张面名册齐备）现场探过；git 由收口提交统一处理"
  "（未获授权前不提交）。"
  "**本卷 %d 条不可与 r142–r313 各卷相加**。★登记面形状沿用现行约定（r311/r312/r313 同形）："
  "本 README 的旧「源码树/判定树/数据树」三张清单已停更，四处齐全＝本小节的**源码／数据三件／判定册／"
  "可视化+runner+正本**链接。**下轮从 r315 起现扫三树 + README 取号**（并行链极活跃）。" % SUM["条目总数"])
A("- **事故与修复（如实登记）**：首跑 rc=2，四处红——①**V6 真红**：正性域合取里遗留一条自己写的假重言"
  "（`33/2 == 99/4*2` 恒假），删掉后改由 N_f=1..40 扫描 + ceiling/floor 现推窗口端点；②**V14 假红**："
  "见上条 X-R314-9/10；③**G7 假阳**：见 X-R314-11；④**G8 空转**：棘轮把 FAIL 名单硬写成 "
  "`[\"V9\",\"V10\"]`，而 `sorted()` 的真实顺序是 `%s` ⇒ 即使全对也永不绿；改为键在模块级"
  "预注册常量 `DESIGN_FAIL` 上并现算顺序。**没有放松任何判据**，二跑 rc=%s。"
  % (fail_ids, RC_RUN))
A("")

BLOCK = "\r\n".join(L)

# ---- 载体审计：登记小节里每一个「数字.数字」都必须逐字出现在已落盘的 md 面或来料正本上 ----
LIA_TEXT = io.open(DATA_LIA, "rb").read().decode("utf-8")
NUMTOK = re.findall(r"\d+\.\d+", BLOCK)
no_carrier = sorted({t for t in NUMTOK if t not in MD_TEXT and t not in LIA_TEXT})
if no_carrier:
    print("REFUSE：登记小节有 %d 枚小数无载体（md 面/正本逐字找不到）：%s"
          % (len(no_carrier), no_carrier))
    sys.exit(2)
print("载体审计：登记小节小数 %d 枚（去重 %d 枚），全部逐字挂在 md 面或正本上"
      % (len(NUMTOK), len(set(NUMTOK))))

# ---- 判词一致性：README 印的判词必须逐字住在判定册面上，且旧写法不留存 ----
JUD_TEXT = io.open(JUD, "rb").read().decode("utf-8")
STALE = "ATTRACTIVITY-ORTHOGONAL-EM "
if SUM["判词"] not in JUD_TEXT or SUM["判词"] not in MD_TEXT:
    print("REFUSE：README 判词未逐字住在判定册面或数据面上")
    sys.exit(2)
if STALE.strip() in JUD_TEXT or STALE.strip() in MD_TEXT or STALE.strip() in BLOCK:
    print("REFUSE：面上仍留存旧判词写法 %r ⇒ 同一判词两种拼法" % STALE.strip())
    sys.exit(2)
print("判词一致性：README/判定册/数据面三处逐字同一，旧拼法留存 0")

b = io.open(README, "rb").read()
PRE_MD5 = hashlib.md5(b).hexdigest()          # 写前图像指纹：写后剪尾必须能逐字节重建它
nl = "\r\n" if b.count(b"\r\n") else "\n"
old = b.decode("utf-8")
old_lines = old.split(nl)

marker = "### %s ·" % RID
if marker in old:
    n = sum(1 for l in old_lines if l.startswith(marker))
    print("SKIP：README 已含 %s 小节（%d 处）；未写入。" % (RID, n))
    sys.exit(0 if n == 1 else 2)

# 追加位置：文件末尾（去掉尾部空行后补两个空行分隔），保持原行序零删除
tail = old_lines[:]
while tail and tail[-1].strip() == "":
    tail.pop()
n_trim = len(old_lines) - len(tail)
new_lines = tail + [""] + L + [""]
new = nl.join(new_lines)

# 零删除对账：写前每一行（去掉尾部空行后）必须按原顺序原样出现在写后
it = iter(new_lines)
kept = 0
for l in tail:
    for x in it:
        if x == l:
            kept += 1
            break
    else:
        print("REFUSE：写前图像有一行在写后消失 ⇒ %r" % l[:80])
        sys.exit(2)
assert kept == len(tail), "逐行对账不平"
assert new.count(marker) == 1 and old.count(marker) == 0

hdr = [l for l in new_lines if l.startswith("### ")]
print("写前 行=%d 字节=%d（尾部空行剪 %d）" % (len(old_lines), len(b), n_trim))
print("写后 行=%d 字节=%d 小节数=%d（本卷小节 %d 处）"
      % (len(new_lines), len(new.encode("utf-8")), len(hdr), new.count(marker)))
print("新增行=%d（=%d 行小节正文） 删除行=%d" % (len(new_lines) - len(old_lines), len(L),
                                        len(old_lines) - len(new_lines) if len(new_lines) < len(old_lines) else 0))
if "--dump" in sys.argv:
    scratch = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(BASE))), "scratch")
    io.open(os.path.join(scratch, "r314_reg_block.txt"), "wb").write(BLOCK.encode("utf-8"))
    print("DUMP：登记小节文本已写入 scratch/r314_reg_block.txt（未写 README）")
    sys.exit(0)
if "--check" in sys.argv:
    print("DRY-RUN：未写盘。")
    sys.exit(0)

io.open(README, "wb").write(new.encode("utf-8"))

# 写后从盘上图像复核（不吃拼装模板）
b2 = io.open(README, "rb").read()
t2 = b2.decode("utf-8")
n_crlf = b2.count(b"\r\n")
n_lf = b2.count(b"\n")
chk = {
    "本卷小节恰 1 处": sum(1 for l in t2.split(nl) if l.startswith(marker)) == 1,
    "剪尾后的写前图像是写后的逐行前缀": all(a == b for a, b in zip(t2.split(nl), tail)),
    "写后 == 写前 + 空行 + 本卷小节 + 空行": t2.split(nl) == tail + [""] + L + [""],
    "写前 md5 可由写后剪尾重建（零删除的第二口径）":
        hashlib.md5((nl.join(tail) + nl * n_trim).encode("utf-8")).hexdigest() == PRE_MD5,
    "CRLF 形状不变": (n_crlf == n_lf) if nl == "\r\n" else True,
    "被引用路径仍全部在盘上": all(os.path.isfile(p) for _, p in PATHS),
}
for k, v in chk.items():
    print("  %s %s" % ("PASS" if v else "FAIL", k))
print("README md5=%s 字节=%d" % (
    __import__("hashlib").md5(b2).hexdigest(), len(b2)))
rc = 0 if all(chk.values()) else 2
print("RC =", rc)
sys.exit(rc)
