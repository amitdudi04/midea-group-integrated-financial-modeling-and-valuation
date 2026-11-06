"""Independent checks of R4.1 consolidated aggregate pro-forma forecast outputs."""
from __future__ import annotations
import csv,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(p):
 with (ROOT/p).open(newline="",encoding="utf8") as f:return list(csv.DictReader(f))
def near(a,b,where,atol=2e-5):
 assert math.isclose(float(a),float(b),abs_tol=atol,rel_tol=0),f"{where}: {a} != {b}"

def main():
 records=read("research_r4/linked_three_statements_proforma.csv")
 values=read("research_r4/dated_three_statement_valuation.csv")
 actual=read("research_r4/interim_nwc_and_share_reconciliation.csv")
 assert len(records)==15 and len(values)==3 and len(actual)==3
 assert {r["Scenario"] for r in records}=={"BEAR","BASE","BULL"}
 assert {r["Scenario"] for r in values}=={"BEAR","BASE","BULL"}
 for case in ("BEAR","BASE","BULL"):
  group=[x for x in records if x["Scenario"]==case]
  assert len(group)==5
  assert group[0]["Period"]=="2026_H2"
  for row in group:
   label=case+"/"+row["Period"]
   assets=sum(float(row[k]) for k in [
    "Cash_End","PPE_End","Operating_NWC_Assets_End","Finance_Loans_Assets_End",
    "Financial_Asset_Treasury_End","Other_Assets_End"])
   liabilities=sum(float(row[k]) for k in [
    "Debt_End","Operating_NWC_Liabilities_End","Finance_Customer_Deposits_End",
    "Other_Liabilities_End"])
   near(row["Total_Assets"],assets,label+" assets")
   near(row["Total_Liabilities"],liabilities,label+" liabilities")
   near(assets,liabilities+float(row["Total_Equity"]),label+" BS")
   near(float(row["Operating_EBIT_This_Period"])-float(row["Debt_Interest"])
        -float(row["Income_Tax"]),row["Net_Income"],label+" income")
   near(float(row["Net_Income"])+float(row["Depreciation_Amortization"])
        -float(row["Delta_Operating_NWC"])-float(row["Delta_Finance_Loans_Net"]),
        row["CFO"],label+" CFO")
   near(-float(row["Capital_Expenditure"]),row["CFI"],label+" CFI")
   near(float(row["New_Borrowing_Financing_Plug"])-float(row["Dividends"]),
        row["CFF"],label+" financing")
   near(float(row["CFO"])+float(row["CFI"])+float(row["CFF"]),
        row["Net_Change_Cash"],label+" movement")
   near(float(row["Operating_EBIT_This_Period"])*(1-.152566)
        +float(row["Depreciation_Amortization"])
        -float(row["Capital_Expenditure"])
        -float(row["Delta_Operating_NWC"])
        -float(row["Delta_Finance_Loans_Net"]),
        row["Unlevered_FCFF"],label+" FCFF")
   assert float(row["Cash_End"])>=0 and float(row["PPE_End"])>=0
   assert abs(float(row["Balance_Sheet_Error"]))<2e-5
  found=next(z for z in values if z["Scenario"]==case)
  pv=sum(float(r["Discounted_FCFF_From_Sep11"]) for r in group)
  near(found["PV_After_Date_FCFF"],pv,case+" discounted operating cash")
  near(found["Enterprise_Value"],pv+float(found["PV_Terminal_Value"]),case+" EV")
  bridge=(float(found["Excess_Cash_Model_Proxy"])+
          float(found["Available_Treasury_And_Deposits"])-
          float(found["Sep_11_Modeled_Debt"])-
          float(found["NCI_June_2026_Latest_Published"]))
  near(found["Modeled_Bridge"],bridge,case+" bridge")
  near(found["Conditional_Equity_Value"],
       float(found["Enterprise_Value"])+bridge,case+" equity")
  near(found["Conditional_Per_Share_Sep10_Denom"],
       float(found["Conditional_Equity_Value"])/
       float(found["Sep10_Indicative_Share_Denominator_M"]),case+" share price")
  assert "SEPT_BALANCES_ESTIMATED" in found["Limitation"]
  assert float(found["Sep10_Indicative_Share_Denominator_M"])>7402
  a=next(z for z in actual if z["Scenario"]==case)
  near(a["June_Assets"],643101.789,case+" issued June BS")
  near(float(a["June_Liabilities"])+float(a["June_Equity"]),
       a["June_Assets"],case+" actual June accounting")
  near(float(a["Date_September_11_Assets_Modeled"]),
       float(a["Date_September_11_Liabilities_Modeled"])+
       float(a["Date_September_11_Equity_Modeled"]),case+" Sept forecast")
 print("PASS 15 aggregate integrated balance sheets, 15 operating-CF reconciliations, "
       "3 June issuer balance sheets, 3 modeled September balance sheets, "
       "3 normalized terminal valuations and sourced share-population sensitivities.")

if __name__=="__main__":main()
