"""Prune root files script

Usage:
  - Review the script, then run in project root (PowerShell):
      python .\scripts\prune_root.py

Behavior:
  - Creates/uses `archive/root_backup/` to store copies of deleted files.
  - Deletes only top-level FILES (not directories) except `main.py` and `README.md`.
  - Prints a summary of files archived and deleted.
  - Does NOT touch directories (e.g., `core/`, `ui/`, `assets/`, etc.).

Be careful: deletion is irreversible unless you restore from `archive/root_backup/`.
"""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "root_backup"
WHITELIST = {"main.py", "README.md"}

print(f"Project root: {ROOT}")
print(f"Archive dir: {ARCHIVE}")

ARCHIVE.mkdir(parents=True, exist_ok=True)

files = [p for p in ROOT.iterdir() if p.is_file()]

to_delete = [p for p in files if p.name not in WHITELIST]

if not to_delete:
    print("No top-level files to delete.")
    exit(0)

print("Top-level files to be archived and deleted:")
for p in to_delete:
    print(" -", p.name)

confirm = input("Proceed and archive+delete these files? Type 'yes' to continue: ")
if confirm.lower() != "yes":
    print("Aborted by user.")
    exit(0)

archived = []
deleted = []
errors = []
for p in to_delete:
    try:
        dest = ARCHIVE / p.name
        # If dest exists, append a numeric suffix to avoid overwrite
        if dest.exists():
            i = 1
            while True:
                alt = ARCHIVE / f"{p.stem}.{i}{p.suffix}"
                if not alt.exists():
                    dest = alt
                    break
                i += 1
        shutil.copy2(p, dest)
        archived.append(dest.name)
        p.unlink()
        deleted.append(p.name)
    except Exception as e:
        errors.append((p.name, str(e)))

print("\nSummary:")
print(f"Archived: {len(archived)} files")
for n in archived:
    print(" -", n)
print(f"Deleted: {len(deleted)} files")
for n in deleted:
    print(" -", n)
if errors:
    print("Errors:")
    for name, err in errors:
        print(f" - {name}: {err}")
else:
    print("No errors.")

print("Done. You can restore files from archive/root_backup/")
