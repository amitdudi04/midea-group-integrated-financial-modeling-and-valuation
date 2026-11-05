# Research Limitations and Valuation Uncertainty

The reported Midea Group price estimates are conditional values from a specified model, **not** a market recommendation or forecast with demonstrated statistical confidence. This document distinguishes computational consistency from uncertain economic judgments. It applies to the main [Results](RESULTS.md), the workbook, dashboard and supplementary sensitivity workpapers.

## Terminal value and discount-rate dependence

Approximately **88.8%** of the base enterprise value is the discounted continuing value. Small changes to WACC and perpetual FCFF growth can therefore change the valuation substantially. The base **5.2666% WACC** derives from one RMB market-rate observation, a 60-month beta regression, a July 2026 country ERP, and an AAA debt-market proxy. Other defensible beta windows, market indices, ERP methods, lending spreads and capital structures could produce different discount rates. The model's upper beta bound is not a probability distribution for intrinsic value.

The scenario and 5×5 WACC–growth outputs should not be misread as statistically calibrated confidence intervals. Extreme negative implied growth from reverse DCF is an inverse-model diagnostic, not a forecast of economically perpetual contraction.

## Operating cash-flow sustainability

Base-case operating NWC grows more negative as the forecast progresses. That is a cash release funded by liabilities, not a riskless long-term cash source. Supplier credit, contract liabilities, customer advances, inventory turnover and sales mix may reverse the pattern. The supplementary 50% and 100% release-removal stresses mechanically reduce future FCFF and terminal value without rebuilding the integrated operating forecast; their purpose is to quantify sensitivity, not to replace forecast economics.

The finance-company net-investment adjustment also involves accounting judgments about which assets and related financing remain necessary to produce modeled earnings. The underlying historical identity can reconcile while the future economic classification remains contestable.

## Cash, investments, debt and the equity bridge

The EV-to-equity bridge adds **RMB 155,362.528 million** of 2025 fixed-income treasury products based on source-accounting classification, plus separately identified excess cash and investments. This does not independently establish the unrestricted, unpledged amount available to ordinary equity investors on **11 September 2026**, or whether taxes, transfer restrictions, timing and treasury reinvestment change the distributable value. The sensitivity workpaper therefore reports explicit availability haircuts. These are economic alternatives, not assertions that the accepted accounting amount is erroneous.

Debt uses the latest certified first-quarter 2026 debt position plus a source-supported May 2026 convertible-bond event; equity uses September market capitalization. The date mismatch is disclosed rather than disguised as simultaneous observation. Shares outstanding, potentially dilutive securities, treasury shares, and convertible instruments deserve separate interpretation in an investment decision.

## Forecast-driver semantics

The Lower/Central/Upper columns in the accepted driver register are named scenario or derived-path outputs, **not necessarily ordered numerical bounds**. There are **30 recorded numeric rows** without increasing Lower→Central→Upper values. Two DSO driver years show Central exceeding Upper; 28 additional rows are from linked PPE and depreciation schedules. These do not by themselves demonstrate broken statement arithmetic, but they undermine interpretation as ordinary lower and upper statistical bounds and require financial explanation. The accepted driver register has not been silently sorted or retuned.

## Relative valuation and peer selection

The six eligible peers include domestic appliances and broader international companies with different geography, segment composition, accounting systems, capital intensity and growth expectations. Some source-native peer financial statements are not fully restated to a common accounting basis. Three selected domestic core peers alone imply materially lower multiples than the six-peer set. The domestic-only comparison is **not** superior by construction; it illustrates selection dependence.

Source-native peer TTM periods are aligned as far as available, not perfectly coincident. Midea's own denominator is LTM through March 2026, and EV/EBITDA is **reference-only** because a compatible Midea LTM EBITDA measure is not independently available. A trading-multiple comparison is a reasonableness cross-check, not independent proof that the DCF is right or wrong.

## Data availability, source and replication constraints

The forecast uses company operating data available by 20 August 2026 and market observations as of 11 September 2026. Some original commercial or publisher-controlled evidence is stored only in private archives, although source provenance, official document references, metadata and hashes are available in the registry. A public clone can verify processed model arithmetic and artifact integrity; it cannot necessarily independently reacquire identical upstream datasets or validate every historical publication and economic judgment without original evidence.

The formula-linked Excel workbook and SQLite database are numerical artifacts. Passing structural and identity tests does not prove that operating assumptions will materialize. Older release audit reports describe their own historical verification snapshots, not certification by an external academic reviewer.

## Decision boundary

The base DCF of **CNY 294.51/share** differs materially from the accepted six-peer central relative valuation of **CNY 90.17/share** and the September 2026 reference price of **CNY 86.26/share**. This dispersion is itself a reason for **high valuation risk and low-to-medium confidence**. No mechanical average or claim of certain undervaluation is warranted.

For the analytical construction see [Methodology](METHODOLOGY.md), for complete model outputs see [Results](RESULTS.md), and for checks see [Reproducibility](REPRODUCIBILITY.md).
