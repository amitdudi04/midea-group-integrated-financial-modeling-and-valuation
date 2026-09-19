# Midea Group — Integrated Financial Modeling, Forecasting & Valuation

## Overview

An academic, source-bound valuation of Midea Group combining a 2026E–2030E integrated forecast, economic working-capital analysis, FCFF DCF, reverse DCF, period-aligned trading comparables, a formula-linked Excel model, SQLite outputs, and an interactive Streamlit dashboard.

**Repository:** https://github.com/amitdudi04/midea-group-integrated-financial-modeling-and-valuation

## Research Objective

The project asks what equity value follows from Midea's operating outlook, cash-flow conversion, market-value cost of capital, non-operating asset/debt bridge, and governed share denominator. It also tests what the market price implies and whether peer valuation supports the DCF signal.

## Executive Results

| Result | Value |
|---|---:|
| Market price (11 September 2026) | CNY 86.26/share |
| WACC low / base / high | 5.0776% / 5.2666% / 7.0262% |
| FCFF 2026E / 2027E / 2028E | RMB 43,472.7m / 50,350.5m / 54,197.5m |
| FCFF 2029E / 2030E | RMB 58,626.5m / 63,639.6m |
| DCF bear / base / bull | CNY 117.44 / 294.51 / 548.94 |
| Comps low / central / high | CNY 76.99 / 90.17 / 99.21 |
| DCF sensitivity minimum / maximum | CNY 149.16 / 380.99 |
| Terminal value / enterprise value | 88.8% |
| Base DCF upside to market | 241.4% |
| Risk / confidence | HIGH / LOW TO MEDIUM |
| Final view | DCF indicates upside, but confidence is low to medium |

## Key Findings

- Revenue grows from RMB 485,985.0 million in 2026E to RMB 664,184.6 million in 2030E.
- FCFF increases from RMB 43,472.7 million to RMB 63,639.6 million over the explicit forecast.
- Economic NWC is negative; continued operating-liability funding supports cash flow but creates execution risk.
- The base WACC is 5.2666%.
- The CNY 294.51 base DCF materially exceeds the CNY 90.17 comps central value.
- 88.8% of base enterprise value comes from terminal value, which limits confidence.
- Reverse DCF indicates that the market price embeds materially lower cash-flow economics than the base case.

For the complete financial interpretation, forecast outputs, valuation reconciliation, market-implied expectations, risks, limitations, and conclusions, see [Final Results and Findings](docs/FINAL_RESULTS_AND_FINDINGS.md).

## Model Architecture

Audited history → 2026 Q1/event bridge → forecast drivers → three statements and schedules → economic NWC and FCFF → WACC → DCF/reverse DCF/comparables → synthesis → Excel, SQLite, dashboard, reports, and verification.

## Methodology

The primary method is an FCFF DCF. Trading comparables use source-native TTM peer data with compatible Midea LTM denominators; P/B uses point-in-time book equity. Reverse DCF and a 5×5 WACC–terminal-growth matrix test the valuation. The operating-information cutoff is **20 August 2026** and the valuation date is **11 September 2026**.

## Repository Structure

| Path | Purpose |
|---|---|
| `data/` | Processed inputs, redistributable sources, and source registry |
| `model/` | Forecast, schedules, valuation outputs, and SQLite model |
| `workpapers/` | NWC, beta, ERP, debt cost, capital structure, cash reserve, comps, synthesis |
| `excel/` | Formula-linked institutional workbook |
| `reports/` | Final report and investment memo |
| `dashboard/` | Read-only interactive Streamlit dashboard |
| `verification/` | Public, independent, end-to-end, cleanroom, and mutation controls |
| `docs/` | Finance paper, methodology, architecture, assumptions, and reproducibility |
| `release/` | Repository manifest and authority |

## Interactive Dashboard

```bash
streamlit run dashboard/app.py
```

Open `http://localhost:8501`. The dashboard reads the SQLite model in read-only mode and provides Bear/Base/Bull scenarios, dynamic charts, sensitivity, comparables, synthesis, and live model checks. No public deployment is implied.

## Reproduce the Analysis

```bash
python -m pip install -r requirements.txt
python -B verification/final_calculation_verifier.py
python -B verification/independent_model_recalculator.py
python -B verification/end_to_end_verifier.py
python -B -m pytest tests/test_repository.py
streamlit run dashboard/app.py
```

## Final Reports

- [Final Results and Findings](docs/FINAL_RESULTS_AND_FINDINGS.md)
- [Excel model](excel/MIDEA_GROUP_INSTITUTIONAL_MODEL_R3.xlsx)
- [Valuation report](reports/MIDEA_GROUP_FINAL_VALUATION_REPORT_R3.docx)
- [Investment memo](reports/MIDEA_GROUP_INVESTMENT_MEMO_R3.pdf)
- [Source registry](data/FINAL_SOURCE_REGISTRY_R3.csv)

## Validation

The public verifier recalculates 375 controls. A separate independent recalculator covers operating NWC, FCFF, WACC, DCF, reverse DCF, EV-to-equity, comparables, EPS, and accounting identities without importing production calculation functions. End-to-end, cleanroom, dashboard, and mutation evidence is retained under `verification/`.

## Assumptions and Limitations

The DCF is terminal-value-heavy and sensitive to WACC, long-run growth, and FCFF assumptions. Peer comparability is imperfect, and EV/EBITDA is reference-only because a compatible Midea LTM EBITDA denominator was unavailable. Forecasts are scenarios, not predictions. See [Assumptions and Limitations](docs/assumptions_and_limitations.md).

## Citation

Citation metadata are available in [CITATION.cff](CITATION.cff). Version: R3.1.

## Disclaimer

This repository is an academic research project. It is not investment advice, an offer, or a recommendation to buy or sell securities.
