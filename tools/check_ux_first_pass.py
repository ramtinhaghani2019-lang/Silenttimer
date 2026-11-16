"""Regression assertions for the first-pass UX patch."""
from pathlib import Path
root=Path("app/src/main/java/com/example/silenttimer")
quick=(root/"QuickAddActivity.java").read_text(encoding="utf-8")
today=(root/"TodayActivity.java").read_text(encoding="utf-8")
assert "مسیرهای پرکاربرد، بدون عبور از منوهای اضافه" not in quick
assert 'open(ModulesActivity.class,null)' in quick
assert 'open(SearchActivity.class,null)' in quick
assert 'open(TimelineActivity.class,null)' in quick
assert 'setTitle("پاک کردن یادداشت؟")' in today
assert '.setNegativeButton("انصراف",null)' in today
assert 'NexaStore.setUnlockNote(this,"");noteDraft="";note.setText("");' in today
assert 'setPositiveButton("پاک کردن"' in today
print("PASS: 8 UX regression assertions")
