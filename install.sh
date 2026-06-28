#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PETS_ROOT="$ROOT_DIR/pets"
DEST_ROOT="${CODEX_HOME:-$HOME/.codex}/pets"
TARGET="${1:-}"

usage() {
  cat <<'USAGE'
Usage:
  ./install.sh all
  ./install.sh <category>
  ./install.sh <category>/<pet>

Examples:
  ./install.sh all
  ./install.sh one-piece
  ./install.sh one-piece/luffy
  ./install.sh original/codex-buddy
USAGE
}

install_pet_dir() {
  local src="$1"
  local pet_json="$src/pet.json"
  if [[ ! -f "$pet_json" || ! -f "$src/spritesheet.webp" ]]; then
    echo "Skipping invalid pet folder: $src" >&2
    return
  fi

  local pet_id
  pet_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["id"])' "$pet_json")"
  local dest="$DEST_ROOT/$pet_id"
  mkdir -p "$dest"
  cp "$src/pet.json" "$dest/pet.json"
  cp "$src/spritesheet.webp" "$dest/spritesheet.webp"
  if [[ -f "$src/contact-sheet.png" ]]; then
    cp "$src/contact-sheet.png" "$dest/contact-sheet.png"
  fi
  echo "Installed $pet_id -> $dest"
}

if [[ -z "$TARGET" || "$TARGET" == "-h" || "$TARGET" == "--help" ]]; then
  usage
  exit 0
fi

mkdir -p "$DEST_ROOT"

if [[ "$TARGET" == "all" ]]; then
  while IFS= read -r -d '' pet_json; do
    install_pet_dir "$(dirname "$pet_json")"
  done < <(find "$PETS_ROOT" -mindepth 3 -maxdepth 3 -name pet.json -print0 | sort -z)
elif [[ -d "$PETS_ROOT/$TARGET" && -f "$PETS_ROOT/$TARGET/pet.json" ]]; then
  install_pet_dir "$PETS_ROOT/$TARGET"
elif [[ -d "$PETS_ROOT/$TARGET" ]]; then
  while IFS= read -r -d '' pet_json; do
    install_pet_dir "$(dirname "$pet_json")"
  done < <(find "$PETS_ROOT/$TARGET" -mindepth 2 -maxdepth 2 -name pet.json -print0 | sort -z)
else
  echo "Unknown target: $TARGET" >&2
  usage >&2
  exit 1
fi

echo "Done. Restart Codex to pick up newly installed pets."
