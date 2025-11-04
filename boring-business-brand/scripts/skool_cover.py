#!/usr/bin/env python3
"""
Skool Course Cover Generator
Creates professional course covers for Skool platform with Boring Business AI branding
"""

from brand_generator import BrandImageGenerator
from PIL import Image, ImageDraw
from typing import Optional, List


class SkoolCoverGenerator(BrandImageGenerator):
    """Generate Skool course covers with consistent branding"""

    def generate_cover(
        self,
        course_title: str,
        subtitle: Optional[str] = None,
        key_points: Optional[List[str]] = None,
        layout: str = 'corner-logo',
        size: str = 'hd',
        output_path: str = 'skool_cover.png'
    ) -> Image.Image:
        """
        Generate a Skool course cover

        Args:
            course_title: Main course title
            subtitle: Optional subtitle or tagline
            key_points: Optional list of key points/topics (max 4)
            layout: Layout style ('corner-logo', 'split', 'overlay', 'banner')
            size: Size preset ('hd' = 1280x720, 'fhd' = 1920x1080)
            output_path: Output file path

        Returns:
            Generated PIL Image
        """
        # Determine dimensions
        dimensions = {
            'hd': (1280, 720),
            'fhd': (1920, 1080)
        }
        width, height = dimensions.get(size, dimensions['hd'])

        # Create blueprint background
        img = self.create_blueprint_background(width, height)

        # Generate based on layout
        if layout == 'corner-logo':
            img = self._layout_corner_logo(img, course_title, subtitle, key_points)
        elif layout == 'split':
            img = self._layout_split(img, course_title, subtitle, key_points)
        elif layout == 'overlay':
            img = self._layout_overlay(img, course_title, subtitle, key_points)
        elif layout == 'banner':
            img = self._layout_banner(img, course_title, subtitle, key_points)
        else:
            img = self._layout_corner_logo(img, course_title, subtitle, key_points)

        # Save optimized
        self.save_optimized(img, output_path, format='PNG', optimize=True)

        return img

    def _layout_corner_logo(
        self,
        img: Image.Image,
        course_title: str,
        subtitle: Optional[str],
        key_points: Optional[List[str]]
    ) -> Image.Image:
        """Logo in corner, title centered"""
        width, height = img.size
        draw = ImageDraw.Draw(img)

        # Add logo in bottom left corner
        img = self.add_logo(
            img,
            position='bottom-left',
            logo_type='icon_nobg',
            max_width=180,
            max_height=180,
            margin=40
        )

        # Title - centered and large
        title_size = 72 if width >= 1500 else 56
        title_font = self.get_font(title_size, bold=True)

        max_width = int(width * 0.75)
        title_lines = self.wrap_text(course_title.upper(), title_font, max_width)

        # Calculate vertical positioning
        title_height = len(title_lines) * (title_size + 15)
        subtitle_height = 0
        keypoints_height = 0

        if subtitle:
            subtitle_size = 36 if width >= 1500 else 28
            subtitle_height = subtitle_size + 25

        if key_points:
            keypoint_size = 28 if width >= 1500 else 22
            keypoints_height = len(key_points) * (keypoint_size + 12) + 30

        total_height = title_height + subtitle_height + keypoints_height
        start_y = (height - total_height) // 2

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
                outline_width=4
            )
            current_y += title_size + 15

        # Draw subtitle
        if subtitle:
            current_y += 20
            subtitle_size = 36 if width >= 1500 else 28
            subtitle_font = self.get_font(subtitle_size)

            subtitle_width, _ = self.get_text_size(subtitle.lower(), subtitle_font)
            x = (width - subtitle_width) // 2

            draw.text(
                (x, current_y),
                subtitle.lower(),
                font=subtitle_font,
                fill=self.colors['white']
            )
            current_y += subtitle_size + 25

        # Draw key points
        if key_points:
            current_y += 30
            keypoint_size = 28 if width >= 1500 else 22
            keypoint_font = self.get_font(keypoint_size)

            for i, point in enumerate(key_points[:4], 1):  # Max 4 points
                bullet_text = f"• {point}"
                bullet_width, _ = self.get_text_size(bullet_text, keypoint_font)
                x = (width - bullet_width) // 2

                draw.text(
                    (x, current_y),
                    bullet_text,
                    font=keypoint_font,
                    fill=self.colors['white']
                )
                current_y += keypoint_size + 12

        return img

    def _layout_split(
        self,
        img: Image.Image,
        course_title: str,
        subtitle: Optional[str],
        key_points: Optional[List[str]]
    ) -> Image.Image:
        """Split layout: logo left, text right"""
        width, height = img.size
        draw = ImageDraw.Draw(img)

        # Logo takes up left third
        logo_width = width // 3

        # Add logo on left side (vertically centered)
        img = self.add_logo(
            img,
            position='center-left',
            logo_type='icon_nobg',
            max_width=int(logo_width * 0.8),
            max_height=int(height * 0.6),
            margin=40
        )

        # Text area
        text_start_x = logo_width + 40
        text_width = width - text_start_x - 60

        # Title
        title_size = 64 if width >= 1500 else 48
        title_font = self.get_font(title_size, bold=True)

        title_lines = self.wrap_text(course_title.upper(), title_font, text_width)

        # Calculate vertical centering
        title_height = len(title_lines) * (title_size + 12)
        subtitle_height = 0
        keypoints_height = 0

        if subtitle:
            subtitle_size = 32 if width >= 1500 else 24
            subtitle_height = subtitle_size + 25

        if key_points:
            keypoint_size = 26 if width >= 1500 else 20
            keypoints_height = len(key_points) * (keypoint_size + 10) + 30

        total_height = title_height + subtitle_height + keypoints_height
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
                outline_width=3
            )
            current_y += title_size + 12

        # Draw subtitle
        if subtitle:
            current_y += 15
            subtitle_size = 32 if width >= 1500 else 24
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

        # Draw key points
        if key_points:
            current_y += 25
            keypoint_size = 26 if width >= 1500 else 20
            keypoint_font = self.get_font(keypoint_size)

            for point in key_points[:4]:
                bullet_text = f"• {point}"
                draw.text(
                    (text_start_x, current_y),
                    bullet_text,
                    font=keypoint_font,
                    fill=self.colors['white']
                )
                current_y += keypoint_size + 10

        return img

    def _layout_overlay(
        self,
        img: Image.Image,
        course_title: str,
        subtitle: Optional[str],
        key_points: Optional[List[str]]
    ) -> Image.Image:
        """Logo watermark with centered text"""
        width, height = img.size
        draw = ImageDraw.Draw(img)

        # Add logo as watermark in center
        if self.logo_icon_nobg:
            logo = self.logo_icon_nobg.copy()

            # Make it semi-transparent and large
            logo_size = int(min(width, height) * 0.6)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            # Reduce opacity
            alpha = logo.split()[-1]
            alpha = alpha.point(lambda p: int(p * 0.15))
            logo.putalpha(alpha)

            # Center it
            logo_x = (width - logo_size) // 2
            logo_y = (height - logo_size) // 2

            img.paste(logo, (logo_x, logo_y), logo)

        # Title - large and centered over watermark
        title_size = 80 if width >= 1500 else 60
        title_font = self.get_font(title_size, bold=True)

        max_width = int(width * 0.8)
        title_lines = self.wrap_text(course_title.upper(), title_font, max_width)

        # Calculate positioning
        title_height = len(title_lines) * (title_size + 15)
        subtitle_height = 0

        if subtitle:
            subtitle_size = 40 if width >= 1500 else 30
            subtitle_height = subtitle_size + 30

        total_height = title_height + subtitle_height
        start_y = (height - total_height) // 2

        # Draw title with strong outline for visibility
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
                outline_width=5
            )
            current_y += title_size + 15

        # Draw subtitle
        if subtitle:
            current_y += 25
            subtitle_size = 40 if width >= 1500 else 30
            subtitle_font = self.get_font(subtitle_size)

            subtitle_lines = self.wrap_text(subtitle.lower(), subtitle_font, max_width)
            for line in subtitle_lines:
                line_width, _ = self.get_text_size(line, subtitle_font)
                x = (width - line_width) // 2

                self.draw_text_with_outline(
                    draw,
                    (x, current_y),
                    line,
                    subtitle_font,
                    self.colors['white'],
                    outline_width=3
                )
                current_y += subtitle_size + 5

        return img

    def _layout_banner(
        self,
        img: Image.Image,
        course_title: str,
        subtitle: Optional[str],
        key_points: Optional[List[str]]
    ) -> Image.Image:
        """Banner style with logo and text in horizontal strip"""
        width, height = img.size
        draw = ImageDraw.Draw(img)

        # Create semi-transparent banner across middle
        banner_height = int(height * 0.4)
        banner_y = (height - banner_height) // 2

        # Draw banner overlay
        overlay = Image.new('RGBA', (width, banner_height), (*self.colors['dark_blue'], 220))
        img.paste(overlay, (0, banner_y), overlay)

        # Add small logo on left of banner
        logo_size = int(banner_height * 0.7)
        img = self.add_logo(
            img,
            position='center-left',
            logo_type='icon_nobg',
            max_width=logo_size,
            max_height=logo_size,
            margin=50
        )

        # Text area
        text_start_x = logo_size + 120
        text_width = width - text_start_x - 60

        # Title
        title_size = 58 if width >= 1500 else 44
        title_font = self.get_font(title_size, bold=True)

        title_lines = self.wrap_text(course_title.upper(), title_font, text_width)

        # Calculate vertical centering within banner
        title_height = len(title_lines) * (title_size + 10)
        subtitle_height = 0

        if subtitle:
            subtitle_size = 30 if width >= 1500 else 24
            subtitle_height = subtitle_size + 15

        total_height = title_height + subtitle_height
        text_start_y = banner_y + (banner_height - total_height) // 2

        # Draw title
        current_y = text_start_y
        for line in title_lines:
            draw.text(
                (text_start_x, current_y),
                line,
                font=title_font,
                fill=self.colors['brand_orange']
            )
            current_y += title_size + 10

        # Draw subtitle
        if subtitle:
            current_y += 10
            subtitle_size = 30 if width >= 1500 else 24
            subtitle_font = self.get_font(subtitle_size)

            draw.text(
                (text_start_x, current_y),
                subtitle.lower(),
                font=subtitle_font,
                fill=self.colors['white']
            )

        return img


def main():
    """Example usage"""
    print("Boring Business AI - Skool Course Cover Generator")
    print("=" * 60)

    generator = SkoolCoverGenerator()

    # Example 1: Corner logo layout
    print("\n1. Generating corner-logo course cover...")
    generator.generate_cover(
        course_title="AI Operations Fundamentals",
        subtitle="From Setup to Scale",
        key_points=[
            "Practical Implementation",
            "Real-World Case Studies",
            "Measurable ROI",
            "Hands-On Projects"
        ],
        layout='corner-logo',
        size='hd',
        output_path='skool_corner.png'
    )

    # Example 2: Split layout
    print("\n2. Generating split layout course cover...")
    generator.generate_cover(
        course_title="Boring Business AI Masterclass",
        subtitle="Real AI for Real Business",
        layout='split',
        size='hd',
        output_path='skool_split.png'
    )

    # Example 3: Overlay layout
    print("\n3. Generating overlay course cover...")
    generator.generate_cover(
        course_title="Advanced AI Automation",
        subtitle="Scale Your Operations with AI",
        layout='overlay',
        size='hd',
        output_path='skool_overlay.png'
    )

    # Example 4: Banner layout
    print("\n4. Generating banner course cover...")
    generator.generate_cover(
        course_title="AI Implementation Bootcamp",
        subtitle="4-Week Intensive Program",
        layout='banner',
        size='hd',
        output_path='skool_banner.png'
    )

    print("\n✓ All Skool course covers generated successfully!")
    print("\nGenerated files:")
    print("  - skool_corner.png")
    print("  - skool_split.png")
    print("  - skool_overlay.png")
    print("  - skool_banner.png")


if __name__ == '__main__':
    main()
