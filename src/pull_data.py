#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 15:21:52 2026

@author: santharhtut
"""
import yfinance as yf

alphabet = yf.Ticker("GOOGL")
income = alphabet.income_stmt
balance = alphabet.balance_sheet
cashflow = alphabet.cashflow

folder = "/Users/santharhtut/Desktop/finance-valuation-project/data/"
income.to_csv(folder + "income_statement.csv")
balance.to_csv(folder + "balance_sheet.csv")
cashflow.to_csv(folder + "cash_flow.csv")