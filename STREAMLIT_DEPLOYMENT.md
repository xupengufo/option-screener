# Streamlit Cloud 部署指南

## 🚀 快速部署步骤

### 1. 准备 GitHub 仓库

首先确保你的代码已经推送到 GitHub：

```bash
# 初始化 git 仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Add dual strategy option screener"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/yourusername/option-screener.git

# 推送到 GitHub
git push -u origin main
```

### 2. 访问 Streamlit Cloud

1. 打开 [share.streamlit.io](https://share.streamlit.io)
2. 使用 GitHub 账号登录
3. 点击 "New app" 按钮

### 3. 配置应用

在部署页面填写以下信息：

- **Repository**: 选择你的 GitHub 仓库
- **Branch**: `main` (或你的主分支)
- **Main file path**: `option_screener_gui.py`
- **App URL**: 选择一个唯一的应用名称

### 4. 高级设置（可选）

点击 "Advanced settings" 可以配置：

- **Python version**: 3.9 (推荐)
- **Requirements file**: `requirements.txt`
- **Secrets**: 如果需要 API 密钥等敏感信息

### 5. 部署

点击 "Deploy!" 按钮，Streamlit Cloud 会：

1. 克隆你的仓库
2. 安装依赖包
3. 启动应用
4. 提供公共访问链接

## 📋 部署前检查清单

### 必需文件
- ✅ `option_screener_gui.py` - 主应用文件
- ✅ `requirements.txt` - 依赖包列表
- ✅ `README.md` - 项目说明（推荐）

### 可选文件
- 📄 `.streamlit/config.toml` - Streamlit 配置
- 📄 `packages.txt` - 系统包依赖（如果需要）
- 📄 `.gitignore` - Git 忽略文件

## ⚙️ 配置文件详解

### requirements.txt
确保包含所有必要的依赖：
```
streamlit>=1.28.0
yfinance>=0.2.0
pandas>=1.5.0
plotly>=5.0.0
```

### .streamlit/config.toml
优化应用配置：
```toml
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
```

## 🔧 常见问题解决

### 1. 依赖安装失败
**问题**: 某些包无法安装
**解决**: 
- 检查 `requirements.txt` 中的包名和版本
- 尝试固定版本号
- 查看部署日志中的错误信息

### 2. 应用启动失败
**问题**: 应用无法正常启动
**解决**:
- 确保主文件路径正确
- 检查代码中是否有语法错误
- 查看 Streamlit Cloud 的日志

### 3. 数据获取失败
**问题**: yfinance 无法获取数据
**解决**:
- 这是正常现象，某些网络环境可能限制访问
- 可以添加错误处理和重试机制
- 考虑使用其他数据源

### 4. 应用运行缓慢
**问题**: 应用响应速度慢
**解决**:
- 添加缓存装饰器 `@st.cache_data`
- 优化数据处理逻辑
- 减少不必要的 API 调用

## 🎯 优化建议

### 1. 添加缓存
```python
@st.cache_data(ttl=300)  # 缓存5分钟
def get_stock_data(ticker_symbol):
    # 你的数据获取代码
    pass
```

### 2. 错误处理
```python
try:
    # 数据获取代码
    pass
except Exception as e:
    st.error(f"数据获取失败: {e}")
    st.info("请稍后重试或检查股票代码是否正确")
```

### 3. 用户体验优化
- 添加加载动画
- 提供默认示例
- 添加使用说明

## 🔗 部署后管理

### 更新应用
1. 修改代码并推送到 GitHub
2. Streamlit Cloud 会自动检测更改
3. 应用会自动重新部署

### 查看日志
1. 在 Streamlit Cloud 控制台
2. 点击你的应用
3. 查看 "Logs" 标签页

### 管理设置
1. 可以修改应用设置
2. 添加或删除协作者
3. 配置自定义域名（付费功能）

## 📱 分享应用

部署成功后，你会得到一个公共链接，例如：
`https://your-app-name.streamlit.app`

你可以：
- 分享给其他用户使用
- 嵌入到网站中
- 添加到社交媒体

## 🔒 安全考虑

### 敏感信息
- 不要在代码中硬编码 API 密钥
- 使用 Streamlit Secrets 管理敏感信息
- 定期检查和更新依赖包

### 使用限制
- Streamlit Cloud 有资源限制
- 避免长时间运行的任务
- 合理使用缓存减少计算

## 💡 进阶功能

### 自定义域名
- 升级到付费计划
- 配置 CNAME 记录
- 添加 SSL 证书

### 团队协作
- 邀请团队成员
- 设置访问权限
- 管理应用版本

---

**部署完成后，记得测试所有功能确保正常工作！**