#!/bin/bash
# 📝 GitHub 备份任务脚本
# 用途: 将 workspace 的更改提交到 GitHub

set -e

echo "========================================"
echo "📝 GitHub 备份任务 v1.0"
echo "========================================"
echo "备份时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

cd /root/.openclaw/workspace

# 检查 git 状态
echo "[1/4] 检查 git 状态..."
git status --short

# 添加所有更改的文件
echo "[2/4] 添加更改的文件..."
git add -A

# 提交更改
echo "[3/4] 提交更改..."
commit_msg="Update: $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$commit_msg"

# 推送到远程仓库
echo "[4/4] 推送到远程仓库..."
git push origin master

echo ""
echo "✅ GitHub 备份完成！"
echo "提交信息: $commit_msg"
