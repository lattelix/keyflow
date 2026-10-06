# Команды: существующие и будущие

## Существуют в пакете планирования
Python 3, только стандартная библиотека; выполнять из root:

```sh
python3 tools/plan.py validate
python3 tools/plan.py next
python3 tools/plan.py next --role designer
python3 tools/plan.py show KF-010
python3 -m unittest discover -s tools -p 'test_*.py'
```

`validate`: ненулевой exit code при ошибках очереди, gates, requirements, ссылок inputs, screen/component contracts или состояний завершения. `next/show`: read-only. Ни одна команда не запускает приложение и не открывает gate.

## Контракт будущего scaffold — KF-017
Эти команды **пока не настроены**, и до создания package.json их нельзя включать в отчёт как выполненные:

| Script | Должен делать |
|---|---|
| `pnpm dev:web` | Запускать web dev server |
| `pnpm lint` | Реально линтить изменяемые app/packages, без always-success заглушек |
| `pnpm typecheck` | Проверять TypeScript во всех активных packages |
| `pnpm test:unit` | Vitest domain/music/learning/storage tests |
| `pnpm test:ui` | Testing Library UI behavior; не только snapshot |
| `pnpm test:e2e` | Playwright Chromium/Firefox/WebKit по acceptance matrix |
| `pnpm build:web` | Production build web и service-worker pipeline |
| `pnpm check` | docs validation + lint + typecheck + unit + UI + build; e2e отдельным явным шагом |

KF-017 должен создать scripts, README запуска, зафиксировать версии и выполнить каждый созданный базовый script. Там, где тестируемой фичи ещё нет, pipeline не должен ложно именоваться полной acceptance-проверкой. Playwright coverage добавляется по мере feature tasks.

В native phase: реальные `expo run:ios`/`expo run:android` через согласованные pinned scripts после development-build setup. EAS optional; cloud build не обязателен и не автоматически бесплатен без ограничений.
