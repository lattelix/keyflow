# Keyflow — instructions for every agent

## Mission
Build a useful song-first piano tutor. Do not turn it into a score marketplace or claim that a player teaches by itself. Read this file on every fresh context.

## Start, in this order
1. Read `docs/STATE.md`, `docs/START_HERE.md`, `docs/decisions.md` and `docs/plan.md`.
2. Run `python3 tools/plan.py validate`, then `python3 tools/plan.py next`. Without a shell, inspect `docs/tasks/queue.json` and `docs/gates.json` manually using the same rules.
3. Read the selected task's `inputs`; do not read every document unnecessarily.
4. Check live repository/Figma state before changing it. Use the exact target repository and file below.
5. Execute **one eligible task**, verify it, and write the handoff. Do not silently start the next task.

## Hard boundaries
- Repository: `lattelix/keyflow`. Figma file: `STjpIkSSiMvFfe9lFog0Yn` only. User's workspace is Latitude X Lab, previously returned by Figma as `lattelix Lab`. Do not use TalentBay, Libman Studio or their libraries without a new explicit request.
- Planning permission is not approval of a finished design. `G-IMPLEMENT` must pass before app scaffolding, technical spikes or deployment setup. Production, native release and sync have additional gates.
- Keep Next.js/PWA + Expo/React Native + TypeScript unless a new ADR is approved. Shared semantics/tokens/domain do not imply identical DOM and native component implementations.
- No paid service, trial, API key, domain purchase, account creation or plan upgrade without explicit owner permission. Do not search local files for credentials.
- No commercial scores, screenshots of scores, audio or third-party video copies in this public repository without distributable rights. No paywall scraping. Import is local by default.
- Never invent note names, fingering, chord labels, tests, screenshots, connected devices, measurements, approvals, deployment URLs or completion percentages.
- MIDI identifies events, not which finger/hand was used, posture or musicianship. No input = no objective performance score. Touch practice is not evidence of acoustic-piano performance.
- An unsupported file must be rejected or visibly downgraded according to `docs/engineering/import-contract.md`; never silently play different music.

## Sources and conflicts
Live state describes what exists. Product/specification describes what should exist. A current approved decision overrides an older design or task; a task never authorizes changing the product. Approved Figma nodes govern visual implementation, not musical correctness. On a conflict: stop the affected task, record the conflicting references, propose the smallest resolution. Never "fix" tests/specs just to make your implementation pass.

## Writes and completion
Use a task branch and a small PR for application work. Do not force-push, remove unrelated files, merge or deploy without the relevant permission. Documentation bootstrap may be committed atomically to `main` under the owner's explicit documentation request; it does not authorize later direct app changes.

Only touch the selected task's `allowed_paths` and explicitly listed Figma pages. Read the actual connector schema before calling it. Re-read before retrying a partially failed write. Keep a single writer per branch and per Figma component family.

`done` requires the task's artifacts, checks, evidence, independent review and satisfied gates/dependencies. Otherwise use `needs_review`, `blocked`, or `in_progress`. A passed planning validator is not proof of a working app.

Finish using `docs/operations/handoff-template.md`: task, changes, evidence, commands actually run, limitations, blockers, next eligible task. See `docs/operations/agent-playbook.md` for the full procedure.
