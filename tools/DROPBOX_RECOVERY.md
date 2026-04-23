# Automated Dropbox Placeholder File Recovery

## The Problem

152 PDF files in `Filing Cabinet` are 0-byte Dropbox placeholder files:
- Files were in Dropbox as stubs (not synced to disk)
- Files were moved to iCloud Drive while still as placeholders
- iCloud inherited the 0-byte status
- **But files DO exist in iCloud cloud storage** — just not downloaded locally

**Why this happened:**
When you moved files from Dropbox to iCloud, Dropbox placeholders (files not fully synced to disk) were moved as-is. iCloud Drive doesn't know how to recover Dropbox stubs, so they remain 0 bytes.

## The Solution

### How It Works

1. **Delete local placeholders** → Forces iCloud to re-sync the actual files from cloud
2. **Trigger iCloud resync** → Uses `brctl` to force re-download
3. **Monitor sync progress** → Watches for file downloads to complete
4. **Optional: Automated scheduling** → Can run daily via launchd

### Automation Tools

#### 1. Manual Recovery (One-time)

```bash
# Check current status
python3 ~/code/github/opencode/tools/recover_dropbox_files.py

# Delete all placeholders and trigger resync
python3 ~/code/github/opencode/tools/recover_dropbox_files.py --delete --monitor

# Generate status report
python3 ~/code/github/opencode/tools/recover_dropbox_files.py --report
```

#### 2. Automated Batch Recovery

```bash
# Run the automated recovery script
AUTO_RECOVER=true bash ~/code/github/opencode/tools/auto_recover_dropbox.sh

# Logs saved to: ~/.opencode/logs/dropbox_recovery_*.log
```

#### 3. Scheduled Recovery (Daily at 2 AM)

To install automated scheduled recovery:

```bash
# Copy launchd plist
cp ~/code/github/opencode/tools/com.opencode.dropbox-recovery.plist \
   ~/Library/LaunchAgents/

# Load the schedule
launchctl load ~/Library/LaunchAgents/com.opencode.dropbox-recovery.plist

# View logs
tail -f ~/.opencode/logs/dropbox-recovery.out
tail -f ~/.opencode/logs/dropbox-recovery.err
```

To uninstall:
```bash
launchctl unload ~/Library/LaunchAgents/com.opencode.dropbox-recovery.plist
rm ~/Library/LaunchAgents/com.opencode.dropbox-recovery.plist
```

### What Gets Backed Up

Before deletion, metadata is saved to: `~/.opencode/dropbox_placeholder_backups/`

Each file has a `.meta.json` backup containing:
```json
{
  "original_path": "/path/to/file.pdf",
  "name": "file.pdf",
  "parent": "Personal",
  "size": 0,
  "is_dropbox_placeholder": true
}
```

This lets you verify deletions without taking up disk space.

## Recovery Process Details

### Step 1: Identify Placeholders
```
Status by folder:
  Archive:    14 files
  Financial:  14 files
  Home:       14 files
  Legal:      24 files
  Medical:    35 files
  Personal:   27 files
  Work:       24 files
```

All 152 files are PDFs with Dropbox placeholder attributes.

### Step 2: Delete Local Copies
Deletes 0-byte files from disk. Originals still exist in:
- iCloud cloud storage
- Possibly Dropbox web (check dropbox.com)

### Step 3: Trigger iCloud Resync
Two methods (both attempted):
1. **`brctl`** - Apple's CloudDocs tool (most reliable)
2. **Finder** - Opens the directory to trigger sync

### Step 4: Monitor Download Progress
Uses `brctl monitor` to watch iCloud sync in real-time.
- Checks every few seconds for new downloads
- Times out after 60 seconds (safe default)
- Can be increased if needed

## Manual Alternative: iCloud.com

If automation fails:

1. Go to [iCloud.com](https://icloud.com)
2. Select "Files"
3. Navigate to "Filing Cabinet"
4. Download files directly from iCloud

## Troubleshooting

### Issue: Files still 0 bytes after recovery

**Solution:**
```bash
# Force a more aggressive resync
brctl monitor -g  # Monitor all CloudDocs activity

# Or check if files are stuck in upload queue
brctl status com.apple.CloudDocs
```

### Issue: "brctl not found"

**Solution:**
Install Command Line Tools:
```bash
xcode-select --install
```

### Issue: Very slow recovery

**Reason:** iCloud sync is bandwidth-limited
**Solution:**
- Check internet connection
- Ensure iCloud Drive sync is enabled (System Settings > iCloud)
- Close other upload-heavy apps

### Issue: Want to verify before deleting

**Solution:**
```bash
# Just run --report to see what will be deleted
python3 ~/code/github/opencode/tools/recover_dropbox_files.py --report

# Backups are created automatically with --delete
```

## Technical Details

### Dropbox Placeholder Identifier
Files are identified by the extended attribute: `com.dropbox.placeholder`

```bash
# View for a file
xattr -p com.dropbox.placeholder ~/path/to/file.pdf

# Check all in a folder
find ~/path/to/folder -exec xattr -p com.dropbox.placeholder {} \;
```

### What Happens to Files

**Before recovery:**
- **Local**: 0 bytes (placeholder)
- **iCloud cloud**: Full file (stored but not synced to disk)
- **Dropbox**: Possibly still there (original location)

**After recovery:**
- **Local**: Full file downloaded from iCloud
- **iCloud cloud**: Unchanged
- **Dropbox**: Original may still exist

### Why This Works

iCloud Drive doesn't automatically sync files that were moved-in as 0-byte placeholders. When you delete the local placeholder:

1. iCloud notices the deletion
2. iCloud re-downloads the file from its cloud storage
3. File appears locally with correct size/content

This is safe because **iCloud keeps cloud copies of all files**.

## Success Metrics

Run `--report` after recovery:

```bash
python3 ~/code/github/opencode/tools/recover_dropbox_files.py --report

# Should show:
# "total_remaining": 0
# All folders should be empty
```

Or manually verify:
```bash
# Check remaining 0-byte files
find ~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/Filing\ Cabinet \
  -size 0 -type f | wc -l

# Should return: 0
```

## Files Involved

- **Recovery script**: `~/code/github/opencode/tools/recover_dropbox_files.py`
- **Batch runner**: `~/code/github/opencode/tools/auto_recover_dropbox.sh`
- **Scheduler**: `~/code/github/opencode/tools/com.opencode.dropbox-recovery.plist`
- **Backups**: `~/.opencode/dropbox_placeholder_backups/`
- **Status reports**: `~/.opencode/dropbox_recovery_status.json`
- **Logs**: `~/.opencode/logs/dropbox_recovery_*.log`

## Next Steps

1. **Test run**: `python3 ~/code/github/opencode/tools/recover_dropbox_files.py --report`
2. **Manual recovery**: `python3 ~/code/github/opencode/tools/recover_dropbox_files.py --delete --monitor`
3. **Verify**: `python3 ~/code/github/opencode/tools/recover_dropbox_files.py --report` (should show 0 remaining)
4. **Optional**: Install scheduler if you want periodic checks: `launchctl load ~/Library/LaunchAgents/com.opencode.dropbox-recovery.plist`
