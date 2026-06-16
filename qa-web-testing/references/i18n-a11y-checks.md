# Internationalization and Accessibility Checks -- Complete Reference

> Comprehensive checklists for testing internationalization (i18n) and accessibility (a11y) in web applications. Each check describes what to do, what to expect, and what constitutes a bug.

---

## 1. Internationalization (i18n)

Internationalization bugs affect every user in the affected locale. These issues are often invisible to developers working in the default language.

### Missing Translations

- [ ] **Switch the application to every available language and navigate through all pages.** Expected: all text is translated in every language. Bug: raw translation keys visible in the UI (e.g., `common.save`, `errors.required`, `dashboard.title` displayed as-is instead of translated text). What to report: the exact key displayed, the page URL, the selected language, and a screenshot.

- [ ] **Check error messages in all languages.** Expected: validation errors, API error messages, and system notifications are all translated. Bug: error messages appear in the default language (usually English) regardless of the selected locale. What to report: the error message text, the expected language, and what triggered the error.

- [ ] **Check dynamic content for translations.** Expected: user-generated content is displayed as-is (no translation needed), but UI labels around it are translated. Bug: labels like "Posted by" or "Comments" remain in the default language while the rest of the page is translated.

- [ ] **Check emails and notifications sent by the application.** Expected: emails and push notifications are sent in the user's preferred language. Bug: all communications are sent in the default language regardless of user preference.

- [ ] **Check placeholder text, tooltips, and aria-labels.** Expected: all helper text is translated. Bug: placeholder text or tooltips remain in the default language. These are frequently overlooked during translation because they are less visible.

### Text Overflow and Layout

- [ ] **Switch to German or French and check all UI elements.** Why: German text is approximately 30% longer than English, and French approximately 20% longer. Expected: all text fits within its container, with wrapping, truncation (with ellipsis and tooltip), or responsive layout adjustments. Bug: text overflows its container, overlaps adjacent elements, is clipped without ellipsis, or breaks the layout.

- [ ] **Check button labels in long-text languages.** Expected: buttons expand to fit the text, text wraps within the button, or text is abbreviated with a tooltip. Bug: text overflows the button boundary, is truncated without indication, or buttons overlap.

- [ ] **Check navigation menus in long-text languages.** Expected: menu items fit or adapt (wrapping, scrolling, truncation with tooltip). Bug: menu items overflow, overlap, or push other elements off-screen.

- [ ] **Check table headers in long-text languages.** Expected: headers wrap, abbreviate, or the table scrolls horizontally. Bug: headers overlap each other or overflow the table container.

- [ ] **Test with very short translations.** Why: some languages (Chinese, Japanese, Korean) produce much shorter text than English. Expected: short text does not break alignment or leave awkward empty space. Bug: layout looks broken with very short text (misaligned elements, empty gaps).

### Date and Time Formatting

- [ ] **Check date display in multiple locales.** Expected format per locale:

| Locale | Expected Date Format | Example |
|--------|---------------------|---------|
| en-US | MM/DD/YYYY or Month DD, YYYY | 03/18/2026 or March 18, 2026 |
| en-GB | DD/MM/YYYY or DD Month YYYY | 18/03/2026 or 18 March 2026 |
| de-DE | DD.MM.YYYY | 18.03.2026 |
| ja-JP | YYYY/MM/DD or YYYY年MM月DD日 | 2026/03/18 |
| ISO 8601 | YYYY-MM-DD (for APIs/exports) | 2026-03-18 |

Bug: dates displayed in the wrong format for the locale (US users seeing DD/MM/YYYY, European users seeing MM/DD/YYYY). This can cause genuine confusion -- "03/04/2026" means March 4 in the US and April 3 in most of Europe.

- [ ] **Check time display.** Expected: 12-hour format with AM/PM for US locale, 24-hour format for most European/Asian locales. Bug: wrong time format for the locale.

- [ ] **Check relative time display** ("2 hours ago", "yesterday", "last week"). Expected: relative time labels are translated and use locale-appropriate phrasing. Bug: relative time in the wrong language or nonsensical phrasing.

- [ ] **Check timezone handling.** Expected: times are displayed in the user's local timezone (or a clearly indicated timezone). Bug: times displayed in UTC or the server's timezone without indication.

### Number and Currency Formatting

- [ ] **Check number display in multiple locales.**

| Locale | Number Format | Example (one million and fifty cents) |
|--------|--------------|---------------------------------------|
| en-US | 1,000,000.50 | Comma for thousands, period for decimal |
| de-DE | 1.000.000,50 | Period for thousands, comma for decimal |
| fr-FR | 1 000 000,50 | Space for thousands, comma for decimal |

Bug: numbers formatted with the wrong locale conventions. A number like "1.050" means 1050 in Germany but 1.05 in the US.

- [ ] **Check currency display.** Expected: correct currency symbol, correct position (prefix vs suffix), and correct decimal precision. Bug: wrong currency symbol, symbol in wrong position ($ vs EUR formatting), or wrong number of decimal places.

- [ ] **Check percentage display.** Expected: locale-appropriate formatting (some locales put a space before the % sign). Bug: inconsistent percentage formatting.

### RTL (Right-to-Left) Support

Only applicable if the application supports RTL languages (Arabic, Hebrew, Farsi, Urdu).

- [ ] **Switch to an RTL language and check the overall layout.** Expected: the entire layout mirrors -- navigation moves to the right, text aligns right, reading order reverses. Bug: layout does not mirror, text reads left-to-right, or navigation stays on the left.

- [ ] **Check directional icons in RTL mode.** Expected: arrows, chevrons, and progress indicators reverse direction. A "next" arrow points left in RTL. Bug: directional icons remain in their LTR orientation.

- [ ] **Check mixed-direction content in RTL mode** (e.g., English brand names, numbers, URLs within Arabic text). Expected: bidirectional text renders correctly with proper isolation. Bug: text direction breaks, words appear in wrong order.

### Pluralization

- [ ] **Check labels that include counts** (items, messages, notifications). Expected:

| Count | English | Rule |
|-------|---------|------|
| 0 | "0 items" or "No items" | Plural or special zero form |
| 1 | "1 item" | Singular |
| 2 | "2 items" | Plural |
| 5 | "5 items" | Plural |

Bug: "1 items" (missing singular form), or pluralization rules incorrect for complex languages (Russian, Arabic, Polish have multiple plural forms).

- [ ] **Check zero-count labels specifically.** Expected: "No items", "0 items", or a contextual empty state. Bug: "-0 items", blank string, or "null items".

### Language Switching

- [ ] **Switch language and verify the entire UI updates.** Expected: all text, labels, dates, numbers, and layout update to the new language without a full page reload (ideal) or with a clean reload. Bug: some elements remain in the previous language, or the page partially renders in mixed languages.

- [ ] **Switch language, navigate to other pages, then refresh.** Expected: the selected language persists across navigation and page refreshes. Bug: language resets to default on navigation or refresh.

- [ ] **Switch language and check that form data is preserved.** Expected: switching language mid-form does not clear the user's input. Bug: form fields are reset when changing language.

### Character Encoding

- [ ] **Enter and display Unicode characters:** emojis, CJK characters (Chinese/Japanese/Korean), accented characters (e, u, n with combining marks), mathematical symbols, currency symbols. Expected: all characters are stored and displayed correctly without corruption. Bug: characters replaced with "?", "□", "???", or mojibake (garbled characters like "Ã©" instead of "e").

- [ ] **Check string length calculations with multi-byte characters.** Expected: character count is based on user-perceived characters, not bytes. Bug: a character limit of 100 allows only 33 CJK characters (counted as 3 bytes each) or truncates emoji mid-sequence.

---

## 2. Accessibility (a11y)

Accessibility issues prevent people with disabilities from using the application. They also frequently indicate general usability problems. Test with keyboard and screen reader, not just visual inspection.

### Keyboard Navigation

- [ ] **Tab through the entire page from top to bottom.** Expected: every interactive element (links, buttons, form fields, dropdowns, toggles, custom controls) receives focus in a logical reading order. Bug: an interactive element is skipped (not focusable), focus jumps to an unexpected location, or non-interactive elements receive focus unnecessarily.

- [ ] **Shift+Tab backwards through the page.** Expected: focus moves in reverse order, hitting every element that Tab reached. Bug: reverse tab order is different from forward tab order, or elements are skipped.

- [ ] **Activate focused elements using Enter and Space.** Expected: buttons and links activate on Enter; checkboxes and toggles activate on Space; links activate on Enter. Bug: a focused element does not respond to keyboard activation.

- [ ] **Navigate dropdown menus and select menus with Arrow keys.** Expected: Up/Down arrows move through options, Enter selects, Escape closes. Bug: arrow keys do not work, or the dropdown cannot be opened/closed via keyboard.

- [ ] **Verify no keyboard traps exist.** Expected: from any focused element, Tab or Shift+Tab moves focus to another element. Bug: focus is stuck on an element with no keyboard method to leave it (common with embedded content, custom widgets, and video players).

- [ ] **Test keyboard shortcuts (if any) for conflicts.** Expected: custom keyboard shortcuts do not conflict with browser or assistive technology shortcuts. Bug: a shortcut overrides a browser shortcut (e.g., Ctrl+P used for something other than print).

### Focus Indicators

- [ ] **Tab through the page and verify every focused element has a visible focus indicator.** Expected: a clear outline, ring, or highlight appears on the focused element, with at least 2px thickness and 3:1 contrast ratio against adjacent colors. Bug: no visible focus indicator on any interactive element (common when `outline: none` is applied without a replacement).

- [ ] **Check that focus indicators are visible on all background colors.** Expected: the focus indicator is visible whether the element is on a white background, dark background, or colored section. Bug: focus indicator is invisible on certain backgrounds (e.g., blue outline on blue background).

- [ ] **Check that custom components have focus indicators.** Expected: custom dropdowns, sliders, tabs, and accordions all show focus. Bug: only native form elements (inputs, buttons) show focus, while custom components do not.

### Skip Navigation

- [ ] **Press Tab once on page load.** Expected: the first focusable element is a "Skip to main content" link (or similar). Bug: no skip link exists, forcing keyboard users to Tab through the entire header and navigation on every page.

- [ ] **Activate the skip link.** Expected: focus moves directly to the main content area, bypassing header and navigation. Bug: the skip link does not move focus, or focus moves to a non-interactive element that loses focus on the next Tab.

### ARIA and Semantic HTML

- [ ] **Check all interactive elements without visible text labels for ARIA labels.** Expected: icon-only buttons, icon links, and image buttons have `aria-label` or `aria-labelledby` providing a descriptive name. Bug: a button with only an icon has no accessible name (screen readers announce "button" with no context).

- [ ] **Check all images for alt text.** Expected: informational images have descriptive alt text; decorative images have `alt=""` (empty alt, not missing alt). Bug: informational images missing alt text (screen readers say "image" with no description), or decorative images with alt text that adds noise.

- [ ] **Check that form labels are properly associated with inputs.** Expected: each input has a `<label>` with matching `for`/`id` attributes, or uses `aria-labelledby`. Clicking the label focuses the input. Bug: labels not associated with inputs (clicking the label does nothing), or inputs with no label at all.

- [ ] **Check error messages are linked to form fields.** Expected: error messages use `aria-describedby` linked to the input's ID, so screen readers announce the error when the field is focused. Bug: error messages are only visually positioned near the field but not programmatically linked.

- [ ] **Check that landmark roles are used correctly.** Expected: page has `<header>`, `<nav>`, `<main>`, `<footer>` landmarks (or ARIA roles). Bug: no landmarks, or the entire page is inside a single `<div>` with no structure.

### Color and Contrast

- [ ] **Check text contrast ratios.** Expected: normal text (under 18px bold or under 24px) has at least 4.5:1 contrast ratio. Large text (18px bold+ or 24px+) has at least 3:1 contrast ratio. Bug: light gray text on white background, or colored text on colored background that fails the ratio. Use a contrast checker tool or browser devtools accessibility panel to measure.

- [ ] **Check that color is not the only indicator of meaning.** Expected: error states use color AND an icon or text label. Active tabs use color AND a different shape/weight/underline. Chart data uses color AND patterns or labels. Bug: a form field turns red for errors with no other indication (screen readers and colorblind users miss this).

- [ ] **Check UI in simulated colorblind modes** (protanopia, deuteranopia, tritanopia). Browser devtools can simulate these. Expected: all information is still distinguishable. Bug: red/green status indicators become indistinguishable, or chart colors blend together.

- [ ] **Check focus indicator contrast.** Expected: the focus indicator has at least 3:1 contrast ratio against the adjacent background. Bug: a light blue focus ring on a white background (common and fails contrast).

### Dynamic Content and Live Regions

- [ ] **Trigger dynamic content updates** (form submission success, error notifications, chat messages, real-time data updates). Expected: screen readers announce the update using `aria-live` regions. `aria-live="polite"` for non-urgent updates, `aria-live="assertive"` for critical alerts. Bug: dynamic content appears visually but screen readers do not announce it.

- [ ] **Check toast notifications and alert banners.** Expected: toast notifications have `role="status"` or `role="alert"` with `aria-live`. Bug: toasts appear and disappear with no screen reader announcement.

- [ ] **Check loading states.** Expected: screen readers announce when content is loading (via `aria-busy="true"` on the loading container, or an `aria-live` announcement). Bug: a loading spinner appears visually but screen readers are silent.

### Modal and Dialog Accessibility

- [ ] **Open a modal and check focus management.** Expected: focus moves to the modal (first focusable element or the modal container). Bug: focus stays behind the modal, on the trigger button.

- [ ] **Tab through a modal.** Expected: Tab cycles within the modal (focus trapping). Tab from the last focusable element goes back to the first. Bug: Tab moves focus behind the modal to the page content.

- [ ] **Press Escape in a modal.** Expected: the modal closes and focus returns to the element that triggered it. Bug: Escape does nothing, or focus does not return to the trigger.

- [ ] **Check that modals have accessible names.** Expected: the modal has `role="dialog"` and `aria-labelledby` pointing to its heading, or `aria-label`. Bug: screen readers announce "dialog" with no title.

- [ ] **Check that background content is inert when a modal is open.** Expected: content behind the modal has `aria-hidden="true"` or uses the `inert` attribute. Bug: screen reader users can navigate to content behind the modal.

### Heading Hierarchy

- [ ] **Check heading levels with a browser accessibility tool or the headings list in a screen reader.** Expected: headings follow a logical hierarchy -- one `<h1>` per page, followed by `<h2>` for major sections, `<h3>` for subsections, and so on. No skipped levels (h1 directly to h3). Bug: multiple `<h1>` tags, skipped heading levels, headings used for visual styling rather than structure, or no headings at all.

- [ ] **Check that heading text is descriptive.** Expected: headings summarize the content of their section. Bug: generic headings like "Details" or "Info" that do not distinguish sections.

### Touch Targets (Mobile)

- [ ] **Check interactive element sizes on mobile viewports.** Expected: all touch targets are at least 44x44 pixels (WCAG minimum), with 48x48 pixels recommended. Bug: small icons, close buttons, or links that are difficult to tap accurately.

- [ ] **Check spacing between touch targets.** Expected: at least 8px between adjacent touch targets. Bug: buttons or links placed so close together that users accidentally tap the wrong one.

### Media Accessibility

- [ ] **Check videos for captions.** Expected: all video content has synchronized captions (closed captions or subtitles). Bug: video plays without any caption option.

- [ ] **Check audio content for transcripts.** Expected: podcasts, audio messages, and other audio content have a text transcript available. Bug: audio content with no text alternative.

- [ ] **Check animations for reduced motion support.** Expected: animations respect the `prefers-reduced-motion` media query. Users who have enabled "Reduce motion" in their OS settings should see minimal or no animations. Bug: complex animations, parallax effects, or auto-playing carousels that do not reduce when the preference is set.

- [ ] **Check for auto-playing media.** Expected: no media auto-plays with sound. If media auto-plays, it should be muted by default with a visible unmute control. Bug: audio or video starts playing with sound immediately on page load.

### Screen Reader Testing Essentials

If testing with a screen reader (VoiceOver on Mac, NVDA or JAWS on Windows), verify these critical paths:

- [ ] **Navigate the page by headings** (VO+Cmd+H on Mac, H on NVDA). Expected: all major sections are reachable via headings. Bug: sections have no headings, or headings are missing or vague.

- [ ] **Navigate by landmarks** (VO+U then arrows on Mac, D on NVDA). Expected: navigation, main, and complementary landmarks are announced. Bug: no landmarks detected.

- [ ] **Navigate by form controls** (VO+U then forms on Mac, F on NVDA). Expected: each form control announces its label and type. Bug: controls announce only "edit" or "button" with no label.

- [ ] **Read a data table** (VO+arrows on Mac, Ctrl+Alt+arrows on NVDA). Expected: table headers are announced when moving between cells. Bug: headers are not associated with cells, or the table is not recognized as a data table.

- [ ] **Complete a full user task using only the screen reader** (sign up, log in, create an item, search). Expected: the entire task is completable. Bug: any step in the task is blocked or confusing without visual context.
