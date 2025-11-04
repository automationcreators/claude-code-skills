#!/usr/bin/env python3
"""
Boring Business AI - Core Brand Image Generator
Provides shared functionality for all image generation sub-skills
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
from pathlib import Path
from typing import Tuple, Optional, Dict, List
import math

# Brand Colors (RGB)
COLORS = {
    'brand_orange': (255, 140, 0),      # #FF8C00
    'brand_blue': (30, 90, 142),        # #1E5A8E
    'dark_blue': (13, 44, 74),          # #0D2C4A
    'blueprint_blue': (42, 95, 142),    # #2A5F8E
    'white': (255, 255, 255),           # #FFFFFF
    'black': (26, 26, 26),              # #1A1A1A
    'pattern_blue': (52, 105, 162)      # For blueprint lines
}

class BrandImageGenerator:
    """Core brand image generation functionality"""

    def __init__(self, assets_dir: str = None):
        """
        Initialize the brand image generator

        Args:
            assets_dir: Path to assets directory (defaults to ../assets)
        """
        if assets_dir is None:
            # Get path relative to this script
            script_dir = Path(__file__).parent
            assets_dir = script_dir.parent / 'assets'

        self.assets_dir = Path(assets_dir)
        self.colors = COLORS

        # Load logo assets
        self.logo_icon_nobg = None
        self.logo_icon_bg = None
        self.logo_full = None
        self.banner = None

        self._load_assets()

    def _load_assets(self):
        """Load all brand assets from the assets directory"""
        try:
            # Load available logo variants
            logo_files = {
                'icon_nobg': 'logo icon no bg.png',
                'icon_bg': 'logo icon.png',
                'full': 'med logo title subtitle w_bg.png',
                'banner': 'banner with subtitle.png'
            }

            for key, filename in logo_files.items():
                filepath = self.assets_dir / filename
                if filepath.exists():
                    img = Image.open(filepath).convert('RGBA')
                    setattr(self, f'logo_{key}', img)
                    print(f"✓ Loaded: {filename}")

        except Exception as e:
            print(f"Warning: Could not load some assets: {e}")

    def create_blueprint_background(
        self,
        width: int,
        height: int,
        grid_size: int = 40,
        opacity: int = 50
    ) -> Image.Image:
        """
        Create a technical blueprint-style background pattern

        Args:
            width: Image width in pixels
            height: Image height in pixels
            grid_size: Size of grid squares in pixels
            opacity: Opacity of pattern lines (0-255)

        Returns:
            PIL Image with blueprint pattern
        """
        # Create base blue background
        img = Image.new('RGBA', (width, height), self.colors['brand_blue'])

        # Create overlay for pattern
        pattern = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(pattern)

        line_color = (*self.colors['pattern_blue'], opacity)

        # Draw grid lines
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill=line_color, width=1)

        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill=line_color, width=1)

        # Draw diagonal technical lines
        for x in range(0, width, grid_size * 3):
            for y in range(0, height, grid_size * 3):
                # Small circuit board style connections
                draw.rectangle(
                    [x - 2, y - 2, x + 2, y + 2],
                    fill=line_color
                )

                # Connecting lines
                if x + grid_size * 3 < width:
                    draw.line(
                        [(x, y), (x + grid_size, y)],
                        fill=line_color,
                        width=1
                    )

        # Add some technical diagram elements
        for i in range(0, width, grid_size * 5):
            for j in range(0, height, grid_size * 5):
                # Rounded corner boxes (like chip diagrams)
                box_size = grid_size * 2
                if i + box_size < width and j + box_size < height:
                    draw.rounded_rectangle(
                        [i, j, i + box_size, j + box_size],
                        radius=5,
                        outline=line_color,
                        width=1
                    )

        # Composite pattern onto background
        img = Image.alpha_composite(img.convert('RGBA'), pattern)

        return img

    def get_font(
        self,
        size: int,
        bold: bool = False,
        fallback_only: bool = False
    ) -> ImageFont.FreeTypeFont:
        """
        Get a font for text rendering

        Args:
            size: Font size in points
            bold: Use bold weight
            fallback_only: Skip trying custom fonts, use system fallback

        Returns:
            PIL ImageFont object
        """
        if not fallback_only:
            # Try to use Montserrat (ideal brand font)
            font_names = [
                'Montserrat-Black.ttf' if bold else 'Montserrat-Regular.ttf',
                'Montserrat-Bold.ttf' if bold else 'Montserrat-Regular.ttf',
                'Inter-Bold.ttf' if bold else 'Inter-Regular.ttf',
                'Poppins-Bold.ttf' if bold else 'Poppins-Regular.ttf',
            ]

            for font_name in font_names:
                try:
                    return ImageFont.truetype(font_name, size)
                except:
                    continue

        # Fallback to system fonts
        system_fonts = [
            '/System/Library/Fonts/Helvetica.ttc',
            '/System/Library/Fonts/SFNSDisplay.ttf',
            'Arial.ttf',
            'arial.ttf'
        ]

        weight = 'Bold' if bold else ''
        for font_path in system_fonts:
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue

        # Last resort: default font
        return ImageFont.load_default()

    def draw_text_with_outline(
        self,
        draw: ImageDraw.ImageDraw,
        position: Tuple[int, int],
        text: str,
        font: ImageFont.FreeTypeFont,
        fill_color: Tuple[int, int, int],
        outline_color: Tuple[int, int, int] = None,
        outline_width: int = 2
    ):
        """
        Draw text with an outline for better readability

        Args:
            draw: ImageDraw object
            position: (x, y) tuple for text position
            text: Text to draw
            font: Font to use
            fill_color: Main text color
            outline_color: Outline color (defaults to black)
            outline_width: Width of outline in pixels
        """
        if outline_color is None:
            outline_color = self.colors['black']

        x, y = position

        # Draw outline
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                if adj_x != 0 or adj_y != 0:
                    draw.text(
                        (x + adj_x, y + adj_y),
                        text,
                        font=font,
                        fill=outline_color
                    )

        # Draw main text
        draw.text(position, text, font=font, fill=fill_color)

    def add_logo(
        self,
        img: Image.Image,
        position: str = 'top-left',
        logo_type: str = 'full',
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        margin: int = 40
    ) -> Image.Image:
        """
        Add logo to an image

        Args:
            img: Base image to add logo to
            position: Position string ('top-left', 'center', 'bottom-right', etc.)
            logo_type: Type of logo ('icon_nobg', 'icon_bg', 'full', 'banner')
            max_width: Maximum logo width (scales down if needed)
            max_height: Maximum logo height (scales down if needed)
            margin: Margin from edges in pixels

        Returns:
            Image with logo composited
        """
        # Get the requested logo
        logo = getattr(self, f'logo_{logo_type}', None)

        if logo is None:
            print(f"Warning: Logo type '{logo_type}' not available")
            return img

        # Resize logo if max dimensions specified
        logo_resized = logo.copy()

        if max_width or max_height:
            logo_w, logo_h = logo.size
            scale = 1.0

            if max_width and logo_w > max_width:
                scale = min(scale, max_width / logo_w)

            if max_height and logo_h > max_height:
                scale = min(scale, max_height / logo_h)

            if scale < 1.0:
                new_size = (int(logo_w * scale), int(logo_h * scale))
                logo_resized = logo.resize(new_size, Image.Resampling.LANCZOS)

        logo_w, logo_h = logo_resized.size
        img_w, img_h = img.size

        # Calculate position
        positions = {
            'top-left': (margin, margin),
            'top-center': ((img_w - logo_w) // 2, margin),
            'top-right': (img_w - logo_w - margin, margin),
            'center-left': (margin, (img_h - logo_h) // 2),
            'center': ((img_w - logo_w) // 2, (img_h - logo_h) // 2),
            'center-right': (img_w - logo_w - margin, (img_h - logo_h) // 2),
            'bottom-left': (margin, img_h - logo_h - margin),
            'bottom-center': ((img_w - logo_w) // 2, img_h - logo_h - margin),
            'bottom-right': (img_w - logo_w - margin, img_h - logo_h - margin),
        }

        x, y = positions.get(position, positions['top-left'])

        # Composite logo onto image
        img_copy = img.copy()
        img_copy.paste(logo_resized, (x, y), logo_resized)

        return img_copy

    def wrap_text(
        self,
        text: str,
        font: ImageFont.FreeTypeFont,
        max_width: int
    ) -> List[str]:
        """
        Wrap text to fit within a maximum width

        Args:
            text: Text to wrap
            font: Font being used
            max_width: Maximum width in pixels

        Returns:
            List of text lines
        """
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]

            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def get_text_size(
        self,
        text: str,
        font: ImageFont.FreeTypeFont
    ) -> Tuple[int, int]:
        """
        Get the size of rendered text

        Args:
            text: Text to measure
            font: Font to use

        Returns:
            (width, height) tuple
        """
        # Create temporary image to measure text
        temp_img = Image.new('RGBA', (1, 1))
        draw = ImageDraw.Draw(temp_img)
        bbox = draw.textbbox((0, 0), text, font=font)

        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        return (width, height)

    def save_optimized(
        self,
        img: Image.Image,
        filepath: str,
        format: str = 'PNG',
        quality: int = 90,
        optimize: bool = True
    ):
        """
        Save image with optimization

        Args:
            img: Image to save
            filepath: Output file path
            format: Image format ('PNG', 'JPEG')
            quality: JPEG quality (1-100)
            optimize: Whether to optimize file size
        """
        if format.upper() == 'JPEG':
            # Convert to RGB for JPEG
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, self.colors['white'])
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1])
                img = background

            img.save(filepath, format='JPEG', quality=quality, optimize=optimize)
        else:
            img.save(filepath, format='PNG', optimize=optimize)

        print(f"✓ Saved: {filepath}")


if __name__ == '__main__':
    # Test the generator
    print("Boring Business AI - Brand Image Generator")
    print("=" * 50)

    gen = BrandImageGenerator()

    # Test blueprint background
    print("\nGenerating test blueprint background...")
    bg = gen.create_blueprint_background(1200, 600)
    bg.save('test_blueprint.png')
    print("✓ Created: test_blueprint.png")

    # Test logo placement
    print("\nTesting logo placement...")
    bg_with_logo = gen.add_logo(bg, position='center', logo_type='full', max_width=400)
    bg_with_logo.save('test_logo_placement.png')
    print("✓ Created: test_logo_placement.png")

    print("\n✓ Core generator tests complete!")
