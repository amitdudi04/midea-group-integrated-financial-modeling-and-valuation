# Reproducibility

1. Use Python 3.11 or later and install `requirements.txt`.
2. Run the three commands in the root README. Each verifier exits with code 0 and emits a JSON `PASS` result.
3. Open `excel/MIDEA_GROUP_INSTITUTIONAL_MODEL_R3.xlsx`; the material valuation sheets are formula-linked and contain no external links.
4. Run `streamlit run dashboard/app.py` to inspect the SQLite-backed presentation layer.
5. Compare repository files with `release/REPOSITORY_MANIFEST_R3_1.json` through the end-to-end verifier.
6. For immutable release authentication, obtain the sealed R3 ZIP separately and run the detached verifier against `release/authentication/FINAL_RELEASE_EXTERNAL_ROOT_R3.json`. The public repository does not redistribute the 55 MB ZIP.

Internet access is not required for the three model verifiers. Excluded third-party payloads are needed only to recreate the processed data from first-party/provider sources; their exact hashes and URLs are in the source registry.
