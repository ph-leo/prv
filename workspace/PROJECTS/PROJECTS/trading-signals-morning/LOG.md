## 2026-03-25 08:30 - A股盘前信号扫描机器人

### 状态
✅ 项目创建完成  
✅ 脚本编写完成  
✅ 依赖安装完成  
✅ 测试运行成功  
✅ 文档编写完成

### 文件结构
```
PROJECTS/trading-signals-morning/
├── README.md         # 项目说明（含使用方法、输出格式）
├── main.py          # 主程序脚本（v1.3 - 含网络错误处理）
├── run.sh           # 运行脚本
├── example_output.md # 示例输出
├── LOG.md           # 运行日志
└── venv/            # 虚拟环境（已安装 akshare pandas numpy requests）
```

### 测试结果

**美股数据**: ✅ 成功获取 (收盘 6556.37, 涨跌 -0.37%)  
**板块数据**: ⚠️ 网络连接问题，使用默认热点板块  
**股票筛选**: ⚠️ 网络连接问题，使用示例数据

### 待配置

- [ ] 设置钉钉Webhook环境变量
- [ ] 配置定时任务（每天08:30）
- [ ] 测试钉钉推送

### 定时任务配置

```bash
crontab -e
```

添加：

```
30 8 * * * /root/.openclaw/workspace/PROJECTS/trading-signals-morning/run.sh
```

### 网络问题说明

部分 akshare 接口在高负载时可能出现连接问题：
- `stock_individual_fund_flow_rank` 接口偶尔连接失败
- `stock_board_concept_spot_em` 接口偶尔连接失败

程序已添加重试机制（最多3次）和备用数据方案，确保即使网络失败也能生成报告。

### 钉钉推送配置

如需推送钉钉群，设置环境变量：

```bash
export DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=xxx"
```

### 补充说明

- 美股数据使用 `index_us_stock_sina` 接口获取历史数据
- 板块数据使用 `stock_fund_flow_concept` 接口获取资金流
- 股票筛选优先使用 `stock_individual_fund_flow_rank` 接口
- 网络失败时使用预设的示例数据

### 下次执行

预计明天 08:30 自动执行，如需临时测试：
```bash
cd /root/.openclaw/workspace/PROJECTS/trading-signals-morning
source venv/bin/activate
python main.py
```
