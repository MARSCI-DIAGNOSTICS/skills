# Data Tables and Search/Filter Patterns -- Complete Reference

> Comprehensive guide to admin portal data tables, column customization, sorting, pagination, density controls, responsive behavior, search patterns, filter types, active filter display, saved filters, and zero-result handling. All patterns include specific measurements, real-world examples, and checkable audit items.

---

## 1. Data Table Design

### Alignment Rules

Consistent alignment is critical for scannability. Follow these rules without exception:

| Data Type | Alignment | Rationale |
|-----------|-----------|-----------|
| Text (names, descriptions, labels) | Left-aligned | Natural reading direction in LTR languages |
| Numbers (counts, amounts, percentages) | Right-aligned | Decimal points and digit places align for comparison |
| Dates and timestamps | Left-aligned | Read as text strings |
| Status badges | Left-aligned or centered | Visual element, not comparable numerically |
| Actions (buttons, icons) | Right-aligned or centered | Consistent position at row end |
| Column headers | Match data alignment | Header visually anchors the column's content |

### Row Clarity

- Apply subtle zebra striping using alternating row backgrounds at 5-10% gray opacity (e.g., `rgba(0,0,0,0.03)` alternating with transparent).
- Alternatively, use 1px bottom borders between rows in a light gray (e.g., `neutral-200`).
- Do not combine both zebra striping and row borders -- pick one approach and apply it consistently.
- Add a hover highlight on rows to indicate interactivity: a subtle background tint (e.g., `neutral-100`) on mouse hover.

### Cell Padding and Typography

| Density | Row Height | Horizontal Padding | Vertical Padding | Body Text Size |
|---------|-----------|-------------------|-----------------|---------------|
| Compact | 32px | 8px | 4px | 13-14px |
| Comfortable (default) | 40px | 12px | 8px | 14px |
| Spacious | 48px | 16px | 12px | 14-16px |

- Use the product's standard body font for most columns.
- Use a monospaced font for numeric, code, and ID columns.
- Truncate long text with ellipsis and show full content in a tooltip on hover. Never wrap text in data cells unless the column is designated for long-form content (e.g., description columns).

### Header Design

- Make column headers visually distinct: use a slightly darker background (e.g., `neutral-50` or `neutral-100`), semibold font weight, and uppercase or small-caps for labels (12-13px).
- Fix the header row so it remains visible during vertical scroll (sticky header).
- Apply a subtle bottom border (2px) to the header row to separate it from data rows.

---

## 2. Sorting

### Visual Indicators

- Display a sort indicator (arrow or chevron) on the currently sorted column header. Use an up arrow for ascending and a down arrow for descending.
- Show a subtle, muted sort icon on all sortable columns to indicate they are interactive. On hover, make the icon fully opaque.
- Non-sortable columns should have no sort indicator at all.

### Sort Behavior

- On first click of a sortable header, sort ascending. On second click, sort descending. On third click, return to the default (unsorted) state.
- Default sort should match the most common use case: typically newest first (descending by date) for activity logs, alphabetical A-Z for name columns.
- Persist the user's sort preference across pagination. When the user changes pages, the sort order must remain the same.
- For server-side sorted tables, show a loading indicator while re-fetching sorted data.

### Multi-Column Sort

- Support multi-column sorting for power users: hold Shift + click to add secondary and tertiary sort columns.
- Show sort priority numbers on each sorted column (1, 2, 3) to indicate the sort hierarchy.
- Limit multi-column sort to 3 levels to prevent confusion.

### Sorting Audit Checklist

- [ ] All data columns are sortable (except action columns)
- [ ] Sort indicator (arrow/chevron) is visible on the active sort column
- [ ] Sortable columns show a subtle icon on hover indicating interactivity
- [ ] First click sorts ascending, second click descending, third click resets
- [ ] Default sort matches the most common use case
- [ ] Sort state persists across pagination
- [ ] Loading indicator appears during server-side sort operations
- [ ] Multi-column sort is supported via Shift+click (for power users)

---

## 3. Pagination

### Pagination Controls

Place pagination controls below the table with these elements:

1. **Items-per-page selector**: Dropdown with options 10, 25, 50, 100. Default to 25 for most admin tables.
2. **Range indicator**: "Showing 26-50 of 1,204 results."
3. **Page navigation**: Previous/Next buttons + page number links. Show first, last, and 2-3 pages around the current page with ellipsis for gaps.
4. **Jump-to-page**: For tables with 20+ pages, include a "Go to page" input for direct navigation.

### Pagination vs. Infinite Scroll vs. Virtual Scroll

| Pattern | Best For | Characteristics |
|---------|---------|-----------------|
| **Pagination** | Admin tables, data management | Deterministic; users can reference specific pages; supports URL bookmarking |
| **Infinite scroll** | Activity feeds, social timelines | Continuous discovery; poor for referencing specific items |
| **Virtual scroll** | Very large datasets (10,000+ rows) with fast interaction | Renders only visible rows; feels like infinite list but performs like pagination |

For admin portals, use pagination as the default. Reserve virtual scroll for specialized data-heavy views (log viewers, large exports).

### Pagination State

- Persist the items-per-page preference per user across sessions.
- Include pagination parameters in the URL (`?page=3&per_page=50`) so users can bookmark and share specific pages.
- When returning from a detail view, restore the user's previous page position (do not reset to page 1).
- When applying filters, reset to page 1 (since the result set changes).

### Pagination Audit Checklist

- [ ] Items-per-page selector offers 10, 25, 50, 100 options
- [ ] Default items per page is 25
- [ ] Range indicator shows "Showing X-Y of Z results"
- [ ] Total record count is always displayed
- [ ] Page navigation includes Previous/Next and numbered page links
- [ ] Jump-to-page input exists for tables with 20+ pages
- [ ] Items-per-page preference persists per user across sessions
- [ ] Pagination parameters are reflected in the URL
- [ ] Returning from a detail view restores the previous page position
- [ ] Applying new filters resets pagination to page 1

---

## 4. Row Density Controls

### Implementation

- Provide a density toggle control in the table toolbar. Use icon buttons or a dropdown showing: Compact, Comfortable, Spacious.
- Apply density changes immediately without page reload. Transition smoothly with a subtle animation (150-200ms).
- Persist the density preference per user, per table view (different tables may warrant different densities).

### When to Default to Each Density

| Context | Default Density | Rationale |
|---------|----------------|-----------|
| Standard admin table | Comfortable (40px) | Balanced readability and data density |
| Log viewer / event stream | Compact (32px) | Maximize visible entries for scanning |
| Touch-optimized / accessibility-focused | Spacious (48px) | Meets 44px minimum touch target requirement |
| Table with complex inline content (avatars, multi-line text) | Spacious (48px) | Prevents content clipping |

### Row Density Audit Checklist

- [ ] Density toggle is available in the table toolbar
- [ ] Three density options are offered: Compact, Comfortable, Spacious
- [ ] Density changes apply immediately without page reload
- [ ] Density preference persists per user per table view
- [ ] Compact density row height is 32px with 4-8px padding
- [ ] Comfortable density row height is 40px with 8-16px padding
- [ ] Spacious density row height is 48px with 12-24px padding
- [ ] Spacious density meets the 44px minimum touch target requirement

---

## 5. Responsive Table Design

### Desktop (> 1024px)

- Display the full table with all default columns visible.
- If columns overflow horizontally, enable horizontal scrolling with the first column (identifier column) frozen/sticky.
- Show a horizontal scroll indicator or shadow on the right edge to signal more content.

### Tablet (768-1024px)

- Reduce visible columns to the 5-6 most important ones.
- Freeze the first column and enable horizontal scrolling for remaining columns.
- Consider converting to a master-detail layout: list on the left, detail panel on the right.

### Mobile (< 768px)

- Convert the table to a card/list layout. Each row becomes a vertical card showing:
  - Primary identifier (name, title) as the card heading
  - 2-3 key attributes below the heading
  - Status badge
  - Action buttons (edit, delete) in the card footer
- Place the search and filter controls above the card list, collapsible into a filter drawer.
- Use a floating action button (FAB) for the primary create action.

### Responsive Table Audit Checklist

- [ ] Full table displayed on desktop with horizontal scroll if columns overflow
- [ ] First column (identifier) is frozen during horizontal scroll
- [ ] Horizontal scroll indicator or shadow is visible
- [ ] Tablet view reduces visible columns to 5-6 most important
- [ ] Mobile view converts table rows to vertical cards
- [ ] Card layout shows primary identifier, 2-3 key attributes, status, and actions
- [ ] Search and filter controls are accessible on mobile (collapsible drawer or inline)
- [ ] Create action is accessible on mobile (FAB or top-bar button)

---

## 6. Column Customization

### Column Visibility

- Provide a "Columns" button in the table toolbar that opens a dropdown or modal listing all available columns.
- Each column has a toggle (checkbox or switch) to show or hide it.
- Mark certain columns as always visible (e.g., name/identifier, actions) -- these cannot be hidden.
- Show column count: "Showing 7 of 15 columns."
- Persist column visibility preferences per user per table.

### Column Reordering

- Support drag-and-drop column reordering in the column configuration panel.
- Alternatively, support drag-and-drop of column headers directly in the table.
- Persist column order preferences per user per table.

### Column Pinning (Freeze)

- Allow users to pin/freeze columns to the left edge so they remain visible during horizontal scroll.
- The identifier column (name, ID) should be pinned by default.
- Show a visual divider (shadow or border) between pinned and scrollable columns.

### Column Resizing

- Support column width resizing via drag handles on column header borders.
- Set minimum column widths to prevent content from becoming unreadable (minimum 80px for text columns, 60px for numeric columns).
- Double-click on a column border to auto-fit the column width to its content.
- Persist column width preferences per user per table.

### Column Customization Audit Checklist

- [ ] "Columns" button exists in the table toolbar
- [ ] All available columns are listed with toggles for visibility
- [ ] Certain columns (name, actions) are locked as always visible
- [ ] Column count indicator shows "Showing X of Y columns"
- [ ] Column visibility preferences persist per user per table
- [ ] Column reordering is supported (drag-and-drop)
- [ ] Column order preferences persist per user per table
- [ ] Identifier column is pinned/frozen by default
- [ ] Visual divider separates pinned from scrollable columns
- [ ] Column resizing is supported via drag handles
- [ ] Minimum column width prevents content from becoming unreadable
- [ ] Double-click auto-fits column width to content
- [ ] Column width preferences persist per user per table

---

## 7. Search Patterns

### Search Bar Placement

- Position the search bar prominently above the table, always visible on desktop. Never hide it behind an icon.
- Use a full-width or partial-width text input (minimum 280px wide) with a search icon (magnifying glass) inside the input.
- Include placeholder text indicating searchable fields: "Search by name, email, or ID..."
- Place the search bar on the left side of the toolbar, with filter and column controls on the right.

### Search Behavior

- Use **incremental search**: begin filtering results after 2-3 characters.
- Apply a **300ms debounce** to avoid excessive API calls during typing. Fire the search request 300ms after the user stops typing.
- Show the match count as results update: "47 results for 'smith'."
- Highlight matching text within table cells to help users locate their search term visually.
- Support clearing the search with a visible "X" button inside the input field.
- Preserve the search query in the URL as a query parameter (`?q=smith`) for bookmarking and sharing.

### Persistent Search

- Maintain the search query when the user navigates to a detail view and returns to the list.
- Clear the search only when the user explicitly clicks the clear button or navigates to a different section entirely.
- Show the active search term visually: either keep the search input populated or show it as a chip below the search bar.

### Full-Text vs. Field-Specific Search

| Pattern | Use When | Implementation |
|---------|----------|---------------|
| **Full-text** (global search) | Users do not know which field contains their term | Search across all visible text columns simultaneously |
| **Field-specific** | Power users who know the exact field | Provide an advanced search mode with per-field inputs or syntax: `email:john@example.com` |

- Default to full-text search for simplicity. Offer field-specific search as an advanced option.

### Search Audit Checklist

- [ ] Search bar is always visible above the table on desktop (not behind an icon)
- [ ] Search input is at least 280px wide with a search icon
- [ ] Placeholder text indicates searchable fields
- [ ] Incremental search begins after 2-3 characters
- [ ] 300ms debounce is applied to search input
- [ ] Match count is displayed as results update
- [ ] Matching text is highlighted within table cells
- [ ] Clear button (X) is visible inside the search input
- [ ] Search query is preserved in URL parameters
- [ ] Search persists when navigating to a detail view and returning
- [ ] Full-text search is the default; field-specific search is available as advanced option

---

## 8. Filter Patterns

### Filter Types by Data Type

Select the correct control for each data type:

| Data Type | Control | Behavior |
|-----------|---------|----------|
| **Enum / Category** (single) | Dropdown or radio buttons | One option selected at a time |
| **Enum / Category** (multi) | Checkboxes, multi-select dropdown, or tag input | Multiple options selected simultaneously |
| **Numeric range** | Two inputs (min/max) or range slider | Both endpoints optional; validate min <= max |
| **Date range** | Date picker with presets + custom range | Presets: Today, Last 7 days, Last 30 days, This month, This quarter, Custom |
| **Boolean** | Toggle switch or checkbox | Yes/No, On/Off, Active/Inactive |
| **Text / Keyword** | Text input with typeahead/autocomplete | Free-text with suggestions from existing values |
| **User / Owner** | Avatar dropdown with search | Searchable list of team members |

### Filter Placement Patterns

| Pattern | Best For | Characteristics |
|---------|---------|----------------|
| **Inline horizontal bar** | 1-5 simple filters | Compact row above the table; always visible; fast access |
| **Side panel** | 6+ filter categories, faceted search | Persistent or toggleable panel on the left; good for dense filtering |
| **Popover / Dropdown** | Space-constrained layouts, moderate filter count | Filter button opens a popover with filter controls; saves space |
| **Modal** | Complex filter builder, infrequent use | Full-screen or large modal for advanced query building |
| **Quick filter chips** | Predefined common filters | Row of clickable chips above results: "Active", "Created this week", "Assigned to me" |

For most admin tables, use an **inline horizontal bar** for the top 3-5 filters, with an "Advanced filters" button that opens a side panel or popover for additional filters.

### Filter Interaction Patterns

| Pattern | When to Use | Behavior |
|---------|-------------|----------|
| **Instant update** | Fast queries (< 500ms response), few filters | Results update on each filter selection; immediate feedback |
| **Batch update** ("Apply" button) | Expensive queries, many filter categories | User selects multiple filters, then clicks "Apply" to execute |

- For tables with fewer than 10,000 rows and fast backend, use instant update.
- For large datasets or complex queries, use batch update with an "Apply" button.

### Active Filter Display

- Show active filters as removable chips/tags above the table results.
- Each chip displays the filter category and value: "Status: Active", "Role: Admin, Editor."
- Each chip has an "X" button to remove that specific filter.
- Show a "Clear all filters" action when any filters are active.
- Display the filtered result count: "Showing 23 of 1,204 results."
- When a filter reduces results to a subset, maintain visual contrast between the filtered count and total count.

### Saved Filters / Saved Views

- Allow power users to save the current filter combination as a named view: "My active projects", "Pending approvals."
- Saved views persist the filter state, sort order, column visibility, and density preference.
- Display saved views as selectable options above the table or in a dropdown.
- Allow sharing saved views with other users via URL.
- Support editing and deleting saved views.
- System-provided default views: "All items", "Recently created", "Assigned to me."

### Faceted Counts

- When feasible, show the count of results each filter option would produce next to the option label.
- Example: "Active (847)", "Inactive (357)", "Invited (12)."
- Disable or dim filter options that would produce zero results to prevent dead-end selections.
- Faceted counts reduce trial-and-error filtering and set expectations before the user commits to a filter.

### Filter State Persistence

- Persist filter state in URL query parameters (`?status=active&role=admin`) so users can bookmark, share, and navigate back to the same filtered view.
- Maintain filter state across pagination (changing pages must not reset filters).
- Maintain filter state when navigating to a detail view and returning to the list.
- Reset filters only when the user explicitly clears them or navigates to a different section.

### Filter Audit Checklist

- [ ] Filter controls use the correct input type for each data type (dropdown, checkbox, date picker, etc.)
- [ ] 1-5 primary filters are visible inline above the table
- [ ] Additional filters are accessible via "Advanced filters" button (side panel or popover)
- [ ] Quick filter chips are available for common predefined filters
- [ ] Active filters are displayed as removable chips above the results
- [ ] Each filter chip shows category and value with an "X" to remove
- [ ] "Clear all filters" action is available when any filters are active
- [ ] Filtered result count is displayed: "Showing X of Y results"
- [ ] Filter state is persisted in URL query parameters
- [ ] Filter state persists across pagination
- [ ] Filter state persists when navigating to detail view and returning
- [ ] Saved filters/views can be created, named, edited, and deleted
- [ ] Saved views persist filter state, sort order, columns, and density
- [ ] Saved views are shareable via URL
- [ ] Faceted counts are shown next to filter options when feasible
- [ ] Zero-result filter options are disabled or dimmed

---

## 9. Zero-Result Handling

### Empty State for No Results

When filters or search produce zero results, never show a blank table. Display a designed empty state:

- **Illustration or icon**: A search icon, empty box, or custom illustration to make the state visually distinct from a loading state.
- **Descriptive heading**: "No results found" or "No items match your filters."
- **Suggestion text**: "Try removing some filters, broadening your search, or checking for typos."
- **Action buttons**:
  - "Clear all filters" to reset to the unfiltered view.
  - "Clear search" if a search term is active.
  - "Create new [entity]" if the user might want to create what they were looking for.

### Distinguishing Zero-Result States

| State | Visual Treatment | Message |
|-------|-----------------|---------|
| **No results from search** | Search icon + suggestion | "No results for 'xyz'. Try a different search term." |
| **No results from filters** | Filter icon + suggestion | "No items match your current filters. Try removing some filters." |
| **Empty collection** (no items exist at all) | Illustration + CTA | "No projects yet. Create your first project to get started." |
| **Error loading data** | Error icon + retry | "We couldn't load the data. Check your connection and try again." |

### Zero-Result Audit Checklist

- [ ] Zero-result state is visually distinct from loading state
- [ ] Zero-result state includes a descriptive heading
- [ ] Zero-result state includes suggestion text for broadening the search
- [ ] "Clear all filters" action button is present in zero-result state
- [ ] "Clear search" action is present when a search term is active
- [ ] Empty collection state (no items at all) includes a CTA to create the first item
- [ ] Error state includes a retry button and is visually distinct from zero-result state
- [ ] Zero-result states are consistent in style across all tables in the admin portal
