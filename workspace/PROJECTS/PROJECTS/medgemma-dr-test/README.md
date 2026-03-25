# A股模拟操盘系统

## 项目说明

本系统是为每天09:30 A股开盘时自动扫描S1级别强信号（≥95%）的模拟交易平台。

## 功能模块

### 1. 账户管理 (`TradingAccount`)
- 初始化5万元模拟账户
- 买入/卖出交易记录
- 持仓管理与成本价计算
- 投资组合价值更新
- 盈亏报告生成

### 2. 信号扫描 (`scan_s1_strong_signals`)
- 扫描S1级别强信号（信号强度≥95%）
- 信号强度计算基于：
  - 价格动量 (30%)
  - 开盘价位置 (20%)
  - 成交额放大 (15%)
  - 价格位置 (20%)
  - 涨停状态 (15%)

### 3. 交易管理
- 待确认交易记录 (`confirmed_trades.json`)
- 交易状态：pending（待确认）、confirmed（已执行）、skipped（跳过）

### 4. 日志记录
- 信号历史 (`signal_history.json`)
- 每日扫描日期记录

## 文件说明

| 文件 | 说明 |
|------|------|
| `trading_simulation.py` | 主脚本，包含所有核心功能 |
| `trading_account.json` | 账户状态文件 |
| `signal_history.json` | 信号历史记录 |
| `confirmed_trades.json` | 待确认/已确认交易列表 |
| `README.md` | 项目说明文档 |

## 运行说明

### 基本运行
```bash
cd /root/.openclaw/workspace/PROJECTS/medgemma-dr-test
python3 trading_simulation.py
```

### 数据重置
```bash
# 清除历史扫描记录（允许当天重新扫描）
rm -f signal_history.json

# 清除所有数据（重置系统）
rm -f signal_history.json confirmed_trades.json trading_account.json
```

## 预设股票池

当前系统使用预设股票池数据进行演示：
- sh600000 浦发银行（S1信号）
- sz000001 平安银行（S1信号）
- sh600036 招商银行（S2信号）
- sz002475 立讯精密（S2信号）

## 下一步

- 集成稳定A股数据源（akshare数据接口不稳定）
- 实现用户确认交易逻辑
- 添加10天盈亏报告生成功能
- 集成钉钉消息通知
