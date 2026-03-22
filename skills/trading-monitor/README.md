# A-Share S1 Signal Monitor

## Overview

A-share stock S1 signal monitoring system using akshare. Detects high-confidence signals (≥95%) during trading hours and sends immediate notifications to DingTalk groups.

## Trigger Times

- **S1 Monitoring**: 10:00 AM daily (during trading hours)
- **Data Sources**: Sina Finance (main), Eastmoney (fallback)

## Quick Start

```bash
# Test mode - no notification
python3 scripts/monitor_s1_signals.py --test

# Full monitoring - with DingTalk notification
export DINGTALK_WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=xxx"
export DINGTALK_SECRET="SECxxx"
python3 scripts/monitor_s1_signals.py
```

## Signal Detection

### S1 Criteria (≥95% confidence)
- **Price movement**: >5% gain contributes 0.25 points
- **Volume**: >500K shares contributes 0.20 points
- **Market strength**: Positive momentum adds 0.10 points

### Scoring Components
- Price movement: 0-30 points
- Volume: 0-30 points  
- Volatility: 0-20 points
- Market strength: 0-20 points

## Resources

### scripts/
- `monitor_s1_signals.py` - Main monitoring script for S1 signal detection
- `send_dingtalk_alert.py` - DingTalk notification delivery

### references/
- `signal_criteria.md` - Complete S1 signal detection criteria and thresholds
- `akshare_api.md` - akshare API documentation for A-share data

## Cron Setup

Add to crontab for daily 10:00 monitoring:
```bash
0 10 * * * cd /root/.openclaw/workspace/skills/trading-monitor && DINGTALK_WEBHOOK_URL="xxx" python3 scripts/monitor_s1_signals.py
```

## Notes

- **Data Sources**: Sina Finance is the primary source, Eastmoney is secondary
- **Availability**: Data availability may vary by network conditions
- **Signal Threshold**: Adjust confidence threshold in `detect_s1_signals()` if needed
- **Test First**: Always test with `--test` flag before enabling production alerts
