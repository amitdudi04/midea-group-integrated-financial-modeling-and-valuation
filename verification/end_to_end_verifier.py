import sys
sys.dont_write_bytecode=True
import json,re,sqlite3,zipfile,subprocess
from pathlib import Path
from verification_core import ROOT,calculate,j,manifest_check,rows,sha
fails=manifest_check();authority=j("release/REPOSITORY_AUTHORITY_R3_1.json");manifest=ROOT/"release/REPOSITORY_MANIFEST_R3_1.json"
if sha(manifest)!=authority["Repository_Manifest_R3_1_SHA256"]:fails.append({"Control":"Authority_Manifest_Binding"})
bindings={"Public_Verifier_SHA256":"verification/final_calculation_verifier.py","End_To_End_Verifier_SHA256":"verification/end_to_end_verifier.py","Independent_Verifier_SHA256":"verification/independent_model_recalculator.py","Economic_NWC_Formula_SHA256":"workpapers/FINAL_OPERATING_NWC_FORMULA.json","Formula_Registry_SHA256":"model/H3B_FORMULA_REGISTRY.csv","Source_Registry_SHA256":"data/FINAL_SOURCE_REGISTRY_R3.csv","SQLite_SHA256":"model/MIDEA_GROUP_FINAL_MODEL_R3.sqlite","Excel_SHA256":"excel/MIDEA_GROUP_INSTITUTIONAL_MODEL_R3.xlsx","Report_SHA256":"reports/MIDEA_GROUP_FINAL_VALUATION_REPORT_R3.docx","Memo_SHA256":"reports/MIDEA_GROUP_INVESTMENT_MEMO_R3.pdf","H6_Authority_SHA256":"verification/inputs/authorities/H6_AUTHORITY_R3.json","H7_Authority_SHA256":"verification/inputs/authorities/H7_AUTHORITY_R3.json"}
for k,p in bindings.items():
    if authority.get(k)!=sha(ROOT/p):fails.append({"Control":"Authority_Binding","Field":k})
for r in rows("data/FINAL_SOURCE_REGISTRY_R3.csv"):
    if r["Archived_File_Path"]=="EXTERNAL_REFERENCE": continue
    p=ROOT/r["Archived_File_Path"]
    if not p.exists() or sha(p)!=r["Archived_File_SHA256"]:fails.append({"Control":"Source_Archive","Source_ID":r["Source_ID"]})
for p in ROOT.rglob("*"):
    if p.is_file() and (p.name=="__pycache__" or p.suffix.lower() in {".pyc",".pyo"}):fails.append({"Control":"Python_Cache","Path":p.relative_to(ROOT).as_posix()})
for p in [ROOT/"verification/verification_core.py",ROOT/"verification/final_calculation_verifier.py",ROOT/"verification/independent_model_recalculator.py"]:
    t=p.read_text(encoding="utf-8")
    if re.search(r"[A-Za-z]:[\\/]",t) or "../" in t or "..\\" in t:fails.append({"Control":"External_Path_Dependency","Path":p.name})
calc=[x for x in calculate() if x["Result"]!="PASS"]
if calc:fails.append({"Control":"Calculation_Verifier","Failures":calc})
ind=subprocess.run([sys.executable,"-B",str(ROOT/"verification/independent_model_recalculator.py")],cwd=ROOT,text=True,capture_output=True)
if ind.returncode:fails.append({"Control":"Independent_Model_Recalculation","Output":ind.stdout.strip(),"Error":ind.stderr.strip()})
db=sqlite3.connect(ROOT/"model/MIDEA_GROUP_FINAL_MODEL_R3.sqlite");db_h7=json.loads(db.execute("select json from authority where name='H7'").fetchone()[0]);db.close();h7=j("verification/inputs/authorities/H7_AUTHORITY_R3.json")
if db_h7!=h7:fails.append({"Control":"SQLite_H7_Mismatch"})
with zipfile.ZipFile(ROOT/"excel/MIDEA_GROUP_INSTITUTIONAL_MODEL_R3.xlsx") as z:
    formulas="".join(z.read(n).decode("utf-8",errors="ignore") for n in z.namelist() if n.startswith("xl/worksheets/sheet") and n.endswith(".xml"))
    workbook=z.read("xl/workbook.xml").decode("utf-8",errors="ignore")
    if any(x in formulas for x in ["#REF!","#DIV/0!","#VALUE!","#NAME?","#N/A"]):fails.append({"Control":"Excel_Formula_Error"})
    if formulas.count("<x:f")<20:fails.append({"Control":"Excel_Formula_Count"})
    if "externalLink" in " ".join(z.namelist()):fails.append({"Control":"Excel_External_Link"})
result={"Schema":"END_TO_END_VERIFIER_R3_1","Status":"PASS" if not fails else "FAIL","Failure_Count":len(fails),"External_Path_Dependencies":sum(x["Control"]=="External_Path_Dependency" for x in fails),"Failures":fails}
print(json.dumps(result,sort_keys=True,separators=(",",":")))
raise SystemExit(0 if not fails else 1)
