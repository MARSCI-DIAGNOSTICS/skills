# CRUD Patterns -- Complete Reference

> Comprehensive guide to Create, Read, Update, and Delete patterns in admin portals. Covers form design, validation, auto-save, detail views, inline editing, diff views, delete safety, bulk CRUD, and consistent pattern application. All patterns include specific measurements, real-world examples, and checkable audit items.

---

## 1. Create Patterns

### Form Layout

Design create forms to minimize cognitive load and prevent data loss:

- Use **single-column layouts** for all create forms. Single-column forms improve completion rates by 15.4% and are completed 15.4 seconds faster than multi-column layouts.
- Group related fields into labeled sections with clear headings. Use the Gestalt principle of proximity: spacing within a group (8-12px) should be notably less than spacing between groups (24-32px).
- Place the most critical fields at the top. Use progressive disclosure: show only essential fields first, with "Advanced settings" collapsed below.
- Provide **smart defaults** to reduce the number of decisions. Pre-populate fields with sensible values (e.g., status defaults to "Draft," timezone defaults to the user's detected timezone).
- Limit create forms to the minimum viable fields. Every additional field reduces completion rates by approximately 10%.

### Field Design

- Display visible labels above every input -- never use placeholder text as the sole label (it disappears when typing and fails WCAG).
- Mark required fields with an asterisk (*) and an `aria-required="true"` attribute. If most fields are required, mark optional fields instead ("Optional" text after the label).
- Use the correct HTML input type for each field (`type="email"`, `type="tel"`, `type="number"`, `type="url"`) to trigger appropriate mobile keyboards and enable browser autofill.
- Show character counts for fields with length limits. Display remaining characters: "142 / 280 characters."
- Provide helper text below fields for format guidance: "Enter a URL starting with https://"

### Inline Validation

- Validate on blur (when the user leaves the field), not on every keystroke. Keystroke validation for fields like email creates premature error states.
- Show errors inline immediately adjacent to the offending field, not in a generic banner at the top of the page.
- Use the structure: red border on the field + red error icon + specific error text below the field.
- Provide constructive correction: "Email must include @ and a domain (e.g., name@company.com)" instead of "Invalid email."
- Validate required fields only after the user has interacted with them (touched + blurred). Never show "required" errors on page load.
- Show success indicators for validated fields (green checkmark) to provide positive reinforcement.
- Inline validation reduces form errors by 22% compared to post-submission-only validation.

### Auto-Save for Long Forms

- For forms with more than 8 fields or forms that take more than 2 minutes to complete, implement auto-save to prevent data loss.
- Save drafts automatically every 30-60 seconds when changes are detected.
- Show a save indicator: "Draft saved 10 seconds ago" or "Saving..." with a subtle animation.
- Persist drafts across browser sessions. When the user returns, prompt: "You have an unsaved draft from [date]. Resume or discard?"
- Provide an explicit "Save as draft" button alongside the primary "Create" action.
- Warn on navigation away from an unsaved form: "You have unsaved changes. Leave without saving?"

### Multi-Step Create Wizards

- For complex create flows with 10+ fields across multiple categories, use a multi-step wizard.
- Limit to 3-7 steps (Miller's Law). Show a step indicator at the top: "Step 2 of 4 -- Configuration."
- Validate each step when the user clicks Next, not on final submission. Prevent advancing until the current step validates.
- Allow backward navigation without losing data.
- Include a final "Review & Confirm" step summarizing all inputs before submission.
- Save progress between steps so users can resume later.
- Multi-step forms increase conversions by up to 300% compared to long single-page forms.

### Post-Create Behavior

- After successful creation, redirect to the newly created resource's detail view (preferred for complex objects) or back to the list with a success toast (preferred for simple objects).
- The success toast should name what was created: "Project 'Alpha' created successfully."
- Include a relevant next action in the toast or detail view: "View project" or "Add team members."

### Create Form Audit Checklist

- [ ] Form uses a single-column layout
- [ ] Fields are grouped into labeled sections with clear headings
- [ ] Spacing within groups (8-12px) is less than spacing between groups (24-32px)
- [ ] Essential fields appear first; advanced settings are collapsed
- [ ] Smart defaults reduce the number of required decisions
- [ ] Labels are visible above inputs (not placeholder-only)
- [ ] Required fields are marked with asterisk (*) and `aria-required="true"`
- [ ] HTML input types match data (`type="email"`, `type="tel"`, etc.)
- [ ] Character counts are displayed for length-limited fields
- [ ] Inline validation triggers on blur (not on every keystroke)
- [ ] Error messages are specific and suggest corrections
- [ ] Error messages appear inline adjacent to the field (not only at page top)
- [ ] Auto-save is implemented for forms with 8+ fields
- [ ] Draft persistence survives browser session loss
- [ ] Navigation away from an unsaved form triggers a warning
- [ ] Post-create redirect goes to detail view or list with success toast
- [ ] Success feedback names the created resource specifically

---

## 2. Read Patterns (List and Detail Views)

### List Views

- Present records in a data table with sortable columns, pagination, and density options (see `tables-filters.md` for full table reference).
- Default to comfortable density (40px row height, 8-16px cell padding). Offer compact mode for power users.
- Show the most important columns first (leftmost). Limit default visible columns to 5-7 to avoid horizontal overflow.
- Provide quick-view preview: a master-detail layout where selecting a row reveals a summary panel beside the list. Use a horizontal split with the master list at 30-40% width and detail at 60-70%.
- Show an empty state in the detail pane when no item is selected: "Select an item to view details."

### Detail Views

- Organize information into logical sections using cards or bordered regions with clear headings.
- Place the resource name and primary identifier at the top as the page heading.
- Include breadcrumb navigation: Home > Resources > Resource Name. Make all levels clickable except the current page.
- Display metadata prominently in a sidebar or header area:
  - Created by (user avatar + name)
  - Created at (relative time with absolute time tooltip)
  - Last modified (relative time)
  - Modified by (user avatar + name)
  - Status badge (color-coded)
  - Resource ID (copyable)

### Quick Actions on Detail Views

- Place an action bar at the top of the detail view with: Edit, Duplicate, Archive/Delete, and a three-dot overflow for less common actions (Export, Print, Share).
- Style Edit as the primary action. Style Delete as destructive (red text or icon).
- Place the action bar in a sticky header so it remains accessible during scroll.

### Read View Audit Checklist

- [ ] List view uses a data table with sortable columns
- [ ] Default visible columns are limited to 5-7
- [ ] Quick-view preview panel is available (master-detail layout)
- [ ] Detail views organize information into labeled sections or cards
- [ ] Breadcrumb navigation is present and all levels are clickable
- [ ] Metadata is displayed: created by, created at, last modified, modified by, status
- [ ] Resource ID is displayed and copyable
- [ ] Action bar with Edit, Duplicate, Delete is present at the top
- [ ] Action bar remains accessible during scroll (sticky positioning)
- [ ] Empty state is designed for the detail pane when no item is selected

---

## 3. Update Patterns

### Inline Editing

Use inline editing for simple, single-field updates directly within tables or detail views:

- Show a pencil/edit icon on hover to indicate the field is editable.
- On click, transform the display value into an editable input. Pre-populate with the current value.
- Show Save (checkmark) and Cancel (X) controls immediately adjacent to the editing field.
- Support keyboard shortcuts: Enter to save, Escape to cancel.
- Apply optimistic UI updates: show the new value immediately, then reconcile with the server. If the server rejects the change, roll back and show an error.
- Suitable field types: names, titles, status toggles, single-select dropdowns, short text fields.

### Side Panel Editing

Use a slide-over side panel for editing 3-8 related fields without losing the context of the list:

- The panel slides in from the right, overlaying part of the list while keeping it partially visible.
- Panel width: 400-600px on desktop. Full-screen on mobile with a back button.
- Pre-populate all fields with current values.
- Include a clear title: "Edit [Resource Name]."
- Place Save and Cancel buttons at the bottom of the panel (sticky footer).

### Full Edit Page

Use a dedicated edit page for complex objects with many fields, rich text editors, or file uploads:

- Use the same form layout as the create form for consistency. Pre-populate all fields with current values.
- Show a page title indicating edit mode: "Edit Project: Alpha."
- Include breadcrumbs back to the detail view and list view.

### Change Indicators and Diffs

- Before saving, visually indicate what the user changed. Highlight modified fields with a subtle left border or background tint.
- For high-stakes edits (configuration, permissions, billing), show a review step: a side-by-side or inline diff of old vs. new values.
- Use color coding for diffs: red background with strikethrough for removed values, green background for new values.
- Show a "Changes summary" badge in the save button area: "3 fields changed."

### Conflict Resolution

- When two users edit the same resource simultaneously, detect the conflict on save.
- Show a conflict resolution dialog: display both versions side by side (yours vs. theirs) and let the user choose which to keep per field or overwrite entirely.
- Timestamp the last save and warn: "This resource was modified by [User] at [time]. Your changes may overwrite theirs."

### Update Audit Checklist

- [ ] Inline editing is available for simple fields (names, statuses, toggles)
- [ ] Hover state reveals a pencil icon indicating editability
- [ ] Inline editing supports Enter to save and Escape to cancel
- [ ] Side panel editing is used for moderate-complexity edits (3-8 fields)
- [ ] Side panel pre-populates with current values
- [ ] Full edit page uses the same layout as the create form
- [ ] Edit page title clearly indicates edit mode with the resource name
- [ ] Modified fields are highlighted before saving (border or background tint)
- [ ] High-stakes edits show a diff (old vs. new values) before confirmation
- [ ] Save button is disabled until changes are detected
- [ ] Optimistic UI is applied for high-success-rate updates with rollback on failure
- [ ] Concurrent edit conflicts are detected and a resolution dialog is provided

---

## 4. Delete Patterns

### Confirmation Dialogs

Never delete without confirmation. Use a confirmation dialog that follows this anatomy:

1. **Title**: Clear statement of the action -- "Delete project?"
2. **Description**: Consequences stated explicitly -- "This will permanently delete 'Project Alpha' and all 47 associated tasks. This action cannot be undone."
3. **Primary action button**: Labeled with the specific action ("Delete project"), styled as destructive (red background, white text).
4. **Cancel button**: Always present, styled as secondary, labeled specifically ("Keep project" or "Cancel").

Never use generic "Yes / No" or "OK / Cancel" labels. Specific labels reduce accidental destructive actions.

### Confirmation Friction Scale

Match confirmation friction to the severity of the action:

| Risk Level | Confirmation Type | Example |
|------------|-------------------|---------|
| Low | Simple dialog with specific action button | Removing a tag or label |
| Medium | Dialog with impact summary | Deleting a single record with no dependencies |
| High | Type-to-confirm (type the resource name) | Deleting a project with associated data |
| Critical | Type-to-confirm + password re-entry + waiting period | Deleting an organization or purging all data |

### Soft Delete (Archive / Trash Pattern)

- Prefer soft delete over hard delete. Move items to a "Trash" or "Archived" state with a 30-day recovery window.
- Show a success toast with an Undo action: "Project 'Alpha' deleted. [Undo] -- This action auto-expires in 10 seconds."
- Provide a Trash view where users can browse, restore, or permanently purge deleted items.
- Display the deletion date and auto-purge countdown in the trash: "Will be permanently deleted in 23 days."
- After the recovery window expires, permanently purge the data (or retain per compliance requirements).

### Cascade Warnings

When deleting a resource that has dependent resources (child records, associations):

- Show the cascade impact in the confirmation dialog: "Deleting this team will also remove 12 members, 45 projects, and 203 tasks."
- List the types and counts of affected resources.
- For critical cascades, provide an option to reassign dependencies before deletion: "Reassign projects to another team before deleting."

### Positioning Delete Actions

- Never place the Delete button immediately adjacent to the Save or Edit button. Fitts's Law: close proximity increases accidental clicks.
- Place Delete in a "Danger Zone" area at the bottom of settings or detail pages, visually separated from standard actions.
- In table row actions, place Delete last in the action list or inside the three-dot overflow menu.
- Style Delete actions with red text, a red icon, or both to visually signal danger.

### Delete Audit Checklist

- [ ] Every delete action requires a confirmation dialog
- [ ] Confirmation dialog names the specific resource being deleted
- [ ] Confirmation dialog states consequences explicitly (cascade impact)
- [ ] Delete button uses danger styling (red)
- [ ] Button labels are specific ("Delete project" / "Keep project"), not generic ("Yes" / "No")
- [ ] High-stakes deletions require type-to-confirm
- [ ] Soft delete (archive/trash) is implemented with a 30-day recovery window
- [ ] Success toast includes a time-limited Undo action (5-10 seconds)
- [ ] Trash view allows browsing, restoring, and permanent purging
- [ ] Trash items display auto-purge countdown
- [ ] Cascade impact is shown when deleting resources with dependencies
- [ ] Option to reassign dependencies before deletion exists for critical cascades
- [ ] Delete button is physically separated from Save/Edit buttons
- [ ] Delete appears last in action lists or inside overflow menus

---

## 5. Bulk CRUD Operations

### Bulk Create

- Support CSV import and multi-line paste for bulk entity creation.
- Show a preview of records to be created before execution, with validation results per row.
- Highlight rows with validation errors in red and allow inline correction before confirming.
- Display a summary after import: "47 records created. 3 records skipped due to errors. [View errors]."

### Bulk Update

- Allow selecting multiple records and applying a change to all selected items simultaneously.
- Show a contextual action bar when items are selected with available bulk update options (change status, assign owner, add tags).
- Use a confirmation dialog: "Change status to 'Published' for 23 items?"
- For mixed eligibility, show: "18 of 23 selected items are eligible for this action. 5 items skipped because [reason]."
- Provide a progress indicator for large batches: "Updating 45 of 200..."

### Bulk Delete

- Show the exact count: "Delete 12 items? This action cannot be undone."
- For bulk deletion of items with dependencies, summarize total cascade impact: "This will also delete 34 associated tasks and 12 comments."
- Offer a time-limited undo toast: "12 items deleted. [Undo]."
- Log every bulk delete operation in the audit trail with the list of affected resource IDs.

### Bulk Operation Audit Checklist

- [ ] Bulk create supports CSV import with preview before execution
- [ ] Validation errors are shown per row before confirming bulk create
- [ ] Post-import summary shows success count, error count, and error details
- [ ] Bulk update contextual action bar appears when items are selected
- [ ] Bulk update confirmation shows exact count and action description
- [ ] Mixed eligibility is handled with clear explanation of skipped items
- [ ] Bulk delete confirmation dialog shows exact count and cascade impact
- [ ] Progress indicator appears for bulk operations exceeding 2 seconds
- [ ] Time-limited undo toast is provided after bulk delete
- [ ] All bulk operations are logged in the audit trail

---

## 6. Consistent Pattern Application

### Pattern Consistency Rules

Adopt one pattern for each interaction type and use it throughout the admin portal:

| Interaction | Choose One Pattern | Apply Everywhere |
|-------------|-------------------|-----------------|
| Simple entity creation | Inline row in table OR modal form | All simple create flows |
| Complex entity creation | Dedicated page OR multi-step wizard | All complex create flows |
| Simple field editing | Inline click-to-edit | All single-field updates |
| Multi-field editing | Side panel OR edit page | All multi-field updates |
| Delete confirmation | Dialog with specific labels | All delete actions |
| Success feedback | Toast notification | All CRUD success states |
| Error feedback | Inline per field + summary banner | All CRUD error states |

### Form Layout Consistency

- Use the same field ordering convention across all forms: identification fields (name, title) first, configuration fields second, metadata fields third.
- Use the same label positioning (above inputs), the same required field indicator (*), and the same error styling (red border + red text below field) on every form.
- Maintain the same button placement: primary action on the right, secondary (Cancel) on the left, destructive action separated or in overflow.

### Pattern Consistency Audit Checklist

- [ ] The same create pattern (modal, page, or inline) is used for the same entity complexity level across the portal
- [ ] The same edit pattern (inline, side panel, or edit page) is used for the same field complexity level
- [ ] All delete confirmations use the same dialog structure and button styling
- [ ] All success feedback uses the same mechanism (toast or inline message)
- [ ] All error feedback uses the same mechanism (inline per field + optional summary)
- [ ] Field ordering convention is consistent across all forms
- [ ] Label positioning is consistent across all forms (above inputs)
- [ ] Required field marking is consistent across all forms (asterisk *)
- [ ] Button placement follows the same convention across all forms
