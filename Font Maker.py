from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from PIL import Image


# ===== SETTINGS =====
CHARS = "1234567890"
PADDING = 1

# Treat alpha <= threshold as transparent (increase if your art has semi-transparent pixels)
ALPHA_THRESHOLD = 20

# Enforce exactly N glyphs even if digits touch
FORCE_EXACT_COUNT = True

# Minimum pixel width per digit segment (prevents absurdly skinny slices)
MIN_GLYPH_WIDTH = 12

# Trim top/bottom of each glyph to non-transparent pixels
TRIM_VERTICAL = True

OUTPUT_BASENAME = "digits"
# ====================


@dataclass
class Glyph:
    ch: str
    x: int
    y: int
    w: int
    h: int
    xoffset: int = 0
    yoffset: int = 0
    xadvance: int = 0


def column_ink(img: Image.Image, alpha_threshold: int) -> List[int]:
    """Sum of alpha>threshold pixels per column (inkiness)."""
    w, h = img.size
    px = img.load()
    ink = [0] * w
    for x in range(w):
        s = 0
        for y in range(h):
            if px[x, y][3] > alpha_threshold:
                s += 1
        ink[x] = s
    return ink


def trim_box_vertical(img: Image.Image, box: Tuple[int, int, int, int], alpha_threshold: int) -> Tuple[int, int, int, int]:
    """Trim top/bottom of a box to content."""
    x0, y0, x1, y1 = box
    px = img.load()
    h = img.size[1]

    top = None
    bottom = None

    for yy in range(0, h):
        for xx in range(x0, x1):
            if px[xx, yy][3] > alpha_threshold:
                top = yy
                break
        if top is not None:
            break

    for yy in range(h - 1, -1, -1):
        for xx in range(x0, x1):
            if px[xx, yy][3] > alpha_threshold:
                bottom = yy
                break
        if bottom is not None:
            break

    if top is None or bottom is None:
        # empty; fall back to original vertical range
        return (x0, y0, x1, y1)

    return (x0, top, x1, bottom + 1)


def forced_k_splits(
    ink: List[int],
    k: int,
    min_width: int,
) -> List[int]:
    """
    Choose k-1 cut positions (integers in [1..W-1]) to create k segments.
    Cuts are chosen at low-ink columns via DP, respecting min segment width.
    Returns sorted cut positions.
    """
    W = len(ink)
    if k * min_width > W:
        raise RuntimeError(f"Image too narrow: width={W}, k={k}, min_width={min_width}")

    # Cost of cutting at x: prefer low ink. Square to strongly avoid cutting through ink.
    cost = [ink[x] * ink[x] for x in range(W)]

    INF = 10**18
    # dp[i][j] = min cost to place j cuts ending exactly at position i (i is a cut)
    # We'll store only predecessors.
    # Valid cut positions are from min_width to W-min_width, and spaced by min_width.
    dp = [[INF] * (k) for _ in range(W)]
    prev = [[-1] * (k) for _ in range(W)]

    # First cut (j=1 means one cut placed): cut at i with first segment width >= min_width
    for i in range(min_width, W - min_width + 1):
        dp[i][1] = cost[i]
        prev[i][1] = 0

    # Subsequent cuts
    for j in range(2, k):  # we place k-1 cuts; j indexes number of cuts placed
        for i in range(min_width * j, W - min_width + 1):
            # previous cut p must be at least min_width behind i
            best_val = INF
            best_p = -1
            p_start = min_width * (j - 1)
            p_end = i - min_width
            for p in range(p_start, p_end + 1):
                val = dp[p][j - 1] + cost[i]
                if val < best_val:
                    best_val = val
                    best_p = p
            dp[i][j] = best_val
            prev[i][j] = best_p

    # Choose final cut position so last segment >= min_width
    j = k - 1
    best_end = -1
    best_val = INF
    for i in range(min_width * j, W - min_width + 1):
        val = dp[i][j]
        if val < best_val:
            best_val = val
            best_end = i

    if best_end < 0:
        raise RuntimeError("Could not compute forced cuts. Try lowering MIN_GLYPH_WIDTH.")

    # Backtrack cuts
    cuts = []
    cur = best_end
    cur_j = j
    while cur_j >= 1:
        cuts.append(cur)
        cur = prev[cur][cur_j]
        cur_j -= 1
        if cur < 0 and cur_j >= 1:
            raise RuntimeError("Backtracking failed.")

    cuts.sort()
    return cuts


def make_boxes(img: Image.Image) -> List[Tuple[int, int, int, int]]:
    w, h = img.size

    if FORCE_EXACT_COUNT:
        ink = column_ink(img, ALPHA_THRESHOLD)
        cuts = forced_k_splits(ink, k=len(CHARS), min_width=MIN_GLYPH_WIDTH)

        xs = [0] + cuts + [w]
        boxes = []
        for i in range(len(xs) - 1):
            x0, x1 = xs[i], xs[i + 1]
            if x1 - x0 <= 0:
                continue
            box = (x0, 0, x1, h)
            if TRIM_VERTICAL:
                box = trim_box_vertical(img, box, ALPHA_THRESHOLD)
            boxes.append(box)

        if len(boxes) != len(CHARS):
            raise RuntimeError(f"Forced split produced {len(boxes)} boxes, expected {len(CHARS)}.")
        return boxes

    else:
        raise RuntimeError("Non-forced mode removed for simplicity in this version.")


def write_fnt(
    out_fnt: Path,
    page_name: str,
    glyphs: List[Glyph],
    atlas_w: int,
    atlas_h: int,
    line_height: int,
    base: int,
) -> None:
    lines = []
    lines.append(
        'info face="digits" size=32 bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=0 aa=0 '
        'padding=0,0,0,0 spacing=0,0'
    )
    lines.append(f"common lineHeight={line_height} base={base} scaleW={atlas_w} scaleH={atlas_h} pages=1 packed=0")
    lines.append(f'page id=0 file="{page_name}"')
    lines.append(f"chars count={len(glyphs)}")

    for g in glyphs:
        cid = ord(g.ch)
        lines.append(
            f"char id={cid} x={g.x} y={g.y} width={g.w} height={g.h} "
            f"xoffset={g.xoffset} yoffset={g.yoffset} xadvance={g.xadvance} page=0 chnl=15"
        )

    out_fnt.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent
    input_png = root / "digits.png"
    if not input_png.exists():
        # fallback: first png in folder
        pngs = sorted(root.glob("*.png"))
        if not pngs:
            raise FileNotFoundError(f"No PNG found next to this script: {root}")
        input_png = pngs[0]

    img = Image.open(input_png).convert("RGBA")

    boxes = make_boxes(img)

    # Crop glyphs
    glyph_imgs: List[Image.Image] = []
    glyph_sizes: List[Tuple[int, int]] = []
    for box in boxes:
        crop = img.crop(box)
        glyph_imgs.append(crop)
        glyph_sizes.append(crop.size)

    # Pack into single-row atlas
    pad = PADDING
    atlas_w = sum(w + pad * 2 for (w, h) in glyph_sizes)
    atlas_h = max(h + pad * 2 for (w, h) in glyph_sizes)

    atlas = Image.new("RGBA", (atlas_w, atlas_h), (0, 0, 0, 0))

    glyphs: List[Glyph] = []
    x_cursor = 0
    for ch, gimg in zip(CHARS, glyph_imgs):
        gw, gh = gimg.size
        x = x_cursor + pad
        y = pad
        atlas.alpha_composite(gimg, (x, y))

        # advance = glyph width (you can add extra spacing by increasing this)
        xadvance = gw
        glyphs.append(Glyph(ch=ch, x=x, y=y, w=gw, h=gh, xadvance=xadvance))

        x_cursor += gw + pad * 2

    atlas_name = f"{OUTPUT_BASENAME}_atlas.png"
    fnt_name = f"{OUTPUT_BASENAME}.fnt"

    out_png = root / atlas_name
    out_fnt = root / fnt_name

    atlas.save(out_png)

    line_height = atlas_h
    base = atlas_h - pad

    write_fnt(out_fnt, atlas_name, glyphs, atlas_w, atlas_h, line_height, base)

    print("Done!")
    print(f"Input:  {input_png}")
    print(f"Output: {out_png}")
    print(f"Output: {out_fnt}")
    print("\nGodot 4 reminders:")
    print("  - Select the atlas PNG in Godot  Import: Filter OFF, Mipmaps OFF Reimport")
    print("  - Create a FontFile and load the .fnt")


if __name__ == "__main__":
    main()
