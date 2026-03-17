# A股模拟操盘系统 - 完整文档

## 📋 项目概述

这是一个专业的A股模拟交易系统，提供开盘信号扫描、智能强度评级和10天模拟交易周期。

## 🏗️ 技术架构

```
trading-simulation/
├── SKILL.md                    # 技能说明（主文档）
├── README.md                   # 用户指南
├── CONFIG.md                   # 配置说明
├── awaken.sh                   # Gateway cron 唤醒脚本
├── scripts/
│   ├── main.py                # 主程序入口
│   ├── test_indicators.py     # 信号强度测试
│   └── test_engine.py         # 交易引擎测试
└── refs/
    ├── akshare_stock_indicators.py    # 信号计算模块
    └── simulation_engine.py          # 交易引擎模块
```

## 🚀 快速开始

### 安装依赖

```bash
pip install akshare pandas numpy
```

### 运行测试

```bash
cd /root/.openclaw/workspace/skills/trading-simulation
python3 scripts/test_engine.py
python3 scripts/test_indicators.py
```

### 运行主程序

```bash
python3 scripts/main.py
```

### Cron 任务配置

```yaml
cron:
  - name: trading-simulation-50k
    schedule:
      kind: cron
      expr: "30 9 * * 1-5"  # 每周一至周五 09:30
      tz: "Asia/Shanghai"
    payload:
      kind: systemEvent
      text: "【A股模拟操盘 - 5万元】"
    sessionTarget: main
    enabled: true
```

## 📊 核心功能

### 1. 信号强度评级

| 等级 | 强度 | 说明 | 操作建议 |
|------|------|------|----------|
| S1 | ≥95% | 强力推荐 | 逢低建仓 |
| S2 | ≥85% | 考虑交易 | 可以考虑 |
| S3 | ≥70% | 观察 | 建议观察 |
| D | <70% | 观望 | 信号较弱 |

### 2. 信号算法

系统使用4个维度计算信号强度（0-100%）：

1. **涨跌幅** (40%): 收益越高，强度越大
2. **成交量** (30%): 成交额越大，热度越高
3. **价格位置** (20%): 高价股往往更强
4. **稳定性** (10%): 价格越稳定，信号越可靠

### 3. 交易流程

```
每日09:30 → 扫描信号 → 发现S1信号 → 发送通知 → 
等待确认 → 执行交易 → 持有10天 → 生成报告
```

## 📁 文件说明

### scripts/

- **main.py**: 主程序入口，扫描信号并模拟交易
- **test_indicators.py**: 信号强度测试脚本
- **test_engine.py**: 交易引擎测试脚本

### refs/

- **akshare_stock_indicators.py**: 信号强度计算模块
- **simulation_engine.py**: 交易引擎模块

## 🎯 使用场景

- 学习股票交易技巧
- 测试交易策略
- 体验A股开盘节奏
- 信号强度评估训练
- 定时任务集成（每天09:30自动扫描）

## ⚠️ 注意事项

1. 本系统为模拟交易，不涉及真实资金
2. 信号基于历史数据和技术指标，不构成投资建议
3. 模拟交易不考虑印花税、手续费等交易成本
4. 请谨慎对待实际投资决策

## 📞 支持

如有问题或建议，请查看对应文档或运行测试脚本。

---

**版本**: v1.0  
**最后更新**: 2026-03-17  
**作者**: OpenClaw AI Assistant
