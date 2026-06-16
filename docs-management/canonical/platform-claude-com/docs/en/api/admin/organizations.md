---
source_url: https://platform.claude.com/docs/en/api/admin/organizations
source_type: sitemap
content_hash: sha256:30bb81a5770079e13d84552647fec9963b8ad8fe87bc5a42101d098031f96052
sitemap_url: https://platform.claude.com/sitemap.xml
fetch_method: markdown
---

# Organizations

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

## Domain Types

### Organization

- `Organization = object { id, name, type }`

  - `id: string`

    ID of the Organization.

  - `name: string`

    Name of the Organization.

  - `type: "organization"`

    Object type.

    For Organizations, this is always `"organization"`.

    - `"organization"`
