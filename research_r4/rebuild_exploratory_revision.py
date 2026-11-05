"""R4 experimental valuation *overlay*, never an overwrite of accepted R3.

Runs offline from tracked R3 model plus explicitly cited 2026 disclosures.
Values are RMB millions. Forecasts are assumptions, not issuer guidance.
No claim is made to rebuild the issuer's full three-statement model.
"""
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"research_r4"
OUT.mkdir(exist_ok=True)
VALUATION=date(2026,9,11)
DAYS_2026=(date(2026,12,31)-VALUATION).days
STUB=DAYS_2026/365
SOURCES={
 "interim_CAS":"https://static.cninfo.com.cn/finalpage/2026-08-28/1225533135.PDF",
 "nine_month_CAS":"https://static.cninfo.com.cn/finalpage/2026-10-30/1225645132.PDF",
}
INTERIM={
 "publication_date":"2026-08-29", "revenue_2026_H1":260042.490,
 "revenue_2025_H1":251123.714, "attributable_2026_H1":26446.037,
 "attributable_2025_H1":26013.690,
 "adjusted_attributable_2026_H1":19595.179,
 "adjusted_attributable_2025_H1":26235.399,
 "cfo_2026_H1":37552.090, "cfo_2025_H1":37281.015,
 "cash_equivalents_2026_06":74614.244,
 "term_deposits_2026_06":8496.066,
 "current_treasury_2026_06":158310.938,
 "nci_2026_06":12931.886,
 "assets_2026_06":643101.789, "parent_equity_2026_06":212861.055
}
NINE_MONTH={
 "publication_date":"2026-10-30", "revenue_2026_9M":367364.936,
 "revenue_2025_9M":363056.751,
 "attributable_2026_9M":41393.371,
 "attributable_2025_9M":37883.383,
 "adjusted_attributable_2026_9M":28787.970,
 "cfo_2026_9M":40187.380
}
# 2026 H1 amounts are Chinese Accounting Standards (CAS) operating revenue,
# not consolidated total revenue inclusive of finance-company interest.
# June 2026 debt is a provisionally sourced rounded aggregate, requiring
# a final note-level face/carrying-value and convertible/lease reconciliation.
H1_DEBT_PROVISIONAL=80327.263
OPERATING_CASH_RESERVE_RATIO=.08285274
TAX=.152566
shares=7402.51366
scenarios={
 "BEAR":{"H2_yoy":-.06,"growth":[-.03,.00,.01,.015],
         "margins":[.075,.070,.069,.069,.070],"da":.018,
         "capex":.027,"nwc_ratio":-.24,"fs_ratio":.030,
         "wacc":.085,"g":.010,"liquid":.25},
 "BASE":{"H2_yoy":.04,"growth":[.04,.045,.045,.04],
         "margins":[.095,.093,.091,.090,.090],"da":.019,
         "capex":.023,"nwc_ratio":-.27,"fs_ratio":.026,
         "wacc":.065,"g":.020,"liquid":.50},
 "BULL":{"H2_yoy":.10,"growth":[.08,.075,.07,.065],
         "margins":[.105,.106,.107,.108,.109],"da":.0195,
         "capex":.021,"nwc_ratio":-.29,"fs_ratio":.024,
         "wacc":.055,"g":.025,"liquid":.75}
}

def read_rows(path):
 with (ROOT/path).open(newline="", encoding="utf-8") as f:
  return list(csv.DictReader(f))

def write_csv(name,rows,fields):
 with (OUT/name).open("w", newline="", encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def fmt(x):
 return round(float(x),8)

def main():
 r3=read_rows("model/H3B_MODEL_LONG.csv")
 idx={(r["Scenario"],int(r["Year"]),r["Metric_ID"]):float(r["Value"]) for r in r3}
 def v(s,y,m):return idx[s,y,m]
 accepted={r["Scenario"]:r for r in read_rows("model/H5_SCENARIO_VALUATION_R3.csv")}
 original=accepted["BASE"]
 def exact_bridge():
  rows=read_rows("model/H5_EV_TO_EQUITY_BRIDGE.csv")
  return sum(float(x["Amount"])*float(x["Sign"]) for x in rows if x["Included"]=="YES")
 assert abs((float(original["Enterprise_Value"])+exact_bridge())-float(original["Equity_Value"]))<.00001
 # EBIT is arithmetically reconciled against non-operating investment, FV
 # and finance result, rather than simply equating accounting op profit to EBIT.
 recurring=[]
 for s in ("BEAR","BASE","BULL"):
  for year in range(2026,2031):
   operating=v(s,year,"IS_OPERATING_PROFIT")
   investments=v(s,year,"IS_INVESTMENT_INCOME")
   fv=v(s,year,"IS_FAIR_VALUE_CHANGE")
   finance=v(s,year,"IS_FINANCE_RESULT")
   core=operating-investments-fv-finance
   assert abs(core-v(s,year,"EBIT"))<.000001
   recurring.append({"Scenario":s,"Year":year,
                     "Operating_Profit":fmt(operating),
                     "Less_Investment_Income":fmt(investments),
                     "Less_Fair_Value_Gains":fmt(fv),
                     "Less_Finance_Result":fmt(finance),
                     "Reconciled_EBIT":fmt(core),
                     "Excluded_Direct_Financial_Gains":"YES",
                     "Other_Income_Still_Requires_Recurrence_Assessment":"YES"})
 write_csv("ebit_bridge_from_r3.csv",recurring,list(recurring[0]))
 # H1 was published before the valuation date, but was excluded from the
 # originally declared Aug 20 operating-cutoff experiment.
 audit=[
  {"Dataset":"FY2025 R3","As_Of":"2025-12-31","Known_By_Valuation":"YES",
   "Revenue_RMBm":fmt(v("BASE",2025,"IS_OPERATING_REVENUE")),
   "Attributable_NI_RMBm":fmt(v("BASE",2025,"IS_ATTRIBUTABLE_NI")),
   "CFO_RMBm":fmt(v("BASE",2025,"CF_CFO")),
   "Use":"HISTORICAL_R3"},
  {"Dataset":"2026 H1 CAS published Aug29","As_Of":"2026-06-30","Known_By_Valuation":"YES",
   "Revenue_RMBm":INTERIM["revenue_2026_H1"],"Attributable_NI_RMBm":INTERIM["attributable_2026_H1"],
   "CFO_RMBm":INTERIM["cfo_2026_H1"],"Use":"R4_INFORMATION_SET"},
  {"Dataset":"2026 9M CAS published Oct30","As_Of":"2026-09-30","Known_By_Valuation":"NO",
   "Revenue_RMBm":NINE_MONTH["revenue_2026_9M"],
   "Attributable_NI_RMBm":NINE_MONTH["attributable_2026_9M"],
   "CFO_RMBm":NINE_MONTH["cfo_2026_9M"],"Use":"POST_SAMPLE_ONLY"}
 ]
 write_csv("publication_cutoff_registry.csv",audit,list(audit[0]))
 old2025=v("BASE",2025,"IS_OPERATING_REVENUE")
 old2025_ni=v("BASE",2025,"IS_ATTRIBUTABLE_NI")
 h2_25=old2025-INTERIM["revenue_2025_H1"]
 projections=[]; valuations=[]; date_bridge=[]
 for s,opts in scenarios.items():
  h1=INTERIM["revenue_2026_H1"]
  revenue=h1+h2_25*(1+opts["H2_yoy"])
  nwc_prev=-131003.796
  fs_prev=11900.780
  total_fcff=[];last={}
  for i,year in enumerate(range(2026,2031)):
   if i:revenue*=1+opts["growth"][i-1]
   ebit=revenue*opts["margins"][i]
   nopat=ebit*(1-TAX)
   da=revenue*opts["da"]
   capex=revenue*opts["capex"]
   nwc=revenue*opts["nwc_ratio"]
   fs=revenue*opts["fs_ratio"]
   delta_nwc=nwc-nwc_prev
   delta_fs=fs-fs_prev
   fcff=nopat+da-capex-delta_nwc-delta_fs
   assert abs(fcff-(nopat+da-capex-delta_nwc-delta_fs))<.00000001
   # 2026 projected annual FCFF has no certified realized Jan-Sep FCFF bridge.
   # Prorate only the remaining 111 days; do not imply accounting-actual stub.
   cash=fcff*(STUB if year==2026 else 1.0)
   power=STUB+(year-2026)
   pv=cash/(1+opts["wacc"])**power
   total_fcff.append(pv)
   projections.append({"Scenario":s,"Year":year,"Revenue":fmt(revenue),
      "EBIT":fmt(ebit),"EBIT_Margin":fmt(opts["margins"][i]),
      "NOPAT":fmt(nopat),"DA":fmt(da),"CAPEX":fmt(capex),
      "Operating_NWC":fmt(nwc),"Delta_Operating_NWC":fmt(delta_nwc),
      "Finance_Services_Net_Investment":fmt(fs),
      "Delta_Finance_Services_Net_Investment":fmt(delta_fs),
      "FCFF":fmt(fcff),"Remaining_2026_Stub_Ratio":fmt(STUB if year==2026 else 1),
      "Dated_FCFF":fmt(cash),"Years_From_Valuation":fmt(power),
      "Discounted_FCFF":fmt(pv)})
   nwc_prev=nwc;fs_prev=fs
   last={"revenue":revenue,"nwc":nwc,"fs":fs,"nopat":nopat,"ebit":ebit,"year":year}
  rev2031=last["revenue"]*(1+opts["g"])
  # Rebuild 2031 steady-state EBIT/reinvestment from revenue, NOT
  # multiply 2030 temporary NWC release by Gordon growth.
  ebit2031=rev2031*opts["margins"][-1]
  nwc2031=rev2031*opts["nwc_ratio"]; fs2031=rev2031*opts["fs_ratio"]
  fcff2031=(ebit2031*(1-TAX)+rev2031*opts["da"]-rev2031*opts["capex"]
           -(nwc2031-last["nwc"])-(fs2031-last["fs"]))
  assert opts["wacc"]>opts["g"] and fcff2031>0
  power2030=STUB+4
  terminal_pv=(fcff2031/(opts["wacc"]-opts["g"]))/(1+opts["wacc"])**power2030
  ev=sum(total_fcff)+terminal_pv
  # H1 2026 semiannual restatement: proven new quantities for cash,
  # current F.I. products and NCI; debt is a rounded *provisional*
  # H1 borrowing source and further adjustments are conservatively omitted.
  min_reserve=OPERATING_CASH_RESERVE_RATIO*(INTERIM["revenue_2026_H1"]+h2_25*(1+opts["H2_yoy"]))
  excess=max(0,INTERIM["cash_equivalents_2026_06"]-min_reserve)
  treasury=INTERIM["current_treasury_2026_06"]*opts["liquid"]
  term=INTERIM["term_deposits_2026_06"]*opts["liquid"]
  nci=INTERIM["nci_2026_06"]
  bridge=excess+treasury+term-H1_DEBT_PROVISIONAL-nci
  equity=ev+bridge
  valuations.append({"Scenario":s,"Valuation_Date":VALUATION.isoformat(),
     "Forecast_Source":"R4_DISCLOSURE_CONSTRAINED_ILLUSTRATIVE",
     "WACC":fmt(opts["wacc"]),"Terminal_Growth":fmt(opts["g"]),
     "Years_To_2026_End":fmt(STUB),
     "PV_Remaining_2026_Through_2030_FCFF":fmt(sum(total_fcff)),
     "Normalized_2031_Revenue":fmt(rev2031),
     "Normalized_2031_EBIT":fmt(ebit2031),
     "Normalized_2031_NWC_Change":fmt(nwc2031-last["nwc"]),
     "Normalized_2031_Finance_Investment_Change":fmt(fs2031-last["fs"]),
     "Normalized_2031_FCFF":fmt(fcff2031),
     "PV_Terminal_Value":fmt(terminal_pv),"Enterprise_Value":fmt(ev),
     "Bridge_Adjustment_Provisional":fmt(bridge),
     "Equity_Value_Provisional":fmt(equity),"Shares_Million_R3":fmt(shares),
     "Per_Share_Provisional":fmt(equity/shares),
     "Source_Limitation":"2026_STUB_ESTIMATED;JUNE_BRIDGE_PROVISIONAL;NOT_FULL_THREE_STATEMENT"})
  date_bridge.append({"Scenario":s,"H1_Cash_Equivalent_RMBm":INTERIM["cash_equivalents_2026_06"],
    "Operating_Cash_Reserve_Proxy":fmt(min_reserve),"Excess_Cash_Proxy":fmt(excess),
    "H1_Current_Fixed_Income_Products":INTERIM["current_treasury_2026_06"],
    "Treasury_Available_Fraction_ASSUMED":opts["liquid"],
    "Available_Treasury_Proxy":fmt(treasury),
    "H1_Term_Deposits_Source":INTERIM["term_deposits_2026_06"],
    "Term_Deposits_Available_Proxy":fmt(term),
    "H1_Debt_Provisional":H1_DEBT_PROVISIONAL,
    "H1_NCI":nci,"Omitted_Stale_2025_Other_Investments":"YES",
    "Bridge_Provisional":fmt(bridge),"Dated_Through":"2026-06-30"})
 write_csv("linked_operating_fcff_scenarios.csv",projections,list(projections[0]))
 write_csv("dated_valuation_scenarios.csv",valuations,list(valuations[0]))
 write_csv("provisional_june_bridge.csv",date_bridge,list(date_bridge[0]))
 # Strict post-sample observations never appear in scenarios or WACC.
 evals=[]
 for metric,fr,ytd,tgt in [
  ("Revenue","IS_OPERATING_REVENUE","revenue_2026_9M","revenue_2025_9M"),
  ("Attributable_Net_Income","IS_ATTRIBUTABLE_NI",
    "attributable_2026_9M","attributable_2025_9M")]:
  fy=v("BASE",2026,fr); actual=NINE_MONTH[ytd]; prior_year=NINE_MONTH[tgt]
  old2025=v("BASE",2025,fr)
  q4_26=fy-actual;q4_25=old2025-prior_year
  evals.append({"Metric":metric,"Model_FY2026_R3":fmt(fy),
    "Observed_2026_9M_POST_SAMPLE":fmt(actual),
    "Implied_2026_Q4":fmt(q4_26),
    "Actual_2025_Q4":fmt(q4_25),
    "Required_Q4_YOY":fmt(q4_26/q4_25-1),
    "Post_Sample_Publication_Date":"2026-10-30",
    "Used_In_Sept_Valuation":"NO"})
 write_csv("post_sample_nine_month_evaluation.csv",evals,list(evals[0]))
 meta={"research_revision":"R4_EXPLORATORY","original_R3_unchanged":True,
  "as_of":"2026-09-11","interim_publication":"2026-08-29",
  "nine_month_publication":"2026-10-30",
  "original_operating_cutoff":"2026-08-20",
  "interim_source":SOURCES["interim_CAS"],"post_sample_source":SOURCES["nine_month_CAS"],
  "partial_2026_stub_days":DAYS_2026,"partial_2026_stub_ratio":STUB,
  "limitations":["calendar_day_pro_rata_2026_FCFF_not_realized_stub",
  "June_balance_sheet_bridge_not_September_11","H1_debt_June_2026_borrowings_80327_263_not_September_date",
  "Treasury_availability_assumed_not_proven",
  "other_operating_income_not_exhaustively_normalized",
  "not_a_rebuilt_three_statement_forecast","not_an_investment_price_target"]}
 (OUT/"assumptions.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
 for row in valuations:
  assert abs(row["Enterprise_Value"]+row["Bridge_Adjustment_Provisional"]-row["Equity_Value_Provisional"])<.00003
  assert row["PV_Terminal_Value"]>0 and row["Per_Share_Provisional"]>0
 print("PASS R4: 15 linked yearly operating-FCFF records; 3 dated discounted scenarios; "
       "15 original EBIT reconciliations; in-date H1 and excluded later 9M; "
       "3 provisional June EV bridges; 2 post-sample comparisons.")
 print(json.dumps({x["Scenario"]:x["Per_Share_Provisional"] for x in valuations},
                  sort_keys=True))

if __name__=="__main__":
 main()
