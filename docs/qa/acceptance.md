# Acceptance scenarios — что именно считать работающим

Статус: **спецификация проверок, не результаты тестирования**. Given/When/Then ниже реализуются в task outputs. Для каждого прогона записывать commit/build, fixture, устройство/браузер, method, actual, evidence и PASS/FAIL/NOT RUN. Тесты не заменять анимацией или mocked success.

## A01 · Первый запуск (R01,R02,R14)
Given: чистое локальное хранилище, русский locale, никакого аккаунта.
When: открыть web → начать обучение → выбрать First Motif.
Then: за не более трёх осмысленных действий доступен первый полезный шаг; не требуется разрешение MIDI/микрофона, логин или покупка; показано конкретное действие и его пример. Повторный запуск не возвращает к обязательному onboarding.

## A02 · Реальный учебный цикл (R02,R03,R06,R07,R21)
Given: authored lesson First Motif, self-report basis.
When: пройти объяснение, Listen, Try, выбрать «Нужно повторить», потренировать RH/LH, соединить первые два такта.
Then: Listen сам не помечает игру правильной; Retry оставляет диапазон; помощь восстанавливается; пользователь сам оценивает попытку. Завершение первой фразы не выдаётся за освоение всего произведения.

## A03 · Музыкальный golden fixture (R03,R04,R05,R23)
Given: точный файл по reference-journey.md.
When: построить каноническую модель, исполнить при speed1 и0.5, выделить bars1–2.
Then: 26 RH +8 LH=34 атаки; длина32Q; 32s/64s без count-in; первые два такта8s/16s. Правильные высоты/октавы, у каждой руки4Q на такт. Review визуальной записи и sound mapping отдельно от вычисления длины.

## A04 · Transport без утечек (R04,R17)
Given: loaded playable score.
When: Play → Pause → Seek → Loop → change speed → resize → close; повторить100циклов.
Then: смена настроек ставит pause; нет лишних атак/сохранённых callbacks/застрявших нот; position/range музыкальные, не пиксельные; после cleanup нет нового звука. Измерить целевую реакцию stop≤100ms в заявленной среде; превышение раскрыть, а не округлить до нуля.

## A05 · Ties/voices/chords (R03,R04,R10)
Given: отдельные очищенные fixtures для tie, chord, rest, backup/forward и pickup.
When: parse → canonical events → rendering/audio mapping.
Then: tie не повторяет атаку на продолжении; slur не удлиняет ноту; chord members имеют одинаковый onset; rest двигает время без звука; второй voice не сдвигает другой; pickup использует actual duration. Snapshot SVG недостаточен без event assertions.

## A06 · Неизвестная рука (R05,R10)
Given: импорт MIDI без явного hand assignment либо неподдержанный cross-staff MusicXML.
When: открыть Practice.
Then: неизвестная рука не объявляется левой/правой по track/clef автоматически. MIDI показывает performance view и понятный mapping step; unsupported notation/playback отключается по import profile. Руки становятся доступны только при подтверждённой карте.

## A07 · Self-report не measurement (R07,R21)
Given: inputBasis=self-report, никаких instrument events.
When: пройти полный playback и нажать «Получилось уверенно».
Then: metrics=null; «самооценка» видна; не появляется точность100%, «сыграно без ошибок», measured/checked physical skill. В screen basis точный выбор клавиши маркируется как экранная практика.

## A08 · Импорт не меняет музыку молча (R10,R11,R19)
Given: valid basic XML/MXL, malformed XML, repeat/tuplet, oversized/zip-bomb/path-traversal/DOCTYPE, SMF0/1, SMPTE и PDF.
When: выбрать каждый файл, отменить часть операций, повторить duplicate import.
Then: playable только заявленный supported subset; конкретные diagnostics; unsupported не превращается в неточную straight-line версию; no network/entity resolution; cancel не меняет library; duplicate предлагает переиспользование. Нет пользовательского файла в запросах/логах/PR.

## A09 · Сохранение/возврат (R01,R08)
Given: шаг7, bars1–2, speed0.5, reduced hints, self-report.
When: pause/save → закрыть → открыть и Continue.
Then: восстанавливаются arrangement revision, lesson/step, range, speed, hintLevel; нет autoplay. Дублированный Save не создаёт второй attempt. Ошибка транзакции не отображается как «Сохранено».

## A10 · Backup/migration (R08,R19)
Given: существующий прогресс и импортированный файл.
When: export → validate preview → restore; затем corrupt/newer-version/quota-failure варианты.
Then: успешный round-trip сохраняет identities/evidence; replace требует явного подтверждения; отказ не уничтожает текущие данные; новая schema не считается пустой БД. При невозможности записи доступен понятный recovery/export path.

## A11 · Production offline (R09,R15)
Given: production build и реально подготовленный урок со всеми resources.
When: отключить сеть → hard reload Home и прямого /practice/?arrangement=... → Listen/Try → сохранить → переоткрыть.
Then: весь основной маршрут работает; нет скрытого server lookup. Missing sample/chunk, eviction и quota имеют разные error/recovery states. Неподготовленный урок не называется offline-ready. Dev server не засчитывается.

## A12 · Обновление во время игры (R08,R09,R17)
Given: sounding session и ожидающий service worker новой версии.
When: update becomes available; затем Pause и explicit Apply.
Then: нет неожиданного refresh/обрыва/стирания данных; после подтверждения session восстановлена, schema совместима; при migration failure старая копия сохранена.

## A13 · Один responsive UI (R12,R13)
Given: все primary/boundary sizes из responsive.md, обе темы, RU/EN, text200%.
When: открыть/resize ключевые экраны и Practice states.
Then: no document overflow, контролы не перекрывают ноты, staff-space соблюдён, critical actions доступны; не всё ужато в страницу. Небольшие piano keys имеют крупный NotePad alternative; hand colors подписаны.

## A14 · Доступность и permission fallback (R13,R14,R15)
Given: keyboard-only, screen-reader/VoiceOver, reduced motion, неподдерживаемый/запрещённый MIDI.
When: пройти основной путь, dialog/theory, вернуться назад; нажать Space в input.
Then: focus order/return/labels корректны; Space не запускает музыку при вводе текста/чужом контроле; доступен self-report; no permission until explicit connect; нет выдуманного connected state.

## A15 · Release plumbing (R11,R16,R18,R19,R22)
Given: reviewed alpha candidate с resolved license, pinned dependencies и gates.
When: clean checkout → install frozen lockfile → scripts → build → linked preview deploy.
Then: actual commands проходят; preview связан с точным SHA; нет платных API/secrets/чужих ресурсов; production не публикуется до explicit G-PRODUCTION. Проверить URL и logs, не только успешный ответ create.

## A16 · MIDI algorithm и hardware (R03,R05,R07,R15,R17)
Given: synthetic clock fixtures отдельно от настоящего identified keyboard.
When: correct/repeated/chord/extra/late/tie/unison/note-on0/disconnect cases.
Then: one-to-one matching, null empty denominator, basis/version/calibration visible, disconnect pauses measured attempt. Synthetic test не заменяет hardware test; fingers/hand/technique не объявлены проверенными.

## A17 · Native parity (R08,R09,R12,R15,R20)
Given: после native gates реальные iOS/Android development builds, одинаковый fixture/lesson.
When: импорт, offline restart, audio interruption/background, MIDI reconnect, backup/restore, deep link.
Then: те же domain invariants и смысл actions; native capabilities честны; SQLite data сохраняются; встроенный local score bundle не обращается к сайту. Emulator-only прогон помечен отдельно.

## A18 · Непрерывность работы агентов (R22,R24)
Given: новая модель без чата, clone репозитория.
When: читает AGENTS/STATE, запускает validate/next/show.
Then: находит ровно текущую разрешённую задачу и её inputs; не угадывает Figma nodes или SDK versions; не считает pending gate одобренным; после задачи пишет evidence и отдаёт reviewer, не автозакрывает этап.
