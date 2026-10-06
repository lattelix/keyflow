# Services, costs and infrastructure boundaries

## Required now
GitHub for source/docs; existing personal Figma file for design. No new SaaS account is needed to read or execute the planning package. Documentation checker is Python stdlib. No API key, backend or deployment is created by the plan.

## Later, after G-IMPLEMENT
| Layer | Choice | Constraint |
|---|---|---|
| Source/CI | GitHub + Actions | Workflow only after scripts exist; least permissions; public-repo allowances do not mean every runner/feature is free |
| Web hosting | Existing Vercel Hobby team, initially preview | Hobby is personal/non-commercial with quotas [S09]; recheck terms/usage before link; no paid upgrades |
| Local data | IndexedDB / SQLite | No paid cloud database; storage risks documented |
| App builds | Local Expo development builds | EAS optional with its own quotas; custom modules need dev build [S05] |
| Native distribution | PWA first, stores later | Apple/Google accounts/signing/fees are separate approvals; do not promise free store publishing [S10] |
| Music rendering | OSS OSMD adapter | No sponsor-only player/native module dependency [S01] |
| Audio | Own scheduler adapter + cleared sounds | Samples rights separate; no paid sample subscription |
| Analytics/AI | None mandatory | Local debug only; no upload of scores or performances |

## Vercel runbook — KF-036, not now
1. Verify G-IMPLEMENT, accepted alpha checks and existence of a production-buildable web directory.
2. Read current Vercel team/repository links; only personal `Alex's projects`, only `lattelix/keyflow`.
3. Check rootDirectory `apps/web`, build mode/output and pnpm workspace source inclusion from actual repo. Static export output `out` only if KF-019 retained this mode; no blind framework defaults.
4. Create/reuse Git-linked project using current connector schema. Initial deployment must be preview. Do not create an unlinked bare duplicate or touch other project domains.
5. Read deployment status/build logs, open actual URL, smoke-test exact commit, routes, assets, offline install readiness and security headers. Write real project/deployment IDs and URL to private-appropriate operational evidence; no secret tokens.
6. Production promotion only after `G-PRODUCTION`. No domain purchase or DNS changes in this task.

## Native distribution
Do not create store credentials or Apple/Google enrollment during a coding task. A local simulator build, device dev build, TestFlight/internal testing and public store release are different outcomes. Report exactly which one occurred. Paid memberships/accounts need owner confirmation with current pricing. Native app work does not require using EAS cloud if local build suffices.

## Deferred infrastructure
No Neon/Supabase/Postgres, authentication, object storage account, Cloudflare deployment, analytics service or sync queue for alpha. KF-048 may prepare a bounded sync design after G-SYNC, but provisioning requires its own accepted ADR and budget. Never reuse a production DB from TalentBay/LS.
