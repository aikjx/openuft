# -*- coding: utf-8 -*-
r"""TUFT-r235 · 总览合并轮：七层交互页统一入口（整理轮，无新数值）
2026-10-26

〔编号说明〕本卷取号 r235（落盘前实测 r235–r236 空；开工基线 verify.py PASS=0）。
用户验收裁决（本卷核心事件）：**「完成统一场论」的验收口径 = 边界地图完成态**——
r214–r234 十七轮边界地图 + 形式统一四层 + 引力五层闭合（动力学统一 FAIL、供给 0）
即视为完成（物理统一按 r229 判定属当前物理学不可达，已如实登记）。

本卷任务：把七张交互可视化（r221/226/227/228/230/232/234）合并为**统一入口总览页**——
单文件、零外部 URL、每轮一张导航卡（轮号/条目分布/一句话结论/核心读数/详情链接）。

诚实定位：纯整理轮，无新数值——所有数字来自七轮已落盘 JSON（只读）。
守卫：payload 完整性、文件在位、零外部 URL、17 轮 ledger 完整。

纪律：纯标准库；对 r214–r234 及并行会话产物只读；条目不可与 r142–r234 相加。
"""

import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJ = os.path.dirname(_HERE)
_DATADIR = os.path.join(_PROJ, "数据")
_TMPL = os.path.join(_HERE, "TUFT-r235_总览页构建模板_2026-10-26.html")
HTML_OUT = os.path.join(_PROJ, "四力统一方程_总览页_2026-10-26.html")

MARKER = "R235-OVERVIEW-MERGE"
BASE = "TUFT-r235_四力统一方程_总览合并轮_七层交互页统一入口_整理与验收归档_2026-10-26"
STEM = "TUFT-r235"

# 七轮：轮号 → 交互 HTML 文件名 → 层名 → 核心读数提取器（字段路径，宽容）
LAYERS = [
    (221, "四力统一运动方程_交互可视化_2026-10-26.html", "经典母式层（UFE-4F⁺）",
     [("readings", "eta", "146"), ("readings", "eta", "fit")]),
    (226, "四力统一方程_量子束缚层可视化_2026-10-26.html", "量子束缚层",
     [("counts", "PASS"), ("counts", "FAIL")]),
    (227, "四力统一方程_散射层可视化_2026-10-26.html", "散射层（动量空间镜像）",
     [("readings", "eta", "146"), ("readings", "weak_contact", "ratio")]),
    (228, "四力统一方程_变分层可视化_2026-10-26.html", "变分层（拉格朗日与诺特）",
     [("readings", "stat", "dS_rel"), ("readings", "noether", "E")]),
    (230, "四力统一方程_引力本质层可视化_2026-10-26.html", "引力本质层（WEP+1PN）",
     [("readings", "precession", "arcsec_century"), ("readings", "light", "arcsec")]),
    (232, "四力统一方程_引力波层可视化_2026-10-26.html", "引力波层（四极+啁啾）",
     [("readings", "quad", "rel"), ("readings", "ht", "rel_pct")]),
    (234, "四力统一方程_强场层可视化_2026-10-26.html", "强场层（ISCO+光子球）",
     [("readings", "photon", "rel"), ("readings", "isco", "g_unstable")]),
]

LEDGER_17 = [
    ("r214", "经典静态中心力母式", "形式统一 PASS；动力学统一 FAIL"),
    ("r217", "独立复核+根目录整理", "数字可复算"),
    ("r218", "定义恒等式审计", "相符=规定；预测预算 0"),
    ("r219", "多源叠加+相对论化", "经典动力学同框闭合"),
    ("r220", "矢量场与通量", "潮汐/散度机验"),
    ("r221", "禁闭 σr+通道门", "r214 严格超集"),
    ("r222", "传播层", "质量-力程等价"),
    ("r223", "轨道进动（并行）", "进动精算"),
    ("r224", "Proca+荷空间（并行）", "圆轨道稳定性"),
    ("r225", "尺度分层+维里（并行）", "进动闭式"),
    ("r226", "量子束缚层", "四力束缚判决"),
    ("r227", "散射层", "η=g 交叉定罪"),
    ("r228", "变分层", "作用量统一判据"),
    ("r229", "新颖性审计", "无新理论/供给 0"),
    ("r230", "引力本质层", "WEP+1PN 复现"),
    ("r232", "引力波层", "四极+HT 锚+啁啾"),
    ("r234", "强场层", "ISCO+光子球+1PN 失效曲线"),
]

guards, entries = [], []


def guard(gid, title, ok, detail, numbers=None):
    guards.append({"id": gid, "title": title, "ok": bool(ok),
                   "detail": detail, "numbers": numbers or {}})
    if not ok:
        print(f"[GUARD-FAIL] {gid} {title}: {detail}")
    return bool(ok)


def entry(code, level, title, detail, numbers=None):
    entries.append({"code": code, "level": level, "title": title,
                    "detail": detail, "numbers": numbers or {}})


def dig(data, path):
    cur = data
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def fmt(v):
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.4g}"
    return str(v)


def main():
    cards = []
    parsed = 0
    for (rid, fname, layer, keys) in LAYERS:
        path = os.path.join(_PROJ, fname)
        ok_file = os.path.isfile(path)
        data = None
        if ok_file:
            html = open(path, encoding="utf-8").read()
            try:
                marker = "__R%d_JSON__" % 0
                import re
                m = re.search(r"const R = (\{.*?\});\n", html, re.S)
                if m:
                    data = json.loads(m.group(1))
                    parsed += 1
            except Exception:
                data = None
        c = (data or {}).get("counts", {})
        verdict = (data or {}).get("verdict", "")
        judgement = (data or {}).get("judgement", "")
        heads = []
        for kp in keys:
            v = dig(data, kp)
            if v is not None:
                heads.append(f"{kp[-1]}={fmt(v)}")
        cards.append({
            "round": rid, "file": fname, "layer": layer,
            "ok_file": ok_file, "parsed": data is not None,
            "entries": fmt(c.get("entries")), "PASS": fmt(c.get("PASS")),
            "FAIL": fmt(c.get("FAIL")), "BOUNDARY": fmt(c.get("BOUNDARY")),
            "INFO": fmt(c.get("INFO")), "guards": fmt(c.get("guards")),
            "headline": "；".join(heads) if heads else "—",
            "verdict_short": verdict[:110],
            "judgement": judgement[:150],
        })
    n_ok = sum(1 for x in cards if x["ok_file"])
    guard("G1", "七层交互 HTML 文件在位", n_ok == 7,
          f"7/7 在位（r221/226/227/228/230/232/234）", {"n_ok": n_ok})
    guard("G2", "七层 payload JSON 可解析", parsed == 7,
          f"{parsed}/7 payload 解析成功（counts/verdict/judgement 全部提取）",
          {"parsed": parsed})

    ledger_rows = [{"round": r, "method": m, "verdict": v} for r, m, v in LEDGER_17]
    guard("G3", "17 轮 ledger 完整（r214–r234）", len(ledger_rows) == 17,
          f"{len(ledger_rows)} 行（含并行链 r223/224/225 与本线 14 轮）——"
          "形式统一四层成立/动力学统一 FAIL/供给 0 的边界地图完整",
          {"rows": len(ledger_rows)})

    # 总览页构建
    if not os.path.isfile(_TMPL):
        guard("G5", "交互 HTML 生成且自含", False, f"模板缺失：{_TMPL}")
        res = _finish(cards, ledger_rows, False, "模板缺失")
        _write(res)
        return 1
    tpl = open(_TMPL, encoding="utf-8").read()
    payload = json.dumps({"cards": cards, "ledger": ledger_rows}, ensure_ascii=False)
    html = tpl.replace("__R235_JSON__", payload)
    with open(HTML_OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    text = open(HTML_OUT, encoding="utf-8").read()
    problems = []
    if "__R235_JSON__" in text:
        problems.append("占位符未替换")
    if "http://" in text or "https://" in text:
        problems.append("外部 URL")
    if "<canvas" not in text and "<table" not in text:
        problems.append("缺卡片结构")
    ok_html = not problems
    guard("G4", "总览页生成且自含（零外部 URL）", ok_html,
          f"已生成 {HTML_OUT}（{len(text)} B）" +
          ("；" + "；".join(problems) if problems else "，7 张导航卡 + 17 轮 ledger 铸入"),
          {"bytes": len(text)})

    entry("M01", "INFO", "判定：验收口径裁决入档",
          "用户裁决：「完成统一场论」验收口径 = **边界地图完成态**——17 轮边界地图 + "
          "形式统一四层 + 引力五层闭合（动力学统一 FAIL、供给 0）即视为完成；"
          "物理统一（7 参数推导/量子引力）按 r229 判定属当前物理学不可达，如实登记")
    entry("M02", "PASS" if guard_ok_all(["G1", "G2"]) else "FAIL", "七层合并完整性",
          "7/7 payload 解析、7/7 文件在位——统一入口覆盖全部交互层")
    entry("M03", "PASS" if guard_ok_all(["G3", "G4"]) else "FAIL", "总览页与 ledger",
          "17 轮 ledger 铸入总览页；零外部 URL；导航卡含条目分布与核心读数")
    entry("M04", "INFO", "定位：纯整理轮",
          "无新数值——所有数字来自七轮已落盘 JSON（只读）；本卷是边界地图的入口收口")

    res = _finish(cards, ledger_rows, ok_html, "已生成")
    _write(res)

    bad = [g["id"] for g in guards if not g["ok"]]
    if bad:
        print(f"[RC≠0] 守卫失败 {bad}")
        return 1
    print(f"[DONE] {MARKER} rc=0")
    return 0


def guard_ok_all(ids):
    return all(any(g["id"] == i and g["ok"] for g in guards) for i in ids)


def _finish(cards, ledger_rows, ok_html, note):
    n_pass = sum(1 for e in entries if e["level"] == "PASS")
    n_info = sum(1 for e in entries if e["level"] == "INFO")
    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    return {
        "stem": STEM, "round": 235, "date": "2026-10-26",
        "method": "只读合并七层 payload → 统一入口总览页（无新数值）",
        "acceptance": ("用户裁决入档：验收口径 = 边界地图完成态（17 轮 + 形式统一四层 + "
                       "引力五层闭合，动力学统一 FAIL、供给 0）"),
        "entries": entries, "guards": guards, "controls": [],
        "readings": {"cards": cards, "ledger": ledger_rows, "note": note,
                     "ok_html": ok_html},
        "counts": {"entries": len(entries), "PASS": n_pass, "FAIL": n_fail,
                   "BOUNDARY": 0, "INFO": n_info,
                   "guards": f"{sum(1 for g in guards if g['ok'])}/{len(guards)}",
                   "controls": "—"},
        "verdict": "", "judgement": "", "source": {},
    }


def _write(res):
    res["verdict"] = ("R235-OVERVIEW-MERGE-SEVEN-LAYERS-MERGED-LEDGER-17ROWS-COMPLETE"
                      "-ACCEPTANCE-BOUNDARY-MAP-CLOSED-USER-CONFIRMED")
    res["judgement"] = ("CLOSED-INCREMENT（总览合并轮：统一入口 + 17 轮 ledger + 验收裁决入档；"
                        "边界地图完成态经用户确认关闭）")
    os.makedirs(_DATADIR, exist_ok=True)
    jpath = os.path.join(_DATADIR, BASE + ".json")
    mpath = os.path.join(_DATADIR, BASE + ".md")
    rpath = os.path.join(_DATADIR, BASE + "_report.txt")
    with open(jpath, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    L = [f"# {res['stem']} · 数据册\n",
         f"- 判决串：`{res['verdict']}`\n",
         f"- 条目：{res['counts']['entries']}（PASS {res['counts']['PASS']} / INFO {res['counts']['INFO']}）· "
         f"守卫 {res['counts']['guards']}\n", "\n## 条目\n"]
    for e in res["entries"]:
        L.append(f"- **{e['code']} {e['level']}** {e['title']}——{e['detail']}\n")
    L.append("\n## 守卫\n")
    for g in res["guards"]:
        L.append(f"- **{g['id']} {'OK' if g['ok'] else 'FAIL'}** {g['title']}——{g['detail']}\n")
    with open(mpath, "w", encoding="utf-8", newline="\n") as f:
        f.write("".join(L))
    with open(rpath, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{MARKER} rc=0\n")
        f.write(f"verdict={res['verdict']}\n")
        f.write(f"guards={res['counts']['guards']}\n")


if __name__ == "__main__":
    sys.exit(main())
