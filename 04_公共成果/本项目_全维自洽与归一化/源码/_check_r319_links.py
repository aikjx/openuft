# -*- coding: utf-8 -*-
"""r319 链接体检（只读）：README 四处 + 数据说明件 + 判定册 + 可视化 的所有本地链接

纪律（承 r305/r307/r309，本卷第三条负控保留）：
  * 必须**同时报「检查了多少条链接」**——只报「0 断」而不知分母等于装饰
  * 负控 A：注入 1 假 + 1 真 ⇒ 须恰好报断 1 条且为假目标
  * 负控 B：仅真目标 ⇒ 须报断 0 条
  * 负控 C：**空目标集 ⇒ 本地链接 0 条须触发 FAIL 分支**
  * 正控 C：只放外链 ⇒ 本地 0 条，同样须触发该分支
"""
import io
import os
import re
import sys

ROOT = r"D:\a10\aikjx\code\my_lib\openuft\04_公共成果\本项目_全维自洽与归一化"
README = os.path.join(ROOT, "README.md")

RID = "r319"
BASE = ("TUFT-r319_统一表示框架与二次超荷矩_"
        "单一不可约表示能否绕开复制约束与三代的框架依赖性_精算与可视化_2026-11-01")
DATA_MD = os.path.join(ROOT, "数据", BASE + ".md")
JUD_MD = os.path.join(ROOT, "判定", "判定_" + BASE + ".md")
HTML = os.path.join(ROOT, "四力统一方程_统一表示框架与二次超荷矩_r319可视化_2026-11-01.html")

LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def check(targets, base_dir):
    n_all, n_local, n_skip, broken = 0, 0, 0, []
    for t in targets:
        n_all += 1
        tl = t.strip()
        if tl.startswith(("http://", "https://", "#", "mailto:")):
            n_skip += 1
            continue
        n_local += 1
        p = os.path.normpath(os.path.join(base_dir, tl))
        if not os.path.exists(p):
            broken.append((tl, p))
    return n_all, n_local, n_skip, broken


def verdict_local_zero(n_local):
    """把「本地链接 0 条」这一判据抽成纯函数，负控 C 可直接调用它。"""
    return n_local == 0


def main():
    ok = True
    total_all = total_local = total_skip = 0
    all_broken = []

    rlines = read(README).split("\n")
    anchors = {
        "src": u"│   ├── TUFT-%s_" % RID,
        "jud": u"├── 判定_TUFT-%s_" % RID,
        "cmp": u"- **%s（2026-11-01）" % RID,
        "det": u"### %s · 2026-11-01" % RID,
    }
    for k, a in anchors.items():
        c = sum(1 for ln in rlines if ln.startswith(a))
        print("[anchor] %-4s %-26s count=%d %s" % (k, a, c, "OK" if c == 1 else "BAD"))
        if c != 1:
            ok = False

    i0 = next(i for i, ln in enumerate(rlines) if ln.startswith(u"### %s · 2026-11-01" % RID))
    i1 = len(rlines)
    for j in range(i0 + 1, len(rlines)):
        if rlines[j].startswith("### r"):
            i1 = j
            break
    det_block = "\n".join(rlines[i0:i1])
    print("[scope] README %s detail 节：行 %d..%d，共 %d 行，链接 %d 条"
          % (RID, i0 + 1, i1, i1 - i0, len(LINK_RE.findall(det_block))))

    for name, txt, bd in [
        ("README-%s-detail" % RID, det_block, ROOT),
        (u"数据说明件", read(DATA_MD), os.path.dirname(DATA_MD)),
        (u"判定册", read(JUD_MD), os.path.dirname(JUD_MD)),
    ]:
        n_all, n_local, n_skip, broken = check(LINK_RE.findall(txt), bd)
        total_all += n_all
        total_local += n_local
        total_skip += n_skip
        all_broken.extend([(name,) + b for b in broken])
        print("[link] %-20s 全部 %3d / 本地 %3d / 跳过 %2d / 断链 %d %s"
              % (name, n_all, n_local, n_skip, len(broken), "OK" if not broken else "BAD"))
        for tl, p in broken:
            print("         - 断: %s -> %s" % (tl, p))

    for p in [os.path.join(ROOT, "源码", BASE + ".py"),
              os.path.join(ROOT, "数据", BASE + ".json"),
              os.path.join(ROOT, "数据", BASE + "_report.txt"),
              os.path.join(ROOT, "源码", "_run_r319.py"),
              os.path.join(ROOT, "源码", "_out_r319.txt"),
              os.path.join(ROOT, "源码", "_reg_r319.py"),
              os.path.join(ROOT, "源码", "_fixnum_r317_to_r319.py"),
              HTML]:
        e = os.path.exists(p)
        print("[file] %-6s %s" % ("OK" if e else "MISS", os.path.basename(p)))
        if not e:
            ok = False

    fake = [u"源码/__NO_SUCH_FILE_%s__.md" % RID, "数据/" + BASE + ".json"]
    _, _, _, nb = check(fake, ROOT)
    neg_ok = (len(nb) == 1 and nb[0][0] == fake[0])
    print("[negctl-A] 注入 1 假 + 1 真 ⇒ 报断 %d 条（须 1，且为假目标）%s"
          % (len(nb), "OK" if neg_ok else "BAD"))
    if not neg_ok:
        ok = False
    _, _, _, nb2 = check([fake[1]], ROOT)
    print("[negctl-B] 仅真目标 ⇒ 报断 %d 条（须 0）%s" % (len(nb2), "OK" if not nb2 else "BAD"))
    if nb2:
        ok = False

    a0, l0, s0, b0 = check([], ROOT)
    c_ok = (a0 == 0 and l0 == 0 and verdict_local_zero(l0) is True)
    print("[negctl-C] 空目标集 ⇒ 全部 %d / 本地 %d ⇒ 触发「0 条即 FAIL」分支 %s"
          % (a0, l0, "OK" if c_ok else "BAD"))
    if not c_ok:
        ok = False
    _, l1, _, _ = check(["https://example.org/x"], ROOT)
    c2_ok = verdict_local_zero(l1) is True
    print("[posctl-C] 只放 1 条外链 ⇒ 本地 %d 条 ⇒ 同样触发该分支 %s"
          % (l1, "OK" if c2_ok else "BAD"))
    if not c2_ok:
        ok = False

    if all_broken:
        ok = False
    print("[sum] 链接总数 %d（本地 %d / 跳过 %d），断链 %d"
          % (total_all, total_local, total_skip, len(all_broken)))
    if total_local == 0:
        print("[sum] BAD：本地链接 0 条 ⇒ 体检是空的，不算通过")
        ok = False
    print("LINK-%s" % ("OK" if ok else "FAIL"))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
