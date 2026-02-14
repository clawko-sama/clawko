#!/usr/bin/env python3
"""Fetch stock data from Yahoo Finance."""

import argparse
import yfinance as yf


def fetch_stock_data(ticker: str, period: str = "1mo"):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Yahoo Finance stock data")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g. AAPL, MSFT)")
    parser.add_argument(
        "-p", "--period", default="1mo",
        help="History period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, max (default: 1mo)",
    )
    args = parser.parse_args()

    fetch_stock_data(args.ticker, args.period)
