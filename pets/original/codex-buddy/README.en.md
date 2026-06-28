# Codex Buddy

[中文](README.md) | [English](README.en.md)

Codex Buddy is a custom Codex desktop pet: a chibi gym buddy with a backward blue cap, strong cartoon arms, orange star shorts, and workout-themed state animations.

The package is intentionally small. A Codex custom pet only needs:

- `pet.json`
- `spritesheet.webp`

`contact-sheet.png` is included as a preview so you can inspect the animation rows before installing.

## Install Manually

Download or clone this repository, then copy the pet files into your Codex pets directory:

```bash
mkdir -p ~/.codex/pets/codex-buddy
cp pet.json spritesheet.webp ~/.codex/pets/codex-buddy/
```

The final layout should look like this:

```text
~/.codex/pets/codex-buddy/
├── pet.json
└── spritesheet.webp
```

Restart Codex after copying the files. If Codex already had a pet loaded, restarting is the safest way to make it pick up the new spritesheet.

## Enable It In Codex

Update Codex to the latest version first so the app supports custom desktop pets. After restarting Codex, open Settings, click the Appearance dropdown, and choose Codex Buddy from the custom pet list.

If Codex Buddy does not appear, check that `pet.json` and `spritesheet.webp` are in the same directory:

```text
~/.codex/pets/codex-buddy/
```

After confirming the files are in place, restart Codex once more.

## Ask Codex To Install It For You

You can also ask Codex to download and configure the pet automatically. Give Codex a prompt like this:

```text
Please install this Codex custom pet from GitHub:
https://github.com/swording-k/codex-buddy-pet

Download the repository, copy pet.json and spritesheet.webp into ~/.codex/pets/codex-buddy/, and do not delete unrelated pets. Then tell me to restart Codex.
```

## State Rows

Codex reads a fixed 8-column by 9-row atlas. Each row corresponds to one app state:

| Row | State | Behavior |
| --- | --- | --- |
| 0 | `idle` | calm barbell breathing loop |
| 1 | `running-right` | rightward dumbbell carry |
| 2 | `running-left` | leftward dumbbell carry |
| 3 | `waving` | gym greeting |
| 4 | `jumping` | hover pull-up |
| 5 | `failed` | failed bench press |
| 6 | `waiting` | ready-to-train ritual while waiting for input |
| 7 | `running` | shoulder press task loop |
| 8 | `review` | double-dumbbell curl form check |

## Files

- `pet.json`: Codex custom pet manifest
- `spritesheet.webp`: transparent-capable WebP atlas, 1536 x 1872 pixels, 192 x 208 cells
- `contact-sheet.png`: visual QA preview of all rows
