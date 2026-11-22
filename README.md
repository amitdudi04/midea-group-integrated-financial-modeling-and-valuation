# Midea Group — Integrated Financial Modeling and Valuation

**Research scope:** Midea Group (000333.SZ) · company information cutoff **20 August 2026** · market reference **11 September 2026** · forecast **2026E–2030E**.

## Research question

What value follows from an integrated consolidated three-statement forecast, operating free cash flow, a market-based cost of capital, and a separately reconciled enterprise-to-equity bridge? How do those values compare with listed peers and the observed share price?

**Study structure:** **R3 is the accepted historical model.** R4 and R4.1 are subsequent, explicitly conditional economic re-examinations. They do not replace the original R3 Excel workbook, SQLite model, source registry, financial schedules or research outputs.

## Principal findings

| Measure | Accepted R3 result |
|---|---:|
| Market reference price, 11 September 2026 | CNY **86.26** per share |
| Base WACC / terminal growth | **5.2666% / 2.5%** |
| 2026E → 2030E revenue | RMB **485,985m → 664,185m** |
| 2026E → 2030E FCFF | RMB **43,473m → 63,640m** |
| DCF: Bear / Base / Bull | CNY **117.44 / 294.51 / 548.94** |
| Six-peer relative valuation: low / central / high | CNY **76.99 / 90.17 / 99.21** |
| Discounted terminal value / base enterprise value | **88.8%** |

**Interpretation:** The R3 DCF is far above the market and peer valuations, but this is **not reliable evidence of undervaluation**. Its result depends strongly on discount rate, continuing value, persistently favorable working-capital financing and the economic availability of treasury investments. The appropriate conclusion is **high valuation uncertainty and low-to-medium confidence**, not an investment recommendation.

## Subsequent economic reassessment

The R4 study uses the interim report released before the 11 September valuation date, rebuilds normalized 2031 free cash flow and separates the October nine-month report as *post-sample* evidence. R4.1 further builds **15 linked aggregate pro-forma statement periods**, an indicative share-population adjustment and a modeled September equity bridge.

| Conditional study result | Bear | Base | Bull |
|---|---:|---:|---:|
| Accepted **R3** (historical convention) | 117.44 | 294.51 | 548.94 |
| **R4** standalone operating-FCFF sensitivity | 37.73 | 125.19 | 269.62 |
| **R4.1** date-corrected linked pro forma | **30.51** | **120.08** | **265.13** |

All values are CNY/share. **These rows do not share the same assumptions or valuation-date balance sheet and must not be interpreted as successive accuracy improvements.** R4.1 discounts the post-11-September portion of 2026 cash flow using **111/365 years**, while estimating its share of June–December cash flow separately using **111/184**. R4.1's September balance sheet, treasury availability and share denominator are **modeled/indicative**, not exact issuer disclosures.

[Detailed revision and scenario definitions](research_r4/README.md) · [R4.1 source dates and unresolved evidence](research_r4/EVIDENCE_AND_CLOSURE.md) · [R4.1 calculated values](research_r4/dated_three_statement_valuation.csv)

The retained [WACC/NWC/treasury stress workpaper](workpapers/SUPPLEMENTARY_VALUATION_STRESSES_R3_1.csv) and [domestic-only peer comparison](workpapers/DOMESTIC_CORE_PEER_SENSITIVITY_R3_1.csv) are diagnostics, not replacement forecasts.

## Academic documentation

The four principal documents have distinct purposes:

1. **[Methodology](docs/METHODOLOGY.md):** source dates, three-statement construction, NWC, FCFF, WACC, DCF and comparables.
2. **[Results](docs/RESULTS.md):** accepted R3 empirical outputs, independent reconciliations, sensitivities and clearly separated R4/R4.1 results.
3. **[Limitations](docs/LIMITATIONS.md):** terminal-value dependence, execution of economic assumptions, cash availability, scenario comparability and missing point-in-time data.
4. **[Reproducibility](docs/REPRODUCIBILITY.md):** environment, exact commands, artifact integrity and boundaries of independent reproduction.

[AI-assistance disclosure](AI_ASSISTANCE_DISCLOSURE.md) · [Citation](CITATION.cff) · [Data and redistribution policy](data/README.md)

## Research artifacts

| Folder | Purpose |
|---|---|
| `data/` | Source registry and available processed historical inputs |
| `model/` | Authoritative R3 schedules, valuation CSVs, assumptions and SQLite model |
| `workpapers/` | Capital cost, cash, NWC, peer and sensitivity calculations |
| `excel/` and `reports/` | Formula-linked workbook, final R3 valuation report and investment memo |
| `research_r4/` | Independent later research code, generated tables and evidentiary boundaries |
| `dashboard/` | Read-only SQLite-backed Streamlit research viewer |
| `verification/` and `release/` | Independent controls, integrity hashes and archived release evidence |

Historical audit, attack-test and authority files are **retained deliberately** for traceability; they are supporting evidence, not additional academic reports.

## Verify the released work

Python 3.12 is used in GitHub Actions. From the repository root:

```bash
python -m pip install -r requirements.txt
python -B -m pytest -p no:cacheprovider tests/test_repository.py -q
python -B verification/final_calculation_verifier.py
python -B verification/independent_model_recalculator.py
python -B verification/supplementary_stress_verifier.py
python -B verification/end_to_end_verifier.py
python -B research_r4/rebuild_exploratory_revision.py
python -B research_r4/verify_exploratory_revision.py
python -B research_r4/linked_three_statement_extension.py
python -B research_r4/verify_linked_three_statement.py
```

The main financial verifier tests **375** controls. The additional R4 scripts recalculate conditional research outputs; source-availability and future-economics claims are **not** verified merely by a passing CI run. Original historical third-party snapshots are not all redistributed.

**Primary deliverables:** [Excel model](excel/MIDEA_GROUP_INSTITUTIONAL_MODEL_R3.xlsx) · [SQLite file](model/MIDEA_GROUP_FINAL_MODEL_R3.sqlite) · [Final report](reports/MIDEA_GROUP_FINAL_VALUATION_REPORT_R3.docx) · [Investment memo](reports/MIDEA_GROUP_INVESTMENT_MEMO_R3.pdf) · [Source registry](data/FINAL_SOURCE_REGISTRY_R3.csv).

*Academic research only. Valuation outputs are conditional on accounting classification, investment availability, financing and long-run operating assumptions; they are not investment advice.*
