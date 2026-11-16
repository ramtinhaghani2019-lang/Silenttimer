"""Regression assertions for the first-pass UX patch."""
from pathlib import Path
root=Path("app/src/main/java/com/example/silenttimer")
quick=(root/"QuickAddActivity.java").read_text(encoding="utf-8")
today=(root/"TodayActivity.java").read_text(encoding="utf-8")
alerts=(root/"AlertEditor.java").read_text(encoding="utf-8")
assert "مسیرهای پرکاربرد، بدون عبور از منوهای اضافه" not in quick
assert 'open(ModulesActivity.class,null)' in quick
assert 'open(SearchActivity.class,null)' in quick
assert 'open(TimelineActivity.class,null)' in quick
assert 'setTitle("پاک کردن یادداشت؟")' in today
assert '.setNegativeButton("انصراف",null)' in today
assert 'NexaStore.setUnlockNote(this,"");noteDraft="";note.setText("");' in today
assert 'setPositiveButton("پاک کردن"' in today
assert 'setTitle("پاک کردن مسیرهای اخیر؟")' in quick
assert 'اطلاعات شما باقی می‌ماند.' in quick
assert 'getSharedPreferences(RECENT_PREFS,MODE_PRIVATE).edit().remove(RECENT_KEY).apply();' in quick
assert quick.count('.setNegativeButton("انصراف",null)') == 1
assert 'setTitle("حذف این هشدار؟")' in alerts
assert 'setNegativeButton("انصراف",null)' in alerts
assert 'setPositiveButton("حذف",(dialog,which)->{data.remove(r);renderRows();})' in alerts
patch = Path(__file__).with_name("patch_ux_first_pass.py").read_text(encoding="utf-8")
assert "pending[p] = src.replace(before, after, 1)" in patch
assert "for path, content in pending.items():" in patch
assert patch.index("for path, content in pending.items():") > patch.index('once("QuickAddActivity.java",', patch.index('once("TodayActivity.java",'))
print("PASS: 18 UX regression assertions")
