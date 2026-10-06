# Контракты данных v1

Это нормативная схема поведения/полей. Runtime validators и TypeScript types создаются в KF-023; не считать этот Markdown скомпилированным кодом.

## Identity/provenance
- Work: `id`, `title`, `composer?`. Не равен конкретной записи/нотам.
- Arrangement: `id`, `workId`, `title`, `arranger?`, `revision`, `sourceId`, `contentHash`, `capabilities`, `lessonIds`, `rightsRef`. Revision immutable; замена файла создаёт новую revision.
- ScoreSource: `id`, `format:musicxml|mxl|midi`, `filename`, `byteLength`, `sha256`, `importedAt`, `origin:bundled|user`, `licenseRef?`, `blobRef`. Не сохранять локальный полный путь/секретный URL.
- Lesson: `id`, `version`, `arrangementRevision`, `stepIds`, `prerequisiteGraph`, `editorialReview`, `localeKeys`.

## Musical position
`Q = {n: integer, d: positive integer}` в четвертных единицах. Fraction reduced by gcd, denominator>0; отрицательные значения для score offsets запрещены. Арифметика проверяет safe integers/overflow; parser возвращает diagnostic вместо float rounding. Quarter={1,1}; eighth={1,2}; triplet eighth={1,3}. Не фиксировать PPQ960 как universal representation всех tuplets.

`Pitch = {step:A|B|C|D|E|F|G, alter:integer, octave:integer, midi:0..127}`. C4=MIDI60; `midi=12*(octave+1)+base(step)+alter`. Written pitch and sounding pitch may differ; unsupported transposition/octave-clef semantics must be diagnosed. Нельзя применить key signature повторно к уже определённому MusicXML pitch.alter.

`NotatedEvent`: `id`, `partId`, `staffId`, `voiceId`, `measureId`, `onsetQ`, `durationQ`, `pitch|null`, `rest`, `tieGroup?`, `sourceLocation`, `fingering?`, `handHint?`.

`PerformanceEvent`: `id`, `onsetQ`, `durationQ`, `midi`, `velocity`, `sourceNoteIds[]`, `assignedHand:left|right|unknown`, `assignmentSource:editorial|user|none`. Tied note segments may map to one sustained event. Staff, voice, track and hand are separate fields.

`Measure`: stable id, displayLabel (не обязательно integer), startQ, actualDurationQ, timeSignature, pickup flag. UI показывает исходные label; engine не считает `(номер-1)*4`.

`TempoPoint`: `onsetQ`, `quarterBpm`; sorted unique offsets. `Phrase`: id, arrangementRevision, startQ, endQExclusive, sourceMeasureIds, editorial label. `Loop`: startQ<endQExclusive. Tempo events входят в model, но заявленная поддержка импорта может быть уже (см. import-contract).

## Session и evidence
`PracticeSession`: id, arrangementRevision, lessonId/version?, stepId?, mode:listen|try, targetHand:left|right|both, audibleHands, range, positionQ, speed, hintLevel, inputBasis:self-report|screen|physical-midi, state, createdAt, updatedAt.

`Attempt`: id, sessionId, arrangementRevision, span, startedAt, endedAt?, outcome:completed|interrupted|abandoned, inputBasis, reflection?, metrics?, environmentRef?. Events времени сохраняются как delta от monotonic session clock; wall-time только для истории. Playback completion не создаёт passed performance attempt.

`Metrics` допустимы только для подтверждаемой inputBasis: expected/matched/missed/extra notes, timing deviations, effectiveTempo, matcherVersion, calibrationStatus. Для self-report поле metrics=null. Пустой denominator даёт null/«нет данных», не100%.

`StepProgress`: lessonId/version, stepId, status, evidenceRefs, lastPractisedAt, reviewDueAt. Не хранить один magic percent для навыка пианиста.

## Persistence ports
`ProgressRepository`: load preferences/library/session; append attempt; commit progress+session atomically; export snapshot; validate/restore snapshot; migrate schema. Методы async и возвращают typed errors. IndexedDB/SQLite details не пересекают boundary. Concurrent writes сериализуются; session writes имеют revision/updatedAt conflict check.

Tables/stores: metadata, preferences, sources, arrangements, lessons, sessions, attempts, progress, resourceManifest. Имена logical, native physical schema может отличаться при contract tests.

## Backup v1
Manifest: schemaVersion, appVersion, exportedAt, records, assets inventory, checksums. Validate before mutation. Неизвестная более новая schema → reject с объяснением; corrupt/hash mismatch → reject; недостаточно места → сохранить текущие данные. В alpha restore mode только **replace after preview and confirmation**, не произвольное частичное слияние. Предложить export текущей копии перед replace. User files в backup остаются пользовательскими, не уходят в public fixtures.

## Acceptance invariants
Stable IDs survive reflow/theme; new arrangement revision does not silently reuse old note-matching progress; missing asset does not erase attempt history; rollback keeps original data on failed migration; no user document is executable HTML; no control/settings value changes source score.
