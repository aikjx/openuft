#!/usr/bin/env bash
# GAQ-UFT 一键编译脚本 (Linux / macOS)
# 依赖: pandoc + TeX Live (xelatex)
set -e
cd "$(dirname "$0")"

OUT="GAQ-UFT_Complete_Book.pdf"
TMP="__book_concat.md"

echo "[1/3] 拼接全部卷章 Markdown ..."
{
  cat main_book.md
  echo
  cat preface.md
  for f in Volume_00_Foundations/*.md \
           Volume_01_Geometric_Vacuum/*.md \
           Volume_02_Constant_Geometry_Origins/*.md \
           Volume_03_Particle_Spectra/*.md \
           Volume_04_Lorentz_Spacetime_Extension/*.md \
           Volume_05_Prediction_Falsification/*.md \
           Volume_06_Open_Problems_Future/*.md \
           Appendices/*.md; do
    echo
    cat "$f"
  done
} > "$TMP"

echo "[2/3] pandoc 转 LaTeX 并由 xelatex 编译 ..."
pandoc "$TMP" -o "$OUT" --pdf-engine=xelatex \
  --template=LaTeX_Templates/book_template.tex \
  -V CJKmainfont="Source Han Serif SC" \
  --toc --number-sections

echo "[3/3] 清理临时文件 ..."
rm -f "$TMP"
echo "完成！输出文件: $OUT"
