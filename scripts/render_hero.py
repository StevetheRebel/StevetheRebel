
from pathlib import Path
from typing import cast
from PIL import Image, ImageEnhance, ImageOps
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parent.parent

IMAGE_PATH = ROOT / "assets" / "profile.png"
CARDS_DIR = ROOT / "cards"

ASCII_CHARS = "@%#*+=-:. "

# Portrait rendering settings
ASCII_COLUMNS = 100
FONT_SIZE = 7
LINE_HEIGHT = 8.5
START_X = 635
START_Y = 75

# Portfolio light theme
THEME = {
    "background": "#FAFAF8",
    "foreground": "#171719",
    "surface": "#FFFFFF",
    "muted": "#F3F3F1",
    "secondary": "#5C5C63",
    "subtle": "#7B7B82",
    "border": "#E5E5E2",
    "portrait": "#262523",
}

CORAL = "#FF5349"
EMERALD = "#00B075"
LAVENDER = "#AA6EFF"


def image_to_ascii_lines(
    image_path: Path,
    cols: int = ASCII_COLUMNS,
) -> list[str]:
    """Convert a photograph into rows of monochrome ASCII characters."""

    if not image_path.exists():
        raise FileNotFoundError(
            f"Profile photograph not found: {image_path}"
        )

    img = Image.open(image_path).convert("RGBA")

    # Crop to a portrait-oriented frame.
    img = ImageOps.fit(
        img,
        (450, 475),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.4),
    )

    # Composite transparent pixels onto white.
    background = Image.new(
        "RGBA",
        img.size,
        (255, 255, 255, 255),
    )

    img = Image.alpha_composite(
        background,
        img,
    ).convert("L")

    # Improve tonal separation without excessive contrast.
    img = ImageEnhance.Contrast(img).enhance(1.2)

    # Monospace characters are taller than they are wide.
    aspect_ratio = img.height / img.width
    rows = int(cols * aspect_ratio * 0.52)

    img = img.resize(
        (cols, rows),
        Image.Resampling.LANCZOS,
    )

    lines = []

    for y in range(rows):
        row_chars = []

        for x in range(cols):
            brightness = cast(int, img.getpixel((x, y)))

            index = int(
                (brightness / 255) *
                (len(ASCII_CHARS) - 1)
            )

            row_chars.append(ASCII_CHARS[index])

        lines.append("".join(row_chars))

    return lines


def build_ascii_text(lines: list[str]) -> str:
    """Build SVG text using one tspan for each ASCII row."""

    tspans = []

    for index, line in enumerate(lines):
        y = START_Y + index * LINE_HEIGHT

        tspans.append(
            f'<tspan x="{START_X}" y="{y:.1f}" '
            f'xml:space="preserve">{escape(line)}</tspan>'
        )

    return "\n      ".join(tspans)


def build_hero_svg(
    ascii_lines: list[str],
    output_path: Path,
):
    """Generate the light-themed hero SVG."""

    theme = THEME
    ascii_block = build_ascii_text(ascii_lines)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  width="1120"
  height="560"
  viewBox="0 0 1120 560"
  role="img"
  aria-labelledby="title desc">

  <title id="title">Steve Odumbe, Software Developer</title>

  <desc id="desc">
    Software developer building web applications with modern
    frontend and backend technologies.
  </desc>

  <defs>
    <linearGradient id="shimmer-grad"
      x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="42%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.45"/>
      <stop offset="58%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>

      <animateTransform
        attributeName="gradientTransform"
        type="translate"
        from="-1 -1"
        to="1 1"
        dur="4.5s"
        repeatCount="indefinite"/>
    </linearGradient>

    <clipPath id="portrait-clip">
      <rect x="625" y="45" width="450" height="475" rx="12"/>
    </clipPath>
  </defs>

  <style>
    .bg {{
      fill: {theme["background"]};
    }}

    .eyebrow {{
      font-family: "JetBrains Mono", monospace;
      font-size: 13px;
      letter-spacing: 0.14em;
      fill: {theme["subtle"]};
    }}

    .display-title {{
      font-family: "Plus Jakarta Sans", Inter, Arial, sans-serif;
      font-size: 106px;
      font-weight: 700;
      letter-spacing: -0.045em;
      fill: {theme["foreground"]};
    }}

    .accent-letter {{
      fill: {CORAL};
    }}

    .role {{
      font-family: "JetBrains Mono", monospace;
      font-size: 15px;
      font-weight: 600;
      letter-spacing: 0.08em;
      fill: {theme["foreground"]};
    }}

    .bio {{
      font-family: Inter, Arial, sans-serif;
      font-size: 19px;
      fill: {theme["secondary"]};
    }}

    .domain-link {{
      font-family: "JetBrains Mono", monospace;
      font-size: 15px;
      fill: {theme["foreground"]};
    }}

    .ascii-art {{
      font-family: "JetBrains Mono", monospace;
      font-size: {FONT_SIZE}px;
      letter-spacing: 0;
      fill: {theme["portrait"]};
    }}
  </style>

  <!-- Main card -->
  <rect class="bg" width="1120" height="560" rx="22"/>

  <rect x="1" y="1" width="1118" height="558"
    rx="21" fill="none"
    stroke="{theme["border"]}"/>

  <!-- Decorative background -->
  <circle cx="1040" cy="85" r="125"
    fill="{CORAL}" opacity="0.07"/>

  <circle cx="1080" cy="475" r="100"
    fill="{LAVENDER}" opacity="0.09"/>

  <path d="M875 0 H1120 V560 H980
    C1045 440 1000 310 940 220
    C900 155 875 80 875 0Z"
    fill="{theme["muted"]}"/>

  <path d="M970 0 H1120 V560 H1060
    C1110 420 1080 300 1030 190
    C1000 125 980 60 970 0Z"
    fill="{EMERALD}" opacity="0.07"/>

  <!-- Eyebrow -->
  <rect x="64" y="62" width="11" height="11"
    rx="3" fill="{CORAL}"/>

  <text class="eyebrow" x="88" y="73">
    GITHUB PROFILE / 01
  </text>

  <!-- Display name -->
  <text class="display-title" x="60" y="205">
    Steve
  </text>

  <text class="display-title" x="60" y="310">
    Odumbe<tspan class="accent-letter">.</tspan>
  </text>

  <!-- Developer role -->
  <rect x="64" y="350" width="8" height="8"
    rx="2" fill="{CORAL}"/>

  <text class="role" x="88" y="360">
    SOFTWARE DEVELOPER
  </text>

  <!-- Introduction -->
  <text class="bio" x="64" y="414">
    Building web applications with modern
  </text>

  <text class="bio" x="64" y="444">
    frontend and backend technologies.
  </text>

  <!-- Portfolio link -->
  <text class="domain-link" x="64" y="510">
    steveodumbe.works
    <tspan fill="{CORAL}"> ↗</tspan>
  </text>

  <!-- ASCII portrait -->
  <g clip-path="url(#portrait-clip)">
    <text class="ascii-art">
      {ascii_block}
    </text>

    <!-- Shimmer effect -->
    <rect x="625" y="45" width="450" height="475"
      fill="url(#shimmer-grad)"
      pointer-events="none"/>
  </g>

  <!-- Portrait frame -->
  <rect x="625" y="45" width="450" height="475"
    rx="12" fill="none"
    stroke="{theme["border"]}"/>

  <!-- Footer label -->
  <text x="1075" y="540"
    text-anchor="end"
    font-family="JetBrains Mono, monospace"
    font-size="10"
    letter-spacing="1.2"
    fill="{theme["subtle"]}">
    DESIGN. BUILD. ITERATE.
  </text>

</svg>
'''

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        svg,
        encoding="utf-8",
    )

    print(f"Generated: {output_path.relative_to(ROOT)}")


def main():
    """Generate the light hero card."""

    if not IMAGE_PATH.exists():
        raise FileNotFoundError(
            "Add your profile photograph at assets/profile.png"
        )

    ascii_lines = image_to_ascii_lines(IMAGE_PATH)

    build_hero_svg(
        ascii_lines,
        CARDS_DIR / "hero-light.svg",
    )

    print("Light hero generation complete.")


if __name__ == "__main__":
    main()
