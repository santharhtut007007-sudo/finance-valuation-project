#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 19:28:59 2026

@author: santharhtut
"""

# Imports
import pandas as pd
import yfinance as yf

# Retrieve Alphabet market data
alphabet = yf.Ticker("GOOGL")
full_info = alphabet.info

# Load the Treasury rate and financial statements
folder = "/Users/santharhtut/Desktop/finance-valuation-project/data/"
us_treasury_data = pd.read_csv(folder + "daily-treasury-rates.csv")
balance = pd.read_csv(folder + "balance_sheet.csv", index_col=0)
income = pd.read_csv(folder + "income_statement.csv", index_col=0)

# Set WACC inputs and assumptions
beta = full_info["beta"]
rf = us_treasury_data["10 Yr"].loc[0] / 100
market_cap = full_info["marketCap"]
total_debt = balance.iloc[:,0].loc["Total Debt"]
interest_expense = income.iloc[:, 0].loc["Interest Expense"]
tax_rate = 0.165
erp = 0.045

# Calculate debt costs, capital weights, and WACC
kd = interest_expense / total_debt
we = market_cap / (market_cap + total_debt)
wd = total_debt / (market_cap + total_debt)
cost_of_equity = rf + beta * erp
wacc = we * cost_of_equity + wd * kd * (1 - tax_rate)
