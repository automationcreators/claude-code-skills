# Boring Business AI - Brand Image Generator

Generate professional, on-brand images for Boring Business AI across multiple platforms and use cases.

## Description

This skill provides comprehensive brand image generation capabilities for the "boring business AI" brand. It includes brand guidelines, asset management, and automated image generation for various platforms including Beehiiv headers, Skool course covers, social media posts, and general branded content.

**Key Features:**
- Complete brand guidelines and asset library
- Platform-specific image generation (Beehiiv, Skool, social media)
- Consistent application of brand colors, typography, and patterns
- Blueprint background pattern generation
- Multiple layout templates and variations
- Automated sizing and formatting for different platforms

## When to Use This Skill

Use this skill when you need to:
- Create email newsletter headers for Beehiiv
- Design course covers for Skool
- Generate social media graphics (Twitter, LinkedIn, Facebook, Instagram)
- Create branded presentation slides
- Design marketing materials with consistent branding
- Generate thumbnails or cover images
- Create profile pictures or banner images
- Access brand guidelines and specifications

## Usage

### View Brand Guidelines

```
I need to see the Boring Business AI brand guidelines.
```

### Generate Beehiiv Email Header

```
Create a Beehiiv header image for our newsletter about [topic].
Title: [title]
Subtitle: [optional subtitle]
```

**Output:** 1200x600px PNG optimized for email headers

### Generate Skool Course Cover

```
Create a Skool course cover image for:
Course: [course name]
Topic: [main topic]
[Optional: Key points or subtitle]
```

**Output:** 1280x720px or 1920x1080px PNG/JPEG

### Generate Social Media Image

```
Create a [platform] post image with:
Message: [main message]
Style: [square/landscape/portrait]
Include logo: [yes/no]
```

**Output:** Platform-specific dimensions (1080x1080, 1200x630, etc.)

### Generate Custom Branded Image

```
Create a branded image:
Dimensions: [width]x[height]
Layout: [centered/left/right/custom]
Text: [main text]
Subtitle: [optional]
Include: [logo/icon/both]
```

## Sub-Skills & Templates

### 1. Beehiiv Header Generator
Optimized email newsletter headers with consistent branding.

**Specifications:**
- Dimensions: 1200x600px or 600x400px
- Format: PNG
- Elements: Logo, title, tagline, blueprint background
- Text: High contrast white on blue
- Optimization: Web-optimized, < 200KB

**Layouts:**
- **Centered:** Logo and text centered
- **Left-aligned:** Logo left, text right
- **Minimal:** Icon only with large title
- **Full brand:** Complete branding with tagline

### 2. Skool Course Cover Generator
Professional course covers for Skool platform.

**Specifications:**
- Dimensions: 1280x720px (16:9) or 1920x1080px
- Format: PNG or JPEG
- Elements: Logo placement, course title, subtitle, blueprint BG
- Thumbnail-friendly: High contrast for small previews

**Layouts:**
- **Corner logo:** Logo in top-left, title centered
- **Split screen:** Logo left half, text right half
- **Overlay:** Logo watermark, text centered
- **Banner style:** Logo + title in banner across top/bottom

### 3. Social Media Image Generator
Platform-specific image generation with proper dimensions and optimization.

**Platforms Supported:**

**Twitter/X:**
- Profile: 400x400px
- Header: 1500x500px
- Post: 1200x675px

**LinkedIn:**
- Profile: 400x400px
- Banner: 1584x396px
- Post: 1200x627px

**Facebook:**
- Profile: 180x180px
- Cover: 820x312px
- Post: 1200x630px

**Instagram:**
- Profile: 320x320px
- Square: 1080x1080px
- Portrait: 1080x1350px
- Landscape: 1080x566px

**Layouts:**
- **Quote card:** Large text with logo
- **Announcement:** Title + subtitle + logo
- **Tip card:** Numbered tip with branding
- **Stat card:** Large number/stat with context

### 4. General Purpose Image Generator
Flexible image generation for presentations, blogs, thumbnails, and more.

**Common Sizes:**
- Blog header: 1200x630px
- Thumbnail: 1280x720px
- Presentation slide: 1920x1080px
- Square graphic: 1080x1080px
- Banner: 728x90px, 970x250px

## Technical Implementation

### Color Palette (RGB)

```python
COLORS = {
    'brand_orange': (255, 140, 0),      # #FF8C00
    'brand_blue': (30, 90, 142),        # #1E5A8E
    'dark_blue': (13, 44, 74),          # #0D2C4A
    'blueprint_blue': (42, 95, 142),    # #2A5F8E
    'white': (255, 255, 255),           # #FFFFFF
    'black': (26, 26, 26)               # #1A1A1A
}
```

### Typography Guidelines

```python
TYPOGRAPHY = {
    'title': {
        'font': 'Montserrat-Black.ttf',  # or Inter-Bold, Poppins-Bold
        'size_large': 72,
        'size_medium': 48,
        'size_small': 36,
        'color': 'brand_orange',
        'case': 'lowercase'
    },
    'subtitle': {
        'font': 'Montserrat-Regular.ttf',
        'size_large': 36,
        'size_medium': 24,
        'size_small': 18,
        'color': 'white',
        'style': 'italic'
    },
    'body': {
        'font': 'Montserrat-Regular.ttf',
        'size': 20,
        'color': 'white'
    }
}
```

### Blueprint Pattern Generation

The blueprint pattern creates a technical, schematic background using:
- Grid lines (vertical and horizontal)
- Circuit-style connection dots
- Technical diagram elements
- 20-30% opacity overlay
- Color: Light blue on darker blue

### Asset References

All brand assets are located in `assets/` directory:
- Logo icon (with/without background)
- Full logo with title and tagline
- Banner variants
- Multiple size variants

## Examples

### Example 1: Newsletter Header

**Input:**
```
Create a Beehiiv header for our weekly newsletter about AI automation in manufacturing.
Title: AI in Manufacturing
Subtitle: This Week's Automation Insights
```

**Output:**
- 1200x600px PNG
- Blue blueprint background
- "boring business AI" logo in top left
- "AI in Manufacturing" in large orange text, centered
- Subtitle in white below title
- Optimized for email display

### Example 2: Skool Course Cover

**Input:**
```
Create a Skool cover for:
Course: AI Operations Fundamentals
Subtitle: From Setup to Scale
```

**Output:**
- 1280x720px PNG
- Logo in bottom left corner
- "AI Operations Fundamentals" in large white text, centered
- "From Setup to Scale" in smaller white text below
- Blueprint background with high contrast
- Thumbnail-readable

### Example 3: LinkedIn Post

**Input:**
```
Create a LinkedIn post image with:
Message: 78% of businesses still struggle with AI implementation
Style: stat card
```

**Output:**
- 1200x627px PNG
- Large "78%" in orange, centered
- Supporting text in white
- Logo watermark in corner
- Blueprint background
- High engagement visual style

### Example 4: Social Media Profile

**Input:**
```
Create a square profile picture for Twitter using the AI OPS character.
```

**Output:**
- 400x400px PNG
- AI OPS character centered
- Blue background (or transparent)
- High contrast, recognizable at small sizes

## Best Practices

### 1. Text Readability
- Always ensure high contrast between text and background
- Use white text on blue backgrounds
- Use orange for emphasis and CTAs
- Avoid placing text over busy areas of the pattern

### 2. Logo Usage
- Always maintain clear space around logo
- Never distort or stretch
- Use appropriate size variant for layout
- Icon-only for small applications (profile pics)

### 3. Brand Consistency
- Always use lowercase for brand name
- Maintain color palette across all materials
- Use blueprint pattern for professional/technical content
- Keep tagline visible in primary brand applications

### 4. Platform Optimization
- Size appropriately for each platform
- Optimize file size for web (use PNG for transparency, JPEG for photos)
- Test thumbnail visibility for course covers
- Ensure mobile readability

### 5. Layout Balance
- Don't overcrowd the design
- Give elements room to breathe
- Use rule of thirds for placement
- Balance text and visual elements

## Troubleshooting

**Issue: Text is hard to read**
- Solution: Increase contrast, add subtle shadow, or place text on solid color overlay

**Issue: Logo too small in thumbnails**
- Solution: Use icon-only variant at larger size, or switch to layout with prominent logo

**Issue: File size too large for email**
- Solution: Reduce dimensions to 600x400px for Beehiiv, or optimize JPEG quality

**Issue: Colors don't match brand**
- Solution: Use exact hex values from brand guidelines, don't eyeball colors

**Issue: Pattern too busy**
- Solution: Reduce pattern opacity to 20%, or use solid blue background

## Technical Requirements

### Python Dependencies

```bash
pip install Pillow  # Image manipulation
pip install numpy   # Pattern generation
```

### Fonts Required

Download and install:
- Montserrat (Black, Bold, Regular)
- Inter (Bold, Regular) - Alternative
- Poppins (Bold, Regular) - Alternative

Or use system fonts:
- Arial Black (fallback for titles)
- Arial (fallback for body)

## Asset Management

### Adding New Assets

1. Place new assets in `assets/` directory
2. Use naming convention: `boringbusiness-[type]-[variant].png`
3. Update asset references in generation scripts
4. Test across all generator templates

### Updating Brand Guidelines

1. Edit `BRAND_GUIDELINES.md`
2. Update color values in generation scripts
3. Test all templates with new specifications
4. Document changes in version history

## Version History

**v1.0** (October 2025)
- Initial skill creation
- Brand guidelines documentation
- Core asset library
- Beehiiv header generator
- Skool cover generator
- Social media image generator
- General purpose image generator

## Related Skills

- `canvas-design`: For interactive canvas-based designs
- `theme-factory`: For exploring color theme variations
- `slack-gif-creator`: For animated branded GIFs
- `social-brand`: For general social media branding

## Support

For questions, custom layouts, or new platform support:
1. Refer to `BRAND_GUIDELINES.md` for visual specifications
2. Check asset library in `assets/` directory
3. Review example outputs in `examples/` directory
4. Consult technical documentation in `scripts/` directory

---

**Skill Type:** Brand Management & Image Generation
**Category:** Design, Marketing, Content Creation
**Complexity:** Intermediate
**Dependencies:** PIL/Pillow, NumPy
**Asset Library:** Included (7 logo variants)
