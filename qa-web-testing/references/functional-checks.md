# Functional Testing Checks -- Complete Reference

> Comprehensive checklists for testing web application functionality: forms, navigation, CRUD operations, authentication, and search/filtering. Each check describes what to do, what to expect, and what constitutes a bug.

---

## 1. Form Testing

Forms are the primary input mechanism in web applications and the most common source of user-facing bugs. Test every form on every page.

### Required Field Validation

- [ ] **Submit the form with all fields empty.** Expected: every required field displays a validation error message. Bug: form submits successfully, or some required fields do not show errors, or a generic "something went wrong" appears instead of field-specific messages.

- [ ] **Submit the form with only one required field filled, leaving others empty.** Expected: validation errors appear on all remaining required fields but not on the filled one. Bug: the filled field also shows an error, or unfilled fields are not flagged.

- [ ] **Submit a field with only whitespace (spaces, tabs).** Expected: the field is treated as empty and validation fires. Bug: whitespace-only input is accepted as valid data.

- [ ] **Check that validation errors disappear when the field is corrected.** Expected: fixing a field's value and moving focus (or re-submitting) clears the error for that field. Bug: error messages persist even after the field is corrected, or all errors disappear when only one field is fixed.

- [ ] **Check that validation errors are associated with the correct field.** Expected: each error message appears next to or below the field it refers to. Bug: error messages appear in the wrong location, or a single generic error is shown without identifying which fields are invalid.

### Format Validation

- [ ] **Enter an invalid email format** (e.g., `user@`, `user@.com`, `@domain.com`, `user@domain`, `user name@domain.com`). Expected: validation rejects all invalid formats with a clear error message. Bug: invalid emails are accepted, or the error message is unclear.

- [ ] **Enter a valid but unusual email** (e.g., `user+tag@domain.com`, `user@sub.domain.co.uk`, `"user name"@domain.com`). Expected: these valid formats are accepted. Bug: overly strict validation rejects valid email addresses.

- [ ] **Enter invalid phone numbers** (letters mixed with digits, too few digits, too many digits, missing country code if required). Expected: validation rejects invalid formats. Bug: invalid phone numbers are accepted, or valid international formats are rejected.

- [ ] **Enter dates in wrong formats** (e.g., `13/25/2024`, `2024-13-01`, `00/00/0000`). Expected: invalid dates are rejected. Bug: impossible dates (month 13, day 32) are accepted.

- [ ] **Enter future dates where only past dates are valid** (e.g., date of birth set to next year). Expected: validation rejects future dates. Bug: future dates are accepted for fields that logically require past dates.

### Boundary Value Testing

- [ ] **Enter exactly 0 characters in a text field, then 1 character.** Expected: 0 characters triggers required validation (if required); 1 character is accepted. Bug: 1 character is rejected, or 0 characters does not trigger validation.

- [ ] **Enter exactly the maximum allowed length.** Expected: the input is accepted without truncation. Bug: the input is silently truncated, or an error occurs at the exact maximum.

- [ ] **Enter one character beyond the maximum allowed length.** Expected: the input is either blocked (character not accepted) or a clear validation error appears. Bug: the extra character is silently accepted and stored, or the input is truncated without warning.

- [ ] **Enter 0 in a numeric field.** Expected: accepted if zero is a valid value; rejected with a clear error if not. Bug: 0 causes a crash, is silently converted to null, or is accepted when it should not be.

- [ ] **Enter -1 in a numeric field that should only accept positive values** (quantity, price, age). Expected: validation rejects negative values. Bug: negative values are accepted and stored.

- [ ] **Enter extremely large numbers** (999999999, 2147483647, 9999999999999999). Expected: validation rejects values beyond the acceptable range, or the system handles them gracefully. Bug: integer overflow, database errors, display overflow (number extends beyond its container), or application crash.

- [ ] **Enter decimal values in an integer-only field** (1.5, 0.001, 3.14159). Expected: decimals are either rounded/truncated with indication, or rejected with an error. Bug: decimals are silently truncated (1.9 becomes 1), or cause a server error.

### Special Characters and Injection

- [ ] **Enter `<script>alert(1)</script>` in every text field.** Expected: the input is either rejected or stored and displayed with proper HTML escaping (visible as literal text, never executed). Bug: a JavaScript alert box appears, or the script tag is rendered as HTML.

- [ ] **Enter `' OR 1=1 --` in text fields.** Expected: the input is treated as a literal string. Bug: database error is shown, unexpected data is returned, or application behavior changes.

- [ ] **Enter `"; DROP TABLE users;--` in text fields.** Expected: the input is treated as a literal string. Bug: database error or unexpected application behavior.

- [ ] **Enter HTML entities and tags** (`<b>bold</b>`, `<img src=x onerror=alert(1)>`, `&amp;`, `&lt;`). Expected: rendered as plain text or safely sanitized. Bug: HTML is rendered, or broken HTML corrupts the page layout.

- [ ] **Enter special characters that affect URLs** (`&`, `=`, `?`, `#`, `%`, `/`). Expected: these are properly encoded when used in URLs or query parameters. Bug: URL breaks, parameters are misinterpreted, or page navigation fails.

- [ ] **Enter Unicode characters** (emojis, CJK characters, Arabic text, combining characters like `cafe\u0301`). Expected: characters are stored and displayed correctly. Bug: encoding errors, garbled text, or characters stripped silently.

### File Upload

- [ ] **Upload a file of the wrong type** (e.g., .exe when only images are allowed). Expected: a clear error message specifying allowed file types. Bug: the file is accepted, or a generic/confusing error appears.

- [ ] **Upload a file that exceeds the size limit.** Expected: a clear error message before the upload begins (if possible) or immediately after, stating the size limit. Bug: the upload runs to completion and then fails, or the error message does not state the allowed size.

- [ ] **Upload an empty file (0 bytes).** Expected: rejected with a clear error, or accepted if empty files are valid. Bug: application crashes, silent failure, or confusing error.

- [ ] **Upload multiple files when only one is expected.** Expected: only one file is accepted, with clear indication. Bug: multiple files are silently accepted, or the interface does not prevent multi-select.

- [ ] **Upload a file with a very long filename** (200+ characters). Expected: the filename is handled gracefully (truncated for display, stored correctly). Bug: filename breaks the layout, causes a server error, or is silently truncated in a way that loses the extension.

- [ ] **Upload a file with special characters in the filename** (spaces, parentheses, Unicode characters). Expected: the file is stored and downloadable with its original name or a sanitized version. Bug: the filename breaks the download, or special characters cause server errors.

### Double Submit Prevention

- [ ] **Click the submit button rapidly 2-3 times in quick succession.** Expected: only one record is created, and the button is disabled after the first click or subsequent clicks are ignored. Bug: multiple duplicate records are created.

- [ ] **Submit a form, then press the browser back button and submit again.** Expected: either the form is re-displayed with a warning about resubmission, or the duplicate is detected and prevented. Bug: a duplicate record is created silently.

- [ ] **Submit a form and immediately refresh the page (before redirect).** Expected: the browser warns about form resubmission, or the application handles it gracefully. Bug: a duplicate record is created.

### Autofill and Paste Behavior

- [ ] **Let the browser autofill the form (name, email, address, credit card).** Expected: autofilled values are recognized by the application, and validation does not reject them. Bug: autofilled fields are treated as empty, or validation fires incorrectly on autofilled values.

- [ ] **Paste text from a rich-text source (Word, Google Docs) into a plain text field.** Expected: only plain text is pasted, or rich formatting is stripped. Bug: HTML/RTF markup appears in the field, or formatting breaks the display.

- [ ] **Paste a value into a field with input restrictions** (numbers only, date picker, phone field). Expected: invalid characters from the pasted text are stripped or the paste is rejected. Bug: invalid characters are accepted, or the field breaks.

- [ ] **Use the browser's password manager to fill credentials.** Expected: the password field is filled correctly and login works. Bug: the password field does not accept autofill, or the filled value is not recognized.

### Form Reset and Cancel

- [ ] **Fill out the form completely, then click Cancel or Reset.** Expected: all fields are cleared and the user is returned to the previous page or a clean form. Bug: some fields retain their values, or the user is not navigated away.

- [ ] **Fill out a multi-step form, navigate to step 3, then click Back to step 1.** Expected: data from steps 1 and 2 is preserved when navigating back. Bug: previously entered data is lost when navigating between steps.

- [ ] **Fill out a multi-step form and close the browser tab.** Expected: either data is lost (acceptable with a beforeunload warning) or saved as a draft. Bug: no warning is shown and data is silently lost, or a draft is created but the user is not informed.

---

## 2. Navigation Testing

Navigation defines how users move through the application. Broken navigation creates confusion and blocks task completion.

### Link Verification

- [ ] **Click every visible link on the page.** Expected: each link navigates to a valid destination or performs the expected action. Bug: any link returns a 404, shows a blank page, or navigates to the wrong destination.

- [ ] **Check links in the footer, header, and sidebar.** Expected: all navigation links work consistently regardless of the current page. Bug: links that work from one page break from another, or footer/header links are outdated.

- [ ] **Right-click a link and open in a new tab.** Expected: the page loads correctly in the new tab. Bug: the page fails to load, shows an error, or requires the previous page's context to function.

- [ ] **Check that external links open in a new tab** (target="_blank"). Expected: clicking a link to an external site opens a new tab. Bug: the user is navigated away from the application without a way to return.

- [ ] **Check external links for rel="noopener noreferrer".** Expected: external links include this attribute for security. Bug: external links can access the opener window via `window.opener`.

### Back Button and Browser History

- [ ] **Navigate through 3-4 pages, then press the back button repeatedly.** Expected: each back press returns to the previous page in the correct order. Bug: back button skips pages, returns to the wrong page, or causes an error.

- [ ] **Fill in a form partially, navigate away, then press back.** Expected: form data is preserved (ideal) or the form is clearly reset. Bug: some fields retain data and others are cleared inconsistently.

- [ ] **Apply filters or sort options on a list, then press back and forward.** Expected: filters and sort state are preserved in the browser history. Bug: filters are lost, and the user sees the unfiltered list.

- [ ] **Scroll down a long page, navigate away, press back.** Expected: scroll position is restored to where the user was. Bug: the page scrolls to the top, losing the user's position.

- [ ] **Open a modal or overlay, then press the back button.** Expected: the modal closes (back button closes the overlay). Bug: pressing back navigates away from the page entirely, leaving the modal context.

### Deep Links and Bookmarks

- [ ] **Copy the URL of a page with specific state** (filtered list, selected tab, open modal, pagination page 3). Expected: opening that URL in a new browser reproduces the exact state. Bug: the URL does not encode the state, and the user sees the default view.

- [ ] **Bookmark a page and open the bookmark later.** Expected: the page loads correctly. Bug: the bookmark leads to an error, a redirect loop, or requires re-authentication without redirect back.

- [ ] **Share a URL with another user who is logged in.** Expected: the second user sees the same page (if they have permission) or a clear "access denied" message. Bug: a generic error, a blank page, or a crash.

### Breadcrumbs

- [ ] **Navigate 3-4 levels deep and check the breadcrumb trail.** Expected: breadcrumbs accurately reflect the navigation path from root to current page. Bug: breadcrumbs show the wrong hierarchy, skip levels, or do not match the actual path taken.

- [ ] **Click each breadcrumb link.** Expected: each link navigates to the correct parent page. Bug: breadcrumb links are broken or navigate to the wrong page.

- [ ] **Check breadcrumbs on a page reached via search or direct link.** Expected: breadcrumbs show the logical hierarchy even if the user did not navigate through it. Bug: breadcrumbs are empty or show an incorrect path.

### Error Pages

- [ ] **Enter a URL that does not exist** (e.g., `/this-page-does-not-exist`). Expected: a custom 404 page with helpful navigation (link to home, search). Bug: browser default error page, a stack trace, or a blank page.

- [ ] **Access a URL for a deleted resource** (e.g., `/projects/deleted-project-id`). Expected: a 404 or a message indicating the resource was deleted. Bug: a crash, a server error, or a blank page.

- [ ] **Access a URL you do not have permission to view.** Expected: a 403 page or redirect to an appropriate page. Bug: a 500 error, a blank page, or partial rendering of the restricted content.

### Redirect Behavior

- [ ] **Access a protected page while not logged in.** Expected: redirect to login, and after login, redirect back to the originally requested page. Bug: login redirects to the home page instead of the intended destination.

- [ ] **Log in with a deep link URL as the referrer.** Expected: after login, the user lands on the deep link destination. Bug: the user always lands on the dashboard regardless of the original URL.

- [ ] **Follow a redirect chain manually** (check the network tab). Expected: no more than 2-3 redirects in sequence. Bug: redirect loops, or chains exceeding 5 redirects.

---

## 3. CRUD Operations

Create, Read, Update, and Delete operations form the backbone of data-driven applications. Test each operation with valid, invalid, and edge-case data.

### Create

- [ ] **Create an entity with only required fields filled.** Expected: the entity is saved successfully, and optional fields are null/empty. Bug: the create fails, or optional fields cause validation errors.

- [ ] **Create an entity with all fields filled (required and optional).** Expected: all values are saved and retrievable. Bug: some optional field values are lost or ignored.

- [ ] **Create an entity with invalid data in each field, one at a time.** Expected: validation catches each invalid field with a specific error message. Bug: invalid data is accepted, or the error message is generic.

- [ ] **Create an entity and immediately verify it appears in the list view.** Expected: the new entity is visible in the list without requiring a page refresh. Bug: the list does not update until manual refresh, or the entity appears at the wrong position.

- [ ] **Create an entity with boundary values** (shortest valid name, longest valid name, minimum value, maximum value). Expected: boundary values are accepted and stored accurately. Bug: boundary values are rejected or stored incorrectly (truncated, rounded).

### Read / Detail View

- [ ] **Open the detail view of a recently created entity.** Expected: every field displays the exact data that was entered during creation. Bug: any field shows different data, is missing, or is formatted incorrectly.

- [ ] **Check that read-only fields are not editable.** Expected: fields meant for display only cannot be modified. Bug: clicking a read-only field opens an edit state.

- [ ] **Check data formatting in the detail view** (dates, numbers, currencies, phone numbers). Expected: data is formatted according to the application's conventions and locale. Bug: raw database values displayed (ISO dates, unformatted numbers).

- [ ] **Verify related data is displayed correctly** (e.g., project shows its tasks, user shows their orders). Expected: related entities are listed accurately. Bug: related data is missing, shows wrong associations, or is duplicated.

### Update

- [ ] **Edit one field and save.** Expected: the edited field is updated, and all other fields remain unchanged. Bug: other fields are cleared, reset to defaults, or overwritten.

- [ ] **Edit a field to an invalid value and save.** Expected: validation prevents the save with a clear error message. Bug: invalid value is saved, or the error message is unclear.

- [ ] **Edit an entity that another user is also editing** (concurrent edit). Expected: either optimistic locking prevents overwrite with a conflict message, or the last save wins with no data corruption. Bug: data is silently overwritten, or a crash occurs.

- [ ] **Edit an entity and cancel.** Expected: no changes are saved, and the entity retains its original values. Bug: changes are partially saved even after cancel.

- [ ] **Edit an entity, navigate away without saving, then return.** Expected: either unsaved changes are preserved (draft behavior) or a warning about unsaved changes is shown before navigation. Bug: changes are silently lost without warning.

### Delete

- [ ] **Delete an entity.** Expected: a confirmation dialog appears before deletion, stating what will be deleted. Bug: the entity is deleted immediately without confirmation.

- [ ] **Cancel a delete confirmation.** Expected: the entity is not deleted and remains in its original state. Bug: the entity is deleted despite canceling.

- [ ] **Delete an entity that has related data** (e.g., delete a category that contains products). Expected: either the delete is prevented with an explanation, related data is also deleted (cascade) with a warning, or related data is reassigned. Bug: orphaned records, broken references, or silent data corruption.

- [ ] **Delete an entity and verify it is removed from all views** (list, search results, filters, related entity displays). Expected: the entity no longer appears anywhere. Bug: the deleted entity still appears in some views until a page refresh.

- [ ] **Attempt to access the URL of a deleted entity directly.** Expected: a 404 page or a "this item has been deleted" message. Bug: a crash, a blank page, or partial rendering.

### Bulk Operations

- [ ] **Select all items and perform a bulk action** (delete, export, status change). Expected: the action applies to all selected items with a confirmation showing the count. Bug: not all items are affected, or no confirmation is shown.

- [ ] **Select items across multiple pages (if applicable) and perform a bulk action.** Expected: items from all pages are included in the action. Bug: only items from the current page are affected.

- [ ] **Perform a bulk delete on a large number of items (50+).** Expected: the operation completes (possibly with a progress indicator) and all items are deleted. Bug: timeout, partial deletion, or UI freeze.

### Duplicate Detection

- [ ] **Create an entity with the exact same data as an existing entity.** Expected: the system either prevents the duplicate (error message) or creates it with a unique identifier. Bug: silent creation of an exact duplicate with no distinction, or a crash.

- [ ] **Create an entity with data that differs only in case** (e.g., "John" vs "john"). Expected: depends on business rules -- either treated as duplicate or distinct. Bug: inconsistent behavior (sometimes duplicate, sometimes not).

---

## 4. Authentication and Authorization

Authentication and authorization bugs can have severe security implications. Test these scenarios carefully.

### Login

- [ ] **Log in with valid credentials.** Expected: successful login redirecting to the dashboard or intended page. Bug: login fails with valid credentials, or redirects to the wrong page.

- [ ] **Log in with a valid email but incorrect password.** Expected: a generic error message like "Invalid email or password" (not "Incorrect password" which reveals the email exists). Bug: the error message reveals whether the email exists in the system.

- [ ] **Log in with a non-existent email.** Expected: the same generic error message as an incorrect password. Bug: a different error message that reveals the email is not registered.

- [ ] **Log in with an empty email and/or password.** Expected: validation prevents submission. Bug: an API call is made with empty credentials.

- [ ] **Attempt login with SQL injection strings** (`' OR 1=1 --`, `admin'--`). Expected: login fails with the generic error. Bug: login succeeds, or a database error is displayed.

### Logout

- [ ] **Log out and verify the session is terminated.** Expected: the user is redirected to the login page, and auth tokens/cookies are cleared. Bug: the session cookie or token persists after logout.

- [ ] **Log out and press the browser back button.** Expected: pressing back does not show authenticated content; the user is redirected to login or sees a non-sensitive page. Bug: cached authenticated pages are visible after logout.

- [ ] **Log out and try to access an API endpoint directly** (using browser dev tools or curl with the old token). Expected: the API returns 401 Unauthorized. Bug: the old token still works after logout.

### Password Reset

- [ ] **Request a password reset for a valid email.** Expected: a success message appears regardless of whether the email exists (to prevent email enumeration), and a reset email is sent. Bug: different messages for existing vs non-existing emails.

- [ ] **Click the password reset link in the email.** Expected: the link opens a page to set a new password. Bug: the link is expired immediately, broken, or leads to an error.

- [ ] **Use the password reset link twice.** Expected: the second use is rejected (link is single-use). Bug: the link can be reused multiple times.

- [ ] **Set a new password and log in with it.** Expected: login succeeds with the new password, and the old password no longer works. Bug: the old password still works, or the new password does not work.

### Session Management

- [ ] **Stay idle past the configured session timeout.** Expected: the next action triggers a re-authentication prompt, and the user's work is not lost. Bug: the user is silently redirected to login and loses unsaved work.

- [ ] **Log in from two different browsers simultaneously.** Expected: both sessions work (if concurrent sessions are allowed), or the older session is invalidated with a notification. Bug: one session silently stops working, data corruption between sessions, or no enforcement of concurrent session limits.

- [ ] **Modify the session token/cookie value manually.** Expected: the modified token is rejected, and the user is logged out. Bug: a modified token grants access (session fixation vulnerability).

### Role-Based Access Control

- [ ] **Access an admin URL while logged in as a regular user.** Expected: a 403 Forbidden response or redirect to an appropriate page. Bug: the admin page loads, the admin action succeeds, or a 500 error occurs.

- [ ] **Check that UI elements are hidden for unauthorized roles** (admin buttons not visible to regular users). Expected: role-restricted UI elements are not rendered in the DOM. Bug: elements are hidden via CSS but present in the DOM (can be revealed via dev tools), or restricted elements are visible.

- [ ] **Attempt a restricted API call directly** (e.g., POST to an admin endpoint using dev tools). Expected: the API returns 403 Forbidden. Bug: the API executes the action regardless of role.

- [ ] **Check role boundaries after a role change** (user is demoted from admin to regular user). Expected: the user immediately loses admin access. Bug: admin access persists until logout or session expiry.

### CSRF Protection

- [ ] **Check that state-changing requests include a CSRF token** (POST, PUT, DELETE). Expected: requests include a CSRF token in headers or body. Bug: state-changing requests have no CSRF protection.

- [ ] **Replay a state-changing request from a different origin** (using curl or a different site). Expected: the request is rejected. Bug: the request succeeds from a different origin.

---

## 5. Search and Filtering

Search and filtering are high-traffic features that often break under edge conditions.

### Search

- [ ] **Search for a term that returns no results.** Expected: a clear empty state with a message like "No results found for [query]" and suggestions (check spelling, try different terms). Bug: a blank page, a loading spinner that never resolves, or no indication that the search returned nothing.

- [ ] **Search for a term that matches exactly one result.** Expected: the single result is displayed. Bug: the results page looks broken with a single item (layout issues).

- [ ] **Search with special characters** (`<`, `>`, `&`, `"`, `'`, `%`, `\`). Expected: special characters are handled safely. Bug: search crashes, returns a server error, or the characters are interpreted as operators.

- [ ] **Search with a very long query** (500+ characters). Expected: the search either works or shows a "query too long" error. Bug: the application crashes, the URL breaks (if query is in URL parameters), or performance degrades significantly.

- [ ] **Search and verify result relevance.** Expected: the most relevant results appear first. Bug: irrelevant results ranked above exact matches.

- [ ] **Search for a recently created item.** Expected: the item appears in search results. Bug: newly created items are not indexed and do not appear in search (stale index).

### Real-Time Search

- [ ] **Type a search query slowly, one character at a time.** Expected: results update after a brief debounce delay (200-500ms), not on every keystroke. Bug: API call fires on every keystroke (performance issue), or no debounce causes UI flickering.

- [ ] **Type a query, then quickly delete it and type a different one.** Expected: only the results for the final query are displayed. Bug: results from the first query appear briefly before being replaced (race condition), or stale results persist.

- [ ] **Type a query and press Enter while results are loading.** Expected: the submitted query takes precedence. Bug: the Enter press is ignored, or conflicting results appear.

### Filtering

- [ ] **Apply a single filter and verify the results match.** Expected: only items matching the filter criteria are shown, and the active filter is visually indicated. Bug: unmatched items appear, or the filter indicator is missing.

- [ ] **Apply multiple filters simultaneously.** Expected: filters combine correctly (typically AND logic), and all active filters are displayed. Bug: filters conflict, only one filter is applied, or the combination produces incorrect results.

- [ ] **Clear all filters.** Expected: the full unfiltered list returns, and all filter indicators are removed. Bug: some filters persist after clearing, or the "clear all" button does not work.

- [ ] **Apply a filter that matches no items.** Expected: an empty state with a message indicating no items match the filters. Bug: blank page, loading spinner, or confusing message.

### Pagination with Filters

- [ ] **Apply a filter and navigate to page 2+.** Expected: the filter persists across all pages. Bug: filters are lost when paginating.

- [ ] **Apply a filter that reduces results to fewer than one page.** Expected: pagination controls disappear or adjust. Bug: pagination still shows multiple pages for a filtered result that fits on one page.

- [ ] **Change the page size (items per page) with active filters.** Expected: the filter persists, and the page is reset to page 1. Bug: filters are cleared, or the user stays on a page number that no longer exists.

### Sorting

- [ ] **Sort by each available column.** Expected: items are ordered correctly (ascending/descending toggle). Bug: sort does not work for a specific column, or sort direction is wrong.

- [ ] **Sort a column that contains mixed data types** (numbers stored as strings, null values). Expected: consistent sorting behavior (nulls first or last, numbers sorted numerically). Bug: lexicographic sort on numbers (1, 10, 2, 20 instead of 1, 2, 10, 20), or nulls cause crashes.

- [ ] **Apply a sort and a filter simultaneously.** Expected: the filtered results are sorted correctly. Bug: sorting resets the filter, or the filter is applied to pre-sorted data incorrectly.

- [ ] **Sort, then paginate.** Expected: sorting is applied across the entire dataset, not just the current page. Bug: sort only affects the items on the current page.

### Search Result Display

- [ ] **Check that search results highlight the matching text.** Expected: the search query is highlighted in each result. Bug: no highlighting, or highlighting appears in the wrong part of the result.

- [ ] **Check that search results include enough context to distinguish similar items.** Expected: each result shows enough metadata (date, type, parent entity) to differentiate it. Bug: multiple identical-looking results with no way to distinguish them.
