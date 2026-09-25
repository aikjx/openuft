#!/bin/bash
# 统一常量k体系 · 全书编译脚本
# 将所有Markdown文件合并为完整书籍

set -e

BOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$BOOK_DIR/build"
mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="$OUTPUT_DIR/unified_field_theory_complete.md"

echo "=========================================="
echo "统一常量k体系 · 全书编译"
echo "=========================================="

# 清空输出文件
> "$OUTPUT_FILE"

# 写入标题页
cat >> "$OUTPUT_FILE" << 'HEADER'
% 统一常量k体系：全维统一场论
% 最终修复优化版 · 无循环论证 · 完全兼容正统物理
% 2026年8月

---

HEADER

# 按顺序合并各卷
VOLUMES=(
    "vol01_foundations/volume01.md"
    "vol02_general_relativity/volume02.md"
    "vol03_quantum_standard/volume03.md"
    "vol04_planck_uv/volume04.md"
    "vol05_em_strong/volume05.md"
    "vol06_cosmology/volume06.md"
    "vol07_astrophysics/volume07.md"
    "vol08_dimensions_constants/volume08.md"
    "vol09_experimental/volume09.md"
    "appendices/appendices.md"
)

for vol in "${VOLUMES[@]}"; do
    if [ -f "$BOOK_DIR/$vol" ]; then
        echo "  合并: $vol"
        cat "$BOOK_DIR/$vol" >> "$OUTPUT_FILE"
        echo -e "\n\n---\n\n" >> "$OUTPUT_FILE"
    else
        echo "  警告: 文件不存在 $vol"
    fi
done

echo ""
echo "=========================================="
echo "编译完成!"
echo "输出文件: $OUTPUT_FILE"
echo "文件大小: $(du -h "$OUTPUT_FILE" | cut -f1)"
echo "字符数: $(wc -m < "$OUTPUT_FILE")"
echo "行数: $(wc -l < "$OUTPUT_FILE")"
echo "=========================================="

# 如果安装了pandoc，尝试生成PDF
if command -v pandoc &> /dev/null; then
    echo ""
    echo "检测到pandoc，尝试生成PDF..."
    pandoc "$OUTPUT_FILE" -o "$OUTPUT_DIR/unified_field_theory_complete.pdf" \
        --pdf-engine=xelatex \
        -V geometry:margin=1in \
        -V fontsize=11pt \
        -V documentclass=book \
        --toc \
        --toc-depth=2 \
        2>/dev/null && echo "PDF生成成功: $OUTPUT_DIR/unified_field_theory_complete.pdf" || echo "PDF生成失败（可能缺少LaTeX环境）"
else
    echo ""
    echo "未检测到pandoc，跳过PDF生成。"
    echo "如需PDF，请安装pandoc和LaTeX后重新运行。"
fi
