"""Small, deterministic UX fixes on extracted Nexa Android sources."""
from pathlib import Path

root = Path("app/src/main/java/com/example/silenttimer")

def once(path, before, after):
    p = root / path
    src = p.read_text(encoding="utf-8")
    if src.count(before) != 1:
        raise SystemExit(f"Expected one exact match in {path}, found {src.count(before)}")
    p.write_text(src.replace(before, after, 1), encoding="utf-8")

# Remove nonessential instructional copy; keep all routes and controls.
once("QuickAddActivity.java",
    'root.addView(UiKit.muted(this,"مسیرهای پرکاربرد، بدون عبور از منوهای اضافه"),UiKit.matchWrap(this,0,12));',
    '// Primary routes are self-explanatory; no introductory instruction needed.')

# Destructive action must not silently erase the user's saved note.
once("TodayActivity.java",
    'clear.setOnClickListener(v->{NexaStore.setUnlockNote(this,"");noteDraft="";note.setText("");});',
    '''clear.setOnClickListener(v->{
            if(note.getText().toString().trim().isEmpty() && NexaStore.unlockNote(this).isEmpty())return;
            new android.app.AlertDialog.Builder(this)
                .setTitle("پاک کردن یادداشت؟")
                .setMessage("این یادداشت حذف می‌شود.")
                .setNegativeButton("انصراف",null)
                .setPositiveButton("پاک کردن",(dialog,which)->{
                    NexaStore.setUnlockNote(this,"");noteDraft="";note.setText("");
                    android.widget.Toast.makeText(this,"یادداشت پاک شد.",android.widget.Toast.LENGTH_SHORT).show();
                }).show();
        });''')
print("PASS: UX patch applied")
