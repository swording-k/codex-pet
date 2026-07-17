#!/usr/bin/env python3
"""Create a registered v2 row-10 strip by mirroring a registered row-9 strip."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

CELL_WIDTH = 192
CELL_HEIGHT = 208
COLUMNS = 8
ATLAS_WIDTH = CELL_WIDTH * COLUMNS


def load_row(path: Path) -> Image.Image:
    with Image.open(path) as opened:
        row = opened.convert("RGBA")
    if row.size != (ATLAS_WIDTH, CELL_HEIGHT):
        raise SystemExit(
            f"registered row must be {ATLAS_WIDTH}x{CELL_HEIGHT}; "
            f"got {row.width}x{row.height}"
        )
    return row


def cell(row: Image.Image, column: int) -> Image.Image:
    return row.crop(
        (
            column * CELL_WIDTH,
            0,
            (column + 1) * CELL_WIDTH,
            CELL_HEIGHT,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--row9", required=True, help="Registered row-9 strip.")
    parser.add_argument(
        "--down-cell",
        required=True,
        help="Registered 180-degree down cell or row strip whose first cell is down.",
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    row9 = load_row(Path(args.row9).expanduser().resolve())
    down_source = Path(args.down_cell).expanduser().resolve()
    with Image.open(down_source) as opened:
        down_image = opened.convert("RGBA")
    if down_image.size == (ATLAS_WIDTH, CELL_HEIGHT):
        down = cell(down_image, 0)
    elif down_image.size == (CELL_WIDTH, CELL_HEIGHT):
        down = down_image
    else:
        raise SystemExit(
            "--down-cell must be a 192x208 cell or 1536x208 row strip; "
            f"got {down_image.width}x{down_image.height}"
        )

    output = Image.new("RGBA", (ATLAS_WIDTH, CELL_HEIGHT), (0, 0, 0, 0))
    output.alpha_composite(down, (0, 0))
    for dest_column, source_column in enumerate([7, 6, 5, 4, 3, 2, 1], start=1):
        mirrored = cell(row9, source_column).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        output.alpha_composite(mirrored, (dest_column * CELL_WIDTH, 0))

    out_path = Path(args.output).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    output.save(out_path)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
