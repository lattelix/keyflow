# Architecture

## Decision
TypeScript monorepo.

- apps/web — Next.js + React + PWA, Vercel
- apps/mobile — Expo + React Native, iOS/Android
- packages/domain — songs, lessons, practice, progress
- packages/music — MusicXML/MIDI parsing, timing and practice-engine contracts
- packages/ui — semantic tokens and cross-platform component contracts
- packages/config — shared tooling

## Data
MVP is local-first. Web uses IndexedDB; native uses SQLite behind repository interfaces. Cloud accounts/sync arrive after the local MVP proves useful.

## Music and input
MusicXML is the notation interchange; MIDI covers performance/input where applicable. Rendering engines remain replaceable behind adapters. Phase 2 adds Web MIDI and native MIDI.

## Deployment
GitHub is source control/CI origin. Vercel hosts web preview/production. Native builds use Expo/EAS when mobile implementation starts.

## Backend
No mandatory backend for v0.1–v0.3. Later sync can use Postgres + object storage; provider choice is intentionally deferred.
