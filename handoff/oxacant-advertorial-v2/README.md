# Oxacant Advertorial v2 — handoff

Це окремо підготовлена версія файлу `oxacant advrtrl v2.html`, розділена на HTML, CSS і JavaScript. Поточну робочу версію сайту в `dist/` не змінено.

## Структура

```text
oxacant-advertorial-v2/
├── index.html       # Розмітка та контент головної сторінки
├── styles.css       # Усі стилі, винесені з початкового HTML
├── script.js        # Інтерактив, квіз, вкладки, tracking та конфігурація CTA
├── article.css      # Спільні стилі наявних сторінок статей
├── assets/          # Локальні зображення
└── ratgeber/        # Дві готові окремі сторінки статей
```

## Локальний запуск

Папку потрібно запускати як корінь локального сервера, оскільки частина посилань починається з `/`.

```bash
npx serve .
```

або:

```bash
python -m http.server 8080
```

## Де що редагувати

- Контент і порядок блоків: `index.html`.
- Кольори, типографіка, адаптивність і компоненти: `styles.css`.
- Квіз, вкладки, progress bar, UTM та CTA-посилання: `script.js`.
- Фото: `assets/`.
- Готові статті: `ratgeber/`.

## Що потрібно заповнити перед публікацією

1. У `script.js`, в об’єкті `LINKS`, додати реальні URL для `locator`, `shopApotheke` і `docmorris`. Поки вони порожні, кнопки ведуть на офіційну сторінку продукту.
2. В `index.html` замінити `[Dr. med. Vorname Nachname, Fachrichtung]` на погоджені дані медичного рецензента або прибрати цей рядок.
3. Погодити, чи потрібен `noindex` для advertorial. Відповідний meta-тег поки залишений закоментованим у `<head>`.
4. Додати відсутні майбутні статті:
   - `/ratgeber/nervoeses-herz/`;
   - `/ratgeber/innere-unruhe/`.
5. Перевірити всі медичні твердження, Pflichttext, дозування, canonical URL та зовнішні посилання.

Наявні та включені сторінки статей:

- `/ratgeber/herzstolpern-extrasystolen/`;
- `/ratgeber/druck-auf-der-brust-durch-stress/`.

