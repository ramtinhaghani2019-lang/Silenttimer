#!/usr/bin/env python3
"""Fast source-level regression checks; run after patch_assets_pin_guard.py."""
from pathlib import Path

source = Path("app/src/main/java/com/example/silenttimer/AssetsActivity.java").read_text(encoding="utf-8")
checks = {
    "single activity-result handler": source.count("void onActivityResult(") == 1,
    "entry PIN gate": "if(NexaStore.lockEnabled(this) && !SecurityGate.isUnlocked())" in source.split("void onCreate(", 1)[1].split("void onActivityResult(", 1)[0],
    "resume PIN gate": "if(NexaStore.lockEnabled(this) && !SecurityGate.isUnlocked())" in source.split("void onResume(", 1)[1].split("void onPause(", 1)[0],
    "unlock result requires valid session": "resultCode==RESULT_OK && SecurityGate.isUnlocked()" in source,
    "receiver cleanup is guarded": "if(marketReceiverRegistered){" in source,
    "UI build is gated": source.index("if(NexaStore.lockEnabled(this) && !SecurityGate.isUnlocked())") < source.index("        build();"),
    "image result is gated": "if(NexaStore.lockEnabled(this) && !SecurityGate.isUnlocked())return;" in source.split("void onActivityResult(", 1)[1],
}
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL") + ": " + name)
if not all(checks.values()):
    raise SystemExit(1)
