# Oracle Layers — Complete Reference

> Oracles are the heuristic rules a tester uses to decide whether observed application behavior constitutes a bug. Since black-box testers have no specification to compare against, oracles provide structured reasoning frameworks ranked by reliability. Higher reliability means the oracle produces fewer false positives.

---

## 1. Crash Oracle (100% Reliability)

**Principle**: The application fails in an unambiguous, undeniable way. There is no interpretation needed -- the system is broken.

A Crash oracle finding is always a real bug. There are zero false positives because the application is objectively non-functional.

### What Counts as a Bug

- **HTTP 500 (Internal Server Error)**: The server encountered an unhandled error. Any 500 response visible to a user is a bug, regardless of context.
- **Uncaught JavaScript Exceptions**: Errors that appear in the browser console as `Uncaught TypeError`, `Uncaught ReferenceError`, `Unhandled Promise Rejection`, or similar. These indicate code paths that the developers did not account for.
- **Blank / White Pages**: A page that should render content but displays nothing. The HTML may load but the application framework fails to mount or render.
- **Infinite Loading States**: A spinner, skeleton loader, or progress bar that never resolves. The page is stuck and the user cannot proceed.
- **Application Crashes**: The browser tab crashes, the application displays a framework-level error screen (e.g., React error boundary, Next.js 500 page, "Something went wrong"), or the entire UI becomes unresponsive.
- **HTTP 4xx on Core Resources**: 404 errors on JavaScript bundles, CSS files, or API endpoints that the page depends on to function.

### How to Detect

1. **Console Monitoring**: Open the browser developer tools Console tab before navigating. Watch for red error entries. Filter by "Errors" to isolate uncaught exceptions from warnings.
2. **Network Tab Monitoring**: Open the Network tab and filter by status codes. Look for any request returning 4xx or 5xx. Pay special attention to XHR/Fetch requests that return errors, as these often power core UI functionality.
3. **Page Content Checks**: After navigation or action, verify that the page contains expected content. A blank `<body>` or a page with only a header/footer but no main content indicates a rendering crash.
4. **Timeout Detection**: If a page or component has not rendered within 15 seconds, it is likely stuck. Note the last network request and any console errors at the time of the freeze.

### Examples

| Scenario | Evidence | Severity |
|----------|----------|----------|
| User clicks "Save" and the API returns 500 | Network tab: `POST /api/projects` → 500 Internal Server Error | S0 — data not saved, no workaround |
| Dashboard page loads blank after login | Console: `Uncaught TypeError: Cannot read properties of undefined (reading 'map')` | S0 — core feature completely broken |
| Image upload causes infinite spinner | Network tab: `POST /api/upload` → pending for 60+ seconds, then timeout | S1 — feature broken, user can retry |
| JavaScript bundle fails to load | Network tab: `GET /static/js/main.chunk.js` → 404 | S0 — entire app fails to render |

### False Positive Risk: None

Crash oracle findings are always real bugs. The only caveat is temporary server issues (deployment in progress, rate limiting), which should be noted but still reported.

---

## 2. Convention Oracle (~95% Reliability)

**Principle**: The application violates widely accepted user interface conventions and interaction patterns that virtually all modern web applications follow.

Convention bugs are almost always real because the patterns they check against are near-universal. The ~5% false positive rate comes from intentional design deviations (e.g., a wizard that deliberately omits a back button to enforce linear flow).

### What Counts as a Bug

- **Missing Feedback After Actions**: User clicks a button (save, submit, delete) and receives no visual confirmation -- no toast, no status change, no redirect. The user cannot tell if the action succeeded.
- **No Validation on Required Fields**: A form submits successfully with empty required fields, or validation occurs only on the server with no client-side indication of which fields are required.
- **Broken Navigation**: Links that lead to 404 pages, breadcrumbs that point to wrong locations, browser back button that produces unexpected results, navigation items that do nothing when clicked.
- **Missing Loading States**: Content areas that remain empty during data fetching with no spinner, skeleton loader, or "Loading..." text. The user sees a blank area and does not know if the page is broken or still loading.
- **Form Submission Without Feedback**: The form clears or resets without telling the user whether submission succeeded or failed. The user is left guessing.
- **Destructive Actions Without Confirmation**: Delete buttons that immediately remove data without a confirmation dialog or undo mechanism.
- **Broken Pagination**: Page numbers that skip, "Next" button that loops back to page 1, total count that does not match actual items, empty pages in the middle of results.
- **Non-Functional UI Elements**: Buttons that do not respond to clicks, dropdowns that do not open, toggles that do not change state, search inputs that do nothing.

### How to Detect

1. **Action-Observation Cycle**: Perform each user action slowly and deliberately. After every click, observe: Did the UI provide feedback? Did the state change as expected? Is the user informed about what happened?
2. **Form Testing**: Fill forms completely, then test with missing fields, invalid data, and edge cases (very long strings, special characters, empty submissions). Observe validation behavior at each step.
3. **Navigation Audit**: Click every link and navigation element. Verify it leads where the label says it should. Use the browser back button after each navigation and verify the previous page restores correctly.
4. **State Transition Checks**: After create/update/delete operations, verify that lists, counts, and related views reflect the change. Look for stale data or caches that do not invalidate.

### Examples

| Scenario | Evidence | Severity |
|----------|----------|----------|
| User submits contact form, page reloads with no success/error message | Visual: form clears, no toast or redirect. Network: POST returns 200 but UI shows nothing. | S2 — user cannot confirm submission worked |
| Delete button removes item instantly with no confirmation | Visual: item disappears immediately on click. No dialog, no undo toast. | S2 — accidental deletion possible |
| Required email field accepts form submission when empty | Visual: form submits. Network: POST returns 422 but UI shows no error state. | S2 — validation gap |
| Navigation link labeled "Settings" leads to 404 | Network: `GET /settings` → 404. Visual: generic "Page Not Found" page. | S1 — feature unreachable |

### False Positive Risk: ~5%

Some applications intentionally deviate from convention. If you suspect a design choice is intentional (e.g., a chatbot that has no traditional navigation), note it as MEDIUM confidence and flag the specific design decision for review rather than declaring it a definitive bug.

---

## 3. Permission Oracle (~90% Reliability)

**Principle**: The application exposes data, actions, or pages to users who should not have access. Authorization boundaries are violated.

Permission bugs are high reliability because authorization is binary -- a user either should or should not see something. The ~10% false positive rate comes from complex role systems where the tester may not fully understand the intended permission model.

### What Counts as a Bug

- **Unauthorized Resource Access**: A regular user can view admin-only pages by navigating directly to the URL. A logged-out user can access authenticated content.
- **Data Leaking Between Roles**: User A can see User B's private data (profile details, orders, documents) by manipulating URLs, IDs, or API parameters.
- **Missing Authentication Redirects**: Accessing a protected URL without being logged in shows a broken page or partial content instead of redirecting to login.
- **IDOR-Like Access Patterns**: Changing a numeric ID in the URL (e.g., `/users/123/profile` → `/users/124/profile`) reveals another user's data without authorization checks.
- **Horizontal Privilege Escalation**: A user with one role can perform actions reserved for a different role at the same privilege level (e.g., editing another team's project).
- **Vertical Privilege Escalation**: A regular user can access or perform admin-level actions (delete other users, change system settings, view admin dashboards).
- **Sensitive Data in Responses**: API responses contain fields that the current user should not see (other users' emails, internal IDs, admin flags) even if the UI does not display them.

### How to Detect

1. **URL Manipulation**: After logging in, copy URLs of authenticated pages. Log out (or open an incognito window) and paste those URLs. Observe whether the application redirects to login or shows content it should not.
2. **ID Enumeration**: When you see numeric or sequential IDs in URLs or API responses, try incrementing/decrementing them. If the application returns data for IDs you should not own, it is a permission bug.
3. **Role-Based Testing**: If provided multiple credentials with different roles, access the same features with each role. Document what each role can and cannot do. Verify that restricted features return proper 403 responses, not just hidden UI elements.
4. **Network Response Inspection**: Even when the UI hides elements, check the raw API responses in the Network tab. If the response JSON contains fields like `is_admin`, `email`, `ssn`, or other sensitive data that the current user should not see, report it.
5. **Direct API Calls**: If the application uses REST or GraphQL APIs, try calling endpoints directly (via the browser address bar or by replaying network requests) with modified parameters.

### Examples

| Scenario | Evidence | Severity |
|----------|----------|----------|
| Logged-out user accesses `/admin/dashboard` and sees the admin panel | Visual: admin page renders with data. Network: API calls return 200 with admin data. | S0 — complete auth bypass |
| Changing `/orders/1001` to `/orders/1002` shows another user's order | Network: `GET /api/orders/1002` returns 200 with another user's order details | S1 — data leak, IDOR vulnerability |
| Regular user can see "Admin Settings" page but cannot make changes | Visual: admin page renders. Network: GET returns 200, but POST returns 403. | S2 — information disclosure, partial auth |
| API response includes `password_hash` field even though UI doesn't show it | Network: `GET /api/users/me` response body contains `password_hash` field | S1 — sensitive data exposure |

### False Positive Risk: ~10%

Complex permission models may have non-obvious access rules. For example, a "viewer" role in a project management tool might legitimately see project details but not edit them. If you are unsure about the intended permission model, report with MEDIUM confidence and clearly state your assumption about what the access rules should be.

---

## 4. Visual Oracle (~80% Reliability)

**Principle**: The interface renders incorrectly, inconsistently, or in a way that degrades usability or professionalism.

Visual bugs are moderately reliable because they often depend on viewport size, browser, OS, font availability, and design intent. What looks like a bug may be an acceptable trade-off or an unsupported configuration.

### What Counts as a Bug

- **Broken Layouts**: Elements that should be in a grid or row are stacked randomly, columns that collapse when they should not, sidebars that overlap main content.
- **Text Truncation / Overflow**: Text that extends beyond its container, is cut off mid-word without an ellipsis, or overflows into adjacent elements. Long strings (names, emails, URLs) that break layouts.
- **Element Overlap**: UI components stacked on top of each other in a way that makes one or both unusable. Modals that appear behind other elements. Dropdowns that render underneath their trigger.
- **Images Not Loading**: Broken image icons, missing avatars, background images that fail to render. Alt text showing when the image should be visible.
- **Responsive Issues**: Layouts that break at specific viewport widths. Content that becomes unreachable on mobile. Touch targets too small for mobile use. Horizontal scrolling on mobile pages.
- **Z-Index Issues**: Tooltips or popovers that render behind modals. Sticky headers that cover dropdown menus. Overlays that do not block interaction with content beneath them.
- **Inconsistent Styling**: Buttons with different border-radius on the same page. Inconsistent font sizes for same-level headings. Color variations between identical components.
- **Missing Visual States**: Buttons with no hover or active state. Selected items with no visual distinction. Focused inputs with no visible focus ring.

### How to Detect

1. **Visual Scan**: After each page load, scan the entire viewport from top to bottom, left to right. Look for anything that seems misaligned, overlapping, truncated, or missing.
2. **Viewport Resizing**: Test at common breakpoints: 320px (small phone), 768px (tablet), 1024px (laptop), 1440px (desktop). Resize slowly between breakpoints and watch for layout breakage at intermediate widths.
3. **Content Stress Testing**: Enter very long strings in text fields and observe how the UI handles them. Upload images of different aspect ratios. Create items with missing optional fields and check how empty states render.
4. **Interaction State Checks**: Hover over every interactive element. Tab through the page and verify focus states. Click and hold buttons to check active states. Verify that selected/active states are visually distinct.
5. **Scroll Testing**: Scroll long pages and verify that sticky elements behave correctly, infinite scroll loads new content, and fixed-position elements do not cover interactive content.

### Examples

| Scenario | Evidence | Severity |
|----------|----------|----------|
| On mobile (375px), the main navigation overlaps the page content | Visual: nav menu covers first 200px of page content, making it unreadable and unclickable | S2 — content inaccessible on mobile |
| User avatar with a long name causes the header to break to two lines | Visual: header height doubles, pushing all content down. Layout shift on every page. | S3 — cosmetic but affects all pages |
| Modal dialog appears behind the dark overlay, making it unclickable | Visual: overlay visible but modal behind it. User cannot interact or dismiss. | S1 — user trapped, must refresh |
| Product images show broken image icon on listing page | Network: `GET /images/product-123.jpg` → 404. Visual: broken image icons throughout listing. | S2 — key content missing |

### False Positive Risk: ~20%

Visual issues are subjective. Extra spacing may be intentional breathing room. A specific truncation behavior may be by design. Report visual bugs with MEDIUM confidence unless they clearly break functionality (overlap that blocks interaction, missing images on a product page). Always describe what you observe factually rather than making assumptions about design intent.

---

## 5. Semantic Oracle (~60-70% Reliability)

**Principle**: The data, labels, or workflow logic feels incorrect based on domain knowledge and common sense, even though the application does not crash or visually break.

Semantic bugs are the lowest reliability because they require understanding the application's intended behavior, business rules, and domain context -- information that a black-box tester may not have.

### What Counts as a Bug

- **Incorrect Calculations**: A shopping cart subtotal that does not match the sum of individual item prices. A discount that applies incorrectly. A date range selector that allows end dates before start dates.
- **Labels That Contradict Content**: A section labeled "Recent Activity" that shows items from 2 years ago. A "Users Online" counter that shows a number higher than total registered users. A "Free Plan" card that lists a price.
- **Illogical Workflow Sequences**: An onboarding wizard that asks for payment before explaining what the product does. A settings page that lets you configure a feature before enabling it. A flow that requires step 3 before step 1 is complete.
- **Data Freshness Issues**: A dashboard showing "Last updated: 3 months ago" when it should be real-time. Cached data that persists after explicit refresh. Counts that do not update after adding/removing items.
- **Missing Business Logic**: A scheduling tool that allows booking overlapping appointments. An e-commerce site that allows ordering 0 or negative quantities. A form that accepts dates in the past for future-only fields.
- **Contradictory Information**: Two different parts of the UI showing different values for the same data point (e.g., profile page says "5 projects" but the sidebar says "3 projects").

### How to Detect

1. **Cross-Reference Data**: Compare numbers, counts, and values across different views of the same data. Does the dashboard count match the list count? Does the detail view match the summary?
2. **Logic Validation**: Perform calculations manually. If the UI shows a total, add up the components yourself. If the UI shows a percentage, calculate it from the raw numbers.
3. **Temporal Checks**: Look at timestamps and date ranges. Are "recent" items actually recent? Do chronological lists sort correctly? Are date constraints enforced (no future birthdays, no past scheduling)?
4. **Workflow Walk-Through**: Follow complete workflows from start to finish. Does each step logically follow the previous? Are there steps that seem out of order or redundant?
5. **Edge Case Reasoning**: Think about boundary values. What happens at 0, 1, the maximum, negative numbers? What happens with empty states?

### Examples

| Scenario | Evidence | Severity |
|----------|----------|----------|
| Shopping cart shows $50 subtotal but items sum to $45 | Visual: three items at $10, $15, $20 = $45, subtotal reads $50 | S1 — financial calculation error (if confirmed) |
| "Active Users" dashboard widget shows 150,000 on a new app with 12 accounts | Visual: widget displays 150,000. Context: app has very few users. | S2 — likely data error but needs confirmation |
| Appointment scheduler allows booking at 3:00 AM for a business open 9-5 | Visual: 3:00 AM slot available and bookable. No validation error. | S3 — missing business rule (if hours are indeed restricted) |
| Date picker for "delivery date" allows selecting yesterday | Visual: past dates are selectable. Form submits successfully with yesterday's date. | S2 — missing date constraint |

### False Positive Risk: ~30-40%

Semantic findings carry the highest false positive risk. What looks like incorrect data might reflect a different business rule you are unaware of. A counter showing an unexpected number might include deleted or archived items by design. An unusual workflow sequence might be intentional.

**Always report semantic findings with LOW confidence** unless you have explicit domain knowledge or documentation that confirms the expected behavior. Frame findings as questions: "The subtotal appears to be $5 higher than the sum of individual items -- is this an added fee or a calculation error?" This phrasing invites clarification rather than assuming a bug.

---

## Oracle Selection Strategy

When testing, apply oracles in order of reliability:

1. **Start with Crash**: Check the console and network tab first. These give you the highest-confidence findings.
2. **Move to Convention**: Interact with each feature and verify that standard patterns are followed.
3. **Test Permission**: If multiple roles are available, test access boundaries. Try URL manipulation.
4. **Scan Visual**: Inspect rendering at multiple viewport sizes and with edge-case content.
5. **Evaluate Semantic**: Only after the above, consider whether the data and logic make sense in context.

This order ensures you spend time on the most reliable, highest-impact findings first.
