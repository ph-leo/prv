#!/bin/bash
# A股盘前信号扫描机器人 - 定时任务脚本
# 执行时间: 每天 08:30（A股开盘前）

cd /root/.openclaw/workspace/PROJECTS/trading-signals-morning

# 激活虚拟环境
source venv/bin/activate

# 设置钉钉Webhook（如果已配置）
if [ -n "$DINGTALK_WEBHOOK" ]; then
    export DINGTALK_WEBHOOK
fi

# 运行脚本
python main.py
