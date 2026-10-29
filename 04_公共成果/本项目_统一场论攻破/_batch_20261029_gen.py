# -*- coding: utf-8 -*-
"""
_batch_20261029_gen.py
=======================
读 _todo_rows_extract.txt + _batch_20261029_classify.py，
生成：
 1) 布局_剩余593项_全量评估与攻破登记_2026-10-29.md（全量评估结论）
 2) _batch_20261029_row_edits.json（母册行替换数据：T -> {old, new, bucket}）
"""
import json, io, re, sys, os

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"
sys.path.insert(0, ROOT)
import _batch_20261029_classify as CLS

EXTRACT = os.path.join(ROOT, "_todo_rows_extract.txt")
OUT_MD = os.path.join(ROOT, "布局_剩余593项_全量评估与攻破登记_2026-10-29.md")
OUT_JSON = os.path.join(ROOT, "_batch_20261029_row_edits.json")

# 可精算行读数（母册行状态单元格内容）
READINGS = {
    "C0392": "PPN γ=(1+ω)/(2+ω)、Cassini |γ−1|=2.4999e-5<2.5e-5、dγ/dω=1/(2+ω)²>0、ω 自由参数、TUFT 供给 0，撞 C2/C3",
    "C0393": "vDVZ 势 4/3 倍、偏折 3/4 倍、缺额 1/4 不连续（lim≠连续）、TUFT 供给 0，撞 C1/C7",
    "C0394": "∫GB(S⁴)=64π²=32π²χ(S⁴)、4D 变分恒零（拓扑）、Lovelock 唯一 GR，TUFT 供给 0，撞 C1/C5",
    "C0395": "测地 Ω_g=6.6″/yr、系拖拽 Ω_LT=0.041″/yr（GR 标准值，实测偏差<1.5%），TUFT 供给 0，撞 C5",
    "C0396": "自旋-2 四极 P=32G⁴m₁²m₂²M/5c⁵a⁵、d lnP/d ln a=−5、Hulse-Taylor Ṗ_b 符合 0.1%，TUFT 供给 0，撞 C1/C5",
    "C0397": "freeze-in Y=45g₁y²M_Pl/(32π⁵g_*S·m₁)、Ωh²=0.12 需 y≈2.88e-11（m₁=1TeV、实算调定）、幂律 2，TUFT 供给 0，撞 C1/C3",
    "C0398": "Kaup M_max=0.633M_Pl²/m：QCD 轴子 m=1e-5 eV → 1.68e25 kg≈8.5e-6 M☉（m=1 eV 参考点 1.68e20 kg≈8.5e-11 M☉）、d lnM/d ln m=−1，TUFT 供给 0，撞 C1/C7",
    "C0399": "BBN 解析 (n/p)_f=e^{−Q/T_f}、Y_p=2x/(1+x)、dY_p/dT_f>0、与观测 0.245 在解析精度内，TUFT 供给 0，撞 C2",
    "C0400": "phantom w=(x+1)/(x−1)、w<−1⟺0<x<1、dw/dx=−2/(x−1)²<0、幽灵不稳定（H 无下界），TUFT 供给 0，撞 C7/C1",
    "C0401": "η_C=1−T_c/T_h=2/3、η_CA=1−√(T_c/T_h)=0.42265、dη_CA/dr=−1/(2√r)<0，TUFT 供给 0，撞 C5/C7",
}

DOMAIN_NAME = {
    "G": "G·引力扩展", "H": "H·粒子物理", "I": "I·宇宙学扩展", "J": "J·量子基础扩展",
    "K": "K·凝聚态扩展", "L": "L·量子场论扩展", "M": "M·核物理/QGP", "N": "N·AMO",
    "O": "O·天体观测", "A": "A·量子引力", "B": "B·粒子物理", "C": "C·宇宙学",
    "D": "D·量子基础", "E": "E·凝聚态", "F": "F·数学物理",
}

def parse_rows(txt):
    rows = []
    for line in txt.splitlines():
        m = re.match(r"^\| (T\d{3}) \| (.*?) \| (.*?) \| (.*?) \| (🔲[^|]*) \|$", line)
        if m:
            rows.append({"t": m.group(1), "name": m.group(2).strip(),
                         "mech": m.group(3).strip(), "coll": m.group(4).strip(),
                         "status": m.group(5).strip(), "orig": line})
    return rows

def new_status(row, bucket, payload):
    t = row["t"]
    if bucket == "A":
        return "✅ **%s**：%s" % (payload, READINGS[payload])
    if bucket == "J":
        return "✅（含于 %s）" % payload
    if bucket == "D":
        return "⚠️ 观测依赖（理论闭式求导已深化入评估册 §三）"
    return "⚠️ %s" % payload

def main():
    txt = io.open(EXTRACT, encoding="utf-8").read()
    rows = parse_rows(txt)
    assert len(rows) == 593, len(rows)
    edits = {}
    for r in rows:
        bucket, payload = CLS.classify(r["t"])
        ns = new_status(r, bucket, payload)
        # 仅替换最后状态单元格，保留其余单元格原文
        head, _, tail = r["orig"].rpartition("|")
        # tail 形如 " 🔲... |"，status cell 前有空格
        newline = r["orig"].replace(r["status"], ns, 1)
        edits[r["t"]] = {"old": r["orig"], "new": newline, "bucket": bucket,
                         "payload": payload, "name": r["name"]}
    io.open(OUT_JSON, "w", encoding="utf-8").write(
        json.dumps(edits, ensure_ascii=False, indent=1))

    # ---- 评估册 ----
    by_bucket = {}
    for r in rows:
        b, _ = CLS.classify(r["t"])
        by_bucket.setdefault(b, []).append(r)
    A = [r for r in by_bucket.get("A", [])]
    J = sorted(by_bucket.get("J", []), key=lambda r: r["t"])
    D = sorted(by_bucket.get("D", []), key=lambda r: r["t"])
    C = sorted(by_bucket.get("C", []), key=lambda r: r["t"])
    out = []
    out.append("# 布局_剩余593项_全量评估与攻破登记_2026-10-29.md")
    out.append("")
    out.append("> 清尾批（2026-10-29）· 母册剩余 593 项 🔲 全量评估结论 + 攻破登记。")
    out.append("> 口径：可精算（四件套）/ 含于补记 / 深化附册 / C 级登记不深攻；红线四句全程保持。")
    out.append("")
    out.append("## 〇 总览")
    out.append("")
    out.append("| 桶 | 数 | 处置 |")
    out.append("|---|---|---|")
    out.append("| A 可精算 | %d | 新编号 C0392–C0401 四件套，行 🔲→✅ |" % len(A))
    out.append("| J 含于补记 | %d | 补记既有编号（不新增编号），行 🔲→✅ |" % len(J))
    out.append("| D 深化附册 | %d | 理论闭式求导分析（见 §三），行 🔲→⚠️ 登记 |" % len(D))
    out.append("| C 级登记 | %d | 观测依赖/诠释层/纯数学/理论开放，行 🔲→⚠️ 登记不深攻 |" % len(C))
    out.append("| 合计 | %d | |" % len(rows))
    out.append("")
    out.append("## 一 可精算项读数表（C0392–C0401）")
    out.append("")
    out.append("| 编号 | 母册行 | 核心闭式读数 | 撞 C | 求导验证 |")
    out.append("|---|---|---|---|---|")
    for r in A:
        cid = CLS.classify(r["t"])[1]
        out.append("| %s | %s · %s | %s | %s | 见判定册 E3（求导链+数值互验） |" % (cid, r["t"], r["name"], READINGS[cid], r["coll"]))
    out.append("")
    out.append("## 二 含于补记项（21，行 🔲→✅，不新增编号）")
    out.append("")
    out.append("| 行 | 名称 | 补记父编号 | 依据 |")
    out.append("|---|---|---|---|")
    for r in J:
        parent = CLS.classify(r["t"])[1]
        out.append("| %s | %s | %s | 含于既有攻破编号 |" % (r["t"], r["name"], parent))
    out.append("")
    out.append("## 三 求导深化附册（3，行 🔲→⚠️ 登记）")
    out.append("")
    for r in D:
        payload = CLS.classify(r["t"])[1]
        out.append("### %s · %s" % (r["t"], r["name"]))
        out.append("")
        out.append("> %s" % payload)
        out.append("")
    out.append("## 四 C 级登记全表（%d，行 🔲→⚠️ 登记不深攻）" % len(C))
    out.append("")
    out.append("| 行 | 名称 | 分类 | 理由 |")
    out.append("|---|---|---|---|")
    for r in C:
        b, payload = CLS.classify(r["t"])
        out.append("| %s | %s | C级 | %s |" % (r["t"], r["name"], payload))
    out.append("")
    out.append("## 五 批次登记")
    out.append("")
    out.append("- 母册：31 行 🔲→✅（10 新编号 + 21 补记）；%d 行 🔲→⚠️；行 20 口径注追加；行 1314 终局表更新。" % len(C))
    out.append("- README：目录表 10 编号 × 4 行、母册行、快照注、进度区 10 条同步。")
    out.append("- 详情见批次回传表。")
    out.append("")
    out.append("## 六 最终快照（登记后）")
    out.append("")
    out.append("| 指标 | 值 |")
    out.append("|---|---|")
    out.append("| T 行总数 | 1037 |")
    out.append("| ✅ | %d |" % (260 + len(A) + len(J)))
    out.append("| ⚠️ | %d |" % (148 + len(D) + len(C)))
    out.append("| 🔲 | %d |" % (593 - len(A) - len(J) - len(D) - len(C)))
    out.append("| ◐ | 1 |")
    out.append("| OTHER | 38 |")
    out.append("")
    io.open(OUT_MD, "w", encoding="utf-8").write("\n".join(out))
    print("GEN OK rows=%d A=%d J=%d D=%d C=%d" % (len(rows), len(A), len(J), len(D), len(C)))
    print("MD:", OUT_MD)
    print("EDITS:", OUT_JSON)

if __name__ == "__main__":
    main()
