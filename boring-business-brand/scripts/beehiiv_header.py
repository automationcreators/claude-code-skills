#!/usr/bin/env python3
"""
Beehiiv Email Header Generator
Creates optimized email newsletter headers for Boring Business AI
"""

from brand_generator import BrandImageGenerator
from PIL import Image, ImageDraw
from typing import Optional


class BeehiivHeaderGenerator(BrandImageGenerator):
    """Generate Beehiiv email headers with consistent branding"""

    def generate_header(
        self,
        title: str,
        subtitle: Optional[str] = None,
        layout: str = 'centered',
        size: str = 'large',
        output_path: str = 'beehiiv_header.png'
    ) -> Image.Image:
        """
        Generate a Beehiiv email header

        Args:
            title: Main title text
            subtitle: Optional subtitle text
            layout: Layout style ('centered', 'left', 'minimal')
            size: Size preset ('large' = 1200x600, 'medium' = 600x400)
            output_path: Output file path

        Returns:
            Generated PIL Image
        """
        # Determine dimensions
        dimensions = {
            'large': (1200, 600),
            'medium': (600, 400)
        }
        width, height = dimensions.get(size, dimensions['large'])

        # Create blueprint background
        img = self.create_blueprint_background(width, height)
        draw = ImageDraw.Draw(img)

        # Generate based on layout
        if layout == 'centered':
            img = self._layout_centered(img, title, subtitle)
        elif layout == 'left':
            img = self._layout_left(img, title, subtitle)
        elif layout == 'minimal':
            img = self._layout_minimal(img, title, subtitle)
        else:
            img = self._layout_centered(img, title, subtitle)

        # Save optimized
        self.save_optimized(img, output_path, format='PNG', optimize=True)

        return img

    def _layout_centered(
        self,
        img: Image.Image,
        title: str,
        subtitle: Optional[str]
    ) -> Image.Image:
        """Centered layout with logo and text"""
        width, height = img.size
        draw = ImageDraw.Draw(img)

        # Add logo at top center
        img = self.add_logo(
            img,
            position='top-center',
            logo_type='icon_nobg',
            max_width=150,
            max_height=150,
            margin=30
        )

        # Calculate vertical spacing
        logo_height = 150 + 30  # logo height + margin
        available_height = height - logo_height - 40

        # Title font
        title_size = 64 if width >= 1000 else 42
        title_font = self.get_font(title_size, bold=True)

        # Wrap title if needed
        max_title_width = int(width * 0.85)
        title_lines = self.wrap_text(title.lower(), title_font, max_title_width)

        # Calculate title block height
        title_height = len(title_lines) * (title_size + 10)

        # Starting Y position for title
        start_y = logo_height + (available_height - title_height) // 2

        if subtitle:
            subtitle_size = 28 if width >= 1000 else 20
            subtitle_font = self.get_font(subtitle_size)
            subtitle_height = subtitle_size + 20
            start_y -= subtitle_height // 2

        # Draw title lines
        current_y = start_y
        for line in title_lines:
            line_width, _ = self.get_text_size(line, title_font)
            x = (width - line_width) // 2

            self.draw_text_with_outline(
                draw,
                (x, current_y),
                line,
                title_font,
                self.colors['brand_orange'],
                outline_width=3
            )
            current_y += title_size + 10

        # Draw subtitle if provided
        if subtitle:
            subtitle_size = 28 if width >= 1000 else 20
            subtitle_font = self.get_font(subtitle_size)

            subtitle_lines = self.wrap_text(
                subtitle.lower(),
                subtitle_font,
                max_title_width
            )

            current_y += 15
            for line in subtitle_lines:
                line_width, _ = self.get_text_size(line, subtitle_font)
                x = (width - line_width) // 2

                draw.text(
                    (x, current_y),
                    line,
                    font=subtitle_font,
                    fill=self.colors['white']
                )
                current_y += subtitle_size + 5

        return img

    def _layout_left(
        self,
        img: Image.Image,
        title: str,
        subtitle: Optional[str]
    ) -> Image.Image:
        """Left-aligned layout with logo and text"""
        width, height = img.size
        draw = ImageDraw.Draw(img)

        margin = 50

        # Add logo on left side
        img = self.add_logo(
            img,
            position='center-left',
            logo_type='icon_nobg',
            max_width=200,
            max_height=200,
            margin=margin
        )

        # Text area starts after logo
        text_start_x = 200 + margin * 2
        text_width = width - text_start_x - margin

        # Title
        title_size = 56 if width >= 1000 else 36
        title_font = self.get_font(title_size, bold=True)

        title_lines = self.wrap_text(title.lower(), title_font, text_width)

        # Calculate vertical centering
        title_height = len(title_lines) * (title_size + 10)
        subtitle_height = 0

        if subtitle:
            subtitle_size = 24 if width >= 1000 else 18
            subtitle_font = self.get_font(subtitle_size)
            subtitle_lines = self.wrap_text(subtitle.lower(), subtitle_font, text_width)
            subtitle_height = len(subtitle_lines) * (subtitle_size + 5) + 20

        total_height = title_height + subtitle_height
        start_y = (height - total_height) // 2

        # Draw title
        current_y = start_y
        for line in title_lines:
            self.draw_text_with_outline(
                draw,
                (text_start_x, current_y),
                line,
                title_font,
                self.colors['brand_orange'],
                outline_width=2
            )
            current_y += title_size + 10

        # Draw subtitle
        if subtitle:
            current_y += 10
            subtitle_size = 24 if width >= 1000 else 18
            subtitle_font = self.get_font(subtitle_size)
            subtitle_lines = self.wrap_text(subtitle.lower(), subtitle_font, text_width)

            for line in subtitle_lines:
                draw.text(
                    (text_start_x, current_y),
                    line,
                    font=subtitle_font,
                    fill=self.colors['white']
                )
                current_y += subtitle_size + 5

        return img

    def _layout_minimal(
        self,
        img: Image.Image,
        title: str,
        subtitle: Optional[str]
    ) -> Image.Image:
        """Minimal layout with just icon and large title"""
        width, height = img.size
        draw = ImageDraw.Draw(img)

        # Small icon in top left
        img = self.add_logo(
            img,
            position='top-left',
            logo_type='icon_nobg',
            max_width=100,
            max_height=100,
            margin=30
        )

        # Large centered title
        title_size = 72 if width >= 1000 else 48
        title_font = self.get_font(title_size, bold=True)

        max_width = int(width * 0.8)
        title_lines = self.wrap_text(title.lower(), title_font, max_width)

        # Calculate centering
        title_height = len(title_lines) * (title_size + 15)
        start_y = (height - title_height) // 2

        if subtitle:
            subtitle_size = 30 if width >= 1000 else 22
            subtitle_font = self.get_font(subtitle_size)
            subtitle_height = subtitle_size + 20
            start_y = (height - title_height - subtitle_height) // 2

        # Draw title
        current_y = start_y
        for line in title_lines:
            line_width, _ = self.get_text_size(line, title_font)
            x = (width - line_width) // 2

            self.draw_text_with_outline(
                draw,
                (x, current_y),
                line,
                title_font,
                self.colors['brand_orange'],
                outline_width=3
            )
            current_y += title_size + 15

        # Draw subtitle
        if subtitle:
            current_y += 20
            subtitle_size = 30 if width >= 1000 else 22
            subtitle_font = self.get_font(subtitle_size)

            subtitle_width, _ = self.get_text_size(subtitle.lower(), subtitle_font)
            x = (width - subtitle_width) // 2

            draw.text(
                (x, current_y),
                subtitle.lower(),
                font=subtitle_font,
                fill=self.colors['white']
            )

        return img


def main():
    """Example usage"""
    print("Boring Business AI - Beehiiv Header Generator")
    print("=" * 60)

    generator = BeehiivHeaderGenerator()

    # Example 1: Centered layout
    print("\n1. Generating centered header...")
    generator.generate_header(
        title="AI in Manufacturing",
        subtitle="This Week's Automation Insights",
        layout='centered',
        size='large',
        output_path='beehiiv_centered.png'
    )

    # Example 2: Left-aligned layout
    print("\n2. Generating left-aligned header...")
    generator.generate_header(
        title="The Boring Business AI Weekly",
        subtitle="Real AI. Real Results.",
        layout='left',
        size='large',
        output_path='beehiiv_left.png'
    )

    # Example 3: Minimal layout
    print("\n3. Generating minimal header...")
    generator.generate_header(
        title="AI Operations Update",
        subtitle="October 2025",
        layout='minimal',
        size='large',
        output_path='beehiiv_minimal.png'
    )

    print("\n✓ All Beehiiv headers generated successfully!")
    print("\nGenerated files:")
    print("  - beehiiv_centered.png")
    print("  - beehiiv_left.png")
    print("  - beehiiv_minimal.png")


if __name__ == '__main__':
    main()
