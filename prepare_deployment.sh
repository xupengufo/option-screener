#!/bin/bash

# Streamlit Cloud 部署准备脚本

echo "🚀 准备部署到 Streamlit Cloud..."

# 检查必要文件
echo "📋 检查必要文件..."

required_files=("option_screener_gui.py" "requirements.txt")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ 缺少必要文件:"
    printf '%s\n' "${missing_files[@]}"
    exit 1
fi

echo "✅ 必要文件检查通过"

# 创建 .streamlit 配置目录
if [ ! -d ".streamlit" ]; then
    echo "📁 创建 .streamlit 配置目录..."
    mkdir .streamlit
fi

# 创建或更新 config.toml
echo "⚙️ 创建 Streamlit 配置文件..."
cat > .streamlit/config.toml << 'EOF'
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#4facfe"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[browser]
gatherUsageStats = false
EOF

# 创建 .gitignore 文件
if [ ! -f ".gitignore" ]; then
    echo "📝 创建 .gitignore 文件..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
test_env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Logs
*.log
EOF
fi

# 检查 requirements.txt 内容
echo "📦 检查依赖包..."
if ! grep -q "streamlit" requirements.txt; then
    echo "⚠️  警告: requirements.txt 中未找到 streamlit"
fi

if ! grep -q "yfinance" requirements.txt; then
    echo "⚠️  警告: requirements.txt 中未找到 yfinance"
fi

# 测试应用是否可以正常导入
echo "🧪 测试应用导入..."
python3 -c "
try:
    import option_screener_gui
    print('✅ 应用导入成功')
except ImportError as e:
    print(f'❌ 应用导入失败: {e}')
    exit(1)
except Exception as e:
    print(f'⚠️  导入时出现警告: {e}')
"

# 检查 Git 状态
echo "📊 检查 Git 状态..."
if [ ! -d ".git" ]; then
    echo "⚠️  未初始化 Git 仓库"
    echo "💡 运行以下命令初始化:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
else
    echo "✅ Git 仓库已初始化"
    
    # 检查是否有未提交的更改
    if [ -n "$(git status --porcelain)" ]; then
        echo "⚠️  有未提交的更改"
        echo "💡 运行以下命令提交更改:"
        echo "   git add ."
        echo "   git commit -m 'Prepare for deployment'"
    else
        echo "✅ 所有更改已提交"
    fi
    
    # 检查远程仓库
    if git remote -v | grep -q origin; then
        echo "✅ 远程仓库已配置"
        remote_url=$(git remote get-url origin)
        echo "🔗 远程仓库: $remote_url"
    else
        echo "⚠️  未配置远程仓库"
        echo "💡 运行以下命令添加远程仓库:"
        echo "   git remote add origin https://github.com/yourusername/your-repo.git"
    fi
fi

echo ""
echo "🎉 部署准备完成!"
echo ""
echo "📋 下一步操作:"
echo "1. 确保代码已推送到 GitHub"
echo "2. 访问 https://share.streamlit.io"
echo "3. 使用 GitHub 账号登录"
echo "4. 点击 'New app' 创建新应用"
echo "5. 选择你的仓库和 option_screener_gui.py 文件"
echo "6. 点击 'Deploy!' 开始部署"
echo ""
echo "📖 详细说明请查看 STREAMLIT_DEPLOYMENT.md"