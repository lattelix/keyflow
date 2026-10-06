# Interaction and copy contract

## Основные подписи RU / EN
Главная/Home; Музыка/Music; Учиться/Learn; Библиотека/Library; Продолжить/Continue; Послушать/Listen; Попробовать/Try; Пауза/Pause; Ещё раз/Retry; Повтор фрагмента/Loop; Темп/Tempo; Левая/Left; Обе/Both; Правая/Right; Метronome label в RU только «Метроном»; Помощь/Hints.

В интерфейсе не показывать «prerequisite graph», «transport», «adapter», «quantization». Термин аккорда можно объяснить в контексте. В code/i18n keys использовать English stable identifiers, не русские фразы как ключи.

## Practice semantics
`Listen`: играет пример, input не оценивается, шаг не завершается автоматически. `Try`: начинается попытка в выбранном basis; count-in перед time-based practice. `Pause`: останавливает scheduling, освобождает ноты, сохраняет позицию. Повторный `Play/Try` продолжает по music-engine contract.

Настройка темпа, рук или loop во время playback автоматически ставит pause; изменение применяется к текущему музыкальному месту. Для продолжения требуется явное нажатие. Не ускорять/переключать руки скрытно.

Tempo UI: quarter BPM оригинала и playback speed раздельно. Для First Motif original60; speed range0.25–1.25 с шагом0.05; показать итоговый quarter BPM. Исходная партитура не переписывается. В alpha нет tempo ramp. Для unsupported meter отображать конкретный import limitation.

Loop range: пользователь задаёт такты start/end включительно в UI; внутренняя граница endExclusive — после последнего выбранного такта. Не допускать пустой диапазон или end<start. Тап по такту выбирает; controls «Начало/Конец» позволяют сделать это без drag. Count-in перед первой попыткой; на повторе опциональный один такт паузы, по умолчанию выключен.

Руки: `targetHand` — что тренирую; `audibleHands` — что слышу. В Listen по умолчанию обе звучат. В Try выбранная рука не должна принудительно заглушаться: отдельный switch «Слышать подсказку моей партии», default off. Accompaniment другой руки можно включить. Метки не смешивать с hideStaff. Без надёжной hand mapping выбор руки недоступен с пояснением.

## Help и overlays
Тап по ноте/символу открывает contextual inspector: название, место/длительность, звук, клавиши, optional источник fingering. Small notation имеет доступный альтернативный выбор предыдущая/следующая нота. Одно нажатие не должно одновременно переместить playhead и раскрыть теорию: selection и seek — разные affordances.

Modal/sheet во время практики ставит pause. Закрытие сохраняет range, position, settings и не включает звук автоматически. Back в Practice завершает/сохраняет текущий attempt как interrupted; подтверждение требуется только для реальной несохранённой операции, не каждый раз. Browser/native Back соблюдает тот же смысл.

## Feedback
Self-report: «Как получилось?» + три действия из learning contract; никаких процента/зелёной отметки автоматически. Touch: «Верно выбрана клавиша на экране». MIDI: «Проверено по MIDI» + диапазон/темп и конкретная ошибка. Цвет дублируется текстом/иконкой. Ошибка не наказание: одна поправка за раз.

Пусто: причина+действие. Error: что не удалось+сохранены ли данные+повтор/другой путь. Loading не бесконечный: доступна отмена тяжёлого import. Offline-ready, offline-missing и storage-unavailable — разные состояния. Не писать «сохранено» до успешной транзакции.

## Keyboard/accessibility
Space=play/pause только когда focus не в text input, menu/dialog или другом control с собственной Space семантикой. Escape закрывает верхний dismissible overlay, возвращая focus; не стирает данные. Arrow shortcuts действуют только в focused score/piano context и имеют screen-reader альтернативу. IconButton всегда имеет accessible name; tooltip не единственный источник смысла.

No sound until gesture. Аудио/видео остановить при уходе с Practice, потере контекста или system interruption. UI animation не является master clock. Reduced motion убирает лишние переходы, сохраняя мгновенную индикацию текущей позиции.
