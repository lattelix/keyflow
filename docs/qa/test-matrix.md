# Матрица проверки и трассировки

Все строки ниже — **ожидаемые проверки**, не заявленные прогоны. Фактические результаты публикуются в docs/reports с точной средой и commit.

| Сценарии | Уровень | Фаза / основные задачи | Evidence |
|---|---|---|---|
| A01,A02 | Prototype usability + UI/e2e | KF-007,009,015,030,035 | Переходы Figma; действия новичка; actual screenshots/log |
| A03,A05 | Canonical fixtures + unit + visual/audio review | KF-018,022,023,025,027,028 | Expected-event JSON, сравнение, notation screenshot, duration assertions |
| A04 | Fake clock unit + runtime profiling | KF-028,031,034 | 100циклов, timing measurements, cleanup counters |
| A06 | Import contract + integration | KF-026,031 | Unknown/mapped hand states, capability diagnostics |
| A07 | Domain/UI/e2e | KF-030,032,039,040 | Проверка отсутствия metrics в self-report; basis labels |
| A08 | Worker/parser negative + integration | KF-025,026,034 | Fixture diagnostics, cancellation/transaction/network assertions |
| A09,A10 | Repository contract + integration/e2e | KF-024,032,033 | Round-trip before/after, migration rollback, no data loss |
| A11,A12 | Production build + browser/device | KF-019,033,034 | Offline manifest, hard reload, interrupted update record |
| A13,A14 | Component/visual/accessibility | KF-014,021,029,034 | Dimensions, focus trace, contrast and screen-reader manual review |
| A15 | CI/build/deploy smoke | KF-017,035,036,037 | Lockfile clean install; script output; actual deployment SHA/URL |
| A16 | Deterministic algorithm + physical device | KF-038–042 | Synthetic fixture results and separate hardware report |
| A17 | Native contract + device lifecycle | KF-043–047 | Actual iOS/Android build/device and lifecycle evidence |
| A18 | Documentation validation + fresh-context walkthrough | Текущий пакет, KF-001,016 | Plan tests; task eligibility; no fake done/gates |

## Runtime matrix
Web automated: Chromium, Firefox, WebKit through Playwright after install. Это engines, не обещание покрыть каждый конкретный мобильный браузер. Manual critical path: actual Safari on macOS/iPhone when available, Chrome/Android, supported desktop browser for MIDI. Record exact versions and actual devices. При отсутствии iPhone/инструмента write NOT RUN и не объявлять соответствующий release gate пройденным.

Для UI: primary390×844,844×390,820×1180,1180×820,1440×900; boundaries320/360/599/600/768/1023/1024/1920; light/dark; RU/EN; text200%; reduced motion. Полный cross-product не требуется на каждом PR: минимум затронутые states, а complete sweep — перед design handoff/alpha release.

## Требования к evidence
Unit может доказать rational math, mapping, state machine, backup validation. Screenshot может подтвердить layout, но не click flow или звук. Browser mock может проверить denied/disconnect path, но не реальную задержку кабеля. Successful deploy API не доказывает working URL/offline. Self-report пользователя не измерение точности.

## Контрольные бюджеты (проектные, требующие измерений)
Планировать split points для renderer/audio, не загружать их на Home без нужды. Цель: управление не создаёт заметных зависаний; task KF-034 записывает long tasks, input response и память в100циклах. Не утверждать универсальные60FPS на любом телефоне. Stop target≤100ms и import timeout5s из соответствующих контрактов измеряются на явно указанном устройстве. Если цель не достигнута, report содержит фактическое значение и решение о блокировке/изменении бюджета; нельзя тихо ослабить assertions.

## Пример записи
`A09 | PASS | <commit> | production build | <device/browser> | exact saved fields matched | <evidence path>`.
Это шаблон, не состоявшийся тест. Для NOT RUN указывать причину и что необходимо для проверки.
