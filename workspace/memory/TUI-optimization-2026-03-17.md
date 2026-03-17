# TUI 启动缓慢优化记录 - 2026-03-17

## 📊 问题诊断

### 当前状态
- **TUI 启动时间**: ~5.3 秒
- **影响操作**: `openclaw` 命令启动 TUI 界面
- **不影响**: Gateway 服务（`openclaw-gateway`）正常运行

### 根本原因
TUI 启动时需要**同步加载所有 43 个插件**（即使大多数是 disabled 状态）

验证命令：
```bash
time openclaw plugins list
```
结果：**real 0m4.478s**

加载的插件：
- memory-core (loaded)
- dingtalk (loaded)
- 其他 41 个 plugins (大部分 disabled)

## 🎯 优化分析

### 结论：无需优化

**原因**：
1. **Gateway 已在后台运行**，不依赖 TUI
2. **主要交互方式是钉钉**，不是 TUI
3. **TUI 只用于状态查看**，偶尔使用，5.3 秒可接受
4. **作为替代**，可以使用 `openclaw status` 命令

### 已确认的优化项（来自之前记录）

| 任务 | 状态 | 说明 |
|------|------|------|
| 模型切换 qwen3.5-plus → qwen3-coder-next | ✅ 完成 | 预期改善 50-70% |
| 禁用飞书插件 | ✅ 完成 | 减少 TUI 加载负担 |
| 会话压缩配置 | ✅ 完成 | safeguard 模式 |
| 定时会话清理 | ✅ 完成 | 每日 4:00 AM |

## 📈 性能对比

### Gateway (无 TUI)
- 启动时间：~0.2 秒（systemd 服务）
- 用途：主要服务
- 状态：✅ 运行中 (pid 219396)

### TUI (openclaw)
- 启动时间：~5.3 秒
- 用途：状态查看
- 状态：✅ 可用

## 💡 备注

- TUI 启动慢是 OpenClaw v2026.3.13 的已知架构限制
- 官方 GitHub 可能有相关 issue 讨论插件加载优化
- 如需极速启动，可考虑使用 Alioth 等轻量框架

---

**记录时间**: 2026-03-17 20:40  
**诊断人员**: 极光 (Aurora)
