# -*- coding: utf-8 -*-
"""_chk_r314.py · 收口只读复核（零写入）

只读盘上图像做六件事：
  1) README 的 r314 小节恰 1 处，且与登记驱动 dump 出的 BLOCK 逐字相同；
  2) 把该小节按登记时的构造式从写后图像里剪掉，重建出的写前图像 md5 必须等于登记前现印的指纹
     ⇒ 这是逐字节的零删除/零改动证明，不是子序列弱对账；并现场反推尾部空行枚数 k；
  3) 小节里每一个「数字.数字」都必须逐字挂在已落盘的数据 md 面或来料正本上（写后口径，吃盘上图像）；
  4) 面名册逐张点名；README 印的五枚面指纹、stdout 面自报的、此刻盘上的，三方逐字对上；
  5) 小节内每个相对链接目标此刻仍在盘上；
  6) 判据有牙：三枚变异体（旧谓词假红、删一行既有内容、人造无载体小数）必须各自按预期报错。
"""
import hashlib
import io
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(ROOT)
README = os.path.join(BASE, "README.md")
LIB = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))   # .../my_lib（scratch 的宿主）
PRE_MD5 = "c8d4f41d3de3350010bec8db6b9ac33f"      # 登记前驱动现印（本轮 stdout 留存）
BLOCK_DUMP = os.path.join(LIB, "scratch", "r314_reg_block.txt")
D = os.path.join(BASE, "数据")
STAMP = "2026-11-01"
STEM = ("TUFT-r314_ROOTV21固定点机制独立复核与截断自等价定理与f0可证伪窗口与记忆擦除律"
        "与格点基准率与六格门禁_精算与可视化_" + STAMP)

OUT, FAIL, NCHK = [], [], [0]


def note(s):
    OUT.append(s)


def chk(name, ok, detail=""):
    NCHK[0] += 1
    note("  %s %s%s" % ("PASS" if ok else "FAIL", name, ("  ⇒ " + detail) if detail else ""))
    if not ok:
        FAIL.append(name)
    return bool(ok)


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def md5_of(p):
    return md5_bytes(io.open(p, "rb").read())


def hhmmss(mt):
    return time.strftime("%H:%M:%S", time.localtime(mt))


for _p, _nm in [(README, "README"), (BLOCK_DUMP, "登记驱动的 BLOCK dump"),
               (os.path.join(ROOT, "_out_r314.txt"), "stdout 面"),
               (os.path.join(D, STEM + ".md"), "数据 md 面")]:
    if not os.path.isfile(_p):
        print("REFUSE：收口复核缺载体 %s ⇒ 无法核对（%s）" % (_nm, _p))
        sys.exit(2)

rb = io.open(README, "rb").read()
nl = "\r\n" if rb.count(b"\r\n") else "\n"
lines = rb.decode("utf-8").split(nl)
marker = "### r314 ·"
note("== r314 收口只读复核（零写入）==")
note("README 此刻：md5=%s 字节=%d 行=%d CRLF=%d 裸LF=%d 行尾形状=%r"
     % (md5_bytes(rb), len(rb), len(lines), rb.count(b"\r\n"), rb.count(b"\n"), nl))

# ---- 1) 小节唯一且与 dump 逐字相同 ----
idxs = [i for i, l in enumerate(lines) if l.startswith(marker)]
chk("README r314 小节恰 1 处", len(idxs) == 1, "命中行号 %s（1 起）" % [i + 1 for i in idxs])
if len(idxs) != 1:
    note("\r\n".join(OUT))
    print("RC = 2（小节不唯一，后续核对无法定位）"); sys.exit(2)
block = io.open(BLOCK_DUMP, "rb").read().decode("utf-8")
nL = block.split("\r\n")
i0 = idxs[0]
written = lines[i0:i0 + len(nL)]
first_diff = next((k for k in range(min(len(nL), len(written))) if written[k] != nL[k]), None)
chk("盘上小节 == 驱动 dump 的 BLOCK（%d 行逐字）" % len(nL),
    len(written) == len(nL) and first_diff is None, "首个差异行 %s" % first_diff)

# ---- 2) 剪小节 ⇒ 重建写前图像（逐字节），并现场反推尾部空行数 k ----
pre_tail = lines[:i0 - 1] if i0 >= 1 and lines[i0 - 1] == "" else None
if pre_tail is None:
    chk("小节前恰有一枚分隔空行（登记构造前提）", False, "行 %d 前不是空行" % (i0 + 1))
    k_list = []
else:
    k_list = [k for k in range(0, 5)
              if md5_bytes((nl.join(pre_tail) + nl * k).encode("utf-8")) == PRE_MD5]
    chk("剪掉「分隔空行 + 小节 + 尾空行」后重建写前图像，逐字节 md5 == 登记前指纹",
        len(k_list) == 1, "可行的尾部空行数 k=%s（写前图像 %d 行）"
        % (k_list, (len(pre_tail) + k_list[0]) if len(k_list) == 1 else "-"))
    chk("写后 == 写前剪尾 + 空行 + 小节 + 空行（构造式逐行复原）",
        lines == pre_tail + [""] + nL + [""])

# ---- 3) 写后口径的载体审计（吃盘上图像） ----
md_face = io.open(os.path.join(D, STEM + ".md"), "rb").read().decode("utf-8")
lia = io.open(os.path.join(D, STEM + "_来料原件_ROOT_V21.0_用户附件逐字_" + STAMP + ".md"),
              "rb").read().decode("utf-8")
toks = re.findall(r"\d+\.\d+", block)
orphan = sorted({t for t in toks if t not in md_face and t not in lia})
chk("盘上小节小数 %d 枚（去重 %d 枚）全部逐字有载体" % (len(toks), len(set(toks))),
    not orphan, "无载体名单 %s" % orphan)
chk("旧判词拼法在盘上小节里 0 留存",
    "ATTRACTIVITY-ORTHOGONAL-EM " not in (block + "\n"))
vm = re.search(r"\*\*判词\*\*：([^\r\n]+)", block)
chk("README 判词逐字住在数据面上", bool(vm) and vm.group(1) in md_face,
    "取到 1 行" if vm else "未取到判词行")
ck = re.search(r"\*\*复现\*\*：.*?条目 \*\*(\d+)\*\*", block, re.S)
json_face = io.open(os.path.join(D, STEM + ".json"), "rb").read().decode("utf-8")
doc_fail = [i["id"] for i in json.loads(json_face)["items"]
            if i["layer"] not in ("控制组", "守卫") and i["verdict"] == "FAIL"]
chk("README 印的条目总数逐字住在数据 json 面上", bool(ck) and ck.group(1) in json_face,
    "总数 %s" % (ck.group(1) if ck else "未取到"))

# ---- 4) 面名册逐张点名 ----
faces = [("数据 json", os.path.join(D, STEM + ".json")),
         ("数据 md", os.path.join(D, STEM + ".md")),
         ("数据 report", os.path.join(D, STEM + "_report.txt")),
         ("判定册", os.path.join(BASE, "判定", "判定_" + STEM + ".md")),
         ("可视化 html", os.path.join(BASE, "四力统一方程_ROOTV21耦合固定点机制审计_r314可视化_"
                                     + STAMP + ".html")),
         ("来料正本", os.path.join(D, STEM + "_来料原件_ROOT_V21.0_用户附件逐字_" + STAMP + ".md")),
         ("引擎", os.path.join(ROOT, STEM + ".py")),
         ("runner", os.path.join(ROOT, "_run_r314.py")),
         ("stdout", os.path.join(ROOT, "_out_r314.txt")),
         ("登记驱动", os.path.join(ROOT, "_reg_r314.py"))]
note("  面名册（字节 / md5 / mtime）：")
for n, p in faces:
    if os.path.isfile(p):
        st = os.stat(p)
        note("    %-10s %8d B  %s  %s" % (n, st.st_size, md5_of(p), hhmmss(st.st_mtime)))
    else:
        chk("面 %s 在盘上" % n, False, p)
out_face = io.open(os.path.join(ROOT, "_out_r314.txt"), "rb").read().decode("utf-8", "replace")
md5s_out = re.findall(r"md5=([0-9a-f]{32})", out_face)
md5s_readme = re.findall(r"md5=([0-9a-f]{32})", block)
five = [p for n, p in faces if n in ("数据 json", "数据 md", "数据 report", "判定册", "可视化 html")]
now5 = [md5_of(p) for p in five]
chk("stdout 面自报 5 枚指纹", len(md5s_out) == 5, "实收 %d" % len(md5s_out))
chk("README 印的 5 枚 == stdout 自报 5 枚", md5s_readme[:5] == md5s_out,
    "README 侧 %d 枚" % len(md5s_readme))
chk("此刻盘上 5 枚 == stdout 自报 5 枚（跑完后无人再改面）", now5 == md5s_out,
    "差异下标 %s" % [k for k in range(min(5, len(now5))) if now5[k] != md5s_out[k]])
chk("stdout 面 RC = 0", re.findall(r"RC = (\d+)", out_face) == ["0"],
    str(re.findall(r"RC = (\d+)", out_face)))
chk("stdout 面：控制组全绿且守卫全绿", "控制组全绿=True 守卫全绿=True" in out_face)
chk("stdout 面 FAIL 名单 == 数据 json 面的 FAIL 名单（期望由对象现推，不手写）",
    re.findall(r"'(V\d+)'", out_face[out_face.rfind("FAIL 主条目"):]) == doc_fail,
    "stdout=%s json=%s" % (re.findall(r"'(V\d+)'", out_face[out_face.rfind("FAIL 主条目"):]),
                           doc_fail))

# ---- 5) 链接目标存在 ----
links = [l for l in re.findall(r"\]\(([^)]+)\)", block) if not l.startswith(("http", "#"))]
bad = [l for l in links if not os.path.isfile(os.path.join(BASE, l.replace("/", os.sep)))]
chk("小节内 %d 枚相对链接目标全在盘上" % len(links), not bad, "缺失 %s" % bad)

# ---- 6) 三枚变异体必须按预期报错（判据有牙） ----
if pre_tail is not None and len(k_list) == 1:
    old_img = pre_tail + [""] * k_list[0]                    # 未剪尾的写前图像（登记驱动当时用的分母）
    old_pred = all(a == b for a, b in zip(lines, old_img))    # 本轮真崩过的那条错谓词
    fixed_pred = all(a == b for a, b in zip(lines, pre_tail))  # 修好的谓词
    chk("旧谓词在「空行搬家」上假红（证明登记时那条 FAIL 是谓词错、不是内容被删）",
        old_pred is False, "old=%s fixed=%s" % (old_pred, fixed_pred))
    chk("修好的谓词为真", fixed_pred)
    mutated = list(pre_tail)
    del mutated[100]
    chk("删一行既有内容的重建无法冒充写前图像（棘轮有牙）",
        md5_bytes((nl.join(mutated) + nl * k_list[0]).encode("utf-8")) != PRE_MD5)
else:
    chk("变异体三枚（前提不成立，未跑）", False, "pre_tail/k 反推失败")
synthetic = block + "\r\n- 人造读数 12345.6789 无载体\r\n"
orph2 = sorted({t for t in re.findall(r"\d+\.\d+", synthetic) if t not in md_face and t not in lia})
chk("载体审计能抓住人造小数（牙）", orph2 == ["12345.6789"], str(orph2))
bad_link_probe = [l for l in links + ["数据/不存在的文件_xxx.md"]
                  if not os.path.isfile(os.path.join(BASE, l.replace("/", os.sep)))]
chk("链接探针能抓住人造缺件（牙）", len(bad_link_probe) == 1, str(bad_link_probe))

note("")
note("判决：%s（判 %d 项，红 %d 项%s）"
     % ("ALL PASS" if not FAIL else "FAIL", NCHK[0], len(FAIL),
        ("：" + "、".join(FAIL)) if FAIL else ""))
text = "\r\n".join(OUT)
io.open(os.path.join(LIB, "scratch", "r314_close.txt"), "wb").write(text.encode("utf-8"))
sys.stdout.write(text.encode("ascii", "backslashreplace").decode("ascii") + "\n")
print("RC =", 0 if not FAIL else 2)
sys.exit(0 if not FAIL else 2)
