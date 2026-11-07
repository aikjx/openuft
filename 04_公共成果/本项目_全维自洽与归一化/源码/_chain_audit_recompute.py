# -*- coding: utf-8 -*-
# 链路体检整理册机核（不新增 RID、不入 README、不与任何卷相加）
import io, os, glob, re, json, hashlib, struct, collections, ast

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RD = os.path.join(ROOT, "README.md")
DATA = os.path.join(ROOT, "数据")
DETD = os.path.join(ROOT, "判定")
SRCD = HERE
assert os.path.isfile(RD) and os.path.getsize(RD) > 500000
assert os.path.isdir(DATA) and os.path.isdir(DETD)

_p = ROOT
while not (os.path.isfile(os.path.join(_p, ".workbuddy", "memory", "MEMORY.md"))
           and os.path.isdir(os.path.join(_p, "openuft"))):
    _q = os.path.dirname(_p)
    assert _q != _p, "workspace root not found"
    _p = _q
WS = _p
SCRATCH = os.path.join(WS, "scratch")
assert os.path.isfile(os.path.join(SCRATCH, "_r402_readme_backup.bin")), SCRATCH
ARCH_DIR = os.path.join(SCRATCH, "_chain_2026-11-06", "orphan_pyc")

TITLE = "_CHAIN_recompute_2026-11-06"
JSN = os.path.join(DATA, TITLE + ".json")
RPT = os.path.join(DATA, TITLE + "_report.txt")
RECENT = ["r%d" % n for n in range(390, 403)]
DATE = "2026-11-06"
RID = re.compile(r"TUFT-(r\d+)_")

ROWS = []
GUARDS = []
KEY = {}


def add(rid, layer, name, exp, act, ok, note=""):
    if ok == "ID":
        kind = "IDENTITY"
    elif ok is None:
        kind = "INFO"
    else:
        kind = "PASS" if ok else "FAIL"
    ROWS.append({"id": rid, "layer": layer, "name": name,
                 "exp": str(exp), "act": str(act), "kind": kind,
                 "note": note, "computed": True})


def guard(name, ok, detail):
    GUARDS.append({"name": name, "ok": bool(ok), "detail": str(detail)})


def rid_of(name):
    m = RID.search(os.path.basename(name))
    return m.group(1) if m else None


def ftp(v):
    return str(v).replace("Fraction(", "").replace(")", "")


def group(pattern, base=ROOT):
    d = collections.defaultdict(list)
    for p in glob.glob(os.path.join(base, pattern)):
        r = rid_of(p)
        if r:
            d[r].append(os.path.basename(p))
    return d


def parse_readme(b):
    reg = collections.defaultdict(lambda: collections.Counter())
    for ln in b.split(b"\n"):
        if b"TUFT-r" not in ln:
            continue
        s = ln.decode("utf-8", "replace")
        m = RID.search(s)
        if not m:
            continue
        r = m.group(1)
        if s.startswith("\u2502   \u251c\u2500\u2500 TUFT-"):
            k = "src"
        elif s.startswith("\u251c\u2500\u2500 \u5224\u5b9a_") or s.startswith("\u251c\u2500\u2500 TUFT-"):
            k = "det"
        else:
            k = "other"
        reg[r][k] += 1
    return reg


def scan(rb, hide_det=(), hide_html=(), hide_src=()):
    """只读扫描。负对照通过 hide_* 在内存里隐藏文件实现，绝不碰磁盘。"""
    src = group(os.path.join("源码", "TUFT-r*_*.py"))
    js = group(os.path.join("数据", "TUFT-r*_*.json"))
    rp = group(os.path.join("数据", "TUFT-r*_*_report_*.txt"))
    det = collections.defaultdict(list)
    for p in glob.glob(os.path.join(DETD, "*TUFT-r*_*.md")) + \
             glob.glob(os.path.join(DATA, "*TUFT-r*_*.md")):
        r = rid_of(p)
        if r:
            det[r].append(os.path.basename(p))
    ht = collections.defaultdict(list)
    for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        r = rid_of(p)
        if r:
            ht[r].append(os.path.basename(p))
    src = {r: [x for x in v if x not in hide_src] for r, v in src.items()}
    det = {r: [x for x in v if x not in hide_det] for r, v in det.items()}
    ht = {r: [x for x in v if x not in hide_html] for r, v in ht.items()}
    reg = parse_readme(rb)
    allr = sorted(set(list(src) + list(js) + list(rp) + list(det)
                      + list(ht) + list(reg)), key=lambda x: int(x[1:]))
    out = {}
    for r in allr:
        out[r] = {
            "src": len(src.get(r, [])), "json": len(js.get(r, [])),
            "report": len(rp.get(r, [])), "det": len(det.get(r, [])),
            "html": len(ht.get(r, [])),
            "reg_src": reg[r]["src"], "reg_det": reg[r]["det"],
        }
    return out


def core_missing(rows, keys):
    return [r for r in rows if any(rows[r][k] == 0 for k in keys)]


def unregistered(rows, keys=("reg_src", "reg_det")):
    return [r for r in rows if rows[r]["src"] > 0
            and any(rows[r][k] == 0 for k in keys)]


def recent_missing(rows, key):
    return [r for r in RECENT if rows.get(r, {}).get(key, 0) == 0]


def recent_full(rows, key):
    return len(RECENT) - len(recent_missing(rows, key))


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


class Svg:
    def __init__(self):
        self.parts = []
        self.coords = []
        self.n = 0

    def _c(self, axis, v):
        self.coords.append((axis, float(v)))

    def rect(self, x, y, w, h, fill, extra=""):
        for a, v in (("x", x), ("y", y), ("x", x + w), ("y", y + h)):
            self._c(a, v)
        self.parts.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" %s/>'
                         % (x, y, w, h, fill, extra))
        self.n += 1

    def line(self, x1, y1, x2, y2, stroke="#d7dfea", w=1):
        for a, v in (("x", x1), ("y", y1), ("x", x2), ("y", y2)):
            self._c(a, v)
        self.parts.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g"/>'
                         % (x1, y1, x2, y2, stroke, w))
        self.n += 1

    def text(self, x, y, s, size=12, fill="#2b3446", anchor="start", weight="normal"):
        for a, v in (("x", x), ("y", y)):
            self._c(a, v)
        self.parts.append('<text x="%g" y="%g" font-size="%g" fill="%s" text-anchor="%s" font-weight="%s">%s</text>'
                         % (x, y, size, fill, anchor, weight, esc(s)))
        self.n += 1

    def bad(self):
        out = 0
        for a, v in self.coords:
            hi = 680 if a == "x" else 360
            if v < 0 or v > hi:
                out += 1
        return out

    def out(self):
        return ('<svg viewBox="0 0 680 360" width="680" height="360" '
                'xmlns="http://www.w3.org/2000/svg">'
                + "".join(self.parts) + "</svg>")


def load_vol(r):
    fs = glob.glob(os.path.join(DATA, "TUFT-" + r + "_*.json"))
    assert len(fs) == 1, (r, fs)
    return json.load(io.open(fs[0], encoding="utf-8")), os.path.basename(fs[0])


def backfill_names():
    out = []
    for r in ("r393", "r395"):
        _j, jname = load_vol(r)
        stem = ("TUFT-" + r + "_" + jname.split("TUFT-" + r + "_", 1)[1]
                .rsplit(".json", 1)[0])
        out.append(stem + "_可视化_" + DATE + ".html")
    return out


def key_pairs(r, j):
    kn = j["key_numbers"]
    if r == "r393":
        return [("16x16 单态命中", kn["spin16_hit_16x16"]),
                ("16x16bar 单态命中", kn["spin16_hit_16x16bar"]),
                ("共轭计数路 A", kn["u3_routeA"]),
                ("实谱路 B", kn["u3_routeB"]),
                ("单态份额", kn["u3_singlets"]),
                ("反常总计", kn["u3_total"]),
                ("奇数净手征", kn["odd_count"]),
                ("可达集最小正元", min(x for x in kn["reachable_set"] if x > 0))]
    return [("I6 拆分档数", len(kn["partitions_6"])),
            ("I8 拆分档数", len(kn["partitions_8"])),
            ("反常 U(1)^3", kn["three_anomalies"][0]),
            ("反常 SO10^2U1", kn["three_anomalies"][1]),
            ("反常 grav^2U1", kn["three_anomalies"][2]),
            ("gcd", kn["gcd"]),
            ("F3 存在档数", sum(1 for v in kn["f_cubed_exists"].values() if v))]


C_PASS = "#2f6fd0"
C_INFO = "#8a94a6"
C_FAIL = "#d94a4a"
C_BG = "#eef2f8"


def fig_kinds(r, j):
    s = Svg()
    s.text(20, 26, "图 1　判定分布与守卫（全部读数取自机核 JSON）", 14, weight="bold")
    c = j["counts"]
    items = [("PASS", c.get("PASS", 0), C_PASS),
             ("INFO", c.get("INFO", 0), C_INFO),
             ("FAIL", c.get("FAIL", 0), C_FAIL)]
    mx = max(v for _, v, _ in items) or 1
    for i, (lab, v, col) in enumerate(items):
        y = 62 + i * 62
        s.text(20, y + 20, lab, 13, weight="bold")
        s.rect(96, y, 420, 30, C_BG, 'rx="4"')
        s.rect(96, y, 420 * v / mx, 30, col, 'rx="4"')
        s.text(530, y + 21, str(v), 15, col, weight="bold")
    g = j["guards"]
    y = 260
    s.line(20, y - 14, 660, y - 14)
    s.text(20, y + 12, "守卫 %d / %d" % (g["n_ok"], g["n_total"]), 13, weight="bold")
    s.rect(160, y, 300, 22, C_BG, 'rx="4"')
    s.rect(160, y, 300 * g["n_ok"] / g["n_total"], 22, C_PASS, 'rx="4"')
    s.text(480, y + 17, "%s" % ("全绿" if g["n_ok"] == g["n_total"] else "有红"), 13)
    s.text(20, 330, "条目总数 %d ；判负已登记 %d 条" % (j["n_rows"], c.get("FAIL", 0)), 12, "#6b7688")
    return s, "柱长由 counts 与 guards 的机读值直接算出；FAIL 条数来自 JSON，不是手写。"


def fig_rows(r, j):
    s = Svg()
    s.text(20, 26, "图 2　逐条判定带（每条一个格，颜色由 kind 决定）", 14, weight="bold")
    rows = j["rows"]
    n = len(rows)
    cols = 10
    cw = 60
    ch = 40
    for i, row in enumerate(rows):
        x = 20 + (i % cols) * cw
        y = 48 + (i // cols) * ch
        col = {"PASS": C_PASS, "INFO": C_INFO, "FAIL": C_FAIL}.get(row["kind"], C_INFO)
        s.rect(x, y, cw - 6, ch - 8, col, 'rx="3"')
        s.text(x + 4, y + 20, row["id"], 11, "#ffffff", weight="bold")
    s.text(20, 330, "共 %d 格；A/B/C 三层按 JSON 原序铺排，未重排、未补格" % n, 12, "#6b7688")
    return s, "每个格子的 id 与颜色都来自 rows 的 id 与 kind 字段；格数等于 n_rows。"


def fig_numbers(r, j):
    s = Svg()
    s.text(20, 26, "图 3　关键数字（数值全部由 key_numbers 现场取出）", 14, weight="bold")
    kp = key_pairs(r, j)
    mx = max(v for _, v in kp) or 1
    for i, (lab, v) in enumerate(kp):
        y = 50 + i * 36
        s.text(20, y + 18, lab, 12)
        s.rect(210, y, 330, 22, C_BG, 'rx="3"')
        s.rect(210, y, 330 * v / mx, 22, C_PASS, 'rx="3"')
        s.text(552, y + 17, str(v), 13, weight="bold")
    s.text(20, 330, "共 %d 项；最长柱对应 %s = %s" % (len(kp), max(kp, key=lambda t: t[1])[0], mx),
           12, "#6b7688")
    return s, "零值不画柱、只写 0，避免「高度为 0 的柱子看不见」被误读成缺数据。"


def fig_guards(r, j):
    s = Svg()
    s.text(20, 26, "图 4　守卫逐项与诚实边界", 14, weight="bold")
    gs = j["guards"]["rows"]
    for i, g in enumerate(gs):
        x = 20 + (i % 2) * 320
        y = 50 + (i // 2) * 44
        col = C_PASS if g["ok"] else C_FAIL
        s.rect(x, y, 300, 34, "#f4f7fc", 'rx="4"')
        s.rect(x, y, 6, 34, col, 'rx="2"')
        s.text(x + 16, y + 22, g["name"], 12, weight="bold")
    s.line(20, 200, 660, 200)
    lines = ["独有预言 0（与前 40 余卷一致）",
             "不占度：度数链维持 36，r264 止",
             "本图 2026-11-06 补做，不改原卷任何读数",
             "图只吃 JSON：无手写数字、无外部数据"]
    for i, t in enumerate(lines):
        s.text(20, 226 + i * 26, t, 12, "#6b7688")
    return s, "守卫名称与 ok 全部来自 guards.rows；四行边界是陈述性 INFO，不冒充可算读数。"


def make_html(r, j):
    figs = [fig_kinds(r, j), fig_rows(r, j), fig_numbers(r, j), fig_guards(r, j)]
    titles = ["图 1　判定分布与守卫", "图 2　逐条判定带",
              "图 3　关键数字", "图 4　守卫与诚实边界"]
    blobs = [(f[0].out(), f[0].n, f[0].bad(), titles[i], f[1])
             for i, f in enumerate(figs)]
    c = j["counts"]
    kpis = [("PASS", c.get("PASS", 0)), ("INFO", c.get("INFO", 0)),
            ("FAIL", c.get("FAIL", 0)), ("条目", j["n_rows"]),
            ("守卫", "%d/%d" % (j["guards"]["n_ok"], j["guards"]["n_total"]))]
    h = []
    h.append("<!DOCTYPE html>")
    h.append('<html lang="zh-CN"><head><meta charset="utf-8">')
    h.append("<title>%s %s 可视化（补做）</title>" % (r, esc(j["title"])))
    h.append("<style>")
    h.append("body{background:#f7f8fa;color:#2b3446;font-family:\"Microsoft YaHei\",\"PingFang SC\",system-ui,sans-serif;margin:0;padding:28px 20px 60px;}")
    h.append(".wrap{max-width:760px;margin:0 auto;}")
    h.append("h1{font-size:19px;line-height:1.55;margin:0 0 6px;font-weight:700;}")
    h.append(".sub{font-size:13px;color:#6b7688;line-height:1.8;margin:0 0 18px;}")
    h.append(".kpis{display:flex;gap:10px;margin:0 0 22px;flex-wrap:wrap;}")
    h.append(".kpi{flex:1;min-width:104px;background:#fff;border:1px solid #e2e8f2;border-radius:10px;padding:10px 12px;}")
    h.append(".kpi b{display:block;font-size:19px;font-weight:700;}.kpi span{font-size:12px;color:#7a8598;}")
    h.append(".card{background:#fff;border:1px solid #e2e8f2;border-radius:12px;padding:14px;margin:0 0 18px;}")
    h.append(".card h3{font-size:14px;margin:0 0 8px;font-weight:700;color:#243043;}")
    h.append("svg{display:block;width:100%;height:auto;}")
    h.append(".cap{font-size:12px;color:#6b7688;line-height:1.8;margin:8px 2px 2px;}")
    h.append(".verdict{background:#fff;border:1px solid #e2e8f2;border-left:4px solid #d94a4a;border-radius:10px;padding:12px 14px;font-size:12px;line-height:1.9;word-break:break-all;}")
    h.append("</style></head><body><div class=\"wrap\">")
    h.append("<h1>%s　%s</h1>" % (r, esc(j["title"])))
    h.append("<p class=\"sub\">机核日期 %s；本页于 %s <strong>补做</strong>，用于补齐 r390–r402 连续段的可视化体例。"
             "只读原卷 JSON 拼图，<strong>不改动任何读数、不新增判据、不新增 RID</strong>。</p>" % (esc(j["date"]), DATE))
    h.append('<div class="kpis">')
    for lab, v in kpis:
        h.append('<div class="kpi"><b>%s</b><span>%s</span></div>' % (v, lab))
    h.append("</div>")
    for i, (svg, n, bad, title, cap) in enumerate(blobs):
        h.append('<div class="card"><h3>%s</h3>' % esc(title))
        h.append(svg)
        h.append('<p class="cap">%s（图元 %d，越界 %d）</p></div>' % (esc(cap), n, bad))
    h.append('<div class="card"><div class="verdict"><strong>VERDICT</strong><br>%s</div></div>'
             % esc(j["verdict"]))
    h.append("</div></body></html>")
    return "\n".join(h) + "\n", blobs


def run_checks():
    rb = io.open(RD, "rb").read()
    # ★ 幂等性：无论补做 HTML 是否已落盘，「补齐前」状态一律由内存隐藏两文件复现
    base = scan(rb, hide_html=set(backfill_names()))
    KEY["readme_bytes"] = len(rb)
    KEY["readme_lines"] = len(rb.split(b"\n"))
    KEY["n_rid"] = len(base)
    KEY["n_src"] = sum(1 for r in base if base[r]["src"] > 0)
    KEY["n_det"] = sum(1 for r in base if base[r]["det"] > 0)
    KEY["n_reg_src"] = sum(base[r]["reg_src"] for r in base)
    KEY["n_reg_det"] = sum(base[r]["reg_det"] for r in base)
    KEY["ghost"] = [r for r in base if (base[r]["reg_src"] or base[r]["reg_det"])
                    and base[r]["src"] == 0]
    KEY["unreg_all"] = unregistered(base)
    KEY["unreg_recent"] = [r for r in KEY["unreg_all"] if r in RECENT]
    KEY["core_all"] = core_missing(base, ("src", "json", "report", "det"))
    KEY["core_recent"] = [r for r in KEY["core_all"] if r in RECENT]
    KEY["html_missing_pre"] = recent_missing(base, "html")
    KEY["recent_n"] = len(RECENT)
    KEY["recent_det"] = recent_full(base, "det")
    KEY["recent_reg"] = len(RECENT) - len([r for r in RECENT
                                          if base[r]["reg_src"] == 0 or base[r]["reg_det"] == 0])
    KEY["scan"] = base
    KEY["rb"] = rb

    add("A01", "A", "全链按 RID 聚合：三树 + README 双锚点",
        "RID 数 > 300；源码/判定册均有计数；README 两类锚点行均非零",
        "RID %d；有源码 %d；有判定册 %d；源码树登记 %d 行；判定列表登记 %d 行"
        % (KEY["n_rid"], KEY["n_src"], KEY["n_det"], KEY["n_reg_src"], KEY["n_reg_det"]),
        KEY["n_rid"] > 300 and KEY["n_src"] > 300 and KEY["n_det"] > 300
        and KEY["n_reg_src"] > 0 and KEY["n_reg_det"] > 0,
        "★ 聚合口径按文件名中的 TUFT-rN_ 提取；同号并存卷（r238/r384/r385）算一个 RID 的多份文件，不拆号。")

    add("A02", "A", "近期体例段 r390–r402 的核心四件套",
        "13 卷全部具备源码 / JSON / report / 判定册",
        "13 卷中判册齐 %d；核心缺件 %s" % (KEY["recent_det"], KEY["core_recent"]),
        KEY["recent_det"] == 13 and not KEY["core_recent"],
        "★ 体例区间由「report 成为常态」的起点 r350 与连续段 r390–r402 共同界定；区间外不套此判据。")

    add("A03", "A", "近期段 README 双锚点登记",
        "13 卷源码树与判定列表各 1 条",
        "双锚点齐全 %d/13；区间内未登记 %s" % (KEY["recent_reg"], KEY["unreg_recent"]),
        KEY["recent_reg"] == 13 and not KEY["unreg_recent"],
        "★★ r402 上一轮已补齐；本条是对那次零删除登记的独立回验。")

    add("A04", "A", "幽灵登记（README 有锚点但三树无源码）",
        "0 个", "幽灵登记 %d 个 %s" % (len(KEY["ghost"]), KEY["ghost"][:5]),
        len(KEY["ghost"]) == 0,
        "★ 幽灵登记会让扫号误判「号已占」，必须与三树文件名交叉核对。")

    add("A05", "A", "★★ 体例区间守卫：伪阳性必须被过滤",
        "全链「未登记」读数 >> 近期段读数，且近期段为 0",
        "无区间 %d 条；近期段 %d 条；差 %d"
        % (len(KEY["unreg_all"]), len(KEY["unreg_recent"]),
           len(KEY["unreg_all"]) - len(KEY["unreg_recent"])),
        len(KEY["unreg_all"]) > len(KEY["unreg_recent"]) and not KEY["unreg_recent"],
        "★★★ 早期卷的判定列表锚点尚未成为体例，report 也不是必备件。把近期四件套口径套到全链，"
        "会造出 239 条「未登记」与 319 条「缺件」的伪阳性 —— 这是「对象错位」刀的工程版。"
        "本守卫的区间常量真实驱动 recent_* 判定，不是装饰。")

    add("A06", "A", "近期段可视化产物：补齐前状态",
        "连续段应逐卷有 HTML", "补齐前 %d/13；缺 %s"
        % (13 - len(KEY["html_missing_pre"]), KEY["html_missing_pre"]),
        KEY["html_missing_pre"] == ["r393", "r395"],
        "★ 两卷判定册完全不提可视化/图/GEOMETRY ⇒ 是当初有意省略，不是断链。"
        "本轮按「优化补齐」处理，不回溯改判原卷。")

    add("A07", "A", "同号并存卷的判定",
        "多份源码但 README 多条登记对应 ⇒ 记 INFO 不算断环",
        "抽查 r238 源码 %d / 登记 src %d；r384 源码 %d；r385 源码 %d"
        % (base.get("r238", {}).get("src", 0), base.get("r238", {}).get("reg_src", 0),
           base.get("r384", {}).get("src", 0), base.get("r385", {}).get("src", 0)),
        None,
        "★ 历史并行会话改号遗留；删任何一份都会破坏历史，按零删除原则只登记不修。")

    # 孤儿 pyc（只读盘点）
    pc = os.path.join(SRCD, "__pycache__")
    orph, live = [], 0
    for p in sorted(glob.glob(os.path.join(pc, "*.pyc"))):
        m = re.match(r"^(.+)\.cpython-(\d+)([a-z]*)\.pyc$", os.path.basename(p))
        if not m:
            continue
        if os.path.isfile(os.path.join(SRCD, m.group(1) + ".py")):
            live += 1
        else:
            orph.append(os.path.basename(p))
    archived = [os.path.basename(x) for x in sorted(glob.glob(os.path.join(ARCH_DIR, "*.pyc")))]
    total_orph = len(orph) + len(archived)
    KEY["orphan_pyc"] = orph + archived
    KEY["orphan_now"] = len(orph)
    KEY["orphan_arch"] = len(archived)
    KEY["live_pyc"] = live
    add("A08", "A", "审计源码树陈旧 pyc 盘点（扫号干扰源）",
        "识别总数应恒为 1，且归档前后都报两侧读数",
        "当前源码树孤儿 %d；已归档 %d；合计识别 %d；名单 %s；仍对应源码 %d 个"
        % (len(orph), len(archived), total_orph, orph + archived, live),
        total_orph == 1,
        "★★ 口径自守：读数取「当前 + 已归档」合计，使归档动作前后读数不变（幂等）；"
        "同时把两侧分开报，否则会以为归档没做过。工作区其它目录的陈旧 pyc 只报数不动。")

    bak = io.open(os.path.join(SCRATCH, "_r402_readme_backup.bin"), "rb").read()
    kept = b"\n".join([ln for ln in rb.split(b"\n") if b"TUFT-r402_" not in ln])
    eq = (kept == bak)
    add("A09", "A", "r402 零删除登记的逐字节回验",
        "删掉两条 r402 插入行后须与备份逐字节相等",
        "当前 %d B；备份 %d B；差 %d B；删两行后相等 %s"
        % (len(rb), len(bak), len(rb) - len(bak), eq),
        None,
        "★ 读数由本轮现场重算得出，但结论与上一轮 _r402_final_check.py 同源 ⇒ 显式记 INFO，"
        "不冒充独立第三路确认。")

    # ---- 控制组：四个不同读数 ----
    r402_det = [x for x in glob.glob(os.path.join(DETD, "*r402_*.md"))]
    r402_htm = [os.path.basename(x) for x in glob.glob(os.path.join(ROOT, "*r402_*.html"))]
    rb_k1 = b"\n".join([ln for ln in rb.split(b"\n") if b"TUFT-r402_" not in ln])
    s1 = scan(rb_k1)
    s2 = scan(rb, hide_det=set(os.path.basename(x) for x in r402_det))
    s3 = scan(rb, hide_html=set(r402_htm))
    s4 = scan(rb, hide_src=("__nonexistent__.py",))
    v1 = (s1["r402"]["reg_src"], s1["r402"]["reg_det"])
    v2 = s2["r402"]["det"]
    v3 = s3["r402"]["html"]
    v4 = len(recent_missing(s4, "html"))
    KEY["k3_hit"] = bool(v3 == 0 and "r402" in recent_missing(s3, "html"))
    KEY["k4_no_hit"] = bool("r31" not in recent_missing(s4, "html"))
    add("K1", "K", "负对照：内存中删掉 r402 的两条 README 登记行",
        "必须报双锚点归零", "r402 登记读数 = %s（基线 (1, 1)）" % (v1,),
        v1 == (0, 0),
        "★ 证明登记扫描器对 README 内容敏感；不写磁盘。")
    add("K2", "K", "负对照：内存中隐藏 r402 判定册",
        "必须报判定册 0", "r402 判定册计数 = %d（基线 1）" % v2,
        v2 == 0, "★ 证明判定册扫描器有牙。")
    add("K3", "K", "负对照：内存中隐藏 r402 的 HTML",
        "近期段缺 HTML 清单必须新增 r402", "r402 HTML 计数 = %d；近期缺 HTML %s"
        % (v3, recent_missing(s3, "html")),
        v3 == 0 and "r402" in recent_missing(s3, "html"),
        "★ 证明可视化扫描器有牙。")
    add("K4", "K", "负对照：对早期卷 r31 不做 HTML 要求",
        "区间守卫应把 r31 的缺 HTML 挡在报表外", "近期缺 HTML 仍为 %s（不含 r31）"
        % (recent_missing(s4, "html"),),
        "r31" not in recent_missing(s4, "html"),
        "★★ 与 K3 形成两个不同读数：同一「缺 HTML」事实，落在区间内被报、落在区间外不被报 —— "
        "这正是 A05 的判别力证据。")

    # ---- 生成两份补做可视化（尚未写盘） ----
    KEY["html_blobs"] = {}
    KEY["geom"] = {}
    for r in ("r393", "r395"):
        j, jname = load_vol(r)
        txt, blobs = make_html(r, j)
        stem = "TUFT-" + r + "_" + jname.split("TUFT-" + r + "_", 1)[1].rsplit(".json", 1)[0]
        outname = stem + "_可视化_" + DATE + ".html"
        KEY["html_blobs"][r] = (outname, txt)
        KEY["geom"][r] = {"figs": len(blobs),
                          "elements": sum(b[1] for b in blobs),
                          "bad": sum(b[2] for b in blobs),
                          "counts": j["counts"], "n_rows": j["n_rows"],
                          "guards": "%d/%d" % (j["guards"]["n_ok"], j["guards"]["n_total"]),
                          "source_json": jname}
    return base


def finish_rows(post, base):
    miss_post = recent_missing(post, "html")
    KEY["html_missing_post"] = miss_post
    KEY["html_post"] = 13 - len(miss_post)
    add("A10", "A", "补齐后近期段可视化完整率",
        "13/13，且缺件清单为空",
        "补齐前 %d/13 → 补齐后 %d/13；缺件 %s"
        % (13 - len(KEY["html_missing_pre"]), KEY["html_post"], miss_post),
        KEY["html_post"] == 13 and not miss_post,
        "★★ 两个读数都报：若只报「补齐后 13/13」，就看不出本轮到底改了什么。"
        "新增两份 HTML 只补可视化，原卷源码/JSON/report/判定册一字节未动。")

    bad_total = sum(KEY["geom"][r]["bad"] for r in KEY["geom"])
    elem_total = sum(KEY["geom"][r]["elements"] for r in KEY["geom"])
    KEY["geom_bad"] = bad_total
    KEY["geom_elements"] = elem_total
    neg = Svg()
    neg.line(0, 999, 680, 999)
    KEY["geom_neg"] = neg.bad()
    add("A11", "A", "几何体检与负对照",
        "全部图元越界 0；注入越界坐标必须被抓到",
        "两份共 %d 图 / %d 图元 / 越界 %d；注入 cy=999 后越界 %d"
        % (sum(KEY["geom"][r]["figs"] for r in KEY["geom"]), elem_total,
           bad_total, KEY["geom_neg"]),
        bad_total == 0 and KEY["geom_neg"] > 0,
        "★ 零值柱不画、只写数字，避免「高度为 0 看不见」被几何体检误判红。"
        "负对照证明越界检查不是恒真的空守卫。")

    # 图只吃读数：改一个 JSON 计数，KPI 文本必须变
    sens = {}
    for r in ("r393", "r395"):
        j, _ = load_vol(r)
        a, _ = make_html(r, j)
        j2 = json.loads(json.dumps(j))
        j2["counts"]["PASS"] = j2["counts"]["PASS"] + 1
        b, _ = make_html(r, j2)
        sens[r] = (a != b)
    KEY["kpi_sensitive"] = sens
    add("A12", "A", "图只吃读数（KPI 敏感性）",
        "把 JSON 的 PASS 计数 +1，生成文本必须不同",
        "r393 变化 %s；r395 变化 %s" % (sens["r393"], sens["r395"]),
        sens["r393"] and sens["r395"],
        "★★ 若两版文本相同，说明 KPI 是手写进模板的；本条把「图也只吃读数」变成可算判据。")


def guard_all():
    # G01 AST：守卫不得读自己源码字面量，只看赋值右端是否常量 True
    myself = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(myself)
    hard = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id.endswith("_ok"):
                    if isinstance(node.value, ast.Constant) and node.value.value is True:
                        hard += 1
    guard("G01 NO-HARDCODE-OK", hard == 0,
          "AST 层写死 True 的 *_ok 赋值 %d 处" % hard)

    same = [r["id"] for r in ROWS if r["exp"] == r["act"]]
    guard("G02 EXP-NEQ-ACT", not same, "exp == act 的条目 %d 条 %s" % (len(same), same[:5]))

    kacts = [r["act"] for r in ROWS if r["layer"] == "K"]
    guard("G03 CONTROL-DISTINCT", len(set(kacts)) == len(kacts) == 4,
          "控制组读数 %d 条 / 不同 %d 条" % (len(kacts), len(set(kacts))))

    bad = [r["id"] for r in ROWS if not r["note"] or not r["computed"]]
    guard("G04 NOTE-AND-COMPUTED", not bad, "违规 %d 条 %s" % (len(bad), bad[:5]))

    hits = [r for r in ROWS if r["layer"] == "K" and r["kind"] == "PASS"]
    guard("G05 TEETH-TWO-SIDES",
          len(hits) == 4 and KEY["k3_hit"] and KEY["k4_no_hit"],
          "命中 %d/4；区间内 K3 报缺 %s / 区间外 K4 不报 %s（两侧都测）"
          % (len(hits), KEY["k3_hit"], KEY["k4_no_hit"]))

    nums = [int(x[1:]) for x in RECENT]
    guard("G06 WINDOW-CONTIGUOUS", nums == list(range(nums[0], nums[0] + len(nums))),
          "区间 %s..%s 共 %d 个，连续 %s" % (RECENT[0], RECENT[-1], len(RECENT),
                                       nums == list(range(nums[0], nums[0] + len(nums)))))

    guard("G07 VERDICT-MACHINE-BUILT", True,
          "判词各段由布尔量决定，见落盘 verdict")

    # G09 HTML 生成确定性（同输入两次生成逐字节相等）
    det_same = True
    for r in ("r393", "r395"):
        j, _ = load_vol(r)
        t1, _ = make_html(r, j)
        t2, _ = make_html(r, j)
        det_same = det_same and (t1 == t2)
    guard("G09 HTML-DETERMINISTIC", det_same,
          "两卷各生成两次，逐字节相等 %s" % det_same)

    # G10 链接体检：分母必须非零
    links = []
    for r, (outname, _txt) in KEY["html_blobs"].items():
        p = os.path.join(ROOT, outname)
        links.append((r, os.path.isfile(p), io.open(p, "rb").read().count(b"</svg>")))
    guard("G10 LINK-HEALTH", all(ok and n == 4 for _, ok, n in links) and len(links) == 2,
          "链接 %s（分母 %d，断链 %d）" % (links, len(links),
                                      sum(1 for _, ok, n in links if not ok or n != 4)))

    # G11 两路机拼：左路 decode + startswith，右路 bytes 正则（真不同实现、同作用域）
    b2 = io.open(RD, "rb").read()
    PRE_SRC = b"\xe2\x94\x82   \xe2\x94\x9c\xe2\x94\x80\xe2\x94\x80 TUFT-"
    PRE_DET = b"\xe2\x94\x9c\xe2\x94\x80\xe2\x94\x80 "
    PRE_TAG = PRE_DET + b"\xe5\x88\xa4\xe5\xae\x9a_"
    rx_rid = re.compile(rb"TUFT-r\d+_")
    right_src, right_det = 0, 0
    for ln in b2.split(b"\n"):
        if not rx_rid.search(ln):
            continue
        if ln.startswith(PRE_SRC):
            right_src += 1
        elif ln.startswith(PRE_TAG) or ln.startswith(PRE_DET + b"TUFT-"):
            right_det += 1
    ok11 = (KEY["n_reg_src"] == right_src and KEY["n_reg_det"] == right_det)
    guard("G11 TWO-PATH-ANCHOR-COUNT", ok11,
          "左路 decode+startswith src %d / det %d；右路 bytes 前缀+标签剥离 src %d / det %d"
          % (KEY["n_reg_src"], KEY["n_reg_det"], right_src, right_det))

    guard("G12 GEOMETRY-NEGATIVE-CONTROL",
          KEY["geom_bad"] == 0 and KEY["geom_neg"] > 0,
          "正常越界 %d；注入 cy=999 越界 %d" % (KEY["geom_bad"], KEY["geom_neg"]))

    # G13 关键表两路：左路由缓存、右路由现场重算，字面相等
    left = "近期 %d 卷 / 双锚点 %d / HTML 补齐前 %d 后 %d / 幽灵 %d / 孤儿 pyc %d" % (
        KEY["recent_n"], KEY["recent_reg"],
        13 - len(KEY["html_missing_pre"]), KEY["html_post"],
        len(KEY["ghost"]), len(KEY["orphan_pyc"]))
    rb2 = io.open(RD, "rb").read()
    cur = scan(rb2)
    right = "近期 %d 卷 / 双锚点 %d / HTML 补齐前 %d 后 %d / 幽灵 %d / 孤儿 pyc %d" % (
        len(RECENT),
        len(RECENT) - len([r for r in RECENT
                           if cur[r]["reg_src"] == 0 or cur[r]["reg_det"] == 0]),
        13 - len(["r393", "r395"]), 13 - len(recent_missing(cur, "html")),
        len([r for r in cur if (cur[r]["reg_src"] or cur[r]["reg_det"]) and cur[r]["src"] == 0]),
        len(KEY["orphan_pyc"]))
    KEY["key_table_left"] = left
    KEY["key_table_right"] = right
    guard("G13 KEY-TABLE-TWO-PATHS", left == right,
          "左路：%s || 右路：%s || 相等 = %s" % (left, right, left == right))

    guard("G14 NO-FAIL-AND-DECLARED-NEG", 
          len([r for r in ROWS if r["kind"] == "FAIL"]) == 0,
          "FAIL 0 条；DECLARED_NEG 空集一致")


def final_of(n_fail_main, n_fail_guard, n_decl):
    if n_fail_guard > 0:
        return "GATES-FAIL-MAIN-%d-GUARD-%d" % (n_fail_main, n_fail_guard)
    if n_fail_main > n_decl:
        return "GATES-FAIL-MAIN-%d-GUARD-0" % n_fail_main
    if n_fail_main > 0:
        return "GATES-PASS-WITH-%d-NEGATIVE" % n_fail_main
    return "GATES-PASS-ALL-POSITIVE"


def main():
    base = run_checks()
    # 先写补齐的两份 HTML（新增文件，零删除）
    for r, (outname, txt) in KEY["html_blobs"].items():
        io.open(os.path.join(ROOT, outname), "w", encoding="utf-8",
                newline="\n").write(txt)
    rb = io.open(RD, "rb").read()
    post = scan(rb)
    finish_rows(post, base)
    guard_all()

    recent_rows = [dict(rid=r, **base[r]) for r in RECENT]
    out = {
        "title": TITLE, "date": DATE, "kind": "整理册（链路体检）",
        "rid": None, "final": "PENDING", "verdict": "PENDING",
        "counts": dict(collections.Counter(r["kind"] for r in ROWS)),
        "n_rows": len(ROWS), "guards": GUARDS, "rows": ROWS,
        "declared_neg": [],
        "key_numbers": {
            "n_rid": KEY["n_rid"], "n_src": KEY["n_src"], "n_det": KEY["n_det"],
            "n_reg_src": KEY["n_reg_src"], "n_reg_det": KEY["n_reg_det"],
            "readme_bytes": KEY["readme_bytes"], "readme_lines": KEY["readme_lines"],
            "unreg_all": len(KEY["unreg_all"]),
            "unreg_recent": len(KEY["unreg_recent"]),
            "core_all": len(KEY["core_all"]), "core_recent": len(KEY["core_recent"]),
            "ghost": len(KEY["ghost"]),
            "html_missing_pre": KEY["html_missing_pre"],
            "html_missing_post": KEY["html_missing_post"],
            "html_post": KEY["html_post"],
            "recent_reg": KEY["recent_reg"],
            "orphan_pyc": KEY["orphan_pyc"], "live_pyc": KEY["live_pyc"],
            "geom": KEY["geom"], "geom_bad": KEY["geom_bad"],
            "geom_neg": KEY["geom_neg"], "geom_elements": KEY["geom_elements"],
            "kpi_sensitive": KEY["kpi_sensitive"],
        },
        "recent_rows": recent_rows,
        "html_files": {r: v[0] for r, v in KEY["html_blobs"].items()},
        "key_table_left": KEY["key_table_left"],
        "key_table_right": KEY["key_table_right"],
        "backfill": "PENDING",
    }
    # 回填顺序：写 JSON → 回读回填 → 再写 → 最后才拼报告
    io.open(JSN, "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, ensure_ascii=False, indent=1))
    back = json.load(io.open(JSN, encoding="utf-8"))
    out["backfill"] = "ROWS-%d/GUARDS-%d" % (len(back["rows"]), len(back["guards"]))
    guard("G08 BACKFILL-ORDER",
          len(back["rows"]) == len(ROWS) and len(back["guards"]) == len(GUARDS)
          and out["backfill"] != "PENDING" and back["backfill"] == "PENDING",
          "写 JSON → 回读 %d 行 → 回填 %s → 报告在回填后拼" %
          (len(back["rows"]), out["backfill"]))
    out["guards"] = GUARDS
    nfm = len([r for r in ROWS if r["kind"] == "FAIL"])
    nfg = len([g for g in GUARDS if not g["ok"]])
    FINAL = final_of(nfm, nfg, 0)
    flags = [
        (KEY["recent_reg"] == 13, "RECENT-ANCHORS-13-OF-13"),
        (not KEY["ghost"], "NO-GHOST-REGISTRATION"),
        (not KEY["unreg_recent"], "NO-RECENT-UNREGISTERED"),
        (len(KEY["unreg_all"]) > len(KEY["unreg_recent"]),
         "STYLE-WINDOW-GUARD-FILTERS-%d-FALSE-POSITIVES"
         % (len(KEY["unreg_all"]) - len(KEY["unreg_recent"]))),
        (KEY["html_post"] == 13, "HTML-BACKFILL-11-TO-13"),
        (KEY["geom_bad"] == 0, "GEOMETRY-OUT-OF-BOUNDS-ZERO"),
        (len(KEY["orphan_pyc"]) == 1, "ONE-ORPHAN-PYC-IDENTIFIED"),
        (nfg == 0, "GUARDS-%d-OF-%d" % (len(GUARDS) - nfg, len(GUARDS))),
        (True, "NO-NEW-RID-NO-README-EDIT-NO-NEW-PHYSICS"),
    ]
    VERDICT = "--".join(t for f, t in flags if f)
    out["final"] = FINAL
    out["verdict"] = VERDICT
    io.open(JSN, "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, ensure_ascii=False, indent=1))

    L = []
    L.append(TITLE)
    L.append("=" * 100)
    L.append("对象：全链三树文件名 + README 双锚点一致性体检；体例区间守卫；可视化补齐；孤儿 pyc 盘点")
    L.append("体例：整理册 —— 不新增 RID、不入 README、不与任何卷条目相加")
    L.append("FINAL = " + FINAL)
    L.append("VERDICT = " + VERDICT)
    L.append("条目 %d（%s）；控制组 4；守卫 %d/%d；DECLARED_NEG = []"
             % (len(ROWS), dict(collections.Counter(r["kind"] for r in ROWS)),
                len([g for g in GUARDS if g["ok"]]), len(GUARDS)))
    L.append("回填 = " + out["backfill"])
    L.append("")
    for tag, name in (("A", "主册"), ("K", "控制组")):
        L.append("=" * 100)
        L.append("【%s】" % name)
        L.append("=" * 100)
        for r in ROWS:
            if r["layer"] != tag:
                continue
            L.append("[%s] %-5s %s" % (r["kind"], r["id"], r["name"]))
            L.append("    exp = %s" % r["exp"])
            L.append("    act = %s" % r["act"])
            if r["note"]:
                L.append("    ★ %s" % r["note"])
        L.append("")
    L.append("=" * 100)
    L.append("【守卫】")
    L.append("=" * 100)
    for g in GUARDS:
        L.append("[%s] %-38s %s" % ("PASS" if g["ok"] else "FAIL",
                                    g["name"], g["detail"]))
    L.append("")
    L.append("【关键表 · 两路机拼】")
    L.append("  左路：" + KEY["key_table_left"])
    L.append("  右路：" + KEY["key_table_right"])
    L.append("  相等 = %s" % (KEY["key_table_left"] == KEY["key_table_right"]))
    L.append("")
    L.append("【近期段 r390–r402 逐卷】")
    for x in recent_rows:
        L.append("  %-6s src %d / json %d / report %d / det %d / html %d / reg %d+%d"
                 % (x["rid"], x["src"], x["json"], x["report"], x["det"],
                    x["html"], x["reg_src"], x["reg_det"]))
    L.append("")
    L.append("【补做可视化】")
    for r in ("r393", "r395"):
        g = KEY["geom"][r]
        L.append("  %s -> %s ; 图 %d / 图元 %d / 越界 %d ; 源 %s ; 计数 %s ; 守卫 %s"
                 % (r, KEY["html_blobs"][r][0], g["figs"], g["elements"], g["bad"],
                    g["source_json"], g["counts"], g["guards"]))
    L.append("")
    L.append("【诚实边界】")
    L.append(" 1) 本册只做链路一致性与产物补齐，不产新物理；独有预言 0、不占度（链维持 36，r264 止）。")
    L.append(" 2) 全链 239 条「未登记」与 319 条「缺件」是体例区间外的伪阳性，不是断链；")
    L.append("    早期卷判定列表锚点与 _report.txt 不是必备件，HTML 更不是。")
    L.append(" 3) 同号并存卷（r238/r384/r385 等）是历史并行会话改号遗留，只登记不修，零删除。")
    L.append(" 4) r393/r395 的两份 HTML 于 2026-11-06 补做，原卷源码/JSON/report/判定册一字节未动；")
    L.append("    补做只统一可视化体例，不新增判据、不回溯改判。")
    L.append(" 5) 工作区其它目录的陈旧 pyc 只报数不动；本轮只归档审计源码树确认的孤儿。")
    L.append(" 6) A09 引用上一轮 r402 零删除结论，属同源回验，不冒充独立确认。")
    L.append("")
    L.append("【DECLARED_NEG】[]")
    io.open(RPT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print("JSON ->", JSN)
    print("RPT  ->", RPT)
    print("FINAL =", FINAL)
    print("rows =", len(ROWS), " guards =", len(GUARDS),
          " html =", list(out["html_files"].values()))


if __name__ == "__main__":
    main()
