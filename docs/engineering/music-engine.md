# Music engine contract

## Разделить три слоя
Notation model хранит записанные ноты/такты/voices. Performance timeline хранит реальные атаки/длительности. Lesson graph хранит цели и упражнения. Нельзя считать DOM/SVG position, MIDI track или количество нот универсальным музыкальным смыслом.

Renderer отображает approved score и возвращает stable source-noteId mapping/geometry. AudioEngine читает performance events. PracticeController хранит позицию в quarter units и командует обоими. Progress обновляется только учебными событиями, не renderer animation.

## State machine
`idle → loading → ready → count_in → playing → paused|ended|error`.

- open: cancel old load/audio, load selected revision, validate capability, then ready; never autoplay.
- play/listen/try: requires user gesture and ready/paused/ended; resume AudioContext if possible; count-in only when policy requires.
- pause: freeze musical position, cancel scheduled future notes, release active voices; status paused. No pending scheduled callback may revive sound.
- seek: pause, clamp requested position to range, keep source settings. On next play, sustaining events crossing seek point may be retriggered for remaining duration **as playback assistance**, not counted as new expected attack.
- range/tempo/hand edit: pause, apply atomically; keep clamped musical position; wait for explicit resume.
- loop boundary: release voices crossing end, cancel obsolete scheduled events, jump start; do not leak notes/events or double-play first attack.
- ended: playback ends cleanly; Listen does not mark lesson success. Try opens reflection or measured result according to basis.
- error/unmount/visibility/system interruption/device disconnect: stop scheduling and release notes; save interrupted session when storage works; user explicitly resumes after recovery.

## Time and scheduling
For constant quarter tempo B and speed S: secondsBetween = durationQ*60/(B*S). For tempo map integrate each segment, not one average BPM. First Motif32Q at60BPM=32s; speed0.5=64s. Count-in is separate, not part of score offsets.

AudioContext clock is master for browser sound [S02]. requestAnimationFrame only draws. Use scheduled absolute audio times from engine callbacks; never sound note events with a UI setInterval alone. Proposed scheduler lookahead100ms/check25ms is an initial engineering setting to measure, not timing guarantee. API exact signatures come from pinned library docs.

Music event IDs own their scheduled handles. Cancel/reload/unmount disposes nodes, callbacks and listeners. Tests must detect leftover callbacks after100 start/stop/loop cycles. Target release/silence≤100ms after pause command under test setup; record audible sample tails and platform variation instead of pretending zero latency.

## Ties/voices/phrases
Tie segments same pitch form sustained performance event; don't retrigger at tie continuation. Slur != tie. Backup/forward determine onsets within measure; chord members share previous onset without advancing cursor separately. Rests advance time and produce no note-on. A pickup uses actual duration. Preserve displayed bar labels, not arbitrary contiguous numbering.

Unison written notes with same sounding pitch/onset can map to one physical expected attack with multiple source IDs, so user is not asked to press the same key twice simultaneously. Hand attribution remains explicit/unknown; clef/staff crossing is not guessed.

## Port shapes to implement and test
`NotationRenderer`: load/resize/selectRange/highlight/setTheme/dispose; outputs geometry and diagnostic, never owns playback.

`AudioEngine`: prepare/start/pause/seek/setPlaybackOptions/stop/dispose; one instance owns scheduled sound; returns typed state/position events.

`InstrumentInput`: capabilities/connect/disconnect/subscribe; emits timestamped note-on/off/controller events and lifecycle. Never initiates SysEx in basic piano profile.

`Clock`: nowMonotonicMs/audioTime mapping for deterministic tests. `PracticeController`: reducer/state machine independent of UI renderer. Commands have unique IDs to make repeated clicks idempotent.

## Audio assets
Samples have their own manifest/license/checksum. Offline preparation includes required samples or explicitly supported synth fallback. Missing piano bank must not show offline-ready. Output volume initially moderate, no forced max. Synth fallback labelled honestly.

## Feedback later
Pitch correctness ≠ timing ≠ duration ≠ technique. MIDI phase may evaluate first two initially. Pedal/velocity data may be retained locally with consented mode but not scored until a separate specification. No finger or posture classifier derived from MIDI.
