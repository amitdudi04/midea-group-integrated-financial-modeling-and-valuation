"""Independent arithmetic, causality and completeness controls for R4 alternatives.

Reads the generated outputs but independently reconstructs source-based dates,
operating FCFF, the 2031 terminal normalization, the provisional bridge
and the after-the-fact nine-month comparison.
"""
from __future__ import annotations
from datetime import date
import csv,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DIR=ROOT/"research_r4"
def rd(path):
 with (ROOT/path).open(encoding="utf8",newline="") as f:return list(csv.DictReader(f))
def ok(a,b,tag,tol=0.000035):
 assert math.isclose(float(a),float(b),abs_tol=tol,rel_tol=0),f"{tag}: {a} != {b}"
def run():
 from rebuild_exploratory_revision import INTERIM,NINE_MONTH,scenarios
 val=rd("research_r4/dated_valuation_scenarios.csv")
 annual=rd("research_r4/linked_operating_fcff_scenarios.csv")
 bridge=rd("research_r4/provisional_june_bridge.csv")
 sources=rd("research_r4/publication_cutoff_registry.csv")
 post=rd("research_r4/post_sample_nine_month_evaluation.csv")
 ebit=rd("research_r4/ebit_bridge_from_r3.csv")
 assert len(val)==3 and len(annual)==15 and len(bridge)==3 and len(sources)==3 and len(post)==2 and len(ebit)==15
 assert {x["Scenario"] for x in val}=={"BEAR","BASE","BULL"}
 assert {x["Scenario"] for x in annual}=={"BEAR","BASE","BULL"}
 assert sources[1]["Known_By_Valuation"]=="YES" and sources[2]["Known_By_Valuation"]=="NO"
 assert sources[2]["Use"]=="POST_SAMPLE_ONLY"
 assert date.fromisoformat(NINE_MONTH["publication_date"])>date(2026,9,11)
 assert date.fromisoformat(INTERIM["publication_date"])<date(2026,9,11)
 r3={(r["Scenario"],int(r["Year"]),r["Metric_ID"]):float(r["Value"])
    for r in rd("model/H3B_MODEL_LONG.csv")}
 orig={r["Scenario"]:r for r in rd("model/H5_SCENARIO_VALUATION_R3.csv")}
 original_ev=float(orig["BASE"]["Enterprise_Value"])
 all_bridge=rd("model/H5_EV_TO_EQUITY_BRIDGE.csv")
 adj=sum(float(x["Amount"])*float(x["Sign"]) for x in all_bridge if x["Included"]=="YES")
 ok(original_ev+adj,orig["BASE"]["Equity_Value"],"baseline bridge")
 for x in ebit:
  s=x["Scenario"];y=int(x["Year"]);p=r3[s,y,"IS_OPERATING_PROFIT"];inv=r3[s,y,"IS_INVESTMENT_INCOME"]
  fair=r3[s,y,"IS_FAIR_VALUE_CHANGE"];finance=r3[s,y,"IS_FINANCE_RESULT"]
  ok(p-inv-fair-finance,x["Reconciled_EBIT"],f"recurring bridge {s}/{y}")
  ok(x["Reconciled_EBIT"],r3[s,y,"EBIT"],"no direct double count")
 stub=(date(2026,12,31)-date(2026,9,11)).days/365
 ok(stub,111/365,"remaining 2026 days")
 fiscal2025rev=r3["BASE",2025,"IS_OPERATING_REVENUE"]
 fiscal2025ni=r3["BASE",2025,"IS_ATTRIBUTABLE_NI"]
 for x in val:
  s=x["Scenario"];par=scenarios[s]
  yr=sorted([r for r in annual if r["Scenario"]==s],key=lambda r:int(r["Year"]))
  assert [int(t["Year"]) for t in yr]==list(range(2026,2031))
  revenue2026=INTERIM["revenue_2026_H1"]+(fiscal2025rev-INTERIM["revenue_2025_H1"])*(1+par["H2_yoy"])
  ok(yr[0]["Revenue"],revenue2026,f"{s} 2026 revenue")
  prev_nwc=-131003.796;prev_fs=11900.780
  pv_sum=0.
  for i,row in enumerate(yr):
   rev=float(row["Revenue"]);margin=par["margins"][i];w=par["wacc"]
   if i:ok(rev,float(yr[i-1]["Revenue"])*(1+par["growth"][i-1]),"revenue forward")
   ebit=rev*margin;nopat=ebit*(1-.152566)
   da=rev*par["da"];capex=rev*par["capex"]
   nwc=rev*par["nwc_ratio"];fs=rev*par["fs_ratio"]
   dnwc=nwc-prev_nwc;dfs=fs-prev_fs
   fcff=nopat+da-capex-dnwc-dfs
   power=stub+i;cash=fcff*(stub if i==0 else 1)
   pv=cash/(1+w)**power;pv_sum+=pv
   for k,num in [("EBIT",ebit),("NOPAT",nopat),("DA",da),("CAPEX",capex),
      ("Operating_NWC",nwc),("Delta_Operating_NWC",dnwc),
      ("Finance_Services_Net_Investment",fs),
      ("Delta_Finance_Services_Net_Investment",dfs),
      ("FCFF",fcff),("Dated_FCFF",cash),
      ("Years_From_Valuation",power),("Discounted_FCFF",pv)]:
    ok(row[k],num,s+"/"+k)
   prev_nwc=nwc;prev_fs=fs
  rev31=float(yr[-1]["Revenue"])*(1+par["g"])
  nwc31=rev31*par["nwc_ratio"];fs31=rev31*par["fs_ratio"]
  fcff31=(rev31*par["margins"][-1]*(1-.152566)
          +rev31*par["da"]-rev31*par["capex"]
          -(nwc31-prev_nwc)-(fs31-prev_fs))
  ok(x["Normalized_2031_FCFF"],fcff31,"terminal FCFF")
  pv_tv=fcff31/(par["wacc"]-par["g"])/(1+par["wacc"])**(stub+4)
  ev=pv_sum+pv_tv
  ok(x["PV_Remaining_2026_Through_2030_FCFF"],pv_sum,"PV periods")
  ok(x["PV_Terminal_Value"],pv_tv,"PV terminal")
  ok(x["Enterprise_Value"],ev,"enterprise")
  b=next(z for z in bridge if z["Scenario"]==s)
  required_cash=.08285274*revenue2026
  excess=max(0,INTERIM["cash_equivalents_2026_06"]-required_cash)
  available_treasury=INTERIM["current_treasury_2026_06"]*par["liquid"]
  adjustment=excess+available_treasury+INTERIM["term_deposits_2026_06"]*par["liquid"]-80327.263-INTERIM["nci_2026_06"]
  ok(b["Operating_Cash_Reserve_Proxy"],required_cash,"cash reserve")
  ok(b["Bridge_Provisional"],adjustment,"provisional bridge")
  ok(x["Bridge_Adjustment_Provisional"],adjustment,"provisional bridge again")
  ok(x["Per_Share_Provisional"],(ev+adjustment)/7402.51366,"per share")
  # Published Sep 10 A-share register, with H shares at last-known June 30
  # population. Indicative only; H treasury and option dilution are uncertain.
  latest=(6811460392+650848500)/1_000_000
  ok(x["Sept10_Indicative_Shares_Million"],latest,"dated shares")
  ok(x["Per_Share_Sept10_Indicative"],(ev+adjustment)/latest,
     "pre-valuation-date indicative share population")
  assert x["Source_Limitation"].startswith("2026_STUB_ESTIMATED")
 for row in post:
  metric=row["Metric"]; m="IS_OPERATING_REVENUE" if metric=="Revenue" else "IS_ATTRIBUTABLE_NI"
  actual=NINE_MONTH["revenue_2026_9M" if metric=="Revenue" else "attributable_2026_9M"]
  prior=NINE_MONTH["revenue_2025_9M" if metric=="Revenue" else "attributable_2025_9M"]
  remaining=r3["BASE",2026,m]-actual
  previous=r3["BASE",2025,m]-prior
  ok(row["Implied_2026_Q4"],remaining,"out-of-sample quarter")
  ok(row["Required_Q4_YOY"],remaining/previous-1,"out-of-sample growth")
  assert row["Used_In_Sept_Valuation"]=="NO"
 metadata=json.loads((DIR/"assumptions.json").read_text(encoding="utf8"))
 assert metadata["original_R3_unchanged"] is True
 assert metadata["partial_2026_stub_days"]==111
 print("PASS R4 independent audit: 15 annual FCFF rows; 3 date discounts; "
       "15 original EBIT reconciliations; 3 provisional bridges; "
       "2 strictly post-valuation 9M comparisons.")

if __name__=="__main__":run()
