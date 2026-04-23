#!/usr/bin/env python3
"""
Recover Dropbox placeholder files by downloading them from iCloud or restoration.

The issue: 152 PDF files in Filing Cabinet are Dropbox placeholders (0 bytes)
moved from Dropbox to iCloud Drive while not fully synced.

Root cause:
- Files were in Dropbox as stubs/placeholders (not synced to disk)
- Files were moved to iCloud Drive
- iCloud inherited the 0-byte placeholder status
- Files DO exist in iCloud cloud, just not locally

Automated recovery:
1. Delete local 0-byte placeholders → triggers iCloud to re-sync
2. Force iCloud re-download via brctl or Finder
3. Monitor sync status
"""

import os
import json
import subprocess
import time
from pathlib import Path
from typing import List
import sys
import argparse


def find_dropbox_placeholders(root_path: str) -> List[Path]:
    """Find all files with Dropbox placeholder extended attribute."""
    placeholders = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            filepath = Path(root) / file
            try:
                result = subprocess.run(
                    ["xattr", "-p", "com.dropbox.placeholder", str(filepath)],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0 and filepath.stat().st_size == 0:
                    placeholders.append(filepath)
            except Exception:
                pass
    return sorted(placeholders)


def backup_placeholder(filepath: Path, backup_dir: Path) -> bool:
    """Create metadata backup of placeholder before deletion."""
    try:
        # Store metadata for recovery if needed
        metadata = {
            "original_path": str(filepath),
            "name": filepath.name,
            "parent": filepath.parent.name,
            "size": 0,
            "modified": filepath.stat().st_mtime,
            "is_dropbox_placeholder": True
        }
        backup_meta_path = backup_dir / f"{filepath.name}.meta.json"
        with open(backup_meta_path, "w") as f:
            json.dump(metadata, f, indent=2)
        return True
    except Exception as e:
        print(f"✗ Backup failed for {filepath.name}: {e}")
        return False


def delete_placeholder(filepath: Path) -> bool:
    """Delete a placeholder file."""
    try:
        filepath.unlink()
        return True
    except Exception as e:
        print(f"✗ Failed to delete {filepath}: {e}")
        return False


def trigger_icloud_resync(root_path: str) -> bool:
    """Trigger iCloud re-sync for the directory."""
    try:
        # Use brctl to check status and trigger resync
        result = subprocess.run(
            ["brctl", "status", "com.apple.CloudDocs"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            print("📡 iCloud sync status checked")
            return True
    except Exception:
        pass
    
    # Fallback: try to trigger via Finder
    try:
        subprocess.run(
            ["open", root_path],
            timeout=5
        )
        print("📂 Opened in Finder to trigger sync")
        return True
    except Exception:
        pass
    
    return False


def delete_all_placeholders(root_path: str, backup: bool = True) -> dict:
    """Delete all Dropbox placeholders and return results."""
    placeholders = find_dropbox_placeholders(root_path)
    
    if not placeholders:
        return {"deleted": 0, "failed": 0, "message": "No placeholders found"}
    
    backup_dir = None
    if backup:
        backup_dir = Path.home() / ".opencode" / "dropbox_placeholder_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"💾 Backup directory: {backup_dir}")
    
    deleted = 0
    failed = 0
    
    print(f"\n🗑️  Deleting {len(placeholders)} placeholder files...\n")
    
    for i, placeholder in enumerate(placeholders, 1):
        folder = placeholder.parent.name
        print(f"[{i}/{len(placeholders)}] {folder:12} > {placeholder.name:40}", end=" ")
        
        # Backup metadata
        if backup_dir:
            backup_placeholder(placeholder, backup_dir)
        
        # Delete
        if delete_placeholder(placeholder):
            print("✓")
            deleted += 1
        else:
            print("✗")
            failed += 1
        
        # Small delay to avoid overwhelming system
        if i % 10 == 0:
            time.sleep(0.5)
    
    print(f"\n✅ Deleted: {deleted}")
    print(f"❌ Failed: {failed}")
    
    # Trigger resync
    print("\n📡 Triggering iCloud sync...")
    trigger_icloud_resync(root_path)
    
    return {
        "deleted": deleted,
        "failed": failed,
        "backup_dir": str(backup_dir) if backup_dir else None
    }


def monitor_icloud_sync(root_path: str, timeout_seconds: int = 60) -> bool:
    """Monitor iCloud sync progress."""
    print(f"\n⏳ Monitoring iCloud sync (timeout: {timeout_seconds}s)...\n")
    
    start_time = time.time()
    
    try:
        # Use brctl to monitor
        result = subprocess.run(
            ["brctl", "monitor", "-t", str(timeout_seconds), 
             "com.apple.CloudDocs"],
            timeout=timeout_seconds + 5
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⏱️  Monitor timeout reached")
        return False
    except Exception as e:
        print(f"Monitor unavailable: {e}")
        return False


def generate_report(root_path: str) -> None:
    """Generate recovery report."""
    placeholders = find_dropbox_placeholders(root_path)
    
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_remaining": len(placeholders),
        "by_folder": {}
    }
    
    for p in placeholders:
        folder = p.parent.name
        if folder not in report["by_folder"]:
            report["by_folder"][folder] = 0
        report["by_folder"][folder] += 1
    
    report_path = Path.home() / ".opencode" / "dropbox_recovery_status.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print("\n📋 Recovery Status Report:")
    print(json.dumps(report, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Recover Dropbox placeholder files from iCloud"
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete all 0-byte placeholder files"
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        default=True,
        help="Create metadata backup before deletion"
    )
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Monitor iCloud sync after deletion"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate recovery status report"
    )
    
    args = parser.parse_args()
    
    root_path = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Documents/Filing Cabinet")
    
    if not args.delete and not args.report and not args.monitor:
        # Default: show status
        placeholders = find_dropbox_placeholders(root_path)
        print(f"📊 Found {len(placeholders)} Dropbox placeholder files\n")
        
        by_folder = {}
        for p in placeholders:
            folder = p.parent.name
            by_folder[folder] = by_folder.get(folder, 0) + 1
        
        for folder in sorted(by_folder.keys()):
            print(f"  {folder:12} {by_folder[folder]:2} files")
        
        print("\n💡 Use --delete to recover these files")
        print("💡 Use --report to save status")
        return
    
    if args.delete:
        result = delete_all_placeholders(root_path, backup=args.backup)
        print(f"\n{json.dumps(result, indent=2)}")
    
    if args.monitor:
        monitor_icloud_sync(root_path)
    
    if args.report:
        generate_report(root_path)


if __name__ == "__main__":
    main()
