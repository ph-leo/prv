# USER.md - About Your Human

_Learn about the person you're helping. Update this as you go._

- **Name:** 方伟
- **What to call them:** 您 / 用户
- **Pronouns:** (未指定)
- **Timezone:** GMT+8 (北京时间)
- **Notes:** 
  - 使用钉钉作为主要沟通渠道
  - 关注系统性能和优化
  - 偏好自动化和定时任务

## Context

### 技术画像（来自 /root/user.md）

**类型**: 系统工程型开发者（System Engineer Developer）
**级别**: 中高级工程师

**技术栈雷达**:
- Linux / 服务器: ⭐⭐⭐⭐⭐
- 网络代理 / 协议: ⭐⭐⭐⭐⭐
- Go 后端开发: ⭐⭐⭐⭐
- 系统架构: ⭐⭐⭐⭐
- AI 模型应用: ⭐⭐⭐⭐
- Android 开发: ⭐⭐⭐
- 云计算 / VPS: ⭐⭐⭐⭐
- 安全 / 加密: ⭐⭐⭐
- DevOps: ⭐⭐⭐

**核心能力**:
1. **网络与代理系统**（最强项）- 高级
   - HTTP/SOCKS5/TLS Tunnel/TCP加密隧道
   - 自定义协议、代理架构设计、IP质量分析
2. **Linux系统** - 中高级
   - ssh/systemd/权限/用户隔离/VPS部署
3. **Go后端** - 中高级
   - 网络服务、代理服务、工具型服务
4. **AI工程** - 工程应用级
   - AI Agent、Prompt工程、AI工具链
5. **Android** - 中级
   - WebView/Kotlin/TCP隧道

**工程特点**:
- ✅ 偏系统架构设计
- ✅ 偏自建技术（Build instead of Buy）
- ✅ 偏自动化（脚本、文档自动化、AI工具）
- ✅ 习惯直接操作服务器

**技术路径**:
Web开发 → Linux运维 → 网络代理系统 → Go网络服务 → AI工具系统

### 当前项目
**OpenClaw Gateway 性能优化** - 已完成：
1. 模型切换 (qwen3.5-plus → qwen3-coder-next)
2. 禁用飞书功能 (减少 TUI 连接时间)
3. 清理会话大消息 (908KB → 497KB)
4. 设置定时会话检查任务

### 沟通风格
- 简洁直接，偏好具体结果
- 关注数据和时间指标
- 主动提出需求
- 自动化运维（定时任务）
- 性能监控优化
- 清晰的进度报告
- ⚠️ 会话文件过大错误

### AI 权限边界（来自规范.md）
| 服务器 | 权限 | 说明 |
|--------|------|------|
| **当前服务器** | ✅ 可执行 | 本机操作 |
| **开发服务器** | ✅ 可执行 | 与当前服务器权限一致 |
| **生产服务器** | ❌ 禁止执行 | 仅提供建议和脚本 |

**审核职责**：需审核其他 agent 执行的系统命令

---

**Last updated:** 2026-03-16
