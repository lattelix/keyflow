# Design direction

## North star
A calm instrument-side workspace, not a score marketplace. Opening the app answers: what am I practicing, why, and what do I press next?

## Cross-platform contract
One semantic design system across Web/PWA, iOS and Android. Layout adapts; information architecture, component names, states and tokens do not fork.

## Device intent
Phone portrait: learning + short practice.
Phone landscape: focused practice.
Tablet: primary digital music stand.
Desktop/web: score + guidance + analytics with additional horizontal space.

## Practice hierarchy
Current goal → score/playhead → assistance → interactive keyboard → transport → feedback/next action.

## Guidance levels
Beginner: note names + keyboard + chord labels + explanations.
Learning: notation + selective keyboard/fingering.
Independent: notation only.
Performance: minimal chrome.

## Figma
00 Cover; 01 Foundations; 02 Components; 03 Flows; 04 Mobile; 05 Tablet; 06 Desktop; 07 Prototype; 99 Archive.

## Core components
AppShell, Navigation, Button, IconButton, Search, SongCard, Progress, SkillChip, LessonCard, ScoreViewport, Playhead, PianoKeyboard, PianoKey, ChordCard, FingeringHint, Transport, TempoControl, LoopControl, HandSelector, MetronomeControl, FeedbackBanner, BottomSheet, Dialog, Tooltip, Tabs, SegmentedControl and Empty/Error/Offline states.
