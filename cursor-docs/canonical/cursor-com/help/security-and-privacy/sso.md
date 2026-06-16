---
source_url: https://cursor.com/help/security-and-privacy/sso
source_type: llms-txt
content_hash: sha256:b81ef23bfeebd20d9a1021c8c0a8d4e4c08b298ffa9b7802941daa978549ebe2
sitemap_url: https://cursor.com/llms.txt
fetch_method: markdown
---

# SSO and authentication

SSO with SAML 2.0 is available at no additional cost on Teams and Enterprise plans.

## What do I need before setting up SSO?

- A Cursor Teams or Enterprise plan
- Admin access to your identity provider (e.g., Okta, Azure AD, Google Workspace)
- Admin access to your Cursor organization

## How do I set up SSO?

Follow the step-by-step guide in the [SSO setup reference](https://cursor.com/docs/account/teams/sso.md). You'll need admin access to both your identity provider and your Cursor organization.

## Does Cursor support SCIM provisioning?

Yes, on Enterprise plans with SSO enabled. SCIM automatically manages team members through your identity provider, keeping your Cursor team in sync with your organization.

## Why do team members see "Not assigned to this application"?

This means the team member hasn't been assigned to the Cursor application in your identity provider's admin console. Add them to the Cursor app in your IdP to fix this.

## Related

- [SSO reference](https://cursor.com/docs/account/teams/sso.md)
- [Set up a team](https://cursor.com/help/account-and-billing/teams-setup.md)


---

## Sitemap

[Overview of all docs pages](/llms.txt)
