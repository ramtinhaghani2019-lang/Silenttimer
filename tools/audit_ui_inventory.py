"""Read-only inventory of Android UI surfaces; never modifies application code."""
from collections import Counter
from pathlib import Path
import json
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("nexa")
java = sorted(root.rglob("app/src/main/java/**/*.java"))
xml = sorted(root.rglob("app/src/main/res/layout/*.xml"))
if not java:
    raise SystemExit("ERROR: no Android Java sources found")
activities = []
for p in java:
    source = p.read_text(encoding="utf-8", errors="replace")
    if re.search(r"\bextends\s+(?:AppCompatActivity|Activity|ComponentActivity)\b", source):
        activities.append(str(p.relative_to(root)))

java_indicators = Counter()
java_review_candidates = []
for p in java:
    source = p.read_text(encoding="utf-8", errors="replace")
    indicators = {
        "click_listeners": source.count(".setOnClickListener("),
        "dialog_builders": source.count("AlertDialog.Builder("),
        "text_setters": source.count(".setText("),
        "hint_setters": source.count(".setHint("),
        "content_descriptions": source.count(".setContentDescription("),
    }
    java_indicators.update(indicators)
    if indicators["click_listeners"] or indicators["text_setters"]:
        java_review_candidates.append({"source": str(p.relative_to(root)), **indicators})

labels = Counter()
for p in xml:
    source = p.read_text(encoding="utf-8", errors="replace")
    labels["layout_files"] += 1
    labels["hardcoded_text_attributes"] += len(re.findall(r'android:(?:text|hint|contentDescription)="(?!@|\?)', source))
    labels["clickable_attributes"] += len(re.findall(r'android:clickable="true"', source))
    labels["content_description_attributes"] += len(re.findall(r'android:contentDescription=', source))
result = {
    "activity_count": len(activities),
    "activities": activities,
    "layout_count": len(xml),
    "java_indicators": dict(java_indicators),
    "java_review_candidates": sorted(java_review_candidates, key=lambda x: (-x["click_listeners"], x["source"])),
    "layout_indicators": dict(labels),
    "note": "Inventory only. Java and XML counts are review indicators, not confirmed defects."
}
Path("nexa-ux-inventory.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"UI inventory: {len(activities)} activities, {len(xml)} XML layouts")
print("Saved nexa-ux-inventory.json")
