#!/bin/bash
# 📊 进度检查脚本 - 每小时运行一次
# 用途: 检查测试进度，生成检查报告，提醒异常

set -e

# ==================== 配置 ====================
SSH_CMD="ssh -p 12222 D@127.0.0.1"
PROJECT_DIR="/e/ai_test_MedGemma/ai/other"
CHECK_INTERVAL=3600  # 1小时（秒）
LOG_DIR="/root/.openclaw/workspace/PROJECTS/medgemma-dr-test/check_logs"

# ==================== 函数 ====================

check_ai_service() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检查 AI 服务..."
    $SSH_CMD "curl -s http://localhost:8000/health" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "⚠️  AI 服务响应异常"
        return 1
    else
        echo "✅ AI 服务正常"
        return 0
    fi
}

check_disk_space() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检查磁盘空间..."
    $SSH_CMD "df -h /e | tail -1"
    available=$($SSH_CMD "df -h /e | tail -1 | awk '{print \$4}'" 2>/dev/null)
    echo "   可用空间: $available"
    
    # 如果可用空间小于 10GB，警告
    available_gb=$(echo $available | sed 's/GB//' 2>/dev/null || echo "100")
    if [ "$available_gb" -lt 10 ] 2>/dev/null; then
        echo "⚠️  磁盘空间不足！"
        return 1
    fi
    return 0
}

check_test_progress() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检查测试进度..."
    
    # 检查测试脚本是否运行
    $SSH_CMD "ps aux | grep full_test_v7.4 | grep -v grep"
    if [ $? -ne 0 ]; then
        echo "⚠️  测试脚本未运行"
        return 1
    fi
    
    # 检查最后更新时间
    last_update=$($SSH_CMD "find $PROJECT_DIR/test_results/v7.4_300cases -name 'summary_report_*.md' -mmin -$((CHECK_INTERVAL/60)) 2>/dev/null | wc -l")
    
    if [ "$last_update" -eq 0 ]; then
        echo "⚠️  进度报告超过 1 小时未更新！"
        return 1
    else
        echo "✅ 进度报告已更新"
        return 0
    fi
}

check_completed_cases() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检查完成案例数..."
    
    completed_count=$($SSH_CMD "ls $PROJECT_DIR/test_results/v7.4_300cases/summary_report_*.md 2>/dev/null | wc -l" || echo "0")
    json_count=$($SSH_CMD "ls $PROJECT_DIR/test_results/v7.4_300cases/*_result.json 2>/dev/null | wc -l" || echo "0")
    
    echo "   Markdown 报告: $completed_count"
    echo "   JSON 结果: $json_count"
    
    if [ "$json_count" -gt 0 ]; then
        echo "✅ 有完成的测试案例"
        return 0
    else
        echo "⚠️  没有完成的测试案例（可能还在启动中）"
        return 1
    fi
}

check_running_time() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检查运行时间..."
    
    running_info=$($SSH_CMD "ps -eo pid,etime,cmd | grep full_test_v7.4 | grep -v grep | awk '{print \$2, \$3}'" 2>/dev/null || echo "Not running")
    echo "   运行信息: $running_info"
}

generate_status_report() {
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local report_file="$LOG_DIR/status_$timestamp.md"
    
    mkdir -p "$LOG_DIR"
    
    cat > "$report_file" << EOF
# 📊 进度检查报告 - $timestamp

## 检查时间
检查时间: $(date '+%Y-%m-%d %H:%M:%S')

## 检查结果

### AI 服务
$(check_ai_service 2>&1)

### 磁盘空间  
$(check_disk_space 2>&1)

### 测试进度
$(check_test_progress 2>&1)

### 完成案例
$(check_completed_cases 2>&1)

### 运行时间
$(check_running_time 2>&1)

## 总体状态
$(if [ $? -eq 0 ]; then echo "✅ 正常"; else echo "⚠️ 异常"; fi)

## 下一步行动
$(if [ $? -eq 0 ]; then echo "继续监控"; else echo "需要人工干预"; fi)
EOF
    
    echo "✅ 检查报告已生成: $report_file"
    cat "$report_file"
}

# ==================== 主流程 ====================

main() {
    echo "========================================"
    echo "📊 进度检查脚本 v1.0"
    echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "========================================"
    
    # 创建日志目录
    mkdir -p "$LOG_DIR"
    
    # 执行所有检查
    all_passed=true
    
    check_ai_service || all_passed=false
    echo ""
    
    check_disk_space || all_passed=false
    echo ""
    
    check_test_progress || all_passed=false
    echo ""
    
    check_completed_cases || all_passed=false
    echo ""
    
    check_running_time
    echo ""
    
    # 生成状态报告
    generate_status_report
    
    # 检查总体状态
    if [ "$all_passed" = true ]; then
        echo ""
        echo "✅ 所有检查通过，测试正常进行"
        echo "下次检查时间: $(date -d '+$CHECK_INTERVAL seconds' '+%H:%M:%S')"
    else
        echo ""
        echo "⚠️ 部分检查失败，请查看检查报告"
        echo "⚠️ 需要人工干预"
    fi
}

# ==================== 入口 ====================

case "${1:-auto}" in
    "auto")
        main
        ;;
    "check")
        check_ai_service
        check_disk_space
        check_test_progress
        check_completed_cases
        ;;
    "report")
        generate_status_report
        ;;
    "run")
        # 每小时运行一次（守护模式）
        while true; do
            main
            sleep $CHECK_INTERVAL
        done
        ;;
    *)
        echo "用法: $0 {auto|check|report|run}"
        ;;
esac
