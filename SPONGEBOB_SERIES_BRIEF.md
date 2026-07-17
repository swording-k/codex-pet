# SpongeBob Series Brief

This brief defines the upload-quality target for the new SpongeBob-themed pet series.

## Quality Bar

The rejected local SpongeBob pets must not be reused. The new series needs to look like deliberate fan-made Codex pets, not rough generated leftovers.

## Visual Direction

- Clean cartoon sprite style.
- Compact full-body silhouettes readable inside `192x208` cells.
- Bright undersea character energy.
- Large expressive faces and clear body language.
- No official screenshots, logos, watermarks, readable text, or traced frames.
- No scenery or UI panels inside sprite cells.
- No detached effects unless allowed by the v2 pet contract.

## Character Targets

| Pet id | Display name | Upload-version intent |
| --- | --- | --- |
| `spongebob` | SpongeBob | Square yellow sponge fan pet with cheerful work, wave, jump, failure, wait, running, review, and look-direction poses. |
| `mr-krabs` | Mr. Krabs | Red crab boss fan pet with readable claws, money-minded work loop, crabby reactions, and clean direction poses. |
| `plankton` | Plankton | Tiny one-eyed green schemer fan pet with antennae, villain gestures, gadget-like work loop, and readable look directions. |
| `patrick` | Patrick | Pink starfish fan pet with sleepy/silly charm, bouncy motion, simple readable limbs, and cohesive look directions. |
| `squidward` | Squidward | Long-nosed grumpy cephalopod fan pet with bored expression, clarinet-inspired work loop, and subtle look directions. |

## V2 Requirements

Every published pet must be created as a v2 atlas:

- `1536x2288`
- 8 columns x 11 rows
- `spriteVersionNumber: 2`
- rows `9-10` are real look-direction poses, not copied idle frames

