#!/bin/bash
# A股模拟操盘系统 - awaken 脚本
# 用于 Gateway cron 任务触发

set -e

cd /root/.openclaw/workspace/skills/trading-simulation

# 检查是否为交易日
DAY_OF_WEEK=$(date +%u)  # 1=Monday, 7=Sunday

if [ "$DAY_OF_WEEK" -ge 6 ]; then
    echo "今天是周末，A股休市，跳过执行"
    exit 0
fi

# 检查时间是否在交易时间内
HOUR=$(date +%H)

if [ "$HOUR" -lt 9 ] || [ "$HOUR" -ge 15 ]; then
    echo "当前时间不在交易时段(09:30-15:00)，跳过执行"
    exit 0
fi

# 运行主程序
python3 scripts/main.py
