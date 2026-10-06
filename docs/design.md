# Designer brief — единый Keyflow

## Результат, который нужен
Не набор красивых страниц, а компонентный интерактивный prototype, по которому новичок понимает действие без устного сопровождения, а разработчик понимает состояния/переходы без догадок. Все размеры — один продукт; desktop не отдельная логика.

Figma: https://www.figma.com/design/STjpIkSSiMvFfe9lFog0Yn. Работать только в личном workspace пользователя. Сначала KF-001: текущая структура частично не подтверждена. Не использовать IDs несуществующих страниц.

## Визуальное направление
Спокойный инструмент рядом с пианино: много пространства для нот, ясный контраст, минимум декоративных панелей. Без рекламных баннеров, streak-pressure, рейтингов пользователей, космических фонов, стеклянных поверхностей и бесконечных карточек. Светлая тема — читабельная нотная бумага; тёмная — комфортный тёмный workspace с хорошо видимыми линиями и нотами.

Стартовые значения и semantic names — `design/tokens.json`. Это baseline-предложение для построения foundations, не утверждённый финальный brand. Изменения после визуальной проверки фиксировать в tokens и report, не локальными цветами. Копировать стиль TalentBay/Libman Studio запрещено; допускаются общие инженерные принципы компонентов.

## Порядок построения
Inventory → tokens/styles → primitives → музыкальные компоненты → composite components → экранные состояния → responsive views → clickable flow → structural/visual QA → handoff. Не строить 30 экранов detached rectangles, чтобы «позже компонентировать».

Страницы-цели: `00 · Cover`, `01 · Foundations`, `02 · Components`, `03 · Flows`, `04 · Mobile`, `05 · Tablet`, `06 · Desktop`, `07 · Prototype`, `99 · Archive`. Эти имена — целевая структура, не inventory. Mobile/Tablet/Desktop содержат instances общего набора.

## Контракт слоёв
Имена: `S08 / Practice / Compact / Paused / Guided / Light`; компонент `KF/Button`; sublayers `Container`, `LeadingIcon`, `Label`, `TrailingIcon`, `FocusRing`. Иконки — instances со swap property, а не векторные копии. Text/Boolean/InstanceSwap properties экспортируются. Варианты — для реальных различий, не всех возможных комбинаций сразу.

Auto Layout для связанных групп; HUG для текста/контентных карточек, FILL для гибкой ширины, FIXED для иконок/контрольных размеров и viewport только по контракту. Absolute position — для слоя playhead/нот/клавиатурной геометрии, а не для обычной компоновки страницы.

Фреймы не являются components по умолчанию: повторяемые UI — main component + instances. Не detach. Значения spacing/color/radius привязаны к variables; type styles едины. Figma design-system publication не включать автоматически, если достаточно local components.

## Что видно во время практики
Один текущий goal, диапазон фразы, реальная партитура, позиция, optional hints, клавиши при необходимости, transport и ясный input basis. Не показывать одновременно chord gallery, skill tree, full analytics, video и ноты на телефоне.

В portrait упор на короткую фразу. На планшете/desktop ноты занимают основную область. Настройки не перекрывают проигрываемый score: открытие блокирующего overlay переводит practice в pause и сохраняет позицию.

## Учебные данные
Использовать `learning/reference-journey.md`. В Figma помечать demo performance feedback как «Пример». Нельзя придумывать ноты ради композиции. Если рендер точной записи недоступен, сначала создать проверенный исходник, затем поместить его для макета и отметить, что в коде он будет интерактивным renderer, а не PNG.

## Обязательные deliverables
1. Token collections + styles с light/dark, scopes и примерами.
2. Inventory `components.json`: требуемые props/states, документация употребления.
3. Inventory `screens.json`: нормальные, пустые, error, unavailable, offline и recovery состояния.
4. Responsive contract: заданные размеры и behaviour, не только скриншоты.
5. Prototype: newcomer route, resume, import failure, MIDI-unavailable fallback, backup restore.
6. Handoff map screen/component ID → stable Figma node → approved state → будущий code path. Не выдумывать IDs. Пока все product nodes могут оставаться null.
7. QA report: screenshots, structural checks, прототип-клики, замечания и исправления.

## Definition of done
Каждый обязательный экран/компонент покрыт; no detached repeated UI; нет overflow/нечитаемых нот; UI понятен в RU и EN; contrast/focus/large targets проверены; состояния не являются тупиками; prototype протестирован; owner принимает результат отдельно в `G-IMPLEMENT`. Обложка или статичный экспорт не закрывают задачу.
