# -*- coding: utf-8 -*-
"""
_batch_20261029_apply.py
=========================
清尾批登记脚本（引擎全部完成后运行）：
 1) 母册：593 行状态转换（读 _batch_20261029_row_edits.json）+
    行17/18/20 口径更新 + 行1314/1315 终局表 + §三 补清尾批块 + §四 收口 + 行1312 附注
 2) README：目录表 10×4 行（读 10 个引擎 JSON 自动生成）+
    母册行 268 编号 + 快照注 283 项判定 + 进度区 10 条 + 归档配套册表加评估册行
全程 UTF8Encoding($false) 直读直写；每步断言替换唯一性。
"""
import json, io, re, sys, os

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_统一场论攻破"
MASTER = os.path.join(ROOT, "布局_物理Top1000难题攻破清单_2026-10-21.md")
README = os.path.join(ROOT, "README.md")
EDITS = os.path.join(ROOT, "_batch_20261029_row_edits.json")

NEW_NUMBERS = ["C0392", "C0393", "C0394", "C0395", "C0396",
               "C0397", "C0398", "C0399", "C0400", "C0401"]
# C 号 -> (主名, T 行, 域, 撞C, 判定册读数摘要)
META = {
    "C0392": ("BransDickePPNγ攻破", "T167", "G", "C2/C3",
              "PPN γ=(1+ω)/(2+ω)、Cassini |γ−1|=2.4999e-5<2.5e-5、dγ/dω=1/(2+ω)²>0"),
    "C0393": ("FierzPauli_vDVZ攻破", "T171", "G", "C1/C7",
              "vDVZ 势 4/3 倍、偏折 3/4 倍、缺额 1/4 不连续（lim≠连续）"),
    "C0394": ("GaussBonnet四维拓扑攻破", "T126", "G", "C1/C5",
              "∫GB(S⁴)=64π²=32π²χ、4D 变分恒零（拓扑）、Lovelock 唯一 GR"),
    "C0395": ("GPB进动攻破", "T193", "G", "C5",
              "测地 6.6″/yr、系拖拽 0.041″/yr（GR 标准值，实测偏差<1.5%）"),
    "C0396": ("自旋2四极辐射攻破", "T208", "G", "C1/C5",
              "四极 P=32G⁴m₁²m₂²M/5c⁵a⁵、d lnP/d ln a=−5、Hulse-Taylor Ṗ_b 符合 0.1%"),
    "C0397": ("freezein暗物质丰度攻破", "T414", "I", "C1/C3",
              "Y=45g₁y²M_Pl/(32π⁵g_*S·m₁)、Ωh²=0.12 需 y≈2.88e-11（m₁=1TeV、实算调定）"),
    "C0398": ("Kaup玻色子星攻破", "T308", "H", "C1/C7",
              "M_max=0.633M_Pl²/m：QCD 轴子 m=1e-5 eV → 1.68e25 kg≈8.5e-6 M☉（m=1 eV 参考 1.68e20 kg≈8.5e-11 M☉）、d lnM/d ln m=−1"),
    "C0399": ("BBN氦丰度攻破", "T431", "I", "C2",
              "(n/p)_f=e^{−Q/T_f}、Y_p=2x/(1+x)、dY_p/dT_f>0、解析精度内含观测 0.245"),
    "C0400": ("phantom幽灵稳定性攻破", "T483", "I", "C7/C1",
              "w=(x+1)/(x−1)、w<−1⟺0<x<1、dw/dx=−2/(x−1)²<0、幽灵不稳定"),
    "C0401": ("三能级量子热机攻破", "T536", "J", "C5/C7",
              "η_C=1−T_c/T_h=2/3、η_CA=1−√(T_c/T_h)=0.42265、dη_CA/dr=−1/(2√r)<0"),
}

CHAIN_ADD = (" + C0392/C0393/C0394/C0395 补 4 + C0396/C0397/C0398/C0399 补 4 + C0400/C0401 补 2")
BUJI_21 = ("另 2026-10-29 清尾批补记 21 项（含于既有编号，不新增编号）："
           "T039→C0145、T041→C0144、T043→C0146、T046→C0144、T051→C0143、T111→C0208、"
           "T139→C0271、T148→C0171、T197→C0167、T200→C0273、T218→C0141、T219→C0214、"
           "T241→C0143、T269→C0243、T291→C0186、T309→C0231、T402→C0177、T411→C0197、"
           "T423→C0177、T543→C0255、T544→C0250。")

def rep1(text, old, new, what):
    n = text.count(old)
    assert n == 1, f"[{what}] 期望唯一匹配，实际 {n}：{old[:80]}..."
    return text.replace(old, new)

def load_engine_json(cid):
    meta = META[cid]
    p = os.path.join(ROOT, f"attack_{cid}_{meta[0]}_2026-10-29.json")
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)

def main():
    # ---------- 母册 ----------
    mtxt = io.open(MASTER, encoding="utf-8").read()
    edits = json.load(io.open(EDITS, encoding="utf-8"))
    # 1) 行状态转换
    for t, e in edits.items():
        n = mtxt.count(e["old"])
        assert n == 1, f"行 {t} 原行唯一性失败: {n}"
        mtxt = mtxt.replace(e["old"], e["new"])
    # 2) 行20 链尾 + 累计判定
    mtxt = rep1(mtxt, "C0388/C0389/C0390/C0391 补 4 = **258 个编号**",
                "C0388/C0389/C0390/C0391 补 4" + CHAIN_ADD + " = **268 个编号**", "行20链尾")
    mtxt = rep1(mtxt, "累计判定 273 项（258 编号 + 4 深化 + 8 元层）",
                "累计判定 283 项（268 编号 + 4 深化 + 8 元层 + 3 深化附册）", "行20累计判定")
    # 3) 行17/18 总账
    mtxt = rep1(mtxt, "| 其中待攻 | 见 §四 | 🔲 按序推进 |",
                "| 其中待攻 | 2026-10-29 清尾批全量评估后清零（可精算/含于全清，余 C 级登记不深攻） | ✅ 收口（见评估册） |", "行17")
    mtxt = rep1(mtxt, "登记在册（域 J/L/P 为主）", "登记在册（域 J/L/P/O 为主）", "行18")
    # 4) 行1314 终局表
    mtxt = rep1(mtxt, "C0388/C0389/C0390/C0391 补 4）",
                "C0388/C0389/C0390/C0391 补 4" + CHAIN_ADD + "）", "行1314链尾")
    mtxt = rep1(mtxt, "258 个编号结构性负面闭合（基线 24",
                "268 个编号结构性负面闭合（基线 24", "行1314计数")
    # 5) 行1315 下一步
    mtxt = rep1(mtxt, "| 下一步 | 待攻队列 §四 按 Phase 推进；先攻 T005/T014/T026 |",
                "| 下一步 | 2026-10-29 清尾批已收口：593 项全量评估（10 新编号 + 21 补记 + 3 深化附册 + 559 C 级登记），可精算项清零；域 O 观测层按惯例登记不硬攻 |", "行1315")
    # 6) 行1312 附注（求导深化册行）
    mtxt = rep1(mtxt, "| 求导深化册判定 | C0156–C0159 共 4 项（引用式→第一性原理求导升级，裁定不变，不新增物理难题编号） |",
                "| 求导深化册判定 | C0156–C0159 共 4 项（引用式→第一性原理求导升级，裁定不变，不新增物理难题编号）；2026-10-29 清尾批新增求导深化附册 3 项（T392/T479/T484，登记不深攻，见评估册 §三） |", "行1312")
    # 7) §三 补清尾批块（插在 §四 标题前）
    san = "\n### 2026-10-29 清尾批 10 个编号（C0392–C0401，mpmath 250 位）\n"
    san += "| T 项 | 对象 | 判定号 | 读数 |\n|---|---|---|---|\n"
    for cid in NEW_NUMBERS:
        m = META[cid]
        san += f"| {m[1]} | {m[0].replace('攻破','')} | **{cid}** | {m[4]} ⟹ **{m[1]} 结构性负面**（撞 {m[3]}） |\n"
    san += "\n### 2026-10-29 清尾批 补记 21 项（含于既有编号，不新增编号）\n"
    san += "| T 项 | 补记父编号 | 依据 |\n|---|---|---|\n"
    buji = [(t, p) for t, p in sorted(json.load(io.open(EDITS, encoding="utf-8")).items()) if p["bucket"] == "J"]
    for t, p in buji:
        san += f"| {t} | {p['payload']} | 含于既有攻破编号（{p['name']}） |\n"
    san += "\n"
    mtxt = rep1(mtxt, "## 四、待攻队列（Phase 顺序，供后续分片参考）", san + "## 四、待攻队列（2026-10-29 清尾批后已收口）", "§三插块")
    # 8) §四 内容收口：整表替换为收口说明
    mtxt = rep1(mtxt, "| 序 | 编号 | 难题 | 备注 |\n|---|---|---|---|\n| 1 | T005 | 时空量子起源 / 离散性 | 基线余项，前置 T001（已攻） |\n| 2 | T014 | 全息原理 / 面积熵律 | 基线余项，可承接 C0148 |\n| 3 | T026 | 质子衰变实验 | 基线余项，承接 C0147 |\n| 4 | T008 | 奇点定理 | 基线余项，承接 attack24 |\n| 5 | T006 | 时间之箭 | 基线余项 |\n| 6 | T013 | 时空维数为何 4 | 基线余项，承接 attack24 N2 |\n| 7 | T016 | 时间旅行/因果闭合 | 基线余项 |\n| 8 | T028/T029/T030 | 暗光子/轴子/禁闭 | 基线余项 |\n| 9 | T032/T033/T034 | 质量谱/新物理/规范统一 | 基线余项 |\n| 10 | T040–T052 | 域 C 剩余 | 基线余项（多含于已攻项） |\n| 11 | T101+ | 扩展域 G–P | 按域分批，遇几何载体即攻 |\n| 12 | T067+ | 域 E/K/P ⚠️ 项 | 登记不深攻 |",
                "> 清尾批（2026-10-29）已全量评估 593 项：可精算 10（C0392–C0401 四件套）/ 含于补记 21 / 深化附册 3 / C 级登记 559（观测依赖·诠释层·纯数学·理论开放·域 O 观测层）。可精算项清零，无剩余待攻队列；C 级登记不深攻，不硬造闭合。详见 布局_剩余593项_全量评估与攻破登记_2026-10-29.md。", "§四收口")
    io.open(MASTER, "w", encoding="utf-8").write(mtxt)

    # ---------- README ----------
    rtxt = io.open(README, encoding="utf-8").read()
    # 1) 目录表：40 行（10×4），插在 C0391 判定册行之后
    blocks = []
    for cid in NEW_NUMBERS:
        m = META[cid]
        js = load_engine_json(cid)
        guards = js.get("guards", [])
        gp = sum(1 for g in guards if g.get("passed"))
        rc = js.get("exit_code")
        fn = f"attack_{cid}_{m[0]}_2026-10-29"
        blocks.append(
            f"| [`{fn}.py`]({fn}.py) | {m[0]}引擎（T{m[1][1:]} 域 {m[2]}·清尾批；{m[0]}；mpmath 250 位；守卫 **{gp}/{len(guards)}**、rc {rc}） |\n"
            f"| [`{fn}_report.txt`]({fn}_report.txt) | {m[0]} 运行报告 |\n"
            f"| [`{fn}.json`]({fn}.json) | {m[0]} 数据（{m[0]} 读数） |\n"
            f"| [`判定_{cid}_{m[0]}_2026-10-29.md`](判定_{cid}_{m[0]}_2026-10-29.md) | 判定册（T{m[1][1:]}）：{m[4]}⟹ **T{m[1][1:]} 结构性负面**（撞 {m[3]}） |")
    anchor = "| [`判定_C0391_X6900四夸克攻破_2026-10-21.md`](判定_C0391_X6900四夸克攻破_2026-10-21.md) | 判定册（T340）：Δ=**706.2 MeV**、Δ/Γ=**5.79**⟹ **T340 结构性负面**（撞 C1/C5） |"
    rtxt = rep1(rtxt, anchor, anchor + "\n" + "\n".join(blocks), "README目录表插块")
    # 2) 母册行 258→268 + 链尾
    rtxt = rep1(rtxt, "已攻破 **258 个编号**", "已攻破 **268 个编号**", "README母册行计数")
    rtxt = rep1(rtxt, "C0388/C0389/C0390/C0391 补 4；C0185 为元层不计编号",
                "C0388/C0389/C0390/C0391 补 4" + CHAIN_ADD + "；C0185 为元层不计编号；" + BUJI_21.replace("另 ", ""), "README母册行链尾")
    # 3) 快照注
    rtxt = rep1(rtxt, "C0153–C0391 后累计 273 项判定（258 编号 + 4 求导深化 + 元层 C0152/C0161/C0162/C0166/C0167/C0168/C0176/C0185）",
                "C0153–C0401 后累计 283 项判定（268 编号 + 4 求导深化 + 3 深化附册 + 元层 C0152/C0161/C0162/C0166/C0167/C0168/C0176/C0185）", "README快照注")
    # 4) 进度区：10 条，插在 C0391 进度行后
    prog = []
    for cid in NEW_NUMBERS:
        m = META[cid]
        js = load_engine_json(cid)
        guards = js.get("guards", [])
        gp = sum(1 for g in guards if g.get("passed"))
        rc = js.get("exit_code")
        prog.append(
            f"- [x] {m[0]}（{cid} · Top1000 {m[1]} · 域 {m[2]}）：判定册 [`判定_{cid}_{m[0]}_2026-10-29.md`](判定_{cid}_{m[0]}_2026-10-29.md) + 引擎 `attack_{cid}_{m[0]}_2026-10-29.py`（守卫 **{gp}/{len(guards)}**、rc {rc}）——{m[4]}⟹ **{m[1]} 结构性负面**（撞 {m[3]}）")
    anchor2 = "- [x] X(6900) 四夸克（C0391 · Top1000 T340 · 域 F）：判定册 [`判定_C0391_X6900四夸克攻破_2026-10-21.md`](判定_C0391_X6900四夸克攻破_2026-10-21.md) + 引擎 `attack_C0391_X6900四夸克攻破_2026-10-21.py`（守卫 **4/4**、rc 0）——Δ/Γ=**5.79**⟹ **T340 结构性负面**（撞 C1/C5）"
    rtxt = rep1(rtxt, anchor2, anchor2 + "\n" + "\n".join(prog), "README进度区插块")
    io.open(README, "w", encoding="utf-8").write(rtxt)
    print("APPLY OK: master + README 已更新")

if __name__ == "__main__":
    main()
