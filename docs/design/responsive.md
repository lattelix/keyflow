# Responsive contract

## Одинаковое и адаптивное
Одинаковы: screen IDs, значения props, команды, состояния, terminology, data model, tokens и доступные действия. Адаптивны: число колонок, navigation chrome, расположение inspector, вид secondary controls. Native system dialogs/file pickers/permissions не должны имитироваться web-макетом.

## Размеры
Primary review: phone390×844; phone landscape844×390; tablet820×1180; tablet landscape1180×820; desktop1440×900. Boundary QA:320,360,599,600,768,1023,1024,1920 px width. Проверять также увеличенный текст200% и короткую высоту.

Compact: width<600. Medium:600≤width<1024. Expanded:width≥1024. При height<500 применяется short-height Practice вне зависимости от width; не заставлять orientation lock.

| Режим | Navigation | Основной layout | Practice |
|---|---|---|---|
| Compact | Bottom navigation4 пункта; safe area отдельно | padding16, gap16, одна колонка | Header/goal → phrase score → optional keyboard → reserved transport; inspector как sheet только на pause |
| Medium | Rail88 или compact nav при short-height | padding24, fluid content | Score flex; theory/controls в sheet; keyboard optional |
| Expanded | Sidebar240 вне Practice | padding32, max content1440 | Score flex + optional inspector320 при достаточной ширине; transport снизу отдельной строкой |
| Short-height | Navigation hidden только в focused Practice | padding8–16, минимум chrome | Score first; один ряд controls48; keyboard свернуть по умолчанию; inspector dialog на pause |

На expanded при доступной ширине score<600 скрыть inspector в drawer; не сжимать ноты. На телефоне показывать одну музыкальную систему/фразу, не всю страницу уменьшенной до нечитаемости. Staff-space не меньше7 logical px: при нехватке ширины reflow, затем горизонтальный просмотр выбранной фразы с явной индикацией продолжения. Document/page-level horizontal overflow запрещён.

## Высоты и safe areas
Transport получает собственное место в layout. Не размещать поверх последней строки нот. Bottom chrome = высота контрола + padding + platform safe-area inset; не хардкодить iPhone notch. На web учитывать dynamic viewport/виртуальную клавиатуру. Modal/Sheet фокусирует свой контент и возвращает фокус исходному контролу.

Если body text не помещается при200%, lesson scroll; primary CTA остаётся достижимой без наложения. Practice может перейти из side-by-side в stack. Screen reader outline сохраняет logical order: цель, basis, score description, controls, feedback.

## Клавиатура
В режиме обучения отдельным нотам compact показывает ограниченную октаву, а не88 микроклавиш. Отдельный `NotePad` предоставляет крупные подписанные кнопки всем доступным pitch — обязательная альтернатива узким чёрным клавишам. Геометрия piano keys остаётся музыкально верной; расширенные hit areas не перекрываются и не выбирают неправильную клавишу.

При аккорде/фразе диапазон автоматически подбирается к видимому материалу и подписывает октавы. Пользователь может переместить диапазон; это не меняет score pitch. NotePad/keyboard не изображаются как доказательство моторного навыка на реальном инструменте.

## Acceptance
По каждому primary frame сохранить screenshot и structural bounds check. На boundary widths проверить reflow при resize, не только отдельные нарисованные экраны. Зафиксировать какая информация скрыта/доступна через overlay. Ни один критический action не должен исчезать без альтернативы.
