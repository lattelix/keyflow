# Проверка документации в CI

Workflow `.github/workflows/docs.yml` проверяет **только пакет планирования** на push/PR: `tools/plan.py validate`, unit tests самого validator и read-only выбор следующей задачи. Это не application CI, не Next/Expo scaffold, не deployment и не разрешение G-IMPLEMENT.

Runner: стандартный `ubuntu-latest`, timeout5min. Permissions: только `contents:read`. Checkout action закреплён на commit `3d3c42e5aac5ba805825da76410c181273ba90b1` (официальный tag v7.0.1, проверен через GitHub API2026-10-06); credentials не сохраняются. Python стандартной библиотеки, без npm/pip/install secrets или внешнего сервиса. Runner не меняет task statuses/gates и не коммитит файлы.

PASS доказывает структуру очереди/ссылок/контрактов и защитные проверки validator, а не корректность музыки/дизайна/реального owner approval. После изменения документации проверить run для exact SHA, а не старый зелёный статус. Если Actions недоступен, выполнить команды локально и честно пометить remote CI NOT RUN. Не включать платный runner или повышать permissions для обхода отказа.
