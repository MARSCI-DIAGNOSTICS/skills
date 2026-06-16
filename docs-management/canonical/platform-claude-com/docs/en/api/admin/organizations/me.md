---
source_url: https://platform.claude.com/docs/en/api/admin/organizations/me
source_type: sitemap
content_hash: sha256:0f7eba6d67fb306efec9878cddabcb3fcc29eab07b6ebfb9edbabd19b5389b5a
sitemap_url: https://platform.claude.com/sitemap.xml
fetch_method: markdown
---

## Me

**get** `/v1/organizations/me`

Retrieve information about the organization associated with the authenticated API key.

### Returns

- `Organization = object { id, name, type }`

  - `id: string`

    ID of the Organization.

  - `name: string`

    Name of the Organization.

  - `type: "organization"`

    Object type.

    For Organizations, this is always `"organization"`.

    - `"organization"`
