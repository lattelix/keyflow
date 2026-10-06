# Toolchain freeze procedure — KF-017

## Why no fabricated exact versions
Existing repository has no installed application stack or lockfile. A version in an old chat is not evidence of current compatible SDKs. Stack family is fixed; exact releases must be resolved once with official compatibility guidance, then frozen. This procedure is part of the task, not permission to continuously choose `latest`.

## Steps
1. Read official stable Next.js and Expo release/compatibility docs and engine requirements. Record URLs, date, stable version, required React/RN/Node and peer ranges. Exclude canary/beta/nightly.
2. Choose one supported Node LTS satisfying the selected tools and one exact pnpm version. Record OS/architecture tested; do not assume container runtime equals user's Mac.
3. Freeze web stack now. Expo/RN version resolution is a documented native compatibility target, revalidated in KF-043 before actual native install; do not force a conflicting global React version across future apps.
4. Resolve OSMD/Tone/import/storage/test libraries, inspect licenses/maintenance/security advisories and peer dependencies. Missing compatibility evidence → blocker/ADR, not package-manager `--force`.
5. Create `docs/engineering/versions-lock.json` with exact versions and sources, packageManager field, engine constraint, `.nvmrc`/equivalent and pnpm lockfile. Do not add these files with invented placeholder versions in planning phase.
6. Install from lockfile on a clean checkout. Materialize command contracts in operations/commands; run existing checks/build. Record exact output and limitations. New app tests require actual feature tests later.

## Future upgrade rule
Dedicated task/PR: purpose, old/new versions, peer-impact, migration notes, clean install, typecheck/unit/UI/e2e/build and real-device checks when native dependencies change. No incidental major update inside a design-fidelity fix.

## Free/test infrastructure
Start local and CI standard runners. No paid cloud credits just to make a build green. Node/SDK/tool install is development setup after G-IMPLEMENT, not a production deployment. Browser binaries for tests may require network; disclose unavailable execution instead of claiming tests passed.
