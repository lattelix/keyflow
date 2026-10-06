# Import capability profile: basic-piano-1

## Не обещать универсальный импорт
Format readability, notation display, playback и tutor availability — разные capabilities. Result содержит status, diagnostics и `canDisplay/canPlay/canSplitHands/hasAuthoredCourse`. Вывод «файл прочитан» не означает «всё можно правильно сыграть». MusicXML несёт notation semantics, которые MIDI обычно не содержит [S04].

## Alpha support matrix
| Вход | Поддержка | При выходе за профиль |
|---|---|---|
| UTF-8 `.musicxml` / `.xml`, score-partwise3.1/4.0 | Один piano part, 1–2 staves; clefs G/F; meter2/4,3/4,4/4; whole/half/quarter/eighth и dots, rests, chords, voices с backup/forward, pitch alter, ties, pickup; один постоянный quarter tempo | Diagnostic; playback disabled |
| `.mxl` | То же после безопасного container.xml rootfile resolution и bounded decompression | Reject container/path/size errors без записи в library |
| `.mid` / `.midi` | SMF0/1, PPQ timing, note on/off, tempo/time-signature events; labelled performance view | Type2/SMPTE → unsupported; нет обещания original notation/fingering/hand |
| PDF/image/audio/YouTube link | Не поддержаны | Понятное объяснение, список поддерживаемых форматов, пример |

Tuplets, grace notes, ornaments, repeat/volta/DC/DS navigation, cross-staff notation, transposing instruments, octave-transposing clefs, unpitched notes, microtones, mid-score tempo/meter/key changes и pedal semantics: вне initial MusicXML playback profile. Не удалять и не проигрывать их как straight-line approximation. Можно предложить view-only только если renderer отображает их корректно и UI ясно сообщает, что playback/course недоступны. Support расширяется отдельной задачей+fixture+review, а не случайно.

MIDI tempo map поддерживается отдельно, не расширяет MusicXML profile автоматически. MIDI files могут иметь quantization ambiguity, overlapping same-pitch notes и arbitrary tracks. Без явной hand assignment не включать руки. Автоматическая нотная запись из MIDI — позже; alpha показывает performance/piano view, а не выдумывает оригинальную партитуру.

## Security/resource limits — проектные стартовые бюджеты
Файл≤5MiB; MXL total uncompressed≤20MiB; entries≤32; ratio≤100:1; нотных событий≤25000; measures≤2000. Limits configurable only through reviewed config. Archive entries не должны быть absolute, содержать `..`, symlinks или external references. Единственный root score выбирается по валидному container metadata, не первому XML в ZIP.

Reject DOCTYPE/ENTITY declarations в initial safe profile; never fetch DTD/network or resolve external entities. Это сознательное ограничение может отклонить некоторые корректные экспорты — сообщить «экспортируйте MusicXML без DTD», не обвинять файл в порче. Parser должен сохранять порядок дочерних элементов, особенно backup/forward/chord. Не разбирать XML regex-ами.

Parsing/decompression в worker с отменой; initial timeout5s на заявленном test device (бюджет валидируется в spike). Отмена прекращает работу, не оставляет half-written records. Credits/title текстом, не innerHTML. SVG renderer/output sanitization и external reference запрет проверяются отдельно.

## Pipeline
1. Read file metadata and bounded bytes; verify type by content, extension is advisory.
2. Parse container safely if needed; validate profile, report unsupported semantic tags before playable state.
3. Parse ordered notation → canonical rational events → tie resolution → performance mapping.
4. Determine capabilities and unknown hand mapping; preview title/source/range/warnings.
5. User confirms; one transaction writes source/arrangement/manifest. Failure rolls back.
6. Duplicate checksum prompts reuse existing import; do not create duplicate on repeated click. New revision distinct from same title.

## Must-test fixtures
Valid basic single staff; two-staff backup/forward; chord onset not advancing twice; rest; dotted duration; accidental; tie across barline; pickup; duplicate file; malformed XML; oversized file; compressed zip bomb; path traversal; DOCTYPE/entity; repeat sign; tuplets; MIDI note-on velocity0; MIDI no note-off; unsupported SMPTE; cancellation; quota failure. Expected notes/durations/capability and diagnostics stored next to each fixture. All fixtures original/cleared.
