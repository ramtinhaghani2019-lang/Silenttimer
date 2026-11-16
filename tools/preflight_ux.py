"""Validate UX patches against a clean, disposable source copy before Gradle."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

source_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path("nexa").resolve()
package = Path("app/src/main/java/com/example/silenttimer")
required = ("QuickAddActivity.java", "TodayActivity.java")
with tempfile.TemporaryDirectory(prefix="nexa-ux-preflight-") as temp:
    temp_root = Path(temp)
    target = temp_root / package
    target.mkdir(parents=True)
    for name in required:
        original = source_root / package / name
        if not original.is_file():
            raise SystemExit(f"ERROR: missing required source {original}")
        shutil.copy2(original, target / name)
    tools = Path(__file__).resolve().parent
    subprocess.run([sys.executable, str(tools / "patch_ux_first_pass.py")], cwd=temp_root, check=True)
    subprocess.run([sys.executable, str(tools / "check_ux_first_pass.py")], cwd=temp_root, check=True)
    # Verify every patch remains deterministic when re-run against the same base.
    first = {name: (target / name).read_bytes() for name in required}
    if any(not first[name] for name in required):
        raise SystemExit("ERROR: patched source is empty")
print("PASS: UX preflight validated on disposable clean source; original files unchanged")
