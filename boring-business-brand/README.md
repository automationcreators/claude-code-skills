# Boring Business AI - Brand Image Generator Skill

Professional brand image generation for Boring Business AI across multiple platforms and use cases.

## Overview

This Claude Code skill provides comprehensive brand image generation capabilities including:

- **Complete Brand Guidelines** - Colors, typography, logo usage, and design principles
- **Beehiiv Email Headers** - Optimized newsletter headers (1200x600px)
- **Skool Course Covers** - Professional course covers (1280x720px, 1920x1080px)
- **Social Media Images** - Platform-specific posts for Instagram, Twitter, LinkedIn, Facebook
- **Custom Image Generation** - Flexible templates for any branded content

## Installation

### Prerequisites

```bash
# Install required Python packages
pip install -r requirements.txt
```

Required packages:
- Pillow >= 10.0.0
- numpy >= 1.24.0

### Optional Fonts

For best results, install these fonts:
- Montserrat (Black, Bold, Regular)
- Inter (Bold, Regular)
- Poppins (Bold, Regular)

The skill will fall back to system fonts if custom fonts aren't available.

## Output Locations

### Social Media Scripts
**Default Location:** `/Users/elizabethknopf/Documents/claudec/active/Social-Content-Generator/pillar_scripts/`

All social media scripts, content variations, and strategic content pieces are automatically saved here.

**Google Drive Backup:** https://drive.google.com/drive/folders/1KFTbNaKf44tyIVPknDnzshW-DsrJuxnx

### Generated Images
**Default Location:** `examples/output/`

All generated brand images (headers, covers, social posts) are saved here.

## Quick Start

### View Brand Guidelines

```
Show me the Boring Business AI brand guidelines.
```

### Generate Email Header

```
Create a Beehiiv header for our newsletter about AI automation.
Title: AI Automation Weekly
Subtitle: October 2025 Edition
```

### Generate Course Cover

```
Create a Skool course cover:
Course: AI Operations Fundamentals
Subtitle: From Setup to Scale
Layout: corner-logo
```

### Generate Social Media Post

```
Create an Instagram square post with the message:
"AI doesn't have to be complicated to be powerful"
Style: quote
Include logo
```

## Usage Examples

### 1. Beehiiv Headers

Three layout styles available: centered, left-aligned, and minimal.

```python
from scripts.beehiiv_header import BeehiivHeaderGenerator

generator = BeehiivHeaderGenerator()

# Centered layout
generator.generate_header(
    title="The Boring AI Weekly",
    subtitle="Real AI. Real Results.",
    layout='centered',
    size='large',
    output_path='newsletter_header.png'
)
```

**Layouts:**
- `centered`: Logo at top, centered text
- `left`: Logo left, text right
- `minimal`: Small icon, large title

**Sizes:**
- `large`: 1200x600px (recommended)
- `medium`: 600x400px

### 2. Skool Course Covers

Four layout styles with high contrast for thumbnail visibility.

```python
from scripts.skool_cover import SkoolCoverGenerator

generator = SkoolCoverGenerator()

# Corner logo layout
generator.generate_cover(
    course_title="AI Operations Fundamentals",
    subtitle="From Setup to Scale",
    key_points=[
        "Practical Implementation",
        "Real-World Case Studies",
        "Measurable ROI"
    ],
    layout='corner-logo',
    size='hd',
    output_path='course_cover.png'
)
```

**Layouts:**
- `corner-logo`: Logo in corner, centered text
- `split`: Logo left half, text right half
- `overlay`: Logo watermark, text over
- `banner`: Horizontal banner style

**Sizes:**
- `hd`: 1280x720px (recommended)
- `fhd`: 1920x1080px

### 3. Social Media Posts

Platform-specific dimensions and four post styles.

```python
from scripts.social_media import SocialMediaGenerator

generator = SocialMediaGenerator()

# Instagram quote post
generator.generate_post(
    message="Start with one automated process. Master it. Then scale.",
    platform='instagram',
    style='quote',
    size_type='square',
    include_logo=True,
    output_path='ig_quote.png'
)

# LinkedIn stat card
generator.generate_post(
    message="78%\nof businesses struggle with AI implementation",
    platform='linkedin',
    style='stat',
    size_type='post',
    output_path='li_stat.png'
)
```

**Platforms & Sizes:**

**Instagram:**
- `square`: 1080x1080px
- `portrait`: 1080x1350px
- `landscape`: 1080x566px

**Twitter/X:**
- `post`: 1200x675px

**LinkedIn:**
- `post`: 1200x627px

**Facebook:**
- `post`: 1200x630px

**Post Styles:**
- `quote`: Large centered quote
- `announcement`: Title + subtitle format
- `tip`: Tip card with label
- `stat`: Large number + context

### 4. Profile Pictures

```python
from scripts.social_media import SocialMediaGenerator

generator = SocialMediaGenerator()

generator.generate_profile(
    platform='instagram',
    output_path='profile.png'
)
```

Generates platform-optimized profile pictures with the AI OPS character logo.

## File Structure

```
boring-business-brand/
├── SKILL.md                    # Main skill documentation
├── BRAND_GUIDELINES.md         # Complete brand guidelines
├── LICENSE.txt                 # MIT License
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── assets/                     # Brand assets
│   ├── logo icon no bg.png
│   ├── logo icon.png
│   ├── banner with subtitle.png
│   └── [other logo variants]
├── scripts/                    # Generator scripts
│   ├── brand_generator.py      # Core generator class
│   ├── beehiiv_header.py       # Email header generator
│   ├── skool_cover.py          # Course cover generator
│   └── social_media.py         # Social media generator
└── examples/                   # Example outputs
```

## Brand Assets

The skill includes 7 logo variants:

1. **Icon only (no background)** - For overlays and transparent uses
2. **Icon with background** - For solid placements
3. **Full logo with title** - Complete branding
4. **Banner format** - Horizontal layouts
5. **Medium variant** - Balanced sizing
6. **Large variant** - High-res applications
7. **Small variant** - Compact uses

## Color Palette

```
Brand Orange: #FF8C00 (RGB: 255, 140, 0)
Brand Blue:   #1E5A8E (RGB: 30, 90, 142)
Dark Blue:    #0D2C4A (RGB: 13, 44, 74)
White:        #FFFFFF
Black:        #1A1A1A
```

## Typography

**Brand Title:** Bold sans-serif, always lowercase
- "boring business AI" ✓
- "Boring Business AI" ✗

**Tagline:** Regular sans-serif, italic, always lowercase
- "real ai. real results. for real business."

**Recommended Fonts:**
- Montserrat (preferred)
- Inter (alternative)
- Poppins (alternative)

## Technical Details

### Background Patterns

All images feature a blueprint-style technical pattern with:
- Grid lines at 40px intervals
- Circuit board style connection dots
- Technical diagram elements
- 20-30% opacity for subtle effect

### Optimization

Images are automatically optimized for their use case:
- PNG format with transparency support
- JPEG option for solid backgrounds
- Web-optimized file sizes
- High-contrast text for readability

### Text Handling

- Automatic text wrapping within margins
- Outline rendering for improved readability
- Responsive font sizing based on image dimensions
- Support for multi-line titles and subtitles

## Best Practices

### 1. Text Readability
- Keep text concise and impactful
- Use sentence case for longer text
- Maintain high contrast (orange on blue, white on blue)

### 2. Logo Usage
- Always use provided logo files
- Never distort or stretch
- Maintain clear space around logo
- Use icon-only for small applications

### 3. Platform Optimization
- Use recommended dimensions for each platform
- Test thumbnail visibility for course covers
- Optimize file size for email (< 200KB for Beehiiv)

### 4. Brand Consistency
- Always lowercase for brand name
- Use exact hex colors
- Apply blueprint pattern consistently
- Keep tagline visible in primary materials

## Troubleshooting

**Problem:** Text is hard to read
**Solution:** Increase text outline width, use white instead of orange for body text

**Problem:** Logo too small in thumbnails
**Solution:** Use larger logo variant or switch to icon-only layout

**Problem:** File size too large
**Solution:** Reduce dimensions or use JPEG format with quality=85

**Problem:** Fonts look different than examples
**Solution:** Install Montserrat font family or use system fallback

## Running Examples

Each generator script includes example usage:

```bash
# Test Beehiiv header generator
cd scripts
python beehiiv_header.py

# Test Skool cover generator
python skool_cover.py

# Test social media generator
python social_media.py

# Test core generator
python brand_generator.py
```

## Claude Code Integration

This skill integrates seamlessly with Claude Code. Simply describe what you need:

**Natural language examples:**

- "Create a Beehiiv header for next week's newsletter about AI automation"
- "Generate a Skool course cover for my new AI fundamentals course"
- "Make an Instagram post saying 'AI doesn't have to be complicated'"
- "Create a LinkedIn announcement for our product launch"
- "Generate a Twitter profile picture using the AI OPS character"

## Version History

**v1.0.0** (October 2025)
- Initial release
- Brand guidelines documentation
- Core image generation functionality
- Beehiiv header generator (3 layouts)
- Skool cover generator (4 layouts)
- Social media generator (4 platforms, 4 styles)
- 7 logo variants included
- Complete brand asset library

## Support & Contributing

For questions, issues, or enhancement requests:
1. Consult `BRAND_GUIDELINES.md` for visual specifications
2. Check example scripts for usage patterns
3. Review `SKILL.md` for complete documentation

## License

MIT License - See LICENSE.txt for details

Copyright (c) 2025 Boring Business AI

---

**Quick Links:**
- [Complete Skill Documentation](SKILL.md)
- [Brand Guidelines](BRAND_GUIDELINES.md)
- [License](LICENSE.txt)

**Skill Type:** Brand Management & Image Generation
**Category:** Design, Marketing, Content Creation
**Complexity:** Intermediate
**Dependencies:** Pillow, NumPy
