# 📈 A股模拟操盘系统

专业A股模拟交易系统，提供开盘信号扫描、智能评级和10天模拟周期。

## 🚀 快速开始

### 安装依赖

```bash
pip install akshare pandas numpy
```

### 运行模拟

```bash
python scripts/main.py
```

## 📊 系统功能

### 1. 开盘信号扫描
- **扫描时间**: 每日09:30（A股开盘）
- **扫描范围**: 沪深京A股全市场
- **信号频率**: 实时扫描

### 2. 信号强度评级

| 等级 | 强度 | 说明 | 操作建议 |
|------|------|------|----------|
| S1 | ≥95% | 强力推荐 | 逢低建仓 |
| S2 | ≥85% | 考虑交易 | 可以考虑 |
| S3 | ≥70% | 观察 | 建议观察 |
| D | <70% | 观望 | 信号较弱 |

### 3. 模拟交易流程

```
每日09:30 → 扫描信号 → 发现S1信号 → 发送通知 → 
等待确认 → 执行交易 → 持有10天 → 生成报告
```

### 4. 盈亏报告

10天后生成详细报告：
- 总收益/亏损
- 胜率统计
- 持仓分析
- 交易记录

## 🛠️ 技术架构

```
trading-simulation/
├── SKILL.md                    # 技能说明
├── scripts/
│   └── main.py                # 主程序入口
├── refs/
│   ├── akshare_stock_indicators.py    # 信号计算
│   └── simulation_engine.py          # 交易引擎
└── tests/
    ├── test_indicators.py     # 信号测试
    └── test_engine.py         # 引擎测试
```

## 📈 数据来源

- **数据源**: akshare (Python股票数据库)
- **覆盖范围**: 沪深京A股
- **更新频率**: 实时行情

## ⚙️ 配置说明

### 定时任务配置 (Gateway)

```yaml
cron:
  - name: trading-simulation-50k
    schedule:
      kind: every
      everyMs: 86400000  # 每天一次
    payload:
      kind: systemEvent
      text: "【A股模拟操盘 - 5万元】"
    sessionTarget: main
    enabled: true
```

## 📝 使用场景

1. **学习交易技巧** - 无风险体验交易流程
2. **测试交易策略** - 验证信号有效性
3. **熟悉A股节奏** - 了解开盘动态
4. **评估信号质量** - 训练信号识别能力

## ⚠️ 重要提示

1. 本系统为模拟交易，不涉及真实资金
2. 信号基于历史数据和技术指标，不构成投资建议
3. 模拟交易不考虑印花税、手续费等交易成本
4. 请谨慎对待实际投资决策

## 🤝 贡献指南

欢迎提交Issue和PR！

1. Fork本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

MIT License - see LICENSE file for details

## 🙏 致谢

- akshare: https://akshare.xyz/
- OpenClaw: https://github.com/openclaw

---

**🌟 让模拟交易成为你的训练场！**
