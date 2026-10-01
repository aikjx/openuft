# -*- coding: utf-8 -*-
"""
tuft_hash_verify.py
===================

TUFT / H-TUFT 全脚本 SHA256 审计工具（**替代原稿 placeholder 版本**）

诚实说明：
- 原稿 §10 的 `hash_verify.py` 把基准哈希写成 `placeholder_sha256_EDM` 等**占位串**，
  永远 `FAIL`，等于无校验。本文件计算**真实 SHA256**并生成清单。
- 本工具**只做哈希审计**，不评价物理结论；缺失脚本如实标 `NOT_FOUND`（不伪造）。
- 额外提供 `--curated` 交叉校验：读全部 `tuft_卷*_CURATED.json`，核对其中声明的
  `script_sha256` 与实际文件是否一致（可发现「声明已落盘但实际缺失/漂移」）。

用法：
    python tuft_hash_verify.py            # 写清单 + 校验 + CURATED 交叉核对
    python tuft_hash_verify.py --write    # 仅写清单 tuft_scripts_manifest.json
    python tuft_hash_verify.py --verify   # 仅按清单校验
    python tuft_hash_verify.py --curated  # 仅做 CURATED 交叉核对
"""

import hashlib
import json
import os
import sys

try:  # Windows GBK 控制台防 UnicodeEncodeError
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "tuft_scripts_manifest.json")

# 关键脚本清单：4 突破脚本 + 味/暴胀 + H-TUFT 各卷 + 引擎 + 本卷新工具
TARGETS = [
    "tuft_EDM_实验对接_OPEN6.py",
    "tuft_g2_电子反常磁矩_OPEN5.py",
    "tuft_sigma_abs0_ringdown_可检验性_OPEN_v2.py",
    "tuft_beta_running_缺口_定理N实例化.py",
    "tuft_flavor_ckm_pmns_OPEN_v1.py",
    "tuft_cmb_inflation_bmode_OPEN_v1.py",
    "tuft_blackhole_torsion_core_OPEN_v1.py",
    "tuft_helical_bundle_H_v1.py",
    "tuft_htuft_cosmic_string_v1.py",
    "tuft_htuft_global_mcmc_v1.py",
    "tuft_htuft_darkmatter_soliton_v1.py",  # 补充卷A（CUR-14）
    "tuft_htuft_vacuum_topology_lambda_v1.py",  # 补充卷B（CUR-15）
    "tuft_htuft_flavor_ckm_topology_v1.py",  # 补充卷F（CUR-16）
    "tuft_dimtrans_lambda_probe.py",        # 卷系突破：Λ 维度嬗变探针（非 CUR 条目）
    "tuft_htuft_particle_spectrum_v1.py",   # 卷28（CUR-12，已落盘）
    "tuft_htuft_scatter_amplitude_v1.py",   # 卷26（CUR-10，已落盘）
    "tuft_global_mcmc_nested_OPEN_v1.py",
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def scan():
    out = {}
    for name in TARGETS:
        path = os.path.join(HERE, name)
        out[name] = sha256_file(path) if os.path.isfile(path) else None
    return out


def cmd_write():
    data = scan()
    payload = {
        "note": "由 tuft_hash_verify.py 生成；--verify 模式据此校验（真实 SHA256，非占位串）",
        "hashes": data,
    }
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=True)
    print("[WRITE] 已写入清单：%s" % os.path.basename(MANIFEST))
    for name in TARGETS:
        v = data[name]
        print("    %-48s %s" % (name, v[:16] + "..." if v else "NOT_FOUND"))
    return 0


def cmd_verify():
    if not os.path.isfile(MANIFEST):
        print("[ERROR] 清单不存在，请先运行 --write")
        return 2
    with open(MANIFEST, encoding="utf-8") as fh:
        ref = json.load(fh)["hashes"]
    now = scan()
    fails = 0
    print("[VERIFY] 按清单校验：")
    for name in TARGETS:
        r = ref.get(name)
        n = now.get(name)
        if r is None and n is None:
            status = "NOT_FOUND (清单亦无)"
        elif r is None and n is not None:
            status = "NEW (清单未记录)"
        elif r is not None and n is None:
            status = "MISSING (清单有, 文件丢失)"; fails += 1
        elif r == n:
            status = "PASS"
        else:
            status = "FAIL (哈希漂移)"; fails += 1
        print("    %-48s %s" % (name, status))
    print("    结果：%s（FAIL/MISSING=%d）" % ("全部通过" if fails == 0 else "存在问题", fails))
    return 1 if fails else 0


def cmd_curated():
    """读全部 tuft_卷*_CURATED.json，核对声明的 script_sha256 与实际文件。"""
    issues = 0
    print("[CURATED] 交叉核对 CURATED 声明的 script_sha256：")
    found_any = False
    for fname in sorted(os.listdir(HERE)):
        if not fname.endswith("_CURATED.json"):
            continue
        found_any = True
        try:
            with open(os.path.join(HERE, fname), encoding="utf-8") as fh:
                doc = json.load(fh)
        except Exception as exc:
            print("    %-38s UNREADABLE %s" % (fname, exc)); issues += 1
            continue
        for ent in doc.get("entries", []):
            eid = ent.get("entry_id", "?")
            sref = ent.get("script_ref", "")
            decl = ent.get("script_sha256", None)
            base = sref.split("（")[0].strip().strip("`")
            path = os.path.join(HERE, base)
            if not os.path.isfile(path):
                state = "NOT_LANDED (脚本缺失)" if decl is None else "MISSING (声明有哈希但文件缺失)"
                issues += 1
            elif decl is None:
                state = "UNDECLARED (文件在但哈希为空)"; issues += 1
            else:
                state = "MATCH" if sha256_file(path) == decl else "MISMATCH (哈希不符)"
                if state != "MATCH":
                    issues += 1
            print("    %-8s %-38s %s" % (eid, (base or "?")[:38], state))
    if not found_any:
        print("    （未找到任何 *_CURATED.json）")
    print("    结果：%s（问题项=%d）" % ("全部一致" if issues == 0 else "存在问题", issues))
    return 1 if issues else 0


def main(argv):
    args = set(argv[1:])
    if args == {"--write"}:
        return cmd_write()
    if args == {"--verify"}:
        return cmd_verify()
    if args == {"--curated"}:
        return cmd_curated()
    rc = 0
    rc |= cmd_write()
    print("-" * 72)
    rc |= cmd_verify()
    print("-" * 72)
    rc |= cmd_curated()
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
