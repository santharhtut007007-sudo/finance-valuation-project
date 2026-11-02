#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 18:20:39 2026

@author: santharhtut
"""

import pandas as pd
import yfinance as yf

full_info = yf.Ticker("GOOGL")

# Forecast assumptions
# ---------------------------------------------------------------------

years = [2026, 2027, 2028, 2029, 2030]

growth = [0.20, 0.17, 0.14, 0.115, 0.09]
op_margin = [0.315, 0.305, 0.295, 0.29, 0.29]
tax_rate = [0.165, 0.165, 0.165, 0.165, 0.165]
capex_pct = [0.41, 0.42, 0.38, 0.33, 0.28]
da_pct = [0.065, 0.085, 0.105, 0.125, 0.14]


# ---------------------------------------------------------------------
# Load historical revenue
# ---------------------------------------------------------------------

folder = "/Users/santharhtut/Desktop/finance-valuation-project/data/"

income = pd.read_csv(folder + "income_statement.csv", index_col=0)
balance = pd.read_csv(folder + "balance_sheet.csv", index_col = 0)
base_revenue = income.loc["Total Revenue"].iloc[0]


# ---------------------------------------------------------------------
# Initialize the projection table
# ---------------------------------------------------------------------

proj = pd.DataFrame(index=years)


# ---------------------------------------------------------------------
# Project revenue using annual growth assumptions
# ---------------------------------------------------------------------

current = base_revenue
revenues = []

for g in growth:
    current = current * (1 + g)
    revenues.append(current)

proj["revenue"] = revenues


# ---------------------------------------------------------------------
# Add forecast assumptions to the projection table
# ---------------------------------------------------------------------

proj["op_margin"] = op_margin
proj["tax_rate"] = tax_rate
proj["capex_pct"] = capex_pct
proj["da_pct"] = da_pct


# ---------------------------------------------------------------------
# Calculate operating profit and after-tax operating profit
# ---------------------------------------------------------------------

proj["ebit"] = proj["op_margin"] * proj["revenue"]
proj["nopat"] = proj["ebit"] * (1 - proj["tax_rate"])


# ---------------------------------------------------------------------
# Calculate depreciation and amortization, capital expenditure, and FCF
# ---------------------------------------------------------------------

proj["da"] = proj["da_pct"] * proj["revenue"]
proj["capex"] = proj["capex_pct"] * proj["revenue"]

# FCF here excludes changes in working capital, matching the original.
proj["fcf"] = proj["nopat"] + proj["da"] - proj["capex"]

# ---------------------------------------------------------------------
# Discounting FCF
# ---------------------------------------------------------------------
from wacc import wacc, full_info, total_debt, balance

discount_factors = []
for t in range(1,6):
    discount_factor = 1/(1+wacc)**t
    discount_factors.append(discount_factor)
    
proj["discount_factor"] = discount_factors    
proj["pv_fcf"] = proj["fcf"] * proj["discount_factor"]

sum_pv_fcf = proj["pv_fcf"].sum()

g = 0.03

terminal_capex = 1.1 * proj["da"].iloc[-1]
terminal_fcf = proj["nopat"].iloc[-1] + proj["da"].iloc[-1] - terminal_capex

terminal_value = terminal_fcf * (1 + g) / (wacc - g)
pv_terminal_value = terminal_value * proj["discount_factor"].iloc[-1]

enterprise_value = sum_pv_fcf + pv_terminal_value
tv_share = pv_terminal_value / enterprise_value

cash = balance.loc["Cash Cash Equivalents And Short Term Investments"].iloc[0]
equity_value = enterprise_value - total_debt + cash
shares = full_info["marketCap"] / full_info["currentPrice"]
value_per_share = equity_value / shares

price = full_info["currentPrice"]
upside = value_per_share / price - 1

def value_per_share_calculation (wacc, g):
    pv_fcf_total = 0
    for t in range(1, 6):
        fcf_t = proj["fcf"].iloc[t - 1]
        pv_fcf_total = pv_fcf_total + fcf_t / (1 + wacc) ** t
    terminal_value = terminal_fcf * (1 + g) / (wacc - g)
    pv_terminal_value = terminal_value / (1 + wacc) ** 5
    enterprise_value = pv_fcf_total + pv_terminal_value
    equity_value = enterprise_value - total_debt + cash
    return equity_value / shares


#Sensitivity Table

wacc_values = [0.08, 0.09, 0.10, 0.104, 0.11]
g_values = [0.02, 0.025, 0.03, 0.035, 0.04]

rows = []

for w in wacc_values:
    row = []
    for gg in g_values:
        row.append(value_per_share_calculation(w,gg))
    rows.append(row)
    
table = pd.DataFrame(rows, index = wacc_values, columns = g_values)
table = table.round(0)
















