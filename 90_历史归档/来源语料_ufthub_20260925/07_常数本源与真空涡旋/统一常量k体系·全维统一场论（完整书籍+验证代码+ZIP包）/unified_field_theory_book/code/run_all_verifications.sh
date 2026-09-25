#!/bin/bash
# 运行所有验证代码
# 统一常量k体系 · 全维精算验证

set -e

CODE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=========================================="
echo "统一常量k体系 · 全维精算验证"
echo "=========================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到python3"
    exit 1
fi

# 运行验证脚本
SCRIPTS=(
    "verify_k_system.py"
    "verify_planck_scale.py"
    "verify_cosmology.py"
    "verify_astrophysics.py"
)

PASSED=0
FAILED=0

for script in "${SCRIPTS[@]}"; do
    echo "------------------------------------------"
    echo "运行: $script"
    echo "------------------------------------------"
    if python3 "$CODE_DIR/$script" 2>&1; then
        echo "✓ $script 通过"
        PASSED=$((PASSED + 1))
    else
        echo "✗ $script 失败"
        FAILED=$((FAILED + 1))
    fi
    echo ""
done

echo "=========================================="
echo "验证总结"
echo "=========================================="
echo "  通过: $PASSED"
echo "  失败: $FAILED"
echo "  总计: $((PASSED + FAILED))"
echo "=========================================="

if [ $FAILED -gt 0 ]; then
    exit 1
fi
