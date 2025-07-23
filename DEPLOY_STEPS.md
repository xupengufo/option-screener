# 🚀 Streamlit Cloud 部署步骤

## 第一步：推送到 GitHub

1. **创建 GitHub 仓库**
   - 访问 [github.com](https://github.com)
   - 点击 "New repository"
   - 仓库名称：`option-screener` (或你喜欢的名称)
   - 设为 Public
   - 点击 "Create repository"

2. **推送代码**
   ```bash
   # 添加远程仓库（替换为你的用户名和仓库名）
   git remote add origin https://github.com/YOUR_USERNAME/option-screener.git
   
   # 推送代码
   git push -u origin main
   ```

## 第二步：部署到 Streamlit Cloud

1. **访问 Streamlit Cloud**
   - 打开 [share.streamlit.io](https://share.streamlit.io)
   - 使用 GitHub 账号登录

2. **创建新应用**
   - 点击 "New app" 按钮
   - 选择你的 GitHub 仓库
   - 主文件路径：`option_screener_gui.py`
   - 应用 URL：选择一个唯一名称

3. **部署**
   - 点击 "Deploy!" 按钮
   - 等待部署完成（通常需要2-5分钟）

## 第三步：测试应用

部署成功后，你会得到一个链接，例如：
`https://your-app-name.streamlit.app`

测试以下功能：
- ✅ 策略选择（现金担保看跌期权/备兑看涨期权）
- ✅ 参数调整
- ✅ 数据获取和筛选
- ✅ 图表显示

## 🔧 如果遇到问题

### 常见错误及解决方案

1. **ModuleNotFoundError**
   - 检查 `requirements.txt` 是否包含所有依赖
   - 确保版本号正确

2. **数据获取失败**
   - 这是正常现象，某些股票可能无法获取数据
   - 尝试使用 AAPL, TSLA 等知名股票测试

3. **应用启动慢**
   - 首次启动需要安装依赖，会比较慢
   - 后续访问会更快

### 查看日志
在 Streamlit Cloud 控制台可以查看详细的部署和运行日志。

## 🎉 部署成功！

恭喜！你的期权筛选器现在可以在线访问了。

**分享你的应用：**
- 发送链接给朋友
- 添加到简历或作品集
- 在社交媒体分享

**持续改进：**
- 修改代码后推送到 GitHub
- Streamlit Cloud 会自动重新部署
- 添加新功能和优化