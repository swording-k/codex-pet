#!/usr/bin/env python3
"""Assemble a v2 atlas by reusing cells from an existing 8x9 pet atlas."""

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


def atlas_cell(atlas: Image.Image, row: int, column: int) -> Image.Image:
    if row < 0 or row >= STANDARD_ROWS or column < 0 or column >= COLUMNS:
        raise SystemExit(f"cell out of range: row={row}, column={column}")
    return atlas.crop(
        (
            column * CELL_WIDTH,
            row * CELL_HEIGHT,
            (column + 1) * CELL_WIDTH,
            (row + 1) * CELL_HEIGHT,
        )
    )


def first_visible_idle(atlas: Image.Image) -> Image.Image:
    for column in [6, 0, 1, 2, 3, 4, 5, 7]:
        cell = atlas_cell(atlas, 0, column)
        if cell.getbbox() is not None:
            return cell
    raise SystemExit("base atlas row 0 has no visible neutral frame")


def load_mapping(path: Path) -> dict[str, dict[str, object]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    directions = data.get("directions")
    if not isinstance(directions, dict):
        raise SystemExit("mapping JSON must contain a directions object")
    missing = [label for label in LOOK_DIRECTION_LABELS if label not in directions]
    if missing:
        raise SystemExit(f"mapping is missing directions: {', '.join(missing)}")
    return directions


def mapped_cell(
    atlas: Image.Image,
    mapping: dict[str, object],
) -> Image.Image:
    try:
        row = int(mapping["row"])
        column = int(mapping["column"])
    except (KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f"invalid mapping entry: {mapping!r}") from exc
    cell = atlas_cell(atlas, row, column)
    if bool(mapping.get("flipX", False)):
        cell = cell.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if cell.getbbox() is None:
        raise SystemExit(f"mapped cell is empty: row={row}, column={column}")
    return cell


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
    parser.add_argument("--mapping", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--webp-output", required=True)
    parser.add_argument("--manifest-output")
    parser.add_argument("--row9-output")
    parser.add_argument("--row10-output")
    args = parser.parse_args()

    base_path = Path(args.base_atlas).expanduser().resolve()
    with Image.open(base_path) as opened:
        base = opened.convert("RGBA")
    if base.size != (ATLAS_WIDTH, STANDARD_HEIGHT):
        raise SystemExit(
            f"base atlas must be {ATLAS_WIDTH}x{STANDARD_HEIGHT}; got {base.width}x{base.height}"
        )
    directions = load_mapping(Path(args.mapping).expanduser().resolve())

    atlas = Image.new("RGBA", (ATLAS_WIDTH, EXTENDED_HEIGHT), (0, 0, 0, 0))
    atlas.alpha_composite(base, (0, 0))
    atlas.alpha_composite(first_visible_idle(base), (6 * CELL_WIDTH, 0))

    row9 = Image.new("RGBA", (ATLAS_WIDTH, CELL_HEIGHT), (0, 0, 0, 0))
    row10 = Image.new("RGBA", (ATLAS_WIDTH, CELL_HEIGHT), (0, 0, 0, 0))
    for index, label in enumerate(LOOK_DIRECTION_LABELS):
        cell = mapped_cell(base, directions[label])
        row = row9 if index < COLUMNS else row10
        row.alpha_composite(cell, ((index % COLUMNS) * CELL_WIDTH, 0))

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
    if args.row9_output:
        row9_path = Path(args.row9_output).expanduser().resolve()
        row9_path.parent.mkdir(parents=True, exist_ok=True)
        clear_transparent_rgb(row9).save(row9_path)
        print(f"wrote {row9_path}")
    if args.row10_output:
        row10_path = Path(args.row10_output).expanduser().resolve()
        row10_path.parent.mkdir(parents=True, exist_ok=True)
        clear_transparent_rgb(row10).save(row10_path)
        print(f"wrote {row10_path}")


if __name__ == "__main__":
    main()
