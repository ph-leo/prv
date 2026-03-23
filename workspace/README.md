# OpenClaw 配置备份

## 说明

这是 OpenClaw 的核心配置备份，用于服务器迁移时快速恢复。

## 包含内容

- `openclaw.json` - 核心配置文件（模型、通道、Agent等）
- `jobs.json` - 定时任务配置
- `agents/` - Agent 身份配置
- `workspace/` - 工作区核心文件
- `backup.sh` - 备份脚本
- `restore.sh` - 恢复脚本

## 使用方法

### 备份（在旧服务器）

```bash
./backup.sh
git add .
git commit -m "备份 OpenClaw 配置"
git push origin main
```

### 恢复（在新服务器）

```bash
# 1. 克隆仓库
git clone git@github.com:ph-leo/prv.git
cd prv

# 2. 运行恢复脚本
./restore.sh

# 3. 重启 Gateway
openclaw gateway restart
```

## 注意事项

- 此备份**不包含**技能目录（skills/），需要重新安装
- 不包含会话文件（sessions/），历史会话会丢失
- 不包含媒体文件（media/）
- 需要重新配置敏感信息（API Key等）

## 手动安装技能

恢复后需要重新安装技能：

```bash
# 示例：安装 team-tasks
openclaw skills install team-tasks

# 安装其他技能...
```

## 检查清单

恢复后请检查：

- [ ] Gateway 正常运行
- [ ] 所有 Agent 已加载
- [ ] 定时任务配置正确
- [ ] 钉钉/飞书通道正常
- [ ] API Key 已配置
