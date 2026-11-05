# Midea Group — Integrated Financial Modeling and Valuation

**An academic, source-traceable study of Midea Group (000333.SZ)**  
**Operating information cutoff:** 20 August 2026 · **Valuation market-data date:** 11 September 2026 · **Forecast:** 2026E–2030E

## Research objective

What equity value follows from a consolidated five-year operating forecast, economically classified cash flows, a market-based discount rate and explicit adjustments for non-operating assets and financing? The project compares an FCFF discounted cash-flow valuation with period-aligned trading multiples and examines what the observed price implies.

The accepted **R3 underlying model and financial outputs are unchanged**. New valuation sensitivities are explicitly labeled supplementary and do not modify the integrated statements, workbook, SQLite outputs or historical research release.

## Accepted valuation results

| Measure | Accepted R3 value |
|---|---:|
| Observed 11 September 2026 price | CNY 86.26/share |
| Base WACC | 5.2666% |
| 2026E / 2030E revenue | RMB 485,985.0m / 664,184.6m |
| 2026E / 2030E FCFF | RMB 43,472.7m / 63,639.6m |
| DCF bear / base / bull | CNY 117.44 / **294.51** / 548.94 |
| Six-peer comparables low / central / high | CNY 76.99 / **90.17** / 99.21 |
| Base terminal value as share of enterprise value | **88.8%** |
| Interpretation | High valuation risk; low-to-medium conviction |

The DCF and six-peer methods disagree substantially. Their dispersion, heavy terminal-value dependence, and assumptions concerning sustained negative operating working capital and treasury-asset availability **limit confidence**. The DCF's large model-implied upside should not be presented as an assured trading opportunity.

## Supplementary robustness and peer-selection diagnostics

These are *one-variable or limited-combination accounting sensitivities*, not fully recalculated three-statement scenarios and not replacements for the accepted R3 prices.

| Diagnostic | Illustrative CNY/share |
|---|---:|
| Accepted base DCF | 294.51 |
| Base FCFF with +100 bps WACC | 219.84 |
| No future negative-NWC cash release (with matching terminal continuation removed) | 234.67 |
| 50% modeled availability haircut on fixed-income treasury products | 284.02 |
| High WACC + half NWC release + half treasury availability | 156.85 |

Domestic-only core-peer medians produce lower indicative per-share values: EV/Revenue **57.68**, EV/EBIT **48.44**, P/E **65.95**, and P/B **51.66**, compared with the corresponding six-peer estimates **83.04**, **97.30**, **104.92**, and **58.86**. Neither peer selection is automatically correct; the difference measures benchmark sensitivity.

The numerical workpapers are [valuation stress tests](workpapers/SUPPLEMENTARY_VALUATION_STRESSES_R3_1.csv) and [domestic-core peer sensitivity](workpapers/DOMESTIC_CORE_PEER_SENSITIVITY_R3_1.csv). The accepted model is not overwritten.

## Academic research documents

1. [Methodology](docs/METHODOLOGY.md) — data cutoff, integrated forecasts, working-capital classification, WACC, DCF, equity bridge and peer-selection conventions.
2. [Results](docs/RESULTS.md) — full accepted financial tables, economic interpretation and separately qualified supplementary diagnostics.
3. [Limitations](docs/LIMITATIONS.md) — economic judgments, terminal-value risk, non-operating-asset availability, peer comparability and data-provenance limits.
4. [Reproducibility](docs/REPRODUCIBILITY.md) — saved artifacts, independent calculation checks and distinctions between model arithmetic and historical source recreation.

The [AI-assistance disclosure](AI_ASSISTANCE_DISCLOSURE.md) describes the role and limitations of development aids. Source inputs, driver schedules and audit evidence retain their names in the technical folders rather than competing with the academic narrative.

## Research artifact map

| Directory | Role |
|---|---|
| `data/` | Source registry, original accessible methodological source files and processed financial inputs |
| `model/` | R3 financial schedules, WACC, FCFF, three scenario DCFs, reverse DCF, peer valuation, SQLite authority |
| `workpapers/` | Capital-structure, ERP, cash taxonomy, working-capital and supplementary stress calculations |
| `excel/` | Formula-linked institutional financial workbook |
| `dashboard/` | SQLite-backed, read-only Streamlit user interface |
| `reports/` | Final valuation report and short investment memo |
| `verification/` | Published calculation verifiers, source integrity checks, retained historical validation evidence |
| `release/` | Repository hashes, release authority and historically dated attestations |

## Reproduce public computations

From a Python 3.11+ environment:

```bash
python -m pip install -r requirements.txt
python -B -m pytest -p no:cacheprovider tests/test_repository.py -q
python -B verification/final_calculation_verifier.py
python -B verification/independent_model_recalculator.py
python -B verification/end_to_end_verifier.py
python -B verification/supplementary_stress_verifier.py
streamlit run dashboard/app.py
```

The original R3 model verification includes **375 controls**. The supplemental verifier independently recomputes the diagnostic cash-flow/peer tables. All original source archives are not redistributed; exact historical input re-creation may require separate authorized access. [Full reproducibility notes](docs/REPRODUCIBILITY.md).

## Deliverables

[Excel model](excel/MIDEA_GROUP_INSTITUTIONAL_MODEL_R3.xlsx) · [SQLite model](model/MIDEA_GROUP_FINAL_MODEL_R3.sqlite) · [Final report](reports/MIDEA_GROUP_FINAL_VALUATION_REPORT_R3.docx) · [Investment memo](reports/MIDEA_GROUP_INVESTMENT_MEMO_R3.pdf) · [Source registry](data/FINAL_SOURCE_REGISTRY_R3.csv)

## Interpretation and citation

This is a retrospective, dated academic valuation and **not investment advice**. The valuation uses a source-bound operating forecast and assumptions, not a prediction of future market prices. Model accuracy is contingent on business performance, cash availability, accounting economics and the cost of capital. [Citation metadata](CITATION.cff).
