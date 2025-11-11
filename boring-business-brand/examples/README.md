# Boring Business AI - Examples & Output Directory

This folder contains example usage documentation and generated content from the Boring Business AI brand image generator skill.

## Directory Structure

```
examples/
├── README.md                    # This file
├── example_usage.py             # Demo script showing all capabilities
├── social_media_scripts.md      # Social media content scripts
├── SCRIPTS_SUMMARY.md           # Executive summary of scripts
└── output/                      # Generated images and content
    ├── beehiiv_*.png           # Email header images
    ├── skool_*.png             # Course cover images
    ├── social_*.png            # Social media post images
    └── profile_*.png           # Profile pictures
```

## File Organization

### Documentation Files (examples/)
Store all **documentation, scripts, and markdown files** directly in `examples/`:

- **Social Media Scripts:** `social_media_scripts.md`
- **Script Summaries:** `SCRIPTS_SUMMARY.md`
- **Usage Examples:** `example_usage.py`
- **Templates:** Any template or reference files

### Generated Content (examples/output/)
Store all **generated images and binary files** in `examples/output/`:

- **Email Headers:** `beehiiv_*.png`
- **Course Covers:** `skool_*.png`
- **Social Posts:** `social_*.png`
- **Profile Pictures:** `profile_*.png`
- **Custom Images:** Any generated brand images

## Usage Guidelines

### For Scripts and Content
When creating social media scripts, blog content, or documentation:

```python
output_path = "examples/social_media_scripts.md"
```

### For Generated Images
When generating brand images using the Python generators:

```python
from pathlib import Path
output_dir = Path(__file__).parent / 'output'
output_path = str(output_dir / 'beehiiv_header.png')
```

### For Ad-hoc Generation
If generating images manually or testing:

```bash
cd boring-business-brand/examples
python ../scripts/beehiiv_header.py
# Images will be saved to output/
```

## Current Files

### Documentation
- `social_media_scripts.md` - 5 comprehensive social media scripts with research
- `SCRIPTS_SUMMARY.md` - Executive summary and implementation guide
- `example_usage.py` - Complete demo of all image generators

### Generated Content
Check `output/` folder for:
- Generated example images
- Test outputs
- Production-ready brand images

## Best Practices

### Naming Conventions

**Script Files:**
- Use descriptive names: `social_media_scripts.md`, `email_templates.md`
- Include date if versioned: `social_scripts_2025-11.md`
- Use underscores for spaces: `content_calendar.md`

**Generated Images:**
- Use format: `{type}_{variant}_{date}.png`
- Examples:
  - `beehiiv_centered_2025-11.png`
  - `skool_corner_ai_fundamentals.png`
  - `social_quote_ig_2025-11-09.png`

### Version Control

**Include in Git:**
- ✅ Documentation files (`.md`)
- ✅ Example scripts (`.py`)
- ✅ Templates and references

**Exclude from Git:**
- ❌ Generated images (`.png`, `.jpg`)
- ❌ Large binary files
- ❌ Test outputs

Add to `.gitignore`:
```
examples/output/*.png
examples/output/*.jpg
examples/output/*.jpeg
```

## Workflows

### Creating New Social Media Scripts

1. Create script in `examples/social_media_scripts.md` (or new file)
2. Include research citations and data
3. Add engagement prompts and CTAs
4. Document in summary file
5. Generate any needed visual assets to `output/`

### Generating Brand Images

1. Use generator scripts from `../scripts/`
2. Save to `examples/output/`
3. Name descriptively
4. Document usage if for production

### Testing New Features

1. Create test script in `examples/`
2. Output test images to `examples/output/test_*.png`
3. Review and iterate
4. Clean up test files when done

## Archive Policy

### When to Archive
- Scripts older than 6 months
- Outdated brand guidelines
- Deprecated templates
- Old test files

### How to Archive
Create `examples/archive/` subdirectory:
```
examples/
├── archive/
│   ├── 2025-q1/
│   └── 2025-q2/
└── current files...
```

## Integration with Skill

This folder structure integrates with the skill's SKILL.md documentation:

**From SKILL.md:**
> "Generated content and examples are stored in the `examples/` directory with generated images in `examples/output/`"

**File Organization:**
- Scripts and docs: `examples/*.md`
- Generated images: `examples/output/*.png`
- Demo code: `examples/*.py`

---

**Last Updated:** November 9, 2025
**Maintained By:** Boring Business AI Brand System
**Questions?** See main `README.md` or `SKILL.md`
