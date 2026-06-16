---
name: qa-web-testing
description: Use this skill whenever the user wants to test a web application, needs a testing checklist, asks what to test, mentions form testing, navigation testing, console errors, network monitoring, i18n testing, accessibility testing in a QA context, or browser-based testing. Also use when the user says "test this page", "check for errors", "run through the checklist", or asks about edge cases to test. This skill provides the comprehensive testing checklists that qa-explorer agents use to systematically find bugs.
---

# Web Application Testing Checklists

This skill provides structured, actionable testing checklists for web applications. It covers functional testing (forms, navigation, CRUD, auth, search), technical testing (console errors, network monitoring, performance), internationalization, accessibility, and edge case patterns designed to surface bugs that typical testing misses.

Apply these checklists to any browser-based application -- public websites, internal tools, SPAs, dashboards, e-commerce platforms, and authenticated web apps.

---

## Functional Testing Quick Reference

Core user-facing behaviors that must work correctly. Test these first.

| Area | Key Checks | Common Bugs Found |
|------|------------|-------------------|
| **Forms** | Empty submit, boundary values, special characters, double submit, paste behavior | Missing validation, XSS vectors, duplicate records, data truncation |
| **Navigation** | All links work, back button state, deep links, breadcrumbs, 404 handling | Dead links, lost form data on back, broken bookmarks, missing 404 page |
| **CRUD** | Create with min/max fields, update preserves unchanged fields, delete confirms, bulk ops | Partial saves, silent data loss on update, orphaned records on delete |
| **Authentication** | Login/logout, session expiry, role boundaries, concurrent sessions, CSRF | Session fixation, privilege escalation, stale sessions after logout |
| **Search & Filters** | Empty results, special chars, filter combinations, pagination with filters, sort + filter | Crashes on special chars, filters lost on paginate, wrong sort order |

### Forms -- What to Test First

1. Submit the form completely empty -- every required field should show a validation error
2. Enter the maximum allowed length, then max + 1 character -- verify truncation or rejection
3. Paste `<script>alert(1)</script>` into every text field -- output must be escaped, never executed
4. Click the submit button rapidly twice -- only one record should be created
5. Fill the form, navigate away, come back -- check if data persists or is properly cleared

### Navigation -- What to Test First

1. Click every visible link on the page -- none should return a 404 or blank page
2. Fill a form partially, click the back button, then forward -- form state should be preserved or intentionally cleared
3. Copy the current URL, open it in a new incognito tab -- the page should load correctly (or redirect to login)
4. Enter a URL that does not exist -- a custom 404 page should appear, not a browser default or stack trace

### CRUD -- What to Test First

1. Create an entity with only the required fields filled -- it should save successfully
2. Open the detail view -- every field you saved should display accurately
3. Edit one field and save -- all other fields must remain unchanged
4. Delete an entity -- a confirmation dialog should appear before deletion
5. Create the same entity twice -- the system should either prevent duplicates or handle them gracefully

### Authentication -- What to Test First

1. Log in with valid credentials -- should redirect to the expected landing page
2. Log out, then press the browser back button -- should not show authenticated content
3. Open an admin-only URL while logged in as a regular user -- should show a 403 or redirect
4. Stay idle past the session timeout -- the next action should prompt re-authentication

### Search & Filters -- What to Test First

1. Search for a term that returns no results -- an empty state message should appear, not a blank page
2. Apply a filter, then paginate -- the filter should persist across pages
3. Apply multiple filters simultaneously, then clear all -- the full unfiltered list should return
4. Search with `' OR 1=1 --` -- should return no results or safe output, never a database error

> Full functional testing checklists with detailed steps and expected outcomes: see `references/functional-checks.md`

---

## Technical Testing Quick Reference

Issues users may not notice immediately but that indicate real bugs or degraded quality.

| Area | What to Monitor | Severity Signals |
|------|----------------|-----------------|
| **Console Errors** | JS exceptions, framework warnings, failed resource loads, CORS errors | TypeError and ReferenceError are almost always real bugs; React key warnings indicate list rendering issues |
| **Network Requests** | 4xx/5xx responses, slow responses (>3s), failed requests, excessive calls | 500 errors are server bugs; 401/403 after login indicate auth problems; 50+ calls to same endpoint suggest N+1 queries |
| **Performance** | LCP, CLS, INP, memory growth, large list rendering | LCP > 2.5s is poor; any visible layout shift is a bug; memory growing on repeated navigation is a leak |
| **Browser State** | localStorage, cookies, cache behavior, History API | Missing secure/httpOnly flags on auth cookies; stale content after deploy |

### Console Errors -- Triage Guide

| Error Type | Usually a Real Bug? | Action |
|-----------|---------------------|--------|
| TypeError: Cannot read property of undefined | Yes | Report with full stack trace and reproduction steps |
| ReferenceError: x is not defined | Yes | Report -- a variable or import is missing |
| React: Each child in a list should have a unique "key" | Yes | Report -- causes rendering issues and performance problems |
| React: Can't perform state update on unmounted component | Yes | Report -- memory leak from async operations |
| Mixed Content warning | Yes | Report -- security issue, resources loaded over HTTP on HTTPS page |
| CORS error | Yes | Report -- API misconfiguration |
| 404 for image/font/CSS/JS | Yes | Report -- missing or misreferenced asset |
| React StrictMode double-render | No | Ignore -- development mode behavior only |
| HMR (Hot Module Replacement) messages | No | Ignore -- development tooling |
| Vue devtools messages | No | Ignore -- development tooling |

### Network Monitoring -- What to Watch For

| Status Code | Meaning | Is It a Bug? |
|------------|---------|-------------|
| 400 Bad Request | Client sent invalid data | Maybe -- could be missing frontend validation |
| 401 Unauthorized | Not authenticated | Bug if user is logged in; expected if session expired |
| 403 Forbidden | Authenticated but not authorized | Bug if user should have access; expected for role restrictions |
| 404 Not Found | Resource does not exist | Bug if the resource should exist; expected for deleted items |
| 409 Conflict | Duplicate or conflicting operation | Usually a bug -- frontend should prevent or handle this |
| 422 Unprocessable Entity | Validation failed server-side | Maybe -- should be caught by frontend validation first |
| 429 Too Many Requests | Rate limited | Bug if triggered by normal usage; investigate excessive API calls |
| 500 Internal Server Error | Server crash | Always a bug -- report with request details |
| 502/503 Bad Gateway/Unavailable | Server down or overloaded | Infrastructure issue -- report immediately |

> Full technical testing checklists with console patterns, network analysis, and performance metrics: see `references/technical-checks.md`

---

## i18n & Accessibility Quick Reference

Internationalization and accessibility issues that are easy to miss but affect large user populations.

| Area | Quick Checks | What Constitutes a Bug |
|------|-------------|----------------------|
| **Missing translations** | Look for raw keys like `common.save` or `errors.required` displayed in the UI | Any translation key visible to the user is a bug |
| **Text overflow** | Switch to German or French (30% longer than English) or test with long strings | Text clipped, overlapping, or breaking layout |
| **Date/number formats** | Check date and number display against the active locale | MM/DD/YYYY shown to European users, or period vs comma decimal |
| **Keyboard navigation** | Tab through the entire page -- every interactive element must be reachable | Any focusable element skipped, or focus order illogical |
| **Focus indicators** | Tab and look -- every focused element needs a visible outline | Missing or invisible focus ring on any interactive element |
| **Color contrast** | Check text against background -- 4.5:1 for normal text, 3:1 for large text | Text that fails contrast ratio requirements |
| **Screen readers** | All interactive elements need accessible names; dynamic content needs aria-live | Buttons with no label, images with no alt text, silent dynamic updates |

### Edge Case Patterns (Quinn QA Methodology)

These inputs are specifically designed to break applications. Test every text input and form field with these values:

| Category | Test Values | What Breaks |
|----------|------------|-------------|
| **Empty/minimal** | Empty string, single space, single character | Missing required validation, whitespace-only accepted as valid |
| **Negative numbers** | -1, -0, -999999 | Fields that should only accept positive values |
| **Extreme values** | 0, 999999999, MAX_INT (2147483647), Number.MAX_SAFE_INTEGER | Integer overflow, display overflow, database column limits |
| **Very long text** | 1000+ characters, 10000+ characters | Text truncation without indication, layout breakage, performance lag |
| **Special characters** | `<script>alert(1)</script>`, `' OR 1=1 --`, `"; DROP TABLE users;--` | XSS, SQL injection (should be handled server-side too, but frontend should escape) |
| **Unicode & emoji** | `cafe\u0301` (combining characters), `\u200B` (zero-width space), emojis, CJK characters | Encoding issues, display corruption, sorting errors, length miscalculation |
| **Rapid interactions** | Click submit 5 times rapidly, toggle switch 10 times quickly | Duplicate submissions, race conditions, UI state desync |
| **Mobile viewports** | 320px width, 768px width, landscape/portrait toggle | Layout overflow, hidden controls, touch target too small, text unreadable |
| **Clipboard** | Paste rich text (from Word/Google Docs), paste into number-only fields | Rich formatting injected, non-numeric characters in number fields |

> Full i18n and accessibility testing checklists: see `references/i18n-a11y-checks.md`

---

## Reference Files

For detailed, step-by-step testing checklists on each topic, consult:

| File | Contents |
|------|----------|
| `references/functional-checks.md` | Forms, navigation, CRUD, authentication, and search/filter testing with specific steps, expected results, and bug criteria for each check |
| `references/technical-checks.md` | Console error monitoring, network request analysis, performance metrics, and browser state verification with triage guides and severity ratings |
| `references/i18n-a11y-checks.md` | Internationalization checks (translations, formatting, RTL), accessibility audits (keyboard, screen reader, contrast, focus), with WCAG compliance criteria |
