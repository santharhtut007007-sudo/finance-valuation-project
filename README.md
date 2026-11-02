# Alphabet (GOOGL) Valuation: DCF with Scenarios and Comps Cross-Check

A discounted cash flow (DCF) valuation of Alphabet Inc., built in Python, with a bear/base/bull scenario analysis, a WACC × terminal growth sensitivity table, and a comparable-company cross-check.

> Educational project. Not investment advice.

## Company Description

Alphabet is the parent of Google and reports three groups of businesses:

- **Google Services:** Search, YouTube, Android, Chrome, and subscriptions/devices. Most of the revenue and profit comes from advertising here.
- **Google Cloud:** infrastructure, AI, and workspace products sold to businesses.
- **Other Bets:** early-stage ventures such as Waymo.

FY2025 revenue was about $402.8B. Operating margin has been about 32% over the last two years. Alphabet is now spending heavily on AI infrastructure (2026 capex guidance is roughly $195–205B), which is the main driver of this valuation.

## Why This Project

I wanted to value a company from the ground up, rather than just quote a price target: where the numbers come from, which assumptions matter, and what you have to believe to justify the market price.

## Method

1. **Historical analysis:** revenue growth, operating margin, tax rate, capex and D&A as % of revenue, from the 10-K financials (pulled with yfinance and checked against the FY2025 10-K).
2. **Projection:** 5 years (2026–2030) of revenue, EBIT, NOPAT, D&A, capex, and free cash flow.
   `FCF = NOPAT + D&A − Capex`, where `NOPAT = EBIT × (1 − tax rate)`.
3. **WACC:** `E/(D+E) × Ke + D/(D+E) × Kd × (1 − t)`.
   `Ke = risk-free rate + beta × equity risk premium`.
4. **Terminal value:** Gordon growth. 2030 capex is normalized to 1.1× D&A, so the "forever" cash flow is not an AI-buildout year.
5. **Equity bridge:** enterprise value − debt + cash, divided by shares outstanding.
6. **Scenarios, sensitivity, and comps** to test how much the answer depends on the assumptions.

## Key Assumptions

| Assumption | Value | Reason |
|---|---|---|
| Risk-free rate | 5.09% | 10-year US Treasury par yield, 16 Oct 2026 |
| Beta | ~1.21 | yfinance |
| Equity risk premium | 4.5% | Assumption (typical range 4–5.5%) |
| Tax rate | 16.5% | Recent effective rate, below the 21% statutory rate |
| WACC | ~10.4% | Computed from the above and market-value weights |
| Terminal growth | 3% | Below long-run nominal GDP growth |
| Terminal capex | 1.1× D&A | Steady state, not AI-buildout spending |
| 2026 capex | ~41% of revenue | Consistent with ~$200B guidance |

## Results

Share price at time of run: **$283.8** (3 Nov 2026). Market data refreshes every time the scripts run.

### DCF scenarios

| Scenario | Value per share | vs price |
|---|---|---|
| Bear | $75 | −73% |
| Base | $126 | −55% |
| Bull | $183 | −36% |

Scenario assumptions (2026 → 2030):

| | Bear | Base | Bull |
|---|---|---|---|
| Revenue growth | 15% → 5% | 20% → 9% | 22% → 11% |
| Operating margin | 30% → 24% | 31.5% → 29% | 32% → 35% |
| Capex % of revenue | 42% → 32% | 41% → 28% | 40% → 25% |

Bear and bull are analyst judgment. The bear margin of 24% is about the 2019–2023 range, and the bull margin of 35% is above any year to date.

### Sensitivity (base case, value per share)

[Paste the sensitivity table from `projection.py` here after re-running it.]

### Comparable companies

| | Price | P/E | Forward P/E | EV/EBITDA |
|---|---|---|---|---|
| GOOGL | 283.8 | 14.8 | 18.7 | 18.0 |
| MSFT | 525.6 | 27.4 | 21.7 | 19.2 |
| AMZN | 253.0 | 20.4 | 23.2 | 15.2 |
| META | 613.8 | 20.9 | 17.2 | 13.8 |
| AAPL | 341.1 | 39.1 | 35.7 | 30.1 |

Applying the peer median to Alphabet gives about **$269** from EV/EBITDA and about **$463** from P/E.

The P/E result is not reliable. Alphabet's trailing P/E (14.8) is below its forward P/E (18.7), which suggests trailing earnings include one-off non-operating gains. EV/EBITDA is not affected by those gains, so I treat it as the better comparison.

## Interpretation

- Relative to its megacap peers, Alphabet trades roughly in line (EV/EBITDA about 18× vs a peer median of about 17×).
- The DCF value is 36% to 73% below the market price in every scenario, so the market is not pricing Alphabet like this model does. The most likely reasons are a lower discount rate than 10.4%, faster or longer growth than my bull case, or the market pricing all megacap tech at rich multiples.
- The terminal value is more than 100% of enterprise value, because the 2026–2028 free cash flows are negative or small while capex is elevated. The result depends heavily on the long-run assumptions.

## Limitations

- **Terminal value dominates.** Small changes in WACC, growth or normalized capex change the answer a lot (see the sensitivity table).
- **Short explicit forecast.** Five years may be too short for a company in an AI investment cycle, and growth drops abruptly to 3% in 2031.
- **FCF ignores working capital changes** and treats stock-based compensation as a non-cash item.
- **Single blended business.** Segments (Search, YouTube, Cloud, Other Bets) are not modeled separately.
- **Effective vs statutory tax:** 16.5% is assumed to continue.
- **Capex definition** may differ slightly from management guidance.
- **Share count** is implied from market cap ÷ price across all share classes, not taken from the latest filing.
- **yfinance is an unofficial data source.** Revenue and net income were checked against the 10-K, but not every line item.
- **Scenario cases are judgment**, not probability-weighted forecasts.

## Files

| File | Purpose |
|---|---|
| `src/pull_data.py` | Downloads financial statements (yfinance) to `data/` |
| `src/historical_analysis.py` | Historical ratios |
| `src/wacc.py` | WACC calculation |
| `src/projection.py` | Projection, DCF, and sensitivity table |
| `src/scenarios.py` | Bear/base/bull scenarios |
| `src/comps.py` | Comparable-company cross-check |
| `data/` | Financial statements and Treasury rates (CSV) |

## How to Run

```
pip install yfinance pandas
python src/pull_data.py
python src/projection.py
python src/scenarios.py
python src/comps.py
```

Edit the folder path at the top of each script to match your machine.

## Data Sources

- Financial statements: yfinance (Yahoo Finance), pulled 17 Oct 2026, checked against the FY2025 10-K.
- Risk-free rate: US Treasury daily par yield curve rates.
- Market data (price, market cap, beta, peer multiples): yfinance, at run time.
