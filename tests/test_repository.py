import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent

def test_public_calculation_verifier():
    p=subprocess.run([sys.executable,"-B","verification/final_calculation_verifier.py"],cwd=ROOT,text=True,capture_output=True)
    assert p.returncode==0, p.stdout+p.stderr
    assert json.loads(p.stdout)["Status"]=="PASS"

def test_independent_recalculator():
    p=subprocess.run([sys.executable,"-B","verification/independent_model_recalculator.py"],cwd=ROOT,text=True,capture_output=True)
    assert p.returncode==0, p.stdout+p.stderr
    assert json.loads(p.stdout)["Status"]=="PASS"
