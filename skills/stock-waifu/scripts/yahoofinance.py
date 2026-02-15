#!/usr/bin/env python3
"""Fetch stock data from Yahoo Finance."""

import argparse
import yfinance as yf


def fmt_mcap(n):
    if n is None:
        return "N/A"
    if n >= 1_000_000_000_000:
        return f"${n / 1_000_000_000_000:.1f}T"
    if n >= 1_000_000_000:
        return f"${n / 1_000_000_000:.1f}B"
    if n >= 1_000_000:
        return f"${n / 1_000_000:.1f}M"
    return f"${n:,.0f}"


def daily_change(info):
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    prev = info.get("previousClose") or info.get("regularMarketPreviousClose")
    if price and prev:
        chg = price - prev
        pct = (chg / prev) * 100
        sign = "+" if chg >= 0 else ""
        if pct >= 5:
            emoji = "🚀"
        elif pct >= 1:
            emoji = "📈"
        elif pct > -1:
            emoji = "➡️"
        elif pct > -5:
            emoji = "📉"
        else:
            emoji = "💀"
        return price, f"{sign}{chg:.2f} ({sign}{pct:.2f}%) {emoji}"
    return price, "N/A"


def fetch_single(ticker: str, period: str = "1mo"):
    """Detailed output for a single stock."""
    stock = yf.Ticker(ticker)
    info = stock.info
    print(f"=== {info.get('shortName', ticker)} ({ticker.upper()}) ===")
    print(f"Sector: {info.get('sector', 'N/A')}")
    print(f"Market Cap: {info.get('marketCap', 'N/A')}")
    print(f"Current Price: {info.get('currentPrice', 'N/A')}")
    print(f"52-Week High: {info.get('fiftyTwoWeekHigh', 'N/A')}")
    print(f"52-Week Low: {info.get('fiftyTwoWeekLow', 'N/A')}")
    print(f"PE Ratio: {info.get('trailingPE', 'N/A')}")
    print(f"Dividend Yield: {info.get('dividendYield', 'N/A')}")

    print(f"\n=== Price History ({period}) ===")
    hist = stock.history(period=period)
    print(hist.to_string())


def fetch_batch(tickers: list[str]):
    """Concise output: one line per stock."""
    print(f"{'TICKER':<7} {'PRICE':>10} {'CHANGE':>18} {'MCAP':>10}")
    print("-" * 48)
    for t in tickers:
        try:
            stock = yf.Ticker(t)
            info = stock.info
            price, chg_str = daily_change(info)
            mcap = fmt_mcap(info.get("marketCap"))
            price_str = f"${price:,.2f}" if price else "N/A"
            print(f"{t.upper():<7} {price_str:>10} {chg_str:>18} {mcap:>10}")
        except Exception as e:
            print(f"{t.upper():<7} {'ERROR':>10} {str(e)[:30]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Yahoo Finance stock data")
    parser.add_argument("tickers", nargs="+", help="Stock ticker symbol(s) (e.g. AAPL MSFT TSLA)")
    parser.add_argument(
        "-p", "--period", default="1mo",
        help="History period (single stock only): 1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, max (default: 1mo)",
    )
    args = parser.parse_args()

    if len(args.tickers) == 1:
        fetch_single(args.tickers[0], args.period)
    else:
        fetch_batch(args.tickers)
