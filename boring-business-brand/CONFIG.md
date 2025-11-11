# Boring Business AI - Brand Skill Configuration

## Output Paths Configuration

### Default Output Locations

**Social Media Scripts & Content:**
```
/Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator/pillar_scripts/
```

**Generated Brand Images:**
```
/Users/elizabethknopf/Documents/claudec/systems/skills-main/boring-business-brand/examples/output/
```

**Documentation & Guides:**
```
/Users/elizabethknopf/Documents/claudec/systems/skills-main/boring-business-brand/examples/
```

## File Naming Conventions

### Social Media Scripts
Format: `{type}_{date}.md`

Examples:
- `social_media_scripts_2025-11-09.md`
- `email_content_series_2025-11.md`
- `linkedin_posts_2025-11-09.md`

### Script Summaries
Format: `{TYPE}_SUMMARY_{date}.md`

Examples:
- `SCRIPTS_SUMMARY_2025-11-09.md`
- `CONTENT_SUMMARY_2025-11.md`

### Generated Images
Format: `{platform}_{variant}_{description}.png`

Examples:
- `beehiiv_centered_weekly_newsletter.png`
- `skool_corner_ai_fundamentals.png`
- `social_quote_ig_nov.png`

## Integration Points

### Google Drive Sync (Future)
**Target Folder:**
- Folder ID: `1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx`
- Name: Content Scripts / Pillar Scripts
- Purpose: Cloud backup and team access

**Sync Strategy:**
- Automatic upload after script generation
- Version naming with timestamps
- Maintain local copies in pillar_scripts/

### GitHub Repository
**Repository:** `automationcreators/claude-code-skills`
**Branch:** `main`
**Path:** `boring-business-brand/`

**Sync Strategy:**
- Commit skill updates
- Push documentation changes
- Keep generated content local (not in repo)

## Script Generation Defaults

### When Generating Social Media Scripts

**Default Location:**
```python
output_path = "/Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator/pillar_scripts/"
filename = f"social_media_scripts_{date.today().strftime('%Y-%m-%d')}.md"
```

**Include:**
- Research citations
- Engagement prompts
- Platform adaptations
- Visual requirements
- Usage notes

### When Generating Brand Images

**Default Location:**
```python
output_dir = Path(__file__).parent.parent / "examples" / "output"
filename = f"{platform}_{layout}_{description}.png"
```

**Include:**
- Optimized file size
- Correct dimensions
- Brand colors applied
- Metadata in filename

## Environment Variables (Optional)

```bash
# Set default pillar scripts location
export PILLAR_SCRIPTS_DIR="/Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator/pillar_scripts"

# Set brand assets location
export BRAND_ASSETS_DIR="/Users/elizabethknopf/Documents/claudec/systems/skills-main/boring-business-brand/assets"

# Set output directory for images
export BRAND_OUTPUT_DIR="/Users/elizabethknopf/Documents/claudec/systems/skills-main/boring-business-brand/examples/output"
```

## Usage in Scripts

### Python Scripts

```python
import os
from pathlib import Path
from datetime import date

# Get pillar scripts directory
PILLAR_SCRIPTS_DIR = os.getenv(
    'PILLAR_SCRIPTS_DIR',
    '/Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator/pillar_scripts'
)

# Generate filename with date
today = date.today().strftime('%Y-%m-%d')
output_path = Path(PILLAR_SCRIPTS_DIR) / f"social_media_scripts_{today}.md"

# Write content
with open(output_path, 'w') as f:
    f.write(content)

print(f"✓ Saved to: {output_path}")
```

### Bash/Shell Scripts

```bash
#!/bin/bash

# Set default directories
PILLAR_SCRIPTS_DIR="${PILLAR_SCRIPTS_DIR:-/Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator/pillar_scripts}"
TODAY=$(date +%Y-%m-%d)

# Generate filename
OUTPUT_FILE="$PILLAR_SCRIPTS_DIR/social_media_scripts_${TODAY}.md"

# Copy or generate content
echo "Saving to: $OUTPUT_FILE"
```

## Directory Structure

```
Social-Content-Generator/
└── pillar_scripts/
    ├── README.md                                    # Documentation
    ├── social_media_scripts_2025-11-09.md          # Latest scripts
    ├── SCRIPTS_SUMMARY_2025-11-09.md               # Summary doc
    ├── FULL_SCRIPT_VARIATION_1_CONTRARIAN.md       # Example variations
    ├── FULL_SCRIPT_VARIATION_2_AUTHORITY.md
    └── 2025-11-05_ai_agents_4x_faster_contrarian.md

boring-business-brand/
├── assets/                  # Brand assets (logos, fonts)
├── examples/
│   ├── output/             # Generated images
│   ├── example_usage.py    # Demo scripts
│   └── README.md           # Examples documentation
└── scripts/                # Python generators
```

## Best Practices

### When Creating New Scripts

1. **Use pillar_scripts as default destination**
   - All social media content
   - Blog post scripts
   - Email sequences
   - Video scripts

2. **Include date in filename**
   - Format: `YYYY-MM-DD`
   - Helps with version tracking
   - Easy to find latest

3. **Create summary document**
   - Executive summary
   - Key stats/research
   - Usage recommendations

4. **Maintain naming consistency**
   - Lowercase with underscores
   - Descriptive names
   - Include type prefix

### When Generating Images

1. **Use examples/output for all images**
   - Keep separate from scripts
   - Easier to manage
   - Better for .gitignore

2. **Name descriptively**
   - Include platform
   - Include variant/layout
   - Include purpose

3. **Optimize before saving**
   - Web-optimized PNG
   - < 200KB for emails
   - Correct dimensions

## Automation Hooks

### Post-Generation Actions

After generating scripts in pillar_scripts/:

1. ✅ Save to local pillar_scripts folder
2. 🔄 (Future) Sync to Google Drive folder
3. 📝 Update SCRIPTS_SUMMARY document
4. 🔔 Notify user of location
5. 📊 Track generation metrics

### Pre-Generation Checks

Before generating new scripts:

1. ✅ Verify pillar_scripts directory exists
2. ✅ Check for existing file with same date
3. ✅ Load previous summaries for context
4. ✅ Confirm research data is current
5. ✅ Validate output path is writable

## Troubleshooting

### Issue: pillar_scripts folder not found

**Solution:**
```bash
mkdir -p ~/Documents/claudec/active/Social-Content-Generator/pillar_scripts
```

### Issue: Permission denied writing to folder

**Solution:**
```bash
chmod 755 ~/Documents/claudec/active/Social-Content-Generator/pillar_scripts
```

### Issue: File already exists

**Solution:**
- Append time to filename: `_YYYY-MM-DD_HHmm`
- Or use version number: `_v2`
- Or prompt user for overwrite

### Issue: Google Drive sync not working

**Status:** Google Drive MCP integration planned but not yet implemented.

**Workaround:**
- Manually upload to Google Drive
- Use Google Drive desktop app for auto-sync
- Or use rclone/gdrive CLI tools

## Future Enhancements

### Planned Features

1. **Google Drive Integration**
   - Automatic upload after generation
   - Two-way sync with Drive folder
   - Version history tracking

2. **Skill Configuration File**
   - YAML/JSON config for paths
   - User-customizable defaults
   - Per-project overrides

3. **Template Management**
   - Save custom templates to pillar_scripts/templates/
   - Quick template selection
   - Template inheritance

4. **Content Calendar Integration**
   - Schedule script generation
   - Track publication dates
   - Auto-archive old scripts

---

**Last Updated:** November 10, 2025
**Version:** 1.1
**Maintained By:** Boring Business AI Brand System
