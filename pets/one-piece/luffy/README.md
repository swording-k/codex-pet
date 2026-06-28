# Luffy Codex Pet

A custom Codex desktop pet inspired by Monkey D. Luffy, with a straw hat, red vest, blue shorts, sandals, and rubbery adventure-themed state animations.

## Install

Copy this folder into your Codex pets directory:

```bash
mkdir -p ~/.codex/pets
cp -R luffy ~/.codex/pets/
```

Then restart Codex so it reloads custom pets.

Expected layout:

```text
~/.codex/pets/luffy/
├── pet.json
└── spritesheet.webp
```

## Ask Codex To Install It

If this folder is hosted on GitHub, you can ask Codex:

```text
Please install this Codex custom pet from GitHub:
<REPOSITORY_URL>

Download the repository, copy the luffy folder into ~/.codex/pets/luffy, and make sure pet.json and spritesheet.webp are together. Then tell me to restart Codex.
```

## Animation Rows

| Row | State | Behavior |
| --- | --- | --- |
| 0 | `idle` | calm grin, blink, and hat bob |
| 1 | `running-right` | rightward rubbery run |
| 2 | `running-left` | leftward rubbery run |
| 3 | `waving` | cheerful greeting |
| 4 | `jumping` | rubber spring jump / hover response |
| 5 | `failed` | deflated failed state |
| 6 | `waiting` | eager ready-to-sail pose |
| 7 | `running` | in-place rubber stretch punch task loop |
| 8 | `review` | lookout / inspection pose |

## Files

- `pet.json`: Codex custom pet manifest.
- `spritesheet.webp`: 1536 x 1872 WebP atlas, 192 x 208 cells.
- `contact-sheet.png`: visual preview of all animation rows.
