#!/usr/bin/env python3
"""
iCloud Drive Organizer
Maintains order in iCloud directory with smart scanning, de-duping, and de-cluttering.
"""

import os
import sys
import json
import hashlib
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set

STATE_FILE = ".icloud_organizer_state.json"
CONFIG_DEFAULTS = {
    "declutter_days": 365,
    "declutter_min_size": 10240,
    "declutter_extensions": [],
    "exclude_dirs": [".Trash", ".DS_Store", "node_modules", ".git"],
    "hash_algorithm": "sha256",
}


class iCloudOrganizer:
    def __init__(self, root_path: str, config: dict = None):
        self.root_path = Path(root_path).expanduser().resolve()
        self.config = {**CONFIG_DEFAULTS, **(config or {})}
        self.state_file = self.root_path / STATE_FILE
        self.state = self._load_state()

    def _load_state(self) -> dict:
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_state(self):
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def _walk_files(self, exclude_dirs: List[str] = None) -> List[dict]:
        exclude_dirs = exclude_dirs or self.config.get("exclude_dirs", [])
        files = []

        for root, dirs, filenames in os.walk(self.root_path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for filename in filenames:
                if filename in exclude_dirs:
                    continue

                filepath = Path(root) / filename
                try:
                    stat = filepath.stat()
                    files.append({
                        "path": str(filepath),
                        "relative_path": str(filepath.relative_to(self.root_path)),
                        "name": filename,
                        "size": stat.st_size,
                        "mtime": stat.st_mtime,
                        "ctime": stat.st_ctime,
                        "atime": stat.st_atime,
                    })
                except (OSError, PermissionError):
                    continue

        return files

    def _compute_hash(self, filepath: Path, algorithm: str = "sha256") -> str:
        if algorithm == "sha256":
            hasher = hashlib.sha256()
        elif algorithm == "md5":
            hasher = hashlib.md5()
        else:
            hasher = hashlib.blake2b()

        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def full_scan(self) -> dict:
        print(f"Running full scan on {self.root_path}...")
        files = self._walk_files()

        self.state = {
            "last_full_scan": datetime.now().isoformat(),
            "last_light_scan": None,
            "file_count": len(files),
            "files": {f["relative_path"]: f for f in files}
        }
        self._save_state()

        print(f"Found {len(files)} files")

        return {
            "total_files": len(files),
            "total_size": sum(f["size"] for f in files),
            "files": files[:100],
            "more_files": len(files) - 100
        }

    def light_scan(self) -> dict:
        if not self.state.get("last_full_scan"):
            print("No previous full scan found. Running full scan first...")
            return self.full_scan()

        print(f"Running light scan on {self.root_path}...")
        current_files = {f["relative_path"]: f for f in self._walk_files()}

        old_files = self.state.get("files", {})
        new_files = []
        modified_files = []
        deleted_files = []

        for path, file_data in current_files.items():
            if path not in old_files:
                new_files.append(file_data)
            elif old_files[path]["mtime"] != file_data["mtime"]:
                modified_files.append(file_data)

        for path in old_files:
            if path not in current_files:
                deleted_files.append(path)

        self.state["last_light_scan"] = datetime.now().isoformat()
        self.state["files"] = current_files
        self.state["file_count"] = len(current_files)
        self._save_state()

        return {
            "new_files": len(new_files),
            "modified_files": len(modified_files),
            "deleted_files": len(deleted_files),
            "new": new_files[:20],
            "modified": modified_files[:20]
        }

    def find_duplicates(self) -> dict:
        print("Finding duplicates...")
        files = self._walk_files()

        size_groups = defaultdict(list)
        for f in files:
            if f["size"] > 0:
                size_groups[f["size"]].append(f)

        duplicates = []
        total_savings = 0

        for size, group in size_groups.items():
            if len(group) < 2:
                continue

            hash_groups = defaultdict(list)
            for f in group:
                filepath = Path(f["path"])
                file_hash = self._compute_hash(filepath, self.config["hash_algorithm"])
                hash_groups[file_hash].append(f)

            for file_hash, dup_group in hash_groups.items():
                if len(dup_group) < 2:
                    continue

                dup_group.sort(key=lambda x: (x["ctime"], x["name"]))
                original = dup_group[0]
                copies = dup_group[1:]

                savings = sum(d["size"] for d in copies)
                total_savings += savings

                duplicates.append({
                    "original": original,
                    "copies": copies,
                    "hash": file_hash,
                    "savings": savings
                })

        print(f"Found {len(duplicates)} duplicate groups, {total_savings / 1024 / 1024:.2f} MB can be freed")

        return {
            "duplicate_groups": len(duplicates),
            "total_savings_bytes": total_savings,
            "duplicates": duplicates[:50]
        }

    def remove_duplicates(self, duplicate_groups: List[dict], keep_originals: bool = True) -> dict:
        removed = []
        total_freed = 0

        for group in duplicate_groups:
            original = group["original"]
            for copy in group["copies"]:
                try:
                    os.remove(copy["path"])
                    removed.append(copy["path"])
                    total_freed += copy["size"]
                    print(f"Removed: {copy['relative_path']}")
                except OSError as e:
                    print(f"Failed to remove {copy['path']}: {e}")

        return {
            "removed_count": len(removed),
            "freed_bytes": total_freed
        }

    def find_old_files(self, days: int = None, min_size: int = None,
                       include_extensions: List[str] = None,
                       exclude_extensions: List[str] = None) -> dict:
        days = days or self.config.get("declutter_days", 365)
        min_size = min_size or self.config.get("declutter_min_size", 10240)

        print(f"Finding files not accessed in {days} days...")
        cutoff = datetime.now() - timedelta(days=days)

        files = self._walk_files()
        candidates = []

        for f in files:
            if f["size"] < min_size:
                continue

            if include_extensions:
                ext = Path(f["name"]).suffix.lower()
                if ext not in include_extensions:
                    continue

            if exclude_extensions:
                ext = Path(f["name"]).suffix.lower()
                if ext in exclude_extensions:
                    continue

            last_access = datetime.fromtimestamp(f["atime"])
            if last_access < cutoff:
                candidates.append({
                    **f,
                    "last_accessed": last_access.isoformat(),
                    "created": datetime.fromtimestamp(f["ctime"]).isoformat(),
                    "days_since_access": (datetime.now() - last_access).days
                })

        candidates.sort(key=lambda x: x["days_since_access"], reverse=True)

        by_year = defaultdict(list)
        for c in candidates:
            year = datetime.fromtimestamp(c["ctime"]).year
            by_year[year].append(c)

        print(f"Found {len(candidates)} files as de-clutter candidates")

        return {
            "total_candidates": len(candidates),
            "by_year": {str(k): len(v) for k, v in sorted(by_year.items())},
            "candidates": candidates[:100]
        }

    def review_and_delete(self, candidates: List[dict], delete: bool = False) -> dict:
        moved_to_trash = []

        if not delete:
            print("\n=== DE-CLUTTER REVIEW MODE ===")
            print(f"Found {len(candidates)} candidates. Run with --delete to actually remove.")
            print("\nShowing oldest files first:")
            for c in candidates[:20]:
                print(f"  {c['days_since_access']} days old: {c['relative_path']}")
            return {"review_mode": True, "candidates_count": len(candidates)}

        for c in candidates:
            try:
                subprocess.run(["trash", c["path"]], check=True)
                moved_to_trash.append(c["path"])
            except subprocess.CalledProcessError:
                try:
                    subprocess.run(["mv", c["path"], os.path.expanduser("~/.Trash/")], check=True)
                    moved_to_trash.append(c["path"])
                except subprocess.CalledProcessError as e:
                    print(f"Failed to trash: {c['path']}: {e}")

        return {
            "moved_to_trash": len(moved_to_trash),
            "paths": moved_to_trash
        }

    def clean_previews(self) -> dict:
        print("Finding preview files...")
        preview_extensions = [".lrprev", ".lrfprev", ".lrprevplugin", ".db"]

        files = self._walk_files()
        preview_files = []

        for f in files:
            ext = Path(f["name"]).suffix.lower()
            if ext in preview_extensions:
                preview_files.append(f)

        total_size = sum(f["size"] for f in preview_files)
        print(f"Found {len(preview_files)} preview files, {total_size / 1024 / 1024:.1f} MB")

        print("Moving to trash...")
        moved = []
        freed = 0
        trash_dir = Path(os.path.expanduser("~/.Trash"))

        for f in preview_files:
            try:
                dest = trash_dir / f["name"]
                counter = 1
                while dest.exists():
                    stem = Path(f["name"]).stem
                    ext = Path(f["name"]).suffix
                    dest = trash_dir / f"{stem}_{counter}{ext}"
                    counter += 1

                os.rename(f["path"], dest)
                moved.append(f["relative_path"])
                freed += f["size"]
                if len(moved) % 100 == 0:
                    print(f"  Moved {len(moved)}...")
            except OSError as e:
                print(f"Failed: {f['path']}: {e}")

        print(f"Done. Moved {len(moved)} files, freed {freed / 1024 / 1024:.1f} MB")
        return {"removed": len(moved), "freed_bytes": freed, "files": moved[:50]}

    def generate_recommendations(self) -> dict:
        files = self._walk_files()

        ext_groups = defaultdict(list)
        for f in files:
            ext = Path(f["name"]).suffix.lower() or "no_extension"
            ext_groups[ext].append(f)

        by_size = sorted(files, key=lambda x: x["size"], reverse=True)[:20]

        return {
            "extension_distribution": {k: len(v) for k, v in sorted(ext_groups.items(), key=lambda x: -len(x[1]))[:10]},
            "largest_files": [{"path": f["relative_path"], "size": f["size"]} for f in by_size],
            "recommended_structure": {
                "Documents/": ["Work/", "Personal/", "Archives/"],
                "Images/": ["Screenshots/", "Photos/", "Screens/"],
                "Projects/": ["<project-name>/"],
                "Downloads/": ["temp/"]
            }
        }


def main():
    parser = argparse.ArgumentParser(description="iCloud Drive Organizer")
    parser.add_argument("path", nargs="?", default=os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs"),
                        help="Path to iCloud Drive (default: Apple CloudDocs)")
    parser.add_argument("--full", action="store_true", help="Run full scan")
    parser.add_argument("--light", action="store_true", help="Run light scan (incremental)")
    parser.add_argument("--dedupe", action="store_true", help="Find and list duplicates")
    parser.add_argument("--dedupe-remove", action="store_true", help="Remove duplicates (keeps oldest)")
    parser.add_argument("--declutter", action="store_true", help="Find old files for cleanup")
    parser.add_argument("--declutter-days", type=int, default=365, help="Files not accessed in N days")
    parser.add_argument("--declutter-delete", action="store_true", help="Actually delete old files (moves to trash)")
    parser.add_argument("--recommend", action="store_true", help="Generate structure/naming recommendations")
    parser.add_argument("--clean-previews", action="store_true", help="Remove Lightroom/Logic preview files")
    parser.add_argument("--output", choices=["json", "text"], default="text", help="Output format")

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: Path does not exist: {args.path}")
        print("Provide a valid iCloud Drive path or ensure iCloud Drive is synced.")
        sys.exit(1)

    organizer = iCloudOrganizer(args.path)

    results = {}

    if args.full:
        results = organizer.full_scan()
    elif args.light:
        results = organizer.light_scan()
    elif args.dedupe:
        results = organizer.find_duplicates()
    elif args.dedupe_remove:
        dupes = organizer.find_duplicates()
        if dupes.get("duplicates"):
            results = organizer.remove_duplicates(dupes["duplicates"])
    elif args.declutter:
        old_files = organizer.find_old_files(days=args.declutter_days)
        if args.declutter_delete:
            results = organizer.review_and_delete(old_files.get("candidates", []), delete=True)
        else:
            results = organizer.review_and_delete(old_files.get("candidates", []), delete=False)
    elif args.recommend:
        results = organizer.generate_recommendations()
    elif args.clean_previews:
        results = organizer.clean_previews()
    else:
        parser.print_help()
        sys.exit(1)

    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        for key, value in results.items():
            if isinstance(value, list):
                if len(value) > 10:
                    print(f"{key}: {len(value)} items (showing first 10)")
                    for v in value[:10]:
                        print(f"  - {v}")
                else:
                    print(f"{key}: {value}")
            elif isinstance(value, dict):
                print(f"{key}:")
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"{key}: {value}")


if __name__ == "__main__":
    main()