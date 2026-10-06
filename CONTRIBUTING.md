# Contributing

Start with [AGENTS.md](AGENTS.md) and [START_HERE](docs/START_HERE.md). The current repository is a planning baseline, not a complete application.

Choose one eligible task using `python3 tools/plan.py next`. Do not open a speculative feature PR that bypasses accepted product/design decisions. Use branch `task/<ID>-<short-slug>`, include the task ID, scope, requirement IDs, actual checks and evidence. See the handoff template and reviewer guide.

No personal score imports, audio recordings, secrets or content with unresolved redistribution rights in public commits. Code-license selection and individual content licenses are separate release checks.

Changes to architecture, supported music semantics, learning evaluation, storage format or paid services require the corresponding decision/gate. Fixing a bug is not permission to disable its test or alter the expected musical fixture.

For documentation changes run the Python planning validator and its tests. Application scripts are a future scaffold contract until implemented; do not report nonexistent scripts as passed.
