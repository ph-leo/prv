# akshare API Reference for A-Share Data

## Installation

```bash
pip install akshare
```

## Core Functions

### Real-time Quotes

```python
import akshare as ak

# Shanghai A-shares (沪市A股)
ak.stock_zh_a_spot_em()

# Shenzhen A-shares (深市A股)
ak.stock_zh_a_spot_em()

#北A股市
ak.stock_zh_a_spot_em()
```

### Response Fields

| Field | Description |
|-------|-------------|
| 序号 | Serial number |
| 代码 | Stock code (6 digits) |
| 名称 | Stock name |
| 最新价 | Current price |
| 涨跌幅 | Change percentage |
| 涨跌额 | Price change amount |
| 成交量 | Volume |
| 成交额 | Turnover amount |
| 振幅 | Amplitude |
| 最高 | High price |
| 最低 | Low price |
| 今开 | Open price |
| 昨收 | Previous close |
| 量比 | Volume ratio |
| 换手率 | Turnover rate |
| 市盈率(动态) | PE ratio |
| 市净率 | PB ratio |

### Historical Data

```python
# Daily K-line
ak.stock_zh_a_hist(symbol="sh600000", period="daily", start_date="20240101", end_date="20241231")

# Weekly K-line
ak.stock_zh_a_hist(symbol="sh600000", period="weekly", start_date="20240101", end_date="20241231")

# Monthly K-line
ak.stock_zh_a_hist(symbol="sh600000", period="monthly", start_date="20240101", end_date="20241231")
```

### Market Index

```python
# Main Index
ak.stock_market_index_ths()

# Sector Index
ak.stock_board_industry_index_ths()

# Concept Index
ak.stock_board_concept_index_ths()
```

### Stock Selection

```python
# High Frequency Stocks
ak.stock_zh_a_gdmt()

# Latest Records
ak.stock_zh_a_new()

# ST Stocks
ak.stock_zh_a_st()
```

## Error Handling

| Error Code | Meaning |
|------------|---------|
| None | Success |
| Network Error | Check internet connection |
| Empty Data | No data for the period |
| Rate Limit | Wait before retrying |

## Usage Example

```python
import akshare as ak
import pandas as pd

def fetch_quotes():
    """Fetch real-time quotes for all A-shares"""
    try:
        # Get all A-shares
        df = ak.stock_zh_a_spot_em()
        
        # Filter signals
        strong_signals = df[
            (df['涨跌幅'].astype(float) > 5) |
            (df['成交量'].astype(float) > 1000000)
        ]
        
        return strong_signals
    except Exception as e:
        print(f"Error fetching quotes: {e}")
        return pd.DataFrame()
```

## Data Frequency

- **Real-time**: Updated every 5 seconds
- **Intraday**: 1-minute interval
- **Daily**: End of day closing

## Market Hours

- **Trading Hours**: 9:30 AM - 3:00 PM (Monday-Friday)
- **Data Update**: Real-time during trading hours
- **Post-market**: Limited data available

## Tips

1. **Rate Limiting**: Add delays between requests
2. **Caching**: Cache frequent queries
3. **Error Retry**: Implement retry logic
4. **Data Validation**: Always validate data types
