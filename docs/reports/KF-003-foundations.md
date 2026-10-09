# KF-003 — Foundations and semantic tokens

## Task and baseline
- Task: `KF-003 · Построить foundations и semantic tokens`
- Role: designer
- Date: 2026-10-10
- Repository: `lattelix/keyflow`
- Branch: `task/KF-003-foundations`
- Starting main SHA: `4b2a2c496c95842554260a6185ea4c007364ee6d`
- Figma file: https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn
- Figma page: `1:2 / 01 · Foundations`
- Preflight: page empty; local variable collections/styles absent; Inter `Regular`, `Semi Bold`, `Bold` confirmed available.

Scope is foundations only. No application screen, product component, prototype, implementation gate or external library is claimed.

## Result

### Figma collections
| Collection | ID | Modes | Variables |
|---|---|---|---:|
| KF Color Primitives | `VariableCollectionId:8:2` | Default | 34 |
| KF Dimensions | `VariableCollectionId:8:37` | Default | 25 |
| KF Theme | `VariableCollectionId:8:63` | Light, Dark | 24 |

Semantic theme variables are aliases to primitives. Each semantic variable exists once in `KF Theme` and therefore has the same name in Light and Dark. Scopes are explicit rather than `ALL_SCOPES`; examples: `text/primary → TEXT_FILL`, `border/control → STROKE_COLOR`, `surface/canvas → FRAME_FILL + SHAPE_FILL`, spacing → `GAP`, radius → `CORNER_RADIUS`, sizes → `WIDTH_HEIGHT`.

Figma rejects dot notation in variable names (`invalid variable name`). The first failed write was followed by a read-back that confirmed **zero partial collections/nodes/styles**. The successful write therefore uses Figma-safe slash names: `surface/canvas` maps 1:1 to source token `surface.canvas`. WEB/ANDROID/iOS code syntax is explicitly set from the source token identity, e.g. `surface/canvas → var(--kf-surface-canvas) / kf_surface_canvas / KF.surfaceCanvas`.

### Typography
Verified Inter styles:
- `KF/Body` — Regular 16/24.
- `KF/Label` — Semi Bold 16/20.
- `KF/Caption` — Regular 14/20.
- `KF/Heading Small` — Semi Bold 20/28.
- `KF/Heading` — Semi Bold 28/36.
- `KF/Display` — Bold 40/48.

These match `docs/design/tokens.json`; no typography token change was required.

### Specimens
- Light: https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn?node-id=8-94 — `8:94`, 1200×1699.
- Dark: https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn?node-id=8-145 — `8:145`, 1200×1699.

Each specimen includes RU/EN typography, primary/outlined 48 px controls, labelled status samples, labelled L/R hand samples, and a score-area specimen. The score specimen deliberately contains no invented notes: only renderer area, staff lines and playhead are shown until a verified fixture is available.

The first visual screenshot check found one real defect: 200% text nodes `8:103` and `8:154` were 1401 px wide inside a 1024 px content area. They were changed to fixed 1024 px width with `textAutoResize=HEIGHT`; final metadata reports 1024×96, available width 1024, `fits=true` in both themes. Final roots auto-resized to 1200×1699. A second screenshot of each root was visually inspected after the fix.

## Contrast verification
Calculated from the exact values already present in `docs/design/tokens.json`; no local color overrides were introduced.

| Pair | Light | Dark | Requirement |
|---|---:|---:|---|
| text.primary / surface.canvas | 15.81:1 | 16.63:1 | ≥4.5 |
| text.secondary / surface.canvas | 6.18:1 | 9.13:1 | ≥4.5 |
| action.onPrimary / action.primary | 6.39:1 | 7.82:1 | ≥4.5 |
| border.control / surface.panel | 4.61:1 | 5.46:1 | ≥3 |
| border.control / surface.canvas | 4.26:1 | 6.24:1 | ≥3 |
| status.error / surface.raised | 5.75:1 | 7.24:1 | ≥3 |
| status.success / surface.raised | 6.07:1 | 8.09:1 | ≥3 |
| status.warning / surface.raised | 5.88:1 | 8.34:1 | ≥3 |
| music.left / surface.raised | 5.27:1 | 7.96:1 | ≥3 |
| music.right / surface.raised | 6.33:1 | 7.25:1 | ≥3 |
| music.ink / music.score | 17.10:1 | 14.54:1 | ≥4.5 |

Status meaning is not color-only: every specimen contains an explicit label. Hand color is not color-only: samples are labelled `L · Левая рука` and `R · Правая рука`.

## Verification
| Check | Method | Actual result | Verdict |
|---|---|---|---|
| Existing Figma state | read-only Plugin API preflight | Foundations empty; 0 local collections/styles; Inter styles available | PASS |
| Partial-write recovery | read after first `invalid variable name` error | page children 0, collections 0, variables 0, styles 0 | PASS |
| Semantic modes/aliases | Plugin API read-back | 24 semantic vars, Light/Dark, every value returned as primitive alias | PASS |
| Scopes | Plugin API read-back | semantic/dimension scopes explicit; no created variable left at ALL_SCOPES | PASS |
| Code names | Plugin API read-back | WEB/ANDROID/iOS syntax present for semantic and dimension tokens | PASS |
| Type styles | Plugin API read-back | six exact Inter styles/sizes/line heights | PASS |
| RU/EN + 200% | specimen metadata + final screenshots | bilingual samples present; 200% nodes wrap to available 1024 px | PASS |
| Min control size | metadata | primary/outlined examples height 48 px | PASS |
| Status/hand non-color evidence | metadata + screenshots | explicit status text and L/R labels | PASS |
| Contrast | WCAG relative luminance calculation from source hex values | all tested intended pairs above thresholds | PASS |
| Token/source consistency | compared Figma values to `tokens.json` | no source value change required; slash↔dot mapping documented | PASS |
| Repository validator | GitHub Actions on final branch head | pending until report/queue commit | NOT RUN YET |

## Remaining risks / limits
- These are foundations specimens, not approved application screens.
- 200% verification here checks the representative specimen and wrapping contract; full responsive screen QA belongs to later screen tasks/A13.
- Score notation itself is intentionally absent until verified music/rendering work; no fake notes were drawn.
- Figma screenshots were inspected through the connector. Temporary screenshot asset URLs are not treated as durable evidence; stable Figma node URLs above allow repeat capture.
- Independent design review is still required before `KF-003 = done`.

## Review
Reviewer: not assigned in this execution session.

Verdict: **NEEDS_REVIEW** after final repository CI. Self-checks above are executor verification and do not impersonate an independent reviewer.

## Continuation
Keep `G-IMPLEMENT` pending. After independent PASS of KF-003 and merge, rerun validator/next and continue the next design card. Do not start app scaffolding.
