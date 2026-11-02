#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 00:00:37 2026

@author: santharhtut
"""

import pandas as pd
import yfinance as yf

tickers = ["GOOGL", "MSFT", "AMZN", "META", "AAPL"]

rows = []
for tk in tickers:
    info = yf.Ticker(tk).info
    rows.append({
        "ticker": tk,
        "price": info.get("currentPrice"),
        "pe": info.get("trailingPE"),
        "fwd_pe": info.get("forwardPE"),
        "ev_ebitda": info.get("enterpriseToEbitda"),
    })

comps = pd.DataFrame(rows).set_index("ticker")
print(comps.round(1))

# peer medians (exclude Alphabet itself)
peers = comps.drop("GOOGL")
median_pe = peers["pe"].median()
median_ev_ebitda = peers["ev_ebitda"].median()

# Alphabet's own numbers
goog = yf.Ticker("GOOGL").info
eps = goog["trailingEps"]
ebitda = goog["ebitda"]
net_debt = goog["totalDebt"] - goog["totalCash"]
shares_out = goog["marketCap"] / goog["currentPrice"]

price_from_pe = median_pe * eps
price_from_ev = (median_ev_ebitda * ebitda - net_debt) / shares_out

print("Implied price from peer P/E:      ", round(price_from_pe, 1))
print("Implied price from peer EV/EBITDA:", round(price_from_ev, 1))
print("Current price:                    ", goog["currentPrice"])