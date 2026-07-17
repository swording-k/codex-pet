# Zoro Identity-Preserving Look Mechanics

The previous generated V2 attempt failed identity review because the look-direction rows looked like a redraw. This candidate reuses original atlas cells so the pet remains visually continuous during app playback.

- Identity is the hard gate: original green hair, face style, line weight, body proportions, haramaki, earrings, sword placement, and palette must remain intact.
- Direction semantics are approximated with existing right-facing, left-facing, upward, crouched, and downward source poses.
- Warnings are acceptable for approximate diagonals when the animation remains the same Zoro.
- Generated redraws that alter face, body scale, or sword styling are rejected for this repair path.
