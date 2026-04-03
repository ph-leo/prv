# MEMORY.md - 长期记忆

## 2026-03-24 任务失败总结

**任务**：获取 HuggingFace 本周热门模型（前5个）  
**状态**：❌ 失败（4次尝试全部失败）

**失败原因**：
1. `agentId is not allowed` - workspace 未配置 huggingface-trending agent
2. `missing_brave_api_key` - 未配置 Brave Search API
3. `fetch failed` - 网络连接问题，无法访问 HuggingFace
4. `browser timed out` - OpenClaw Gateway 浏览器服务异常

**解决方案**：
- 短期：手动访问 https://huggingface.co/models 获取数据
- 长期：创建 Python 脚本 + cron job 定时执行

**技术限制**：
- 当前服务器可能被防火墙限制出站访问
- 代理端口 55555 已关闭（临时使用规则）
- OpenClaw Gateway 服务需重启（gateway.bind 问题？）

---

## 2026-03-31 A股模拟交易 API受限事件

**事件**：A股模拟交易系统无法获取实时行情数据  
**状态**：⚠️ 跳过今日交易（连续失败 >6小时）

**API失败记录**（2026-03-31）：
| 尝试时间 | API | 状态 | 说明 |
|---------|-----|------|------|
| 04:20 | 新浪财经 hq.sinajs.cn | ❌ 403 Forbidden | 持续被屏蔽 |
| 04:50 | 新浪财经 hq.sinajs.cn | ❌ 403 Forbidden | 重复失败 |
| 05:20 | 新浪财经 hq.sinajs.cn | ❌ 403 Forbidden | 仍被屏蔽 |

**根因分析**：
1. 服务器出口 IP 被 A 股 API 提供商屏蔽（影响 99% 的公开数据源）
2. SSH 隧道（端口 12222）需要动态验证码，无法完全自动化
3. 临时代理（端口 55555）未运行

**已生成的缓存数据**：
- `/PROJECTS/stock-trading-sim/DATA_20260330.md` - 2026-03-30 数据检查报告
- `/PROJECTS/stock-trading-sim/DATA_20260331.md` - 2026-03-31 数据检查报告

**后续计划**：
1. 短期：启用代理服务或使用浏览器自动化工具模拟登录
2. 中期：探索其他可用数据源（akshare、聚源等）
3. 长期：申请正式 API Key 或使用付费数据服务

**已记录文件**：
- 交易报告：`/PROJECTS/stock-trading-sim/TRADE_20260331.md`
- 数据报告：`/PROJECTS/stock-trading-sim/DATA_20260331.md`
