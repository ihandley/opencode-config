# Quick Recovery Guide

## TL;DR - Three Options

### Option 1: Quick Check (No Changes)
```bash
python3 ~/code/github/opencode/tools/recover_dropbox_files.py
```
Shows status of 152 placeholder files by folder.

### Option 2: One-Time Recovery (Manual)
```bash
python3 ~/code/github/opencode/tools/recover_dropbox_files.py --delete --monitor
```
- Deletes local 0-byte placeholders
- Triggers iCloud resync
- Monitors progress (60 second timeout)
- Backups saved to `~/.opencode/dropbox_placeholder_backups/`

Then verify:
```bash
python3 ~/code/github/opencode/tools/recover_dropbox_files.py --report
```
Should show 0 remaining files.

### Option 3: Automated Scheduling (Daily at 2 AM)
```bash
cp ~/code/github/opencode/tools/com.opencode.dropbox-recovery.plist \
   ~/Library/LaunchAgents/

launchctl load ~/Library/LaunchAgents/com.opencode.dropbox-recovery.plist
```

## What Gets Backed Up
Metadata only (no disk space used):
- File names and paths
- Modification dates
- Folder locations

## What Happens to Files
1. Local 0-byte placeholders → **Deleted**
2. iCloud cloud copies → **Re-downloaded** to your Mac
3. Files appear locally with proper size/content

## Safety Notes
✅ **Safe to delete** - Files exist in iCloud cloud storage
✅ **Backed up** - Metadata saved before deletion
✅ **Reversible** - Can restore from iCloud.com if needed

## Monitoring Recovery
```bash
# Watch real-time download progress
brctl monitor -g

# Check sync status
brctl status com.apple.CloudDocs
```

## Manual Fallback
If scripts fail, use iCloud.com:
1. Visit [iCloud.com](https://icloud.com)
2. Click Files
3. Go to Filing Cabinet
4. Download files directly

## Need Help?
See `DROPBOX_RECOVERY.md` for detailed documentation.
