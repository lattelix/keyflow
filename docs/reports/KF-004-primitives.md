# KF-004 — base controls as real Figma components

## Task and baseline
- Task: `KF-004 · Собрать базовые контролы как настоящие компоненты`
- Role: designer
- Date: 2026-10-10
- Repository: `lattelix/keyflow`
- Branch: `task/KF-004-primitives`
- Starting main SHA: `0ca7c91faf3b8ea37c4f84b6c13f9b67fdead458`
- Figma file: https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn
- Figma page: `1:3 / 02 · Components`

Scope is limited to C01, C02, C03, C04, C21, C22 and C24 plus helper icons and QA specimens. No application screen or implementation gate is claimed.

## Result

### Product component sets
| ID | Family | Figma node | Variants | External properties |
|---|---|---|---:|---|
| C01 | Button | `12:248` | 48 | Label; leading/trailing visibility + INSTANCE_SWAP; Kind; Size; State |
| C02 | IconButton | `12:295` | 6 | Icon INSTANCE_SWAP; Accessible label; State |
| C03 | SearchField | `13:82` | 5 | Label; Value; Placeholder; Error message; Clearable; Clear icon INSTANCE_SWAP; State |
| C04 | SegmentedControl | `13:164` | 9 | Option 1/2/3 labels; Disable third option; State; Value |
| C21 | BottomSheet | `16:114` | 3 | Title; Content; Dismissible; exposed nested Close action + Primary action |
| C22 | Dialog | `16:327` | 6 | Title; Body; State; Destructive; exposed nested Cancel + Confirm Button instances |
| C24 | StatePanel | `16:446` | 4 | Title; Body; Show secondary action; Kind; exposed nested primary/secondary Button instances |

Stable links:
- https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn?node-id=12-248
- https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn?node-id=12-295
- https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn?node-id=13-82
- https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn?node-id=13-164
- https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn?node-id=16-114
- https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn?node-id=16-327
- https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn?node-id=16-446

Six local helper icon main components were created as editable SVG-based instances: `11:2` Search, `11:5` ArrowRight, `11:8` Close, `11:11` Refresh, `11:14` Refresh OnPrimary, `11:17` ChevronRight. They exist only to support actual INSTANCE_SWAP properties and nested composition.

### Composition
C21/C22/C24 do not redraw actions. They contain real C01/C02 instances. Nested action instances are marked exposed so their properties remain reachable from parent instances. No detach operation was used.

Common color/radius/spacing/control sizing is bound to KF variables. Structural audit found token bindings on all seven sets (bound descendant counts: C01 104, C02 12, C03 32, C04 60, C21 22, C22 50, C24 27).

C01 preserves layout width in Loading by rendering the loading indicator outside normal auto-layout flow. QA instances `18:142` Default and `18:253` Loading, both with label «Сохранить изменения», are exactly **209 px** wide.

C02 uses a fixed 48×48 logical target. SearchField and SegmentedControl use 48 px as minimum height and can grow under larger text.

### Review specimens
- Light: https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn?node-id=18-136 — `18:136`, 1200×4652.
- Dark: https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn?node-id=18-1182 — `18:1182`, 1200×4652.

Both are review-only frames made from component **instances**. Structural audit found zero COMPONENT / COMPONENT_SET descendants in either review frame.

The review covers:
- C01: Default, Hover, Pressed, Focus, Disabled, Loading plus Secondary/Ghost/Destructive and a long RU/EN label with icon swap.
- C02: all 6 states, including a swapped Close icon and explicit accessible label property.
- C03: Empty, Filled, Focused, Error, Disabled, long bilingual content, clearable state.
- C04: left/both/right selection, Focus and Disabled.
- C21: Closed, Open, Busy.
- C22: Open, Busy, Error + destructive example.
- C24: Empty, Loading, Error, Unsupported with explicit reason/recovery copy.
- 200% text stress: Button `18:1124`, SearchField `18:1141`, SegmentedControl `18:1164`.

### 200% text and clipping
The 200% QA is implemented as instance overrides; main components remain attached.

Read-back results:
- Button 200%: 784×64; label 752×40 inside 784×64 → fits.
- SearchField 200%: 360×236; visible value 272×192 inside a 360×192 field → fits and the field grows vertically.
- SegmentedControl 200%: stays 360×48; its visible 32 px / 40 px-line-height labels fit each 120×48 segment. The longest visible label is 118×40 and remains inside its segment.
- Search/Segment fixes use 48 px **minimum**, not a hard maximum.

## Defects found and corrected
1. First helper-component script ended after creating six icons before C01/C02. A page read confirmed only those six nodes existed; continuation reused them rather than duplicating.
2. Initial C21 attempt failed because Figma rejects `isExposedInstance=true` before an instance is parented inside a component. Read-back confirmed no partial C21/C22/C24 set; corrected write exposes nested instances after parenting.
3. BottomSheet Open/Busy were initially cloned after the Closed base had been compressed. Review metadata exposed Open/Busy as 48 px high. Targeted repair restored `primaryAxisSizingMode=AUTO`, opacity and unclipped content: component variants now Open 480×232 and Busy 480×232. Review Open is 480×232; Busy is 480×212 when `Dismissible=false`.
4. SearchField and SegmentedControl were changed from fixed 48 px vertical sizing to a 48 px minimum with auto vertical growth before 200% QA.

## Verification
| Check | Method | Actual result | Verdict |
|---|---|---|---|
| Seven required families exist | Plugin API structural audit | all exact IDs above, expected variant counts | PASS |
| Every inventory state shown as instance | Light/Dark review audit + metadata | all listed states represented | PASS |
| No detached repeated UI in review | descendant type audit | 0 COMPONENT / COMPONENT_SET descendants | PASS |
| Component properties | set definition read-back | TEXT / BOOLEAN / INSTANCE_SWAP / variant axes present as designed | PASS |
| Nested modal/panel actions | default-variant audit | C21 exposes Close + Primary; C22 Cancel + Confirm; C24 Primary + Secondary | PASS |
| Loading width stable | actual instance measurement | 209 px Default = 209 px Loading | PASS |
| 48 px minimum target | variant/instance geometry | C01 48/56, C02 48, C03 field min 48, C04 min 48 | PASS |
| Disabled/focus/error states | final review + variant bindings | explicit state variants and semantic borders/fills | PASS |
| Long RU/EN | review specimens | long button/search/segment labels rendered as instances | PASS |
| 200% text | structural geometry + final screenshot | visible stress text fits; Search grows to 236 px | PASS |
| Light/Dark | explicit KF Theme modes + final screenshots | both final 1200×4652 review frames | PASS |
| Final visual QA | final screenshots after C21 fix | no observed clipping/overlap in reviewed sections | PASS |
| Repository validator | GitHub Actions on final branch head | pending until repository evidence commit | NOT RUN YET |

Temporary Figma screenshot asset URLs are not stored as durable evidence; stable node links above allow screenshots to be regenerated.

## Remaining limits
- Components are design contracts, not running accessibility semantics. Keyboard arrows, focus trap/return, dismissal and inactive/disabled behavior must be implemented and tested later in code.
- C04 is a bounded three-option Figma representation used by current product needs; implementation semantics still follow the generic options/value/disabledOptions contract.
- Complete product design has not been accepted by the owner. `G-IMPLEMENT` remains pending.
- Musical notation was not introduced in this task.

## Review
Executor verification is complete. Per the owner's 2026-10-10 instruction, an additional executor self-review may be used to merge and continue intermediate design tasks, but it must be recorded separately and **must not be described as independent review or owner acceptance of the complete design**.

Current verdict before that checkpoint: **NEEDS_REVIEW**.

## Continuation
After the recorded owner-authorized self-review exception and exact-head CI pass, KF-004 may be marked done/merged and the queue may continue. `G-IMPLEMENT` remains pending.
