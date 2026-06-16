# Technical Testing Checks -- Complete Reference

> Comprehensive checklists for monitoring console errors, network requests, performance metrics, and browser state during web application testing. Each check describes what to monitor, how to interpret it, and what constitutes a reportable bug.

---

## 1. Console Error Monitoring

Open the browser's developer tools (F12 or Cmd+Option+I) and keep the Console tab visible during all testing. Every console error is a potential bug until triaged.

### JavaScript Exceptions

These are almost always real bugs. Report them with the full stack trace, the action that triggered them, and the URL.

- [ ] **TypeError: Cannot read properties of undefined/null.** What it means: code is accessing a property on an object that does not exist. Cause: missing null checks, data loaded in unexpected shape, race condition between rendering and data fetch. Severity: High -- usually causes a broken UI element or crash. What to report: the full error message, the stack trace (which file and line), what action triggered it, and what the user sees.

- [ ] **ReferenceError: x is not defined.** What it means: code references a variable or function that was never declared. Cause: missing import, typo in variable name, code runs before script is loaded. Severity: High -- the dependent feature is broken. What to report: the undefined variable name and what feature stops working.

- [ ] **SyntaxError in loaded scripts.** What it means: a JavaScript file contains invalid syntax. Cause: build error, corrupted deployment, or incomplete file upload. Severity: Critical -- may break entire application sections. What to report: the affected script URL and any features that fail.

- [ ] **RangeError: Maximum call stack size exceeded.** What it means: infinite recursion. Cause: a function calls itself endlessly, often due to circular references or unguarded recursive logic. Severity: Critical -- causes the browser tab to freeze. What to report: what action causes the freeze and the stack trace.

- [ ] **Unhandled Promise Rejection.** What it means: an async operation failed and no `.catch()` or try/catch handled the error. Cause: API call failed without error handling, or an unexpected rejection occurred. Severity: High -- indicates missing error handling. What to report: the rejection reason and what async action triggered it.

### Framework-Specific Errors

#### React

- [ ] **"Each child in a list should have a unique key prop."** What it means: a list is rendering items without unique identifiers. Impact: React cannot efficiently re-render the list and may produce incorrect UI on updates. Severity: Medium -- causes subtle rendering bugs and performance issues. Is it a bug? Yes -- it can cause items to swap positions, lose state, or fail to update.

- [ ] **"Can't perform a React state update on an unmounted component."** What it means: an async operation (API call, timer) completes and tries to update a component that no longer exists. Impact: memory leak. Severity: Medium -- memory leak that grows over time. Is it a bug? Yes -- the async operation needs cleanup on unmount.

- [ ] **"Invalid hook call" or "Hooks can only be called inside the body of a function component."** What it means: React hooks are used incorrectly. Severity: Critical -- the component will not render at all.

- [ ] **Hydration mismatch warnings (SSR apps).** What it means: server-rendered HTML does not match what the client renders. Impact: UI flickering, content flash, or incorrect initial state. Severity: Medium to High depending on visibility.

#### Vue

- [ ] **"Property or method is not defined on the instance."** What it means: template references a variable not declared in data, computed, or methods. Severity: High -- the template element will not render correctly.

- [ ] **Reactivity warnings** ("Vue warn: Avoid adding reactive properties to a plain object"). Impact: data changes may not trigger re-renders. Severity: Medium.

#### Angular

- [ ] **"ExpressionChangedAfterItHasBeenCheckedError."** What it means: a binding value changed after Angular's change detection ran. Impact: UI shows stale data until the next detection cycle. Severity: Medium -- inconsistent UI state.

### Resource Load Failures

- [ ] **404 errors for images, fonts, CSS, or JS files.** How to spot: console shows "Failed to load resource: net::ERR_FILE_NOT_FOUND" or a 404 status for asset URLs. Severity: High for JS/CSS (breaks functionality or styling), Medium for images/fonts (visual degradation). What to report: the asset URL, what visual or functional element is broken.

- [ ] **Mixed content warnings** ("Mixed Content: The page was loaded over HTTPS but requested an insecure resource"). What it means: HTTPS page is loading HTTP resources. Impact: browsers may block the resource; security vulnerability. Severity: High -- security issue. What to report: the insecure resource URL.

- [ ] **CORS errors** ("Access to fetch has been blocked by CORS policy"). What it means: an API call is blocked because the server does not allow requests from this origin. Impact: the dependent feature completely breaks. Severity: Critical -- feature is non-functional. What to report: the blocked URL, the requesting origin, and the feature that fails.

- [ ] **CSP (Content Security Policy) violations.** How to spot: console shows "Refused to execute inline script" or "Refused to load the script" with a CSP directive reference. Impact: scripts or styles are blocked. Severity: varies -- could block critical functionality.

### Distinguishing Real Bugs from Development Noise

Not every console message is a bug. Learn to distinguish:

| Message Type | Is It a Bug? | How to Tell |
|-------------|-------------|-------------|
| React StrictMode double-renders | No | Only appears in development; message includes "StrictMode" |
| Hot Module Replacement (HMR) messages | No | Messages reference "hot update", "HMR", or "[vite]" |
| Vue devtools connection messages | No | Messages reference "vue-devtools" |
| Webpack compilation warnings | No | Only in development; reference "webpack" or module paths |
| Source map warnings | No | Messages about ".map" files failing to load |
| "DevTools failed to load source map" | No | Browser tooling issue, not application bug |
| Browser extension errors | No | Stack trace points to extension code, not application code |
| Third-party script errors (analytics, chat widgets) | Maybe | Only report if they visibly break the application |

**Rule of thumb:** If the error originates from the application's own code (check the stack trace file paths) and is triggered by a user action, it is a bug. If it originates from browser internals, extensions, or development tooling, it is not.

---

## 2. Network Request Monitoring

Open the browser's Network tab during all testing. Monitor API calls for errors, unexpected responses, and performance issues.

### HTTP Error Responses

#### Client Errors (4xx)

- [ ] **400 Bad Request.** What it means: the server rejected the request because the client sent invalid data. When it is a bug: if the frontend allowed the user to submit invalid data that should have been caught by client-side validation. When it is not a bug: if the server has stricter validation than the frontend by design. What to report: the request payload, the response body (often contains validation details), and the user action that triggered it.

- [ ] **401 Unauthorized.** What it means: the request lacks valid authentication. When it is a bug: if the user is logged in and should be authenticated. This usually means the auth token expired silently or was not sent with the request. When it is not a bug: expected after session timeout. What to report: was the user logged in? Did the UI handle this gracefully (redirect to login) or fail silently?

- [ ] **403 Forbidden.** What it means: the user is authenticated but not authorized for this action. When it is a bug: if the user should have permission (role-based access error), or if the UI shows a button/link for an action the user cannot perform. When it is not a bug: expected when testing role restrictions. What to report: the user's role, the attempted action, and whether the UI indicated the action was available.

- [ ] **404 Not Found.** What it means: the requested resource does not exist. When it is a bug: if the resource should exist (the frontend is requesting a wrong URL, or a slug/ID is incorrect). When it is not a bug: expected for deleted resources. What to report: the requested URL and what the UI was trying to display.

- [ ] **409 Conflict.** What it means: the request conflicts with the current state (duplicate, concurrent edit). When it is a bug: if the frontend does not handle this response and show a user-friendly message. What to report: the user action that triggered it and what the UI displayed.

- [ ] **422 Unprocessable Entity.** What it means: the server understood the request but the data is semantically invalid. When it is a bug: when frontend validation should have caught this before the request was made. What to report: what validation was missing on the frontend.

- [ ] **429 Too Many Requests.** What it means: rate limit exceeded. When it is a bug: if triggered by normal user behavior (not automation). Investigate whether the frontend is making excessive API calls. What to report: how many requests were sent in what time period, and what user action triggered them.

#### Server Errors (5xx)

- [ ] **500 Internal Server Error.** What it means: the server crashed while processing the request. This is always a bug. What to report: the request URL, method, payload, and the user action that triggered it. Include the response body if it contains an error message or stack trace.

- [ ] **502 Bad Gateway.** What it means: the server acting as a gateway received an invalid response from the upstream server. Usually an infrastructure issue. What to report: the request URL and whether it is reproducible.

- [ ] **503 Service Unavailable.** What it means: the server is temporarily unable to handle the request (overloaded or down for maintenance). What to report: whether the UI shows a maintenance message or fails silently.

### Performance Monitoring

- [ ] **Slow API responses (over 3 seconds).** How to identify: sort the Network tab by time, or look for requests with long duration. What to report: the endpoint URL, response time, and any correlation (slow only with large datasets, slow only at certain times).

- [ ] **Slow page loads (over 5 seconds).** How to identify: check the total page load time in the Network tab or Performance tab. What to report: the page URL, total load time, and which resources are slowest.

- [ ] **Excessive API calls (same endpoint called many times).** How to identify: filter the Network tab by URL and look for the same endpoint called 10, 50, or 100+ times on a single page load. This is a strong signal of an N+1 query problem or a re-rendering loop. What to report: the endpoint URL, the number of calls, and the page where this happens.

- [ ] **Large payloads (over 1MB response).** How to identify: sort the Network tab by size. What to report: the endpoint URL, response size, and whether the data could be paginated or compressed.

- [ ] **Unnecessary requests on navigation.** How to identify: navigate between pages and watch for requests that fire on every navigation even when the data has not changed. What to report: the endpoint URL and the navigation pattern that triggers redundant calls.

### Error Handling in the UI

- [ ] **Trigger an API error and observe what the UI shows.** Expected: a user-friendly error message (not a stack trace, not a raw JSON error). Bug: no visible feedback, a generic "something went wrong" without detail, or raw technical error data displayed to the user.

- [ ] **Disconnect from the network and attempt an action.** Expected: the UI shows an offline indicator or a clear network error message. Bug: the action appears to succeed but silently fails, or a cryptic error appears.

- [ ] **Check retry behavior after API failure.** Expected: the app either retries automatically with backoff or provides a "Retry" button. Bug: no retry mechanism, infinite retry loop, or retry without backoff (hammering the server).

- [ ] **Check loading states during slow requests.** Expected: a loading indicator (spinner, skeleton, progress bar) appears during requests. Bug: the UI appears frozen, or no indication that something is loading.

---

## 3. Performance Metrics

Use the browser's Performance tab and Lighthouse to measure these Core Web Vitals.

### Largest Contentful Paint (LCP)

LCP measures how long it takes for the largest visible content element (image, video, text block) to render.

| LCP Time | Rating |
|----------|--------|
| Under 2.5 seconds | Good |
| 2.5 - 4.0 seconds | Needs improvement |
| Over 4.0 seconds | Poor -- report as a bug |

- [ ] **Measure LCP on initial page load** (hard refresh with empty cache). What to report if poor: the LCP element (is it a large image? a text block waiting for fonts?), the network waterfall (what is blocking rendering?).

- [ ] **Measure LCP on subsequent navigation** (soft navigation within the app). Expected: faster than initial load due to cached resources.

### Cumulative Layout Shift (CLS)

CLS measures visual stability -- how much the layout shifts as the page loads.

| CLS Score | Rating |
|-----------|--------|
| Under 0.1 | Good |
| 0.1 - 0.25 | Needs improvement |
| Over 0.25 | Poor -- report as a bug |

- [ ] **Watch for layout shifts during page load.** What to look for: elements jumping position as images load, fonts swap, or ads/banners inject into the page. What to report: which element shifted, what caused the shift (missing image dimensions, late-loading content, dynamic injection).

- [ ] **Watch for layout shifts during interaction.** What to look for: clicking a button causes distant content to jump, or an error message pushes content down. What to report: the action that triggered the shift and the elements that moved.

### Interaction to Next Paint (INP)

INP measures responsiveness -- how long it takes for the page to visually respond to user input.

| INP Time | Rating |
|----------|--------|
| Under 200ms | Good |
| 200 - 500ms | Needs improvement |
| Over 500ms | Poor -- report as a bug |

- [ ] **Click buttons, links, and interactive elements and note any delay before visual feedback.** What to report: the element clicked, the perceived delay, and whether any visual feedback (button state change, loading spinner) appeared during the delay.

- [ ] **Type in search fields and note any lag between keystrokes and visible changes.** Expected: less than 100ms delay per keystroke. Bug: noticeable lag, dropped characters, or frozen input.

### Memory Leaks

- [ ] **Navigate between pages repeatedly (10-20 times) and check memory usage in the Performance Monitor.** Expected: memory usage remains stable after initial loading. Bug: memory grows continuously with each navigation, never returning to baseline.

- [ ] **Open and close modals repeatedly (10-20 times).** Expected: memory usage remains stable. Bug: each open/close cycle increases memory, indicating event listeners or DOM nodes are not being cleaned up.

- [ ] **Run the application for an extended period (10+ minutes of active use).** Expected: memory usage remains within a stable range. Bug: steadily increasing memory that eventually causes the tab to slow down or crash.

### Large List Performance

- [ ] **Load a page with 100+ items in a list or table.** Expected: the list renders smoothly, scrolling is fluid. Bug: noticeable jank during scroll, delayed rendering, or the page freezes during initial load.

- [ ] **Load a page with 1000+ items if possible.** Expected: virtual scrolling is used (only visible items are rendered in the DOM). Bug: all 1000+ items are in the DOM simultaneously, causing slow rendering and scroll jank.

- [ ] **Sort or filter a large list.** Expected: results update within 1 second. Bug: UI freezes during sort/filter, or results take multiple seconds to appear.

### Image and Asset Optimization

- [ ] **Check image formats in the Network tab.** Expected: modern formats (WebP, AVIF) with fallbacks. Bug: large PNG/JPEG images that could be smaller in modern formats.

- [ ] **Check image dimensions vs display size.** Expected: images are served at or near their display dimensions (not a 4000px image displayed at 200px). Bug: images significantly larger than their display size, wasting bandwidth.

- [ ] **Check for lazy loading of below-the-fold images.** Expected: images not visible on initial viewport load lazily as the user scrolls. Bug: all images load immediately, slowing initial page load.

---

## 4. Browser State

### localStorage and sessionStorage

- [ ] **Check what the application stores in localStorage.** Expected: user preferences, UI state, non-sensitive cached data. Bug: sensitive data (passwords, tokens, PII) stored in localStorage (which has no expiration and is accessible to any script on the domain).

- [ ] **Clear localStorage and reload the application.** Expected: the application works correctly, regenerating any needed stored data. Bug: the application crashes or enters a broken state when localStorage is empty.

- [ ] **Fill localStorage to its limit (~5MB) and test the application.** Expected: the application handles the storage quota exceeded error gracefully. Bug: crash or silent failure when storage is full.

### Cookies

- [ ] **Check authentication cookies for security flags.** Expected: `Secure` flag (cookie only sent over HTTPS), `HttpOnly` flag (cookie not accessible via JavaScript), `SameSite` attribute set. Bug: missing security flags on auth cookies.

- [ ] **Check cookie expiration.** Expected: session cookies expire when the browser closes; persistent cookies have a reasonable expiration. Bug: auth cookies that never expire, or cookies with excessive lifetimes.

- [ ] **Delete all cookies and reload.** Expected: the user is logged out and redirected to the login page. Bug: the application crashes or shows a broken state instead of the login page.

### Cache Behavior

- [ ] **Deploy a new version and check if stale content is served.** Expected: updated content is visible after a normal page refresh (not hard refresh). Bug: old JavaScript, CSS, or content persists despite a new deployment (cache busting failure).

- [ ] **Check Cache-Control headers on API responses.** Expected: dynamic data has `no-cache` or short max-age; static assets have long max-age with content hashing in filenames. Bug: dynamic data cached too aggressively (stale data shown), or static assets not cached (slow loads).

### History API

- [ ] **Navigate within the SPA and check the URL bar.** Expected: the URL updates to reflect the current page/state. Bug: URL does not change during navigation (single URL for the entire app), or URL changes but does not reflect the actual page.

- [ ] **Copy the URL mid-navigation and open it in a new tab.** Expected: the same page/state loads. Bug: the URL is not a valid deep link.

- [ ] **Use the browser's back and forward buttons after SPA navigation.** Expected: back/forward work correctly, matching the navigation history. Bug: back/forward skip pages, loop, or navigate outside the application.
