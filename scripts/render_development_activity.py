
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random
import math

# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "cards"
OUTPUT.mkdir(parents=True, exist_ok=True)

WIDTH = 1120
HEIGHT = 550

# Portfolio colours
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

# Contribution graph colours
LEVELS = [
    "#EBF5F0",
    "#BDE5D3",
    "#79CBA7",
    "#35AF7B",
    "#008F5E",
]

# GitHub-style contribution graph dimensions
WEEKS = 53
DAYS = 7

CELL_SIZE = 11
CELL_GAP = 3
CELL_STEP = CELL_SIZE + CELL_GAP

GRAPH_WIDTH = WEEKS * CELL_STEP - CELL_GAP
GRAPH_HEIGHT = DAYS * CELL_STEP - CELL_GAP

GRAPH_X = (WIDTH - GRAPH_WIDTH) // 2 + 16
GRAPH_Y = 280

# Animation settings
FRAME_COUNT = 60
FRAME_DURATION = 90

# Reproducible illustrative activity pattern
random.seed(42)


# --------------------------------------------------
# FONTS
# --------------------------------------------------

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


FONT_KICKER = load_font(12, mono=True)
FONT_TITLE = load_font(34)
FONT_SUBTITLE = load_font(15)
FONT_STAT = load_font(23, bold=True)
FONT_LABEL = load_font(12)
FONT_SMALL = load_font(11, mono=True)


# --------------------------------------------------
# ILLUSTRATIVE CONTRIBUTION DATA
# --------------------------------------------------

def generate_activity():
    """
    Generates illustrative contribution levels.

    Levels:
    0 = No activity
    1 = Low activity
    2 = Moderate activity
    3 = High activity
    4 = Very high activity

    Replace this function with actual GitHub contribution
    data when connecting the graph to live activity.
    """

    activity = []

    for week in range(WEEKS):
        weekly_activity = []

        # Create natural variation across weeks.
        weekly_intensity = random.uniform(0.2, 1.0)

        for day in range(DAYS):
            chance = random.random()

            if chance < 0.24:
                level = 0
            elif chance < 0.52:
                level = 1
            elif chance < 0.76:
                level = 2
            elif chance < 0.94:
                level = 3
            else:
                level = 4

            # Vary intensity across the year.
            if weekly_intensity < 0.35 and level > 2:
                level -= 1

            weekly_activity.append(level)

        activity.append(weekly_activity)

    return activity


ACTIVITY = generate_activity()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

def draw_header(draw):
    draw.text(
        (48, 35),
        "DEVELOPMENT ACTIVITY",
        font=FONT_KICKER,
        fill=CORAL,
    )

    draw.text(
        (48, 62),
        "Building consistently.",
        font=FONT_TITLE,
        fill=TEXT,
    )

    draw.text(
        (50, 112),
        "A snapshot of development work and GitHub contributions.",
        font=FONT_SUBTITLE,
        fill=SECONDARY,
    )

    draw.text(
        (1072, 45),
        "03 / 06",
        font=FONT_SMALL,
        fill=MUTED,
        anchor="ra",
    )


# --------------------------------------------------
# STATISTIC PANELS
# --------------------------------------------------

def draw_stat_cards(draw):
    stats = [
        {
            "label": "PUBLIC REPOSITORIES",
            "value": "GitHub",
            "accent": CORAL,
        },
        {
            "label": "CONTRIBUTION HISTORY",
            "value": "All activity",
            "accent": EMERALD,
        },
        {
            "label": "PRIVATE CONTRIBUTIONS",
            "value": "Included",
            "accent": LAVENDER,
        },
    ]

    card_width = 326
    card_height = 76
    gap = 22

    start_x = (WIDTH - (card_width * 3 + gap * 2)) // 2
    y = 158

    for index, stat in enumerate(stats):
        x = start_x + index * (card_width + gap)

        draw.rounded_rectangle(
            (
                x,
                y,
                x + card_width,
                y + card_height,
            ),
            radius=12,
            fill=SURFACE,
            outline=BORDER,
            width=1,
        )

        draw.rounded_rectangle(
            (
                x + 17,
                y + 18,
                x + 21,
                y + 58,
            ),
            radius=2,
            fill=stat["accent"],
        )

        draw.text(
            (x + 34, y + 14),
            stat["label"],
            font=FONT_SMALL,
            fill=MUTED,
        )

        draw.text(
            (x + 34, y + 34),
            stat["value"],
            font=FONT_STAT,
            fill=TEXT,
        )


# --------------------------------------------------
# CONTRIBUTION GRAPH LABELS
# --------------------------------------------------

def draw_graph_labels(draw):
    # Weekday labels
    weekday_labels = {
        1: "Mon",
        3: "Wed",
        5: "Fri",
    }

    for day, label in weekday_labels.items():
        y = GRAPH_Y + day * CELL_STEP + 1

        draw.text(
            (GRAPH_X - 34, y),
            label,
            font=FONT_SMALL,
            fill=MUTED,
        )

    # Month labels.
    # Approximate month positions across 53 weeks.
    months = [
        ("Jan", 0),
        ("Feb", 4),
        ("Mar", 8),
        ("Apr", 13),
        ("May", 17),
        ("Jun", 21),
        ("Jul", 26),
        ("Aug", 30),
        ("Sep", 34),
        ("Oct", 39),
        ("Nov", 43),
        ("Dec", 47),
    ]

    for month, week in months:
        x = GRAPH_X + week * CELL_STEP

        draw.text(
            (x, GRAPH_Y - 25),
            month,
            font=FONT_SMALL,
            fill=MUTED,
        )


# --------------------------------------------------
# CONTRIBUTION CELLS
# --------------------------------------------------

def draw_contribution_cells(draw):
    for week in range(WEEKS):
        for day in range(DAYS):
            level = ACTIVITY[week][day]

            x = GRAPH_X + week * CELL_STEP
            y = GRAPH_Y + day * CELL_STEP

            draw.rounded_rectangle(
                (
                    x,
                    y,
                    x + CELL_SIZE,
                    y + CELL_SIZE,
                ),
                radius=2,
                fill=LEVELS[level],
            )


# --------------------------------------------------
# SHIMMER ANIMATION
# --------------------------------------------------

def apply_shimmer(image, frame_index):
    """
    Applies a subtle diagonal shimmer across existing
    contribution cells.

    The shimmer does not change the contribution levels.
    It only adds a temporary highlight.
    """

    overlay = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0),
    )

    draw = ImageDraw.Draw(overlay)

    # Sweep across the graph from left to right.
    progress = frame_index / FRAME_COUNT

    sweep_position = (
        GRAPH_X - 100
        + progress * (GRAPH_WIDTH + 200)
    )

    shimmer_width = 34

    for week in range(WEEKS):
        for day in range(DAYS):
            level = ACTIVITY[week][day]

            # Do not highlight empty cells.
            if level == 0:
                continue

            x = GRAPH_X + week * CELL_STEP
            y = GRAPH_Y + day * CELL_STEP

            # Diagonal sweep position.
            cell_center = x + day * 5

            distance = abs(
                cell_center - sweep_position
            )

            if distance < shimmer_width:
                intensity = 1 - distance / shimmer_width

                alpha = int(65 * intensity)

                draw.rounded_rectangle(
                    (
                        x,
                        y,
                        x + CELL_SIZE,
                        y + CELL_SIZE,
                    ),
                    radius=2,
                    fill=(255, 255, 255, alpha),
                )

    return Image.alpha_composite(
        image.convert("RGBA"),
        overlay,
    ).convert("RGB")


# --------------------------------------------------
# GRAPH FOOTER
# --------------------------------------------------

def draw_graph_footer(draw):
    footer_y = GRAPH_Y + GRAPH_HEIGHT + 23

    draw.text(
        (GRAPH_X, footer_y),
        "Less",
        font=FONT_SMALL,
        fill=MUTED,
    )

    legend_x = GRAPH_X + 39

    for colour in LEVELS:
        draw.rounded_rectangle(
            (
                legend_x,
                footer_y + 1,
                legend_x + CELL_SIZE,
                footer_y + 1 + CELL_SIZE,
            ),
            radius=2,
            fill=colour,
        )

        legend_x += CELL_STEP + 3

    draw.text(
        (legend_x + 3, footer_y),
        "More",
        font=FONT_SMALL,
        fill=MUTED,
    )

    draw.text(
        (
            WIDTH - 48,
            footer_y,
        ),
        "PUBLIC + PRIVATE CONTRIBUTIONS",
        font=FONT_SMALL,
        fill=MUTED,
        anchor="ra",
    )


# --------------------------------------------------
# FRAME RENDERING
# --------------------------------------------------

def render_frame(frame_index):
    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        BG,
    )

    draw = ImageDraw.Draw(image)

    draw_header(draw)
    draw_stat_cards(draw)
    draw_graph_labels(draw)
    draw_contribution_cells(draw)
    draw_graph_footer(draw)

    image = apply_shimmer(
        image,
        frame_index,
    )

    return image


# --------------------------------------------------
# GENERATE OUTPUTS
# --------------------------------------------------

def main():
    print("Rendering development activity...")

    frames = []

    for frame_index in range(FRAME_COUNT):
        frames.append(
            render_frame(frame_index)
        )

    # Static PNG
    static_frame = render_frame(0)

    static_frame.save(
        OUTPUT / "development-activity.png",
        optimize=True,
    )

    # GIF palette conversion
    gif_frames = [
        frame.quantize(
            colors=128,
            method=Image.Quantize.MEDIANCUT,
        )
        for frame in frames
    ]

    # Animated GIF
    gif_frames[0].save(
        OUTPUT / "development-activity.gif",
        save_all=True,
        append_images=gif_frames[1:],
        duration=FRAME_DURATION,
        loop=0,
        optimize=True,
        disposal=2,
    )

    print("Generated successfully:")
    print(OUTPUT / "development-activity.gif")
    print(OUTPUT / "development-activity.png")


if __name__ == "__main__":
    main()
