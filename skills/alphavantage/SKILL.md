---
name: alphavantage
description: Access Alpha Vantage financial data (stocks, options, technicals, forex, crypto, commodities, economic indicators) via mcporter MCP integration.
---

# Alpha Vantage (via MCPorter)

Call tools on any configured MCP server directly from the command line using mcporter.

## Available servers

Check what's connected:

```bash
npx mcporter list
```

See tools for a specific server:

```bash
npx mcporter list alphavantage --schema
```

## Calling tools

### Function-call syntax (recommended)

```bash
npx mcporter call 'alphavantage.TOOL_CALL(tool_name: "GLOBAL_QUOTE", arguments: "{\"symbol\": \"VOO\"}")'
```

### Flag-delimited syntax

```bash
npx mcporter call alphavantage.TOOL_CALL tool_name:GLOBAL_QUOTE arguments:'{"symbol": "VOO"}'
```

## Alpha Vantage quick reference

Alpha Vantage uses a meta-tool pattern — call `TOOL_CALL` with a `tool_name` and `arguments` JSON string.

### Common tool_names

| Tool | Description |
|------|-------------|
| `GLOBAL_QUOTE` | Latest price & volume for a ticker |
| `TIME_SERIES_DAILY` | Daily OHLCV, 20+ years |
| `COMPANY_OVERVIEW` | Company info, ratios, key metrics |
| `ETF_PROFILE` | ETF metrics and holdings |
| `RSI` | Relative strength index |
| `MACD` | Moving average convergence/divergence |
| `BBANDS` | Bollinger bands |
| `NEWS_SENTIMENT` | Market news & sentiment |
| `TOP_GAINERS_LOSERS` | Top 20 gainers, losers, most active |
| `REALTIME_OPTIONS` | US options data |
| `EARNINGS` | Annual & quarterly EPS |
| `SEARCH` | Natural language search |

### Get full parameter schema for any tool

```bash
npx mcporter call 'alphavantage.TOOL_GET(tool_name: "RSI")'
```

### Examples

```bash
# Quick stock quote
npx mcporter call 'alphavantage.TOOL_CALL(tool_name: "GLOBAL_QUOTE", arguments: "{\"symbol\": \"AAPL\"}")'

# Company fundamentals
npx mcporter call 'alphavantage.TOOL_CALL(tool_name: "COMPANY_OVERVIEW", arguments: "{\"symbol\": \"MSFT\"}")'

# RSI indicator
npx mcporter call 'alphavantage.TOOL_CALL(tool_name: "RSI", arguments: "{\"symbol\": \"TSLA\", \"interval\": \"daily\", \"time_period\": 14, \"series_type\": \"close\"}")'

# Market news sentiment
npx mcporter call 'alphavantage.TOOL_CALL(tool_name: "NEWS_SENTIMENT", arguments: "{\"tickers\": \"AAPL\"}")'

# Top gainers/losers
npx mcporter call 'alphavantage.TOOL_CALL(tool_name: "TOP_GAINERS_LOSERS", arguments: "{}")'
```

## Adding more servers

```bash
npx mcporter config add <name> <url>
```

Then call their tools the same way: `npx mcporter call '<server>.<tool>(...)'`

## Rate limits

Alpha Vantage has limited API calls. Use Yahoo Finance (stock-waifu skill) for routine lookups. Reserve mcporter/Alpha Vantage for deeper analysis: options, technicals, fundamentals, macro data, news sentiment.
