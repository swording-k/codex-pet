# Codex Pet V2 Upgrade Plan

This repository is moving toward Codex v2 pets.

## Goal

Publish only Codex-compatible v2 pets:

- `spritesheet.webp` is exactly `1536x2288`.
- `pet.json` contains `"spriteVersionNumber": 2`.
- Rows `0-8` contain the normal animation states.
- Rows `9-10` contain 16 clockwise look-direction poses.
- QA artifacts prove the package was validated before publishing.

## Scope

1. Rebuild a high-quality SpongeBob-themed fan pet series from scratch.
2. Upgrade every existing published pet from v1 to v2.

## Current Published Pets

| Pet | Path | Current version | Required action |
| --- | --- | --- | --- |
| Codex Buddy | `pets/original/codex-buddy` | v1 | Add v2 look directions |
| Luffy | `pets/one-piece/luffy` | v1 | Add v2 look directions |
| Zoro | `pets/one-piece/zoro` | v1 | Add v2 look directions |
| Sanji | `pets/one-piece/sanji` | v1 | Add v2 look directions |
| Nami | `pets/one-piece/nami` | v1 | Add v2 look directions |
| Law | `pets/one-piece/law` | v1 | Add v2 look directions |
| Robin | `pets/one-piece/robin` | v1 | Add v2 look directions |
| Ace | `pets/one-piece/ace` | v1 | Add v2 look directions |
| Shanks | `pets/one-piece/shanks` | v1 | Add v2 look directions |
| Uta | `pets/one-piece/uta` | v1 | Add v2 look directions |
| Chopper | `pets/one-piece/chopper` | v1 | Add v2 look directions |
| Usopp | `pets/one-piece/usopp` | v1 | Add v2 look directions |

## SpongeBob Series Target

Do not reuse the rejected local SpongeBob files.

Initial target roster:

- SpongeBob
- Mr. Krabs
- Plankton
- Patrick
- Squidward

The public upload version should be recognizable fan-pet art, not copied official art. Avoid official screenshots, logos, readable show text, UI overlays, or exact trace-like reproductions.

## Work Directory Policy

Unverified generated work belongs under:

```text
work/v2-runs/<pet-id>/
```

Do not copy a pet into `pets/` until it has all required v2 QA evidence.

## Required QA Evidence

Each completed v2 pet must keep:

- `final/spritesheet-extended.webp`
- `final/validation-extended.json`
- `qa/contact-sheet-extended.png`
- `qa/look-directions.png`
- `qa/direction-semantics.json`
- `qa/look-continuity.json`
- `qa/run-summary.json`

Publishing requires:

- `validation-extended.json` has `ok: true`.
- `pet.json` has `"spriteVersionNumber": 2`.
- Local install test succeeds with `./install.sh <category>/<pet>`.

## Publication Rule

Never publish placeholder v2 pets. A pet is either:

- valid v1 and clearly documented as v1, or
- validated v2 with complete QA evidence.

