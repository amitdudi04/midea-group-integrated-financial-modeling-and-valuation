"""Independent, additive checks for supplementary valuation sensitivities.

The authoritative R3 three-statement model and output tables are read-only.
This script tests arithmetic of NEW diagnostic files without repricing the baseline.
"""
from __future__ import annotations
import csv, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def rows(path):
    with (ROOT / path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def near(a, b, tolerance=0.00002):
    assert math.isclose(float(a), float(b), abs_tol=tolerance, rel_tol=0), (a, b)

def median(values):
    ordered = sorted(map(float, values))
    n = len(ordered)
    return (ordered[(n - 1)//2] + ordered[n//2])/2

def main():
    model = {(r["Scenario"], int(r["Year"]), r["Metric_ID"]): float(r["Value"])
             for r in rows("model/H3B_MODEL_LONG.csv")}
    base = next(r for r in rows("model/H5_SCENARIO_VALUATION_R3.csv")
                if r["Scenario"] == "BASE")
    bridge = rows("model/H5_EV_TO_EQUITY_BRIDGE.csv")
    adjustment = sum(float(r["Amount"]) * float(r["Sign"])
                     for r in bridge if r["Included"] == "YES")
    treasury = float(next(r["Amount"] for r in bridge if
                          r["Bridge_Item"] == "Current fixed-income treasury products"))
    shares = float(base["Shares_Million"])
    fcff = [model["BASE", y, "FCFF"] for y in range(2026, 2031)]
    nwc = [r for r in rows("workpapers/ECONOMIC_NWC_REPLAY_R3.csv")
           if r["Scenario"] == "BASE" and 2026 <= int(r["Year"]) <= 2030]
    release = [-float(r["Delta_Economic_NWC"]) for r in nwc]
    stress = rows("workpapers/SUPPLEMENTARY_VALUATION_STRESSES_R3_1.csv")
    assert len(stress) == 10
    for row in stress:
        w, g = float(row["WACC"]), float(row["Terminal_Growth"])
        fraction = float(row["NWC_Release_Fraction"])
        liquid = float(row["Treasury_Availability_Fraction"])
        assert w > g and 0 <= fraction <= 1 and 0 <= liquid <= 1
        adj_fcff = [v - (1 - fraction) * r for v, r in zip(fcff, release)]
        pv = sum(x/(1 + w)**(i+1) for i, x in enumerate(adj_fcff))
        terminal = adj_fcff[-1]*(1 + g)/(w-g)/(1+w)**5
        equity = pv + terminal + adjustment - (1-liquid)*treasury
        per_share = equity/shares
        for label, actual in (
            ("PV_Explicit_FCFF", pv),
            ("PV_Terminal_Value", terminal),
            ("Equity_Value_RMBm", equity),
            ("Implied_CNY_Per_Share", per_share),
            ("Delta_From_Accepted_Base_CNY", per_share-float(base["Per_Share"])),
        ):
            near(actual, row[label])
    near(float(stress[0]["Implied_CNY_Per_Share"]), base["Per_Share"])

    peers = [r for r in rows("model/H6_NORMALIZED_PEER_DATA_R3.csv")
             if r["Status"] == "ELIGIBLE"]
    assert len(peers) == 6
    workpaper = {r["Metric"]: float(r["Value"]) for r in rows(
        "workpapers/MIDEA_COMPARABLE_PERIOD_WORKPAPER_R3.csv") if r["Value"]}
    sensitivity = rows("workpapers/DOMESTIC_CORE_PEER_SENSITIVITY_R3_1.csv")
    assert len(sensitivity) == 8
    for row in sensitivity:
        selected = peers if row["Peer_Set"] == "All six eligible" else [
            p for p in peers if p["Classification"] == "CORE PEER"]
        assert len(selected) == int(row["Peer_Count"])
        multiple = median([r[row["Multiple"]] for r in selected])
        denominator = workpaper[row["Midea_Denominator"]]
        value = (multiple*denominator +
                 (adjustment if row["Multiple"].startswith("EV_") else 0))/shares
        near(multiple, row["Median_Multiple"])
        near(denominator, row["Midea_Denominator_RMBm"])
        near(value, row["Implied_CNY_Per_Share"])

    # Scenario-bound labels are not numerical order statistics:
    drivers = rows("model/H3AS3_FINAL_FORECAST_DRIVER_REGISTER.csv")
    numeric = [r for r in drivers if all(
        _is_float(r[x]) for x in ("Lower", "Central", "Upper"))]
    not_sorted = [r for r in numeric if not (
        float(r["Lower"]) <= float(r["Central"]) <= float(r["Upper"]))]
    assert len(not_sorted) == 30, len(not_sorted)
    print("PASS supplementary valuation arithmetic: 10 DCF stresses, "
          "8 peer sensitivities, 30 recorded nonmonotonic scenario rows.")

def _is_float(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False

if __name__ == "__main__":
    main()
