# Verification methodology

The public calculation verifier independently recomputes accounting identities, EPS, operating NWC, FCFF, WACC, DCF, and peer valuation outputs from released tables. The independent recalculator uses a separate implementation. The end-to-end verifier binds the repository manifest and authority, validates locally distributed source hashes, checks the SQLite authority, inspects workbook formulas and links, and runs the independent recalculator.

The sealed R3 attack suite contains 44 closure-rehash tests. Each begins from a passing baseline, mutates a target, refreshes attacker-controlled descendants, leaves the detached external root unchanged, and requires rejection. Full individual evidence is under `verification/attacks/executions/`.

Internal and role-separated verification passed in the builder environment. The status remains pending genuine external review of the sealed R3 ZIP and detached root.
