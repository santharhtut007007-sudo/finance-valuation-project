#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 16:21:16 2026

@author: santharhtut
"""

import pandas as pd


# =============================================================================
# 1. Load and prepare historical income statements
# =============================================================================

folder = "/Users/santharhtut/Desktop/finance-valuation-project/data/"

income = pd.read_csv(folder + "income_statement.csv", index_col=0)

# Put years in rows and sort them into chronological order.
income = income.T
income = income.sort_index()


# =============================================================================
# 2. Calculate historical revenue growth, margins, and tax rates
# =============================================================================

hist = pd.DataFrame(index=income.index)

hist["revenue"] = income["Total Revenue"]
hist["growth"] = hist["revenue"].pct_change()
hist["op_margin"] = income["Operating Income"] / income["Total Revenue"]
hist["tax_rate"] = income["Tax Provision"] / income["Pretax Income"]


# =============================================================================
# 3. Load and prepare historical cash flow statements
# =============================================================================

cashflow = pd.read_csv(folder + "cash_flow.csv", index_col=0)

# Match the income statement's year-by-row layout and chronological order.
cashflow = cashflow.T
cashflow = cashflow.sort_index()


# =============================================================================
# 4. Calculate capital expenditure and depreciation as shares of revenue
# =============================================================================

# Reverse the capital expenditure sign to express spending as a positive ratio.
hist["capex_pct"] = (
    -cashflow["Capital Expenditure"] / income["Total Revenue"]
)

hist["da_pct"] = (
    cashflow["Depreciation And Amortization"] / income["Total Revenue"]
)