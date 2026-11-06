# R4.1 — Financial-statement linkage and dated evidence controls

**Status:** Supplementary *aggregate* three-statement pro forma, not a restatement of Midea Group’s accounting statements and not a certified 11 September 2026 market valuation.

## Primary-source evidence and time boundary

The 30 June 2026 statement was approved on 28 August and published on 28/29 August 2026. This information was available before the 11 September date, although excluded by the original R3 20 August operating-data cutoff. The separate 30 September actual results were only published on 30 October and remain *post-sample*.

- [Official interim balance sheet and financial report](https://static.cninfo.com.cn/finalpage/2026-08-28/1225533135.PDF)
- [Hong Kong interim-report financial information](https://financialfilings.com/filings/midea-group-co-ltd-1/interim-quarterly-report/2026/60036329/)
- [HKEX filing search, issuer 00300](https://www1.hkexnews.hk/search/titlesearch.xhtml?category=0&lang=EN&market=SEHK&stockId=1000231771) — 10 September 2026 17:03 issued A-share/treasury-share movement return, **published before valuation**; 11 September 17:46 return is **after the market-close valuation reference** and cannot be used as information known at the preceding close
- [30 October 2026 nine-month release, post-sample only](https://static.cninfo.com.cn/finalpage/2026-10-30/1225645132.PDF)

### Latest verified published consolidated anchor

| 30 June 2026 CAS figure | RMB million |
|---|---:|
| Total assets | 643,101.789 |
| Total liabilities | 417,308.848 |
| Total shareholders’ equity | 225,792.941 |
| Cash and equivalents | 74,614.244 |
| Interest-bearing bank loans and debentures | 80,327.263 |
| Net fixed assets (PPE) | 44,320.997 |
| Current fixed-income treasury investments | 158,310.938 |
| Term deposits | 8,496.066 |
| Finance-company customer deposits | 101.708 |

The existing separate R4 valuation uses this latest reported balance sheet to build a **June-based provisional** enterprise-to-equity bridge. It is not a verified September 11 balance sheet.

## More complete three-statement pro-forma construction

[linked_three_statement_extension.py](linked_three_statement_extension.py) expands the experimental operating cash-flow forecasts into **15 linked income statement, cash flow and aggregate balance-sheet observations**.

1. The June 2026 balance-sheet totals and selected subaccounts are source-anchored.
2. An operating working-capital bridge is constructed from published June receivables, notes, inventory, prepayments, accrued payments, contract liabilities and supplier financing. The operating components inside mixed *other current asset/liability and tax* totals are estimated using the accepted R3 2025 source-split ratios; this **is not a fully disclosed June 2026 line-item reconstruction**.
3. The 2026 H2 operating EBIT is the scenario's FY2026 operating EBIT less the H1 observed accounting EBIT adjusted for investments, fair-value changes and the finance result; 2027–2030 use their full scenario year.
4. Depreciation and capital expenditure roll forward tangible assets; forecast net operating working capital and financial services loans/deposits flow into CFO.
5. Interest is calculated at a transparent 2% financing assumption, rather than hidden in operating EBIT. Taxes are calculated separately. Dividends are assumed at 25% of positive consolidated model net profit.
6. Any cash shortfall below the stated operating cash reserve is financed using **new borrowing explicitly labeled an *assumed financing plug***. A balanced model does **not** establish that lenders will provide that debt.
7. Cash + PPE + operating assets + finance loans + financial investments + residual other assets = operating accruals + customer deposits + debt + residual liabilities + accumulated equity. June source assets, liabilities and equity balance; future accounting identities are checked independently.
8. The 11 September balance sheet is interpolated between the **actual June** and the **modeled December** snapshots. Such an account balance is **an estimate, not a public September 11 issuer disclosure**.
9. The 2026 second-half operating FCFF is prorated by 111/184 remaining calendar days rather than multiplying a full-year forecast by 111/365. Cash flow seasonality is still not externally verified.

The output is a **simplified and internally consistent three-statement pro forma**, not a complete original-account taxonomy with projected subsidiaries, debt tranches, OCI, restricted instruments, dilutive share schemes and statutory tax footnotes. Such completeness is **not observable without source-supported subsidiary-level forecasts and a September filing**.

## September share denominator: critical population correction

R3 uses **7,402.513660 million** shares. That population belongs to its accepted original market reference and must not be silently overwritten. Midea's 30 June filing instead reports **7,613.438907 million issued shares**, including 650.848500 million H shares and treasury shares. The HKEX issuer's 10 September movement return reports **6,811,460,392 A shares excluding treasury**. Combining that published A population with the last verified 650,848,500 H share population gives **7,462.308892 million shares** as a *pre-valuation indicative denominator*, before unresolved potential H-treasury and conversion adjustments.

The model publishes both the original R3 and dated indicative denominator so investors cannot mistake an arbitrary issuer gross share count for unrestricted shares outstanding. The later 11 September after-hours disclosure is not used to determine what was known at the 11 September close.

## Remaining evidentiary constraints that cannot be made to disappear

| Requirement | Status / reason |
|---|---|
| Actual consolidated 11 September 2026 cash, financing debt, treasury investments and minority interest | **Not publicly reported for that date**; cannot be certified from a June 30 reporting date |
| Exact September 11 freely distributable share count including all A/H treasury and options | Exchange movement data improves estimation; class-by-class issued, treasury and dilution terms still need the exact valuation cutoff |
| Full disclosed June 30 industrial operating-NWC component classification | June totals observed, but the economic split inside mixed *other* accounts is not fully certified |
| Actual July 1–September 11 free cash flow | No interim reporting on that exact end date; forecast cash flows must remain estimated |
| A completely substantiated 2031 margin, capex and supplier-credit regime | Forecast judgment; cannot be fact-checked as a realized 2031 result |
| Model financing capacity and dividends | Explicit hypothetical assumptions; accounting balance is not confirmation of debt capacity |
| Recurrence of other operating income/subsidies and hedging gains | Direct investment, fair-value and financial items are reconciled out of EBIT; remaining recurrence requires item-level economics and cannot be inferred from the net income statement alone |

### Audit commands

```bash
python -B research_r4/rebuild_exploratory_revision.py
python -B research_r4/verify_exploratory_revision.py
python -B research_r4/linked_three_statement_extension.py
python -B research_r4/verify_linked_three_statement.py
```

The new extension does not change R3 historical results or R4's initial financial assumptions; it provides **an independent and more financially complete scenario alternative**. See [R4 methodology and original calculations](README.md) and [original R3 documents](../docs/REPRODUCIBILITY.md).
