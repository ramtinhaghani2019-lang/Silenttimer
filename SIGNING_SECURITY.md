# Nexa signing security — 5.4.150 / Build 172

The original signing keystore and hardcoded credentials were present in public ZIPs. Treat that key as compromised. Removing them from the current tree does not remove Git history, clones, caches, or forks.

This commit preserves the app version and production applicationId. It removes the embedded key and passwords, and removes obsolete unsafe ZIPs from the current tree. Original archives remain in prior Git history; history has not been rewritten.

Configure these repository Actions secrets privately:
- NEXA_KEYSTORE_BASE64: Base64 encoding of the approved signing keystore
- NEXA_STORE_PASSWORD: keystore password
- NEXA_KEY_ALIAS: signing alias
- NEXA_KEY_PASSWORD: private key password

Never paste values into an issue, commit, workflow, log, or chat. The workflow restores the key under RUNNER_TEMP and removes it even on failure. It uploads only the APK.

An APK build fails without all four secrets, rather than silently changing the update signature. Regression uses -PnexaRegressionOnly=true, a disposable debug signature and the separate com.example.silenttimer.regression application ID. Never distribute that package as an update.

Before production distribution, decide the supported signing-key rotation/migration path for existing installations. Merely changing a password does not revoke a leaked private key. Do not uninstall the existing app to bypass a signature mismatch: that risks user data. No rotation or destructive history rewrite has been performed here.
