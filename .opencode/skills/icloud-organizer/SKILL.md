---
name: icloud-organizer
description: Maintain order in iCloud directory with smart scanning, de-duping, and de-cluttering
license: MIT
compatibility: opencode
metadata:
  audience: users
  workflow: file-management
---

## What I do

This skill helps you organize and maintain your iCloud directory with:
- **Full Scan**: Complete analysis of all files (first run or periodic)
- **Light Scan**: Quick check for new/changed files only
- **Smart Organization**: Recommends logical directory structure and naming conventions
- **De-duplication**: Finds and removes duplicate files using hash-based detection
- **De-clutter**: Identifies old/unaccessed files as candidates for deletion

## When to use me

Use this skill when you want to:
- First-time organization of a messy iCloud directory
- Regular maintenance to keep things organized
- Find and remove duplicate files
- Clean up old, unused files

## Directory Structure Recommendation

### Recommended: Hybrid Approach (Category + Date)

```
iCloud Drive/
├── Documents/
│   ├── Work/
│   │   ├── 2024/
│   │   ├── 2025/
│   │   └── 2026/
│   ├── Personal/
│   │   └── 2026/
│   └── Archives/
├── Images/
│   ├── Screenshots/
│   ├── Photos/
│   └── Screens/
├── Videos/
├── Audio/
├── Projects/
└── Downloads/
```

### Alternative Approaches

**Pure Category** (best for small, focused collections):
```
Documents/
├── Contracts/
├── Receipts/
└── Reports/
```

**Pure Date** (best for chronological records):
```
2024/
├── 01_January/
├── 02_February/
└── ...
```

**Pros/Cons Summary:**

| Approach | Pros | Cons |
|----------|------|------|
| Category + Date | Best of both, scalable | More complex |
| Pure Category | Easy to find type | Can mix unrelated |
| Pure Date | Chronological order | Hard to find by topic |
| Project-based | All related files together | Overhead for small files |

## Naming Convention Recommendation

### Format: `[Date]_[Category]_[Description]_[Version].ext`

**Examples:**
- `2026-04-15_Work_ProjectProposal_v1.pdf`
- `2026-03-20_Personal_TaxReturn_2025.pdf`
- `2026-01-05_Receipt_Amazon_Order-123.pdf`

### Key Rules

1. **Date Format**: Always use `YYYY-MM-DD` at the beginning (sorts chronologically)
2. **Separator**: Use underscores `_` instead of spaces
3. **Lowercase**: Use lowercase for consistency
4. **Version**: Use `v1`, `v2` instead of "final", "final2", "REALLY_FINAL"
5. **No Special Characters**: Avoid `/`, `:`, `*`, `?`, `"`, `<`, `>`, `|`

## Metadata Files

### Benefits
- **Preserve Dates**: Store original creation dates if lost during transfer
- **Search Enhancement**: Add searchable tags and descriptions
- **Context**: Add project info, people, locations
- **Backup**: Extra copy of important metadata

### Drawbacks
- **Extra Files**: Doubles file count
- **Maintenance**: Can become stale/out of sync
- **Tool Support**: Not all apps understand sidecar files
- **Clutter**: May feel unnecessary for simple files

### Recommendation
Use metadata files for:
- Photos (to preserve EXIF data)
- Important documents (contracts, legal)
- Files that have been transferred between systems

For routine files, skip metadata to avoid clutter.

## De-duplication Strategy

### Approach
1. **Group by Size**: Files with unique sizes cannot be duplicates
2. **Quick Hash**: Use xxHash/MD5 for fast comparison
3. **Full Hash**: SHA-256 for final verification
4. **Preserve Original**: Keep oldest or most descriptive filename

### Hash Algorithms
- **xxHash**: Very fast, good for first pass (blake2b also excellent)
- **SHA-256**: Slower but cryptographic certainty
- **Combined**: Fast pre-filter + slow final check

### Workflow
```
1. Scan all files → collect size + path
2. Group by size → unique sizes skip
3. For groups >1 → compute hash
4. Group by hash → duplicates found
5. Show results → user reviews
6. User confirms → delete selected
```

## De-clutter Options

### Criteria for "Old" Files
- **Not Accessed**: No access in X days (default: 365)
- **Created**: Created more than X years ago (default: 3 years)
- **Size Threshold**: Ignore very small files (<10KB)
- **Extensions**: Include/exclude specific types

### Review Process
1. List candidate files with metadata (date accessed, created, size)
2. Group by folder/age
3. User reviews before any deletion
4. Move to trash (not permanent delete)

### Configurable Options
- `--declutter-days N` (e.g., 365)
- `--created-before YYYY-MM-DD`
- `--min-size N` (bytes)
- `--include-extensions` (e.g., ".pdf,.doc")
- `--exclude-extensions` (e.g., ".log")

## Usage Examples

### Full Scan (First Run)
```
Scan the entire iCloud directory and provide:
- Current file inventory
- Duplicate detection
- Old file candidates
- Structure recommendations

python tools/icloud_organizer.py --full
```

### Light Scan (Incremental)
```
Scan only for:
- New files since last scan
- Modified files
- Recently changed duplicates

python tools/icloud_organizer.py --light
```

### Run De-dupe
```
Find all duplicate files and present:
- Groups of duplicates
- Size savings potential
- Options to keep/remove

python tools/icloud_organizer.py --dedupe
```

### Run De-clutter
```
Find files not accessed in:
- 1+ year
- 3+ years
- 5+ years

Present as review candidates

python tools/icloud_organizer.py --declutter --declutter-days 365
```

## Implementation Notes

- Use `os.walk()` for directory traversal
- Use `hashlib.sha256()` or `xxhash` for hashing
- Store scan state in `.icloud_organizer_state.json`
- Use `os.path.getmtime()`, `os.path.getctime()` for dates
- Handle symlinks and aliases appropriately
- Respect macOS extended attributes