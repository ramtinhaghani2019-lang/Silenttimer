"""Self-test Java/XML UI inventory on a small synthetic Android project."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import subprocess
import sys

script = Path(__file__).with_name("audit_ui_inventory.py").resolve()
with TemporaryDirectory(prefix="nexa-inventory-test-") as tmp:
    root = Path(tmp) / "project"
    java = root / "app/src/main/java/example/DemoActivity.java"
    layout = root / "app/src/main/res/layout/demo.xml"
    java.parent.mkdir(parents=True)
    layout.parent.mkdir(parents=True)
    java.write_text('class DemoActivity extends Activity { void build(){button.setOnClickListener(v->{}); label.setText("سلام"); new AlertDialog.Builder(this); } }', encoding="utf-8")
    layout.write_text('<TextView android:text="نمونه" android:clickable="true" android:contentDescription="توضیح"/>', encoding="utf-8")
    subprocess.run([sys.executable, str(script), str(root)], cwd=tmp, check=True)
    report = json.loads((Path(tmp) / "nexa-ux-inventory.json").read_text(encoding="utf-8"))
    assert report["activity_count"] == 1, report
    assert report["layout_count"] == 1, report
    assert report["java_indicators"]["click_listeners"] == 1, report
    assert report["java_indicators"]["dialog_builders"] == 1, report
    assert report["java_indicators"]["text_setters"] == 1, report
    assert report["layout_indicators"]["hardcoded_text_attributes"] == 2, report
    assert report["layout_indicators"]["clickable_attributes"] == 1, report
    assert len(report["java_review_candidates"]) == 1, report
print("PASS: Java/XML inventory smoke test")
