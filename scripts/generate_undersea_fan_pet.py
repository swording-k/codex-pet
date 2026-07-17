#!/usr/bin/env python3
"""Generate deterministic undersea fan-pet V2 atlases.

This generator is intentionally deterministic. It keeps each character's
identity anchored to one reusable vector model so animation and look-direction
frames do not drift from frame to frame.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

COLUMNS = 8
ROWS = 11
CELL_W = 192
CELL_H = 208
ATLAS_W = COLUMNS * CELL_W
ATLAS_H = ROWS * CELL_H
SCALE = 4

LOOK_DIRECTIONS = [
    0,
    22.5,
    45,
    67.5,
    90,
    112.5,
    135,
    157.5,
    180,
    202.5,
    225,
    247.5,
    270,
    292.5,
    315,
    337.5,
]

CHARACTERS = {
    "spongebob": "SpongeBob",
    "patrick": "Patrick",
    "mr-krabs": "Mr. Krabs",
    "plankton": "Plankton",
    "squidward": "Squidward",
}


def sc(value: float) -> int:
    return round(value * SCALE)


def point(x: float, y: float) -> tuple[int, int]:
    return (sc(x), sc(y))


def box(x0: float, y0: float, x1: float, y1: float) -> tuple[int, int, int, int]:
    return (sc(x0), sc(y0), sc(x1), sc(y1))


def draw_line(draw: ImageDraw.ImageDraw, pts: list[tuple[float, float]], fill: tuple[int, int, int, int], width: float) -> None:
    draw.line([point(x, y) for x, y in pts], fill=fill, width=sc(width), joint="curve")


def draw_eye(draw: ImageDraw.ImageDraw, x: float, y: float, gaze: tuple[float, float], *, r: float = 12, iris=(72, 153, 213, 255)) -> None:
    outline = (42, 37, 25, 255)
    draw.ellipse(box(x - r, y - r, x + r, y + r), fill=(255, 255, 250, 255), outline=outline, width=sc(2))
    gx, gy = gaze
    draw.ellipse(box(x + gx - 4, y + gy - 4, x + gx + 4, y + gy + 4), fill=iris, outline=outline, width=sc(1))
    draw.ellipse(box(x + gx - 1.7, y + gy - 1.7, x + gx + 1.7, y + gy + 1.7), fill=(20, 20, 20, 255))


def draw_smile(draw: ImageDraw.ImageDraw, x0: float, y0: float, x1: float, y1: float, mood: str) -> None:
    outline = (42, 37, 25, 255)
    if mood == "sad":
        draw.arc(box(x0, y0 + 10, x1, y1 + 15), 200, 340, fill=outline, width=sc(3))
    elif mood == "surprised":
        draw.ellipse(box((x0 + x1) / 2 - 8, y0 + 8, (x0 + x1) / 2 + 8, y0 + 24), fill=(92, 45, 38, 255), outline=outline, width=sc(2))
    elif mood == "focused":
        draw.line([point(x0 + 9, y0 + 16), point(x1 - 9, y0 + 16)], fill=outline, width=sc(3))
    else:
        draw.arc(box(x0, y0, x1, y1), 10, 170, fill=outline, width=sc(3))


def pose_for_state(state: str, frame: int, direction: float | None) -> dict[str, object]:
    mood = "happy"
    arm_pose = "idle"
    bob = 0.0
    sway = 0.0
    leg_phase = frame * math.pi / 2
    gaze = (0.0, 0.0)

    if state == "idle":
        bob = math.sin(frame / 6 * math.tau) * 2
        mood = "blink" if frame == 2 else "happy"
    elif state == "running-right":
        sway = 5 * math.sin(frame / 8 * math.tau)
        gaze = (4, 0)
        arm_pose = "work"
    elif state == "running-left":
        sway = -5 * math.sin(frame / 8 * math.tau)
        gaze = (-4, 0)
        arm_pose = "work"
    elif state == "waving":
        arm_pose = "wave"
        gaze = (0, -1)
    elif state == "jumping":
        bob = [-8, -18, -28, -16, -6][frame]
        mood = "surprised" if frame == 2 else "happy"
        arm_pose = "wave" if frame == 2 else "idle"
    elif state == "failed":
        mood = "sad"
        bob = 5 if frame in (3, 4) else 0
        arm_pose = "failed"
        gaze = (0, 4)
    elif state == "waiting":
        mood = "surprised" if frame in (1, 4) else "happy"
        arm_pose = "wave" if frame in (1, 4) else "idle"
    elif state == "running":
        mood = "focused"
        arm_pose = "work"
        bob = math.sin(frame / 6 * math.tau) * 2
    elif state == "review":
        mood = "focused" if frame in (1, 2) else "happy"
        gaze = (3 if frame in (1, 2) else 0, -2)
    elif state == "look":
        assert direction is not None
        rad = math.radians(direction - 90)
        gaze = (math.cos(rad) * 5, math.sin(rad) * 5)
        if 150 <= direction <= 210:
            mood = "focused"
        elif direction in (0, 22.5, 337.5):
            mood = "surprised"

    return {"mood": mood, "arm_pose": arm_pose, "bob": bob, "sway": sway, "leg_phase": leg_phase, "gaze": gaze}


def draw_spongebob(draw: ImageDraw.ImageDraw, pose: dict[str, object]) -> None:
    ox = float(pose["sway"])
    oy = float(pose["bob"])
    mood = str(pose["mood"])
    gaze = pose["gaze"]  # type: ignore[assignment]
    arm_pose = str(pose["arm_pose"])
    leg_phase = float(pose["leg_phase"])

    outline = (43, 38, 24, 255)
    yellow = (245, 213, 58, 255)
    dark = (196, 159, 31, 255)
    skin = yellow
    for lx, stride in [(78, math.sin(leg_phase) * 8), (114, -math.sin(leg_phase) * 8)]:
        draw_line(draw, [(lx + ox, 134 + oy), (lx + ox + stride * 0.35, 160 + oy)], outline, 7)
        draw_line(draw, [(lx + ox, 134 + oy), (lx + ox + stride * 0.35, 160 + oy)], skin, 4)
        draw.ellipse(box(lx + ox + stride * 0.35 - 11, 158 + oy, lx + ox + stride * 0.35 + 12, 169 + oy), fill=(24, 24, 24, 255))

    left_arm = [(61 + ox, 90 + oy), (44 + ox, 102 + oy)]
    right_arm = [(130 + ox, 90 + oy), (148 + ox, 102 + oy)]
    if arm_pose == "wave":
        left_arm = [(61 + ox, 82 + oy), (42 + ox, 64 + oy), (36 + ox, 43 + oy)]
    elif arm_pose == "work":
        left_arm = [(61 + ox, 90 + oy), (45 + ox, 100 + oy), (55 + ox, 113 + oy)]
        right_arm = [(130 + ox, 90 + oy), (145 + ox, 100 + oy), (137 + ox, 113 + oy)]
    elif arm_pose == "failed":
        left_arm = [(61 + ox, 90 + oy), (49 + ox, 113 + oy)]
        right_arm = [(130 + ox, 90 + oy), (141 + ox, 113 + oy)]
    for arm in (left_arm, right_arm):
        draw_line(draw, arm, outline, 7)
        draw_line(draw, arm, skin, 4)
        hx, hy = arm[-1]
        draw.ellipse(box(hx - 4, hy - 4, hx + 4, hy + 4), fill=skin, outline=outline, width=sc(1))

    draw.rounded_rectangle(box(58 + ox, 34 + oy, 134 + ox, 130 + oy), radius=sc(10), fill=yellow, outline=outline, width=sc(3))
    for px, py, r in [(70, 50, 3), (120, 48, 2.5), (83, 71, 2.5), (113, 82, 3), (69, 104, 2.5), (125, 111, 3.5), (96, 119, 2)]:
        draw.ellipse(box(px + ox - r, py + oy - r, px + ox + r, py + oy + r), fill=dark)
    draw.rectangle(box(58 + ox, 104 + oy, 134 + ox, 120 + oy), fill=(247, 247, 238, 255))
    draw.rectangle(box(58 + ox, 120 + oy, 134 + ox, 132 + oy), fill=(145, 96, 43, 255))
    draw.polygon([point(91 + ox, 104 + oy), point(101 + ox, 104 + oy), point(96 + ox, 119 + oy)], fill=(190, 39, 44, 255), outline=outline)
    if mood == "blink":
        draw.arc(box(72 + ox, 62 + oy, 92 + ox, 77 + oy), 5, 175, fill=outline, width=sc(3))
        draw.arc(box(100 + ox, 62 + oy, 120 + ox, 77 + oy), 5, 175, fill=outline, width=sc(3))
    else:
        draw_eye(draw, 82 + ox, 62 + oy, gaze)  # type: ignore[arg-type]
        draw_eye(draw, 110 + ox, 62 + oy, gaze)  # type: ignore[arg-type]
    draw_smile(draw, 76 + ox, 76 + oy, 116 + ox, 104 + oy, mood)
    draw.rectangle(box(89 + ox, 88 + oy, 96 + ox, 99 + oy), fill=(255, 255, 250, 255), outline=outline, width=sc(1))
    draw.rectangle(box(96 + ox, 88 + oy, 103 + ox, 99 + oy), fill=(255, 255, 250, 255), outline=outline, width=sc(1))


def draw_patrick(draw: ImageDraw.ImageDraw, pose: dict[str, object]) -> None:
    ox = float(pose["sway"])
    oy = float(pose["bob"])
    mood = str(pose["mood"])
    gaze = pose["gaze"]  # type: ignore[assignment]
    outline = (53, 36, 39, 255)
    pink = (244, 139, 154, 255)
    shorts = (121, 199, 97, 255)
    flower = (119, 80, 161, 255)
    draw_line(draw, [(72 + ox, 136 + oy), (66 + ox, 162 + oy)], outline, 8)
    draw_line(draw, [(120 + ox, 136 + oy), (126 + ox, 162 + oy)], outline, 8)
    draw.polygon([point(96 + ox, 30 + oy), point(54 + ox, 137 + oy), point(138 + ox, 137 + oy)], fill=pink, outline=outline)
    draw.rectangle(box(58 + ox, 118 + oy, 134 + ox, 143 + oy), fill=shorts, outline=outline, width=sc(2))
    for px in (74, 113):
        draw.ellipse(box(px + ox - 8, 124 + oy - 4, px + ox + 8, 124 + oy + 4), fill=flower)
    if str(pose["arm_pose"]) == "wave":
        left = [(58 + ox, 85 + oy), (35 + ox, 58 + oy)]
    else:
        left = [(58 + ox, 90 + oy), (34 + ox, 110 + oy)]
    right = [(134 + ox, 90 + oy), (158 + ox, 110 + oy)]
    for arm in (left, right):
        draw_line(draw, arm, outline, 8)
        draw_line(draw, arm, pink, 5)
    draw_eye(draw, 86 + ox, 76 + oy, gaze, r=9, iris=(45, 45, 45, 255))  # type: ignore[arg-type]
    draw_eye(draw, 108 + ox, 76 + oy, gaze, r=9, iris=(45, 45, 45, 255))  # type: ignore[arg-type]
    draw_smile(draw, 77 + ox, 87 + oy, 117 + ox, 113 + oy, mood)


def draw_krabs(draw: ImageDraw.ImageDraw, pose: dict[str, object]) -> None:
    ox = float(pose["sway"])
    oy = float(pose["bob"])
    mood = str(pose["mood"])
    gaze = pose["gaze"]  # type: ignore[assignment]
    outline = (50, 25, 24, 255)
    red = (210, 42, 39, 255)
    shirt = (117, 198, 214, 255)
    pants = (76, 71, 168, 255)
    for lx in (76, 116):
        draw_line(draw, [(lx + ox, 132 + oy), (lx - 8 + ox, 162 + oy)], outline, 7)
        draw_line(draw, [(lx + ox, 132 + oy), (lx - 8 + ox, 162 + oy)], red, 4)
    draw.ellipse(box(55 + ox, 55 + oy, 137 + ox, 137 + oy), fill=red, outline=outline, width=sc(3))
    draw.rectangle(box(62 + ox, 104 + oy, 130 + ox, 132 + oy), fill=shirt, outline=outline, width=sc(2))
    draw.rectangle(box(70 + ox, 128 + oy, 122 + ox, 143 + oy), fill=pants, outline=outline, width=sc(2))
    for ex in (80, 112):
        draw_line(draw, [(ex + ox, 60 + oy), (ex + ox, 31 + oy)], outline, 6)
        draw_line(draw, [(ex + ox, 60 + oy), (ex + ox, 31 + oy)], red, 3)
        draw_eye(draw, ex + ox, 30 + oy, gaze, r=8, iris=(35, 45, 35, 255))  # type: ignore[arg-type]
    if str(pose["arm_pose"]) == "wave":
        left = [(58 + ox, 87 + oy), (34 + ox, 62 + oy)]
    else:
        left = [(58 + ox, 92 + oy), (31 + ox, 107 + oy)]
    right = [(134 + ox, 92 + oy), (161 + ox, 107 + oy)]
    for arm, claw_x, claw_y in ((left, left[-1][0], left[-1][1]), (right, right[-1][0], right[-1][1])):
        draw_line(draw, arm, outline, 8)
        draw_line(draw, arm, red, 5)
        draw.ellipse(box(claw_x - 11, claw_y - 8, claw_x + 11, claw_y + 10), fill=red, outline=outline, width=sc(2))
    draw_smile(draw, 78 + ox, 82 + oy, 116 + ox, 111 + oy, mood)


def draw_plankton(draw: ImageDraw.ImageDraw, pose: dict[str, object]) -> None:
    ox = float(pose["sway"])
    oy = float(pose["bob"])
    mood = "focused" if str(pose["mood"]) == "happy" else str(pose["mood"])
    gaze = pose["gaze"]  # type: ignore[assignment]
    outline = (25, 47, 35, 255)
    green = (78, 157, 94, 255)
    draw_line(draw, [(84 + ox, 57 + oy), (68 + ox, 22 + oy)], outline, 4)
    draw_line(draw, [(108 + ox, 57 + oy), (124 + ox, 22 + oy)], outline, 4)
    draw.ellipse(box(69 + ox, 50 + oy, 123 + ox, 150 + oy), fill=green, outline=outline, width=sc(3))
    draw_eye(draw, 96 + ox, 84 + oy, gaze, r=18, iris=(198, 44, 55, 255))  # type: ignore[arg-type]
    draw_smile(draw, 82 + ox, 104 + oy, 110 + ox, 129 + oy, mood)
    if str(pose["arm_pose"]) == "wave":
        left = [(73 + ox, 105 + oy), (50 + ox, 79 + oy)]
    else:
        left = [(73 + ox, 109 + oy), (52 + ox, 121 + oy)]
    right = [(119 + ox, 109 + oy), (140 + ox, 121 + oy)]
    for arm in (left, right):
        draw_line(draw, arm, outline, 5)
        draw_line(draw, arm, green, 3)
    for lx in (84, 108):
        draw_line(draw, [(lx + ox, 148 + oy), (lx + ox, 166 + oy)], outline, 5)


def draw_squidward(draw: ImageDraw.ImageDraw, pose: dict[str, object]) -> None:
    ox = float(pose["sway"])
    oy = float(pose["bob"])
    mood = "focused" if str(pose["mood"]) == "happy" else str(pose["mood"])
    gaze = pose["gaze"]  # type: ignore[assignment]
    outline = (37, 62, 58, 255)
    teal = (116, 190, 181, 255)
    shirt = (121, 87, 52, 255)
    draw.ellipse(box(64 + ox, 30 + oy, 128 + ox, 93 + oy), fill=teal, outline=outline, width=sc(3))
    draw.rounded_rectangle(box(83 + ox, 77 + oy, 109 + ox, 126 + oy), radius=sc(12), fill=teal, outline=outline, width=sc(3))
    draw.rectangle(box(72 + ox, 112 + oy, 120 + ox, 138 + oy), fill=shirt, outline=outline, width=sc(2))
    draw.rounded_rectangle(box(86 + ox, 72 + oy, 106 + ox, 108 + oy), radius=sc(9), fill=teal, outline=outline, width=sc(2))
    draw_eye(draw, 84 + ox, 60 + oy, gaze, r=10, iris=(189, 169, 51, 255))  # type: ignore[arg-type]
    draw_eye(draw, 108 + ox, 60 + oy, gaze, r=10, iris=(189, 169, 51, 255))  # type: ignore[arg-type]
    draw_smile(draw, 80 + ox, 92 + oy, 112 + ox, 118 + oy, mood)
    if str(pose["arm_pose"]) == "wave":
        left = [(73 + ox, 119 + oy), (50 + ox, 91 + oy)]
    else:
        left = [(73 + ox, 121 + oy), (50 + ox, 133 + oy)]
    right = [(119 + ox, 121 + oy), (142 + ox, 133 + oy)]
    for arm in (left, right):
        draw_line(draw, arm, outline, 6)
        draw_line(draw, arm, teal, 4)
    for lx in (84, 96, 108):
        draw_line(draw, [(lx + ox, 137 + oy), (lx - 7 + ox, 165 + oy)], outline, 5)
        draw_line(draw, [(lx + ox, 137 + oy), (lx - 7 + ox, 165 + oy)], teal, 3)


DRAWERS = {
    "spongebob": draw_spongebob,
    "patrick": draw_patrick,
    "mr-krabs": draw_krabs,
    "plankton": draw_plankton,
    "squidward": draw_squidward,
}


def render_cell(character: str, state: str, frame: int, direction: float | None = None) -> Image.Image:
    canvas = Image.new("RGBA", (CELL_W * SCALE, CELL_H * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    DRAWERS[character](draw, pose_for_state(state, frame, direction))
    return canvas.resize((CELL_W, CELL_H), Image.Resampling.LANCZOS)


def build_atlas(character: str) -> Image.Image:
    atlas = Image.new("RGBA", (ATLAS_W, ATLAS_H), (0, 0, 0, 0))
    states = [
        "idle",
        "running-right",
        "running-left",
        "waving",
        "jumping",
        "failed",
        "waiting",
        "running",
        "review",
    ]
    frame_counts = {
        "idle": 6,
        "running-right": 8,
        "running-left": 8,
        "waving": 4,
        "jumping": 5,
        "failed": 8,
        "waiting": 6,
        "running": 6,
        "review": 6,
    }
    for row, state in enumerate(states):
        for column in range(frame_counts[state]):
            atlas.alpha_composite(render_cell(character, state, column), (column * CELL_W, row * CELL_H))

    atlas.alpha_composite(render_cell(character, "idle", 0), (6 * CELL_W, 0))

    for index, degrees in enumerate(LOOK_DIRECTIONS):
        row = 9 + index // COLUMNS
        column = index % COLUMNS
        atlas.alpha_composite(render_cell(character, "look", index, degrees), (column * CELL_W, row * CELL_H))
    return atlas


def clear_transparent_rgb(image: Image.Image) -> Image.Image:
    data = bytearray(image.convert("RGBA").tobytes())
    for index in range(0, len(data), 4):
        if data[index + 3] == 0:
            data[index] = data[index + 1] = data[index + 2] = 0
    return Image.frombytes("RGBA", image.size, bytes(data))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--character", choices=sorted(CHARACTERS), default="spongebob")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    atlas = clear_transparent_rgb(build_atlas(args.character))
    png_path = output_dir / "spritesheet.png"
    webp_path = output_dir / "spritesheet.webp"
    atlas.save(png_path)
    atlas.save(webp_path, format="WEBP", lossless=True, quality=100, method=6, exact=True)

    manifest = {
        "generator": Path(__file__).name,
        "character": args.character,
        "displayName": CHARACTERS[args.character],
        "spriteVersionNumber": 2,
        "size": {"width": ATLAS_W, "height": ATLAS_H},
        "cell": {"width": CELL_W, "height": CELL_H},
        "lookDirections": LOOK_DIRECTIONS,
        "identityStrategy": "deterministic vector model shared across all animation states",
    }
    (output_dir / "generation-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "character": args.character, "png": str(png_path), "webp": str(webp_path)}, indent=2))


if __name__ == "__main__":
    main()
