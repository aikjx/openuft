# -*- coding: utf-8 -*-
"""把本卷从 r267 整体改号到 r270（第三次改号），并清理误落在 r267 树内的草稿。"""
import os
import io
import glob
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))

STEM = ("可机检验收规范层_统一场论验收器十二条必要条件与正负对照"
        "及GR_SM_TUFT三对象实跑_精算与可视化_2026-10-31")
SRC = os.path.join(HERE, "TUFT-r267_" + STEM + ".py")
NEW = os.path.join(HERE, "TUFT-r270_" + STEM + ".py")

assert os.path.exists(SRC), "SRC missing: %s" % SRC
s = io.open(SRC, encoding="utf-8").read()

reps = [
    ('RID = "r267"', 'RID = "r270"'),
    ("TUFT-r267_" + STEM, "TUFT-r270_" + STEM),
    ("源码/_run_r267.py", "源码/_run_r270.py"),
    ("VOLUME_RANGE = list(range(243, 266))", "VOLUME_RANGE = list(range(243, 270))"),
    ("r243–r265", "r243–r269"),
    ("r243–r266", "r243–r269"),
    ("r142–r266", "r142–r269"),
]
for a, b in reps:
    n = s.count(a)
    s = s.replace(a, b)
    print("  rep %-48s x%d" % (a[:48], n))

# ---- 重写卷号沿革（docstring 块） ----
i0 = s.index("卷号沿革")
i1 = s.index("复现：", i0)
new_doc = """卷号沿革（2026-10-31 撞号链，本卷连改三次）
------------------------------------------
16:11 起草时实测 r266/r267/r268 三树**全空** ⇒ 拟取 r266。
16:19 复查发现 r266 被**两个**并行会话抢占：
      · 16:19:34 已落齐四件套《力的大统一方程层》⇒ 权威；
      · 16:19:50 正在起草《统一场论完成度终局验收层》（与本卷原定「跨卷收口」同层）。
      ⇒ 第一次改号 r266 → r267。
16:33 复查发现 r267 亦被抢占：上述第二个会话同样撞号并改号到 r267，
      已于 16:33:37 落齐四件套 ⇒ 权威；⇒ 第二次改号 r267 → r268。
16:34 复查发现 **r268 = ROOT-V5.0 融合审计**、**r269 = 候选比例多元性定理**
      亦均已被并行会话占用；实测 r270/r271/r272 三树全空 ⇒ 第三次改号 **r268 → r270**。

按「已产四件套并登记者为权威、后到者整体改号」纪律，本卷**整体迁至 r270**，
并把内容重定位为**只做「立」轴**（验收规范），破的收口指向 r267 并行会话
《统一场论完成度终局验收层》，不与他人重复。
误落在 r267 树内的本卷草稿已移入 `源码/_scratch_dead/`，未触碰他人任何字节。

"""
s = s[:i0] + new_doc + s[i1:]

# ---- A3 条目正文 ----
k0 = s.index('ent("A3"')
k1 = s.index('"实测三树：', k0)
new_a3 = (
    'ent("A3", "★破的收口交由 r267 并行会话：本卷不重复做跨卷总账",\n'
    '        "INFO",\n'
    '        "起草期间三次撞号：r266（16:19:34 落齐四件套《力的大统一方程层》；'
    '16:19:50 另一会话正在起草《统一场论完成度终局验收层》）、'
    'r267（同一会话改号后 16:33:37 落齐四件套）、'
    'r268（ROOT-V5.0 融合审计）、r269（候选比例多元性定理）均已被占。"\n'
    '        "按「已产四件套并登记者为权威、后到者整体改号」纪律，'
    '本卷经 r266→r267→r268 三次改号后**整体迁至 r270**，'
    '并把内容重定位为只做「立」轴。",\n'
)
s = s[:k0] + new_a3 + s[k1:]

s = s.replace("破的收口指向 r266 并行会话，本卷不重复",
              "破的收口指向 r267 并行会话《统一场论完成度终局验收层》，本本卷不重复")
s = s.replace("本本卷不重复", "本卷不重复")
s = s.replace("**整体迁至 r267**", "**整体迁至 r270**")

io.open(NEW, "w", encoding="utf-8").write(s)
print()
print("  wrote r270 engine  bytes=%d" % os.path.getsize(NEW))

# ---- 残留检查：r267/r268/r269 只应出现在叙事文字里 ----
resid = [l.strip()[:100] for l in s.split("\n")
         if ("r267" in l or "r268" in l or "r269" in l)]
print("  residual mentions = %d (narrative only)" % len(resid))
for l in resid[:10]:
    print("     ", l)

# ---- 把误落 r267 的草稿移入 scratch（禁 rm -rf） ----
dead = os.path.join(HERE, "_scratch_dead")
if not os.path.isdir(dead):
    os.makedirs(dead)
shutil.move(SRC, os.path.join(dead, "_discarded_r267_mine_" + STEM + ".py"))
print("  moved stray r267 draft -> 源码/_scratch_dead/")

print()
for r in ("r267", "r268", "r269", "r270"):
    print("  %s : 源码=%d 数据=%d"
          % (r, len(glob.glob(os.path.join(HERE, "*%s*" % r))),
             len(glob.glob(os.path.join(ROOT, "数据", "*%s*" % r)))))
