# Risk register

| Риск | Ранний сигнал | Защита / задача | Правило остановки |
|---|---|---|---|
| Создали player вместо tutor | Можно слушать, но новичок не понимает действие | Authored First Motif route, KF-030/A02 | Alpha не принимается без законченного учебного цикла |
| Красивые, но неверные ноты | Pitch/октава/длительность расходятся | Golden fixture и независимая музыкальная сверка | Не исправлять fixture под случайный renderer output |
| «Универсальный» парсер теряет semantics | Repeat/tuplet сыгран как простой ряд | basic-piano-1 capability profile | Unsupported до отдельной спецификации поддержки |
| UI/native split ломает единый продукт | Native переименовал руки/режимы/прогресс | Shared contracts+cross-platform scenarios | Не принимать отдельный UX под видом адаптации |
| Платный OSMD player/native dependency | Нужен sponsor token для базовой практики | Core renderer+own adapters | Заблокировать зависимость; ADR, не покупка |
| PWA install принят за offline | После reload пропадает chunk/sample | KF-019,033 production offline tests | Offline-ready только после manifest verification |
| Локальные данные потеряны | Quota/eviction/migration error | Backup/export, atomic storage, rollback | Не инициализировать пустую БД поверх ошибки |
| Неверная вера в browser MIDI | На iPhone нет API или устройство исчезло | Capability detection+physical testing | Self-report fallback; no fake connected |
| Непроверенная педагогическая эффективность | Counts/streak выданы за mastery | Evidence basis и novice testing | Не обещать pro-level по количеству уроков |
| Агент пишет в чужой workspace | Имя account содержит TalentBay | Exact file key and live inventory | Остановиться при неизвестной цели |
| Статусы оторваны от реальности | done без файлов/проверок | Validator+independent reviewer | Не продолжать зависимые задачи |
| Бесплатный hosting стал недостаточным | Quota/terms не подходят deployment | KF-036 live check | Не включать paid plan автоматически |
| Документация устарела | Task/spec/code противоречат | ADR+traceability+readback | Зафиксировать конфликт до реализации |

Владелец решения определяется gate/decision. Нельзя решить риск снижением честности статуса или отключением теста. Сложность, неизвестный API или недоступный инструмент фиксируются как конкретный блокер, а не заменяются обещанием «потом доделаем» внутри принятой задачи.
