# Primary-source register

Checked 2026-10-06. These sources support technical boundaries, not claims that Keyflow already implements or has tested them. Recheck mutable capabilities, releases and plan terms at the relevant task. Numerical UX/learning/performance thresholds in this specification are project defaults to validate, not external scientific guarantees.

| ID | Primary source | What it supports |
|---|---|---|
| S01 | https://github.com/opensheetmusicdisplay/opensheetmusicdisplay and https://opensheetmusicdisplay.org/typescript-library/ | OSMD renders MusicXML; core is BSD-3-Clause; playback/native sponsor offerings must not be assumed part of free renderer |
| S02 | https://tonejs.github.io/ and https://github.com/tonejs/tone.js/wiki/Transport | Browser audio scheduling uses the audio clock and scheduled callback time; UI timers are not an audio master clock |
| S03 | https://nextjs.org/docs/app/guides/progressive-web-apps | Manifest/install and offline implementation are distinct; installation support differs; static exports need deliberate design |
| S04 | https://www.w3.org/2021/06/musicxml40/tutorial/notation-basics/ | MusicXML notation semantics go beyond MIDI performance data; staff/voice/chord/rhythm information matters |
| S05 | https://docs.expo.dev/workflow/customizing/ and https://docs.expo.dev/faq/ | Custom native modules require development builds, Expo Go is restricted, EAS is optional with plan limits |
| S06 | https://docs.expo.dev/versions/latest/sdk/sqlite/ | Official native SQLite adapter documentation; verify target SDK before use |
| S07 | https://developer.mozilla.org/en-US/docs/Web/API/Web_MIDI_API and https://webmidijs.org/docs/getting-started/ | Web MIDI has limited browser availability and secure-context requirements; detect capability rather than promise all browsers |
| S08 | https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria | Quotas/eviction/persistence caveats motivate explicit resource state and backup |
| S09 | https://vercel.com/docs/plans/hobby | Hobby restrictions and quotas; recheck before deployment; not unrestricted free commercial hosting |
| S10 | https://developer.apple.com/help/account/basics/about-your-developer-account | Development/distribution account capabilities differ; no promise of free unrestricted App Store distribution |
| S11 | https://reactnative.dev/docs/platform-specific-code | Platform-specific implementations are valid; shared contracts need not mean identical renderer code |
| S12 | https://www.w3.org/TR/WCAG22/ | WCAG accessibility requirements; Keyflow48px normal-control target is an internal stricter design choice, not quoted minimum for all cases |

## Candidate checks still required
Parser `fast-xml-parser`, ZIP `fflate`, `@tonejs/midi`, Dexie, Workbox and exact test-tool releases are selected candidates, not locked/verified dependencies in the current repository. KF-017/KF-018/KF-019 must fetch their official docs/package metadata/licenses, record versions, exercise required paths and add evidence before use. Do not cite this table as proof those spikes passed.

## User-content evidence
Repository tree/commit read on2026-10-06 confirmed six initial documents. Figma metadata confirmed only Cover0:1/frame1:10. Vercel Git deployment context showed the existing personal Hobby team but no linked Keyflow project. Detailed initial state is in `docs/STATE.md`. These are connector observations, not facts inferred from web search.
