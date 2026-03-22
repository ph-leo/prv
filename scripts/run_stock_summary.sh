#!/bin/bash
# A股收盘总结定时任务脚本
# 执行时间：每天 15:10

cd /root/.openclaw/workspace

# 执行Python脚本并记录日志
python3 scripts/stock_market_close_summary.py 2>&1 | tee logs/stock_summary_$(date +%Y%m%d_%H%M%S).log

# 检查脚本是否成功执行
if [ $? -eq 0 ]; then
    echo "收盘总结生成成功"
    
    # 发送到钉钉群（使用curl发送webhook）
    # 请根据实际钉钉机器人配置修改以下参数
    DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=YOUR_ACCESS_TOKEN"
    SUMMARY_FILE="/root/.openclaw/workspace/stock_summary.txt"
    
    if [ -f "$SUMMARY_FILE" ]; then
        MESSAGE=$(cat "$SUMMARY_FILE")
        curl "$DINGTALK_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"msgtype\": \"text\", \"text\": {\"content\": \"$MESSAGE\"}}"
    fi
else
    echo "收盘总结生成失败"
    exit 1
fi
