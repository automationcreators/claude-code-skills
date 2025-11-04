#!/usr/bin/env python3
"""
Social Media Image Generator
Creates platform-specific social media images for Boring Business AI
"""

from brand_generator import BrandImageGenerator
from PIL import Image, ImageDraw
from typing import Optional, Dict


# Platform specifications
PLATFORM_SIZES = {
    'twitter': {
        'profile': (400, 400),
        'header': (1500, 500),
        'post': (1200, 675)
    },
    'linkedin': {
        'profile': (400, 400),
        'banner': (1584, 396),
        'post': (1200, 627)
    },
    'facebook': {
        'profile': (180, 180),
        'cover': (820, 312),
        'post': (1200, 630)
    },
    'instagram': {
        'profile': (320, 320),
        'square': (1080, 1080),
        'portrait': (1080, 1350),
        'landscape': (1080, 566)
    }
}


class SocialMediaGenerator(BrandImageGenerator):
    """Generate social media images for multiple platforms"""

    def generate_post(
        self,
        message: str,
        platform: str = 'instagram',
        style: str = 'quote',
        size_type: str = 'square',
        include_logo: bool = True,
        output_path: str = 'social_post.png'
    ) -> Image.Image:
        """
        Generate a social media post image

        Args:
            message: Main message/text for the post
            platform: Platform name ('instagram', 'twitter', 'linkedin', 'facebook')
            style: Post style ('quote', 'announcement', 'tip', 'stat')
            size_type: Size variant ('square', 'post', 'portrait', 'landscape')
            include_logo: Whether to include logo
            output_path: Output file path

        Returns:
            Generated PIL Image
        """
        # Get dimensions for platform
        platform_lower = platform.lower()
        if platform_lower not in PLATFORM_SIZES:
            print(f"Unknown platform '{platform}', using Instagram")
            platform_lower = 'instagram'

        sizes = PLATFORM_SIZES[platform_lower]
        if size_type not in sizes:
            # Use first available size
            size_type = list(sizes.keys())[0]

        width, height = sizes[size_type]

        # Create blueprint background
        img = self.create_blueprint_background(width, height)

        # Generate based on style
        if style == 'quote':
            img = self._style_quote(img, message, include_logo)
        elif style == 'announcement':
            img = self._style_announcement(img, message, include_logo)
        elif style == 'tip':
            img = self._style_tip(img, message, include_logo)
        elif style == 'stat':
            img = self._style_stat(img, message, include_logo)
        else:
            img = self._style_quote(img, message, include_logo)

        # Save optimized
        self.save_optimized(img, output_path, format='PNG', optimize=True)

        return img

    def generate_profile(
        self,
        platform: str = 'instagram',
        output_path: str = 'profile.png'
    ) -> Image.Image:
        """
        Generate a profile picture for a platform

        Args:
            platform: Platform name
            output_path: Output file path

        Returns:
            Generated PIL Image
        """
        platform_lower = platform.lower()
        if platform_lower not in PLATFORM_SIZES:
            platform_lower = 'instagram'

        width, height = PLATFORM_SIZES[platform_lower]['profile']

        # Create blueprint background
        img = self.create_blueprint_background(width, height)

        # Add centered logo icon
        img = self.add_logo(
            img,
            position='center',
            logo_type='icon_nobg',
            max_width=int(width * 0.8),
            max_height=int(height * 0.8)
        )

        # Save optimized
        self.save_optimized(img, output_path, format='PNG', optimize=True)

        return img

    def _style_quote(
        self,
        img: Image.Image,
        message: str,
        include_logo: bool
    ) -> Image.Image:
        """Quote card style with large centered text"""
        width, height = img.size
        draw = ImageDraw.Draw(img)

        # Add logo if requested
        if include_logo:
            logo_size = min(width, height) // 6
            img = self.add_logo(
                img,
                position='bottom-right',
                logo_type='icon_nobg',
                max_width=logo_size,
                max_height=logo_size,
                margin=30
            )

        # Large quote text
        quote_size = self._scale_font_size(width, 48, 64, 80)
        quote_font = self.get_font(quote_size, bold=True)

        # Wrap text
        max_width = int(width * 0.85)
        text_lines = self.wrap_text(message.lower(), quote_font, max_width)

        # Calculate centering
        line_spacing = quote_size // 3
        total_height = len(text_lines) * (quote_size + line_spacing)
        start_y = (height - total_height) // 2

        # Draw quote
        current_y = start_y
        for line in text_lines:
            line_width, _ = self.get_text_size(line, quote_font)
            x = (width - line_width) // 2

            self.draw_text_with_outline(
                draw,
                (x, current_y),
                line,
                quote_font,
                self.colors['brand_orange'],
                outline_width=3
            )
            current_y += quote_size + line_spacing

        return img

    def _style_announcement(
        self,
        img: Image.Image,
        message: str,
        include_logo: bool
    ) -> Image.Image:
        """Announcement style with title and subtitle"""
        width, height = img.size
        draw = ImageDraw.Draw(img)

        # Add small logo at top
        if include_logo:
            logo_size = min(width, height) // 5
            img = self.add_logo(
                img,
                position='top-center',
                logo_type='icon_nobg',
                max_width=logo_size,
                max_height=logo_size,
                margin=40
            )

        # Parse message (split on newline or use full text)
        lines = message.split('\n')
        title = lines[0]
        subtitle = lines[1] if len(lines) > 1 else None

        # Title
        title_size = self._scale_font_size(width, 56, 72, 90)
        title_font = self.get_font(title_size, bold=True)

        max_width = int(width * 0.85)
        title_lines = self.wrap_text(title.lower(), title_font, max_width)

        # Calculate positioning
        title_height = len(title_lines) * (title_size + 15)
        subtitle_height = 0

        if subtitle:
            subtitle_size = self._scale_font_size(width, 32, 40, 48)
            subtitle_height = subtitle_size + 30

        logo_offset = (logo_size if include_logo else 0) + 80
        available_height = height - logo_offset
        start_y = logo_offset + (available_height - title_height - subtitle_height) // 2

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
            current_y += 25
            subtitle_size = self._scale_font_size(width, 32, 40, 48)
            subtitle_font = self.get_font(subtitle_size)

            subtitle_lines = self.wrap_text(subtitle.lower(), subtitle_font, max_width)
            for line in subtitle_lines:
                line_width, _ = self.get_text_size(line, subtitle_font)
                x = (width - line_width) // 2

                draw.text(
                    (x, current_y),
                    line,
                    font=subtitle_font,
                    fill=self.colors['white']
                )
                current_y += subtitle_size + 10

        return img

    def _style_tip(
        self,
        img: Image.Image,
        message: str,
        include_logo: bool
    ) -> Image.Image:
        """Tip card with numbered or bulleted tip"""
        width, height = img.size
        draw = ImageDraw.Draw(img)

        # Add logo watermark in corner
        if include_logo:
            logo_size = min(width, height) // 6
            img = self.add_logo(
                img,
                position='top-left',
                logo_type='icon_nobg',
                max_width=logo_size,
                max_height=logo_size,
                margin=30
            )

        # "TIP" label at top
        label_size = self._scale_font_size(width, 36, 48, 60)
        label_font = self.get_font(label_size, bold=True)

        label_text = "TIP"
        label_width, label_height = self.get_text_size(label_text, label_font)
        label_x = (width - label_width) // 2
        label_y = height // 6

        draw.text(
            (label_x, label_y),
            label_text,
            font=label_font,
            fill=self.colors['brand_orange']
        )

        # Tip text
        tip_size = self._scale_font_size(width, 40, 52, 64)
        tip_font = self.get_font(tip_size)

        max_width = int(width * 0.85)
        tip_lines = self.wrap_text(message.lower(), tip_font, max_width)

        # Calculate centering
        line_spacing = tip_size // 4
        total_height = len(tip_lines) * (tip_size + line_spacing)
        start_y = (height - total_height) // 2 + 40

        # Draw tip text
        current_y = start_y
        for line in tip_lines:
            line_width, _ = self.get_text_size(line, tip_font)
            x = (width - line_width) // 2

            self.draw_text_with_outline(
                draw,
                (x, current_y),
                line,
                tip_font,
                self.colors['white'],
                outline_width=2
            )
            current_y += tip_size + line_spacing

        return img

    def _style_stat(
        self,
        img: Image.Image,
        message: str,
        include_logo: bool
    ) -> Image.Image:
        """Stat card with large number and context"""
        width, height = img.size
        draw = ImageDraw.Draw(img)

        # Add small logo in corner
        if include_logo:
            logo_size = min(width, height) // 7
            img = self.add_logo(
                img,
                position='bottom-right',
                logo_type='icon_nobg',
                max_width=logo_size,
                max_height=logo_size,
                margin=30
            )

        # Parse message (expect format like "78%\nof businesses struggle with AI")
        lines = message.split('\n', 1)
        stat_number = lines[0].strip()
        context = lines[1].strip() if len(lines) > 1 else ""

        # Huge stat number
        stat_size = self._scale_font_size(width, 120, 160, 200)
        stat_font = self.get_font(stat_size, bold=True)

        stat_width, stat_height = self.get_text_size(stat_number, stat_font)
        stat_x = (width - stat_width) // 2

        # Context text
        context_size = self._scale_font_size(width, 32, 40, 48)
        context_font = self.get_font(context_size)

        max_width = int(width * 0.85)
        context_lines = self.wrap_text(context.lower(), context_font, max_width)
        context_height = len(context_lines) * (context_size + 10)

        # Calculate vertical centering
        total_height = stat_height + 40 + context_height
        start_y = (height - total_height) // 2

        # Draw stat number
        self.draw_text_with_outline(
            draw,
            (stat_x, start_y),
            stat_number,
            stat_font,
            self.colors['brand_orange'],
            outline_width=4
        )

        # Draw context
        current_y = start_y + stat_height + 40
        for line in context_lines:
            line_width, _ = self.get_text_size(line, context_font)
            x = (width - line_width) // 2

            draw.text(
                (x, current_y),
                line,
                font=context_font,
                fill=self.colors['white']
            )
            current_y += context_size + 10

        return img

    def _scale_font_size(
        self,
        width: int,
        small: int,
        medium: int,
        large: int
    ) -> int:
        """Scale font size based on image width"""
        if width < 800:
            return small
        elif width < 1200:
            return medium
        else:
            return large


def main():
    """Example usage"""
    print("Boring Business AI - Social Media Image Generator")
    print("=" * 60)

    generator = SocialMediaGenerator()

    # Example 1: Instagram quote post
    print("\n1. Generating Instagram quote post...")
    generator.generate_post(
        message="AI doesn't have to be complicated to be powerful",
        platform='instagram',
        style='quote',
        size_type='square',
        output_path='social_quote_ig.png'
    )

    # Example 2: LinkedIn announcement
    print("\n2. Generating LinkedIn announcement...")
    generator.generate_post(
        message="New Course Launch\nAI Operations Fundamentals - Enroll Now",
        platform='linkedin',
        style='announcement',
        size_type='post',
        output_path='social_announcement_li.png'
    )

    # Example 3: Twitter tip
    print("\n3. Generating Twitter tip card...")
    generator.generate_post(
        message="Start with one automated process. Master it. Then scale.",
        platform='twitter',
        style='tip',
        size_type='post',
        output_path='social_tip_tw.png'
    )

    # Example 4: Instagram stat card
    print("\n4. Generating Instagram stat card...")
    generator.generate_post(
        message="78%\nof businesses still struggle with AI implementation",
        platform='instagram',
        style='stat',
        size_type='square',
        output_path='social_stat_ig.png'
    )

    # Example 5: Profile picture
    print("\n5. Generating profile picture...")
    generator.generate_profile(
        platform='instagram',
        output_path='profile_picture.png'
    )

    print("\n✓ All social media images generated successfully!")
    print("\nGenerated files:")
    print("  - social_quote_ig.png")
    print("  - social_announcement_li.png")
    print("  - social_tip_tw.png")
    print("  - social_stat_ig.png")
    print("  - profile_picture.png")


if __name__ == '__main__':
    main()
