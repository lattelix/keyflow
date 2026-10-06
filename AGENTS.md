# AGENTS.md

Keyflow is an open-source, song-first piano tutor.

Before implementation read docs/product.md, docs/design.md, docs/architecture.md and docs/roadmap.md.

Rules:
- Figma is the visual source of truth.
- Keep shared domain logic platform-agnostic TypeScript.
- Web and native share semantics, tokens, data models and behavior.
- Prefer local-first; account/sync is not an MVP dependency.
- Use MusicXML/MIDI and legally distributable demo content. Never commit copyrighted commercial scores without permission.
- Accessibility and keyboard/touch targets are requirements.
- Do not add backend infrastructure before a roadmap requirement needs it.
