"""Update the public R3.1 repository manifest after an intentional file change.

This does not modify historical valuation models, external roots, sealed ZIPs,
original release attestations or the financial results. Use only for deliberate
repository releases and then run the entire verification suite.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "release/REPOSITORY_MANIFEST_R3_1.json"
AUTHORITY = ROOT / "release/REPOSITORY_AUTHORITY_R3_1.json"
EXCLUDED = {
    "release/REPOSITORY_MANIFEST_R3_1.json",
    "release/REPOSITORY_AUTHORITY_R3_1.json",
    "release/FINAL_GITHUB_PUBLICATION_RESULT_R3_1.json",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes())


def tracked_release_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix()
        if relative in EXCLUDED or ".git" in path.parts or ".pytest_cache" in path.parts:
            continue
        if "__pycache__" in path.parts or path.suffix.lower() in (".pyc", ".pyo"):
            continue
        yield relative, path


def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    authority = json.loads(AUTHORITY.read_text(encoding="utf-8"))
    manifest["Files"] = [
        {"Path": rel, "SHA256": file_sha(path), "Bytes": path.stat().st_size}
        for rel, path in tracked_release_files()
    ]
    manifest["Generated_UTC"] = datetime.now(timezone.utc).isoformat()
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Every changed academically authoritative document has a binding.
    authority["README_SHA256"] = file_sha(ROOT / "README.md")
    authority["Final_Results_And_Findings_SHA256"] = file_sha(ROOT / "docs/RESULTS.md")
    authority["Repository_Manifest_R3_1_SHA256"] = file_sha(MANIFEST)
    AUTHORITY.write_text(json.dumps(authority, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "Status": "MANIFEST_REBUILT",
        "Members": len(manifest["Files"]),
        "ManifestSHA256": authority["Repository_Manifest_R3_1_SHA256"],
        "ModelEconomics": "UNCHANGED"
    }, sort_keys=True))


if __name__ == "__main__":
    main()
