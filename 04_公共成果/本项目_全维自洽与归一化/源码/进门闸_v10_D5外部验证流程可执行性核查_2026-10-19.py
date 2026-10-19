# -*- coding: utf-8 -*-
"""进门闸 v10 · D5「外部验证流程」可执行性核查（治理词表／生成视图／闸门本底 三道锁）。

达成度册把 D5 排在第一位（「工程量最小、当前为 0、不依赖新物理」）。它的流程文本第 2 步要求
把 system.json.status 由 unreviewed 改为 reviewed。本册不猜这一步能不能做：
把 module_catalog.discover() 打在**仓外**一份最小良定模块上跑单一变量差异实验，
再用同一把尺量真仓，并把「改了 status 会连带什么」逐项定价。

纪律：除三张闸门承载文件与本册三件产物外零写入；所有数字现场从盘上读；
不动任何 system.json、不动 module_types.json、不跑 refresh_catalog.py、不跑 module_catalog.py refresh。
"""
import collections
import csv
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = _here
while ROOT and not os.path.isdir(os.path.join(ROOT, "openuft")):
    _up = os.path.dirname(ROOT)
    if _up == ROOT:
        break
    ROOT = _up
if not os.path.isdir(os.path.join(ROOT, "openuft")):
    raise SystemExit("FATAL: 找不到 openuft 的仓根（本册须放在 源码/ 或 scratch/）")
LIB = os.path.join(ROOT, "openuft")
GOV = os.path.join(LIB, "00_项目治理")
SYSROOT = os.path.join(LIB, "01_独立体系")
PROJP = os.path.join(LIB, "04_公共成果", "本项目_全维自洽与归一化")
SRC = os.path.join(PROJP, "源码")
DATA = os.path.join(PROJP, "数据")
SCRATCH = os.path.join(ROOT, "scratch")

TAX = os.path.join(GOV, "module_types.json")
LAYOUT = os.path.join(GOV, "layout.json")
MCAT = os.path.join(GOV, u"维护工具", "module_catalog.py")
VERIFY = os.path.join(LIB, "verify.py")
HEALTH = os.path.join(DATA, u"体系第一性健康度总览.json")
FLOW_SRC = os.path.join(SRC, u"本项目_统一场论收口执行_D4D6D5_2026-10-09.py")
TYPEIDX = os.path.join(SYSROOT, "TYPE_INDEX.md")
SYSREADME = os.path.join(SYSROOT, "README.md")
CATALOG = os.path.join(GOV, u"资料索引", "material_catalog.md")
R76_CARRIER = os.path.join(SCRATCH, "verify_r76.txt")
V9_FACE = os.path.join(DATA, u"进门闸_v9_登记行的判别力复算_V侧判决_2026-10-19.json")
ACHIEVE_DOC = os.path.join(PROJP, u"判定_本项目_统一场论达成度重算与最小闭合清单_2026-10-08.md")
D45_DOC = os.path.join(PROJP, u"判定_本项目_统一场论收口执行_D4D6D5_2026-10-09.md")

STEM = u"进门闸_v10_D5外部验证流程可执行性核查_2026-10-19"
INSTR_NAME = STEM + ".py"
FACE_NAME = STEM + ".json"
VOL_NAME = u"判定_" + STEM + ".md"
SELF_PATH = os.path.abspath(__file__)
LAND = "--land" in sys.argv[1:]
OUT_DIR = DATA if LAND else SCRATCH
SUB_CARRIER = os.path.join(SCRATCH, "v10_verify_subrun.txt")

FIXTURE_DIR = "FX_D5_probe"
FIXTURE_ID = "fx_probe_d5"

# 变异体：各断本册一处推理，指定的控制必须红——否则那条控制是橡皮章。
MUT = None
for _a in sys.argv[1:]:
    if _a.startswith("--mutant="):
        MUT = _a.split("=", 1)[1]
        LAND = False
        OUT_DIR = SCRATCH
TYPED_STATUSES = [u"unreviewed", u"reviewed", u"validated", u"archived"]   # m1 用的假词表
EXPECTED_RED = {u"m1": u"X1",    # 词表从打字常量取：reviewed 竟「合法」
                u"m2": u"X2",    # 差异实验两侧同 status：单一变量被抹平
                u"m3": u"X7",    # 资格名册只按 rating 筛：连词的后两半被丢掉
                u"m4": u"X9",    # 伪造判决后语料移动
                u"m5": u"X5"}    # 把 verify.py 的短路当成不存在（行号对调）
MUT_NAMES = {u"m1": u"词表改成打字常量", u"m2": u"差异实验抹平单一变量",
             u"m3": u"资格名册丢掉连词后两半", u"m4": u"输入图像在判决后移动",
             u"m5": u"闸门短路顺序被对调"}


class Fatal(Exception):
    pass


def md5(b):
    return hashlib.md5(b).hexdigest()


def rb(p):
    with open(p, "rb") as fh:
        return fh.read()


def txt(p):
    return rb(p).decode("utf-8", "replace")


def load(tag, path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(tag, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules[tag] = mod
    return mod


def sanitize(s):
    return (s or u"").replace(u"|", u"∣").replace(u"\r", u" ").replace(u"\n", u" ")


CONTROLS = []


def ctl(code, title, fired, payload=None):
    leftover = re.findall(u"%[sdfg]", title or u"")
    if leftover:
        raise Fatal(u"控制 %s 的题面有未插值的占位符 %s：%s" % (code, leftover, title))
    CONTROLS.append({"code": code, "title": title, "fired": bool(fired), "payload": payload or {}})
    print(u"%s %s｜%s" % (u"[RED]" if not fired else u"[ok]", code, title))
    if not fired:
        print(u"      payload: %s" % json.dumps(payload or {}, ensure_ascii=False, default=str)[:700])


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


# ---------------------------------------------------------------------------
# 仓外最小良定模块：discover() 的每条要求都补齐，使 status＝unreviewed 时错误集为空
# ---------------------------------------------------------------------------
def build_fixture(tmp, vocab, status_value):
    tax = json.loads(txt(TAX))
    lay = json.loads(txt(LAYOUT))
    if vocab is not None:
        tax[u"statuses"] = list(vocab)
    gov = Path(tmp) / u"00_项目治理"
    gov.mkdir(parents=True, exist_ok=True)
    (gov / "module_types.json").write_text(json.dumps(tax, ensure_ascii=False, indent=1), encoding="utf-8")
    (gov / "layout.json").write_text(json.dumps(lay, ensure_ascii=False, indent=1), encoding="utf-8")
    base = Path(tmp) / u"01_独立体系" / FIXTURE_DIR
    base.mkdir(parents=True, exist_ok=True)
    kind = sorted(tax[u"types"].keys())[0]
    entry = {u"id": FIXTURE_ID, u"directory": FIXTURE_DIR, u"title": u"D5 差异实验夹具",
             u"kind": kind, u"status": status_value, u"premise_summary": u"夹具前提（只用于本册差异实验）",
             u"premise_status": u"open", u"source_records": [], u"related_systems": [],
             u"code_dependencies": [], u"postulates": []}
    (base / "system.json").write_text(json.dumps(entry, ensure_ascii=False, indent=1), encoding="utf-8")
    for stage in lay[u"stages"]:
        d = base / stage
        d.mkdir(parents=True, exist_ok=True)
        (d / "README.md").write_text(u"# 夹具阶段占位\n", encoding="utf-8")
    (base / "claims.csv").write_text(
        u"claim_id,hypothesis_revision,statement,assumptions,derivation,prediction,prediction_value,"
        u"prediction_urel,run_id,data_id,uncertainty,evidence_level,status,reviewer\n", encoding="utf-8")
    d = base / u"08_研究数据"
    d.mkdir(parents=True, exist_ok=True)
    (d / "data_registry.csv").write_text(u"data_id,path\n", encoding="utf-8")
    d = base / u"07_计算复现" / u"运行记录"
    d.mkdir(parents=True, exist_ok=True)
    (d / "run_template.json").write_text(json.dumps({u"system_id": FIXTURE_ID}, ensure_ascii=False), encoding="utf-8")
    return tax, lay


def main():
    t0 = time.time()
    own_lf = rb(SELF_PATH).replace(b"\r\n", b"\n")
    landed_image = own_lf.replace(b"\n", b"\r\n")
    instr_image = landed_image if LAND else own_lf
    instr_bytes, instr_md5 = len(instr_image), md5(instr_image)

    sys_json_paths = sorted([p for p in Path(SYSROOT).glob(u"*/system.json") if p.parent.name != u"新体系模板"])
    claims_paths = sorted([p for p in Path(SYSROOT).glob(u"*/claims.csv") if p.parent.name != u"新体系模板"])
    # 只读复量名单： kinds 与 paths 由同一份构造出来，卷面枚举不另打字（打字枚举会随输入增删而失真）。
    corpus_groups = [(u"词表", [TAX]), (u"layout", [LAYOUT]), (u"两把治理刀", [MCAT, VERIFY]),
                     (u"健康度台账", [HEALTH]), (u"流程源", [FLOW_SRC]),
                     (u"两份生成视图", [TYPEIDX, SYSREADME]),
                     (u"两份主张承载卷", [ACHIEVE_DOC, D45_DOC]),
                     (u"上轮闸门承载", [R76_CARRIER]), (u"v9 面", [V9_FACE]),
                     (u"资料目录", [CATALOG]), (u"system.json", list(sys_json_paths))]
    corpus_paths = sorted(set([str(p) for _, g in corpus_groups for p in g]))
    corpus_before = dict([(p, md5(rb(p))) for p in corpus_paths])
    if MUT == u"m4" and corpus_paths:
        corpus_before[corpus_paths[0]] = u"0" * 32

    def sweep(tag):
        now = dict([(p, md5(rb(p))) for p in corpus_paths])
        moved = sorted([rel(p) for p in corpus_paths if now.get(p) != corpus_before.get(p)])
        return {"tag": tag, "inputs": len(corpus_paths), "moved": moved}

    catalog = load("module_catalog_v10", MCAT)

    # ---- X1 词表现读（唯一权威＝module_types.json 的 statuses）
    tax_disk = json.loads(txt(TAX))
    statuses = TYPED_STATUSES if MUT == u"m1" else tax_disk[u"statuses"]
    x1_ok = (isinstance(statuses, list) and all(isinstance(x, str) for x in statuses)
             and u"reviewed" not in statuses and u"validated" not in statuses)
    ctl(u"X1", u"词表现读：module_types.json 的 statuses＝%s（%d 个）；流程第 2 步要写的 reviewed／validated 均不在其中（命中 %d）"
        % (u"、".join(statuses), len(statuses), sum(1 for w in (u"reviewed", u"validated") if w in statuses)),
        x1_ok, {"statuses_on_disk": tax_disk[u"statuses"], "typed_used": MUT == u"m1"})

    # ---- X2 单一变量差异实验（仓外夹具；status 之外逐字节相同）
    tmp = tempfile.mkdtemp(prefix="v10_d5_fixture_")
    if str(Path(tmp).resolve()).lower().startswith(str(Path(LIB).resolve()).lower()):
        raise Fatal(u"夹具落进了仓内：%s" % tmp)
    try:
        tax_fx, lay_fx = build_fixture(tmp, None, u"unreviewed")
        ent_ok, e_ok = catalog.discover(Path(tmp))
        build_fixture(tmp, None, u"reviewed")
        ent_bad, e_bad = catalog.discover(Path(tmp))
        sig = lambda errs: [x for x in errs if u"Unknown lifecycle status" in x]
        want = u"Unknown lifecycle status: " + FIXTURE_DIR
        added = list(Counter(e_bad) - Counter(e_ok))
        removed = list(Counter(e_ok) - Counter(e_bad))
        if MUT == u"m2":
            build_fixture(tmp, None, u"unreviewed")
            ent_bad, e_bad = catalog.discover(Path(tmp))
            added = list(Counter(e_bad) - Counter(e_ok))
        x2_ok = (e_ok == [] and len(ent_ok) == 1 and sig(e_ok) == []
                 and added == [want] and removed == [] and sig(e_bad) == [want])
        ctl(u"X2", u"单一变量差异实验（仓外夹具 %s／%s，跑完即删）：status＝unreviewed 时 discover 错误集为空（实测 %d 枚），"
            u"只把 status 换成 reviewed 后错误集恰好多出一行「%s」" % (os.path.basename(tmp), FIXTURE_DIR, len(e_ok), want),
            x2_ok, {"tmp": tmp, "e_ok": e_ok, "e_bad": e_bad, "added": added, "removed": removed})

        # ---- X3 真根对照
        ent_real, err_real = catalog.discover(Path(LIB))
        sig_real = [x for x in err_real if u"Unknown lifecycle status" in x]
        dirs_real = sorted([p.parent.name for p in sys_json_paths])
        x3_ok = (sig_real == [] and len(ent_real) == len(dirs_real) == len(sys_json_paths)
                 and Counter([x for x in err_real]) == Counter())
        ctl(u"X3", u"真根对照：同一把尺打在真仓（%d 体系）上，Unknown lifecycle status 0 枚、discover 总错误 %d 枚 ⇒ "
            u"今天没有第 22 枚坏，红是这一步将来才会踩的" % (len(ent_real), len(err_real)),
            x3_ok, {"entries": len(ent_real), "errors": err_real, "dirs": len(sys_json_paths)})

        # ---- X4 归因反事实：把 reviewed 补进夹具词表 ⇒ 红消失；validated 仍红
        build_fixture(tmp, list(tax_disk[u"statuses"]) + [u"reviewed"], u"reviewed")
        _, e_ext_rev = catalog.discover(Path(tmp))
        build_fixture(tmp, list(tax_disk[u"statuses"]) + [u"reviewed"], u"validated")
        _, e_ext_val = catalog.discover(Path(tmp))
        want_val = u"Unknown lifecycle status: " + FIXTURE_DIR
        x4_ok = (sig(e_ext_rev) == [] and sig(e_ext_val) == [want_val])
        ctl(u"X4", u"归因反事实：夹具词表补一个 reviewed 后，reviewed 侧红消失（%d 枚）、validated 侧仍红（%d 枚）⇒ "
            u"红由词表成员定，不由 discover 的别的分支；两个词要两次决定"
            % (len(sig(e_ext_rev)), len(sig(e_ext_val))), x4_ok,
            {"ext_statuses": list(tax_disk[u"statuses"]) + [u"reviewed"], "sig_rev": sig(e_ext_rev),
             "sig_val": sig(e_ext_val)})

        # ---- X5 闸门短路：状态红不是「多一条 issue」，而是关掉整台闸门
        vlines = txt(VERIFY).splitlines()
        idx_guard = next((i + 1 for i, l in enumerate(vlines)
                          if l.strip().startswith(u"if catalog_errors:")), None)
        idx_ret = next((i + 1 for i, l in enumerate(vlines)
                        if idx_guard and i + 1 > idx_guard and re.match(u"^\\s+return\\b", l)), None)
        idx_links = next((i + 1 for i, l in enumerate(vlines) if u"local links:" in l), None)
        idx_ident = next((i + 1 for i, l in enumerate(vlines) if u"identity/type validation" in l), None)
        ml = txt(MCAT).splitlines()
        idx_refresh_guard = next((i + 1 for i, l in enumerate(ml)
                                  if u"Never generate a partial catalog" in l), None)
        idx_outputs = next((i for i, l in enumerate(ml) if l.strip().startswith(u"outputs = {")), None)
        if idx_outputs is None:
            raise Fatal(u"module_catalog.py 里找不到 refresh 的 outputs 块，无法给「重建要写几份」定价")
        _blk = ml[idx_outputs + 1:]
        _stop = next((i for i, l in enumerate(_blk) if l.rstrip() == u"    }"), len(_blk))
        n_outputs = sum(1 for l in _blk[:_stop] if u"root /" in l)
        if n_outputs < 1:
            raise Fatal(u"refresh 的 outputs 现读为 %d 份 ⇒ 解析失效" % n_outputs)
        eff_ret, eff_links = (idx_links, idx_ret) if MUT == u"m5" else (idx_ret, idx_links)
        x5_ok = (idx_guard and idx_ret and idx_links and idx_ident and eff_ret < eff_links
                 and idx_refresh_guard)
        ctl(u"X5", u"闸门短路（结构现读）：verify.py 第 %s 行 `if catalog_errors:` ⇒ 第 %s 行 return，"
            u"早于第 %s 行的 local links 计数行；module_catalog.refresh 第 %s 行同样拒绝 ⇒ "
            u"状态红会让整台闸门熄灯并令重建失效，不是多一条 issue"
            % (idx_guard, idx_ret, idx_links, idx_refresh_guard), x5_ok,
            {"guard": idx_guard, "return": idx_ret, "links": idx_links, "ident_fail": idx_ident,
             "refresh_refusal": idx_refresh_guard})

        # ---- X6 生成视图承载 status（改一处 status 不是单文件动作）
        ti_rows = re.findall(u"^- \\[.*?\\]\\(.*?/README\\.md\\) · `([^`]+)` · ", txt(TYPEIDX), re.M)
        rd_rows = re.findall(u"^\\| \\[.*?\\]\\(.*?/README\\.md\\) \\| ([^|]*) \\| ", txt(SYSREADME), re.M)
        st_multiset = Counter([e[u"status"] for e in ent_real])
        render_ti = catalog.render_types(sorted(ent_real, key=lambda e: str(e.get("id"))), tax_disk)
        render_rd = catalog.render_overview(sorted(ent_real, key=lambda e: str(e.get("id"))), tax_disk)
        # 渲染器吐 LF，盘上视图是 CRLF ⇒ 比同步前先把两把尺换到同一种货币，否则「不同步」是线段的形状不是账。
        ti_disk_lf = txt(TYPEIDX).replace(u"\r\n", u"\n")
        rd_disk_lf = txt(SYSREADME).replace(u"\r\n", u"\n")
        ti_sync = render_ti == ti_disk_lf
        rd_sync = render_rd == rd_disk_lf
        x6_ok = (Counter(ti_rows) == st_multiset and Counter(rd_rows) == st_multiset
                 and len(ti_rows) == len(ent_real) and len(rd_rows) == len(ent_real)
                 and ti_sync and rd_sync)
        ctl(u"X6", u"派生视图承载 status：TYPE_INDEX.md 的 %d 行与 README.md 的 %d 行的状态列多重集，"
            u"与 %d 份 system.json 的 status 逐值相等（含反引号／表格单元格两种形状）；"
            u"且两份视图今天与其渲染器逐字同步（EOL 归一后 %s／%s）⇒ 陈旧只可能由「改 status 不跑 refresh」这一步引入"
            % (len(ti_rows), len(rd_rows), len(ent_real), ti_sync, rd_sync), x6_ok,
            {"type_index_rows": len(ti_rows), "readme_rows": len(rd_rows),
             "status_multiset": dict(st_multiset),
             "renderer_vs_disk_typeindex": render_ti == txt(TYPEIDX),
             "renderer_vs_disk_readme": render_rd == txt(SYSREADME),
             "renderer_vs_disk_eol_normalized": {"TYPE_INDEX.md": ti_sync, "README.md": rd_sync}})

        # ---- X7 资格名册（流程第 2 步的前件：H/O 且无 falsified claim）
        health = json.loads(txt(HEALTH))
        rows = health[u"rows"]
        ho = [r for r in rows if r.get(u"rating") in (u"H", u"O")]
        elig = [r for r in ho if not r.get(u"self_falsified") and not r.get(u"audit_conflicts")]
        if MUT == u"m3":
            elig = list(ho)
        led_ids = sorted([r[u"id"] for r in rows])
        reg_ids = sorted([e[u"id"] for e in ent_real])
        st_by_id = dict([(e[u"id"], e[u"status"]) for e in ent_real])
        x7_ok = (0 < len(elig) < len(ho) and led_ids == reg_ids
                 and all(st_by_id[r[u"id"]] in tax_disk[u"statuses"] for r in elig))
        ctl(u"X7", u"资格名册：%d 行台账里 H/O %d 枚，同时满足「无自我记录证伪」「无审计冲突」者 %d 枚（严格更少）；"
            u"台账 id 集与已登记 system.json id 集逐字相等（%d＝%d）" % (len(rows), len(ho), len(elig), len(led_ids), len(reg_ids)),
            x7_ok, {"ho": [r[u"id"] for r in ho], "eligible": [r[u"id"] for r in elig],
                    "excluded": sorted(set(r[u"id"] for r in ho) - set(r[u"id"] for r in elig)),
                    "statuses": dict([(r[u"id"], st_by_id[r[u"id"]]) for r in elig])})

        # ---- X10 词表唯一性（治理管辖域内只有一份 statuses 词表）
        gov_json = [p for p in Path(GOV).rglob(u"*.json")]
        sys_json_all = list(sys_json_paths)
        scan_set = gov_json + sys_json_all
        hits = sorted([rel(p) for p in scan_set if b'"statuses"' in rb(p)])
        x10_ok = len(scan_set) > 0 and hits == [rel(TAX)]
        ctl(u"X10", u"词表唯一性：扫治理域 *.json %d 份（00_项目治理 全部 %d ＋ system.json %d），"
            u"含 \"statuses\" 键者恰 1 份＝%s ⇒ 没有第二份可绕的活词表"
            % (len(scan_set), len(gov_json), len(sys_json_all), u"、".join(hits)), x10_ok,
            {"scan_size": len(scan_set), "hits": hits})

        # ---- X11 两个账的对照（primary claims.csv vs 健康度台账）
        claims_stat = {}
        for p in claims_paths:
            rs = list(csv.DictReader(io.open(str(p), encoding="utf-8-sig", errors="replace")))
            dname = os.path.basename(os.path.dirname(str(p)))
            claims_stat[dname] = {
                "rows": len(rs),
                "falsified_literal": sum(1 for x in rs if (x.get("status") or "").strip() == u"falsified"),
                "falsified_loose": sum(1 for x in rs if u"falsif" in (x.get("status") or "").lower()),
                "statuses": dict(collections.Counter([(x.get(u"status") or u"").strip() for x in rs])),
            }
        dir_by_id = dict([(e[u"id"], e[u"directory"]) for e in ent_real])
        cmp_rows = []
        for r in rows:
            dname = dir_by_id.get(r[u"id"], u"")
            c = claims_stat.get(dname, {u"rows": 0, u"falsified_literal": 0, u"falsified_loose": 0, u"statuses": {}})
            cmp_rows.append({"id": r[u"id"], "rating": r.get(u"rating"), "dir": dname,
                             "ledger_sf": len(r.get(u"self_falsified") or []),
                             "claims_falsified": c[u"falsified_literal"],
                             "claims_rows": c[u"rows"], "status_vocab_size": len(c[u"statuses"])})
        mismatch = [x for x in cmp_rows if x["ledger_sf"] != x["claims_falsified"]]
        elig_ids = set(r[u"id"] for r in elig)
        elig_clean = [x for x in cmp_rows if x["id"] in elig_ids
                      and x["ledger_sf"] == 0 and x["claims_falsified"] == 0]
        claims_total = sum(v["rows"] for v in claims_stat.values())
        status_vocab_all = sorted({k for v in claims_stat.values() for k in v["statuses"]})
        x11_ok = len(elig_clean) == len(elig)
        ctl(u"X11", u"两账对照：资格名册 %d 枚在**一手记录**上同样干净（claims.csv 里 status 恰为 falsified 者 0 行）；"
            u"但全仓 %d 行里台账 self_falsified 与 claims.csv 的 falsified 行数不等者 %d 枚 ⇒ 「无 falsified claim」这句话有两个账"
            % (len(elig), claims_total, len(mismatch)), x11_ok,
            {"eligible_clean": [x["id"] for x in elig_clean], "mismatch": mismatch,
             "claims_total_rows": claims_total, "claims_status_vocab": len(status_vocab_all)})

        # ---- X12 跨轮同源：本册的一手行数必须与 v9 面的分母同值（两台仪器各算各的）
        v9_face = json.loads(txt(V9_FACE))
        v9_rows = v9_face.get(u"denominator", {}).get(u"rows_total")
        v9_na = v9_face.get(u"aggregate", {}).get(u"V_gt_0_count")
        x12_ok = (v9_rows == claims_total and v9_na == 0)
        ctl(u"X12", u"跨轮同源：v9 面自报分母 rows_total＝%s，本册现扫 claims.csv 总行＝%d（两台仪器各自解析，须同值）；"
            u"v9 的 V>0 计数＝%s" % (v9_rows, claims_total, v9_na), x12_ok,
            {"v9_rows_total": v9_rows, "this_rows_total": claims_total, "v9_V_gt_0": v9_na,
             "v9_generated": v9_face.get(u"generated_utc"), "v9_md5": md5(rb(V9_FACE))})

        # ---- X8 验收第 5 步现场（子进程真跑 verify.py，承载文件本轮写出并复量）
        proc = subprocess.Popen([sys.executable, "-B", "verify.py"], cwd=LIB,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = proc.stdout.read()
        proc.stdout.close()
        rc_verify = proc.wait()
        open(SUB_CARRIER, "wb").write(out)
        carrier = rb(SUB_CARRIER)
        if not carrier or len(carrier) < 20:
            raise Fatal(u"验收承载未写或为空（%d B）⇒ rc=%s 不可引用" % (len(carrier), rc_verify))
        ct = carrier.decode("utf-8", "replace")
        m_fail = re.search(u"FAIL: (\\d+) issues", ct)
        m_links = re.search(u"local links: (\\d+)", ct)
        ident_line = u"identity/type validation" in ct
        mine_named = sum(1 for w in [STEM] if w in ct)
        r76_ct = txt(R76_CARRIER)
        r76_fail = re.search(u"FAIL: (\\d+) issues", r76_ct)
        r76_links = re.search(u"local links: (\\d+)", r76_ct)
        x8_ok = (m_fail and m_links and not ident_line and mine_named == 0)
        ctl(u"X8", u"验收第 5 步现场：子进程真跑 verify.py 得 rc=%d、判决行「FAIL: %s issues」、链接计数 %s；"
            u"承载 %s 本轮写出（%d B／md5 %s，mtime 晚于本册启动 %s）；点名本轮产物 %d 次"
            % (rc_verify, m_fail.group(1) if m_fail else u"?", m_links.group(1) if m_links else u"?",
               os.path.basename(SUB_CARRIER), len(carrier), md5(carrier),
               os.path.getmtime(SUB_CARRIER) >= t0, mine_named), x8_ok,
            {"rc": rc_verify, "fail_issues": int(m_fail.group(1)) if m_fail else None,
             "links": int(m_links.group(1)) if m_links else None,
             "identity_short_circuit": ident_line, "carrier_bytes": len(carrier),
             "carrier_md5": md5(carrier),
             "r76_fail_issues": int(r76_fail.group(1)) if r76_fail else None,
             "r76_links": int(r76_links.group(1)) if r76_links else None,
             "elapsed_sec": round(time.time() - t0, 2)})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- X9 中立性：判决计算后与写出前各复量一次
    sweep_mid = sweep(u"判决计算后、落盘前")
    x9_ok = not sweep_mid[u"moved"]
    ctl(u"X9", u"中立性：本册 %d 份输入（%s）在判决计算后逐份复量，移动 %d 份"
        % (sweep_mid[u"inputs"],
           u"＋".join(u"%s×%d" % (lbl, len(g)) for lbl, g in corpus_groups),
           len(sweep_mid[u"moved"])),
        x9_ok, {"sweep": sweep_mid,
                "kinds": dict([(lbl, len(g)) for lbl, g in corpus_groups])})

    gate_md5_flow = md5(rb(FLOW_SRC))
    flow_lines = [l for l in txt(FLOW_SRC).splitlines() if u"reviewed" in l or u"validated" in l]

    def line_of(path, needle, want_unique=True):
        """把一句主张钉回「印出它的那一行」：行号从盘上现读，不打字。"""
        if not os.path.isfile(path):
            raise Fatal(u"承载文件不存在，主张无处可挂：%s" % rel(path))
        hits = [i + 1 for i, l in enumerate(txt(path).splitlines()) if needle in l]
        if not hits:
            raise Fatal(u"%s 里没有含「%s」的行" % (os.path.basename(path), needle))
        if want_unique and len(hits) != 1:
            raise Fatal(u"%s 里「%s」命中 %d 行（%s），无法唯一定位" % (
                os.path.basename(path), needle, len(hits), hits))
        return hits[0]

    rank_line = line_of(ACHIEVE_DOC, u"先做 D5")
    rank_text = txt(ACHIEVE_DOC).splitlines()[rank_line - 1].strip()
    promote_line = line_of(D45_DOC, u"推进到 reviewed/validated")
    promote_text = txt(D45_DOC).splitlines()[promote_line - 1].strip()
    flow2_line = line_of(FLOW_SRC, u"由 unreviewed 改为 reviewed")
    flow6_line = line_of(FLOW_SRC, u"体系进入 reviewed/validated")
    flow6_text = txt(FLOW_SRC).splitlines()[flow6_line - 1].strip().strip(u'",')

    face = {
        "instrument": INSTR_NAME,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "rc": 0 if all(c["fired"] for c in CONTROLS) else 1,
        "mode": (u"mutant:" + MUT) if MUT else (u"land" if LAND else u"dry"),
        "authorities": {
            "module_types": {"path": rel(TAX), "bytes": len(rb(TAX)), "md5": md5(rb(TAX)),
                             "statuses": tax_disk[u"statuses"]},
            "module_catalog": {"path": rel(MCAT), "bytes": len(rb(MCAT)), "md5": md5(rb(MCAT))},
            "verify": {"path": rel(VERIFY), "bytes": len(rb(VERIFY)), "md5": md5(rb(VERIFY))},
            "health_ledger": {"path": rel(HEALTH), "bytes": len(rb(HEALTH)), "md5": md5(rb(HEALTH)),
                              "counts": health.get(u"counts")},
            "flow_source": {"path": rel(FLOW_SRC), "md5": gate_md5_flow, "lines": flow_lines},
        },
        "fixture": {"root_outside_repo": True, "dir_name": FIXTURE_ID, "clean_errors": e_ok,
                    "reviewed_added_error": added, "extended_vocab_reviewed": sig(e_ext_rev),
                    "extended_vocab_validated": sig(e_ext_val)},
        "real_root": {"entries": len(ent_real), "discover_errors": err_real,
                      "unknown_status_rows": sig_real},
        "derived_views": {"type_index_rows": len(ti_rows), "readme_rows": len(rd_rows),
                          "status_multiset": dict(st_multiset),
                          "renderer_matches_disk_eol_normalized": {
                              "TYPE_INDEX.md": ti_sync, "README.md": rd_sync},
                          "renderer_matches_disk_raw_bytes": {
                              "TYPE_INDEX.md": render_ti == txt(TYPEIDX),
                              "README.md": render_rd == txt(SYSREADME),
                              "note": u"渲染器吐 LF、盘上视图为 CRLF ⇒ 原始字节比较恒为 false，是货币差不是陈旧"}},
        "roster": {"systems_total": len(rows), "H_or_O": len(ho), "eligible": [r[u"id"] for r in elig],
                   "excluded": sorted(set(r[u"id"] for r in ho) - set(r[u"id"] for r in elig)),
                   "eligible_status": dict([(r[u"id"], st_by_id[r[u"id"]]) for r in elig])},
        "two_ledgers": {"mismatch": mismatch, "mismatch_count": len(mismatch),
                        "claims_total_rows": claims_total,
                        "claims_status_vocab": len(status_vocab_all), "cmp": cmp_rows},
        "target_addressing": {"flow_step1": [l for l in flow_lines if u"晋升对象" in l],
                              "system_json_mentioning_L6_UFE2": sum(
                                  1 for p in sys_json_paths
                                  if any(k in rb(p).decode("utf-8", "replace") for k in (u"UFE-2", u"39 总纲", u"L6")))},
        "acceptance_step5": [c for c in CONTROLS if c["code"] == u"X8"][0]["payload"],
        "read_only_sweep": sweep_mid,
        "claim_carriers": {
            "ranking": {"file": rel(ACHIEVE_DOC), "line": rank_line, "text": rank_text},
            "promotion_target": {"file": rel(D45_DOC), "line": promote_line, "text": promote_text},
            "flow_step2": {"file": rel(FLOW_SRC), "line": flow2_line},
            "vocabulary": {"file": rel(TAX), "statuses": tax_disk[u"statuses"]},
        },
        "controls": CONTROLS,
        "controls_total": len(CONTROLS),
        "controls_fired": sum(1 for c in CONTROLS if c["fired"]),
        "controls_red": [c["code"] for c in CONTROLS if not c["fired"]],
        "elapsed_sec": round(time.time() - t0, 2),
    }
    face_json = json.dumps(face, ensure_ascii=False, indent=1)
    face_bytes = face_json.encode(u"utf-8")
    suffix = (u".mut-" + MUT) if MUT else u""
    face_path = os.path.join(OUT_DIR, FACE_NAME.replace(u".json", suffix + u".json"))

    if not all(c["fired"] for c in CONTROLS):
        print(u"控制未全点火：%s ⇒ 不落库（只把预跑面与卷写进 scratch）" % face["controls_red"])
        rc = 1
    else:
        rc = 0

    if MUT:
        want_code = EXPECTED_RED[MUT]
        if want_code not in face["controls_red"]:
            raise Fatal(u"变异体 %s（%s）没有打破它点名的控制 %s ⇒ 该控制是橡皮章，本册不许自证有效"
                        % (MUT, MUT_NAMES[MUT], want_code))
        others = [c for c in face["controls_red"] if c != want_code]
        print(u"MUT=%s（%s）：指定控制 %s 已红；连带红＝%s；rc=1" % (MUT, MUT_NAMES[MUT], want_code, others))

    sweep_last = sweep(u"判决计算后、写出前")
    if sweep_last[u"moved"] and not MUT:
        raise Fatal(u"语料在判决计算后移动（%d 份：%s）⇒ 本面/本卷作废，须重跑"
                    % (len(sweep_last[u"moved"]), sweep_last[u"moved"]))

    n_ho = len(ho)
    n_elig = len(elig)
    mism = len(mismatch)
    ap = face[u"acceptance_step5"]
    v_statuses = u"、".join(tax_disk[u"statuses"])
    v_worst = sorted(cmp_rows, key=lambda x: -abs(x["ledger_sf"] - x["claims_falsified"]))[:3]
    v_worst_ct = u"；".join(u"`%s` 台账 %d／一手 %d" % (x["id"], x["ledger_sf"], x["claims_falsified"]) for x in v_worst)
    v_st_dist = json.dumps(dict(Counter([e[u"status"] for e in ent_real])), ensure_ascii=False)
    n_promoted = sum(1 for e in ent_real if e[u"status"] in (u"reviewed", u"validated"))
    v_excl = u"、".join(face[u"roster"][u"excluded"])
    v_elig_ids = u"、".join(u"`%s`" % i for i in face[u"roster"][u"eligible"])
    v_carrier_ti = u"%s:%d" % (os.path.basename(ACHIEVE_DOC), rank_line)
    v_carrier_flow = u"%s:%d" % (os.path.basename(D45_DOC), promote_line)
    cat_rows_mine = sum(1 for l in txt(CATALOG).splitlines() if STEM in l)
    links_delta = ap[u"links"] - ap[u"r76_links"]
    links_attrib = (u"与目录里点名本册三件的行数 %d 同值（每件各成一行本地链接）" % cat_rows_mine
                    if links_delta == cat_rows_mine else
                    u"与目录点名行数 %d 不等 ⇒ 增量另有来源（同窗并发写者），本册不替它归属" % cat_rows_mine)
    issues_clause = (u"与上轮同值" if ap[u"fail_issues"] == ap[u"r76_fail_issues"]
                     else u"由 %s 变到 %s（本轮未点名任何产物，见下）" % (ap[u"r76_fail_issues"], ap[u"fail_issues"]))

    L = []
    P = L.append
    P(u"# 判定 · 进门闸 v10 · D5「外部验证流程」**可执行性**核查 · 2026-10-19")
    P(u"")
    P(u"问题只有一句：达成度册把 D5 排在第一位——`%s` 第 %d 行印着「%s」；" % (os.path.basename(ACHIEVE_DOC), rank_line, rank_text))
    P(u"而同一册的收口卷 `%s` 第 %d 行把目标写成「%s」。本册测的是**这一步今天能不能落地**，" % (
        os.path.basename(D45_DOC), promote_line, promote_text))
    P(u"判据全部来自治理域的三份权威（`%s` 的词表、`%s` 的谓词、`%s` 的接线），不用散文。"
      % (rel(TAX), rel(MCAT), rel(VERIFY)))
    P(u"")
    P(u"## §1 三道锁（逐把有反证）")
    P(u"")
    P(u"1. **词表锁**。statuses 词表盘上为 `%s`——`reviewed`／`validated` 都不在其中（X1）。" % v_statuses)
    P(u"   在仓外一份**良定**的最小模块上（status＝unreviewed 时 discover 错误集为空，实测 %d 枚，X2）只改 status 一个字段，" % len(e_ok))
    P(u"   错误集恰好多出 `Unknown lifecycle status: %s`；把夹具词表补一个 reviewed 后这一行消失，而 `validated` 仍红（X4）⇒" % FIXTURE_DIR)
    P(u"   红由**词表成员**决定，不由 discover 的其它分支决定。这一句要付两次账：流程文本里的两个词，是两个独立决定。")
    P(u"2. **短路锁**。`verify.py` 第 %s 行 `if catalog_errors:` 之后第 %s 行就 `return`，早于第 %s 行的 `local links:` 计数行（X5 现读）。"
      % (idx_guard, idx_ret, idx_links))
    P(u"   所以一个非法状态不是「多一条 issue」，而是**整台闸门熄灯**：结构／迁移／溯源／链接全部不再执行，")
    P(u"   连 issue 总数都不再印出。同一把尺里 `refresh()` 第 %s 行「Never generate a partial catalog」⇒ 非法身份还令目录重建失效。" % idx_refresh_guard)
    P(u"3. **派生视图锁**。status 不止住在 system.json 一处：TYPE_INDEX.md 的 %d 行（反引号单元格）与 README.md 的 %d 行（表格中段）"
      % (len(ti_rows), len(rd_rows)))
    P(u"   的状态多重集与 %d 份 system.json 逐值相等（X6）⇒ 改一个 status 而不重跑 `module_catalog.py refresh` 会留下陈旧的生成视图。" % len(ent_real))
    P(u"   两份视图今天与其渲染器**逐字同步**（EOL 归一后 %s／%s；按原始字节比必然为假——渲染器吐 LF、盘上视图是 CRLF，那是线段的货币差不是账）"
      u"⇒ 陈旧不会由别处先来，只会由「改 status 不跑 refresh」这一步引入。" % (ti_sync, rd_sync))
    P(u"   而 refresh 现读要写 %d 份**共享治理文件**（索引／layout／system_registry／两份入口），且被第 2 把锁拒绝执行；" % n_outputs)
    P(u"   本册连 refresh 也没跑（X9 只读复量移动 %d 份，写出前复量 %d 份）。" % (len(sweep_mid[u"moved"]), len(sweep_last[u"moved"])))
    P(u"")
    P(u"## §2 名册：谁有资格被晋升")
    P(u"")
    P(u"流程第 2 步的前件是「H/O 且无 falsified claim」。按盘上台账（`%s`，counts %s）现算："
      % (rel(HEALTH), json.dumps(health.get(u"counts"), ensure_ascii=False)))
    P(u"")
    P(u"| 口径 | 枚数 |")
    P(u"|---|---:|")
    P(u"| 台账行数（＝已登记体系数） | %d |" % len(rows))
    P(u"| rating ∈ {H, O} | %d |" % n_ho)
    P(u"| 再要求「无自我记录证伪」且「无审计冲突」 | **%d** |" % n_elig)
    P(u"| 这 %d 枚在一手记录（claims.csv 的 status 恰为 `falsified`）上同样为 0 枚者 | %d |" % (n_elig, len(elig_clean)))
    P(u"| 今天已是 reviewed／validated 者 | %d（现役分布 %s） |" % (n_promoted, v_st_dist))
    P(u"")
    P(u"被前件挡掉的 %d 枚：%s。名册非空（%s）⇒ **D5 不是没有候选人，是被词表挡在门外**；"
      % (n_ho - n_elig, u"、".join(face[u"roster"][u"excluded"]), v_elig_ids))
    P(u"这与流程第 6 行自报的「%s」（`%s:%d`）一致，但把原因从「没人去做」换成「按原文做不了」。" % (
        flow6_text, os.path.basename(FLOW_SRC), flow6_line))
    P(u"")
    P(u"两处必须并读的第二账：全仓 claims.csv %d 行里，台账 `self_falsified` 数与一手记录 `falsified` 行数**不等者 %d 枚**"
      % (claims_total, mism))
    P(u"（逐枚印在面内 `two_ledgers.mismatch`；claims.csv 的 status 列现扫有 %d 种取值，含把散文写进状态列的行）⇒" % len(status_vocab_all))
    P(u"「无 falsified claim」这句话在写晋升理由之前，必须先说清吃哪一个账。差异最大的三枚：%s。" % v_worst_ct)
    P(u"资格名册这一侧干净（%d 枚两侧同为 0），所以本册裁定不受影响；受影响的是**将来任何一条晋升理由的措辞**。" % len(elig_clean))
    P(u"")
    P(u"## §3 验收第 5 步今天不可达（与本轮无关）")
    P(u"")
    P(u"本轮子进程真跑 `python -B verify.py`：rc=%d，判决行「FAIL: %s issues」，`local links: %s`；承载 `%s`（%d B／md5 %s，本轮写出）。"
      % (ap[u"rc"], ap[u"fail_issues"], ap[u"links"], os.path.basename(SUB_CARRIER), ap[u"carrier_bytes"], ap[u"carrier_md5"]))
    P(u"上轮承载 `scratch/verify_r76.txt` 为 FAIL %s issues／links %s ⇒ issues %s，非本轮引入；"
      % (ap[u"r76_fail_issues"], ap[u"r76_links"], issues_clause))
    P(u"links %+d（%d→%d）：%s——这一句只给副作用定价，不改判决。" % (
        links_delta, ap[u"r76_links"], ap[u"links"], links_attrib))
    P(u"承载文本点名本册产物 **%d 次**。故流程第 5 步「门禁 PASS」这一验收今天为红，且红在别人管辖的文件里——" % mine_named)
    P(u"D5 既不是把它变绿的东西，也不能在自己没做完时替它签字。第 2 把锁还有一层后果：若先写了非法 status，连 issue 计数都不再印出，")
    P(u"本仓将**失去可引用的闸门账本**。")
    P(u"")
    P(u"## §4 决策项（不在本册权限内，逐条给出口）")
    P(u"")
    P(u"1. **词表决定**：把 `reviewed`（及是否含 `validated`）加进 `%s` 的 statuses，" % rel(TAX))
    P(u"   还是把达成度册／流程第 2 步改写成现役词表里的某个值（`active`／`paused`）。前者动治理词表、影响 %d 份登记的判据；" % len(ent_real))
    P(u"   后者只动一句措辞。X4 证明这两条路是**可分辨的**：补词表 ⇒ 红消失；不改词表 ⇒ 红常驻。")
    P(u"2. **重建路径决定**：无论走哪条，改 status 之后必须有人跑 `module_catalog.py refresh`（该函数现读写出 %d 份共享治理文件）并复跑 verify；"
      % n_outputs)
    P(u"   本册一份也没写（X9 只读复量）。")
    P(u"3. **晋升对象寻址**：流程第 1 步写「L6 UFE-2 / 39 总纲」，而 %d 份 system.json 里含 `UFE-2`／`39 总纲`／`L6` 者 %d 份（现读）⇒"
      % (len(sys_json_paths), face[u"target_addressing"][u"system_json_mentioning_L6_UFE2"]))
    P(u"   第 1 步的对象不落在登记身份上，须由人把它映射到 `s01…s18/p01…p04` 之一，否则第 2 步「改哪一份」无人能答。")
    P(u"4. **两账口径**：晋升理由里的「无 falsified claim」须点名吃台账还是 claims.csv（§2 已给 %d 枚不等的名册）。" % mism)
    P(u"")
    P(u"## §5 中立性与跨轮漂移")
    P(u"")
    P(u"本册对真仓**零改动**：词表 md5 `%s`、两把治理刀 md5 `%s`／`%s`、%d 份 system.json 全部在只读复量名单里（共 %d 份输入）。"
      % (md5(rb(TAX)), md5(rb(MCAT)), md5(rb(VERIFY)), len(sys_json_paths), sweep_mid[u"inputs"]))
    P(u"判决计算后与写出前各量一次，移动 %d／%d 份（写出前若移动即 FATAL，本面作废）。" % (
        len(sweep_mid[u"moved"]), len(sweep_last[u"moved"])))
    P(u"夹具树落在系统临时目录（`v10_d5_fixture_*`，仓外），跑出后即 `rmtree`，仓内不留夹具。")
    P(u"跨轮对照（数字取自盘上的 v9 面，不打字）：v9 判**判别力**——登记上界 %d 枚里 V>0＝%d 枚；本册判**治理动作的可执行性**。"
      % (len(v9_face[u"denominator"][u"ceiling"]), v9_face[u"aggregate"][u"V_gt_0_count"]))
    P(u"两册同向——门禁放行≠可登记≠对世界有预言，而「可登记」这一环今天还多一道锁：**词表里没有那个词**。")
    P(u"达成度册的 D5 主张逐字挂在 `%s`，晋升对象主张挂在 `%s`（两处行号由本册现读，原文引在卷首）。" % (v_carrier_ti, v_carrier_flow))
    P(u"")
    P(u"## §6 自检控制（%d/%d 点火）" % (sum(1 for c in CONTROLS if c["fired"]), len(CONTROLS)))
    P(u"")
    P(u"| 码 | 题面 | 点火 |")
    P(u"|---|---|---|")
    for c in CONTROLS:
        P(u"| %s | %s | %s |" % (c["code"], sanitize(c["title"]), u"是" if c["fired"] else u"**否**"))
    P(u"")
    P(u"绿只证明控制**在真数据上不报警**。五枚变异体（`--mutant=m1｜m2｜m3｜m4｜m5`：词表改成打字常量／差异实验抹平单一变量／")
    P(u"资格名册丢掉连词后两半／伪造判决后语料移动／把闸门短路顺序对调）各点名打破一条控制（m1→X1、m2→X2、m3→X7、m4→X9、m5→X5），")
    P(u"产物另存 `…mut-mN` 名，不覆盖本面；指定控制不红则仪器自己 FATAL——「全绿不算证据」写在代码里，不写在 prose 里。")
    P(u"")
    P(u"## §7 裁定与债")
    P(u"")
    P(u"1. **裁定**：D5 按流程文本执行**当前不可行**（词表缺词＋闸门短路＋生成视图三把锁，X1／X2／X4／X5／X6 逐把带反证）。")
    P(u"   达成度册「工程量最小」这一排序在**治理权限**上，不在机器上；把它当机器可完成项去推进，会先撞第 2 把锁并把整台闸门弄熄灯。")
    P(u"2. **净读数**：候选非空（%d／%d，且两侧账同为 0）、已晋升 %d／%d、验收步 5 现场红（FAIL %s issues，非本轮引入）⇒"
      % (n_elig, len(rows), n_promoted, len(ent_real), ap[u"fail_issues"]))
    P(u"   D5 的卡点是**一个词表决定**加**一次重建**，不是物理，也不是登记口径的放宽。")
    P(u"3. 债 **G（本册新增）**：晋升理由的「无 falsified claim」两账口径未定（%d 枚不等，方向双向）。" % mism)
    P(u"4. 债 **H（本册新增）**：流程第 1 步的晋升对象未寻址（%d／%d 份 system.json 能被「L6 UFE-2／39 总纲」钉住）。"
      % (face[u"target_addressing"][u"system_json_mentioning_L6_UFE2"], len(sys_json_paths)))
    P(u"5. 旧债 **B／C／D／E／F** 原样挂着（`ineq_bare` 档裁定、列语义分工、基线欠登记 106、有量纲值进池口径、误差棒来源分档）。")
    P(u"")
    P(u"## §8 产物钉")
    P(u"")
    P(u"（本卷不钉自己；下面这一行钉面与仪器，`--land` 分支在落盘后从**盘上的卷**找回这两个数并量盘像，不符即 FATAL。）")
    P(u"")
    P(u"面 `%s` %d B／md5 `%s`；仪器 `%s` %d B／md5 `%s`" % (FACE_NAME, len(face_bytes), md5(face_bytes),
                                                        INSTR_NAME, instr_bytes, instr_md5))
    P(u"")
    vol_text = u"\r\n".join(L) + u"\r\n"
    residue = re.findall(u"%[sdfg]", vol_text)
    if residue:
        raise Fatal(u"卷面有 %d 处未插值占位符 %s ⇒ 不落盘" % (len(residue), sorted(set(residue))))
    vol_bytes = vol_text.encode(u"utf-8")
    vol_path = os.path.join(PROJP if LAND else SCRATCH,
                            VOL_NAME.replace(u".md", suffix + u".md") if MUT else VOL_NAME)

    open(face_path, "wb").write(face_bytes)
    if LAND:
        open(os.path.join(SRC, INSTR_NAME), "wb").write(landed_image)
    open(vol_path, "wb").write(vol_bytes)
    if LAND:
        if os.path.dirname(face_path) != DATA:
            raise Fatal(u"面分箱走偏：%s" % face_path)
        preced = sorted([f for f in os.listdir(PROJP) if f.startswith(u"判定_进门闸_v")])
        if VOL_NAME not in preced or len(preced) < 4:
            raise Fatal(u"卷未与 v7／v8／v9 同目录并列（PROJP 下判定_进门闸_v*＝%s）" % preced)
        landed_instr = rb(os.path.join(SRC, INSTR_NAME))
        scratch_src = rb(SELF_PATH) if SELF_PATH != os.path.join(SRC, INSTR_NAME) else landed_instr
        if scratch_src.replace(b"\r\n", b"\n") != landed_instr.replace(b"\r\n", b"\n"):
            raise Fatal(u"W1 落盘的刀≠手里的刀")
        on_vol = open(vol_path, "rb").read().decode(u"utf-8")
        on_face = rb(face_path)
        m = re.search(u"面 `%s` (\\d+) B／md5 `([0-9a-f]{32})`；仪器 `%s` (\\d+) B／md5 `([0-9a-f]{32})`"
                      % (re.escape(FACE_NAME), re.escape(INSTR_NAME)), on_vol)
        if not m:
            raise Fatal(u"卷里找不到它自己印的产物钉行——本次产物不得引用")
        bad_f = (int(m.group(1)), m.group(2)) != (len(on_face), md5(on_face))
        bad_i = (int(m.group(3)), m.group(4)) != (len(landed_instr), md5(landed_instr))
        if bad_f or bad_i:
            raise Fatal(u"卷印的钉与盘上图像不符（面 %s／仪器 %s）——本次产物不得引用"
                        % (u"异" if bad_f else u"同", u"异" if bad_i else u"同"))
        print(u"W1＋钉行盘上复核通过：仪器 %d B（scratch 源 %d B，EOL 归一后逐字同）" % (len(landed_instr), len(scratch_src)))

    print(u"控制 %d/%d 点火，rc=%d｜面 %s %d B md5 %s｜卷 %s %d B md5 %s｜耗时 %.1fs" % (
        face["controls_fired"], face["controls_total"], rc,
        rel(face_path), len(face_bytes), md5(face_bytes),
        rel(vol_path), len(vol_bytes), md5(vol_bytes), time.time() - t0))
    print(u"H/O %d 枚｜资格 %d 枚｜两账不等 %d 枚｜verify 子跑 rc=%s FAIL=%s links=%s｜只读移动 %d／%d" % (
        n_ho, n_elig, mism, ap[u"rc"], ap[u"fail_issues"], ap[u"links"],
        len(sweep_mid[u"moved"]), len(sweep_last[u"moved"])))
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fatal as e:
        print(u"FATAL: %s" % e)
        sys.exit(2)
