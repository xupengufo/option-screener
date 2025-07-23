# 期权筛选器部署指南

## 部署选项对比

| 平台 | 类型 | 优点 | 缺点 | 推荐度 |
|------|------|------|------|--------|
| **Vercel** | 静态网站 | 免费、快速、CDN | 无后端支持 | ⭐⭐⭐⭐⭐ |
| **Cloudflare Pages** | 静态网站 | 免费、全球CDN | 无后端支持 | ⭐⭐⭐⭐⭐ |
| **Netlify** | 静态网站 | 免费、易用 | 无后端支持 | ⭐⭐⭐⭐ |
| **GitHub Pages** | 静态网站 | 完全免费 | 功能有限 | ⭐⭐⭐ |
| **Streamlit Cloud** | 动态应用 | 支持Python | 需要真实数据源 | ⭐⭐⭐⭐ |

## 方案1: 部署到 Vercel (推荐)

### 步骤1: 准备文件
确保你有以下文件：
- `index.html` (主页面)
- `vercel.json` (配置文件，可选)

### 步骤2: 创建 vercel.json (可选)
```json
{
  "functions": {
    "app.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    { "src": "/", "dest": "/index.html" }
  ]
}
```

### 步骤3: 部署方法

#### 方法A: 通过 Vercel CLI
```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录
vercel login

# 部署
vercel

# 生产环境部署
vercel --prod
```

#### 方法B: 通过 GitHub 集成
1. 将代码推送到 GitHub 仓库
2. 访问 [vercel.com](https://vercel.com)
3. 点击 "New Project"
4. 选择你的 GitHub 仓库
5. 点击 "Deploy"

### 步骤4: 自定义域名 (可选)
在 Vercel 控制台中可以添加自定义域名。

## 方案2: 部署到 Cloudflare Pages

### 步骤1: 通过 GitHub 集成
1. 访问 [pages.cloudflare.com](https://pages.cloudflare.com)
2. 点击 "Create a project"
3. 连接你的 GitHub 账户
4. 选择仓库
5. 配置构建设置：
   - Build command: (留空)
   - Build output directory: `/`
6. 点击 "Save and Deploy"

### 步骤2: 通过 Wrangler CLI
```bash
# 安装 Wrangler
npm install -g wrangler

# 登录
wrangler login

# 创建项目
wrangler pages project create option-screener

# 部署
wrangler pages publish . --project-name=option-screener
```

## 方案3: 部署到 Netlify

### 步骤1: 拖拽部署
1. 访问 [netlify.com](https://netlify.com)
2. 将包含 `index.html` 的文件夹拖拽到部署区域
3. 等待部署完成

### 步骤2: 通过 Git 集成
1. 将代码推送到 GitHub
2. 在 Netlify 中连接 GitHub 仓库
3. 配置构建设置并部署

## 方案4: 部署到 GitHub Pages

### 步骤1: 创建仓库
1. 在 GitHub 创建新仓库
2. 上传 `index.html` 文件

### 步骤2: 启用 GitHub Pages
1. 进入仓库设置
2. 找到 "Pages" 部分
3. 选择源分支 (通常是 `main`)
4. 保存设置

### 步骤3: 访问网站
网站将在 `https://username.github.io/repository-name` 可用

## 方案5: Streamlit Cloud (动态版本)

### 前提条件
- 需要修改代码以使用真实的金融API
- 需要处理API密钥和限制

### 步骤1: 准备代码
```python
# requirements.txt
streamlit
yfinance
pandas
plotly
```

### 步骤2: 部署到 Streamlit Cloud
1. 将代码推送到 GitHub
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 连接 GitHub 仓库
4. 选择 `option_screener_gui.py`
5. 点击 "Deploy"

## 添加真实数据源

### 免费API选项
1. **Alpha Vantage** - 免费层每天500次请求
2. **IEX Cloud** - 免费层每月50万次请求
3. **Yahoo Finance** (通过yfinance) - 免费但有限制
4. **Polygon.io** - 免费层每分钟5次请求

### 示例：集成 Alpha Vantage API
```javascript
// 在 index.html 中添加
async function getRealStockData(ticker) {
    const API_KEY = 'YOUR_API_KEY';
    const url = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${ticker}&apikey=${API_KEY}`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        return {
            symbol: ticker,
            price: parseFloat(data['Global Quote']['05. price'])
        };
    } catch (error) {
        throw new Error('无法获取股票数据');
    }
}
```

## 环境变量配置

### Vercel
```bash
# 设置环境变量
vercel env add API_KEY
```

### Cloudflare Pages
在 Cloudflare 控制台的 "Settings" > "Environment variables" 中添加。

### Netlify
在 Netlify 控制台的 "Site settings" > "Environment variables" 中添加。

## 性能优化建议

1. **启用缓存**: 对API响应进行缓存
2. **压缩资源**: 启用Gzip压缩
3. **CDN加速**: 利用平台提供的CDN
4. **懒加载**: 按需加载图表库
5. **错误处理**: 添加完善的错误处理机制

## 监控和分析

### 添加 Google Analytics
```html
<!-- 在 index.html 的 <head> 中添加 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 安全考虑

1. **API密钥保护**: 使用环境变量存储API密钥
2. **CORS设置**: 正确配置跨域请求
3. **输入验证**: 验证用户输入
4. **速率限制**: 实现客户端速率限制

## 故障排除

### 常见问题
1. **部署失败**: 检查文件路径和权限
2. **API调用失败**: 验证API密钥和配额
3. **样式问题**: 检查CSS文件路径
4. **JavaScript错误**: 查看浏览器控制台

### 调试技巧
1. 使用浏览器开发者工具
2. 检查网络请求
3. 查看控制台错误
4. 测试不同浏览器

## 总结

对于你的期权筛选器项目，我推荐：

1. **快速原型**: 使用当前的 HTML 版本部署到 Vercel
2. **生产环境**: 集成真实API后部署到 Cloudflare Pages
3. **高级功能**: 考虑使用 Streamlit Cloud 部署动态版本

选择哪个平台主要取决于你的具体需求和技术栈偏好。