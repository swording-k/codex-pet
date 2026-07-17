# V2 Identity Review

The V2 upgrade is not complete just because `validate_atlas.py --require-v2` passes. The added look-direction rows must also look like the same pet as rows 0-8.

## Current Finding

| Pet | Structural V2 | Identity Review | Decision |
| --- | --- | --- | --- |
| Codex Buddy | pass | acceptable | Keep as current V2 unless later review finds a stronger issue. |
| Luffy | pass | fail | Look-direction frames are taller, thinner, and drawn in a noticeably different style than the original pet. Requires identity repair before upload-quality completion. |
| Zoro | pass | fail | Look-direction frames preserve broad character cues but drift in body proportions, face style, and line feel. Requires identity repair before upload-quality completion. |

## Updated Gate

For each existing-pet V2 upgrade:

1. Generate or derive look-direction rows.
2. Assemble and validate the `1536x2288` V2 atlas.
3. Compare `qa/look-directions.png` against the original `qa/contact-sheet.png`.
4. Accept only when the new look cells read as the same pet at normal display size.
5. If the look cells read like a redraw in a different style, mark the pet as needing identity repair even if deterministic validation passes.

## Repair Direction

Prefer identity-preserving approaches before more open-ended regeneration:

- stronger reference prompts using the original neutral cell and full contact sheet
- smaller gaze/head changes rather than full redraws
- deterministic reuse of original atlas cells when it produces a better upload-quality identity match
- independent visual QA before changing `PET_STATUS.md` to `v2`
