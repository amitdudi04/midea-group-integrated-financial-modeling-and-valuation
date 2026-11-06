# Reproducibility and Verification

## Evidence levels

The repository supplies a frozen **R3 model-output baseline** through a 22-sheet workbook, a SQLite model and CSV/JSON research schedules. Reproduction should distinguish: (1) arithmetic verification of released tables; (2) independent code-based recomputation from those tables; (3) reconstructing historical source datasets; and (4) economically validating the forecast assumptions. Passing levels (1) and (2) cannot certify levels (3) and (4).

The company-information cutoff is 20 August 2026; the market-input reference date is 11 September 2026. Original third-party evidence may require permitted access and cannot always be fetched from a fresh public clone. The [source registry](../data/FINAL_SOURCE_REGISTRY_R3.csv) records the provenance and transformations.

## Environment and commands

Use a Python 3.11+ environment with dependencies installed from the repository root:

```bash
python -m pip install -r requirements.txt
python -B -m pytest -p no:cacheprovider tests/test_repository.py -q
python -B verification/final_calculation_verifier.py
python -B verification/independent_model_recalculator.py
python -B verification/end_to_end_verifier.py
python -B verification/supplementary_stress_verifier.py
```

The public calculation verifier recomputes **375** accounting and financial checks. The independent model recalculator separately verifies forecast balances, FCFF, WACC, three scenario DCFs, reverse DCF, core multiples and per-share calculations without importing the calculation verifier's central functions. The end-to-end verifier checks data and document hashes, model authority, workbook formulas and SQLite content against the release manifest.

The supplementary verifier checks the **10** additive valuation sensitivities, **8** peer-comparison rows and identifies the **30** driver rows whose scenario values are not numerically ordered. It does **not** refit a new company forecast, independently validate upstream peer data or rerun 44 historical mutation experiments.

## Workbook, SQLite and dashboard

Open [the Excel model](../excel/MIDEA_GROUP_INSTITUTIONAL_MODEL_R3.xlsx) for formula-linked valuation statements and sensitivities. Open [the SQLite model](../model/MIDEA_GROUP_FINAL_MODEL_R3.sqlite) for the archived structured source/output authority.

```bash
streamlit run dashboard/app.py
```

The Streamlit dashboard is a read-only client to the model database, rather than a separate independent calculation engine. It presents the selected Bear/Base/Bull scenario, market context, charts, valuation tables and a limited set of live consistency checks. Historical UI audit records are stored in `verification/audit/`; these should not be represented as a new user-browser test performed during each later GitHub commit.

## Integrity and release provenance

The tracked [repository manifest](../release/REPOSITORY_MANIFEST_R3_1.json) and [authority](../release/REPOSITORY_AUTHORITY_R3_1.json) bind the published repository's files and financial-research source artifacts. Any deliberate academic-document or new-workpaper change **must regenerate** the manifest and its authority digest in the correct order, then rerun the entire end-to-end verifier. Never disable this check merely to obtain a passing workflow.

Historical attestations, cryptographic external roots, tagged releases, and sealed-distribution evidence refer to the original R3/R3.1 publication and should remain distinguishable from later documentation-only or supplementary research work. The separately sealed approximately 55 MB release ZIP is not included in the public repository; its detached verification requires access to the exact archive.

## Separately reproducible R4 exploratory research

The accepted R3 model remains the historical authority. A distinct [R4 research appendix](../research_r4/README.md) analyzes valuation-date timing, original EBIT financial-income exclusions, the August 2026 interim report, a normalized 2031 terminal FCFF, later October 2026 forecast errors and re-estimated *operating FCFF* scenarios.

```bash
python -B research_r4/rebuild_exploratory_revision.py
python -B research_r4/verify_exploratory_revision.py
python -B research_r4/linked_three_statement_extension.py
python -B research_r4/verify_linked_three_statement.py
```

CI executes all four research commands and checks that generated tracked files reproduce byte-for-byte without unstaged or untracked outputs. The R4 source script uses the pre-valuation CAS half-year disclosure; the 30 October nine-month results enter only its separate post-sample diagnostic. The 2026 remainder FCFF is **pro-rated**, and its June 2026 net-financial-assets bridge does not establish exact 11 September account balances. R4 is a linked operating/FCFF forecast, **not a complete replacement three-statement model**.

## What remains unverified from a fresh clone

A passing public verifier establishes consistency of the shipped model and source-bound schedules. It does **not** independently confirm all issuer disclosures, liquidity of treasury holdings at the valuation date, 2030 operating assumptions, future market returns, third-party source reacquisition or the economic desirability of the shares. See [Limitations](LIMITATIONS.md) and [Research Methodology](METHODOLOGY.md) for those interpretive boundaries.
