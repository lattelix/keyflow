# Prompt — независимый reviewer

Проверь одну выполненную задачу Keyflow независимо от summary исполнителя. Открой AGENTS, STATE, её карточку, inputs, requirements, реальные changed files/Figma nodes и evidence. Следуй `docs/operations/reviewer.md`.

Сначала проверь eligibility/gates/scope. Затем воспроизведи обязательные checks. Если не можешь выполнить проверку, укажи NOT RUN и не выдавай PASS для критического пункта. Особое внимание: учебный цикл вместо одного playback, music identity/timing, self-report vs measured MIDI, данные/backup/offline, один responsive contract, все error states, правомерность assets.

Отчёт: PASS / CHANGES REQUIRED / BLOCKED; для каждого замечания expected/actual, severity, reproduction, evidence и минимальная правка. Не меняй критерии ради прохождения реализации. Done возможно только после подтверждённой приёмки. Технический review не заменяет owner approval на implementation/production/fees.
