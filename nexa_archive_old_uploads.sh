#!/usr/bin/env bash
# Archive legacy Nexa ZIP uploads without altering the active GitHub Actions source.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
if [[ "$(git branch --show-current)" != 'main' ]]; then
  echo 'Switch to the main branch before running this script.' >&2
  exit 1
fi
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo 'Tracked working tree has changes. Commit or stash changes before running.' >&2
  exit 1
fi
if [[ ! -f Nexa_Latest_GitHub_Ready.zip ]]; then
  echo 'Active ZIP missing; stopping without changing anything.' >&2
  exit 1
fi
active_before=$(git hash-object Nexa_Latest_GitHub_Ready.zip)
count=0
for path in Nexa_*.zip; do
  [[ -f "$path" ]] || continue
  [[ "$path" == Nexa_Latest_GitHub_Ready.zip ]] && continue
  name="${path%.zip}"
  dest="archive/nexa-uploads/${name}/Nexa_Latest_GitHub_Ready.zip"
  if [[ -e "$dest" ]]; then
    echo "Archive destination exists: $dest; stopping." >&2
    exit 1
  fi
  mkdir -p "$(dirname "$dest")"
  git mv -- "$path" "$dest"
  count=$((count+1))
done
active_after=$(git hash-object Nexa_Latest_GitHub_Ready.zip)
if [[ "$active_before" != "$active_after" ]]; then
  echo 'Active ZIP unexpectedly changed: aborting commit.' >&2
  exit 1
fi
if [[ "$count" -eq 0 ]]; then
  echo 'No legacy root ZIP files to archive.'
  exit 0
fi
cat > archive/nexa-uploads/README.md <<'DOC'
# Nexa legacy ZIP uploads

Each folder contains one historical uploaded ZIP renamed to the standard filename
`Nexa_Latest_GitHub_Ready.zip`. Folder names preserve the original uploaded names.
These are archives, **not** active GitHub Actions build inputs.

The active build source is `/Nexa_Latest_GitHub_Ready.zip` at repository root.
Archive ZIPs should never be uploaded in sequence expecting their contents to merge.
Only explicitly replacing that root file changes the build source.
DOC
git add -- archive/nexa-uploads/README.md
printf 'Archived %d legacy ZIPs; active ZIP Git blob remained %s\n' "$count" "$active_after"
git status --short
git commit -m "Archive legacy Nexa ZIPs under stable names; preserve active build ZIP"
echo 'Commit made locally. Review the commit, then run: git push origin main'
