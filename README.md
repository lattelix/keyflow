# Keyflow

**Learn the music you actually want to play.**

Keyflow is a song-first piano-learning project: a learner chooses a piece, learns the missing basics in context, practices manageable phrases, and gradually removes assistance. Web/PWA first; iOS/Android later using the same product contracts and domain logic.

## Start here

- [Agent entry point](AGENTS.md)
- [Context and document map](docs/START_HERE.md)
- [Verified project state](docs/STATE.md)
- [Execution plan](docs/plan.md) · [Roadmap](docs/roadmap.md)
- [Product specification](docs/product.md) · [Designer brief](docs/design.md)
- [Architecture](docs/architecture.md) · [Decisions](docs/decisions.md)
- [Task queue](docs/tasks/queue.json) · [Execution guide](docs/operations/agent-playbook.md)

Repository: https://github.com/lattelix/keyflow

Figma: https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn

## Actual status

This repository contains the execution specification and its validation tooling. **It is not a working piano app.** Designs, application code, application CI, deployment, native builds and instrument verification must not be reported as completed because they appear in the plan.

The first useful release must contain one complete guided learning journey, not just a score player. Automatic grading is unavailable without a supported input source; self-assessment is explicitly labelled.

## Commands available now

```sh
python3 tools/plan.py validate
python3 tools/plan.py next
python3 tools/plan.py show KF-001
python3 -m unittest discover -s tools -p 'test_*.py'
```

These validate/select planning tasks, not the application. Application commands are defined as future contracts in [commands.md](docs/operations/commands.md).

## Scope and costs

No required account, backend, paid AI API, subscription or proprietary music-player dependency for the web MVP. Hosting/build quotas and app-store distribution have separate conditions; see [services.md](docs/engineering/services.md). Music rights are separate from code rights. `Another Love` is a personal UX reference, not bundled demo content.

License selection is recorded as an owner decision before release; public visibility alone is not an open-source license. See [content policy](docs/content/policy.md).
