# Architecture baseline

## Выбор и причина
Сохраняем согласованный TypeScript monorepo: Next.js + React для Web/PWA, Expo + React Native для iOS/Android. Нужен хороший браузерный продукт без обязательной установки и отдельный native доступ к устройствам позже. Не создавать второй продукт при добавлении native.

**Общий UI означает общий контракт, а не обещание одного JSX для любого renderer.** DOM/SVG и native views различаются. Делим tokens/domain/music/learning; допускаем web/native адаптеры и тонкие платформенные UI-реализации. См. [S11] в `research/sources.md`.

## Целевая структура после KF-017
```text
apps/web/                  Next.js routes, client composition, PWA shell
apps/mobile/               Expo app; только после G-NATIVE
packages/domain/           identities, immutable models, validation interfaces
packages/music/            rational time, score/performance event contracts
packages/learning/         authored lesson DAG, attempts, review heuristics
packages/tokens/           generated approved semantic tokens
packages/ui-web/           accessible DOM components using shared contracts
packages/ui-native/        native counterparts, later
packages/adapters-web/     IndexedDB, file import worker, OSMD, Tone, Web MIDI
packages/adapters-native/  SQLite, native audio/MIDI, score bridge, later
packages/content/          approved original lessons and content manifest
packages/config/           shared build/lint/test settings
```

Это уточняет прежний набросок `packages/ui`; не устанавливать библиотеку «универсального UI» ради максимального процента shared code. Не создавать пустые mobile/native packages до своей фазы.

## Границы зависимостей
`domain` не импортирует framework/DOM/storage/audio. `music` зависит только от domain и чистых утилит. `learning` зависит от domain/music, не от UI. Adapters реализуют ports и могут зависеть от платформенных библиотек. UI вызывает application/session controller, а не общается напрямую с MIDI и БД. Apps связывают реализации. Нельзя импортировать OSMD/Tone/IndexedDB в общие domain/learning packages.

## Целевые библиотеки, не проверенная инсталляция
- OSMD: engraving MusicXML в браузере; отдельный `NotationRenderer` adapter. Его спонсорский player/native bundle не является бесплатной зависимостью проекта [S01].
- Tone.js: браузерный audio scheduling/synth/sample playback за `AudioEngine`; не источник truth для учебного прогресса [S02].
- MusicXML parser: `fast-xml-parser` с сохранением порядка и отключённой обработкой entities — кандидат KF-018; либо иной утверждённый в ADR parser, если тесты безопасности/семантики не проходят. Самостоятельно незаметно подменять нельзя.
- `.mxl`: ограниченная ZIP-распаковка с `fflate` как кандидат; validate sizes/paths до принятия содержимого.
- MIDI file parsing: `@tonejs/midi` как кандидат для поддерживаемого SMF-профиля, не audio transcription.
- Web storage: IndexedDB adapter (Dexie как кандидат); native: expo-sqlite adapter [S06].
- Web UI: React, CSS variables + CSS Modules, Lucide icons. Не нужен платный UI kit.
- Tests: Vitest + Testing Library + Playwright; pnpm workspaces; GitHub Actions после scaffold.

Кандидаты должны пройти version/license/API check в KF-017–KF-020. Не копировать неподтверждённые сигнатуры из этой концептуальной таблицы; детальный lock будет существующим артефактом после spike.

## Web routing и offline
Целевой web alpha — client-heavy app с известными route shells. Next.js static export предпочтителен: `/song/?arrangement=...`, `/lesson/?lesson=...&step=...`, `/practice/?arrangement=...`; не dynamic path для произвольного ID из локальной БД. Каждый route shell существует на build-time. KF-019 обязан доказать reload/deep-link/offline cache для выбранного build режима.

Нет Server Actions, обязательного API route, server database или динамического server lookup для открытия локального файла. Manifest не равен offline; caching/ресурсы/стратегия обновления реализуются отдельно [S03]. Service worker build pipeline выбирается и фиксируется в spike; базовый кандидат — Workbox precache generation после web build.

## Native
Expo development build, а не предположение о любых native modules внутри Expo Go [S05]. Для notation планируется isolated local WebView bundle с тем же OSMD-renderer и версионированным message contract; remote website в WebView не является offline/native решением. Audio/MIDI остаются native adapters; не гонять каждый MIDI timestamp через произвольную UI-webview очередь для grading. Эта схема проверяется в KF-043 и может блокировать native, но не web.

## Data и сеть
Локальные versioned records, raw score blob отдельно, immutable attempts, explicit backup/export. Никакой cloud sync в alpha. Внешние ссылки на видео открываются по действию пользователя; основная практика работает без них. Не отправлять imports, MIDI traces, персональные результаты в аналитику или AI.

## Доказательство архитектуры
Короткие spikes обязаны проверить тяжёлые места до feature implementation: совпадение note IDs/тайминга/score reflow; browser gesture audio; safe import; offline reload; storage versioning. Только потом `G-ENGINE`. Решение по новым SDK/native/sync требует отдельного принятого ADR, не импровизации исполнителя.
