---
source_url: https://platform.claude.com/docs/en/api/admin/users/update
source_type: sitemap
content_hash: sha256:f9d2cc9bcfea6555f14766fb0ff677b3680c8f4b55b1ecd8df00812a6eb6ef89
sitemap_url: https://platform.claude.com/sitemap.xml
fetch_method: markdown
---

## Update

**post** `/v1/organizations/users/{user_id}`

Update User

### Path Parameters

- `user_id: string`

  ID of the User.

### Body Parameters

- `role: "user" or "developer" or "billing" or 2 more`

  New role for the User. Cannot be "admin".

  - `"user"`

  - `"developer"`

  - `"billing"`

  - `"claude_code_user"`

  - `"managed"`

### Returns

- `User = object { id, added_at, email, 3 more }`

  - `id: string`

    ID of the User.

  - `added_at: string`

    RFC 3339 datetime string indicating when the User joined the Organization.

  - `email: string`

    Email of the User.

  - `name: string`

    Name of the User.

  - `role: "user" or "developer" or "billing" or 3 more`

    Organization role of the User.

    - `"user"`

    - `"developer"`

    - `"billing"`

    - `"admin"`

    - `"claude_code_user"`

    - `"managed"`

  - `type: "user"`

    Object type.

    For Users, this is always `"user"`.

    - `"user"`
