# Luffy Identity-Preserving Look Mechanics

The previous generated V2 attempt failed because the look-direction rows were redrawn in a different style. This run reuses original atlas cells so the pet remains visually continuous during app playback.

- Identity is the hard gate: original face, line weight, proportions, hat, vest, shorts, sash, sandals, and body scale must remain intact.
- Direction semantics are approximated with existing right-facing, left-facing, upward, and downward source poses.
- Warnings are acceptable for subtle or approximate diagonals when the animation remains the same Luffy.
- Any generated redraw that changes face or proportions is rejected for this repair path.
