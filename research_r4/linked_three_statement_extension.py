"""R4.1: source-anchored, simplified three-statement operating scenario extension.

Separate from accepted R3 and original R4 alternative. June 2026 actual consolidated
totals anchor all schedules; forecasted line items and September balances are
MODEL ESTIMATES, not subsequently filed facts. RMB millions throughout.
"""
from __future__ import annotations
import csv,json,math
from datetime import date
from pathlib import Path
from rebuild_exploratory_revision import INTERIM,scenarios,shares,SEPT10_INDICATIVE_TOTAL_OUTSTANDING_M

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
JUNE=date(2026,6,30); VALUE=date(2026,9,11); YEAR_END=date(2026,12,31)
FRACTION_TO_VAL=(VALUE-JUNE).days/(YEAR_END-JUNE).days
FRACTION_AFTER_VAL=(YEAR_END-VALUE).days/(YEAR_END-JUNE).days
# June financials taken from issuer's 2026-08-28/29 interim CAS reporting.
H1={
"assets":643101.789,"liabilities":417308.848,"equity":225792.941,
"cash_equivalents":74614.244,"gross_borrowings":80327.263,
"ppe":44320.997,
"term_deposits":8496.066,"treasury_products":158310.938,
"loans_advances_current":14480.660,"loans_advances_long":448.686,
"finance_asset_current_portion":158530.134-158310.938,
"customer_deposits":101.708,
"revenue":INTERIM["revenue_2026_H1"],
"operating_profit":31684.489,"investment_income":3040.102,
"fair_value_gains":4997.108,"finance_result":-3273.004,
"da":5002.775,"capex_cash":2634.210,
"cfo":37552.090,"net_profit":26582.874
}
# Historical 2025 R3 note splits used ONLY to allocate aggregate June 2026
# other current-asset/liability and payable-tax accounts; estimated, not fact.
R3_SPLIT={
"other_operating_assets_fraction":20747.946/25376.475,
"other_operating_liabilities_fraction":92515.939/92537.419,
"other_tax_fraction":2678.872/7164.093
}
JUNE_WC={
 "receivables":61954.826,"notes_receivable":6234.318,
 "receivables_financing":7659.731,"inventory":55440.969,
 "contract_assets":6124.720,"prepayments":4120.736,
 "other_receivables":3172.621,"other_current_assets":20802.405,
 "accounts_payable":109516.782,"contract_liabilities":45458.117,
 "notes_payable":47519.044,"employee_comp":6450.966,
 "other_payables":6340.917,"other_current_liabilities":104511.504,
 "taxes_payable":7942.735
}
NWC_ASSETS=sum(JUNE_WC[k] for k in (
 "receivables","notes_receivable","receivables_financing","inventory",
 "contract_assets","prepayments","other_receivables"))+JUNE_WC["other_current_assets"]*R3_SPLIT["other_operating_assets_fraction"]
NWC_LIABS=sum(JUNE_WC[k] for k in (
 "accounts_payable","contract_liabilities","notes_payable","employee_comp",
 "other_payables"))+JUNE_WC["other_current_liabilities"]*R3_SPLIT["other_operating_liabilities_fraction"]+JUNE_WC["taxes_payable"]*R3_SPLIT["other_tax_fraction"]
FIN_LOANS=(H1["loans_advances_current"]+H1["loans_advances_long"]
          +H1["finance_asset_current_portion"])
H1_TREASURY=H1["term_deposits"]+H1["treasury_products"]
OTHER_ASSETS=H1["assets"]-(H1["cash_equivalents"]+H1["ppe"]+NWC_ASSETS+FIN_LOANS+H1_TREASURY)
OTHER_LIABS=H1["liabilities"]-(H1["gross_borrowings"]+NWC_LIABS+H1["customer_deposits"])
H1_EBIT=H1["operating_profit"]-H1["investment_income"]-H1["fair_value_gains"]-H1["finance_result"]
assert abs(H1["assets"]-H1["liabilities"]-H1["equity"])<1e-5
assert OTHER_ASSETS>0 and OTHER_LIABS>0 and FIN_LOANS>H1["customer_deposits"]
assert 0 < FRACTION_AFTER_VAL < 1

DIVIDEND_RATIO=.25
INTEREST_RATE=.02
TAX_RATE=.152566
# Apart from explicit estimated ratios, published H1 financial accounts are
# fixed anchors. All other net assets/liabilities are held constant.
def save(name,rows):
 assert rows
 cols=list(rows[0])
 with (OUT/name).open("w",encoding="utf8",newline="") as f:
  w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
  w.writeheader()
  w.writerows(rows)

def round_row(row):
 return {k:round(v,9) if isinstance(v,float) else v for k,v in row.items()}

def main():
 orig={(r["Scenario"],int(r["Year"]),r["Metric_ID"]):float(r["Value"])
       for r in csv.DictReader((ROOT/"model/H3B_MODEL_LONG.csv").open(encoding="utf8"))}
 r4={(r["Scenario"],int(r["Year"])):r
     for r in csv.DictReader((OUT/"linked_operating_fcff_scenarios.csv").open(encoding="utf8"))}
 date_values=[]
 rolls=[]
 audit=[]
 for case,par in scenarios.items():
  state={"cash":H1["cash_equivalents"],"debt":H1["gross_borrowings"],
         "ppe":H1["ppe"],"wc_assets":NWC_ASSETS,"wc_liabs":NWC_LIABS,
         "fs_loans":FIN_LOANS,"treasury":H1_TREASURY,
         "customer_deposits":H1["customer_deposits"],"other_assets":OTHER_ASSETS,
         "other_liabs":OTHER_LIABS,"equity":H1["equity"]}
  def bs(st):
   assets=(st["cash"]+st["ppe"]+st["wc_assets"]+st["fs_loans"]+
           st["treasury"]+st["other_assets"])
   liabilities=(st["debt"]+st["wc_liabs"]+st["customer_deposits"]+st["other_liabs"])
   return assets,liabilities,st["equity"],assets-liabilities-st["equity"]
  assert abs(bs(state)[-1])<1e-6
  valuations=[]
  sep_state=None
  for year in range(2026,2031):
   row=r4[(case,year)]
   revenue=float(row["Revenue"])
   # 2026 H2 modeled EBIT = full-year operating forecast minus actual H1
   # recurring EBIT. Future full years use the R4 annual operating forecast.
   ebit=float(row["EBIT"])-(H1_EBIT if year==2026 else 0)
   da=float(row["DA"])-(H1["da"] if year==2026 else 0)
   capex=float(row["CAPEX"])-(H1["capex_cash"] if year==2026 else 0)
   if da < 0 or capex < 0: raise ValueError("Forecast less than recorded H1 amounts")
   # An explicit forecast operating working-capital asset intensity equals
   # the June ratio against annualized June sales; liability is implied by the
   # scenario NWC target. Neither is misrepresented as independently filed.
   wc_assets=revenue*(NWC_ASSETS/(2*H1["revenue"]))
   target_nwc=float(row["Operating_NWC"])
   wc_liabs=wc_assets-target_nwc
   fs_net=float(row["Finance_Services_Net_Investment"])
   fs_loans=fs_net+state["customer_deposits"]
   delta_wc=(wc_assets-wc_liabs)-(state["wc_assets"]-state["wc_liabs"])
   delta_fin=fs_loans-state["fs_loans"]
   interest=state["debt"]*INTEREST_RATE*(.5 if year==2026 else 1.0)
   tax=max(0,ebit-interest)*TAX_RATE
   net_income=ebit-interest-tax
   dividends=max(0,net_income)*DIVIDEND_RATIO
   cfo=net_income+da-delta_wc-delta_fin
   cfi=-capex
   pretax_unlevered=ebit
   unlevered_fcff=pretax_unlevered*(1-TAX_RATE)+da-capex-delta_wc-delta_fin
   # Pro-forma borrowing increases only to fund any cash deficit against
   # a stated minimum liquidity target; it is not evidence of credit access.
   cash_pre=state["cash"]+cfo+cfi-dividends
   reserve=revenue*.08285274
   new_debt=max(0.0,reserve-cash_pre)
   financing=new_debt-dividends
   cash_end=state["cash"]+cfo+cfi+financing
   new=state.copy()
   new.update({"cash":cash_end,"debt":state["debt"]+new_debt,
      "ppe":state["ppe"]+capex-da,"wc_assets":wc_assets,
      "wc_liabs":wc_liabs,"fs_loans":fs_loans,
      "equity":state["equity"]+net_income-dividends})
   A,L,E,error=bs(new)
   if abs(error)>1e-6:raise AssertionError((case,year,error))
   if cash_end<0 or new["ppe"]<0: raise AssertionError("Nonphysical financial stocks")
   # A linear interpolation of modeled June->Dec account balances estimates
   # September stocks; these are NOT issuer-reported September balance sheets.
   if year==2026:
    sep_state={k:state[k]+(new[k]-state[k])*FRACTION_TO_VAL
               for k in state}
    assert abs(bs(sep_state)[-1])<1e-6
    sep_assets,sep_liabs,sep_equity,_=bs(sep_state)
    sep_debt=sep_state["debt"]
    sep_cash=sep_state["cash"]
    # 2026 H2 cash flow is forecast starting June 30; only the
    # remaining 111/184 share is discounted after Sep 11.
    val_cash=unlevered_fcff*FRACTION_AFTER_VAL
    term=FRACTION_AFTER_VAL
   else:
    val_cash=unlevered_fcff
    term=FRACTION_AFTER_VAL+(year-2026)
   pv=val_cash/(1+par["wacc"])**term
   valuations.append(pv)
   vals={
     "Scenario":case,"Period":"2026_H2" if year==2026 else str(year),
     "Revenue_Annual_Basis":revenue,"Operating_EBIT_This_Period":ebit,
     "Debt_Interest":interest,"Income_Tax":tax,"Net_Income":net_income,
     "Depreciation_Amortization":da,"Capital_Expenditure":capex,
     "Delta_Operating_NWC":delta_wc,"Delta_Finance_Loans_Net":delta_fin,
     "CFO":cfo,"CFI":cfi,"Dividends":dividends,
     "New_Borrowing_Financing_Plug":new_debt,
     "CFF":financing,"Net_Change_Cash":cash_end-state["cash"],
     "Cash_End":cash_end,"PPE_End":new["ppe"],
     "Operating_NWC_Assets_End":wc_assets,
     "Operating_NWC_Liabilities_End":wc_liabs,
     "Finance_Loans_Assets_End":fs_loans,
     "Financial_Asset_Treasury_End":new["treasury"],
     "Other_Assets_End":new["other_assets"],"Total_Assets":A,
     "Debt_End":new["debt"],"Finance_Customer_Deposits_End":new["customer_deposits"],
     "Other_Liabilities_End":new["other_liabs"],"Total_Liabilities":L,
     "Total_Equity":E,"Balance_Sheet_Error":error,
     "Unlevered_FCFF":unlevered_fcff,
     "R4_Original_FCFF_Same_Year":float(row["FCFF"]),
     "Discounted_FCFF_From_Sep11":pv,
     "Remainder_Of_2026_FCFF_Fraction":FRACTION_AFTER_VAL if year==2026 else 1,
     "Assumption_Status":"CONDITIONAL_AGGREGATED_3STATEMENT_NOT_COMPANY_GUIDANCE"
   }
   rolls.append(round_row(vals))
   state=new
  # Terminal uses a new steady-state 2031 FCFF after 2030, as in R4.
  rev31=float(r4[(case,2030)]["Revenue"])*(1+par["g"])
  ebit31=rev31*par["margins"][-1]
  wc31=rev31*par["nwc_ratio"];fin31=rev31*par["fs_ratio"]
  wc30=float(r4[(case,2030)]["Operating_NWC"])
  fin30=float(r4[(case,2030)]["Finance_Services_Net_Investment"])
  fcff31=(ebit31*(1-TAX_RATE)+rev31*(par["da"]-par["capex"])-
          (wc31-wc30)-(fin31-fin30))
  pvterminal=fcff31/(par["wacc"]-par["g"])/(1+par["wacc"])**(FRACTION_AFTER_VAL+4)
  ev=sum(valuations)+pvterminal
  # Approximate Sep 11 financial asset/debt bridge with a modeled cash
  # trajectory, rather than passing off June accounting balances as Sep 11.
  # Treasury and term deposits remain held at their June values.
  september_reserve=float(r4[(case,2026)]["Revenue"])*.08285274
  excess_cash=max(0.0,sep_cash-september_reserve)
  available_treasury=H1_TREASURY*par["liquid"]
  nci=INTERIM["nci_2026_06"] # latest published, NOT September actual
  bridge=excess_cash+available_treasury-sep_debt-nci
  equity=ev+bridge
  date_values.append(round_row({
    "Scenario":case,"Date":"2026-09-11","Period_Basis":"June_2026_Financial_Actuals_Projected_To_Sept11",
    "PV_After_Date_FCFF":sum(valuations),
    "Normalized_2031_FCFF":fcff31,"PV_Terminal_Value":pvterminal,
    "Enterprise_Value":ev,"Sep_11_Modeled_Cash":sep_cash,
    "Sep_11_Modeled_Debt":sep_debt,"June_Treasury_And_Deposits":H1_TREASURY,
    "Available_Fraction_Assumed":par["liquid"],
    "Available_Treasury_And_Deposits":available_treasury,
    "Cash_Reserve_Proxy":september_reserve,"Excess_Cash_Model_Proxy":excess_cash,
    "NCI_June_2026_Latest_Published":nci,
    "Modeled_Bridge":bridge,"Conditional_Equity_Value":equity,
    "Original_R3_Share_Denominator_M":shares,
    "Sep10_Indicative_Share_Denominator_M":SEPT10_INDICATIVE_TOTAL_OUTSTANDING_M,
    "Conditional_Per_Share_Sep10_Denom":equity/SEPT10_INDICATIVE_TOTAL_OUTSTANDING_M,
    "Limitation":"SEPT_BALANCES_ESTIMATED;INTERIM_NWC_SPLITS_ESTIMATED;FINANCING_PUG_NOT_CONFIRMED"
  }))
  audit.append(round_row({"Scenario":case,"June_Assets":H1["assets"],
    "June_Liabilities":H1["liabilities"],"June_Equity":H1["equity"],
    "Estimated_June_Operating_NWC":NWC_ASSETS-NWC_LIABS,
    "R3_2025_Operating_NWC":-131003.796,
    "Date_September_11_Assets_Modeled":sep_assets,
    "Date_September_11_Liabilities_Modeled":sep_liabs,
    "Date_September_11_Equity_Modeled":sep_equity,
    "Sep_BS_Difference":sep_assets-sep_liabs-sep_equity}))
 save("linked_three_statements_proforma.csv",rolls)
 save("dated_three_statement_valuation.csv",date_values)
 save("interim_nwc_and_share_reconciliation.csv",audit)
 print("PASS: 3 source-anchored June BS; 15 forecast BS identities; "
       "15 cash-flow identities; 3 modeled September BS identities; "
       "3 separately dated, normalized FCFF valuations.")
 print(json.dumps({r["Scenario"]:r["Conditional_Per_Share_Sep10_Denom"]
                   for r in date_values},sort_keys=True))

if __name__=="__main__":
 main()
