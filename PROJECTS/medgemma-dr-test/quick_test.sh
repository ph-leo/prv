#!/bin/bash
# MedGemma DR 测试快速启动脚本
# Usage: ./quick_test.sh
# 注意：此脚本需要在开发电脑上通过 SSH 连接后执行

set -e

echo "========================================"
echo "MedGemma DR 测试快速启动 v1.0"
echo "========================================"

# 连接开发电脑后执行的命令
SSH_CMD="ssh -p 12222 D@127.0.0.1"

# 检查 AI 服务
echo "[1/3] 检查 AI 服务状态..."
$SSH_CMD "curl -s http://localhost:8000/health | head -1"
if [ $? -ne 0 ]; then
    echo "❌ AI 服务未响应！请先启动 medgemma_api_plus.py"
    exit 1
fi

# 导航到项目目录
echo "[2/3] 导航到项目目录..."
$SSH_CMD "cd /e/ai_test_MedGemma/ai/other && pwd"

# 执行测试
echo "[3/3] 开始测试（约 30-40 分钟）..."
$SSH_CMD "cd /e/ai_test_MedGemma/ai/other && python scripts/full_test_v7.4_300cases.py"

echo ""
echo "========================================"
echo "测试完成！"
echo "========================================"
echo ""
echo "生成的文件："
$SSH_CMD "ls -1 /e/ai_test_MedGemma/ai/other/测试记录_V7.2_*.xlsx 2>/dev/null | sed 's|/e/ai_test_MedGemma/ai/other/||'"
$SSH_CMD "ls -1 /e/ai_test_MedGemma/ai/other/test_results/v7.4_300cases/summary_report_*.md 2>/dev/null | sed 's|/e/ai_test_MedGemma/ai/other/||'"
echo ""
echo "请将生成的文件名发送给负责人"
