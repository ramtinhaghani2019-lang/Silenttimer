"""Small, deterministic UX fixes on extracted Nexa Android sources."""
from pathlib import Path

root = Path("app/src/main/java/com/example/silenttimer")
pending = {}

def once(path, before, after):
    """Stage exact source edits; do not write until all matches are verified."""
    p = root / path
    src = pending.get(p)
    if src is None:
        src = p.read_text(encoding="utf-8")
    matches = src.count(before)
    if matches != 1:
        raise SystemExit(f"Expected one exact match in {path}, found {matches}")
    pending[p] = src.replace(before, after, 1)

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
# Clearing recent shortcuts should be reversible by cancelling; actual saved data is untouched.
once("QuickAddActivity.java",
    '''clear.setOnClickListener(v->{
            getSharedPreferences(RECENT_PREFS,MODE_PRIVATE).edit().remove(RECENT_KEY).apply();
            build();
        });''',
    '''clear.setOnClickListener(v->new android.app.AlertDialog.Builder(this)
            .setTitle("پاک کردن مسیرهای اخیر؟")
            .setMessage("فقط فهرست دسترسی‌های اخیر پاک می‌شود؛ اطلاعات شما باقی می‌ماند.")
            .setNegativeButton("انصراف",null)
            .setPositiveButton("پاک کردن",(dialog,which)->{
                getSharedPreferences(RECENT_PREFS,MODE_PRIVATE).edit().remove(RECENT_KEY).apply();
                build();
            }).show());''')

# Alert rules are shared across several editors; confirm removal to prevent mis-taps.
once("AlertEditor.java",
    'Button del=UiKit.deleteIconButton(c);del.setOnClickListener(v->{data.remove(r);renderRows();});line.addView(del,new LinearLayout.LayoutParams(UiKit.dp(c,48),UiKit.dp(c,48)));',
    '''Button del=UiKit.deleteIconButton(c);del.setOnClickListener(v->new AlertDialog.Builder(c)
                .setTitle("حذف این هشدار؟")
                .setMessage(label(r))
                .setNegativeButton("انصراف",null)
                .setPositiveButton("حذف",(dialog,which)->{data.remove(r);renderRows();})
                .show());line.addView(del,new LinearLayout.LayoutParams(UiKit.dp(c,48),UiKit.dp(c,48)));''')

# Commit only after every expected source fragment has been validated.
for path, content in pending.items():
    path.write_text(content, encoding="utf-8")
print(f"PASS: UX patch applied to {len(pending)} source files")
