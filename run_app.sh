#!/bin/bash

# 期权筛选器启动脚本

echo "🚀 启动期权筛选器..."

# 检查是否存在虚拟环境
if [ ! -d "test_env" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv test_env
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source test_env/bin/activate

# 安装依赖
echo "📚 安装依赖包..."
pip install -r requirements.txt

# 启动应用
echo "🌐 启动 Streamlit 应用..."
echo "📱 应用将在浏览器中自动打开"
echo "🔗 如果没有自动打开，请访问: http://localhost:8501"
echo ""

streamlit run option_screener_gui.py