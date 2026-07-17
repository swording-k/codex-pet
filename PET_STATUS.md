# Pet Status

This file tracks the requested end state: all SpongeBob series pets completed, and all existing pets upgraded to v2.

## Legend

- `v1`: published old-format pet.
- `candidate`: generated work exists but is not publishable.
- `identity-candidate`: a structurally valid v2 candidate exists using original atlas cells; identity is preserved, but direction quality still needs review.
- `identity-repair`: a prior v2 attempt exists, but it was not publishable because the added look-direction art did not match the original pet closely enough.
- `v2`: published and validated Codex v2 pet.
- `blocked`: cannot proceed without a viable source image or generation path.

## SpongeBob Series

| Pet | Status | Notes |
| --- | --- | --- |
| SpongeBob | v2 | Published from a deterministic series generator; atlas validates as v2 and preserves identity across look directions. |
| Mr. Krabs | v2 | Published from a deterministic series generator; atlas validates as v2. Direction QA has visual-review warnings from intentional eye-stalk gaps. |
| Plankton | v2 | Published from a deterministic series generator; atlas validates as v2 and preserves identity across look directions. |
| Patrick | v2 | Published from a deterministic series generator; atlas validates as v2. Direction QA has visual-review warnings from intentional body/shorts gaps. |
| Squidward | v2 | Published from a deterministic series generator; atlas validates as v2 and preserves identity across look directions. |

## Existing Published Pets

| Pet | Status | Notes |
| --- | --- | --- |
| Codex Buddy | v2 | Published atlas passes `validate_atlas.py --require-v2`; install path was validated. |
| Luffy | v2 | Published identity-first V2 atlas; original rows preserved and look rows reuse original cells to avoid redraw drift. |
| Zoro | v2 | Published identity-first V2 atlas; original rows preserved and look rows reuse original cells to avoid redraw drift. |
| Sanji | v2 | Published identity-first V2 atlas; original rows preserved and look rows reuse original cells. |
| Nami | v2 | Published identity-first V2 atlas; original rows preserved and look rows reuse original cells. |
| Law | v2 | Published identity-first V2 atlas; original rows preserved and look rows reuse original cells. |
| Robin | v2 | Published identity-first V2 atlas; original rows preserved and look rows reuse original cells. |
| Ace | v2 | Published identity-first V2 atlas; original rows preserved and look rows reuse original cells. |
| Shanks | v2 | Published identity-first V2 atlas; original rows preserved and look rows reuse original cells. |
| Uta | v2 | Published identity-first V2 atlas; original rows preserved and look rows reuse original cells. |
| Chopper | v2 | Published identity-first V2 atlas; original rows preserved and look rows reuse original cells. |
| Usopp | v2 | Published identity-first V2 atlas; original rows preserved and look rows reuse original cells. |
