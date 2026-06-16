# Role-Based Access Control UI -- Complete Reference

> Comprehensive guide to role-based access control presentation in admin portals. Covers display strategies (show/hide/disable/read-only), permission granularity, graceful access denial, role indicators, context switching, audit log design, and user management interfaces. All patterns include specific measurements, real-world examples, and checkable audit items.

---

## 1. RBAC Display Strategies

### Core Principle

Frontend role-based access control is about **user experience, not security**. Security enforcement must always happen on the backend. The frontend adapts the interface to reduce confusion, prevent frustration, and guide users toward actions they are permitted to take.

### Strategy Decision Tree

Choose the display strategy based on the user's relationship to the feature:

| Strategy | When to Use | Implementation | Example |
|----------|-------------|----------------|---------|
| **Hide** the element entirely | Feature is irrelevant to the role; the user has no reason to know it exists | Do not render the component; remove the navigation item | Hide "User Management" nav item for non-admin roles |
| **Disable** the element | User should know the feature exists but currently lacks permission; upgrade path is relevant | Render the element grayed out with `aria-disabled="true"`; show a tooltip explaining why | Grey out "Publish" button for users with editor-only permissions |
| **Show read-only** | User needs to see the data but must not modify it | Render content without edit controls; hide edit/save/delete buttons | Display system settings as informational text for viewer roles |
| **Redirect** to access-denied page | User navigates directly to a protected route via URL | Intercept at the route level; redirect to a clear 403 page | User types a URL for admin settings they cannot access |

### When to Hide vs. Disable

The choice between hiding and disabling depends on the purpose of the feature's visibility:

| Context | Approach | Rationale |
|---------|----------|-----------|
| Feature is only for specific roles and irrelevant to others | **Hide** | Reduces noise; simpler interface |
| Feature exists across all roles but requires upgrade or approval | **Disable with tooltip** | Drives awareness and upgrade conversion |
| Feature is temporarily unavailable (maintenance, usage limit) | **Disable with explanation** | Sets expectation that functionality will return |
| Feature is visible for audit or compliance (users must see what exists) | **Show read-only** | Transparency requirements |

### Implementation Patterns

#### Route Guards

Protect entire pages at the routing level:

- Use framework-specific route guards (Angular guards, React higher-order components, Next.js middleware, Vue navigation guards) to check permissions before rendering a page.
- If the user lacks access, redirect to a meaningful access-denied page (not a blank page or generic 403).
- Log unauthorized access attempts for security auditing.

#### Permission-Aware Components

Conditionally render UI elements based on permission strings:

- Wrap permission-dependent UI in a component like `<CanAccess permission="users:delete">` that checks the user's permissions and renders children only if permitted.
- Centralize permission checking logic to ensure consistent enforcement across the application.
- Use a permission context provider or store that hydrates on login and refreshes on role changes.

#### Permission Caching

- Cache permissions on the client after login for immediate UI rendering.
- Refresh permissions from the server on navigation to critical pages, role changes, or at regular intervals (every 5-15 minutes).
- Handle stale permission caches gracefully: if the server rejects an action due to revoked permission, update the local cache and adjust the UI immediately.

### RBAC Display Strategy Audit Checklist

- [ ] Unauthorized features are hidden (not disabled) when irrelevant to the role
- [ ] Upgrade-path features are disabled with explanatory tooltips
- [ ] Disabled elements use `aria-disabled="true"` and remove click handlers
- [ ] Tooltips on disabled elements explain why the action is unavailable and how to gain access
- [ ] Read-only views remove all edit/save/delete controls
- [ ] Route guards protect all protected pages
- [ ] Unauthorized route access redirects to a meaningful access-denied page (not generic 403)
- [ ] Permission-aware components are used for element-level visibility
- [ ] Permission checking is centralized (single source of truth)
- [ ] Permissions are cached client-side and refreshed on role changes

---

## 2. Permission Granularity

### Permission Structure

Structure permissions as `resource:action` pairs. This model scales cleanly and maps directly to UI elements.

| Resource | Actions | UI Mapping |
|----------|---------|-----------|
| `users` | `create`, `read`, `update`, `delete` | User management table, create form, edit panel, delete button |
| `posts` | `create`, `read`, `update`, `delete`, `publish` | Content table, editor, publish button |
| `settings` | `read`, `update` | Settings page (read-only vs. editable) |
| `billing` | `read`, `update` | Billing page visibility and edit controls |
| `reports` | `read`, `export` | Report viewing and export button |
| `roles` | `create`, `read`, `update`, `delete` | Role management interface |

### Ownership-Based Permissions

Some permissions depend on whether the user owns the resource:

| Permission | Scope | UI Behavior |
|-----------|-------|-------------|
| `posts:update:own` | Only the user's own posts | Show Edit button only on posts the user created |
| `posts:update:all` | All posts regardless of author | Show Edit button on every post |
| `posts:delete:own` | Only the user's own posts | Show Delete button only on posts the user created |
| `posts:delete:all` | All posts | Show Delete button on every post |

- Evaluate ownership permissions at the component level, not just the route level.
- For tables, check ownership per row and render action buttons conditionally.
- The backend must also enforce ownership checks -- never rely on frontend-only enforcement.

### Role Hierarchy

Define clear role hierarchies where higher roles inherit all permissions of lower roles:

| Role Level | Example Role | Inherits From | Additional Permissions |
|-----------|-------------|---------------|----------------------|
| 1 (lowest) | Viewer | None | Read access to assigned resources |
| 2 | Editor | Viewer | Create, update own resources |
| 3 | Manager | Editor | Update/delete all resources in their team, manage team members |
| 4 | Admin | Manager | Full CRUD on all resources, manage roles, manage billing |
| 5 (highest) | Super Admin | Admin | System configuration, impersonation, audit log access |

### Permission Granularity Audit Checklist

- [ ] Permissions follow the `resource:action` naming convention
- [ ] Permissions cover CRUD operations per resource (create, read, update, delete)
- [ ] Special actions beyond CRUD are defined where needed (publish, export, approve)
- [ ] Ownership-based permissions are evaluated per record, not just per page
- [ ] Role hierarchy is clearly defined with inheritance
- [ ] Frontend permission checks are duplicated on the backend (defense in depth)
- [ ] Permission strings are documented and maintainable
- [ ] New features include permission definitions as part of the design specification

---

## 3. Graceful Access Denial

### Access-Denied Page Design

When a user navigates to a URL they lack access to, never show a blank page, a raw HTTP 403, or a generic "Forbidden" message. Design a helpful access-denied page:

**Required elements:**

1. **Clear heading**: "You don't have access to this page" (not "403 Forbidden" or "Error").
2. **Explanation**: Brief description of why access is denied: "This page requires Admin permissions."
3. **Current role indicator**: Show the user's current role: "Your current role: Editor."
4. **Resolution path**: Provide specific guidance on how to gain access:
   - "Contact your organization admin to request access."
   - "Upgrade your plan to access this feature." (with upgrade CTA)
   - "Switch to a different organization that has access."
5. **Navigation options**: Link back to the dashboard or the previous page.
6. **Support contact**: Link to support or help documentation.

### Mid-Session Permission Revocation

Handle the scenario where a user's permissions change while they are actively using the application:

- If a permission is revoked mid-session, do not crash or show a blank screen.
- On the next server interaction that returns a 403, show an inline notification: "Your permissions have been updated. Some actions may no longer be available."
- Refresh the permission cache and update the UI to reflect new permissions immediately.
- If the user is on a page they no longer have access to, show the access-denied state inline (not a redirect) so they do not lose context.
- For real-time applications, use WebSocket or server-sent events to push permission changes to the client immediately.

### Contextual Denial Within Pages

When a user has access to a page but lacks permission for a specific action on that page:

- Do not show a full access-denied page. Instead, show an inline message near the disabled control.
- Use a tooltip or inline text: "You need Editor permissions to modify this field."
- For form submissions that fail due to permissions, show an inline error: "You don't have permission to perform this action. Contact your admin."

### Access Denial Audit Checklist

- [ ] Access-denied page has a clear, plain-language heading (not "403" or "Forbidden")
- [ ] Access-denied page explains why access is denied
- [ ] Access-denied page shows the user's current role
- [ ] Access-denied page provides a resolution path (contact admin, upgrade, switch org)
- [ ] Access-denied page includes navigation back to dashboard or previous page
- [ ] Access-denied page includes support/help links
- [ ] Mid-session permission revocation is handled gracefully (no crash or blank screen)
- [ ] Permission cache refreshes on 403 responses
- [ ] UI updates immediately when permissions change
- [ ] Contextual denial uses inline messages near disabled controls (not full-page redirects)

---

## 4. Role Indicators and Context Switching

### Role Indicators

- Display the user's current role in the user profile area (header, sidebar footer, or avatar dropdown).
- Use a role badge next to the user's name: a small colored label showing "Admin", "Editor", "Viewer."
- In multi-tenant systems, also display the current organization/tenant name prominently.
- Provide a link from the role indicator to a "My permissions" page where the user can see what their role allows.

### Role Badge Design

| Element | Specification |
|---------|---------------|
| Size | 20-24px height, horizontal padding 8px |
| Typography | 11-12px, semibold, uppercase or small caps |
| Color | Distinct color per role level (e.g., blue for Admin, green for Editor, gray for Viewer) |
| Position | Right of username in header, or below username in sidebar footer |
| Accessibility | Include `aria-label="Role: Admin"` for screen readers |

### Context Switching

For users who belong to multiple organizations or hold multiple roles:

- Provide a context switcher in the top-left area (header or sidebar top).
- Show the current organization name and role with a dropdown to switch.
- On switching context, reload the relevant data and update the UI immediately. Do not require logout/login.
- Show a brief confirmation: "Switched to Organization: Acme Corp (Admin)."
- Persist the last-used context so the user returns to it on next login.
- Style the context switcher prominently enough that users do not forget which context they are operating in.

### Context Switching Safety

- Before switching context, warn the user if they have unsaved changes: "You have unsaved changes. Switch anyway?"
- Clearly differentiate the visual appearance of different contexts (e.g., different accent color per organization) to prevent accidental actions in the wrong context.
- In audit-sensitive environments, log every context switch with timestamp and source/target context.

### Role Indicator Audit Checklist

- [ ] User's current role is displayed in the profile/header area
- [ ] Role badge uses distinct colors per role level
- [ ] Role badge meets accessibility requirements (`aria-label`)
- [ ] "My permissions" page is accessible from the role indicator
- [ ] Organization/tenant name is displayed in multi-tenant systems
- [ ] Context switcher is available for multi-org users
- [ ] Context switch does not require logout/login
- [ ] Context switch confirmation is displayed after switching
- [ ] Last-used context persists across sessions
- [ ] Unsaved changes warning appears before context switch
- [ ] Visual differentiation exists between different organization contexts

---

## 5. Audit Logs

### Purpose

Audit logs answer four questions: **Who** did **what**, **when**, and to **which resource**. They are critical for compliance (SOC 2, GDPR, HIPAA), debugging, and accountability.

### Data Fields

Each audit log entry must capture and display:

| Field | Display Format | Notes |
|-------|---------------|-------|
| **Timestamp** | Relative for recent ("2 min ago"), absolute for older ("Jan 15, 2026 14:32 UTC") | Show in user's local timezone with UTC tooltip |
| **Actor** | Avatar + name + email | Include system/automated actions with a "System" actor |
| **Action** | Human-readable verb | Created, Updated, Deleted, Exported, Logged in, Permission changed, Invited, Archived |
| **Resource** | Resource type + name/ID | "User: jane@example.com", "Project: Alpha", "Setting: Notification preferences" |
| **Changes (diff)** | Before/after values | For updates, show field name + old value + new value |
| **IP address** | Available on expand | For security audits |
| **User agent** | Available on expand | Browser/device info for security |
| **Request ID** | Available on expand | For cross-system tracing |

### Log Layout

Use a **timeline/activity feed layout** as the primary view:

- Each entry is a single row: `[Avatar] [Actor name] [action description] [resource] [timestamp]`
- Example: `[JD] Jane Doe updated User 'john@example.com' -- 2 minutes ago`
- Make rows **expandable** to reveal the full change diff, IP address, user agent, and request ID.
- Show a **"Changes" badge** on entries with field-level diffs: "3 fields changed."

### Change Diff Display

For update actions, show a structured diff:

| Field | Previous Value | New Value |
|-------|---------------|-----------|
| Role | Editor | Admin |
| Status | Active | Inactive |
| Email | old@example.com | new@example.com |

- Use **red background with strikethrough** for removed/old values.
- Use **green background** for new values.
- Apply **syntax highlighting** for JSON payloads in API-related changes.

### Filtering and Search

Audit logs require robust filtering because they grow continuously:

- **Date range**: Date picker with presets (Today, Last 7 days, Last 30 days, Custom range).
- **Actor**: Searchable dropdown of all users who have performed actions.
- **Action type**: Multi-select checkbox list (Created, Updated, Deleted, etc.).
- **Resource type**: Multi-select (Users, Projects, Settings, etc.).
- **Resource ID**: Text input for searching a specific resource.
- **Full-text search**: Search across action descriptions and resource names.
- Show active filters as removable chips above the log.

### Export

- Support **CSV and JSON export** of filtered audit log data for compliance reporting.
- Respect current filters and date range in the export (do not export all data by default).
- For large exports, use background processing with a download notification when ready.

### Pagination

- Use pagination for audit logs (not infinite scroll). Admin users need to reference specific time periods.
- Show 25-50 entries per page by default.
- Display total entry count: "Showing 1-50 of 12,847 entries."

### Audit Log Audit Checklist

- [ ] Each log entry captures: timestamp, actor, action, resource, and changes
- [ ] Timestamps display in the user's local timezone with UTC tooltip
- [ ] Recent timestamps use relative format ("2 min ago"); older use absolute
- [ ] Actor information includes avatar, name, and email
- [ ] System/automated actions are attributed to a "System" actor
- [ ] Action verbs are human-readable (Created, Updated, Deleted)
- [ ] Resource entries include type and name/ID
- [ ] Entries are expandable to reveal full diff, IP, user agent, and request ID
- [ ] Update entries show before/after diff with color coding (red old, green new)
- [ ] "Changes" badge shows the count of modified fields
- [ ] Date range filter with presets is available
- [ ] Actor filter with searchable dropdown is available
- [ ] Action type and resource type multi-select filters are available
- [ ] Full-text search is available across descriptions and resource names
- [ ] Active filters display as removable chips
- [ ] CSV and JSON export is available, respecting current filters
- [ ] Pagination with total entry count is implemented

---

## 6. User Management Interfaces

### User List Table

Display a data table with these columns:

| Column | Type | Notes |
|--------|------|-------|
| Checkbox | Selection | For bulk actions |
| Avatar | Image / Initials | Fallback: first+last initial with deterministic background color |
| Name | Text (primary identifier) | Clickable, links to user detail |
| Email | Text | Copyable on click |
| Role(s) | Badge(s) | Color-coded per role |
| Status | Badge | Active (green), Inactive (gray), Invited (yellow), Suspended (red) |
| Last active | Relative timestamp | "2 hours ago", "3 days ago", "Never" |
| Date created | Date | Absolute date |
| Actions | Buttons/overflow | Edit, Deactivate/Activate, Reset Password, Delete |

### Quick Actions Per Row

- **Edit**: Opens side panel or navigates to edit page.
- **Activate / Deactivate**: Toggle with confirmation: "Deactivate user Jane Doe? They will lose access immediately."
- **Reset Password**: Sends a password reset link. Confirm: "Send a password reset email to jane@example.com?"
- **Delete**: Requires confirmation with cascade impact: "Delete user Jane Doe? This will remove their access and reassign 12 owned projects."

### Bulk User Actions

Support these bulk operations when multiple users are selected:

- **Assign role**: Apply a role change to all selected users.
- **Activate / Deactivate**: Toggle status for all selected users.
- **Delete**: With confirmation showing exact count and cascade impact.
- **Export**: Export selected user data to CSV.

Show the contextual action bar with selection count: "4 users selected."

### User Detail Page

Organize the user detail page into tabbed or sectioned areas:

| Section | Contents |
|---------|----------|
| **Profile** | Name, email, avatar, bio, phone, timezone, language preference |
| **Roles & Permissions** | Assigned roles, effective permissions summary (inherited + direct), role change controls |
| **Security** | Password (last changed date), 2FA status (enabled/disabled), active sessions with revoke option, login history |
| **Activity** | Recent audit log entries filtered to this user's actions |
| **Teams / Groups** | Team memberships, group assignments |

### Effective Permissions View

Show a consolidated view of all permissions the user has, across all their roles:

- List each resource with its permitted actions: `users: read, update (own) | posts: create, read, update, delete, publish`
- Indicate which role each permission comes from: "Via: Admin role" or "Via: Direct assignment."
- Highlight any conflicting or overlapping permissions.
- Show this as a reference view (read-only) to help admins understand the full permission picture.

### User Invitation Flow

- Provide a **multi-email input** for batch invitations. Accept comma-separated or line-separated email addresses.
- Allow **role pre-assignment** during invitation: select the role each invitee will receive.
- Show **invitation status tracking**: Pending, Accepted, Expired.
- Support **resend invitation** for pending invitations.
- Set invitation expiration (e.g., 7 days) with the option to extend or revoke.
- Send a welcome email with a clear CTA: "Accept invitation and set up your account."

### Impersonation (Super Admin)

For super-admin users who need to see the product from another user's perspective:

- Provide an "Impersonate" button on the user detail page (visible only to super admins).
- When impersonating, show a **persistent top banner**: "You are impersonating Jane Doe (Editor). [Stop impersonating]" in a distinct color (e.g., yellow or orange background).
- Log all impersonation sessions in the audit log: who impersonated whom, start time, end time.
- Restrict impersonation to read-only actions or clearly log all actions taken during impersonation.
- Ensure the impersonation banner cannot be dismissed and remains visible on every page.

### User Management Audit Checklist

- [ ] User list table includes: avatar, name, email, role(s), status, last active, date created, actions
- [ ] User name is clickable and links to the user detail page
- [ ] Email is copyable on click
- [ ] Role badges are color-coded per role level
- [ ] Status badges use semantic colors (green/active, gray/inactive, yellow/invited, red/suspended)
- [ ] Quick actions per row include: Edit, Activate/Deactivate, Reset Password, Delete
- [ ] Deactivation confirmation warns about immediate access loss
- [ ] Delete confirmation shows cascade impact (owned resources)
- [ ] Bulk user actions are available: assign role, activate/deactivate, delete, export
- [ ] Contextual action bar shows selection count
- [ ] User detail page has sections: Profile, Roles & Permissions, Security, Activity, Teams
- [ ] Effective permissions view shows all permissions with source role
- [ ] Active sessions are listed with revoke capability
- [ ] Login history is available in the security section
- [ ] Multi-email invitation input is supported for batch invites
- [ ] Role pre-assignment is available during invitation
- [ ] Invitation status tracking shows Pending, Accepted, Expired
- [ ] Resend invitation is available for pending invitations
- [ ] Impersonation is available for super admins with a persistent banner
- [ ] Impersonation sessions are logged in the audit trail
- [ ] Impersonation banner cannot be dismissed and is visible on every page

---

## 7. Role-Based Dashboard Adaptation

### Role-Appropriate Default Views

Tailor the default dashboard view to each role's needs:

| Role | Default Dashboard Content | Rationale |
|------|--------------------------|-----------|
| **Super Admin** | System health, total users, active sessions, error rates, storage usage | System-wide operational visibility |
| **Admin** | Organization metrics, team activity, pending approvals, recent user signups | Organization management focus |
| **Manager** | Team metrics, team member activity, task completion rates, pending reviews | Team oversight focus |
| **Editor** | Own content stats, published items, draft items, assigned tasks | Personal productivity focus |
| **Viewer** | Shared reports, dashboards assigned to them, bookmarked items | Consumption-focused view |

### Navigation Filtering

- Filter sidebar navigation items based on the user's role and permissions.
- Hide entire navigation sections that the user has no access to.
- If a navigation section has only one accessible sub-item, show it as a direct link rather than an expandable section.
- Show a maximum of 5-7 primary navigation items per role to prevent cognitive overload.

### Feature Gating

- For features that require a higher plan or role, show a preview state: a blurred or skeleton version of the feature with an overlay message: "Upgrade to Pro to access advanced analytics."
- Include a clear CTA: "Upgrade now" or "Contact your admin."
- Never show a fully functional-looking feature and then block the user when they try to use it (bait and switch).

### Role-Based Adaptation Audit Checklist

- [ ] Default dashboard content is tailored to each role
- [ ] Navigation items are filtered based on role and permissions
- [ ] Empty navigation sections are hidden entirely
- [ ] Primary navigation shows 5-7 items maximum per role
- [ ] Upgrade-path features show a preview with a clear upgrade CTA
- [ ] Feature previews do not mislead users into thinking functionality is available
- [ ] Role-appropriate empty states guide users toward permitted actions
