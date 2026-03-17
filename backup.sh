#!/bin/bash
# OpenClaw 自动备份脚本
# 由定时任务调用

BACKUP_TIME=$(date '+%Y-%m-%d %H:%M')
echo "=== OpenClaw 自动备份 ==="
echo "时间: $BACKUP_TIME"
echo ""

# 进入备份目录
cd ~/openclaw-backup || exit 1

# 1. 备份核心配置
echo "1. 备份核心配置..."
cp ~/.openclaw/openclaw.json .
cp ~/.openclaw/cron/jobs.json . 2>/dev/null || echo "警告: 没有定时任务"

# 2. 备份 Agent 身份
echo "2. 备份 Agent 配置..."
mkdir -p agents
cp ~/.openclaw/agents/*/IDENTITY.md agents/ 2>/dev/null || true

# 3. 备份工作区核心文件
echo "3. 备份工作区..."
mkdir -p workspace
cp ~/.openclaw/workspace/*.md workspace/ 2>/dev/null || true

# 统计文件数量
FILE_COUNT=$(find . -type f -not -path './.git/*' | wc -l)

# 4. Git 提交
echo "4. Git 提交..."
git add .
COMMIT_MSG="Daily backup: $BACKUP_TIME"
git commit -m "$COMMIT_MSG" || echo "没有变更需要提交"

# 5. Git 推送
echo "5. Git 推送到 GitHub..."
if git push origin master; then
    PUSH_STATUS="✅ 推送成功"
    echo "$PUSH_STATUS"
else
    PUSH_STATUS="❌ 推送失败"
    echo "$PUSH_STATUS"
fi

echo ""
echo "=== 备份完成 ==="
echo "时间: $(date)"
echo "文件数: $FILE_COUNT"
echo "推送状态: $PUSH_STATUS"

# 返回状态信息（供 Agent 读取）
echo ""
echo "【备份报告】"
echo "备份时间: $BACKUP_TIME"
echo "文件数量: $FILE_COUNT"
echo "推送状态: $PUSH_STATUS"
echo "GitHub: git@github.com:ph-leo/prv.git"
