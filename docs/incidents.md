# Incident publishing

[← Repository overview](../README.md)

Incident posts are public customer communications. Publish only confirmed facts,
describe the customer impact, and keep credentials, internal hostnames, account
identifiers, and personal information out of the post.

## Start an incident

Create a Markdown file in `content/issues/` with a descriptive name, such as
`2026-10-16-billing-delays.md`. Use the incident's actual start time in UTC.

The following is an example only; replace its dates, impact, and update time:

```yaml
---
title: Delays opening invoices
date: '2026-10-16T18:00:00Z'
resolved: false
severity: disrupted
affected:
  - Billing
section: issue
---

We are investigating delays when opening invoices. Sign-in and other account
features remain available.

Next update: October 16, 2026 at 18:30 UTC.
```

Use exact component names from `config.yml`. List only affected components;
an incident affecting Billing should not mark Portal or Sign-in as unavailable
if they still work.

| Front matter | When to use it |
| --- | --- |
| `severity: notice` | Maintenance or another service notice |
| `severity: disrupted` | Degraded service or partial availability |
| `severity: down` | An outage affecting the listed components |
| `resolved: false` | The incident or maintenance is still active |
| `resolved: true` | Service has recovered or maintenance has ended |
| `resolvedWhen` | Actual recovery time, required by the publishing process when resolving |

`buildFuture` is enabled. A future-dated post with `resolved: false` can affect
current status as soon as it is deployed. Do not assume its date schedules
activation. Review planned-maintenance behavior in preview before publishing.

## Keep customers informed

Add timestamped updates in the body with the latest known impact and the next
update time. Distinguish investigation, mitigation, and recovery; do not claim a
root cause or full recovery before it is confirmed.

For example:

```markdown
### Update — October 16, 2026 at 18:20 UTC

Invoice access is recovering after a mitigation. We are checking for remaining
delays and will update this post by 18:45 UTC.
```

Use explicit UTC timestamps consistently. Avoid exposing internal logs or naming
an affected customer without permission.

## Resolve the incident

Set `resolved: true`, add `resolvedWhen` using the actual recovery time, and add
a closing update in the body. Keep the original start date and affected components.
The resolution time must not precede the start time.

```yaml
resolved: true
resolvedWhen: '2026-10-16T18:40:00Z'
```

Keep resolved posts in the history. The empty launch history is a one-time reset,
not the normal incident retention process.

## Validate and publish

Run the checks below, review the change in a pull request, and inspect its preview:

```sh
python3 scripts/validate_status.py
hugo --environment production --gc --minify
python3 scripts/check_rendered_site.py public
```

Confirm the affected component, group summary, incident text, timestamps, and
resolved state. Follow the [production settings](production-checks.md) before
merging. The merge to `master` triggers Cloudflare Pages production publishing;
a local build or successful CI run does not publish the incident by itself.
