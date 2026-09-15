# -*- coding: utf-8 -*-
"""把「第一性冲突」登记写入受影响体系的 11_证伪与反例 与 claims.csv。

可复跑：幂等——重复执行不会重复追加（按 claim_id 去重）；
README 末句按「本阶段产物：」锚点幂等替换。

用法：python 登记冲突到体系.py
"""

import io
import os
import re
import sys
import json

sys.stdout.reconfigure(encoding="utf-8", errors="replace") if hasattr(sys.stdout, "reconfigure") else None

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SYSTEMS = os.path.join(ROOT, "01_独立体系")

RECORD = "11_证伪与反例/普朗克锚定谬误冲突记录.md"
RECORD_MOMENTUM = "11_证伪与反例/统一动量低速极限冲突记录.md"

# 体系 -> [(claim_id, statement, assumptions, derivation, uncertainty)]
# hypothesis_revision 从各体系 system.json 自动读取，避免硬编码漂移。
CLAIMS = {
    "S07_GAQ复曲率融合体系": [
        ("S07-C0001",
         "【冲突】普朗克锚定谬误：A3（κ²+τ²=1/R²）与 G=c³/(ℏ(κ²+τ²)) 联立推出 R=ℓ_P 且 m=m_P 唯一解"
         "——与 m_p/m_e=1836.15 冲突 1835.15 倍；根因为普朗克尺度恒等式（m=m_P 时 α_grav=1）"
         "被误用为任意粒子关系式",
         "S07-A3;派生式 G=c³/(ℏ(κ²+τ²));派生式 m=ℏ/(cR)", RECORD,
         "引擎 M01-n 残差 1835.15（FAIL）；M02-n α_grav=(m_e/m_P)² 残差 1.69e-81（PASS）"),
    ],
    "S08_GAQ常数几何化体系": [
        ("S08-C0001",
         "【冲突】普朗克锚定谬误（继承 v4）：A2（κ²+τ²=1/R²）与 G 式联立推出 m=m_P 唯一解"
         "——与 m_p/m_e=1836.15 冲突 1835.15 倍",
         "S08-A2;派生式 G=c³/(ℏ(κ²+τ²))", RECORD,
         "引擎 M01-n 残差 1835.15（FAIL）"),
        ("S08-C0002",
         "【误置】c=ωR 与 ħ=mcR 把 SI 定义常数（c、h 为精确值且不确定度为零）当作几何化成就；"
         "自然单位下二者归一为 1，不构成物理预言；归一化后仍剩 α 与 m/m_P 两个外部无量纲输入",
         "S08-A3;S08-A4", RECORD,
         "引擎 H04 归一化后自由度=2；D10 无量化判据"),
    ],
    "S09_GAQ粒子质量谱体系": [
        ("S09-C0001",
         "【冲突】质量谱派生链被普朗克锚定污染：继承 v5/v4 的 G 式与 m 式联立只能给出 m=m_P 唯一解，"
         "故任何由其推出 m_p/m_e 或 m_τ/m_e 的构造必然系统性失败（既有 27.1.4 偏差 40%–2000%）；"
         "另归一化后 κ̃ 与 τ̃ 与质量无关，本源方程不携带质量信息",
         "S09-A1;S09-A2;S09-A3;派生链（继承 v5）", RECORD,
         "引擎 C02 六粒子残差 2.1e-81（正因与质量无关）；M04；H04 自由度 2"),
    ],
    "S10_频率本源与复螺旋宇宙": [
        ("S10-C0001",
         "【冲突】派生关系 G=c³/(ℏ(κ²+τ²)) 与 m=ℏ√(κ²+τ²)/c 联立推出 Gm²=ℏc 即 m=m_P 唯一解；"
         "电子锚点下该式给出 ℏc/m_e²=3.81e+34，与实测 G 差 5.71e+44 倍（约 44 个数量级），"
         "而普朗克锚点残差仅 1.84e-81",
         "S10-A1;S10-A2;S10-A3", RECORD,
         "引擎 D06（FAIL 5.71e+44）与 D07（PASS 1.84e-81）同式双锚点对照"),
    ],
    "S02_空间光速螺旋统一力": [
        ("S02-C0001",
         "【冲突】统一动量 P=m(c−v) 在 v=0 时给出 P=mc≠0（电子 2.73e-22 kg·m/s），"
         "且 m、c 恒定时 F=dP/dt=−ma 与牛顿 F=+ma 反号；恢复 F=+ma 所需前提"
         "（c 的数学身份、dm/dt 项或低速退化条件）均未在公设中声明",
         "S02-A1;S02-A2", RECORD_MOMENTUM,
         "引擎 M03-n 登记 P(0)=m_e c=2.73e-22 kg·m/s；低速极限符号冲突未量化阈值"),
    ],
    "S12_空间光速螺旋统一体系": [
        ("S12-C0006",
         "【冲突】借用项 S12-A4（P=m(c−v)）带入低速极限冲突：v=0 时 P=mc≠0，F=dP/dt=−ma 与牛顿反号；"
         "又因本体 A2 要求 v≡c，若 v 指内部速度则 P≡0 且 F≡0，与四力分解初衷冲突"
         "——本体与借用动力学的接口未定义",
         "S12-A2;S12-A4（借用 s02_light_speed_helix_force）", RECORD_MOMENTUM,
         "引擎 M03；本体公设与动力学接口无量化判据"),
    ],
}

# 体系 -> README 末句替换后的产物句
README_TAIL = {
    "S07_GAQ复曲率融合体系":
        "本阶段产物：[普朗克锚定谬误冲突记录](普朗克锚定谬误冲突记录.md)"
        "（S07-C0001，内部冲突；A3 与 G 式联立推出 m=m_P，与 m_p/m_e=1836.15 冲突 1835.15 倍）。",
    "S08_GAQ常数几何化体系":
        "本阶段产物：[普朗克锚定谬误冲突记录](普朗克锚定谬误冲突记录.md)"
        "（S08-C0001 内部冲突：m=m_P 唯一解；S08-C0002 方向误置：c、ħ 为 SI 定义常数，几何化不构成物理预言）。",
    "S09_GAQ粒子质量谱体系":
        "本阶段产物：[普朗克锚定谬误冲突记录](普朗克锚定谬误冲突记录.md)"
        "（S09-C0001，内部冲突；质量谱派生链退化至 m=m_P，与既有 27.1.4 质量比失败同源）。",
    "S10_频率本源与复螺旋宇宙":
        "本阶段产物：[普朗克锚定谬误冲突记录](普朗克锚定谬误冲突记录.md)"
        "（S10-C0001，内部冲突；G 式与 m 式联立推出 m=m_P，电子锚点偏离 5.71e+44 倍）。",
    "S02_空间光速螺旋统一力":
        "本阶段产物：[统一动量低速极限冲突记录](统一动量低速极限冲突记录.md)"
        "（S02-C0001，内部冲突；P=m(c−v) 在 v=0 时给出 P=mc≠0，且与牛顿第二定律 F=+ma 反号）。",
    "S12_空间光速螺旋统一体系":
        "本阶段产物：[证伪标准与失效阈值](falsification_criteria.md)；"
        "[统一动量低速极限冲突记录](统一动量低速极限冲突记录.md)"
        "（S12-C0006，内部冲突；借用项 S12-A4 带入低速极限矛盾，且本体 A2 与动力学接口未定义）。",
}

OLD_TAIL = "当前尚无本阶段独立产物；不因目录存在而标记完成。"


def get_revision(base):
    try:
        d = json.loads(io.open(os.path.join(base, "system.json"), encoding="utf-8").read())
        return d.get("hypothesis_revision", "")
    except Exception:
        return ""


def append_claims(base):
    path = os.path.join(base, "claims.csv")
    text = io.open(path, encoding="utf-8").read()
    existing = {line.split(",", 1)[0] for line in text.splitlines()[1:] if line.strip()}
    added = 0
    if not text.endswith("\n"):
        text += "\n"
    rev = get_revision(base)
    for cid, statement, assumptions, derivation, uncertainty in CLAIMS[os.path.basename(base)]:
        if cid in existing:
            continue
        dp = os.path.join(base, derivation.replace("/", os.sep))
        if not os.path.isfile(dp):
            print("警告：推导记录缺失 " + derivation + " @ " + name)
        row = [cid, rev, statement, assumptions, derivation, "", "", "", uncertainty,
               "mathematical_result", "falsified", ""]
        for field in row:
            if "," in field or '"' in field:
                raise ValueError("字段不得含裸逗号或引号: " + field)
        text += ",".join(row) + "\n"
        added += 1
    io.open(path, "w", encoding="utf-8").write(text)
    return added


def update_readme(base):
    path = os.path.join(base, "11_证伪与反例", "README.md")
    text = io.open(path, encoding="utf-8").read()
    tail = README_TAIL[os.path.basename(base)]
    if tail in text:
        return False
    # 已存在「本阶段产物：」行则整行替换为合并句（S12 等多产物情形）
    new_text, n = re.subn(r".*本阶段产物：.*\n?", tail + "\n", text)
    if n > 0:
        io.open(path, "w", encoding="utf-8").write(new_text)
        return True
    if OLD_TAIL in text:
        text = text.replace(OLD_TAIL, tail)
    else:
        text = text.rstrip() + "\n\n" + tail + "\n"
    io.open(path, "w", encoding="utf-8").write(text)
    return True


def main():
    total_claims = 0
    total_readme = 0
    for name in CLAIMS:
        base = os.path.join(SYSTEMS, name)
        if not os.path.isdir(base):
            print("跳过（目录不存在）: " + name)
            continue
        total_claims += append_claims(base)
        if update_readme(base):
            total_readme += 1
        print("已登记: " + name)
    print("-" * 60)
    print("claims.csv 新增行: %d；11_证伪与反例/README.md 更新: %d" % (total_claims, total_readme))


if __name__ == "__main__":
    main()
