from __future__ import annotations
import argparse,hashlib,json,os,subprocess,sys,tempfile,zipfile,zlib
from pathlib import Path
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fail(code,msg,detail=None):
    print(json.dumps({"Schema":"DETACHED_FINAL_RELEASE_VERIFIER_R3","Status":"REJECT","Code":msg,"Detail":detail},sort_keys=True,separators=(",",":")));raise SystemExit(code)
a=argparse.ArgumentParser();a.add_argument("zip");a.add_argument("root");a.add_argument("--optimized",action="store_true");x=a.parse_args();zp=Path(x.zip).resolve();rp=Path(x.root).resolve();r=json.loads(rp.read_text(encoding="utf-8"))
if sha(zp)!=r["R3_ZIP_SHA256"]:fail(20,"ZIP_SHA256_MISMATCH")
if zp.stat().st_size!=r["R3_ZIP_Bytes"]:fail(21,"ZIP_SIZE_MISMATCH")
if f"{zlib.crc32(zp.read_bytes())&0xffffffff:08x}"!=r["R3_CRC"]:fail(22,"ZIP_CRC_MISMATCH")
with zipfile.ZipFile(zp) as z:
    bad=z.testzip()
    if bad:fail(23,"ZIP_MEMBER_CRC_FAILURE",bad)
    if len(z.infolist())!=r["R3_ZIP_Member_Count"]:fail(24,"ZIP_MEMBER_COUNT_MISMATCH")
    names=set(z.namelist())
    for n in ["RELEASE_MANIFEST_R3.json","FINAL_VALUATION_AUTHORITY_R3.json","verifier/final_calculation_verifier.py","verifier/end_to_end_verifier.py","independent_verifier/independent_model_recalculator.py"]:
        if n not in names:fail(25,"REQUIRED_MEMBER_MISSING",n)
    if hashlib.sha256(z.read("RELEASE_MANIFEST_R3.json")).hexdigest()!=r["Release_Manifest_R3_SHA256"]:fail(26,"MANIFEST_ROOT_MISMATCH")
    if hashlib.sha256(z.read("FINAL_VALUATION_AUTHORITY_R3.json")).hexdigest()!=r["Final_Valuation_Authority_R3_SHA256"]:fail(27,"AUTHORITY_ROOT_MISMATCH")
    if hashlib.sha256(z.read("verifier/final_calculation_verifier.py")).hexdigest()!=r["Public_Verifier_SHA256"]:fail(28,"PUBLIC_VERIFIER_ROOT_MISMATCH")
    if hashlib.sha256(z.read("verifier/end_to_end_verifier.py")).hexdigest()!=r["End_To_End_Verifier_SHA256"]:fail(29,"E2E_VERIFIER_ROOT_MISMATCH")
    if hashlib.sha256(z.read("independent_verifier/independent_model_recalculator.py")).hexdigest()!=r["Independent_Verifier_SHA256"]:fail(30,"INDEPENDENT_VERIFIER_ROOT_MISMATCH")
post=json.dumps(r["Final_Post_Package_Result"],sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
if hashlib.sha256(post).hexdigest()!=r["Final_Post_Package_Result_SHA256"]:fail(31,"POST_PACKAGE_RESULT_ROOT_MISMATCH")
with tempfile.TemporaryDirectory(prefix="midea_r3_external_") as td:
    with zipfile.ZipFile(zp) as z:z.extractall(td)
    env=os.environ.copy();env["PYTHONDONTWRITEBYTECODE"]="1";env["NO_PROXY"]="*";env["no_proxy"]="*"
    exe=[sys.executable,"-B"]+(["-O"] if x.optimized else [])
    outputs=[]
    for rel in ["verifier/final_calculation_verifier.py","verifier/end_to_end_verifier.py"]:
        p=subprocess.run(exe+[str(Path(td)/rel)],cwd=td,env=env,text=True,capture_output=True)
        outputs.append({"Command":rel,"ReturnCode":p.returncode,"Stdout":p.stdout.strip(),"Stderr":p.stderr.strip()})
        if p.returncode:fail(32,"PACKAGE_LOCAL_VERIFIER_FAILURE",outputs)
print(json.dumps({"Schema":"DETACHED_FINAL_RELEASE_VERIFIER_R3","Status":"PASS","Code":"PASS","Optimized":x.optimized,"Package_Verifiers":outputs},sort_keys=True,separators=(",",":")))
