from __future__ import annotations
import csv, hashlib, json, math, sqlite3, statistics, zipfile
from datetime import datetime, timezone
from decimal import Decimal as D, getcontext
from pathlib import Path
getcontext().prec=50
ROOT=Path(__file__).resolve().parent.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def j(rel):return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def rows(rel):
    with (ROOT/rel).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def near(a,b,tol=D("0.000001")):return abs(D(str(a))-D(str(b)))<=tol
def quantile(values,f):
    v=sorted(D(str(x)) for x in values);p=D(len(v)-1)*D(str(f));lo=int(p);hi=min(lo+1,len(v)-1);w=p-lo;return v[lo]*(D(1)-w)+v[hi]*w
def calculate():
    checks=[]
    def check(name,ok,detail=""):checks.append({"Control":name,"Result":"PASS" if ok else "FAIL","Detail":detail})
    gate=j("model/H3B_ATTEMPT005_FINAL_GATE.json")
    for k in ["BS_Identity_Failures","Cash_Rollforward_Failures","Debt_Rollforward_Failures","PPE_Rollforward_Failures","Equity_Rollforward_Failures","Statement_Linkage_Failures","Balancing_Plug_Count","Post_Cutoff_Uses"]:check(k,gate[k]==0,str(gate[k]))
    check("Candidate_Difference_Not_Plugged",gate["Candidate_Difference_Plugged"] is False)
    check("Detailed_Candidate_Not_Authority",gate["Detailed_Candidate_As_Authority"] is False)
    check("Not_Exchange_Ex_Treasury_Only",gate["Exchange_Ex_Treasury_Only"] is False)
    model=rows("model/H3B_MODEL_LONG.csv");idx={(r["Scenario"],int(r["Year"]),r["Metric_ID"]):D(r["Value"]) for r in model};mv=lambda s,y,m:idx[(s,y,m)]
    for s in ["BEAR","BASE","BULL"]:
      for y in range(2026,2031):
        check(f"EPS_{s}_{y}",near(mv(s,y,"IS_BASIC_EPS"),mv(s,y,"IS_ATTRIBUTABLE_NI")/(mv(s,y,"EPS_DENOMINATOR_SHARES")/D(1_000_000)),D(".00000002")),s)
    # Independent accounting and economic recomputation from released rows.
    ca=["BS_CASH","BS_TRADING_FINANCIAL_ASSETS","BS_DERIVATIVE_FINANCIAL_ASSETS","BS_NOTES_RECEIVABLE","BS_AR","BS_RECEIVABLES_FINANCING","BS_PREPAYMENTS","BS_INVENTORY","BS_CONTRACT_ASSETS","BS_OTHER_RECEIVABLES","BS_CURRENT_PORTION_NONCURRENT_ASSETS","BS_LOANS_ADVANCES_CURRENT","BS_OTHER_CURRENT_ASSETS"]
    nca=["BS_LONG_TERM_INVESTMENTS","BS_OTHER_NONCURRENT_FINANCIAL_ASSETS","BS_PPE","BS_CIP","BS_INTANGIBLES","BS_GOODWILL"]
    cl=["BS_SHORT_TERM_BORROWING","BS_CURRENT_PORTION_DEBT","BS_AP","BS_NOTES_PAYABLE","BS_EMPLOYEE_COMP","BS_TAXES_PAYABLE","BS_CONTRACT_LIABILITIES","BS_OTHER_PAYABLES","BS_OTHER_CURRENT_LIABILITIES","BS_DERIVATIVE_LIABILITIES","BS_CUSTOMER_DEPOSITS","BS_TRADING_FINANCIAL_LIABILITIES"]
    op=["IS_TOTAL_REVENUE","IS_OPERATING_COST","IS_TAXES_SURCHARGES","IS_SELLING_EXPENSE","IS_ADMIN_EXPENSE","IS_RD_EXPENSE","IS_OTHER_INCOME","IS_INVESTMENT_INCOME","IS_FAIR_VALUE_CHANGE","IS_ASSET_DISPOSAL","IS_CREDIT_IMPAIRMENT","IS_ASSET_IMPAIRMENT","IS_FEE_COMMISSION_EXPENSE","IS_FINANCE_RESULT"]
    nwca=["BS_AR","BS_NOTES_RECEIVABLE","BS_RECEIVABLES_FINANCING","BS_INVENTORY","BS_CONTRACT_ASSETS","BS_PREPAYMENTS","BS_OTHER_RECEIVABLES","BS_OTHER_CURRENT_ASSETS_OPERATING"]
    nwcl=["BS_AP","BS_CONTRACT_LIABILITIES","BS_NOTES_PAYABLE","BS_EMPLOYEE_COMP","BS_OTHER_PAYABLES","BS_OTHER_CURRENT_LIABILITIES_OPERATING","BS_OTHER_TAXES_PAYABLE"]
    policy=j("workpapers/FINAL_OPERATING_NWC_FORMULA.json")
    check("Economic_NWC_Asset_Population",policy.get("Asset_Accounts")==nwca,str(policy.get("Asset_Accounts")))
    check("Economic_NWC_Liability_Population",policy.get("Liability_Accounts")==nwcl,str(policy.get("Liability_Accounts")))
    check("Economic_NWC_Formula",policy.get("Formula")=="SUM(OPERATING_NWC_ASSETS)-SUM(OPERATING_NWC_LIABILITIES)")
    check("Economic_NWC_Delta_Formula",policy.get("Delta_Formula")=="OPERATING_NWC_t-OPERATING_NWC_t-1")
    check("Economic_NWC_FCFF_Formula",policy.get("FCFF_Formula")=="NOPAT+D&A-CAPEX-DELTA_OPERATING_NWC-DELTA_FINANCIAL_SERVICES_NET_INVESTMENT")
    check("Taxes_Payable_Economic_Treatment",policy.get("Taxes_Payable_Treatment")=="SPLIT: income-tax payable excluded because NOPAT uses accrual tax; other taxes payable included as operating accrual")
    check("Receivables_Financing_Economic_Treatment",policy.get("Receivables_Financing_Treatment")=="OPERATING_NWC_ASSET_AND_NOT_EV_BRIDGE_ADDITION")
    for s in ["BEAR","BASE","BULL"]:
      for y in range(2026,2031):
        check(f"Revenue_Segments_{s}_{y}",near(mv(s,y,"IS_OPERATING_REVENUE"),sum(mv(s,y,"SEGMENT_REVENUE_"+x) for x in ["BUILDING_TECH","INDUSTRIAL_TECH","OTHER","SMART_HOME","ELIMINATIONS"])))
        check(f"Operating_Profit_{s}_{y}",near(mv(s,y,"IS_OPERATING_PROFIT"),sum(mv(s,y,x) for x in op)))
        check(f"Net_Profit_{s}_{y}",near(mv(s,y,"IS_NET_PROFIT"),mv(s,y,"IS_PBT")+mv(s,y,"IS_INCOME_TAX")))
        check(f"Attributable_NI_{s}_{y}",near(mv(s,y,"IS_ATTRIBUTABLE_NI"),mv(s,y,"IS_NET_PROFIT")-mv(s,y,"IS_NCI_PROFIT")))
        check(f"Current_Assets_{s}_{y}",near(mv(s,y,"BS_TOTAL_CURRENT_ASSETS"),sum(mv(s,y,x) for x in ca)+mv(s,y,"BS_TOTAL_CURRENT_ASSETS_OTHER_IMMATERIAL_COMPONENTS")))
        check(f"Noncurrent_Assets_{s}_{y}",near(mv(s,y,"BS_TOTAL_NONCURRENT_ASSETS"),sum(mv(s,y,x) for x in nca)+mv(s,y,"BS_TOTAL_NONCURRENT_ASSETS_OTHER_IMMATERIAL_COMPONENTS")))
        check(f"Total_Assets_{s}_{y}",near(mv(s,y,"BS_TOTAL_ASSETS"),mv(s,y,"BS_TOTAL_CURRENT_ASSETS")+mv(s,y,"BS_TOTAL_NONCURRENT_ASSETS")))
        check(f"Current_Liabilities_{s}_{y}",near(mv(s,y,"BS_TOTAL_CURRENT_LIABILITIES"),sum(mv(s,y,x) for x in cl)+mv(s,y,"BS_TOTAL_CURRENT_LIABILITIES_OTHER_IMMATERIAL_COMPONENTS")))
        check(f"Total_Liabilities_{s}_{y}",near(mv(s,y,"BS_TOTAL_LIABILITIES"),mv(s,y,"BS_TOTAL_CURRENT_LIABILITIES")+mv(s,y,"BS_TOTAL_NONCURRENT_LIABILITIES")))
        check(f"Parent_Equity_{s}_{y}",near(mv(s,y,"BS_PARENT_EQUITY"),sum(mv(s,y,x) for x in ["BS_SHARE_CAPITAL","BS_CAPITAL_RESERVE","BS_OTHER_RESERVES","BS_RETAINED_EARNINGS","BS_TREASURY_SHARES"])))
        check(f"Equity_{s}_{y}",near(mv(s,y,"BS_TOTAL_EQUITY"),mv(s,y,"BS_PARENT_EQUITY")+mv(s,y,"BS_NCI")))
        check(f"BS_Identity_{s}_{y}",near(mv(s,y,"BS_TOTAL_ASSETS"),mv(s,y,"BS_TOTAL_LIABILITIES")+mv(s,y,"BS_TOTAL_EQUITY")))
        check(f"Cash_Rollforward_{s}_{y}",near(mv(s,y,"CF_CLOSING_CASH"),mv(s,y,"CF_OPENING_CASH")+mv(s,y,"CF_CFO")+mv(s,y,"CF_CFI")+mv(s,y,"CF_CFF")+mv(s,y,"CF_FX_EFFECT")))
        check(f"Cash_Taxonomy_{s}_{y}",near(mv(s,y,"BS_CASH"),mv(s,y,"CF_CLOSING_CASH")+mv(s,y,"BS_RESTRICTED_CASH")+mv(s,y,"BS_TERM_DEPOSITS")+mv(s,y,"BS_CASH_TAXONOMY_OTHER")))
        check(f"Other_Current_Assets_Split_{s}_{y}",near(mv(s,y,"BS_OTHER_CURRENT_ASSETS"),mv(s,y,"BS_OTHER_CURRENT_ASSETS_OPERATING")+mv(s,y,"BS_OTHER_CURRENT_ASSETS_TREASURY")+mv(s,y,"BS_OTHER_CURRENT_ASSETS_HEDGE")))
        check(f"Current_Noncurrent_Assets_Split_{s}_{y}",near(mv(s,y,"BS_CURRENT_PORTION_NONCURRENT_ASSETS"),mv(s,y,"BS_CURRENT_PORTION_NONCURRENT_ASSETS_TREASURY")+mv(s,y,"BS_CURRENT_PORTION_NONCURRENT_ASSETS_FINANCE")))
        check(f"Taxes_Payable_Split_{s}_{y}",near(mv(s,y,"BS_TAXES_PAYABLE"),mv(s,y,"BS_INCOME_TAX_PAYABLE")+mv(s,y,"BS_OTHER_TAXES_PAYABLE")))
        check(f"Other_Current_Liabilities_Split_{s}_{y}",near(mv(s,y,"BS_OTHER_CURRENT_LIABILITIES"),mv(s,y,"BS_OTHER_CURRENT_LIABILITIES_OPERATING")+mv(s,y,"BS_OTHER_CURRENT_LIABILITIES_HEDGE")))
        check(f"Retained_Earnings_{s}_{y}",near(mv(s,y,"BS_RETAINED_EARNINGS"),mv(s,y-1,"BS_RETAINED_EARNINGS")+mv(s,y,"IS_ATTRIBUTABLE_NI")-mv(s,y,"DIVIDENDS")))
        check(f"PPE_CIP_{s}_{y}",near(mv(s,y,"BS_PPE")+mv(s,y,"BS_CIP"),mv(s,y-1,"BS_PPE")+mv(s,y-1,"BS_CIP")+mv(s,y,"PPE_CAPEX")-mv(s,y,"PPE_DEPRECIATION")))
        nwc=sum(mv(s,y,x) for x in nwca)-sum(mv(s,y,x) for x in nwcl);pnwc=sum(mv(s,y-1,x) for x in nwca)-sum(mv(s,y-1,x) for x in nwcl)
        fin=mv(s,y,"BS_LOANS_ADVANCES_CURRENT")+mv(s,y,"BS_CURRENT_PORTION_NONCURRENT_ASSETS_FINANCE")-mv(s,y,"BS_CUSTOMER_DEPOSITS");pfin=mv(s,y-1,"BS_LOANS_ADVANCES_CURRENT")+mv(s,y-1,"BS_CURRENT_PORTION_NONCURRENT_ASSETS_FINANCE")-mv(s,y-1,"BS_CUSTOMER_DEPOSITS")
        fcff=mv(s,y,"EBIT")*(1-mv(s,y,"DRV_EFFECTIVE_TAX_RATE_PERCENT")/100)+mv(s,y,"PPE_DEPRECIATION")+mv(s,y,"PPE_AMORTIZATION")-mv(s,y,"PPE_CAPEX")-(nwc-pnwc)-(fin-pfin)
        check(f"FCFF_Economic_NWC_{s}_{y}",near(mv(s,y,"FCFF"),fcff,D(".000002")),str(fcff))
    br=rows("data/processed/BETA_MONTHLY_RETURNS_R3.csv");ar=[D(r["Midea_Simple_Return"]) for r in br];mr=[D(r["Market_Simple_Return"]) for r in br];am=sum(ar)/D(len(ar));mm=sum(mr)/D(len(mr));beta=sum((x-mm)*(y-am) for x,y in zip(mr,ar))/sum((x-mm)**2 for x in mr)
    h4=j("model/H4_WACC_CALCULATION_R3.json");check("Beta_Recomputation",near(beta,h4["Raw_Beta"],D(".00000002")),str(beta))
    rf=D(h4["Risk_Free_Rate"]);erp=D(h4["ERP_Full_Precision"]);b=D(h4["Beta"]);kd=D(h4["PreTax_Cost_of_Debt"]);tax=D(h4["Tax_Rate"]);ew=D(h4["Equity_Weight"]);dw=D(h4["Debt_Weight"]);w=(rf+b*erp)*ew+kd*(1-tax)*dw;check("WACC_Recomputation",near(w,h4["WACC"],D(".00000002")),str(w))
    low=(rf+b*D(h4["ERP_CDS_Alternative"]))*ew+kd*(1-tax)*dw;high=(rf+D(h4["Beta_95pct_CI_High"])*erp)*ew+kd*(1-tax)*dw
    check("WACC_Low_Source_Method",near(low,h4["WACC_Low"],D(".00000002")),str(low));check("WACC_High_Statistical_Method",near(high,h4["WACC_High"],D(".00000002")),str(high));check("WACC_Range_Not_Arbitrary","ARBITRARY" not in h4["WACC_Range_Method"])
    scenarios=rows("model/H5_SCENARIO_VALUATION_R3.csv");bridge=rows("model/H5_EV_TO_EQUITY_BRIDGE.csv");adj=sum(D(r["Amount"])*D(r["Sign"]) for r in bridge if r["Included"]=="YES")
    for r in scenarios:
      s=r["Scenario"];ww=D(r["WACC"]);g=D(r["Terminal_Growth"]);fc=[mv(s,y,"FCFF") for y in range(2026,2031)];pv=sum(v/(1+ww)**n for n,v in enumerate(fc,1));tv=fc[-1]*(1+g)/(ww-g);pvt=tv/(1+ww)**5;ev=pv+pvt;eq=ev+adj;ps=eq/(mv(s,2026,"EPS_DENOMINATOR_SHARES")/D(1_000_000));check(f"DCF_{s}",near(ps,r["Per_Share"],D(".00002")),str(ps))
    base=next(r for r in scenarios if r["Scenario"]=="BASE");evrow=next(r for r in bridge if r["Item"]=="Enterprise value");eqrow=next(r for r in bridge if r["Item"]=="Equity value")
    check("Bridge_Base_EV",near(evrow["Amount"],base["Enterprise_Value"],D(".000001")))
    check("Bridge_Base_Equity",near(eqrow["Amount"],base["Equity_Value"],D(".000001")))
    check("Bridge_Current_Treasury_Included",any(r["Accounting_Metric"]=="BS_CURRENT_PORTION_NONCURRENT_ASSETS_TREASURY" and r["Included"]=="YES" and r["Sign"]=="1" for r in bridge))
    check("Bridge_Trading_Liability_Deducted",any(r["Accounting_Metric"]=="BS_TRADING_FINANCIAL_LIABILITIES" and r["Included"]=="YES" and r["Sign"]=="-1" for r in bridge))
    check("Receivables_Financing_Not_Double_Counted",any(r["Accounting_Metric"]=="BS_RECEIVABLES_FINANCING" and r["Included"]=="NO" for r in bridge))
    peers=rows("model/H6_NORMALIZED_PEER_DATA_R3.csv");eligible=[r for r in peers if r["Status"]=="ELIGIBLE"];h6=j("verification/inputs/authorities/H6_AUTHORITY_R3.json")
    keymap={"EV_Revenue":"EV_Revenue","EV_EBITDA":"EV_EBITDA","EV_EBIT":"EV_EBIT","PE":"PE","PB":"PB"}
    selected={k:quantile([D(r[v]) for r in eligible],D(".5")) for k,v in keymap.items()}
    for k,v in selected.items():check("H6_Median_"+k,near(v,h6["Selected_Multiples"][k],D(".00000002")),str(v))
    mp={r["Metric"]:r for r in rows("workpapers/MIDEA_COMPARABLE_PERIOD_WORKPAPER_R3.csv")};shares=D(scenarios[1]["Shares_Million"]);imp=[(selected["EV_Revenue"]*D(mp["Revenue"]["Value"])+adj)/shares,(selected["EV_EBIT"]*D(mp["EBIT"]["Value"])+adj)/shares,selected["PE"]*D(mp["Attributable_NI"]["Value"])/shares,selected["PB"]*D(mp["Book_Equity"]["Value"])/shares]
    for label,val in zip(["EV/Revenue","EV/EBIT","P/E","P/B"],imp):check("H6_Implied_"+label,near(val,h6["Implied_Values_Per_Share"][label],D(".00002")),str(val))
    for label,f in [("Low",D(".25")),("Central",D(".5")),("High",D(".75"))]:check("H6_Range_"+label,near(quantile(imp,f),h6["Comps_Range"][label],D(".00002")))
    check("Peer_Midea_Period_Basis_Mismatches",h6["Peer_Midea_Period_Basis_Mismatches"]==0)

    registry={r["Formula_ID"]:r for r in rows("model/H3B_FORMULA_REGISTRY.csv")}
    expected_registry="EBIT*(1-DRV_EFFECTIVE_TAX_RATE_PERCENT/100)+PPE_DEPRECIATION+PPE_AMORTIZATION-PPE_CAPEX-DELTA(BS_AR+BS_NOTES_RECEIVABLE+BS_RECEIVABLES_FINANCING+BS_INVENTORY+BS_CONTRACT_ASSETS+BS_PREPAYMENTS+BS_OTHER_RECEIVABLES+BS_OTHER_CURRENT_ASSETS_OPERATING-BS_AP-BS_CONTRACT_LIABILITIES-BS_NOTES_PAYABLE-BS_EMPLOYEE_COMP-BS_OTHER_PAYABLES-BS_OTHER_CURRENT_LIABILITIES_OPERATING-BS_OTHER_TAXES_PAYABLE)-DELTA(BS_LOANS_ADVANCES_CURRENT+BS_CURRENT_PORTION_NONCURRENT_ASSETS_FINANCE-BS_CUSTOMER_DEPOSITS)"
    check("H3B_Formula_Registry_FCFF_Semantics",registry.get("F-H3B-FCFF",{}).get("Formula")==expected_registry,registry.get("F-H3B-FCFF",{}).get("Formula","MISSING"))
    return checks
def manifest_check():
    manifest=j("release/REPOSITORY_MANIFEST_R3_1.json");fails=[]
    governance_roots={"release/REPOSITORY_MANIFEST_R3_1.json","release/REPOSITORY_AUTHORITY_R3_1.json","release/FINAL_GITHUB_PUBLICATION_RESULT_R3_1.json"}
    expected={r["Path"]:r for r in manifest["Files"]};actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file() and p.relative_to(ROOT).as_posix() not in governance_roots and ".git" not in p.parts and ".pytest_cache" not in p.parts and "__pycache__" not in p.parts and p.suffix.lower() not in {".pyc",".pyo"}}
    if set(expected)!=actual:fails.append({"Control":"Manifest_Member_Set","Missing":sorted(actual-set(expected)),"Extra":sorted(set(expected)-actual)})
    for rel,r in expected.items():
      p=ROOT/rel
      if not p.exists() or sha(p)!=r["SHA256"] or p.stat().st_size!=r["Bytes"]:fails.append({"Control":"Manifest_Hash","Path":rel})
    return fails
