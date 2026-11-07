# Nexa legacy ZIP uploads

Each folder contains one historical uploaded ZIP renamed to the standard filename
`Nexa_Latest_GitHub_Ready.zip`. Folder names preserve the original uploaded names.
These are archives, **not** active GitHub Actions build inputs.

The active build source is `/Nexa_Latest_GitHub_Ready.zip` at repository root.
Archive ZIPs should never be uploaded in sequence expecting their contents to merge.
Only explicitly replacing that root file changes the build source.
