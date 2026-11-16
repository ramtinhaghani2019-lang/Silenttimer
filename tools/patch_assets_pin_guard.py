from pathlib import Path
p=Path('app/src/main/java/com/example/silenttimer/AssetsActivity.java')
s=p.read_text(encoding='utf-8')
def replace_once(old,new):
    global s
    count=s.count(old)
    if count!=1:
        raise SystemExit(f'Unexpected AssetsActivity source: expected one match, found {count}: {old[:90]}')
    s=s.replace(old,new,1)

replace_once('    private boolean assetsInitialized=false;', '''    private boolean assetsInitialized=false;
    private static final int REQUEST_ASSETS_UNLOCK=8138;
    private boolean awaitingAssetsUnlock=false;
    private boolean assetsUiReady=false;
    private boolean marketReceiverRegistered=false;
    private void requestAssetsUnlock(){
        if(awaitingAssetsUnlock || isFinishing())return;
        awaitingAssetsUnlock=true;
        startActivityForResult(new Intent(this,UnlockActivity.class),REQUEST_ASSETS_UNLOCK);
    }''')

replace_once('    @Override protected void onCreate(Bundle b){super.onCreate(b);UiKit.applyWindow(this);', '''    @Override protected void onCreate(Bundle b){super.onCreate(b);UiKit.applyWindow(this);
        // Enforce the same app lock on direct and exported ACTION_SEND entry points.
        if(NexaStore.lockEnabled(this) && !SecurityGate.isUnlocked()){
            getWindow().getDecorView().setVisibility(View.INVISIBLE);
            requestAssetsUnlock();
            return;
        }''')
replace_once('list.postDelayed(()->editForm(null),250);', '''list.postDelayed(()->{
                if(isFinishing() || isDestroyed())return;
                if(NexaStore.lockEnabled(this) && !SecurityGate.isUnlocked())return;
                editForm(null);
            },250);''')
replace_once('if(shared!=null)list.post(()->readReceiptFromImage(shared));', '''if(shared!=null)list.post(()->{
                if(isFinishing() || isDestroyed())return;
                if(NexaStore.lockEnabled(this) && !SecurityGate.isUnlocked())return;
                readReceiptFromImage(shared);
            });''')

replace_once('        build();\n        if(restoredPage!=null){', '        build();\n        assetsUiReady=true;\n        if(restoredPage!=null){')
replace_once('''        super.onActivityResult(request,resultCode,data);
        if(request==REQUEST_RECEIPT_IMAGE''', '''        super.onActivityResult(request,resultCode,data);
        if(request==REQUEST_ASSETS_UNLOCK){
            awaitingAssetsUnlock=false;
            if(resultCode==RESULT_OK && SecurityGate.isUnlocked())recreate();
            else finish();
            return;
        }
        if(NexaStore.lockEnabled(this) && !SecurityGate.isUnlocked())return;
        if(request==REQUEST_RECEIPT_IMAGE''')
replace_once('''    @Override protected void onResume(){
        super.onResume();
        android.content.IntentFilter filter''', '''    @Override protected void onResume(){
        super.onResume();
        if(NexaStore.lockEnabled(this) && !SecurityGate.isUnlocked()){
            getWindow().getDecorView().setVisibility(View.INVISIBLE);
            requestAssetsUnlock();
            return;
        }
        if(!assetsUiReady)return;
        getWindow().getDecorView().setVisibility(View.VISIBLE);
        android.content.IntentFilter filter''')
replace_once('''        else registerReceiver(marketUiReceiver,filter);
        if(list!=null){''', '''        else registerReceiver(marketUiReceiver,filter);
        marketReceiverRegistered=true;
        if(list!=null){''')
replace_once('    @Override protected void onPause(){unregisterReceiver(marketUiReceiver);super.onPause();}', '''    @Override protected void onPause(){
        if(marketReceiverRegistered){
            unregisterReceiver(marketUiReceiver);
            marketReceiverRegistered=false;
        }
        super.onPause();
    }''')
p.write_text(s,encoding='utf-8')
print('PASS: AssetsActivity PIN guard patch applied')
