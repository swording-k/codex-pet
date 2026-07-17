#!/usr/bin/env python3
"""Assemble a v2 Codex pet atlas from a base atlas and registered look rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image

COLUMNS = 8
STANDARD_ROWS = 9
EXTENDED_ROWS = 11
CELL_WIDTH = 192
CELL_HEIGHT = 208
ATLAS_WIDTH = COLUMNS * CELL_WIDTH
STANDARD_HEIGHT = STANDARD_ROWS * CELL_HEIGHT
EXTENDED_HEIGHT = EXTENDED_ROWS * CELL_HEIGHT
LOOK_DIRECTION_LABELS = [
    "000",
    "022.5",
    "045",
    "067.5",
    "090",
    "112.5",
    "135",
    "157.5",
    "180",
    "202.5",
    "225",
    "247.5",
    "270",
    "292.5",
    "315",
    "337.5",
]


def clear_transparent_rgb(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    data = bytearray(rgba.tobytes())
    for index in range(0, len(data), 4):
        if data[index + 3] == 0:
            data[index] = data[index + 1] = data[index + 2] = 0
    return Image.frombytes("RGBA", rgba.size, bytes(data))


def visible_cell(atlas: Image.Image) -> Image.Image:
    for column in [6, 0, 1, 2, 3, 4, 5, 7]:
        cell = atlas.crop(
            (
                column * CELL_WIDTH,
                0,
                (column + 1) * CELL_WIDTH,
                CELL_HEIGHT,
            )
        )
        if cell.getbbox() is not None:
            return cell
    raise SystemExit("base atlas must contain at least one visible neutral frame in row 0")


def load_base(path: Path) -> Image.Image:
    with Image.open(path) as opened:
        base = opened.convert("RGBA")
    if base.width != ATLAS_WIDTH or base.height not in {STANDARD_HEIGHT, EXTENDED_HEIGHT}:
        raise SystemExit(
            f"base atlas must be {ATLAS_WIDTH}x{STANDARD_HEIGHT} or "
            f"{ATLAS_WIDTH}x{EXTENDED_HEIGHT}; got {base.width}x{base.height}"
        )
    output = Image.new("RGBA", (ATLAS_WIDTH, EXTENDED_HEIGHT), (0, 0, 0, 0))
    output.alpha_composite(base.crop((0, 0, ATLAS_WIDTH, STANDARD_HEIGHT)), (0, 0))
    return output


def load_registered_row(path: Path) -> Image.Image:
    with Image.open(path) as opened:
        row = opened.convert("RGBA")
    if row.size != (ATLAS_WIDTH, CELL_HEIGHT):
        raise SystemExit(
            f"registered row must be {ATLAS_WIDTH}x{CELL_HEIGHT}; "
            f"got {row.width}x{row.height}"
        )
    return row


def write_manifest(path: Path, atlas_path: Path) -> None:
    manifest = {
        "spritesheetPath": atlas_path.name,
        "spritesheetLayout": {
            "columns": COLUMNS,
            "rows": EXTENDED_ROWS,
            "cellWidth": CELL_WIDTH,
            "cellHeight": CELL_HEIGHT,
            "lookDirectionCount": len(LOOK_DIRECTION_LABELS),
            "neutralLookFrame": {"rowIndex": 0, "columnIndex": 6},
        },
        "lookDirections": [
            {
                "degrees": float(label),
                "rowIndex": STANDARD_ROWS + index // COLUMNS,
                "columnIndex": index % COLUMNS,
            }
            for index, label in enumerate(LOOK_DIRECTION_LABELS)
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-atlas", required=True)
    parser.add_argument("--registered-row-9", required=True)
    parser.add_argument("--registered-row-10", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--webp-output", required=True)
    parser.add_argument("--manifest-output")
    args = parser.parse_args()

    base_path = Path(args.base_atlas).expanduser().resolve()
    atlas = load_base(base_path)
    neutral = visible_cell(atlas)
    row9 = load_registered_row(Path(args.registered_row_9).expanduser().resolve())
    row10 = load_registered_row(Path(args.registered_row_10).expanduser().resolve())

    atlas.alpha_composite(neutral, (6 * CELL_WIDTH, 0))
    atlas.alpha_composite(row9, (0, 9 * CELL_HEIGHT))
    atlas.alpha_composite(row10, (0, 10 * CELL_HEIGHT))
    atlas = clear_transparent_rgb(atlas)

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(output)
    print(f"wrote {output}")

    webp_output = Path(args.webp_output).expanduser().resolve()
    webp_output.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(webp_output, format="WEBP", lossless=True, quality=100, method=6, exact=True)
    print(f"wrote {webp_output}")

    if args.manifest_output:
        manifest_output = Path(args.manifest_output).expanduser().resolve()
        write_manifest(manifest_output, webp_output)
        print(f"wrote {manifest_output}")


if __name__ == "__main__":
    main()
