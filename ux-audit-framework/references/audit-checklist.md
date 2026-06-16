# UX Audit Checklist

This checklist provides a comprehensive evaluation instrument for conducting UX audits. Work through each category systematically, checking items as they pass evaluation. Any unchecked item is a potential finding that requires severity rating and documentation in the audit report.

Use this checklist during **Phase 2 (Analyze)** of the audit process described in the SKILL.md.

---

## A. Navigation and Information Architecture

### A1. Main Navigation Structure

- [ ] Main navigation is clearly visible and consistently placed across all pages
- [ ] Active/current page is visually indicated in the navigation (color, weight, or indicator bar)
- [ ] Top-level navigation contains 7 or fewer items (Miller's Law compliance)
- [ ] Navigation items use clear, descriptive labels (no jargon or internal terminology)
- [ ] Navigation items are logically grouped by function or domain
- [ ] Primary actions (Dashboard, Projects, etc.) are separated from utility actions (Settings, Help)
- [ ] Navigation placement is consistent — it does not move or change position between pages

### A2. Hierarchy and Wayfinding

- [ ] Breadcrumbs are present for any page deeper than 2 levels in the hierarchy
- [ ] URL structure reflects the content hierarchy and is human-readable
- [ ] Users can reach any primary section within 2 clicks from any page
- [ ] Browser back button works as expected on every page (no trapping, no unexpected behavior)
- [ ] Page titles are unique and descriptive (visible in browser tab)
- [ ] Site map or footer navigation provides an alternative path to content

### A3. Search

- [ ] Search bar is always visible on desktop (not hidden behind an icon)
- [ ] Search provides results within 300ms of input (instant/incremental search)
- [ ] Search results are relevant and ranked by usefulness
- [ ] Search handles typos and synonyms gracefully (did-you-mean, fuzzy matching)
- [ ] Search shows result count and supports filtering of results
- [ ] Zero-result search states provide suggestions to broaden the query
- [ ] Recent searches or search history is available for repeat lookups

### A4. Mobile Navigation

- [ ] Mobile navigation is reachable within 1 tap (hamburger menu or bottom nav)
- [ ] Mobile menu provides access to all primary navigation items
- [ ] Menu opens and closes predictably without unexpected content shifts
- [ ] Active page is indicated in the mobile navigation
- [ ] Navigation gestures (swipe to go back) work where platform-appropriate

---

## B. Visual Design and Hierarchy

### B1. Visual Hierarchy

- [ ] Every page has a clear visual focal point (one primary metric, heading, or action)
- [ ] Typography uses at least 3 distinct size levels to establish hierarchy (heading, subheading, body)
- [ ] Visual weight (size, color, contrast, position) correctly reflects element importance
- [ ] Primary CTA or key action is visible without scrolling on all standard viewports
- [ ] Information follows natural scanning patterns (F-pattern or Z-pattern for LTR languages)

### B2. Typography

- [ ] Body text is at least 16px on all devices
- [ ] Line height is 1.4-1.6 for body text for comfortable readability
- [ ] Line length is 50-75 characters for optimal readability
- [ ] Font family is consistent and limited to 2-3 typefaces maximum
- [ ] Text contrast meets WCAG requirements (4.5:1 for normal text, 3:1 for large text)
- [ ] Heading hierarchy is logical (h1 through h6, no skipped levels)

### B3. Color and Spacing

- [ ] Color palette is consistent across all pages (primary, secondary, accent, semantic colors)
- [ ] Semantic colors are used consistently: red/danger for errors, green/success for confirmations, yellow/warning for cautions
- [ ] Color is never the sole means of conveying information (pattern, icon, or text also used)
- [ ] Sufficient whitespace exists between sections (minimum 16px between groups)
- [ ] Spacing within groups is visibly less than spacing between groups (Gestalt proximity)
- [ ] Brand identity is consistent across all pages and states

### B4. Iconography and Imagery

- [ ] Icons are recognizable and consistently styled (outline vs. filled, size, stroke width)
- [ ] Icons are paired with text labels (no icon-only navigation on desktop)
- [ ] Images are relevant and high quality (no pixelated, stretched, or generic stock photos)
- [ ] Decorative images use empty alt text (alt=""); informative images have descriptive alt text
- [ ] Dark mode is supported and tested (if applicable to the product)

---

## C. Content and Messaging

### C1. Language and Tone

- [ ] Language is clear, concise, and free of jargon or internal terminology
- [ ] Tone is consistent across the product (professional, friendly, technical — as appropriate)
- [ ] Headings are descriptive and scannable — users can understand page purpose from headings alone
- [ ] Button labels are action-oriented and specific ("Save changes" not "Submit"; "Delete project" not "OK")
- [ ] Link text is descriptive ("View billing history" not "Click here")

### C2. Microcopy

- [ ] Form labels are clear and consistent across the product
- [ ] Placeholder text provides helpful examples, not instructions (labels remain visible)
- [ ] Tooltip text is concise and adds value beyond the visible label
- [ ] Confirmation messages clearly state what action was completed ("Project saved successfully")
- [ ] Warning messages explain the consequence ("This will permanently delete 23 items")

### C3. Empty States

- [ ] Every list, table, and content area has a designed empty state
- [ ] Empty states include descriptive text explaining what the area is for
- [ ] Empty states include a primary CTA to help users populate the area
- [ ] Empty states use illustration or preview content to set expectations
- [ ] Tone of empty states is positive and encouraging, not blaming ("No projects yet" not "No data found")

### C4. Help and Documentation

- [ ] Contextual help is available where users are likely to need it (tooltips, info icons, inline guidance)
- [ ] Help center or documentation is searchable and accessible from any page
- [ ] Keyboard shortcut reference is available (for keyboard-heavy applications)
- [ ] Onboarding or tutorial content can be re-accessed at any time
- [ ] Error documentation or troubleshooting guides exist for common issues

---

## D. Forms and Input

### D1. Labels and Structure

- [ ] All form fields have visible labels (not just placeholder text)
- [ ] Labels are positioned consistently (above or to the left of fields, matching product convention)
- [ ] Required fields are clearly marked (asterisk, "required" text, or equivalent)
- [ ] Optional fields are marked or the form indicates "all fields required unless marked optional"
- [ ] Related fields are grouped with visible section headings
- [ ] Form layout follows a single-column structure for primary flows (no side-by-side fields unless semantically related, like first/last name)

### D2. Input Types and Behavior

- [ ] Input types match the expected data: email fields use type="email", phone uses type="tel", numbers use type="number" or inputmode="numeric"
- [ ] Date inputs use a date picker with preset options (Last 7 days, This month) where applicable
- [ ] Dropdowns with more than 15 options include search/filter functionality
- [ ] Multi-select inputs use checkboxes, tag inputs, or multi-select dropdowns (not ctrl+click)
- [ ] Autofill is supported (autocomplete attributes are set correctly)
- [ ] Password fields include a show/hide toggle

### D3. Validation and Error Handling

- [ ] Inline validation appears as the user completes each field (not only on submit)
- [ ] Validation messages are specific: "Email must include an @ symbol" not "Invalid input"
- [ ] Error messages appear adjacent to the field they refer to (not only at the top of the form)
- [ ] Fields with errors are visually highlighted (border color change, icon, and text)
- [ ] Valid fields receive positive confirmation where helpful (green checkmark on availability checks)
- [ ] Form data is preserved when validation fails (no field clearing on error)

### D4. Submission and Feedback

- [ ] Submit button is clearly labeled with the action outcome ("Create account" not "Submit")
- [ ] Submit button shows a loading state during processing (spinner or disabled state with indicator)
- [ ] Success confirmation is shown after submission (toast, redirect with message, or inline confirmation)
- [ ] Failed submission shows a clear error with guidance on how to fix it
- [ ] Form state is preserved on accidental navigation (autosave or unsaved-changes warning)
- [ ] Long forms support saving progress as a draft

---

## E. Performance (Core Web Vitals)

### E1. Loading Speed

- [ ] Largest Contentful Paint (LCP) is under 2.5 seconds
- [ ] First Input Delay (FID) / Interaction to Next Paint (INP) is under 100ms / 200ms
- [ ] Time to First Byte (TTFB) is under 800ms
- [ ] Total page weight is reasonable for the content type (target under 3MB for content pages)
- [ ] Critical rendering path is optimized (above-the-fold content loads first)

### E2. Visual Stability

- [ ] Cumulative Layout Shift (CLS) is under 0.1
- [ ] Images and embeds have explicit width and height attributes (prevent layout shift)
- [ ] Web fonts use font-display: swap or optional to prevent invisible text
- [ ] Dynamic content (ads, banners, notifications) does not push existing content down
- [ ] Skeleton/placeholder states match the dimensions of the content they replace

### E3. Asset Optimization

- [ ] Images use modern formats (WebP or AVIF) with fallbacks
- [ ] Images are lazy-loaded below the fold
- [ ] CSS and JavaScript are minified and bundled appropriately
- [ ] Third-party scripts are loaded asynchronously and do not block rendering
- [ ] Caching headers are configured for static assets (long cache duration with versioned filenames)

### E4. Perceived Performance

- [ ] Skeleton screens or shimmer placeholders appear for async-loaded content
- [ ] Progress indicators appear for operations exceeding 1 second
- [ ] Optimistic UI updates are used where appropriate (action reflects immediately, syncs in background)
- [ ] Pagination or virtualization is used for large data sets (no rendering of 1,000+ DOM nodes)
- [ ] Transitions and animations do not exceed 300ms for UI state changes

---

## F. Accessibility (WCAG 2.2 Level AA)

### F1. Perceivable

- [ ] All non-decorative images have descriptive alt text
- [ ] Decorative images use alt="" (empty alt attribute)
- [ ] Text color contrast is at least 4.5:1 for normal text and 3:1 for large text (18px+ bold or 24px+)
- [ ] UI component contrast (borders, icons, focus indicators) is at least 3:1 against adjacent colors
- [ ] Color is not the sole means of conveying information (error states, status indicators, chart data)
- [ ] Text can be resized to 200% without loss of content or functionality
- [ ] Video content has captions; audio content has transcripts
- [ ] Content is usable in both portrait and landscape orientations

### F2. Operable

- [ ] All functionality is available via keyboard alone (no mouse-only interactions)
- [ ] No keyboard traps exist — users can Tab away from every interactive element
- [ ] Skip navigation link is provided as the first focusable element
- [ ] Focus order follows a logical sequence that matches visual layout
- [ ] Focus indicator is visible and high-contrast (at least 2px outline, 3:1 contrast ratio)
- [ ] Touch targets are at least 44x44 CSS pixels with at least 8px spacing between targets
- [ ] No content flashes more than 3 times per second
- [ ] Time-limited interactions provide sufficient time or allow extension
- [ ] Drag-and-drop interactions have keyboard-accessible alternatives

### F3. Understandable

- [ ] Page language is declared in HTML (`<html lang="en">` or appropriate language code)
- [ ] Form labels are programmatically associated with inputs (label for/id or aria-labelledby)
- [ ] Error messages identify the field in error and suggest how to fix it
- [ ] Navigation is consistent across pages (same items in the same order)
- [ ] Help text or instructions are provided for complex or unusual inputs
- [ ] Abbreviations and technical terms are explained on first use or via glossary

### F4. Robust

- [ ] HTML is valid and semantic (proper heading hierarchy h1-h6, no skipped levels)
- [ ] ARIA attributes are used correctly (roles, states, properties match actual behavior)
- [ ] Dynamic content changes are announced to screen readers (aria-live regions)
- [ ] Custom interactive components have appropriate ARIA roles and keyboard behavior
- [ ] Status messages (success, error, progress) are announced without moving focus (role="status" or aria-live="polite")
- [ ] The interface works with major screen readers (VoiceOver, NVDA, JAWS)

---

## G. Mobile and Responsive Design

### G1. Layout and Adaptation

- [ ] No horizontal scrolling occurs at any standard breakpoint (320px through 1440px+)
- [ ] Layout adapts gracefully across breakpoints: mobile (320-480px), tablet (481-768px), laptop (769-1024px), desktop (1025-1440px)
- [ ] Content stacking on mobile follows a logical priority order (not just desktop columns stacked arbitrarily)
- [ ] Fluid grids use relative units (%, rem, vw) rather than fixed pixel widths
- [ ] Images are responsive (srcset or max-width: 100%) and do not crop critical content

### G2. Touch Interaction

- [ ] Touch targets are at least 44x44px with at least 8px gap between adjacent targets
- [ ] Primary actions are positioned in thumb-reachable zones (bottom half of the screen for mobile)
- [ ] Swipe gestures have button alternatives (swipe-to-delete also has a delete button)
- [ ] No hover-dependent interactions without a touch/tap equivalent
- [ ] Pull-to-refresh or equivalent reload mechanism is available where appropriate

### G3. Mobile-Specific Patterns

- [ ] Mobile navigation uses an appropriate pattern (hamburger menu, bottom tab bar, or drawer)
- [ ] Inputs trigger the correct mobile keyboard (numeric keypad for numbers, email keyboard for email)
- [ ] Modals and dialogs are properly sized and dismissible on mobile (no overflow, can scroll within)
- [ ] Tables transform to a readable format on mobile (card view, horizontal scroll with frozen column, or collapsible rows)
- [ ] All features available on desktop are accessible on mobile (no desktop-only functionality)

---

## H. Error Handling

### H1. Error Prevention

- [ ] Input constraints prevent invalid data entry (disabled dates in date picker, character limits)
- [ ] Destructive actions require explicit confirmation (delete, cancel subscription, revoke access)
- [ ] High-stakes destructive actions require typing the resource name to confirm
- [ ] Smart defaults reduce the likelihood of user error
- [ ] Disabled states are used for unavailable actions with explanation of why they are disabled

### H2. Error Messages

- [ ] Error messages are written in plain language (no error codes, stack traces, or technical jargon)
- [ ] Error messages are specific about what went wrong ("Password must be at least 8 characters" not "Invalid password")
- [ ] Error messages suggest a corrective action or next step
- [ ] Error messages appear in context (next to the field or action that caused the error)
- [ ] System errors (500, timeouts) have a user-friendly error page with retry option and support contact

### H3. Error Recovery

- [ ] Undo is available for reversible actions (with toast notification and 5-10 second timer)
- [ ] Soft delete (trash/archive) is used instead of hard delete where possible
- [ ] Form data is not lost when a submission error occurs
- [ ] Session timeout is handled gracefully (warning before timeout, data preserved on re-login)
- [ ] Network errors trigger automatic retry with user notification
- [ ] 404 pages include navigation options and search to help users find what they were looking for

---

## I. Loading States and Feedback

### I1. System Status Visibility

- [ ] Every user action produces visible feedback within 100ms (button press state, loading indicator)
- [ ] Operations taking more than 1 second show a loading indicator (spinner, progress bar, or skeleton)
- [ ] Operations taking more than 10 seconds show progress indication (percentage, items processed, or estimated time)
- [ ] Background operations (file upload, data export) show progress and allow the user to continue other tasks
- [ ] System status is visible at all times (connection status, sync status, save status)

### I2. Loading Patterns

- [ ] Skeleton screens are used for initial page loads and content areas (not blank space or only spinners)
- [ ] Skeleton layouts match the dimensions of the content they replace (preventing layout shift)
- [ ] Loading states are used for individual components, not just full-page loaders
- [ ] Cached or stale data is shown immediately while fresh data loads in the background (stale-while-revalidate)
- [ ] Infinite scroll or pagination handles the loading of additional content smoothly

### I3. Success and Confirmation Feedback

- [ ] Save operations produce visible confirmation (toast notification, inline checkmark, or status text)
- [ ] Toast notifications persist for at least 4 seconds (or until manually dismissed)
- [ ] Toast notifications do not obscure important content or interactive elements
- [ ] Completed multi-step processes show a summary/confirmation screen
- [ ] Email or notification confirmations are sent for significant account actions

---

## J. Conversion Optimization (Landing Pages)

### J1. Hero and Value Proposition

- [ ] Headline communicates a clear benefit in under 12 words
- [ ] Subheadline expands on the headline with specifics or a quantifiable claim
- [ ] The hero answers three questions within 3 seconds: What is this? Why should I care? What do I do next?
- [ ] Exactly one primary CTA button is present in the hero section
- [ ] CTA text is action-oriented and specific ("Start your free trial" not "Learn more")
- [ ] Hero section is fully visible without scrolling on a 1280x800 viewport

### J2. Social Proof

- [ ] Logo bar of recognizable customers appears within the first 2 viewport heights
- [ ] Testimonials include name, role, company, and ideally a photo
- [ ] At least one testimonial or metric includes a specific, quantified result
- [ ] Third-party review badges (G2, Capterra, etc.) link to actual review profiles
- [ ] Social proof appears before the pricing section in the page flow

### J3. Pricing and Conversion

- [ ] Pricing page displays 2-4 tiers (no more, to avoid decision fatigue)
- [ ] One plan is visually highlighted as recommended ("Most Popular" badge, color emphasis)
- [ ] Monthly/annual toggle is present with savings percentage shown
- [ ] Each plan has its own CTA button
- [ ] Feature comparison shows at least 5 differentiating features between plans
- [ ] FAQ section addresses common pricing objections (cancellation, what counts as a user, upgrades)

### J4. Trust and Friction Reduction

- [ ] Trust signals (security badges, "no credit card required", privacy assurance) appear near the CTA/form
- [ ] Initial conversion form requires 3 or fewer fields
- [ ] CTA button has at least 3:1 contrast ratio with its background
- [ ] CTA button meets minimum touch target size (44x44px)
- [ ] CTA is repeated at least 2-3 times on long-scroll pages
- [ ] Page has a single primary conversion goal (no competing navigation or distracting links)

### J5. Page Performance for Conversion

- [ ] Page Largest Contentful Paint (LCP) is under 2.5 seconds
- [ ] Page Cumulative Layout Shift (CLS) is under 0.1
- [ ] Content is scannable: short paragraphs, bullet points, subheadings throughout
- [ ] Mobile viewport has tap-friendly targets (at least 44px) and properly sized text (at least 16px)
- [ ] No dark patterns are used (confirmshaming, fake urgency, hidden costs, misdirection)
