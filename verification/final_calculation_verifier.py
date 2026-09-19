import sys
sys.dont_write_bytecode=True
import json
from verification_core import calculate
checks=calculate();failed=[x for x in checks if x["Result"]!="PASS"]
result={"Schema":"FINAL_CALCULATION_VERIFIER_R3_1","Status":"PASS" if not failed else "FAIL","Control_Count":len(checks),"Failure_Count":len(failed),"Failures":failed}
print(json.dumps(result,sort_keys=True,separators=(",",":")))
raise SystemExit(0 if not failed else 1)
