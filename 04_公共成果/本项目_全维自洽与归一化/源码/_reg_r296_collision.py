# -*- coding: utf-8 -*-
# r296 编号碰撞消歧登记（纯追加，不改任何既有字节）
import io, os, re, shutil, collections

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RD = os.path.join(BASE, "README.md")
BAK = os.path.join(BASE, "_backup", "README.bak_r296b_2026-11-01.md")

with io.open(RD, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")
orig = list(lines)

# 备份（首次创建不覆盖）
if not os.path.exists(BAK):
    shutil.copy2(RD, BAK)
    print("备份已建：", BAK)
else:
    print("备份已存在（不覆盖）：", BAK)

# 幂等：若消歧条已存在则跳过
marker = "r296 编号碰撞消歧"
if any(marker in ln for ln in lines):
    print("消歧条已存在，跳过")
else:
    block = [
        "",
        "### r296 编号碰撞消歧 · 2026-11-01（治理注，非独立卷）",
        "",
        "- **事实（时间戳证据）**：本目录出现**三份**使用编号 r296 的源码文件——",
        "  1. `源码/TUFT-r296_磁通手征谱可实现方程_多U1推广与充要判据与千组随机负对照_精算与可视化_2026-11-01.py`（**03:57**，本卷，四件套 + 判定册 + README 四处注册齐备）；",
        "  2. `源码/TUFT-r296_KK电磁耦合链求导证明验证精算_符号多项式Christoffel与非平坦背景曲率分解_EL变分导出Maxwell与光子质量零定理_正负对照_2026-11-01.py`（**04:00**，并行会话，**仅源码，无数据/判定/报告配套，未注册**）；",
        "  3. `源码/TUFT-r296_六维EinsteinMaxwell完整框架终局审计_Einstein框架势幂次与FreundRubin极小与Minkowski微调与α自由参数定理_精算与可视化_2026-11-01.py`（**04:01**，并行会话，**仅源码，无配套，未注册**）。",
        "- **处置（后到者整体改号）**：按「**先到者保号、后到者整体改号、不改他人任何字节**」纪律，**本卷（03:57）保留 r296**；上列第 2、3 两份属**后到未成型草稿**，本轮**不触碰其任一字节**，改号由其归属会话自行完成（建议顺延至 r297 / r298，落盘前须重扫三树；本卷登记时 r297 指针已被占用预告，**实际取号前必须实测**）。",
        "- **连带风险**：README 中「r296」四处锚点目前**唯一指向本卷**（磁通手征谱 FCSRE），检索/引用时请以**完整文件名**区分，勿仅凭编号定位。",
        "- **本条性质**：**纯治理登记**，不含任何物理判定、不计入条目数、不占度数、不改变任何判词。",
    ]
    # 保证末尾有换行
    if lines and lines[-1].strip() != "":
        lines.append("")
    lines.extend(block)
    with io.open(RD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("消歧条已追加，新增", len(block), "行")

# 校验：零删除
with io.open(RD, "r", encoding="utf-8") as f:
    new = f.read().split("\n")
c_old = collections.Counter(l for l in orig if l.strip())
c_new = collections.Counter(l for l in new if l.strip())
lost = c_old - c_new
print("删除行检查：备份", len(orig), "→ 新版", len(new), "行；丢失行种类", len(lost))
for k, v in list(lost.items())[:5]:
    print("   LOST:", v, k[:80])

# 逐 RID 清点
txt = "\n".join(new)
for anchor in ["TUFT-r296_磁通手征谱", "判定_TUFT-r296_", "- **r296（", "### r296 · "]:
    print("清点 %-28s = %d" % (anchor, txt.count(anchor)))
print("消歧条 =", txt.count(marker))
