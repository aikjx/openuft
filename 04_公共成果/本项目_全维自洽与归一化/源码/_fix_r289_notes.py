# -*- coding: utf-8 -*-
"""r289 编号消歧补钉（幂等）：修正 README 取号叙述 + 数据说明/判定册加消歧节。"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
README = os.path.join(ROOT, "README.md")

OLD1 = "取号：三树实测 r287 已占、r289 空；**下轮从 r289 复查起**。"
NEW1 = ("取号：起草时实测 **r288 三树全空**；落盘前（23:41）复测 **r288 已被并行会话同题占用**"
        "（`TUFT-r288_高维几何与电磁耦合第一性原理审计_…`）⇒ 按「后到者整体改号、不改他人字节」纪律"
        "**整体改号 r289**；该并行卷随后亦改号 **r290**（让出 r289），两卷构成 **r289 / r290 同题双审**"
        "（r290 视角＝KK 规范变换 / 曲率分解系数 / 半径模与 radion 反作用；本卷视角＝排除定理的自由度性质 / "
        "真空能量级 / 随机测试判别力）。**下轮从 r291 复查起**。")

OLD2 = ("- **取号**：2026-10-31 23:3x 三树实测 **r287 已占**（V10 §七 可行性否证）、**r289 三树全空**"
        "（src/json/md/report 均 0、README 锚 0、判定锚 0）⇒ 取 **r289**。"
        "**下轮从 r289 复查起（并行链活跃，取号前必扫）**。")
NEW2 = ("- **取号**：起草时实测 **r288 三树全空**（src/json/md/report 均 0、README 锚 0、判定锚 0）；"
        "落盘前（23:41）复测 **r288 已被并行会话同题占用**（`TUFT-r288_高维几何与电磁耦合第一性原理审计_…`，"
        "引擎 23:39 / 数据 23:41 落盘）⇒ 按「后到者整体改号、不改他人字节」纪律**整体改号 r289**，"
        "**未触碰 r288 任何字节**；该并行卷随后亦整体改号 **r290**（让出 r289），故最终形成 "
        "**r289 / r290 同题双审**：r290 视角＝KK 规范变换 / 曲率分解系数 / 半径模与 radion 反作用；"
        "本卷视角＝排除定理的自由度性质（快子唯一解）/ 真空能量级 / 随机测试判别力。"
        "**下轮从 r291 复查起（并行链活跃，取号前必扫）**。")

NOTE_SECTION = """
## 附 · 编号消歧（撞号第 N 次）

本卷起草时实测 **r288 三树全空**；落盘前（2026-10-31 23:41）复测发现 **r288 已被并行会话同题占用**
（`TUFT-r288_高维几何与电磁耦合第一性原理审计_KK规范变换与曲率分解系数验证_…`，引擎 23:39、数据 23:41）。
按「已产四件套并登记者为权威、后到者整体改号」纪律，本卷**整体改号 r289**，未触碰 r288 任何字节；
该并行卷随后亦整体改号 **r290**（让出 r289）。

最终两卷构成 **r289 / r290 同题双审**：

| 卷 | 视角 | 侧重点 |
|---|---|---|
| r289（本卷） | 排除定理的**自由度性质** | 2 参数对 2 观测的唯一解是快子 / 真空能 9.74e116 / 随机测试判别力 |
| r290（并行卷） | **几何结构** | KK 规范变换 / 曲率分解系数 / 半径模与质量矛盾 / radion 反作用 |

**下轮从 r291 复查起**。
"""


def patch_readme():
    with open(README, "r", encoding="utf-8") as f:
        s = f.read()
    hit = 0
    for o, n in ((OLD1, NEW1), (OLD2, NEW2)):
        if o in s:
            s = s.replace(o, n, 1)
            hit += 1
        else:
            print("[readme] NOT FOUND:", o[:36])
    if hit:
        with open(README, "w", encoding="utf-8") as f:
            f.write(s)
    print("[readme] replaced", hit)


def patch_md(path, anchor):
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
    if "编号消歧（撞号" in s:
        print("[md] already patched:", os.path.basename(path)[:40])
        return
    if anchor not in s:
        print("[md] ANCHOR MISS:", os.path.basename(path)[:40])
        return
    s = s.replace(anchor, anchor + NOTE_SECTION, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("[md] patched:", os.path.basename(path)[:40])


def main():
    patch_readme()

    d = os.path.join(ROOT, "数据")
    j = os.path.join(ROOT, "判定")
    data_md = [f for f in os.listdir(d) if f.startswith("TUFT-r289_") and f.endswith("_2026-10-31.md")
               and "来料原件" not in f]
    jud_md = [f for f in os.listdir(j) if f.startswith("判定_TUFT-r289_")]
    if data_md:
        patch_md(os.path.join(d, data_md[0]), "## 九、分层声明")
    if jud_md:
        patch_md(os.path.join(j, jud_md[0]), "---\n\n**最终一句**")

    # 读回验证
    with open(README, "r", encoding="utf-8") as f:
        disk = f.read()
    print("[verify] 下轮从 r291 出现:", disk.count("下轮从 r291"))
    print("[verify] r288 计数:", disk.count("r288"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
