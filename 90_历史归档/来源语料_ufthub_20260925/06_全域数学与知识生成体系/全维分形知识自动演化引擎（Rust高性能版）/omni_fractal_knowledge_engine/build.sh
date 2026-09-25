#!/bin/bash
echo "全维分形知识自动演化引擎 编译脚本"
echo "================================"

# 检查Rust环境
if ! command -v cargo &> /dev/null
then
    echo "安装Rust环境..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
fi

# 编译
echo "开始编译release版本..."
cargo build --release

if [ $? -eq 0 ]; then
    echo "编译成功！可执行文件位于 target/release/omni-fractal-knowledge-engine"
    echo "运行 ./target/release/omni-fractal-knowledge-engine 启动引擎"
else
    echo "编译失败，请检查错误信息"
fi
