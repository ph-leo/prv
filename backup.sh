#!/bin/bash
# OpenClaw 备份脚本
# 用法: ./backup.sh

echo "=== OpenClaw 备份 ==="
echo "时间: $(date)"

# 备份核心配置
cp ~/.openclaw/openclaw.json .
cp ~/.openclaw/cron/jobs.json . 2>/dev/null || echo "警告: 没有定时任务"

# 备份 Agent 身份
mkdir -p agents
cp ~/.openclaw/agents/*/IDENTITY.md agents/ 2>/dev/null || true

# 备份工作区核心文件
mkdir -p workspace
cp ~/.openclaw/workspace/*.md workspace/ 2>/dev/null || true

echo "备份完成!"
echo "文件列表:"
ls -la
echo ""
echo "Git 状态:"
git status --short
