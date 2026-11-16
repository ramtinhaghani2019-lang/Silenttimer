from pathlib import Path
p=Path('app/src/main/java/com/example/silenttimer/AssetsActivity.java')
s=p.read_text(encoding='utf-8')
def replace_once(old,new):
 global s
 if s.count(old)!=1: raise SystemExit(f'Unexpected AssetsActivity source: expected one match, found {s.count(old)}: {old[:90]}')
 s=s.replace(old,new,1)
replace_once('    private boolean assetsInitialized=false;', '''    private boolean assetsInitialized=false;
    private static final int REQUEST_ASSETS_UNLOCK=8138;
    private boolean awaitingAssetsUnlock=false;
    private boolean assetsUiReady=false;
    private void requestAssetsUnlock(){
        if(awaitingAssetsUnlock || isFinishing())return;
        awaitingAssetsUnlock=true;
        startActivityForResult(new Intent(this,UnlockActivity.class),REQUEST_ASSETS_UNLOCK);
    }
    @Override protected void onActivityResult(int request,int result,Intent data){
        super.onActivityResult(request,result,data);
        if(request==REQUEST_ASSETS_UNLOCK){
            awaitingAssetsUnlock=false;
            if(result==RESULT_OK && SecurityGate.isUnlocked()){
                if(!assetsUiReady)recreate();
                else getWindow().getDecorView().setVisibility(View.VISIBLE);
            }else finish();
        }
    }''')
replace_once('    @Override protected void onCreate(Bundle b){super.onCreate(b);UiKit.applyWindow(this);', '''    @Override protected void onCreate(Bundle b){super.onCreate(b);UiKit.applyWindow(this);
        // Guard all entry points (including exported ACTION_SEND) before reading portfolio data.
        if(NexaStore.lockEnabled(this) && !SecurityGate.isUnlocked()){
            getWindow().getDecorView().setVisibility(View.INVISIBLE);
            requestAssetsUnlock();
            return;
        }''')
replace_once('        build();\n        if(restoredPage!=null){', '        build();\n        assetsUiReady=true;\n        if(restoredPage!=null){')
replace_once('    @Override protected void onResume(){\n        super.onResume();', '''    @Override protected void onResume(){
        super.onResume();
        if(NexaStore.lockEnabled(this) && !SecurityGate.isUnlocked()){
            getWindow().getDecorView().setVisibility(View.INVISIBLE);
            requestAssetsUnlock();
            return;
        }
        if(!assetsUiReady)return;
        getWindow().getDecorView().setVisibility(View.VISIBLE);''')
replace_once('    @Override protected void onPause(){unregisterReceiver(marketUiReceiver);super.onPause();}', '''    @Override protected void onPause(){
        if(assetsUiReady)unregisterReceiver(marketUiReceiver);
        super.onPause();
    }''')
p.write_text(s,encoding='utf-8')
print('PASS: AssetsActivity entry and resume PIN guards patched')
