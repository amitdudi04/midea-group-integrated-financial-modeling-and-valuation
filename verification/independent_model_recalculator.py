from __future__ import annotations
import csv,json,sys
from decimal import Decimal as D,getcontext
from pathlib import Path
getcontext().prec=50;sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent.parent
def rows(rel):
    with (ROOT/rel).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def obj(rel):return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def near(a,b,t=D(".000002")):return abs(D(str(a))-D(str(b)))<=t
def quantile(values,f):
    x=sorted(values);p=D(len(x)-1)*f;lo=int(p);hi=min(lo+1,len(x)-1);w=p-lo;return x[lo]*(1-w)+x[hi]*w
fail=[]
def ck(name,ok,detail=""):
    if not ok:fail.append({"Control":name,"Detail":detail})
data=rows("model/H3B_MODEL_LONG.csv");ix={(r["Scenario"],int(r["Year"]),r["Metric_ID"]):D(r["Value"]) for r in data}
v=lambda s,y,m:ix[(s,y,m)]
assets=["BS_AR","BS_NOTES_RECEIVABLE","BS_RECEIVABLES_FINANCING","BS_INVENTORY","BS_CONTRACT_ASSETS","BS_PREPAYMENTS","BS_OTHER_RECEIVABLES","BS_OTHER_CURRENT_ASSETS_OPERATING"]
liabs=["BS_AP","BS_CONTRACT_LIABILITIES","BS_NOTES_PAYABLE","BS_EMPLOYEE_COMP","BS_OTHER_PAYABLES","BS_OTHER_CURRENT_LIABILITIES_OPERATING","BS_OTHER_TAXES_PAYABLE"]
for s in ["BEAR","BASE","BULL"]:
  for y in range(2026,2031):
    ck(f"BS_{s}_{y}",near(v(s,y,"BS_TOTAL_ASSETS"),v(s,y,"BS_TOTAL_LIABILITIES")+v(s,y,"BS_TOTAL_EQUITY")))
    ck(f"CASH_{s}_{y}",near(v(s,y,"CF_CLOSING_CASH"),v(s,y,"CF_OPENING_CASH")+v(s,y,"CF_CFO")+v(s,y,"CF_CFI")+v(s,y,"CF_CFF")+v(s,y,"CF_FX_EFFECT")))
    ck(f"PPE_{s}_{y}",near(v(s,y,"BS_PPE")+v(s,y,"BS_CIP"),v(s,y-1,"BS_PPE")+v(s,y-1,"BS_CIP")+v(s,y,"PPE_CAPEX")-v(s,y,"PPE_DEPRECIATION")))
    ck(f"EQUITY_{s}_{y}",near(v(s,y,"BS_RETAINED_EARNINGS"),v(s,y-1,"BS_RETAINED_EARNINGS")+v(s,y,"IS_ATTRIBUTABLE_NI")-v(s,y,"DIVIDENDS")))
    ck(f"EPS_{s}_{y}",near(v(s,y,"IS_BASIC_EPS"),v(s,y,"IS_ATTRIBUTABLE_NI")*D(1000000)/v(s,y,"EPS_DENOMINATOR_SHARES"),D(".00000002")))
    nwc=lambda yy:sum(v(s,yy,k) for k in assets)-sum(v(s,yy,k) for k in liabs)
    fin=lambda yy:v(s,yy,"BS_LOANS_ADVANCES_CURRENT")+v(s,yy,"BS_CURRENT_PORTION_NONCURRENT_ASSETS_FINANCE")-v(s,yy,"BS_CUSTOMER_DEPOSITS")
    fcff=v(s,y,"EBIT")*(1-v(s,y,"DRV_EFFECTIVE_TAX_RATE_PERCENT")/100)+v(s,y,"PPE_DEPRECIATION")+v(s,y,"PPE_AMORTIZATION")-v(s,y,"PPE_CAPEX")-(nwc(y)-nwc(y-1))-(fin(y)-fin(y-1))
    ck(f"FCFF_{s}_{y}",near(v(s,y,"FCFF"),fcff),str(fcff))
h4=obj("model/H4_WACC_CALCULATION_R3.json");rf=D(h4["Risk_Free_Rate"]);erp=D(h4["ERP_Full_Precision"]);beta=D(h4["Beta"]);kd=D(h4["PreTax_Cost_of_Debt"]);tax=D(h4["Tax_Rate"]);ew=D(h4["Equity_Weight"]);dw=D(h4["Debt_Weight"])
w=(rf+beta*erp)*ew+kd*(1-tax)*dw;ck("WACC",near(w,h4["WACC"],D(".00000002")),str(w))
bridge=rows("model/H5_EV_TO_EQUITY_BRIDGE.csv");adj=sum(D(r["Amount"])*D(r["Sign"]) for r in bridge if r["Included"]=="YES")
scenarios=rows("model/H5_SCENARIO_VALUATION_R3.csv")
for r in scenarios:
    s=r["Scenario"];ww=D(r["WACC"]);g=D(r["Terminal_Growth"]);fc=[v(s,y,"FCFF") for y in range(2026,2031)];pv=sum(x/(1+ww)**n for n,x in enumerate(fc,1));tv=fc[-1]*(1+g)/(ww-g);ev=pv+tv/(1+ww)**5;eq=ev+adj;ps=eq/(v(s,2026,"EPS_DENOMINATOR_SHARES")/D(1000000));ck("DCF_"+s,near(ps,r["Per_Share"],D(".00002")),str(ps))
base=next(r for r in scenarios if r["Scenario"]=="BASE");rev=obj("model/H5_REVERSE_DCF_R3.json");target=D(rev["Target_Enterprise_Value"]);pv=D(base["PV_Forecast_FCFF"]);last=v("BASE",2030,"FCFF");g=D(rev["Implied_Terminal_Growth"]);replayed=pv+last*(1+g)/(D(base["WACC"])-g)/(1+D(base["WACC"]))**5;ck("REVERSE_DCF",near(target,replayed,D(".02")),str(replayed))
peers=[r for r in rows("model/H6_NORMALIZED_PEER_DATA_R3.csv") if r["Status"]=="ELIGIBLE"];h6=obj("verification/inputs/authorities/H6_AUTHORITY_R3.json")
for k in ["EV_Revenue","EV_EBITDA","EV_EBIT","PE","PB"]:ck("COMPS_MEDIAN_"+k,near(quantile([D(r[k]) for r in peers],D(".5")),h6["Selected_Multiples"][k],D(".00000002")))
result={"Schema":"INDEPENDENT_MODEL_RECALCULATION_R3_1","Status":"PASS" if not fail else "FAIL","Failure_Count":len(fail),"Failures":fail,"Production_Calculation_Functions_Imported":False,"Controls":["OPERATING_NWC","DELTA_NWC","FCFF","WACC","DCF","REVERSE_DCF","EV_TO_EQUITY","COMPS","EPS","ACCOUNTING_IDENTITIES"]}
print(json.dumps(result,sort_keys=True,separators=(",",":")));raise SystemExit(0 if not fail else 1)
