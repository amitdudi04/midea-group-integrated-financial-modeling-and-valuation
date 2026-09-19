# Midea Group — Integrated Financial Modeling, Forecasting & Valuation

A reproducible corporate-finance research project that builds an integrated
2026E–2030E forecast for Midea Group and evaluates equity value using FCFF DCF,
reverse DCF, period-aligned trading comparables, scenario analysis, and
sensitivity testing.

The project combines financial-statement analysis, three-statement modeling,
economic working-capital classification, cost-of-capital estimation, valuation,
Python/SQL-based validation, a formula-linked Excel model, and an interactive
Streamlit dashboard.

**Repository:**  
https://github.com/amitdudi04/midea-group-integrated-financial-modeling-and-valuation

**Version:** `v3.1`

---

## Start Here

For a quick review:

1. Read this `README.md`
2. Read [Final Results and Findings](docs/FINAL_RESULTS_AND_FINDINGS.md)
3. Read the [Investment Memo](reports/MIDEA_GROUP_INVESTMENT_MEMO_R3.pdf)

For a deeper technical review:

4. Open the [Excel Model](excel/MIDEA_GROUP_INSTITUTIONAL_MODEL_R3.xlsx)
5. Review [Methodology](docs/methodology.md)
6. Review the [`workpapers/`](workpapers/) folder
7. Review the [`verification/`](verification/) framework

---

## Research Objective

The project asks:

> **What equity value follows from Midea Group's operating outlook, cash-flow
> conversion, capital intensity, working-capital structure, market-value cost of
> capital, non-operating assets and liabilities, and governed share denominator?**

It also asks two secondary questions:

- What operating and valuation assumptions are implied by the market price?
- Do period-aligned comparable-company valuations support the DCF result?

The objective is not to produce a single "correct" target price. It is to build
a transparent valuation framework, identify where different methods agree or
disagree, and understand which assumptions drive that disagreement.

---

## Information Boundary

| Item | Date / Period |
|---|---|
| Operating-information cutoff | **20 August 2026** |
| Valuation market-data date | **11 September 2026** |
| Explicit forecast period | **2026E–2030E** |
| Primary valuation method | **FCFF DCF** |
| Secondary valuation method | **Trading comparables** |
| Supporting analyses | **Reverse DCF, scenario analysis, WACC–g sensitivity** |

The separation between the operating-information cutoff and valuation date is
intentional: post-cutoff operating information is not introduced into the
forecast, while market inputs required for valuation are measured at the stated
valuation date.

---

## Executive Results

| Result | Final model output |
|---|---:|
| Market price — 11 September 2026 | **CNY 86.26/share** |
| WACC — low / base / high | **5.0776% / 5.2666% / 7.0262%** |
| FCFF — 2026E | **RMB 43,472.7m** |
| FCFF — 2027E | **RMB 50,350.5m** |
| FCFF — 2028E | **RMB 54,197.5m** |
| FCFF — 2029E | **RMB 58,626.5m** |
| FCFF — 2030E | **RMB 63,639.6m** |
| DCF — bear / base / bull | **CNY 117.44 / 294.51 / 548.94** |
| DCF sensitivity range | **CNY 149.16 – 380.99** |
| Comps — low / central / high | **CNY 76.99 / 90.17 / 99.21** |
| Terminal value / enterprise value | **88.8%** |
| Base DCF upside vs. market | **241.4%** |
| Risk assessment | **High** |
| Confidence | **Low to medium** |
| Final interpretation | **DCF indicates model-implied upside, but confidence remains constrained** |

---

## Central Finding: Valuation Methods Disagree Materially

The most important result of the project is **not simply the CNY 294.51 base
DCF value**.

The three principal reference points are:

- **Market price:** CNY 86.26/share
- **Comps central value:** CNY 90.17/share
- **Base DCF:** CNY 294.51/share

The market price and comparable-company result are relatively close, while the
base DCF is substantially higher.

This dispersion is treated as an analytical finding rather than ignored or
averaged away.

The DCF captures the present value of the model's projected long-run cash-flow
economics, while the comparable-company analysis reflects current market
pricing of peer businesses. At the same time, approximately **88.8% of base-case
enterprise value comes from terminal value**, making the DCF highly sensitive
to long-run FCFF, WACC, and terminal-growth assumptions.

For that reason, the project does **not** interpret CNY 294.51 as a
high-confidence target price.

The governed conclusion is:

> **DCF indicates substantial model-implied upside, but the large dispersion
> versus market/comparable valuation and high terminal-value dependence justify
> a high-risk, low-to-medium-confidence interpretation.**

---

## Key Financial Findings

### 1. Revenue and Cash Flow Grow Through the Explicit Forecast

Revenue increases from approximately:

**RMB 485,985.0m in 2026E**

to:

**RMB 664,184.6m in 2030E**

while FCFF increases from:

**RMB 43,472.7m**

to:

**RMB 63,639.6m**.

The valuation therefore depends not only on revenue growth, but on the model's
assumptions regarding operating profitability, capital expenditure, working
capital, and other operating investment requirements.

### 2. Operating Working Capital Is Economically Classified

The model does not define working capital mechanically as:

`Current Assets − Current Liabilities`

Instead, balance-sheet accounts are classified according to their economic role
in operations.

The final operating-NWC framework includes items such as:

- accounts receivable;
- notes receivable;
- receivables financing;
- inventory;
- contract assets;
- prepayments;
- operating portions of other current assets;
- accounts and notes payable;
- contract liabilities;
- employee-related liabilities;
- operating portions of other current liabilities; and
- operating taxes payable.

Income-tax payable is treated separately because NOPAT already reflects accrual
income tax.

This treatment is important because the definition of operating NWC directly
affects `ΔNWC` and therefore FCFF.

### 3. Midea Operates With Negative Economic NWC

Economic NWC remains negative in the forecast.

This supports cash generation because operating liabilities finance part of the
operating asset base.

However, this is also a valuation risk: if those working-capital economics
normalize or become less favorable, FCFF would weaken relative to the base
forecast.

### 4. The Base Cost of Capital Is 5.2666%

The WACC framework combines:

- a China sovereign risk-free rate;
- a reproducible monthly equity beta;
- a dated China equity-risk premium;
- a market borrowing-cost proxy;
- the effective tax rate; and
- market-value capital-structure weights.

The model also uses explicit low/base/high WACC cases rather than treating one
discount rate as certain.

### 5. DCF Is Highly Sensitive to Terminal Assumptions

Approximately **88.8% of base enterprise value** is attributable to terminal
value.

This does not invalidate the DCF, but it makes long-run assumptions especially
important.

Accordingly, sensitivity and scenario analysis are treated as core parts of the
valuation rather than optional appendices.

### 6. Reverse DCF Provides a Market-Implied Perspective

The reverse DCF starts with the observed market price rather than an assumed
intrinsic value.

Under the governed model structure, the CNY 86.26 market price is consistent
with a materially weaker long-run FCFF path than the project's base case.

This should not be interpreted as a literal market forecast. It is a way to
translate the current share price into the operating assumptions required to
justify that price within the same valuation framework.

### 7. Comparable Companies Provide a Useful Counterweight to DCF

The central comparable-company result of approximately **CNY 90.17/share** is
much closer to the observed market price than the base DCF.

This disagreement is one reason the project retains a cautious final
interpretation despite the apparent DCF upside.

---

## Model Architecture

```text
Audited Historical Financial Statements
                    ↓
          2026 Q1 Interim Bridge
                    ↓
            Forecast Drivers
                    ↓
          Segment / Revenue Forecast
                    ↓
        Integrated Income Statement
                    ↓
        Integrated Balance Sheet
                    ↓
         Integrated Cash Flow
                    ↓
         Economic Operating NWC
                    ↓
                  FCFF
                    ↓
          Cost of Capital / WACC
                    ↓
                FCFF DCF
              ↙          ↘
       Reverse DCF    Sensitivity
              ↘          ↙
                    ↓
        Comparable Companies
                    ↓
          EV-to-Equity Bridge
                    ↓
          Valuation Synthesis
                    ↓
   Excel / SQLite / Dashboard / Reports
                    ↓
      Independent Recalculation
          and Model Validation
```

For the detailed architecture, see
[Model Architecture](docs/model_architecture.md).

---

## Methodology

### Integrated Forecast

The model links operating and financing assumptions through the:

- income statement;
- balance sheet;
- cash-flow statement;
- PPE and depreciation schedule;
- debt and interest schedule;
- working-capital model; and
- share/EPS mechanics.

The explicit forecast covers **2026E–2030E**.

### Free Cash Flow to the Firm

The valuation is based primarily on FCFF:

```text
FCFF
=
NOPAT
+ Depreciation & Amortization
− Capital Expenditure
− Change in Operating NWC
± Other Governed Operating Investment Adjustments
```

### Cost of Capital

Cost of equity follows CAPM:

```text
Cost of Equity
=
Risk-Free Rate
+
Beta × Equity Risk Premium
```

WACC follows:

```text
WACC
=
(E / V × Cost of Equity)
+
(D / V × Pre-Tax Cost of Debt × (1 − Tax Rate))
```

### Discounted Cash Flow

Forecast FCFF is discounted at the applicable scenario WACC.

Enterprise value consists of:

```text
PV of Explicit FCFF
+
PV of Terminal Value
```

which is then reconciled to equity value through the governed
EV-to-equity bridge.

### Reverse DCF

Reverse DCF asks what long-run cash-flow economics would be required for the
model to reconcile to the observed market price.

### Comparable Companies

Trading comparables use source-native peer TTM/latest-quarter information
against compatible Midea LTM denominators.

P/B uses point-in-time book equity.

The selected valuation framework includes:

- EV/Revenue;
- EV/EBIT;
- P/E; and
- P/B.

EV/EBITDA is retained as a peer reference multiple but is not used as a primary
Midea implied-value output where a sufficiently compatible Midea LTM EBITDA
denominator is unavailable.

---

## Why DCF and Comps Should Not Be Mechanically Averaged

The project deliberately avoids taking an arbitrary average of DCF and
comparable-company valuations.

The two methods answer different questions.

**DCF asks:**

> What are the modeled future operating cash flows worth today?

**Trading comparables ask:**

> How is the market currently valuing economically comparable businesses?

When the two methods differ materially, the difference itself contains
information.

In this project, that disagreement increases uncertainty and is reflected in
the final risk/confidence assessment rather than being hidden by averaging the
two methodologies.

---

## Repository Structure

| Path | Purpose |
|---|---|
| [`data/`](data/) | Processed historical/interim inputs, redistributable valuation sources, and source registry |
| [`model/`](model/) | Forecast model, schedules, valuation outputs, and SQLite model |
| [`workpapers/`](workpapers/) | NWC, beta, ERP, debt cost, capital structure, cash reserve, comparable-period, and synthesis analyses |
| [`excel/`](excel/) | Formula-linked Excel financial model |
| [`reports/`](reports/) | Final valuation report and investment memo |
| [`dashboard/`](dashboard/) | Read-only interactive Streamlit dashboard |
| [`docs/`](docs/) | Results, methodology, architecture, assumptions, data dictionary, and reproducibility documentation |
| [`verification/`](verification/) | Financial recalculation, independent validation, cleanroom, consistency, and mutation tests |
| [`release/`](release/) | Repository manifest, authority, authentication, and publication metadata |

---

## Main Project Outputs

### Financial Interpretation

[**Final Results and Findings**](docs/FINAL_RESULTS_AND_FINDINGS.md)

Detailed discussion of:

- historical and forecast results;
- FCFF;
- working capital;
- WACC;
- DCF;
- reverse DCF;
- comparable companies;
- valuation dispersion;
- risks;
- limitations; and
- final conclusions.

### Excel Model

[**Midea Group Institutional Model R3**](excel/MIDEA_GROUP_INSTITUTIONAL_MODEL_R3.xlsx)

Formula-linked workbook covering the forecast, WACC, DCF, sensitivity,
EV-to-equity bridge, comparables, and synthesis.

### Investment Memo

[**Investment Memo**](reports/MIDEA_GROUP_INVESTMENT_MEMO_R3.pdf)

Concise investment-research interpretation of the model.

### Full Valuation Report

[**Valuation Report**](reports/MIDEA_GROUP_FINAL_VALUATION_REPORT_R3.docx)

Detailed report covering the financial-modeling and valuation framework.

### Source Registry

[**Final Source Registry**](data/FINAL_SOURCE_REGISTRY_R3.csv)

Tracks material source provenance used in the project.

---

## Interactive Dashboard

Launch from the repository root:

```bash
streamlit run dashboard/app.py
```

Then open:

```text
http://localhost:8501
```

The dashboard reads the final SQLite model in read-only mode and provides:

- revenue and FCFF forecasts;
- Bear / Base / Bull scenario selection;
- WACC;
- DCF outputs;
- DCF sensitivity;
- comparable-company valuation;
- valuation synthesis; and
- live model-consistency indicators.

Material financial outputs are read from the governed model rather than
maintained as a separate manually entered dashboard dataset.

No public dashboard deployment is implied by this repository.

---

## Reproduce the Analysis

Create a Python environment and install the requirements:

```bash
python -m pip install -r requirements.txt
```

Run the public financial verification:

```bash
python -B verification/final_calculation_verifier.py
```

Run the independent model recalculation:

```bash
python -B verification/independent_model_recalculator.py
```

Run the end-to-end repository verification:

```bash
python -B verification/end_to_end_verifier.py
```

Run repository tests:

```bash
python -B -m pytest tests/test_repository.py
```

Launch the dashboard:

```bash
streamlit run dashboard/app.py
```

For detailed instructions, see
[Reproducibility](docs/reproducibility.md).

---

## Validation

The project uses multiple layers of validation.

### Financial Controls

The public verifier recalculates **375 financial/model controls**.

### Independent Recalculation

A separate recalculation process independently covers major areas including:

- operating NWC;
- FCFF;
- WACC;
- DCF;
- reverse DCF;
- EV-to-equity bridge;
- comparable-company valuation;
- EPS; and
- accounting identities.

The independent recalculator does not rely on the same production calculation
functions for the material checks it verifies.

### Cross-Deliverable Consistency

Material outputs are compared across:

- model files;
- SQLite;
- Excel;
- dashboard;
- reports; and
- repository authorities.

### Reproducibility

The final public release is also checked through fresh-clone and cleanroom
execution.

Detailed evidence is retained under [`verification/`](verification/).

> **Validation improves confidence in implementation correctness; it does not
> eliminate economic or forecasting uncertainty.**

---

## Assumptions and Limitations

The project has several important limitations.

### Terminal-Value Dependence

Approximately **88.8% of base enterprise value** comes from terminal value.

The DCF is therefore highly sensitive to WACC, terminal growth, and long-run
cash-flow assumptions.

### Working-Capital Sustainability

Negative operating NWC supports FCFF in the base model.

If supplier/customer financing economics normalize, forecast FCFF could be
lower.

### Comparable-Company Limitations

Midea operates across multiple businesses, while no peer perfectly reproduces
its operating mix.

Peer period endpoints also follow source-native reporting periods rather than
an artificially identical reporting date.

### Cost-of-Capital Uncertainty

Beta, ERP, borrowing-cost proxies, and capital-structure assumptions are
estimates rather than observable constants.

### Forecast Uncertainty

Forecasts are scenarios based on stated assumptions and available information.
They are not predictions of realized future results.

### Information Boundary

The model uses an operating-information cutoff of **20 August 2026** and a
valuation market-data date of **11 September 2026**.

Subsequent developments are outside the governed analysis.

For additional detail, see
[Assumptions and Limitations](docs/assumptions_and_limitations.md).

---

## What This Project Demonstrates

From a finance perspective, the project applies:

- financial-statement analysis;
- integrated three-statement forecasting;
- segment and operating-driver modeling;
- economic working-capital analysis;
- FCFF;
- CAPM and WACC;
- DCF;
- reverse DCF;
- comparable-company valuation;
- EV-to-equity reconciliation;
- sensitivity analysis;
- scenario analysis;
- valuation-risk assessment; and
- interpretation of conflicting valuation methods.

From a technical perspective, it uses:

- Excel;
- Python;
- SQL / SQLite;
- Streamlit;
- source provenance;
- automated financial controls; and
- independent reproducibility testing.

The technical infrastructure supports the finance analysis; it is not a
substitute for economic judgment.

---

## Research Integrity

This is an author-led academic finance project.

The author remains responsible for the research design, financial methodology,
accounting classifications, assumptions, interpretation, and conclusions.

A concise disclosure regarding the use of AI-assisted development tools is
available in
[AI Assistance Disclosure](docs/AI_ASSISTANCE_DISCLOSURE.md).

---

## Citation

Citation metadata are available in
[`CITATION.cff`](CITATION.cff).

**Version:** `v3.1`

**Repository:**  
https://github.com/amitdudi04/midea-group-integrated-financial-modeling-and-valuation

---

## Disclaimer

This repository is an academic research and financial-modeling project.

The valuation outputs are model-dependent estimates subject to uncertainty in
forecast assumptions, market inputs, cost of capital, terminal value,
accounting judgment, and peer comparability.

Nothing in this repository constitutes investment advice, an offer, a
recommendation, or a solicitation to buy or sell securities.
