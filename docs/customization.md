# Site customization

[← Repository overview](../README.md)

Keep the status page centered on services customers recognize. Explain affected
infrastructure in incident details rather than exposing it as extra components.

## Services and component pages

Edit `params.categories` and `params.systems` in `config.yml`. Keep names short,
descriptions specific, and categories in the intended display order. The
`closed: true` setting collapses a group by default.

For each new component, create `content/affected/<slug>/_index.md` using an existing
component file as the model. Its title must match the configured component name.
Explicit pages keep detail links available before the first incident.

When renaming a component, review its term page and existing incidents together.
Changing a configured name without updating references can break validation or
split incident history. Confirm that a component is actually offered before
adding it to the public inventory.

## Branding and interface text

| Change | Location |
| --- | --- |
| Page title, description, logo, colors, and date formatting | `config.yml` |
| Group summaries and component presentation | `layouts/partials/index/components.html` |
| English interface wording | `i18n/en.yaml` |
| Logo and other public assets | `static/` |

Prefer small overrides in `layouts/` to editing `themes/cstate/` directly. The
theme is a Git submodule; review its update diff and rerun the production checks
when advancing its pinned commit.

## Public files and security contact

Hugo copies `static/` into the published site without treating its files as
private. Do not store secrets, internal-only documents, or customer data there.

Keep `static/.well-known/security.txt` and `static/security.txt` identical. Verify
the contact mailbox and policy link, and renew `Expires` before April 16, 2027.
If the domain changes, update `baseURL`, both `Canonical` fields, the README,
and the security policy together.

The files in `netlify/`, `.gitlab-ci.yml`, and `vercel.json` are inherited hosting
configuration. They do not define the active Cloudflare Pages deployment. Do
not follow those providers' instructions when configuring this production site.

## Review the result

Check desktop and mobile layouts, category expansion, component detail links,
incident severity, and dark mode. Keep the cState attribution and upstream
license. Use [Production checks](production-checks.md) for build and validation
commands and the required GitHub/Cloudflare settings.
