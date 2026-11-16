"""Validate UX patches against a clean, disposable source copy before Gradle."""
from pathlib import Path
import shutil
import hashlib
import subprocess
import sys
import tempfile

source_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path("nexa").resolve()
package = Path("app/src/main/java/com/example/silenttimer")
required = ("QuickAddActivity.java", "TodayActivity.java", "AlertEditor.java")
with tempfile.TemporaryDirectory(prefix="nexa-ux-preflight-") as temp:
    temp_root = Path(temp)
    target = temp_root / package
    target.mkdir(parents=True)
    original_hashes = {}
    for name in required:
        original = source_root / package / name
        if not original.is_file():
            raise SystemExit(f"ERROR: missing required source {original}")
        original_hashes[name] = hashlib.sha256(original.read_bytes()).hexdigest()
        shutil.copy2(original, target / name)
    tools = Path(__file__).resolve().parent
    subprocess.run([sys.executable, str(tools / "patch_ux_first_pass.py")], cwd=temp_root, check=True)
    subprocess.run([sys.executable, str(tools / "check_ux_first_pass.py")], cwd=temp_root, check=True)
    # Confirm the patched copies are nonempty; source archive stays unchanged.
    first = {name: (target / name).read_bytes() for name in required}
    if any(not first[name] for name in required):
        raise SystemExit("ERROR: patched source is empty")
for name in required:
    original = source_root / package / name
    if hashlib.sha256(original.read_bytes()).hexdigest() != original_hashes[name]:
        raise SystemExit(f"ERROR: preflight changed original source: {name}")
print("PASS: UX preflight validated on disposable clean source; original files unchanged")
