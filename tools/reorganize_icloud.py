#!/usr/bin/env python3
"""
iCloud Drive Reorganization Script
Moves files to new structured layout:

iCloud Drive/
├── Documents/
│   ├── Work/
│   ├── Personal/
│   ├── Archive/
│   ├── Filing Cabinet/
│   └── Scans/
├── Media/
│   ├── Photos/
│   ├── Music/
│   └── Audio/
├── Projects/
│   ├── Fusion360/
│   ├── Garden/
│   ├── Art/
│   └── BambuStudio/
└── Reference/
    └── Manuals/
"""

import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime

CLOUD_DOCS = Path(os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs"))

MOVES = [
    # Projects - move to Projects/
    {"src": "Fusion360", "dest": "Projects/Fusion360", "action": "move"},
    {"src": "Garden", "dest": "Projects/Garden", "action": "move"},
    {"src": "Art", "dest": "Projects/Art", "action": "move"},
    {"src": "BambuStudio", "dest": "Projects/BambuStudio", "action": "move"},
    
    # Audio - move to Media/Audio
    {"src": "Hardcore History", "dest": "Media/Audio", "action": "move"},
    
    # Documents - move to Documents/
    {"src": "Filing Cabinet", "dest": "Documents/Filing Cabinet", "action": "move"},
    {"src": "Scans", "dest": "Documents/Scans", "action": "move"},
    
    # Reference
    {"src": "Manual Library/Product Manuals", "dest": "Reference/Manuals", "action": "move"},
    
    # Media - will need special handling for Photos by year
    {"src": "Music", "dest": "Media/Music", "action": "move"},
    {"src": "Manual Library/Music", "dest": "Media/Music", "action": "merge"},
]


def ensure_dirs():
    """Create target directory structure."""
    dirs = [
        "Documents/Work",
        "Documents/Personal",
        "Documents/Archive",
        "Documents/Filing Cabinet",
        "Documents/Scans",
        "Media/Photos/2018",
        "Media/Photos/2019",
        "Media/Photos/2020",
        "Media/Photos/2021",
        "Media/Photos/2022",
        "Media/Photos/2023",
        "Media/Photos/2024",
        "Media/Photos/2025",
        "Media/Music",
        "Media/Audio",
        "Projects/Fusion360",
        "Projects/Garden",
        "Projects/Art",
        "Projects/BambuStudio",
        "Reference/Manuals",
    ]
    
    for d in dirs:
        target = CLOUD_DOCS / d
        if not target.exists():
            target.mkdir(parents=True, exist_ok=True)
            print(f"Created: {d}/")


def move_folder(src: str, dest: str, action: str = "move", dry_run: bool = True):
    """Move or merge a folder."""
    src_path = CLOUD_DOCS / src
    dest_path = CLOUD_DOCS / dest
    
    if not src_path.exists():
        print(f"  SKIP: {src} (doesn't exist)")
        return
    
    if dry_run:
        print(f"  [DRY RUN] Would {action}: {src} → {dest}")
        return
    
    if action == "move":
        shutil.move(str(src_path), str(dest_path))
        print(f"  Moved: {src} → {dest}")
    elif action == "merge":
        if not dest_path.exists():
            shutil.move(str(src_path), str(dest_path))
            print(f"  Moved: {src} → {dest}")
        else:
            # Merge contents
            for item in src_path.iterdir():
                dest_item = dest_path / item.name
                if dest_item.exists():
                    print(f"    Conflict: {item.name} exists in {dest}")
                else:
                    shutil.move(str(item), str(dest_item))
            # Remove empty dir
            if not any(src_path.iterdir()):
                shutil.rmtree(src_path)
            print(f"  Merged: {src} → {dest}")


def organize_photos(dry_run: bool = True):
    """Move photos to year folders."""
    pictures_path = CLOUD_DOCS / "Manual Library" / "Pictures"
    
    if not pictures_path.exists():
        print("  SKIP: Pictures folder not found")
        return
    
    # Known year folders
    year_folders = ["2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]
    
    for year in year_folders:
        src = pictures_path / year
        dest = CLOUD_DOCS / "Media" / "Photos" / year
        
        if src.exists():
            if dry_run:
                print(f"  [DRY RUN] Would move: Pictures/{year} → Media/Photos/{year}")
            else:
                if not dest.exists():
                    dest.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dest))
                print(f"  Moved: Pictures/{year} → Media/Photos/{year}")


def main():
    parser = argparse.ArgumentParser(description="Reorganize iCloud Drive")
    parser.add_argument("--execute", action="store_true", help="Actually perform moves (default is dry-run)")
    parser.add_argument("--photos", action="store_true", help="Also organize photos by year")
    args = parser.parse_args()
    
    dry_run = not args.execute
    
    print("=" * 60)
    if dry_run:
        print("DRY RUN MODE - No files will be moved")
        print("Run with --execute to actually move files")
    else:
        print("EXECUTING - Files will be moved!")
    print("=" * 60)
    
    print("\n1. Creating directory structure...")
    ensure_dirs()
    
    print("\n2. Moving folders...")
    for move in MOVES:
        move_folder(move["src"], move["dest"], move.get("action", "move"), dry_run)
    
    if args.photos:
        print("\n3. Organizing photos by year...")
        organize_photos(dry_run)
    
    print("\n" + "=" * 60)
    if dry_run:
        print("DRY RUN complete. Run with --execute to apply changes.")
    else:
        print("Reorganization complete!")
        print("\nNote: You may still need to:")
        print("  - Manually review Music/Manual Library/Pictures")
        print("  - Delete empty 'Manual Library' if empty")
    print("=" * 60)


if __name__ == "__main__":
    main()