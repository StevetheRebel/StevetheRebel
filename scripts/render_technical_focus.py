
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

# Project paths
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "cards"
OUTPUT.mkdir(parents=True, exist_ok=True)

# Portfolio colour scheme
BG = "#FAFAF8"
SURFACE = "#FFFFFF"
TEXT = "#171719"
SECONDARY = "#5C5C63"
MUTED = "#7B7B82"
BORDER = "#E5E5E2"
SOFT = "#F3F3F1"

CORAL = "#FF5349"
EMERALD = "#00B075"
LAVENDER = "#AA6EFF"

WIDTH = 1120
HEIGHT = 790

# Technical focus areas
CARDS = [
    {
        "number": "01",
        "title": "Frontend Engineering",
        "description": (
            "Responsive interfaces, reusable components "
            "and accessible user experiences."
        ),
        "tags": ["Interfaces", "Components", "Responsive UI"],
        "color": CORAL,
    },
    {
        "number": "02",
        "title": "Backend Engineering",
        "description": (
            "APIs, server-side logic and structured "
            "application architectures."
        ),
        "tags": ["REST APIs", "Application Logic", "Architecture"],
        "color": EMERALD,
    },
    {
        "number": "03",
        "title": "Data & Databases",
        "description": (
            "Relational data models, database operations "
            "and data integrity."
        ),
        "tags": ["Data Modelling", "SQL", "Database Operations"],
        "color": LAVENDER,
    },
    {
        "number": "04",
        "title": "Systems Integration",
        "description": (
            "External services, API connections "
            "and application workflows."
        ),
        "tags": ["API Integration", "Services", "Workflows"],
        "color": CORAL,
    },
    {
        "number": "05",
        "title": "Cloud & Delivery",
        "description": (
            "Cloud infrastructure, deployment workflows "
            "and version control."
        ),
        "tags": ["Cloud", "Deployment", "Git"],
        "color": EMERALD,
    },
]


# Font loading with Windows and Linux fallbacks
def load_font(size, mono=False, bold=False):
    if mono:
        candidates = [
            "C:/Windows/Fonts/consola.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        ]
    elif bold:
        candidates = [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)

    return ImageFont.load_default()


FONT_KICKER = load_font(13, mono=True)
FONT_TITLE = load_font(38)
FONT_SUBTITLE = load_font(17)
FONT_CARD_TITLE = load_font(21, bold=True)
FONT_DESCRIPTION = load_font(15)
FONT_TAG = load_font(12, mono=True)
FONT_META = load_font(12, mono=True)


def draw_header(draw):
    draw.text(
        (48, 42),
        "TECHNICAL FOCUS",
        font=FONT_KICKER,
        fill=CORAL,
    )

    draw.text(
        (48, 72),
        "What I work with.",
        font=FONT_TITLE,
        fill=TEXT,
    )

    draw.text(
        (50, 126),
        "Core areas of software development and engineering.",
        font=FONT_SUBTITLE,
        fill=SECONDARY,
    )

    draw.text(
        (1072, 52),
        "01 / 05",
        font=FONT_META,
        fill=MUTED,
        anchor="ra",
    )


def draw_tag(draw, x, y, label):
    bbox = draw.textbbox((0, 0), label, font=FONT_TAG)
    text_width = bbox[2] - bbox[0]

    tag_width = text_width + 20
    tag_height = 23

    draw.rounded_rectangle(
        (x, y, x + tag_width, y + tag_height),
        radius=7,
        fill=SOFT,
    )

    draw.text(
        (x + 10, y + 5),
        label,
        font=FONT_TAG,
        fill=SECONDARY,
    )

    return tag_width


def draw_card(draw, card, index, line_progress, pulse):
    # Consistent horizontal panel dimensions
    x1 = 48
    y1 = 184 + index * 112
    x2 = 1072
    y2 = y1 + 98

    color = card["color"]

    # Panel
    draw.rounded_rectangle(
        (x1, y1, x2, y2),
        radius=14,
        fill=SURFACE,
        outline=BORDER,
        width=1,
    )

    # Left accent rail
    draw.rounded_rectangle(
        (x1 + 20, y1 + 20, x1 + 24, y2 - 20),
        radius=2,
        fill=color,
    )

    # Heading
    draw.text(
        (x1 + 42, y1 + 14),
        card["title"],
        font=FONT_CARD_TITLE,
        fill=TEXT,
    )

    # Description
    draw.text(
        (x1 + 42, y1 + 45),
        card["description"],
        font=FONT_DESCRIPTION,
        fill=SECONDARY,
    )

    # Tags on a separate line
    tag_x = x1 + 42
    tag_y = y1 + 69

    for tag in card["tags"]:
        tag_width = draw_tag(draw, tag_x, tag_y, tag)
        tag_x += tag_width + 8

    # Number
    draw.text(
        (x2 - 60, y1 + 17),
        card["number"],
        font=FONT_META,
        fill=MUTED,
    )

    # Animated accent dot
    dot_x = x2 - 28
    dot_y = y1 + 29

    radius = 4 + round(pulse * 1.5)

    draw.ellipse(
        (
            dot_x - radius,
            dot_y - radius,
            dot_x + radius,
            dot_y + radius,
        ),
        fill=color,
    )

    # Accent line background
    line_y = y2 - 2
    line_start = x1 + 42
    line_end = x2 - 20

    draw.line(
        (line_start, line_y, line_end, line_y),
        fill=SOFT,
        width=2,
    )

    # Animated accent line
    animated_end = (
        line_start
        + int((line_end - line_start) * line_progress)
    )

    if animated_end > line_start:
        draw.line(
            (line_start, line_y, animated_end, line_y),
            fill=color,
            width=2,
        )


def render_frame(frame_index, total_frames):
    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        BG,
    )

    draw = ImageDraw.Draw(image)

    draw_header(draw)

    cycle = frame_index / total_frames

    for index, card in enumerate(CARDS):
        # Stagger the accent-line animation
        start = index * 0.13

        progress = max(
            0.0,
            min(1.0, (cycle - start) / 0.18),
        )

        # Gentle marker pulse
        pulse = (
            math.sin(cycle * math.tau * 2 + index * 0.55) + 1
        ) / 2

        draw_card(
            draw,
            card,
            index,
            progress,
            pulse,
        )

    return image


def main():
    frame_count = 60

    frames = [
        render_frame(frame, frame_count)
        for frame in range(frame_count)
    ]

    # Static PNG preview
    static_image = render_frame(
        frame_count - 1,
        frame_count,
    )

    static_image.save(
        OUTPUT / "technical-focus.png",
        optimize=True,
    )

    # Convert frames to a shared GIF-compatible palette
    gif_frames = [
        frame.quantize(
            colors=128,
            method=Image.Quantize.MEDIANCUT,
        )
        for frame in frames
    ]

    # Animated GIF
    gif_frames[0].save(
        OUTPUT / "technical-focus.gif",
        save_all=True,
        append_images=gif_frames[1:],
        duration=100,
        loop=0,
        optimize=True,
        disposal=2,
    )

    print("Technical Focus assets generated:")
    print(OUTPUT / "technical-focus.gif")
    print(OUTPUT / "technical-focus.png")


if __name__ == "__main__":
    main()
