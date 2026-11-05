# Research Methodology

**Company:** Midea Group (000333.SZ)  
**Valuation date:** 11 September 2026  
**Company operating-information cutoff:** 20 August 2026  
**Explicit forecast horizon:** 2026E–2030E  
**Accounting units:** RMB million unless otherwise specified

## Research question and analytical sequence

The study estimates Midea Group's equity value from independently sourced historical financial statements, operating forecasts, free cash flow to the firm (FCFF), a market-consistent cost of capital and explicit non-operating asset and liability adjustments. It treats an FCFF discounted cash-flow (DCF) valuation as its primary *model-implied* intrinsic-value estimate and period-aligned listed-company multiples as an external reasonableness check. Reverse DCF and scenario sensitivity help evaluate whether the large difference between intrinsic and market-implied values is economically credible.

The calculation sequence is: audited annual statements → 2026 Q1 fact and disclosure-taxonomy bridges → forecast driver register → integrated income statement, balance sheet, cash flows and financing/PPE schedules → economic working capital and FCFF → cost of capital → independently computed DCF and comparables → reverse DCF → qualitative synthesis. DCF and comparable-company valuation are **parallel** approaches at the synthesis stage, not inputs to each other.

## Historical data, valuation date and accounting population

The source registry at [data/FINAL_SOURCE_REGISTRY_R3.csv](../data/FINAL_SOURCE_REGISTRY_R3.csv) records source document, publisher, observation and publication dates, valuation eligibility, transformation, and inclusion status. The integrated model uses audited annual history through 2025 and a 2026 Q1 source bridge. The 20 August 2026 company-fact cutoff is distinct from the 11 September 2026 market-input observation date. This distinction is preserved in [the valuation-date register](../model/H7_VALUATION_DATE_BRIDGE_R3.csv).

The Q1 disclosure categories are not automatically identical to the controlling annual segment taxonomy. Compatible signals are mapped and incompatible segments remain separately labeled in [the Q1 taxonomy bridge](../model/H3B_Q1_DISCLOSURE_TO_FORECAST_TAXONOMY_BRIDGE.csv). The modeled operating segments are Smart Home, Building Technology, Industrial Technology, Other and Eliminations.

The company is consolidated; forecast accounting share populations, equity and non-controlling interests are carried in separate schedules. Share counts used for per-share DCF reflect the governed valuation population and may differ marginally across scenario-specific projected populations.

## Three-statement forecast

The scenario-specific forecast is governed by [the forecast driver register](../model/H3AS3_FINAL_FORECAST_DRIVER_REGISTER.csv) and the long-form [statement output](../model/H3B_MODEL_LONG.csv). Revenue, cost, operating margins, investment, receivables, inventory, supplier credit, financing and distributions flow through integrated income, balance sheet and cash-flow schedules. Cash, retained earnings, PPE and debt roll-forwards reconcile to the projected balance sheet.

The driver register's **Lower, Central and Upper columns represent separately constructed scenario-path values or analytical alternatives**, not mathematical lower and upper confidence limits. In particular, **30 numeric rows are not in ascending Lower–Central–Upper order**, including two direct 2026–2027 DSO rows and 28 PPE/depreciation schedule rows. These should not be silently sorted or relabeled as statistical interval bounds. “Upper” can mean the value under the named business scenario rather than the largest output, especially for derived accounting quantities. The specific DSO crossing remains an assumption-design issue to be challenged economically, even though the modeled statements balance.

## Operating working capital and unlevered free cash flow

Operating working capital consists of eight economically operating current-asset accounts less seven operating current-liability accounts. Trade receivables, notes, inventory, operating prepayments and receivables financing enter the operating asset population. Payables, contract liabilities, employee accruals and operating taxes enter operating liabilities. Income-tax payable is excluded to avoid counting income taxes again when using after-tax operating profit.

A separate financial-services net-investment schedule includes loans/advances and finance-company assets net of customer deposits. The operating FCFF formula is:

```text
FCFF = EBIT × (1 − operating effective tax rate)
     + depreciation + amortization − capital expenditure
     − change in operating NWC
     − change in financial-services net investment
```

Negative NWC provides a cash benefit while it becomes more negative; its continued release is a **forecast assumption**, not independently assured cash generation. Definitions and historical replay are in [the NWC policy](../workpapers/FINAL_OPERATING_NWC_POLICY.csv) and [NWC reconciliation](../workpapers/ECONOMIC_NWC_REPLAY_R3.csv).

## Cost of capital

The cost of equity applies CAPM using the 11 September 2026 RMB risk-free rate, a beta fitted from **60 paired monthly adjusted-price returns** against the Shanghai Composite over September 2021–September 2026, and the 1 July 2026 Damodaran China equity-risk premium. The estimated beta is **0.7855**, with an approximate 95% confidence interval of **0.4014–1.1696**.

The pre-tax cost of debt is a **market borrowing proxy**, using a 5-year AAA ChinaBond curve observation, not the company's historical effective interest expense. The WACC uses market-value capital structure: approximately **90.31% equity**, **9.69% debt**. The base model uses a **5.2666% WACC**; low/high sensitivity rates incorporate the CDS-based ERP alternative and upper beta estimate respectively. These rates are evidence-linked modeling choices, but they are not universal or indisputably correct capital-cost estimates.

## DCF, enterprise-to-equity bridge and reverse DCF

Each scenario discounts five annual FCFF observations at its own WACC. Continuing value is computed by the Gordon formula `FCFF_2030 × (1+g) / (WACC−g)`, discounted five years; WACC must exceed terminal growth. The enterprise-to-equity bridge adds the model-classified excess cash, deposits and non-operating investments and deducts interest-bearing obligations, separately classified financial liabilities and minority interests. Restricted cash and the operational cash reserve are excluded. Receivables financing remains within operating NWC, and is not added as a second treasury asset.

The model's large fixed-income treasury-product amount is traceable to the 2025 annual note but **recorded accounting classification does not alone prove unrestricted availability to shareholders at the September 2026 valuation date**. The accepted baseline does not change in this review. Supplementary cash-availability haircuts explore that uncertainty without modifying the accounting bridge.

Reverse DCF solves for market-implied FCFF scaling and, separately, an implied Gordon-growth solution at the historical price. Negative implied perpetuity growth is a mathematical inversion, not a prediction.

## Comparable companies and inference

The accepted relative-valuation benchmark uses median source-native multiples across **three domestic core peers and three broader secondary peers**. The six selected peers' financial measures use their latest available TTM periods; Midea applies compatible LTM revenue, EBIT and attributable earnings through March 2026, while P/B uses point-in-time book equity. EV/EBITDA is reference-only because a compatible Midea LTM depreciation-and-amortization denominator was unavailable.

The [domestic-only peer workpaper](../workpapers/DOMESTIC_CORE_PEER_SENSITIVITY_R3_1.csv) reports core-peer median multiples and implied Midea valuations using **exactly the same denominators and bridge**. It is a diagnostic illustrating benchmark composition sensitivity, not a new statistically validated target price.

## Supplementary valuation stress methodology

The [supplementary sensitivity workpaper](../workpapers/SUPPLEMENTARY_VALUATION_STRESSES_R3_1.csv) recomputes the accepted base cash flows under alternative discount rates, terminal growth, fractions of projected operating-NWC releases and haircuts to treasury-product availability. Each case holds other modeled financial and tax relationships unchanged and therefore **is not a newly balanced three-statement forecast**.

The accepted R3 valuation is retained; these scenarios cannot be read as probabilities or formal confidence limits. The independent [supplementary verifier](../verification/supplementary_stress_verifier.py) recomputes each sensitivity from the accepted tracked model rather than overwriting it.

See [Results](RESULTS.md), [Limitations](LIMITATIONS.md) and [Reproducibility](REPRODUCIBILITY.md) for findings, interpretation and validation.
