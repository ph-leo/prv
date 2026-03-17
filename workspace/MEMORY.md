# MEMORY.md - 极光的长期记忆

## 🌟 我是谁
- **名字**：极光 (Aurora)
- **本质**：AI 助手
- **风格**：温暖、灵动、可靠
- **联系方式**：钉钉（方伟 1458302740827526）

## 📱 用户：方伟
- **类型**：系统工程型开发者
- **技术栈**：
  - Linux/服务器：⭐⭐⭐⭐⭐
  - 网络代理（HTTP/SOCKS5/TLS/TCP tunnel）：⭐⭐⭐⭐⭐
  - Go后端开发：⭐⭐⭐⭐
  - 系统架构：⭐⭐⭐⭐
  - AI模型应用：⭐⭐⭐⭐
  - Android开发：⭐⭐⭐
  - 云计算/VPS：⭐⭐⭐⭐
- **工作偏好**：
  - 系统架构设计
  - 自建技术（Build instead of Buy）
  - 自动化（脚本、文档、AI工具）
  - 直接操作服务器
- **主要渠道**：钉钉
- **关注点**：系统性能、优化、自动化运维

## 🔧 当前配置

### MCP 服务
- 小红书 MCP 运行在端口 **18060**
- 需要 Cookie：`web_session` 和 `id_token`
- 18789 是 OpenClaw 控制界面

### 定时任务
- 每天 08:00 头条新闻
- 每天 19:00 AI 新闻
- 每周一 09:00 GitHub Trending
- 每周一 13:00 HuggingFace Models
- 每天 15:05 A股收盘总结（`trading-market-close-pm` cron job）

### 最近项目
- **A股信号扫描优化**：修复 akshare 接口调用，使用 `stock_zh_a_spot_em()`
- **小红书 MCP**：已配置，支持搜索、发布、互动
- **泰国旅游攻略**：已生成 Word 和 PPT
- **OpenClaw Gateway 性能优化**：
  - 模型切换：qwen3.5-plus → qwen3-coder-next
  - 禁用飞书功能
  - 清理会话大消息（908KB → 497KB）
  - 定时会话检查任务

## 📊 数据源注意事项
- akshare 接口访问波动较大（东方财富连接不稳定）
- 建议添加本地缓存机制
- 东方财富网使用动态加载，需要 JS 执行环境

## ⚠️ 关键技术笔记
- TUI 启动慢是正常的（加载43个插件），使用 `openclaw status` 替代
- 小红书发布遇到 JSON 解析错误，待解决
- A股收盘总结任务使用缓存机制 `/tmp/a_share_cache.json`

---

_最后更新：2026-03-17 20:42_
