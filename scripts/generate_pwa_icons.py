#!/usr/bin/env python3
# scripts/generate_pwa_icons.py — Generates PNG app icons for My Reading Corner PWA
# Usage: python3 scripts/generate_pwa_icons.py

from PIL import Image, ImageDraw
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
BOOKSHELF_DIR = ROOT / "bookshelf"

def draw_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Warm rounded squircle background (gradient approximation: #8A2814 to #E08736)
    radius = int(size * 0.22)
    
    # Create mask for rounded rectangle
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    margin = int(size * 0.04)
    mask_draw.rounded_rectangle([margin, margin, size - margin, size - margin], radius=radius, fill=255)

    # Base gradient image
    gradient = Image.new("RGBA", (size, size))
    g_draw = ImageDraw.Draw(gradient)
    for y in range(size):
        ratio = y / size
        # From #8A2814 (138, 40, 20) to #E08736 (224, 135, 54)
        r = int(138 + (224 - 138) * ratio)
        g = int(40 + (135 - 40) * ratio)
        b = int(20 + (54 - 20) * ratio)
        g_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    img.paste(gradient, (0, 0), mask)

    # Subtle inner gold border
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin], 
        radius=radius, 
        outline=(245, 158, 11, 70), 
        width=max(2, int(size * 0.015))
    )

    scale = size / 36.0

    # 2. Floor Arc Lamp
    lamp_stroke = max(2, int(scale * 1.5))
    # Base
    draw.line([(int(8 * scale), int(31 * scale)), (int(14 * scale), int(31 * scale))], fill=(254, 243, 199, 240), width=lamp_stroke)
    # Arc stem
    # Approximate arc with line segments
    pts = [
        (int(10.5 * scale), int(31 * scale)),
        (int(10.5 * scale), int(18 * scale)),
        (int(12 * scale), int(12 * scale)),
        (int(16 * scale), int(8 * scale)),
        (int(22 * scale), int(8.5 * scale))
    ]
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=(254, 243, 199, 240), width=lamp_stroke)

    # Shade
    shade_pts = [
        (int(20.5 * scale), int(8.5 * scale)),
        (int(25.5 * scale), int(12 * scale)),
        (int(22.5 * scale), int(14 * scale))
    ]
    draw.polygon(shade_pts, fill=(253, 230, 138, 255))

    # Ambient Glow cone
    cone_pts = [
        (int(23 * scale), int(13.5 * scale)),
        (int(15 * scale), int(28 * scale)),
        (int(30 * scale), int(28 * scale))
    ]
    glow_overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    glow_draw.polygon(cone_pts, fill=(253, 230, 138, 45))
    img = Image.alpha_composite(img, glow_overlay)
    draw = ImageDraw.Draw(img)

    # 3. Open Book
    # Left page
    left_pts = [
        (int(16 * scale), int(24 * scale)),
        (int(22 * scale), int(23 * scale)),
        (int(22 * scale), int(28 * scale)),
        (int(16 * scale), int(28.5 * scale))
    ]
    draw.polygon(left_pts, fill=(255, 247, 237, 255), outline=(180, 83, 9, 200))
    
    # Right page
    right_pts = [
        (int(22 * scale), int(23 * scale)),
        (int(28 * scale), int(24 * scale)),
        (int(28 * scale), int(28.5 * scale)),
        (int(22 * scale), int(28 * scale))
    ]
    draw.polygon(right_pts, fill=(254, 235, 200, 255), outline=(180, 83, 9, 200))
    
    # Spine line
    draw.line([(int(22 * scale), int(23 * scale)), (int(22 * scale), int(28 * scale))], fill=(200, 90, 50, 255), width=max(1, int(scale * 0.8)))

    # 4. Corner star / sparkle
    sx = int(29 * scale)
    sy = int(8 * scale)
    sr = int(2.5 * scale)
    star_pts = [
        (sx, sy - sr),
        (sx + int(sr*0.3), sy - int(sr*0.3)),
        (sx + sr, sy),
        (sx + int(sr*0.3), sy + int(sr*0.3)),
        (sx, sy + sr),
        (sx - int(sr*0.3), sy + int(sr*0.3)),
        (sx - sr, sy),
        (sx - int(sr*0.3), sy - int(sr*0.3))
    ]
    draw.polygon(star_pts, fill=(251, 191, 36, 255))

    return img

def main():
    for target_dir in [DOCS_DIR, BOOKSHELF_DIR]:
        target_dir.mkdir(parents=True, exist_ok=True)
        img192 = draw_icon(192)
        img192.save(target_dir / "icon-192.png", "PNG")
        
        img512 = draw_icon(512)
        img512.save(target_dir / "icon-512.png", "PNG")
        
        img180 = draw_icon(180) # Apple touch icon
        img180.save(target_dir / "apple-touch-icon.png", "PNG")
        
        print(f"Generated PWA icons in {target_dir}")

if __name__ == "__main__":
    main()
