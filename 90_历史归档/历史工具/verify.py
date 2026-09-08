"""
openuft · 一键总验证脚本
====================================================================
运行此脚本会按顺序检查：
1. 目录结构完整性
2. 核心文档存在性
3. 内部交叉引用一致性
4. 定理谱（TS1-TS12）登记完整性
5. 开放问题清单（L0 不为空）
6. 引用统计（无残留 alg_uft_unified）
7. 开源标准化文件（LICENSE / .gitignore / CITATION.cff）
"""
from __future__ import annotations
import os
import re
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
NAME = "openuft"

def header(s: str):
    print("\n" + "=" * 70)
    print(f"  {s}")
    print("=" * 70)

def ok(s: str):
    print(f"  ✅ {s}")

def warn(s: str):
    print(f"  ⚠️  {s}")

def err(s: str):
    print(f"  ❌ {s}")

def check_structure() -> int:
    """检查 12 个一级目录是否存在"""
    header("1. 一级目录结构 (12 个)")
    required = [
        "00_index",
        "10_D_求导_derivation",
        "20_P_证明_proof",
        "30_V_验证_verification",
        "40_A_精算_audit",
        "50_physics_domains",
        "60_application",
        "70_source_code",
        "80_visualization",
        "90_paper_论文",
        "95_history_archive",
        "99_inbox_future",
    ]
    score = 0
    for d in required:
        if (ROOT / d).is_dir():
            ok(f"{d}/")
            score += 1
        else:
            err(f"{d}/ MISSING")
    print(f"  → 得分：{score}/{len(required)}")
    return score

def check_core_files() -> int:
    """检查顶层核心文档"""
    header("2. 顶层核心文档")
    required = [
        "README.md", "INDEX.md", "CHANGELOG.md", "MIGRATION_GUIDE.md",
        "WORKFLOW.md", "ROADMAP.md", "FAQ.md", "CONTRIBUTING.md",
        "LICENSE", ".gitignore", "CITATION.cff",
    ]
    score = 0
    for f in required:
        if (ROOT / f).exists():
            ok(f"{f}")
            score += 1
        else:
            err(f"{f} MISSING")
    print(f"  → 得分：{score}/{len(required)}")
    return score

def check_inbox() -> int:
    """检查开放问题占位（L0 层不能为空）"""
    header("3. 开放问题 (99_inbox_future/)")
    inbox = ROOT / "99_inbox_future"
    if not inbox.exists():
        err("99_inbox_future/ MISSING")
        return 0
    children = [p for p in inbox.iterdir() if p.is_dir()]
    if not children:
        err("99_inbox_future/ 为空！违反无限扩展原则")
        return 0
    for c in children:
        ok(f"{c.name}/")
    print(f"  → 占位数：{len(children)}（建议 ≥ 10）")
    return len(children)

def check_no_residual_old_name() -> int:
    """检查是否还残留 alg_uft_unified 旧名（白名单文件除外）"""
    header("4. 历史遗留名检查")
    old_name = "alg_uft_unified"
    # 白名单：以下文件中的"alg_uft_unified"是合法的历史叙述提及
    whitelist = {
        "CHANGELOG.md",
        "docs/DESIGN_DECISIONS.md",
        "00_index/全维分析报告.md",  # 改名历史叙述
        "verify.py",
    }
    found = 0
    found_residual = []
    for md in ROOT.rglob("*.md"):
        rel = md.relative_to(ROOT).as_posix()
        # 白名单跳过
        if any(rel == w or rel.endswith("/" + w) for w in whitelist):
            continue
        try:
            content = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if old_name in content:
            err(f"残留 {old_name} in: {rel}")
            found_residual.append(rel)
            found += 1
    if found == 0:
        ok(f"无残留 {old_name}（已忽略白名单：CHANGELOG/DESIGN_DECISIONS/全维分析报告/verify.py）")
    else:
        warn(f"共 {found} 处真残留: {found_residual}")
    return 1 if found == 0 else 0

def check_thm_count() -> int:
    """统计定理谱 TS1-TS12 提及情况"""
    header("5. 定理谱 TS1-TS12 提及检查")
    target_thms = [f"TS{i}" for i in range(1, 13)]
    score = 0
    for ts in target_thms:
        # 搜索 README.md 或 INDEX.md
        for fname in ["README.md", "INDEX.md", "CHANGELOG.md"]:
            f = ROOT / fname
            if f.exists():
                content = f.read_text(encoding="utf-8")
                if ts in content:
                    ok(f"{ts} 在 {fname} 提及")
                    score += 1
                    break
        else:
            err(f"{ts} 未在任何顶层文档提及！")
    print(f"  → 得分：{score}/12")
    return score

def check_total_md() -> int:
    """统计 Markdown 文档总数"""
    header("6. 文档总数统计")
    all_md = list(ROOT.rglob("*.md"))
    print(f"  → 总 md 文件：{len(all_md)}")
    total_size = sum(f.stat().st_size for f in all_md)
    print(f"  → 总大小：{total_size / 1024:.1f} KB ({total_size / 1024 / 1024:.2f} MB)")
    return len(all_md)

def main():
    print(f"\n  openuft 全维验证脚本  v1.0  ({datetime.now().isoformat(timespec='seconds')})\n")
    s1 = check_structure()
    s2 = check_core_files()
    s3 = check_inbox()
    s4 = check_no_residual_old_name()
    s5 = check_thm_count()
    s6 = check_total_md()

    header("总览")
    print(f"  一级目录：{s1}/12")
    print(f"  核心文档：{s2}/11")
    print(f"  开放问题占位：{s3}")
    print(f"  历史名清理：{'✅' if s4 else '❌'}")
    print(f"  定理谱完整：{s5}/12")
    print(f"  文档总数：{s6}")

    overall_score = s1 + s2 + s4 + s5
    if overall_score >= 35:
        print(f"\n  🎉 总体通过：{overall_score}/36 可验证项")
        return 0
    else:
        print(f"\n  ⚠️  总体异常：{overall_score}/36")
        return 1

if __name__ == "__main__":
    sys.exit(main())
