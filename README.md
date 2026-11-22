# Midea Group — Integrated Financial Modeling and Valuation

**Company:** Midea Group (000333.SZ) · **Forecast:** 2026E–2030E · **Original company-data cutoff:** 20 August 2026 · **Market-price reference:** 11 September 2026

## Research objective and approach

This project asks what Midea Group's equity value would be under a consolidated operating forecast, and whether that value can be defended against the observed share price and comparable-company trading multiples.

The accepted **R3** research model links historical statements, segment forecasts, income statement, balance sheet, cash flows, operating working capital, capital expenditure and financing schedules. Free cash flow to the firm (FCFF) is discounted at a weighted average cost of capital (WACC), then converted from enterprise value into equity value. Peer multiples, reverse DCF and sensitivity tests challenge—not confirm—the DCF result.

**Version boundary:** R3 uses company information available by **20 August 2026** and a market reference dated **11 September 2026**. Its annual 2026–2030 discounting is an original research convention, **not a fully stub-period-adjusted September spot valuation**. The separately documented R4/R4.1 studies address this and other concerns. Neither revision overwrites the accepted R3 financial files.

## 1. Principal R3 results — and what they mean

| Measure | Accepted R3 finding | Financial interpretation |
|---|---:|---|
| Market reference, 11 Sep 2026 | **CNY 86.26/share** | Observed benchmark, not an estimated intrinsic value |
| Forecast revenue, 2026E → 2030E | **RMB 485.99bn → 664.18bn** | Approximately **8.12%** annual modeled growth |
| Forecast EBIT margin, 2026E → 2030E | **10.20% → 9.46%** | Revenue grows faster than operating profit; margin expansion does **not** explain the high DCF |
| Forecast FCFF, 2026E → 2030E | **RMB 43.47bn → 63.64bn** | Cash-flow growth includes a material benefit from operating working-capital releases |
| WACC / terminal growth, base | **5.2666% / 2.5%** | Valuation is highly sensitive to their **2.7666 percentage-point spread** |
| DCF Bear / Base / Bull | **CNY 117.44 / 294.51 / 548.94** | Conditional values under differing operating, cost-of-capital and terminal assumptions |
| Six-peer relative-valuation low / central / high | **CNY 76.99 / 90.17 / 99.21** | Peer-based estimates sit much nearer the observed market price |
| Base terminal-value share of enterprise value | **88.8%** | Most modeled enterprise value is generated **after 2030** |

**Central finding:** The base DCF of **CNY 294.51** is much higher than both the **CNY 86.26** market reference and **CNY 90.17** central peer estimate. That disagreement is a result to investigate, **not proof that the shares are undervalued**. The evidence supports **high valuation uncertainty and low-to-medium confidence** in the point estimate.

Source tables: [R3 scenario DCF](model/H5_SCENARIO_VALUATION_R3.csv) · [Forecast statement data](model/H3B_MODEL_LONG.csv) · [Detailed results](docs/RESULTS.md).

## 2. Why forecast FCFF increases

The model estimates **FCFF**, the cash flow attributable to all capital providers *before* financing distributions:

```text
FCFF = EBIT × (1 − effective operating tax rate)
       + depreciation and amortization − capital expenditure
       − change in operating net working capital
       − change in financial-services net investment
```

For **2026E**, EBIT is **RMB 49.56bn**, after-tax operating profit is **RMB 42.00bn**, D&A is **RMB 8.69bn**, capex is **RMB 8.74bn**, the *change* in operating NWC is **−RMB 2.30bn**, and the change in financial-services net investment is **+RMB 0.77bn**. Together these yield **RMB 43.47bn FCFF**.

By **2030E**, the forecast NWC change is **−RMB 14.07bn**, contributing **positive RMB 14.07bn** to FCFF. Negative NWC means modeled operating liabilities exceed the selected operating current assets: the business obtains financing through, for example, supplier payables and customer advances. When NWC becomes *more* negative, cash is released.

**Why a professor might question it:** Supplier credit, contract liabilities and inventory requirements cannot be assumed to keep releasing cash at the same pace forever. This is a central reason why R3's terminal FCFF requires normalization and why R4/R4.1 produce different values. See the [economic NWC reconciliation](workpapers/ECONOMIC_NWC_REPLAY_R3.csv) and [FCFF tables](docs/RESULTS.md#7-operating-working-capital-and-fcff).

## 3. How the 5.2666% WACC was calculated

The original cost of equity uses **CAPM: risk-free rate + beta × equity risk premium**. WACC then combines the cost of equity and after-tax debt cost using market-value financing weights.

| Input | R3 base assumption |
|---|---:|
| RMB risk-free rate | 1.6899% |
| Estimated equity beta | 0.7855 |
| China equity risk premium | 5.0728% |
| Derived cost of equity | 5.6745% |
| Pre-tax borrowing-cost proxy | 1.7292% |
| Equity / debt market-value weights | 90.31% / 9.69% |
| Effective model tax rate | 15.2566% |
| **Resulting WACC** | **5.2666%** |

The beta is estimated from **60 paired monthly returns**; its approximate 95% interval (**0.4014–1.1696**) indicates substantial estimation uncertainty. The low/high WACC cases (**5.0776% / 7.0262%**) use alternative ERP/beta assumptions. The debt rate is a **market proxy**, not proof that all company debt could be refinanced at 1.7292%.

**Why the low WACC matters:** With a 2.5% terminal growth rate, the base continuing-value denominator is approximately **2.7666%**. Even a modest higher discount rate can materially reduce DCF value. In the separately computed baseline cash-flow sensitivity, raising WACC **100 basis points** decreases the illustrative estimate from **CNY 294.51 to 219.84** without changing underlying FCFF. This is an assumption stress, not an updated integrated forecast.

Sources: [WACC calculation](model/H4_WACC_CALCULATION_R3.json) · [WACC and long-run growth sensitivity](model/H5_WACC_G_SENSITIVITY_R3.csv) · [Supplementary stresses](workpapers/SUPPLEMENTARY_VALUATION_STRESSES_R3_1.csv).

## 4. How the DCF becomes CNY 294.51/share

The **base R3** model discounts five annual FCFF estimates and a Gordon-growth terminal value:

| Base DCF component | RMB billion |
|---|---:|
| Present value of explicit 2026E–2030E FCFF | **230.18** |
| Present value of continuing value | **1,824.10** |
| **Enterprise value** | **2,054.28** |
| Net included EV-to-equity adjustments | **+125.84** |
| **Equity value** | **2,180.12** |
| Governed R3 share denominator | **7,402.514 million shares** |
| **Implied value per share** | **CNY 294.51** |

The signed bridge **adds** excess cash (RMB **30.69bn**), term deposits (**11.94bn**), separately classified investments (**10.27bn**) and current fixed-income treasury products (**155.36bn**). It **subtracts** interest-bearing debt (**68.52bn**), a fund-investor financial liability (**0.71bn**) and non-controlling interests (**13.20bn**). Operating cash reserves, restricted cash and receivables financing already counted in working capital are **not** added again.

**What remains uncertain:** The RMB **155.36bn** treasury-product figure is traceable to a 2025 accounting disclosure, but its classification does **not** prove that the entire amount was unrestricted and distributable to ordinary shareholders on 11 September 2026. The model also uses account values from different available reporting dates. R3 retains its source-bound original convention; later studies test economic availability rather than quietly rewriting the original bridge.

**Most important valuation limitation:** **RMB 1,824.10bn**, or **88.8%** of base enterprise value, comes from the terminal period. Therefore the point result depends predominantly on long-run, unobserved cash-flow economics—not just the visible 2026–2030 projections.

Sources: [R3 DCF calculation](model/H5_SCENARIO_VALUATION_R3.csv) · [Signed EV-to-equity bridge](model/H5_EV_TO_EQUITY_BRIDGE.csv) · [Limitations](docs/LIMITATIONS.md).

## 5. Why peer valuation and reverse DCF disagree with R3

**Relative valuation.** The selected peer set contains **Gree, Haier Smart Home, Hisense Home Appliances, Carrier, Daikin and Panasonic**. The median multiples are applied to Midea's compatible financial measures, with method-specific adjustments:

| Valuation multiple | Selected peer median | Midea implied value |
|---|---:|---:|
| EV / revenue | 1.06× | CNY **83.04** |
| EV / EBIT | 11.23× | CNY **97.30** |
| P / E | 17.57× | CNY **104.92** |
| P / B | 1.88× | CNY **58.86** |

The research reports **CNY 76.99 / 90.17 / 99.21** as its **interquartile-based low / central / high summary**, not the arithmetic average of the four numbers above. EV/EBITDA is **reference-only** because a compatible Midea LTM EBITDA denominator was not established.

An additional **domestic-core-only** sensitivity produces **CNY 57.68 / 48.44 / 65.95 / 51.66** by EV/revenue, EV/EBIT, P/E and P/B respectively. The large change when the peer population narrows demonstrates **peer-selection risk**; neither peer group is automatically the correct benchmark.

**Reverse DCF.** At the observed market price of CNY 86.26, the model's inverse calculation finds that a uniform FCFF scaling factor of approximately **24.96%** of the R3 base path would match the market-implied enterprise value under its held-fixed assumptions. The alternative **−10.36%** implied terminal-growth solution is a mathematical inversion—not a credible forecast of perpetual contraction or evidence that the market must be wrong.

**Why they differ:** R3 DCF capitalizes optimistic long-run FCFF and a narrow WACC–growth spread; peer multiples reflect prices paid for other companies with different growth, capital structure, geography and accounting. Neither independently validates the other. Their divergence is **the central economic finding**, rather than independent confirmation of either method, and more conservative assumptions materially reduce modeled value.

Sources: [Comparable valuation inputs/outputs](model/H6_COMPS_VALUATION_R3.csv) · [Peer-universe sensitivity](workpapers/DOMESTIC_CORE_PEER_SENSITIVITY_R3_1.csv) · [Full interpretation](docs/RESULTS.md#13-why-dcf-and-comparable-companies-differ).

## 6. Why R4 and R4.1 generate much lower values

After R3, the study explicitly challenged its information cutoff, valuation-date timing, terminal working-capital behavior, operating forecasts and financial-asset bridge. These are **new conditional research exercises**, not revisions that make the original R3 estimate retrospectively correct.

| Research version (CNY/share) | Bear | Base | Bull | What changed |
|---|---:|---:|---:|---|
| **R3: original study** | 117.44 | **294.51** | 548.94 | Original full-year discount convention and company data through 20 Aug |
| **R4: operating-FCFF reassessment** | 37.73 | **125.19** | 269.62 | Published June interim data, different operating/WACC assumptions, normalized 2031 FCFF, provisional June bridge |
| **R4.1: linked pro-forma reassessment** | **30.51** | **120.08** | **265.13** | Linked aggregate statements, modeled September stocks, indicative pre-date share count, corrected discount timing |

**R4.1 cash-flow timing:** **111/184** allocates an estimated fraction of modeled June–December 2026 FCFF to the period remaining after 11 September. **111/365 years** is the *different* discount exponent to 31 December 2026. The earlier use of the cash-allocation fraction as a discount exponent was corrected and regression-tested.

**Why the revised values are lower:** More conservative cash-flow, financing and terminal assumptions; discount-rate differences; different treatment of available investments; date-aligned estimated remaining cash flows; and a changed share population. The differences cannot be decomposed into a single causal factor because several inputs change simultaneously. **R4.1 is an internally balanced aggregate pro forma, not an audited company forecast or an exact September balance sheet.**

**Disclosure timing:** The June 2026 interim report was published **after R3's 20 August information cutoff** but **before 11 September**. R4 uses it. The **30 October** nine-month report is **post-sample** and appears only in retrospective forecast diagnostics; it is not used to price the company as of September. The 2026 R3 forecast would require an unusually strong final-quarter revenue increase alongside a sharp profit decline to reconcile with the subsequently reported nine-month totals; see the [post-sample calculation](research_r4/post_sample_nine_month_evaluation.csv).

Sources: [R4 methodology and assumptions](research_r4/README.md) · [R4.1 source and date constraints](research_r4/EVIDENCE_AND_CLOSURE.md) · [R4.1 figures](research_r4/dated_three_statement_valuation.csv).

## 7. Questions a reviewer should be able to answer

| Question | Evidence-based answer |
|---|---|
| **Does CNY 294.51 mean Midea is undervalued?** | **No.** It is a conditional model-implied result. The market, peer methods and R4/R4.1 studies challenge its robustness. |
| **Why does FCFF grow faster than operating profit?** | The forecast assumes increasingly negative operating NWC releases cash. Reversal would reduce FCFF. |
| **Why is the model's WACC so low?** | CAPM beta/ERP inputs and a market-rate debt proxy generate 5.2666%. The beta interval and alternative rates show material uncertainty. |
| **Are treasury assets double-counted?** | The original bridge excludes operating receivables financing and restricted cash and subtracts specified liabilities. **Actual treasury availability and other potential economic overlap remain assumptions**, not independently proven absence of every overlap. |
| **Why does the DCF differ so much from peers?** | Heavy terminal dependence, narrow WACC–growth spread and favorable working-capital assumptions; peer selection is itself imperfect. |
| **Which valuation is the final share-price target?** | **None is presented as an investable target.** R3 is the accepted historical calculation; R4 and R4.1 are explicitly conditional stress/research alternatives. |
| **What do passing tests prove?** | That released formulas, schedules and tracked outputs reconcile; **not** that future forecasts or September account balances are economically certain. |

## 8. Documents, outputs and independent checks

The main academic reading path contains exactly four documents: **[Methodology](docs/METHODOLOGY.md)** · **[Results](docs/RESULTS.md)** · **[Limitations](docs/LIMITATIONS.md)** · **[Reproducibility](docs/REPRODUCIBILITY.md)**.

Supporting files remain in [source data](data/FINAL_SOURCE_REGISTRY_R3.csv), [financial workpapers](workpapers/), [R3 model](model/), [R4/R4.1 research](research_r4/), [Excel](excel/MIDEA_GROUP_INSTITUTIONAL_MODEL_R3.xlsx), [SQLite](model/MIDEA_GROUP_FINAL_MODEL_R3.sqlite), [dashboard](dashboard/app.py), [final valuation report](reports/MIDEA_GROUP_FINAL_VALUATION_REPORT_R3.docx) and [investment memo](reports/MIDEA_GROUP_INVESTMENT_MEMO_R3.pdf). Historical audit and authority evidence are retained for traceability, not as separate academic claims.

The original verifier includes **375 financial controls**; a separate recalculator tests core R3 identities, and the later R4/R4.1 scripts test their own data and forecast outputs. From the repository root (Python 3.12 in CI):

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

A passing result establishes **calculation consistency and repository integrity** for the published files; it does not recreate unavailable third-party historical evidence or establish the future realizability of the assumptions. The end-to-end verifier uses the governed [release manifest](release/REPOSITORY_MANIFEST_R3_1.json).

[AI-assistance disclosure](AI_ASSISTANCE_DISCLOSURE.md) · [Citation](CITATION.cff) · [Data availability and redistribution](data/README.md)

*Academic research, not an investment recommendation.*
