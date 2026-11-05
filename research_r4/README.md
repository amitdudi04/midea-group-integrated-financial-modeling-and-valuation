# R4 exploratory valuation revision — independent of accepted R3

**Status:** Conditional research illustration, **not a revised certified price target**.  
**Value date:** 11 September 2026.  
**Latest issuer interim information that was public on that date:** 2026 half-year Chinese Accounting Standards (CAS) report, disclosed 29 August 2026.  
**Post-sample evaluation:** 2026 third-quarter report, disclosed 30 October 2026.  
**Accepted R3 outputs:** Entirely retained; the original four academic chapters, workbook, SQLite store, WACC calculation and all three published DCF scenarios are unchanged.

## Purpose and research boundary

This is a **separate economic plausibility experiment** addressing timing, terminal cash-flow normalization, newly available issuer disclosures, non-operating income, out-of-sample forecast error and the plausibility of coherent directional business scenarios. It does **not** claim that the resulting values are investable prices, that the forecast has been rebuilt as a full three-statement model, or that a precise 11 September 2026 net-debt/treasury account is observable. In particular, the original 20 August 2026 company-operating-data cutoff is preserved as a historical R3 research design. The August 29 interim report is an **R4 revision to the information set**, not proof the R3 original should have included it under its declared cutoff.

## 1. Valuation-date-consistent discounting and a *provisional* bridge

The alternative values cash flows remaining after 11 September 2026 instead of discounting an entire 2026 year as though it were wholly in the future. The remaining days from 11 September to 31 December number **111**, equivalent to **111/365** of a calendar year. The 2026 stub FCFF uses a **calendar-prorated approximation** because there is no validated January–September FCFF schedule. This is a material limitation: seasonal cash generation may differ significantly from calendar-day proration.

The 2026 year-end cash flow is discounted over 111/365 years; year-end 2027–2030 FCFF and the terminal value use 1+111/365 through 4+111/365 years. No historical January–September cash flow is added to the remaining-cash-flow present value.

The equity bridge uses June 30 CAS evidence where identifiable: cash and equivalents **RMB 74,614.244 million**, current portion of long-term fixed-income investments **RMB 158,310.938 million**, term deposits **RMB 8,496.066 million**, June borrowings **RMB 80,327.263 million**, and non-controlling interests **RMB 12,931.886 million**. Operating cash is retained using a stated historical cash/revenue reserve proxy. Fixed-income-product availability is **assumed at 25%, 50% or 75%** across illustrative scenarios rather than certified. The June borrowing figure is taken at disclosed precision from the interim borrowing schedule, including bank loans and debentures; precise September balances, separate leases and convertible dilution still require an as-of-date reconciliation. June 2026 term deposits are included subject to the same explicit availability haircut as current treasury products; stale 2025 *other* investment add-backs are omitted rather than carried into September.

**Not yet solved:** No reconciled September 11 closing balance sheet exists in the public source set, and the June figure cannot be treated as a September exact balance. Share denominators use the original R3 market valuation population pending a dated repurchase/dilution reconciliation. Thus R4 is a *cash-flow date-aligned illustration with a provisional June bridge*, not a completely dated spot valuation.

## 2. Normalized terminal FCFF

The new long-run 2031 FCFF is constructed afresh, rather than extending the unusually large 2030 negative-working-capital release. For each alternative operating scenario:

```text
Revenue_2031 = Revenue_2030 × (1 + long_run_growth)
EBIT_2031 = Revenue_2031 × normalized_terminal_EBIT_margin
NOPAT_2031 = EBIT_2031 × (1 − tax)
NWC_2031 = Revenue_2031 × long_run_operating_NWC_ratio
Financial_investment_2031 = Revenue_2031 × long_run_financial_services_ratio
FCFF_2031 = NOPAT_2031 + normalized_DA − normalized_capex
            − (NWC_2031 − NWC_2030)
            − (financial_investment_2031 − financial_investment_2030)
Terminal_EV_2030 = FCFF_2031 / (WACC − long_run_growth)
```

A new terminal year whose revenues only grow 1–2.5% no longer perpetuates the 2030 annual 14-billion-RMB working-capital cash release by default. The NWC-to-revenue ratio is assumed to stabilize at each scenario's stated long-run level; this remains a forecast assumption.

## 3. The half-year report and 2026 forecast anchoring

The [company's 2026 CAS half-year report](https://static.cninfo.com.cn/finalpage/2026-08-28/1225533135.PDF) is dated 28/29 August 2026 and therefore **was public before the September 11 valuation date**:

| 2026 Jan–Jun | 2026 actual (RMB m) | 2025 comparison (RMB m) |
|---|---:|---:|
| Operating revenue | 260,042.490 | 251,123.714 |
| Net profit attributable to parent | 26,446.037 | 26,013.690 |
| Adjusted attributable net profit | 19,595.179 | 26,235.399 |
| Operating cash flow | 37,552.090 | 37,281.015 |

Revenue, earnings, adjusted earnings and cash generation must not be conflated. The adjusted-profit measure is particularly affected by FX losses and derivative gains; its fall cannot automatically be translated into a recurring EBIT decline. The 2026 annual revenue alternatives are calculated as observed H1 2026 revenue plus 2025 H2 revenue multiplied by an explicit hypothetical second-half growth rate. This prevents the model from ignoring the published first half but **does not establish issuer-consistent full-year guidance**.

## 4. Operating EBIT versus investment and financial gains

A line-by-line reconciliation of all 15 accepted R3 scenario-years confirms exactly:

```text
R3 EBIT = CAS income-statement operating profit
         − investment income − fair-value change − finance result
```

Thus the suspected **direct** capitalization of these three line items inside R3 EBIT is **not present**. This is established numerically, not inferred from labels. The composition of other operating income (including subsidies and potentially non-recurring recoveries) is not exhaustively rebuilt; R4 uses explicit, independently assumed operating EBIT margins rather than declaring all historical EBIT recurring.

## 5. Cleanly separated October post-sample evidence

The [CAS nine-month report published 30 October 2026](https://static.cninfo.com.cn/finalpage/2026-10-30/1225645132.PDF) was **not available on September 11**. R4 uses its results **only** to diagnose the original FY2026 forecast:

| 2026 Jan–Sep actual | RMB million |
|---|---:|
| Operating revenue | 367,364.936 |
| Parent-attributable net income | 41,393.371 |
| Adjusted parent-attributable net income | 28,787.970 |
| Operating cash flow | 40,187.380 |

Original R3 FY2026 forecast revenue was **485,985.020m**, and parent net profit **43,195.616m**. Actual Jan–Sep results leave roughly **118,620.084m** revenue and **1,802.245m** profit to meet those full-year projections in the remaining quarter. Against 2025 Q4 comparators, this requires about **+27.0% revenue growth and −70.3% profit growth**. This unusual implied combination is flagged, not corrected by retrospectively feeding October actuals into September inputs.

## 6. Independently linked operating cash-flow alternatives

Bear/Base/Bull do not merely change the WACC around a frozen FCFF. Each has a *coherent, explicit operating-driver path* for post-H1 revenue growth, operating EBIT margin, tax, depreciation/amortization, capex, NWC and finance-company net investment. The same definitions are applied in every forecast year. The terminal operating and investment ratios are then held steady while revenues grow at a distinct long-run rate.

| Hypothetical input | Bear | Base | Bull |
|---|---:|---:|---:|
| 2026 H2 revenue YoY | −6% | +4% | +10% |
| 2026 operating EBIT margin | 7.5% | 9.5% | 10.5% |
| 2030 operating EBIT margin | 7.0% | 9.0% | 10.9% |
| D&A / revenue | 1.8% | 1.9% | 1.95% |
| Capex / revenue | 2.7% | 2.3% | 2.1% |
| Operating NWC / revenue | −24% | −27% | −29% |
| Financial-services net investment / revenue | 3.0% | 2.6% | 2.4% |
| WACC | 8.5% | 6.5% | 5.5% |
| Perpetual FCFF/revenue growth driver | 1.0% | 2.0% | 2.5% |
| Assumed treasury-product availability | 25% | 50% | 75% |

**These are researcher-selected assumptions, not estimates from a fitted scenario distribution.** They are connected through annual EBIT → NOPAT → D&A/capex → NWC and financial-investment movements → FCFF → dated DCF. They are **not a rebuilt GAAP/CAS three-statement forecast**: the full scenario balance sheets, distributions, debt roll-forward, tax accounting and changes to consolidated reserves have not been recomputed. Academic review must distinguish this operating cash-flow model from a full three-statement reconstruction.

## Generated outputs and validation

Run from the repository root:

```bash
python -B research_r4/rebuild_exploratory_revision.py
python -B research_r4/verify_exploratory_revision.py
```

Generated workpapers:

- `linked_operating_fcff_scenarios.csv` — 15 scenario-year linked FCFF calculations
- `dated_valuation_scenarios.csv` — dated enterprise value and provisional equity value
- `provisional_june_bridge.csv` — dated-but-incomplete cash, debt and NCI information
- `ebit_bridge_from_r3.csv` — original EBIT exclusion checks
- `publication_cutoff_registry.csv` — source timing and holdout separation
- `post_sample_nine_month_evaluation.csv` — subsequent actual/forecast diagnostics
- `assumptions.json` — parameter source convention, limitations and experiment metadata

The baseline is unaffected because the script reads the authoritative R3 files and writes only within `research_r4/`. An independent checker tests all generated output rows, PV mathematics, value bridges and prevention of October information leakage into the September model.

## Issue register: resolved versus constrained

| Review issue | R4 status |
|---|---|
| Calendar timing / discount period | Corrected in the **illustrative** DCF; 2026 cash-flow stub still approximated |
| Full 11 September EV-to-equity bridge | **Not fully proven**; June-based provisional bridge requires certified reconciliation |
| 2031 sustainable FCFF and NWC | New independent, linked steady-state calculation implemented |
| H1 disclosure available before valuation | Incorporated into R4 data inputs; original R3 cutoff preserved |
| Suspected investment/FV/finance income double count | Direct source of overlap **ruled out** for these three categories; other-income normalization remains judgmental |
| October 2026 post-sample results | Strictly excluded from valuation; explicitly analyzed afterward |
| Coherent three-statement Bear/Base/Bull | Coherent **FCFF** paths built; full linked three-statement reconstruction **not completed** |
| Independent audit | Automated historical/exploratory separation and arithmetic checks; no investment performance guarantee |

**Do not use any R4 provisional per-share figure as an unqualified investment conclusion.** Further primary evidence is required to close the two remaining high-priority research gaps (September bridge; full three-statement scenario re-projection).
