# Offline and storage contract

## What offline means
После явной подготовки урока доступны app shell, нужные routes/chunks, score/lesson, audio assets или разрешённый synth, fonts и local progress. Видео по внешней ссылке не считается offline resource. «Установлено как PWA» не равно «все уроки сохранены» [S03].

## Статусы
`not_prepared → preparing → ready`; runtime может выявить `missing_resources`, `quota_error`, `storage_unavailable`. `ready` ставить после fetch/checksum/write проверки всех требуемых файлов и записей. Не полагаться исключительно на navigator.onLine.

Browser storage имеет quotas/eviction; запрос persistent storage не гарантирует предоставление [S08]. Поэтому «хранится на устройстве» не равно «никогда не потеряется». UI предлагает экспорт резервной копии и раскрывает очистку данных браузером. Private/incognito persistence не обещать.

## Cache/DB ownership
Service worker cache: versioned app assets/approved bundled resources. IndexedDB: user records/imported blobs и manifest. Не смешивать cache eviction с удалением progress. Внешние ресурсы не precache без rights и явного решения.

User imports никогда не запрашиваются сервером по local ID. Deep links ведут к известному static route shell; local arrangement ID из query разрешается на клиенте. Отсутствующий ID показывает recovery, а не необъяснимый404.

## Save
При pause/end/step reflection сохранять session+progress transactionally; попытки append-only. Debounce intermediate position допускается, но explicit exit/pause требует завершить commit либо показать ошибку. Recovery screen сохраняет in-memory export option, когда DB не работает. Повторный click Save не создаёт дубликат attempt.

## Update
Новая версия service worker может ждать. Во время sounding practice не делать forced refresh, skipWaiting reload или destructive migration. Показать «Обновление готово» после pause; сохранить snapshot, подтвердить install, reload, проверить compatible schema. Старые caches удалять только после успешного восстановления и только собственные versioned caches.

Migration: versioned and tested forward; make backup/checkpoint before destructive schema changes; on failure leave old records intact and show retry/export. Newer backup/app schema never treated as empty database.

## Offline test procedure
Build production; serve locally; open First Motif and prepare; inspect complete manifest; stop network; hard reload Home; enter saved lesson; Listen/Try; save reflection; close and reopen; verify exact range/progress. Repeat direct `/practice/` query URL, missing chunk/sample, quota denied, storage eviction and service-worker update while playing. Dev-server success is not proof of production PWA offline.
