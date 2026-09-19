from __future__ import annotations

import json
import sqlite3
from decimal import Decimal as D
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "model/MIDEA_GROUP_FINAL_MODEL_R3.sqlite"
if not DB.is_file():
    raise FileNotFoundError(f"Required certified model database is unavailable: {DB.name}")


def load_release() -> dict:
    con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    try:
        authorities = {n: json.loads(v) for n, v in con.execute("select name,json from authority")}
        missing = sorted({"H4", "H6", "H7", "REVERSE_DCF"} - set(authorities))
        if missing:
            raise RuntimeError(f"Required authority rows are missing: {', '.join(missing)}")
        tables = {name: pd.read_sql_query(f'SELECT * FROM "{name}"', con) for name in [
            "model", "h5_scenarios", "h5_sensitivity", "ev_equity_bridge",
            "peers", "peer_periods", "h6_valuation", "sources",
        ]}
    finally:
        con.close()
    return {"authorities": authorities, **tables}


def numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    result = frame.copy()
    for column in columns:
        result[column] = pd.to_numeric(result[column], errors="raise")
    return result


def live_checks(data: dict) -> pd.DataFrame:
    model = numeric(data["model"], ["Year", "Value"])
    idx = {(r.Scenario, int(r.Year), r.Metric_ID): D(str(r.Value)) for r in model.itertuples()}
    scenarios = numeric(data["h5_scenarios"], ["Per_Share"])
    years = sorted(model.loc[model["Metric_ID"].eq("FCFF"), "Year"].astype(int).unique())
    assets = ["BS_AR", "BS_NOTES_RECEIVABLE", "BS_RECEIVABLES_FINANCING", "BS_INVENTORY", "BS_CONTRACT_ASSETS", "BS_PREPAYMENTS", "BS_OTHER_RECEIVABLES", "BS_OTHER_CURRENT_ASSETS_OPERATING"]
    liabilities = ["BS_AP", "BS_CONTRACT_LIABILITIES", "BS_NOTES_PAYABLE", "BS_EMPLOYEE_COMP", "BS_OTHER_PAYABLES", "BS_OTHER_CURRENT_LIABILITIES_OPERATING", "BS_OTHER_TAXES_PAYABLE"]
    value = lambda s, y, m: idx[(s, y, m)]
    accounting_ok = fcff_ok = True
    for scenario in scenarios["Scenario"]:
        for year in years:
            accounting_ok &= abs(value(scenario, year, "BS_TOTAL_ASSETS") - value(scenario, year, "BS_TOTAL_LIABILITIES") - value(scenario, year, "BS_TOTAL_EQUITY")) <= D(".000002")
            nwc = lambda yy: sum(value(scenario, yy, x) for x in assets) - sum(value(scenario, yy, x) for x in liabilities)
            finance = lambda yy: value(scenario, yy, "BS_LOANS_ADVANCES_CURRENT") + value(scenario, yy, "BS_CURRENT_PORTION_NONCURRENT_ASSETS_FINANCE") - value(scenario, yy, "BS_CUSTOMER_DEPOSITS")
            fcff = value(scenario, year, "EBIT") * (1 - value(scenario, year, "DRV_EFFECTIVE_TAX_RATE_PERCENT") / 100) + value(scenario, year, "PPE_DEPRECIATION") + value(scenario, year, "PPE_AMORTIZATION") - value(scenario, year, "PPE_CAPEX") - (nwc(year) - nwc(year - 1)) - (finance(year) - finance(year - 1))
            fcff_ok &= abs(fcff - value(scenario, year, "FCFF")) <= D(".000002")
    h4, h6, h7 = (data["authorities"][x] for x in ["H4", "H6", "H7"])
    wacc = (D(h4["Risk_Free_Rate"]) + D(h4["Beta"]) * D(h4["ERP_Full_Precision"])) * D(h4["Equity_Weight"]) + D(h4["PreTax_Cost_of_Debt"]) * (1 - D(h4["Tax_Rate"])) * D(h4["Debt_Weight"])
    dcf_ok = all(abs(D(str(r.Per_Share)) - D(h7["DCF"][str(r.Scenario).title()])) <= D(".000002") for r in scenarios.itertuples())
    comps_ok = all(D(h6["Comps_Range"][x]) == D(h7["Comps"][x]) for x in ["Low", "Central", "High"])
    checks = [
        ("Accounting identities", accounting_ok), ("FCFF independent recomputation", fcff_ok),
        ("WACC independent recomputation", abs(wacc - D(h4["WACC"])) <= D(".00000002")),
        ("DCF authority linkage", dcf_ok), ("Comparable-company synthesis", comps_ok),
        ("Peer/Midea period basis", h6["Peer_Midea_Period_Basis_Mismatches"] == 0),
    ]
    return pd.DataFrame([{"Control": name, "Status": "PASS" if ok else "FAIL"} for name, ok in checks])


data = load_release()
h4, h6, h7, reverse = (data["authorities"][x] for x in ["H4", "H6", "H7", "REVERSE_DCF"])
model = numeric(data["model"], ["Year", "Value"])
scenarios = numeric(data["h5_scenarios"], ["WACC", "Terminal_Growth", "PV_Forecast_FCFF", "Terminal_Value", "PV_Terminal_Value", "Enterprise_Value", "Equity_Value", "Shares_Million", "Per_Share", "Terminal_Value_Percent_EV"])
sensitivity = numeric(data["h5_sensitivity"], ["WACC", "Terminal_Growth", "Per_Share"])
peers = numeric(data["peers"], ["Share_Price", "Shares", "Market_Cap", "Gross_Debt", "Cash_And_Short_Term_Investments", "NCI", "Enterprise_Value", "Revenue", "EBITDA", "EBIT", "Net_Income", "Book_Equity", "EV_Revenue", "EV_EBITDA", "EV_EBIT", "PE", "PB"])

st.set_page_config(page_title="Midea Group Forecasting and Valuation", page_icon="📊", layout="wide")
st.title("Midea Group Forecasting and Valuation")
st.caption(f"Model information cutoff {h7['Model_Information_Cutoff']} · Valuation date {h7['Valuation_Market_Data_Date']} · CNY/share and RMB million")
scenario_names = list(scenarios["Scenario"])
scenario = st.selectbox("Valuation scenario", scenario_names, index=scenario_names.index("BASE"), help="Updates all scenario-linked outputs from the certified SQLite model.")
selected = scenarios.loc[scenarios["Scenario"].eq(scenario)].iloc[0]
market_price = float(h7["Market_Price"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Market price", f"CNY {market_price:,.2f}")
c2.metric(f"DCF {scenario.title()}", f"CNY {float(selected['Per_Share']):,.2f}")
c3.metric("Upside / (downside)", f"{(float(selected['Per_Share']) / market_price - 1) * 100:,.1f}%")
c4.metric("Risk / confidence", f"{h7['Risk_Rating']} / {h7['Confidence_Rating'].replace('_', ' ')}")

tabs = st.tabs(["Overview", "Forecast", "WACC", "DCF", "Comparable Companies", "Synthesis", "Model Verification"])

with tabs[0]:
    st.subheader("Valuation overview")
    overview = pd.DataFrame([
        ["Market price", market_price], ["DCF bear", float(h7["DCF"]["Bear"])], ["DCF base", float(h7["DCF"]["Base"])], ["DCF bull", float(h7["DCF"]["Bull"])],
        ["Comps low", float(h7["Comps"]["Low"])], ["Comps central", float(h7["Comps"]["Central"])], ["Comps high", float(h7["Comps"]["High"])],
    ], columns=["Measure", "CNY/share"])
    st.dataframe(overview.style.format({"CNY/share": "{:,.2f}"}), hide_index=True, width="stretch")
    st.info("DCF is the primary method. Period-aligned trading comparables are a secondary reference. Wide method dispersion and terminal-value concentration support low-to-medium confidence.")

with tabs[1]:
    st.subheader(f"{scenario.title()} forecast")
    years = sorted(model.loc[model["Metric_ID"].eq("FCFF"), "Year"].astype(int).unique())
    metrics = ["IS_OPERATING_REVENUE", "EBIT", "IS_ATTRIBUTABLE_NI", "FCFF"]
    forecast = model.loc[model["Scenario"].eq(scenario) & model["Year"].astype(int).isin(years) & model["Metric_ID"].isin(metrics), ["Year", "Metric_ID", "Value"]].pivot(index="Year", columns="Metric_ID", values="Value").reset_index().rename(columns={"IS_OPERATING_REVENUE": "Revenue", "IS_ATTRIBUTABLE_NI": "Attributable net income"})
    st.line_chart(forecast.set_index("Year")[["Revenue", "EBIT", "Attributable net income", "FCFF"]], width="stretch")
    st.dataframe(forecast.style.format({x: "{:,.1f}" for x in forecast.columns if x != "Year"}), hide_index=True, width="stretch")
    st.caption("RMB million; selected-scenario rows from the certified SQLite model.")

with tabs[2]:
    st.subheader("Weighted average cost of capital")
    wacc_rows = [("Risk-free rate", h4["Risk_Free_Rate"]), ("Beta", h4["Beta"]), ("Equity risk premium", h4["ERP"]), ("Cost of equity", h4["Cost_of_Equity"]), ("Pre-tax cost of debt", h4["PreTax_Cost_of_Debt"]), ("Tax rate", h4["Tax_Rate"]), ("Equity weight", h4["Equity_Weight"]), ("Debt weight", h4["Debt_Weight"]), ("WACC low", h4["WACC_Low"]), ("WACC base", h4["WACC"]), ("WACC high", h4["WACC_High"])]
    wacc_table = pd.DataFrame([[label, f"{float(value):.4f}x" if label == "Beta" else f"{float(value) * 100:.4f}%"] for label, value in wacc_rows], columns=["Input / output", "Display"])
    st.dataframe(wacc_table, hide_index=True, width="stretch")
    st.caption(f"ERP source date {h4['ERP_Source_Date']} · Capital-structure date {h4['Capital_Structure_Date']}")

with tabs[3]:
    st.subheader("Discounted cash flow")
    dcf = scenarios[["Scenario", "WACC", "Terminal_Growth", "PV_Forecast_FCFF", "PV_Terminal_Value", "Enterprise_Value", "Equity_Value", "Per_Share", "Terminal_Value_Percent_EV"]].copy()
    for col in ["WACC", "Terminal_Growth", "Terminal_Value_Percent_EV"]: dcf[col] *= 100
    st.dataframe(dcf.style.format({"WACC": "{:.4f}%", "Terminal_Growth": "{:.2f}%", "PV_Forecast_FCFF": "{:,.1f}", "PV_Terminal_Value": "{:,.1f}", "Enterprise_Value": "{:,.1f}", "Equity_Value": "{:,.1f}", "Per_Share": "{:,.2f}", "Terminal_Value_Percent_EV": "{:.1f}%"}), hide_index=True, width="stretch")
    st.subheader("WACC / terminal-growth sensitivity")
    matrix = sensitivity.pivot(index="WACC", columns="Terminal_Growth", values="Per_Share").sort_index(ascending=False)
    matrix.index = [f"{x * 100:.4f}%" for x in matrix.index]; matrix.columns = [f"{x * 100:.2f}%" for x in matrix.columns]
    st.dataframe(matrix.style.format("{:,.2f}"), width="stretch")
    st.subheader("Reverse DCF")
    reverse_table = pd.DataFrame([
        ["Market price", float(reverse["Market_Price_CNY"]), "CNY/share"], ["Implied terminal growth", float(reverse["Implied_Terminal_Growth"]) * 100, "%"],
        ["Implied uniform FCFF scale", float(reverse["Implied_Uniform_FCFF_Scale"]) * 100, "% of base"], ["Implied 2030 FCFF", float(reverse["Implied_2030_FCFF"]), "RMB million"],
    ], columns=["Measure", "Value", "Unit"])
    st.dataframe(reverse_table.style.format({"Value": "{:,.2f}"}), hide_index=True, width="stretch")
    st.caption(reverse["Result"].replace("_", " ").title())

with tabs[4]:
    st.subheader("Period-aligned comparable companies")
    eligible = peers.loc[peers["Status"].eq("ELIGIBLE"), ["Peer", "Classification", "Price_Date", "Fiscal_Basis", "EV_Revenue", "EV_EBITDA", "EV_EBIT", "PE", "PB"]]
    st.dataframe(eligible.style.format({x: "{:.2f}x" for x in ["EV_Revenue", "EV_EBITDA", "EV_EBIT", "PE", "PB"]}), hide_index=True, width="stretch")
    selected_multiples = pd.DataFrame([[key.replace("_", "/"), float(value)] for key, value in h6["Selected_Multiples"].items()], columns=["Selected multiple", "Value"])
    st.dataframe(selected_multiples.style.format({"Value": "{:.2f}x"}), hide_index=True, width="stretch")
    st.caption(h6["Period_Basis"] + " · EBITDA is reference-only because a compatible Midea LTM denominator is unavailable.")

with tabs[5]:
    st.subheader("Valuation synthesis")
    synthesis = pd.DataFrame({"CNY/share": [market_price, float(h7["Comps"]["Low"]), float(h7["Comps"]["Central"]), float(h7["Comps"]["High"]), float(h7["DCF"]["Bear"]), float(h7["DCF"]["Base"]), float(h7["DCF"]["Bull"])]}, index=["Market", "Comps low", "Comps central", "Comps high", "DCF bear", "DCF base", "DCF bull"])
    st.bar_chart(synthesis, horizontal=True, width="stretch")
    st.markdown(f"**Investment view:** {h7['Investment_View'].replace('_', ' ').title()}")
    st.markdown(f"**Terminal-value share of enterprise value:** {float(h7['Terminal_Value_Percent_EV']) * 100:.1f}%")
    left, right = st.columns(2)
    with left:
        st.markdown("**Key catalysts**")
        for item in h7["Key_Catalysts"]: st.markdown(f"- {item}")
    with right:
        st.markdown("**Key risks**")
        for item in h7["Key_Risks"]: st.markdown(f"- {item}")

with tabs[6]:
    st.subheader("Model verification")
    checks = live_checks(data)
    st.dataframe(checks, hide_index=True, width="stretch")
    if checks["Status"].eq("PASS").all():
        st.success("All live model checks passed.")
    else:
        st.error("One or more live checks failed.")
    st.caption(f"Model version R3.1 · Source rows {len(data['sources']):,} · SQLite connection read-only")
