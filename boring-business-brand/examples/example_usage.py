#!/usr/bin/env python3
"""
Example Usage: Boring Business AI Brand Image Generator

This script demonstrates all the capabilities of the brand image generator skill.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from beehiiv_header import BeehiivHeaderGenerator
from skool_cover import SkoolCoverGenerator
from social_media import SocialMediaGenerator


def main():
    print("=" * 70)
    print("  Boring Business AI - Brand Image Generator")
    print("  Example Usage Demonstration")
    print("=" * 70)

    # Create output directory for examples
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)

    print(f"\nOutput directory: {output_dir}")
    print("\n" + "=" * 70)

    # 1. Beehiiv Headers
    print("\n📧 BEEHIIV EMAIL HEADERS")
    print("-" * 70)

    beehiiv = BeehiivHeaderGenerator()

    print("\n1. Centered layout header...")
    beehiiv.generate_header(
        title="AI Automation Weekly",
        subtitle="Your Guide to Practical AI Implementation",
        layout='centered',
        size='large',
        output_path=str(output_dir / 'beehiiv_centered.png')
    )

    print("\n2. Left-aligned layout header...")
    beehiiv.generate_header(
        title="The Boring Business AI Newsletter",
        subtitle="October 2025 Edition",
        layout='left',
        size='large',
        output_path=str(output_dir / 'beehiiv_left.png')
    )

    print("\n3. Minimal layout header...")
    beehiiv.generate_header(
        title="AI Operations Update",
        layout='minimal',
        size='large',
        output_path=str(output_dir / 'beehiiv_minimal.png')
    )

    # 2. Skool Course Covers
    print("\n" + "=" * 70)
    print("\n📚 SKOOL COURSE COVERS")
    print("-" * 70)

    skool = SkoolCoverGenerator()

    print("\n1. Corner logo layout...")
    skool.generate_cover(
        course_title="AI Operations Fundamentals",
        subtitle="From Setup to Scale in 4 Weeks",
        key_points=[
            "Practical Implementation Strategies",
            "Real-World Case Studies",
            "Measurable ROI Frameworks",
            "Hands-On Projects"
        ],
        layout='corner-logo',
        size='hd',
        output_path=str(output_dir / 'skool_corner.png')
    )

    print("\n2. Split layout...")
    skool.generate_cover(
        course_title="Boring Business AI Masterclass",
        subtitle="Real AI for Real Business",
        layout='split',
        size='hd',
        output_path=str(output_dir / 'skool_split.png')
    )

    print("\n3. Overlay layout...")
    skool.generate_cover(
        course_title="Advanced AI Automation",
        subtitle="Scale Your Operations with AI",
        layout='overlay',
        size='hd',
        output_path=str(output_dir / 'skool_overlay.png')
    )

    print("\n4. Banner layout...")
    skool.generate_cover(
        course_title="AI Implementation Bootcamp",
        subtitle="4-Week Intensive Program",
        layout='banner',
        size='hd',
        output_path=str(output_dir / 'skool_banner.png')
    )

    # 3. Social Media Posts
    print("\n" + "=" * 70)
    print("\n📱 SOCIAL MEDIA POSTS")
    print("-" * 70)

    social = SocialMediaGenerator()

    print("\n1. Instagram quote post...")
    social.generate_post(
        message="AI doesn't have to be complicated to be powerful",
        platform='instagram',
        style='quote',
        size_type='square',
        include_logo=True,
        output_path=str(output_dir / 'social_quote_ig.png')
    )

    print("\n2. LinkedIn announcement...")
    social.generate_post(
        message="New Course Launch\nAI Operations Fundamentals - Enroll Now",
        platform='linkedin',
        style='announcement',
        size_type='post',
        include_logo=True,
        output_path=str(output_dir / 'social_announcement_li.png')
    )

    print("\n3. Twitter tip card...")
    social.generate_post(
        message="Start with one automated process. Master it. Then scale.",
        platform='twitter',
        style='tip',
        size_type='post',
        include_logo=True,
        output_path=str(output_dir / 'social_tip_tw.png')
    )

    print("\n4. Instagram stat card...")
    social.generate_post(
        message="78%\nof businesses still struggle with AI implementation",
        platform='instagram',
        style='stat',
        size_type='square',
        include_logo=True,
        output_path=str(output_dir / 'social_stat_ig.png')
    )

    print("\n5. Profile picture (Instagram)...")
    social.generate_profile(
        platform='instagram',
        output_path=str(output_dir / 'profile_instagram.png')
    )

    # Summary
    print("\n" + "=" * 70)
    print("\n✅ COMPLETE! All example images generated successfully.")
    print("\n" + "=" * 70)
    print("\nGenerated Images:")
    print("-" * 70)

    images = sorted(output_dir.glob('*.png'))
    for i, img_path in enumerate(images, 1):
        print(f"  {i:2d}. {img_path.name}")

    print("\n" + "=" * 70)
    print(f"\nView your images in: {output_dir}")
    print("\nNext Steps:")
    print("  • Review the generated images")
    print("  • Check BRAND_GUIDELINES.md for design specifications")
    print("  • Customize scripts for your specific needs")
    print("  • Integrate with your workflow\n")


if __name__ == '__main__':
    main()
