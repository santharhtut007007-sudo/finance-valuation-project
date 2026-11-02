#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 15:36:57 2026

@author: santharhtut
"""

from projection import base_revenue, da_pct, tax_rate, wacc, g, total_debt, cash, shares

scenarios = {
    "bear": {
        "growth":    [0.15, 0.12, 0.09, 0.07, 0.05],
        "op_margin": [0.30, 0.27, 0.25, 0.24, 0.24],
        "capex_pct": [0.42, 0.43, 0.40, 0.36, 0.32],
    },
    "base": {
        "growth":    [0.20, 0.17, 0.14, 0.115, 0.09],
        "op_margin": [0.315, 0.305, 0.295, 0.29, 0.29],
        "capex_pct": [0.41, 0.42, 0.38, 0.33, 0.28],
    },
    "bull": {
        "growth":    [0.22, 0.20, 0.17, 0.14, 0.11],
        "op_margin": [0.32, 0.33, 0.34, 0.35, 0.35],
        "capex_pct": [0.40, 0.39, 0.35, 0.30, 0.25],
    },
}

print(da_pct)

def run_scenario(growth, op_margin, capex_pct):
    current = base_revenue
    revenue = []
    for g in growth:
        current = current * (1+g)
        revenue.append(current)
        
        EBIT = []
        for opmg in op_margin:
            ebit = current * opmg
            EBIT.append(ebit)
        
            NOPAT = []
            nopat = ebit * (1-tax_rate)
            NOPAT.append(nopat)
            
            DA = []
            da = dc_pct * current
            DA.append(da)
            
            CAPEX = []
            capex = capex_pct * current
            CAPEX.append(capex)
            
            FCF = []
            fcf = nopat + da  - capex
            FCF.append(fcf)
        
        