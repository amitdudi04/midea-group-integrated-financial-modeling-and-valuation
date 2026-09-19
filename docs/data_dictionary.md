# Data dictionary

| Location | Contents | Unit / basis |
|---|---|---|
| `data/processed/H1_*` | Audited historical statements and normalized matrix | RMB million; source-native precision |
| `data/processed/H2_*` | 2025 Q1 comparative and 2026 Q1 actual bridge | RMB million |
| `data/processed/BETA_MONTHLY_RETURNS_R3.csv` | Paired monthly simple returns used for beta | Decimal returns |
| `model/H3B_MODEL_LONG.csv` | Scenario-year-metric forecast fact table | Metric-specific; monetary values RMB million |
| `model/H4_WACC_CALCULATION_R3.json` | WACC inputs and calculation | Decimal rates |
| `model/H5_*` | DCF, sensitivity, reverse DCF, and EV-to-equity bridge | RMB million and CNY/share |
| `model/H6_*` | Peer observations, period registry, multiples and implied values | Native currencies normalized as documented |
| `model/MIDEA_GROUP_FINAL_MODEL_R3.sqlite` | Canonical machine-readable model | SQLite |
| `data/FINAL_SOURCE_REGISTRY_R3.csv` | Per-input provenance, URL, date, transformation, and SHA-256 | Mixed |

Canonical calculations retain full available precision. Authorities serialize material ratios and outputs to eight decimal places; display outputs normally use two decimals for CNY/share and one or two decimals for RMB million.
