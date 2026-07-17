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

    outline = (34, 30, 22, 255)
    yellow = (248, 219, 55, 255)
    yellow_light = (255, 232, 82, 255)
    dark = (179, 143, 25, 255)
    skin = yellow
    shoe = (18, 18, 18, 255)
    sock_blue = (62, 142, 205, 255)
    sock_red = (206, 40, 43, 255)

    # Legs, socks, shoes. Keep the feet grounded so the app-sized sprite
    # does not look like it floats.
    for lx, stride in [(78, math.sin(leg_phase) * 9), (114, -math.sin(leg_phase) * 9)]:
        knee_x = lx + ox + stride * 0.22
        foot_x = lx + ox + stride * 0.45
        draw_line(draw, [(lx + ox, 132 + oy), (knee_x, 151 + oy), (foot_x, 163 + oy)], outline, 7)
        draw_line(draw, [(lx + ox, 132 + oy), (knee_x, 151 + oy), (foot_x, 163 + oy)], skin, 4)
        draw.rectangle(box(foot_x - 3, 151 + oy, foot_x + 3, 162 + oy), fill=(255, 252, 241, 255), outline=outline, width=sc(1))
        draw.rectangle(box(foot_x - 3, 153 + oy, foot_x + 3, 155 + oy), fill=sock_blue)
        draw.rectangle(box(foot_x - 3, 156 + oy, foot_x + 3, 158 + oy), fill=sock_red)
        draw.ellipse(box(foot_x - 13, 160 + oy, foot_x + 14, 171 + oy), fill=shoe, outline=outline, width=sc(1))

    left_arm = [(58 + ox, 84 + oy), (40 + ox, 101 + oy)]
    right_arm = [(134 + ox, 84 + oy), (153 + ox, 101 + oy)]
    if arm_pose == "wave":
        left_arm = [(58 + ox, 80 + oy), (41 + ox, 60 + oy), (36 + ox, 38 + oy)]
        right_arm = [(134 + ox, 84 + oy), (151 + ox, 101 + oy)]
    elif arm_pose == "work":
        left_arm = [(58 + ox, 88 + oy), (43 + ox, 99 + oy), (54 + ox, 113 + oy)]
        right_arm = [(134 + ox, 88 + oy), (149 + ox, 99 + oy), (139 + ox, 113 + oy)]
    elif arm_pose == "failed":
        left_arm = [(58 + ox, 90 + oy), (44 + ox, 114 + oy)]
        right_arm = [(134 + ox, 90 + oy), (148 + ox, 114 + oy)]
    for arm in (left_arm, right_arm):
        draw_line(draw, arm, outline, 8)
        draw_line(draw, arm, skin, 5)
        hx, hy = arm[-1]
        draw.ellipse(box(hx - 5, hy - 5, hx + 5, hy + 5), fill=skin, outline=outline, width=sc(1))

    # Slightly irregular square silhouette: much more characterful than a
    # perfect rounded rectangle, while still remaining clean at 192x208.
    body_points = [
        (59 + ox, 33 + oy), (69 + ox, 29 + oy), (122 + ox, 30 + oy),
        (134 + ox, 37 + oy), (137 + ox, 58 + oy), (133 + ox, 76 + oy),
        (137 + ox, 100 + oy), (130 + ox, 129 + oy), (115 + ox, 134 + oy),
        (72 + ox, 132 + oy), (58 + ox, 124 + oy), (55 + ox, 101 + oy),
        (58 + ox, 80 + oy), (54 + ox, 57 + oy),
    ]
    draw.polygon([point(x, y) for x, y in body_points], fill=yellow, outline=outline)
    draw.line([point(x, y) for x, y in body_points + [body_points[0]]], fill=outline, width=sc(3), joint="curve")
    draw.polygon([point(67 + ox, 38 + oy), point(122 + ox, 36 + oy), point(130 + ox, 52 + oy), point(125 + ox, 92 + oy), point(68 + ox, 92 + oy), point(62 + ox, 54 + oy)], fill=yellow_light)

    for px, py, r in [(69, 47, 3), (121, 47, 2.5), (80, 69, 2.8), (116, 78, 3.2), (68, 101, 2.6), (125, 113, 3.5), (96, 121, 2.2), (91, 42, 1.8)]:
        draw.ellipse(box(px + ox - r, py + oy - r, px + ox + r, py + oy + r), fill=dark)

    # Shirt / shorts are part of the identity, make them readable.
    draw.rectangle(box(57 + ox, 105 + oy, 134 + ox, 121 + oy), fill=(252, 249, 235, 255), outline=outline, width=sc(2))
    draw.rectangle(box(58 + ox, 121 + oy, 133 + ox, 136 + oy), fill=(139, 89, 43, 255), outline=outline, width=sc(2))
    draw.rectangle(box(70 + ox, 122 + oy, 82 + ox, 130 + oy), fill=(102, 62, 31, 255))
    draw.rectangle(box(109 + ox, 122 + oy, 121 + ox, 130 + oy), fill=(102, 62, 31, 255))
    draw.polygon([point(90 + ox, 105 + oy), point(102 + ox, 105 + oy), point(96 + ox, 122 + oy)], fill=(190, 39, 44, 255), outline=outline)

    if mood == "blink":
        draw.arc(box(69 + ox, 58 + oy, 95 + ox, 75 + oy), 5, 175, fill=outline, width=sc(3))
        draw.arc(box(98 + ox, 58 + oy, 124 + ox, 75 + oy), 5, 175, fill=outline, width=sc(3))
    else:
        draw_eye(draw, 82 + ox, 64 + oy, gaze, r=14)  # type: ignore[arg-type]
        draw_eye(draw, 111 + ox, 64 + oy, gaze, r=14)  # type: ignore[arg-type]
        # Eyelashes read well at final pet size and help avoid "generic square".
        for ex in (82, 111):
            draw.line([point(ex - 10 + ox, 51 + oy), point(ex - 14 + ox, 45 + oy)], fill=outline, width=sc(2))
            draw.line([point(ex + ox, 49 + oy), point(ex + ox, 43 + oy)], fill=outline, width=sc(2))
            draw.line([point(ex + 10 + ox, 51 + oy), point(ex + 14 + ox, 45 + oy)], fill=outline, width=sc(2))
    # Cheeks and expressive smile.
    draw.ellipse(box(72 + ox, 83 + oy, 80 + ox, 91 + oy), fill=(247, 121, 82, 255))
    draw.ellipse(box(113 + ox, 83 + oy, 121 + ox, 91 + oy), fill=(247, 121, 82, 255))
    draw_smile(draw, 76 + ox, 78 + oy, 118 + ox, 108 + oy, mood)
    draw.rectangle(box(89 + ox, 91 + oy, 96 + ox, 104 + oy), fill=(255, 255, 250, 255), outline=outline, width=sc(1))
    draw.rectangle(box(96 + ox, 91 + oy, 103 + ox, 104 + oy), fill=(255, 255, 250, 255), outline=outline, width=sc(1))


def draw_patrick(draw: ImageDraw.ImageDraw, pose: dict[str, object]) -> None:
    ox = float(pose["sway"])
    oy = float(pose["bob"])
    mood = str(pose["mood"])
    gaze = pose["gaze"]  # type: ignore[assignment]
    outline = (58, 37, 42, 255)
    pink = (245, 139, 154, 255)
    pink_light = (255, 163, 176, 255)
    shorts = (116, 202, 92, 255)
    flower = (121, 75, 164, 255)
    for lx, stride in [(75, math.sin(float(pose["leg_phase"])) * 6), (116, -math.sin(float(pose["leg_phase"])) * 6)]:
        draw_line(draw, [(lx + ox, 136 + oy), (lx + stride * 0.35 + ox, 162 + oy)], outline, 9)
        draw_line(draw, [(lx + ox, 136 + oy), (lx + stride * 0.35 + ox, 162 + oy)], pink, 6)
        draw.ellipse(box(lx + stride * 0.35 + ox - 9, 159 + oy, lx + stride * 0.35 + ox + 11, 170 + oy), fill=pink, outline=outline, width=sc(1))
    body = [
        (95 + ox, 26 + oy), (108 + ox, 57 + oy), (139 + ox, 62 + oy),
        (121 + ox, 96 + oy), (139 + ox, 139 + oy), (109 + ox, 135 + oy),
        (96 + ox, 154 + oy), (82 + ox, 135 + oy), (52 + ox, 139 + oy),
        (70 + ox, 96 + oy), (53 + ox, 62 + oy), (84 + ox, 57 + oy),
    ]
    draw.polygon([point(x, y) for x, y in body], fill=pink, outline=outline)
    draw.line([point(x, y) for x, y in body + [body[0]]], fill=outline, width=sc(3), joint="curve")
    draw.polygon([point(92 + ox, 42 + oy), point(104 + ox, 68 + oy), point(117 + ox, 83 + oy), point(103 + ox, 119 + oy), point(84 + ox, 118 + oy), point(73 + ox, 83 + oy)], fill=pink_light)
    draw.polygon([point(61 + ox, 116 + oy), point(132 + ox, 116 + oy), point(137 + ox, 139 + oy), point(111 + ox, 146 + oy), point(96 + ox, 134 + oy), point(80 + ox, 146 + oy), point(55 + ox, 139 + oy)], fill=shorts, outline=outline)
    for px, py in [(75, 126), (112, 128), (95, 139)]:
        draw.ellipse(box(px + ox - 8, py + oy - 5, px + ox + 8, py + oy + 5), fill=flower, outline=(86, 56, 125, 255), width=sc(1))
    if str(pose["arm_pose"]) == "wave":
        left = [(58 + ox, 85 + oy), (35 + ox, 58 + oy)]
    else:
        left = [(58 + ox, 90 + oy), (34 + ox, 110 + oy)]
    right = [(134 + ox, 90 + oy), (158 + ox, 110 + oy)]
    for arm in (left, right):
        draw_line(draw, arm, outline, 10)
        draw_line(draw, arm, pink, 7)
        hx, hy = arm[-1]
        draw.ellipse(box(hx - 7, hy - 6, hx + 7, hy + 6), fill=pink, outline=outline, width=sc(1))
    draw_eye(draw, 86 + ox, 74 + oy, gaze, r=10, iris=(45, 45, 45, 255))  # type: ignore[arg-type]
    draw_eye(draw, 108 + ox, 74 + oy, gaze, r=10, iris=(45, 45, 45, 255))  # type: ignore[arg-type]
    draw.ellipse(box(73 + ox, 91 + oy, 81 + ox, 99 + oy), fill=(235, 106, 128, 255))
    draw.ellipse(box(112 + ox, 91 + oy, 120 + ox, 99 + oy), fill=(235, 106, 128, 255))
    draw_smile(draw, 77 + ox, 86 + oy, 117 + ox, 116 + oy, mood)


def draw_krabs(draw: ImageDraw.ImageDraw, pose: dict[str, object]) -> None:
    ox = float(pose["sway"])
    oy = float(pose["bob"])
    mood = str(pose["mood"])
    gaze = pose["gaze"]  # type: ignore[assignment]
    outline = (52, 24, 22, 255)
    red = (212, 42, 39, 255)
    red_light = (238, 67, 54, 255)
    shirt = (112, 203, 220, 255)
    pants = (75, 68, 166, 255)
    for lx, stride in [(75, math.sin(float(pose["leg_phase"])) * 5), (116, -math.sin(float(pose["leg_phase"])) * 5)]:
        draw_line(draw, [(lx + ox, 132 + oy), (lx - 6 + stride + ox, 162 + oy)], outline, 8)
        draw_line(draw, [(lx + ox, 132 + oy), (lx - 6 + stride + ox, 162 + oy)], red, 5)
        draw.ellipse(box(lx - 16 + stride + ox, 159 + oy, lx + 2 + stride + ox, 169 + oy), fill=(42, 25, 24, 255))
    draw.ellipse(box(52 + ox, 54 + oy, 140 + ox, 139 + oy), fill=red, outline=outline, width=sc(3))
    draw.pieslice(box(59 + ox, 62 + oy, 133 + ox, 133 + oy), 205, 335, fill=red_light)
    draw.rectangle(box(61 + ox, 103 + oy, 131 + ox, 132 + oy), fill=shirt, outline=outline, width=sc(2))
    draw.polygon([point(66 + ox, 103 + oy), point(96 + ox, 124 + oy), point(126 + ox, 103 + oy)], fill=(236, 244, 231, 255), outline=outline)
    draw.rectangle(box(70 + ox, 128 + oy, 122 + ox, 145 + oy), fill=pants, outline=outline, width=sc(2))
    draw.rectangle(box(91 + ox, 128 + oy, 101 + ox, 145 + oy), fill=(48, 45, 112, 255))
    for ex in (80, 112):
        draw_line(draw, [(ex + ox, 61 + oy), (ex + ox, 28 + oy)], outline, 7)
        draw_line(draw, [(ex + ox, 61 + oy), (ex + ox, 28 + oy)], red, 4)
        draw_eye(draw, ex + ox, 28 + oy, gaze, r=9, iris=(33, 48, 37, 255))  # type: ignore[arg-type]
    if str(pose["arm_pose"]) == "wave":
        left = [(58 + ox, 87 + oy), (34 + ox, 62 + oy)]
    else:
        left = [(58 + ox, 92 + oy), (31 + ox, 107 + oy)]
    right = [(134 + ox, 92 + oy), (161 + ox, 107 + oy)]
    for arm, claw_x, claw_y in ((left, left[-1][0], left[-1][1]), (right, right[-1][0], right[-1][1])):
        draw_line(draw, arm, outline, 9)
        draw_line(draw, arm, red, 6)
        draw.ellipse(box(claw_x - 13, claw_y - 10, claw_x + 10, claw_y + 12), fill=red, outline=outline, width=sc(2))
        draw.pieslice(box(claw_x - 18, claw_y - 15, claw_x + 3, claw_y + 6), 220, 45, fill=red_light, outline=outline, width=sc(2))
        draw.line([point(claw_x - 3, claw_y - 2), point(claw_x + 10, claw_y - 13)], fill=outline, width=sc(2))
    draw_smile(draw, 78 + ox, 82 + oy, 116 + ox, 113 + oy, mood)


def draw_plankton(draw: ImageDraw.ImageDraw, pose: dict[str, object]) -> None:
    ox = float(pose["sway"])
    oy = float(pose["bob"])
    mood = "focused" if str(pose["mood"]) == "happy" else str(pose["mood"])
    gaze = pose["gaze"]  # type: ignore[assignment]
    outline = (23, 48, 35, 255)
    green = (79, 164, 93, 255)
    green_light = (111, 193, 113, 255)
    draw_line(draw, [(84 + ox, 58 + oy), (69 + ox, 25 + oy), (64 + ox, 15 + oy)], outline, 5)
    draw_line(draw, [(108 + ox, 58 + oy), (123 + ox, 25 + oy), (128 + ox, 15 + oy)], outline, 5)
    draw.ellipse(box(69 + ox, 48 + oy, 123 + ox, 154 + oy), fill=green, outline=outline, width=sc(3))
    draw.ellipse(box(82 + ox, 57 + oy, 110 + ox, 142 + oy), fill=green_light)
    draw_eye(draw, 96 + ox, 84 + oy, gaze, r=20, iris=(200, 42, 54, 255))  # type: ignore[arg-type]
    draw.line([point(77 + ox, 68 + oy), point(88 + ox, 63 + oy)], fill=outline, width=sc(3))
    draw.line([point(104 + ox, 63 + oy), point(116 + ox, 68 + oy)], fill=outline, width=sc(3))
    draw_smile(draw, 80 + ox, 107 + oy, 112 + ox, 133 + oy, mood)
    if str(pose["arm_pose"]) == "wave":
        left = [(73 + ox, 105 + oy), (50 + ox, 79 + oy)]
    else:
        left = [(73 + ox, 109 + oy), (52 + ox, 121 + oy)]
    right = [(119 + ox, 109 + oy), (140 + ox, 121 + oy)]
    for arm in (left, right):
        draw_line(draw, arm, outline, 6)
        draw_line(draw, arm, green, 4)
    for lx in (84, 108):
        draw_line(draw, [(lx + ox, 149 + oy), (lx + ox, 166 + oy)], outline, 5)
        draw.ellipse(box(lx + ox - 5, 164 + oy, lx + ox + 5, 170 + oy), fill=outline)


def draw_squidward(draw: ImageDraw.ImageDraw, pose: dict[str, object]) -> None:
    ox = float(pose["sway"])
    oy = float(pose["bob"])
    mood = "focused" if str(pose["mood"]) == "happy" else str(pose["mood"])
    gaze = pose["gaze"]  # type: ignore[assignment]
    outline = (37, 62, 58, 255)
    teal = (114, 190, 181, 255)
    teal_light = (146, 210, 201, 255)
    shirt = (122, 86, 52, 255)
    draw.ellipse(box(60 + ox, 27 + oy, 132 + ox, 97 + oy), fill=teal, outline=outline, width=sc(3))
    draw.ellipse(box(73 + ox, 39 + oy, 119 + ox, 84 + oy), fill=teal_light)
    draw.rounded_rectangle(box(82 + ox, 78 + oy, 110 + ox, 128 + oy), radius=sc(12), fill=teal, outline=outline, width=sc(3))
    draw.polygon([point(70 + ox, 112 + oy), point(122 + ox, 112 + oy), point(129 + ox, 139 + oy), point(63 + ox, 139 + oy)], fill=shirt, outline=outline)
    draw.rounded_rectangle(box(85 + ox, 72 + oy, 107 + ox, 112 + oy), radius=sc(10), fill=teal, outline=outline, width=sc(2))
    draw.line([point(96 + ox, 89 + oy), point(96 + ox, 107 + oy)], fill=outline, width=sc(2))
    draw_eye(draw, 83 + ox, 61 + oy, gaze, r=11, iris=(191, 169, 51, 255))  # type: ignore[arg-type]
    draw_eye(draw, 109 + ox, 61 + oy, gaze, r=11, iris=(191, 169, 51, 255))  # type: ignore[arg-type]
    draw.line([point(75 + ox, 50 + oy), point(91 + ox, 49 + oy)], fill=outline, width=sc(2))
    draw.line([point(101 + ox, 49 + oy), point(117 + ox, 50 + oy)], fill=outline, width=sc(2))
    draw_smile(draw, 80 + ox, 94 + oy, 112 + ox, 121 + oy, mood)
    if str(pose["arm_pose"]) == "wave":
        left = [(73 + ox, 119 + oy), (50 + ox, 91 + oy)]
    else:
        left = [(73 + ox, 121 + oy), (50 + ox, 133 + oy)]
    right = [(119 + ox, 121 + oy), (142 + ox, 133 + oy)]
    for arm in (left, right):
        draw_line(draw, arm, outline, 7)
        draw_line(draw, arm, teal, 5)
    for lx, stride in [(82, -5), (96, 0), (110, 5)]:
        draw_line(draw, [(lx + ox, 137 + oy), (lx + stride + ox, 165 + oy)], outline, 6)
        draw_line(draw, [(lx + ox, 137 + oy), (lx + stride + ox, 165 + oy)], teal, 4)
        draw.ellipse(box(lx + stride + ox - 5, 163 + oy, lx + stride + ox + 7, 170 + oy), fill=teal, outline=outline, width=sc(1))


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
