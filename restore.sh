#!/bin/bash
# OpenClaw 恢复脚本
# 用法: ./restore.sh

echo "=== OpenClaw 恢复 ==="
echo "时间: $(date)"

# 检查目标目录
if [ -d ~/.openclaw ]; then
    echo "警告: ~/.openclaw 已存在"
    read -p "是否覆盖? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "取消恢复"
        exit 1
    fi
    mv ~/.openclaw ~/.openclaw.bak.$(date +%Y%m%d_%H%M%S)
fi

# 创建目录
mkdir -p ~/.openclaw

# 恢复核心配置
cp openclaw.json ~/.openclaw/
cp jobs.json ~/.openclaw/cron/ 2>/dev/null || true

# 恢复 Agent 配置
mkdir -p ~/.openclaw/agents
cp -r agents/* ~/.openclaw/agents/ 2>/dev/null || true

# 恢复工作区
mkdir -p ~/.openclaw/workspace
cp -r workspace/* ~/.openclaw/workspace/ 2>/dev/null || true

echo "恢复完成!"
echo "请运行: openclaw gateway restart"
