# MIDI phase contract — gated, not implemented

## Capability and device model
Detect `navigator.requestMIDIAccess`/secure context at runtime on web; request only on explicit connect with SysEx disabled. Unsupported, denied, no-device and disconnected are separate UI states. Browser coverage is limited; do not promise native Web MIDI in Safari or identical iPhone behavior based only on installing the PWA [S07]. Native adapters use their platform APIs after a development-build spike [S05].

Resolve actual keyboard/cable/port before claiming hardware compatibility. Connecting an app does not prove every digital piano has the required interface. When input disappears: release notes, pause measured attempt, save interrupted basis, offer reconnect or explicit self-report switch. Never silently continue measured scoring from fake events.

## Normalized events
`note_on(pitch, velocity>0, timestampDeltaMs, channel)`, `note_off(pitch, timestampDeltaMs, channel)`, optional controller. MIDI note-on velocity0 normalizes to off. Maintain active pitches per channel/device; aggregate only when matching policy says so. Ignore messages outside selected input; do not transmit arbitrary commands to instrument.

## Two separate modes
1. **Step/wait**: match next expected pitch set, allow no tempo score. Chord assembly window initial200ms from first matching press; exact expected set required within window, wrong pitches explained. This is a configurable learning heuristic, not virtuosity standard. Timeout doesn't permanently lock the learner.
2. **In-time**: match onsets one-to-one by pitch within time window; unmatched expected=missed, unmatched played=extra. Do not reuse a played note for two expected attacks. Ties expect one initial attack, not one per printed segment.

Initial timing window W=min(250ms,max(100ms,0.2*quarterDurationMs)); explicit matcherVersion. Systematic latency correction only from a recorded calibration procedure; unknown calibration displayed as such. Audio/USB/Bluetooth latency cannot be universally inferred from one browser timer.

## Metrics
Show matched/expected, missed, extra, timing distribution and actual tempo/range. Precision=matched/(matched+extra), recall=matched/expected, null for zero denominator. Avoid one opaque score. Never label self-report as either metric. Fingering, hand used, pedalling quality, phrasing and musicality remain unmeasured unless separately implemented and validated.

## Deterministic QA
Fixtures: single note, repeated same pitch, simultaneous chord, arpeggiated input, extra note, late note, tie, unison voices, note-on0, sustain event, device disconnect, double connection, calibration unknown, no events. Use a fake clock for algorithm tests, but label them synthetic.

Physical QA then repeats a known phrase on an actual identified instrument. Record device/interface, OS/browser/build, audio output route, calibrated status, expected and observed failures. Never use an emulator screenshot as proof of real latency or MIDI compatibility.
