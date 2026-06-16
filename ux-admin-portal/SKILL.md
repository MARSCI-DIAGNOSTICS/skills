---
name: ux-admin-portal
description: Use this skill whenever the user mentions admin portal, admin panel, back office, CMS, content management, user management, CRUD interface, data tables, bulk actions, role-based access, RBAC, filters, search, pagination, or any interface for managing data, users, or content. Also use when building or reviewing any internal tool, management dashboard, or data-heavy interface with tables — even if the user doesn't say "admin". If it has a data table with sorting and filtering, this skill applies.
---

# Admin Portal UX Design

This skill provides a complete framework for designing, evaluating, and optimizing admin portal interfaces. It covers data tables, CRUD patterns, bulk operations, search and filtering, role-based access control, audit logs, user management, and content management workflows.

Apply these principles to any administrative interface whose primary purpose is managing data, users, content, or system configuration -- including internal tools, CMS platforms, CRM systems, e-commerce back offices, and enterprise management dashboards.

---

## Data Table Essentials

Data tables are the backbone of admin portals. Build every table on these foundations:

### Alignment and Readability

- Left-align text columns. Right-align numeric columns. Match header alignment to column data type.
- Use subtle zebra striping (5-10% gray alternating rows) or row dividers to aid horizontal scanning.
- Set cell padding to minimum 8-12px horizontal and 8-16px vertical at comfortable density.
- Use monospaced fonts for numeric and code columns.

### Sorting

- Make every column header clickable for sorting. Display ascending/descending indicators (arrow or chevron) on the active sort column.
- Default sort to the most common use case (typically newest first or alphabetical by name).
- Persist sort state across pagination and navigation.

### Pagination

- Use pagination for admin tables (not infinite scroll) -- users need to reference specific pages and jump to ranges.
- Show items-per-page control with options: 10, 25, 50, 100.
- Display total record count and current range: "Showing 1-25 of 1,204."

### Row Density

- Offer three density options for power users: compact (32px row height, 4-8px padding), comfortable (40px, 8-16px padding), and spacious (48px, 12-24px padding).
- Default to comfortable density. Persist the density preference per user.

### Responsive Behavior

- On desktop, display the full table with horizontal scroll and a frozen first column if columns overflow.
- On mobile, convert to card/list layout where each row becomes a vertical card.
- Never silently cut off or hide data -- show a column count indicator: "Scroll to see 4 more columns."

### Row Actions and Selection

- Provide per-row actions via icon buttons or a three-dot overflow menu. Place the most frequent action as a direct button.
- Add a checkbox column for multi-selection. Include a header checkbox with disambiguation: "Select all on this page" vs. "Select all 2,341 results."
- Define a consistent row click behavior: either the entire row navigates to a detail view, or only specific elements are clickable. Apply the same pattern across all tables.

> Full data table reference with column customization, search patterns, filter types, saved filters, and audit checklists: see `references/tables-filters.md`

---

## CRUD Pattern Quick Reference

Maintain consistent CRUD patterns across the entire admin portal. Train users once; let them apply the same interactions everywhere.

### Create

- Use a dedicated creation page for complex objects. Reserve inline row creation for simple, few-field entities.
- Show only essential fields first; collapse advanced settings under progressive disclosure.
- Provide smart defaults to reduce field count. Pre-populate with sensible values.
- Validate inline per field -- never delay all validation until form submission.
- Auto-save drafts for long forms to prevent data loss on navigation or browser crash.
- After successful creation, redirect to the new resource's detail view or back to the list with a success toast.

### Read

- Organize detail views into logical sections or cards with clear headings.
- Display metadata prominently: created by, created at, last modified, modified by.
- Include quick-action buttons: Edit, Delete, Duplicate.
- Provide a quick-view preview panel (master-detail) so users can inspect records without navigating away from the list.

### Update

- Prefer inline editing for simple fields (status toggles, names) -- show a pencil icon on hover to indicate editability.
- Use a side panel or dedicated edit page for complex multi-field edits.
- Show a change indicator or diff so users see what they modified before saving.
- Disable the Save button until changes are detected. Provide both Save and Cancel.

### Delete

- Always require confirmation with a dialog that names the specific resource: "Delete 'Project Alpha'? This will permanently remove all 23 associated tasks."
- Use danger-styled buttons (red) in the confirmation dialog.
- Prefer soft delete (archive/trash) with a recovery period over permanent deletion.
- After deletion, return to the list with a success toast that includes a time-limited Undo option (5-10 seconds).
- Never place delete buttons adjacent to frequently used actions.

> Full CRUD reference with form validation, auto-save, diff patterns, cascade warnings, and audit checklists: see `references/crud-patterns.md`

---

## Bulk Actions

### Selection Model

- Place a bulk selector (split button) as the leftmost toolbar item above the data view.
- Use a three-state checkbox: unchecked (none), checked (all), indeterminate (partial).
- Include dropdown options: Select none, Select page, Select all (across all pages).
- Always display a count: "12 items selected" or "All 1,847 items selected."
- Persist selection across pagination -- selecting items on page 1 must remain when navigating to page 2.

### Contextual Action Bar

- When items are selected, replace or overlay the toolbar with a contextual action bar showing available bulk actions and the selection count.
- Show only actions valid for all selected items. If mixed eligibility exists, show "X of Y items eligible" or disable with explanation.

### Safety and Feedback

- **Preview before execution**: For destructive or impactful actions, show a confirmation dialog summarizing what will happen with the exact count.
- **Progressive confirmation**: Low-risk actions (tag, assign) need simple confirmation. High-risk actions (delete, status change) need explicit confirmation with impact summary. Irreversible actions require typing a confirmation word.
- **Progress feedback**: For operations exceeding 2 seconds, show a progress bar or count ("Processing 45 of 200...") with a cancel option.
- **Undo**: Provide a time-limited undo toast (5-10 seconds) after completion.
- **Partial failure handling**: If some items fail, show a summary ("8 succeeded, 4 failed") with item-level failure details.
- Clear selection state after action completion.

---

## Search and Filter Quick Reference

### Search Bar

- Keep the search bar always visible at the top of the page or table -- never hide it behind an icon on desktop.
- Use a text input with a search icon and placeholder indicating searchable fields.
- Begin showing results after 2-3 characters or 300ms debounce. Display match count.

### Filter Types by Data

| Data Type | Control | Example |
|-----------|---------|---------|
| Single-select | Radio buttons or dropdown | Status: Active / Inactive |
| Multi-select | Checkboxes or tag input | Roles: Admin, Editor, Viewer |
| Range | Slider or min/max inputs | Price: $10 - $100 |
| Date | Date picker with presets | Created: Last 7 days, This month |
| Boolean | Toggle switch | Published: Yes / No |

### Active Filter Display

- Show active filters as removable chips/tags above the results.
- Display result count reflecting active filters: "Showing 23 of 1,204 results."
- Provide a "Clear all filters" action.
- Persist filter state in URL parameters for bookmarking and sharing.

### Saved Filters

- Allow power users to save and name filter combinations.
- Make saved filters shareable via URL.
- Provide faceted counts when feasible -- show how many results each filter option would produce.

### Zero-Result States

- When no results match, show an empty state with suggestions: "No results found. Try removing some filters or broadening your search."
- Include a "Clear all filters" action in the zero-result state.

> Full search and filter reference with filter placement patterns, debounce timing, faceted search, and audit checklists: see `references/tables-filters.md`

---

## Role-Based Access (RBAC) Quick Reference

Frontend RBAC is about user experience, not security. Security enforcement must happen on the backend. The frontend adapts the UI to reduce confusion and guide users toward permitted actions.

### Display Strategy Decision Tree

| Strategy | When to Use |
|----------|-------------|
| **Hide** elements | When the feature is irrelevant to the role |
| **Disable** elements | When the user should know the feature exists but lacks permission |
| **Show read-only** | When the user needs to see data but not modify it |
| **Redirect** | When the user navigates to a protected route directly |

### Core Principles

- Apply the Principle of Least Privilege: show only what the role needs.
- Structure permissions as `resource:action` pairs (e.g., `users:create`, `posts:delete`). Map UI elements to these permission strings.
- Filter navigation items based on permissions. Hide empty navigation sections entirely.
- Show the user their current role and what it means. In multi-role or multi-tenant systems, allow context switching.
- Handle graceful degradation: if a permission is removed mid-session, show a contextual message rather than crashing.
- When a user navigates to a URL they lack access to, show a clear access-denied page with guidance on who to contact -- never a generic 403 or blank page.

> Full RBAC reference with permission granularity, audit logs, user management interfaces, and audit checklists: see `references/rbac-ui.md`

---

## Admin Portal Anti-Patterns

Flag these issues as high-severity problems in any admin portal audit:

- **No sorting or filtering on data tables** -- admin users need to locate specific records quickly; unsortable tables create friction on every task
- **Delete without confirmation** -- destructive actions executed without naming the resource and confirming consequences
- **No undo after destructive actions** -- permanent deletion without soft-delete, trash, or undo toast
- **Inconsistent CRUD patterns** -- create via modal on one page, via full page on another, via inline on a third
- **Bulk actions without count or progress** -- executing on "selected items" without showing exactly how many or providing progress feedback
- **Search hidden behind an icon** -- forcing users to discover and click an icon before they can search
- **Filters that reset on navigation** -- losing filter state when viewing a detail and returning to the list
- **Generic 403 pages** -- showing "Forbidden" without explaining why or whom to contact
- **No loading states for table data** -- displaying an empty table while data loads, creating confusion about whether results exist
- **Select-all ambiguity** -- a "Select all" checkbox that does not clarify whether it selects this page or all results across all pages

---

## Reference Files

For detailed, audit-ready content on each topic, consult:

| File | Contents |
|------|----------|
| `references/crud-patterns.md` | Create forms, validation, auto-save, read/detail views, inline editing, diff patterns, delete confirmation, soft-delete, cascade warnings, bulk CRUD operations, with checkable audit items |
| `references/tables-filters.md` | Data table sorting, pagination, density, responsive design, column customization, search patterns, filter types, active filter chips, saved filters, zero-result handling, with checkable audit items |
| `references/rbac-ui.md` | Role-based view strategies, permission granularity, graceful access denial, role indicators, context switching, audit log presentation, user management interfaces, with checkable audit items |
