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
| SpongeBob | not started | Must be rebuilt from scratch. Rejected old local files are not allowed. |
| Mr. Krabs | not started | Must be rebuilt from scratch. |
| Plankton | not started | Must be rebuilt from scratch. |
| Patrick | not started | Must be rebuilt from scratch. |
| Squidward | not started | Must be rebuilt from scratch. |

## Existing Published Pets

| Pet | Status | Notes |
| --- | --- | --- |
| Codex Buddy | v2 | Published atlas passes `validate_atlas.py --require-v2`; install path was validated. |
| Luffy | identity-candidate | Official pet remains coherent v1; `work/v2-runs/luffy-identity` has a structurally valid identity-preserving V2 candidate with direction warnings. |
| Zoro | identity-candidate | Official pet remains coherent v1; `work/v2-runs/zoro-identity` has a structurally valid identity-preserving V2 candidate with direction warnings. |
| Sanji | v1 | Needs v2 look-direction upgrade. |
| Nami | v1 | Needs v2 look-direction upgrade. |
| Law | v1 | Needs v2 look-direction upgrade. |
| Robin | v1 | Needs v2 look-direction upgrade. |
| Ace | v1 | Needs v2 look-direction upgrade. |
| Shanks | v1 | Needs v2 look-direction upgrade. |
| Uta | v1 | Needs v2 look-direction upgrade. |
| Chopper | v1 | Needs v2 look-direction upgrade. |
| Usopp | v1 | Needs v2 look-direction upgrade. |
