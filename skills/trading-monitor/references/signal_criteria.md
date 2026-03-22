# A-Share S1 Signal Detection Criteria

## Signal Levels

| Level | Confidence | Description |
|-------|------------|-------------|
| S1 | ≥95% | Strong signal - immediate action recommended |
| S2 | 80-94% | Medium signal - monitor closely |
| S3 | 60-79% | Weak signal - watch for confirmation |
| S4 | <60% | Very weak - ignore |

## S1 Detection Factors

### 1. Price Momentum (30% weight)
- **Rapid rise**: >5% in 5 minutes = 15%
- **Strong incline**: 3-5% = 10%
- **Moderate gain**: 1-3% = 5%

### 2. Volume Surge (25% weight)
- **High volume**: >1M shares = 15%
- **Above average**: 500K-1M shares = 10%
- **Normal volume**: <500K shares = 5%

### 3. Technical Patterns (25% weight)
- **Breakout**: Price breaks resistance = 15%
- **Reversal pattern**: Bullish patterns = 10%
- **Continuation**: Trend reinforcement = 5%

### 4. Market Sentiment (20% weight)
- **Sector leadership**: Top sector performer = 10%
- **News catalyst**: Positive news = 8%
- **Index correlation**: Strong market correlation = 5%

## Algorithm

```
confidence = min(
    price_momentum + 
    volume_factor + 
    technical_score + 
    sentiment_score,
    1.0
)
```

## Data Sources

### akshare API Endpoints
- `ak.stock_zh_a_spot_em()` - Eastmoney A-stock real-time data
- `ak.stock_zh_a_hist()` - Historical data
- `ak.stock_market_index_ths()` - Market index data

### Data Fields
| Field | Description |
|-------|-------------|
| 代码 | Stock code |
| 名称 | Stock name |
| 最新价 | Current price |
| 涨跌幅 | Change percentage |
| 成交量 | Volume |
| 成交额 | Turnover |
| 振幅 | Amplitude |
| 涨跌额 | Price change |

## Status Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1001 | Data fetch failed |
| 1002 | No signals detected |
| 1003 | Notification sent |
| 1004 | Warning: web these values
