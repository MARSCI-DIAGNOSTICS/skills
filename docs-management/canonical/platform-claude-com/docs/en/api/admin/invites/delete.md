---
source_url: https://platform.claude.com/docs/en/api/admin/invites/delete
source_type: sitemap
content_hash: sha256:17e962d49b249dcf0fcecf40c329a5a5afa77acc8aa0dbb2d2b20a609c883490
sitemap_url: https://platform.claude.com/sitemap.xml
fetch_method: markdown
---

## Delete

**delete** `/v1/organizations/invites/{invite_id}`

Delete Invite

### Path Parameters

- `invite_id: string`

  ID of the Invite.

### Returns

- `id: string`

  ID of the Invite.

- `type: "invite_deleted"`

  Deleted object type.

  For Invites, this is always `"invite_deleted"`.

  - `"invite_deleted"`
