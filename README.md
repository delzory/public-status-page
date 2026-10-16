# Delzory Status

Public customer-service status page built with [cState](https://github.com/cstate/cstate).
The configured components live in `config.yml`; incident posts live in `content/issues/`.

## Public components

| Component | Report problems with |
| --- | --- |
| Delzory Website | Delzory.com and its public information pages |
| Customer Portal | Sign-in, account settings, and service management |
| Customer Sites | Customer sites, managed domains, and certificates |
| Billing & Payments | Invoices, payments, and subscriptions |
| Support Requests | Ability to submit general or urgent support requests |
| Service Notifications | Delivery of account emails and service alerts |

Keep the page focused on services customers can recognize. Describe affected
infrastructure (for example DNS, authentication, a processing queue, or a
regional cluster) in the incident details, and list each affected public
component by its exact configured name. For example, a billing outage should
not mark the Customer Portal as down if sign-in and service management still
work. Support Requests describes the availability of contact channels, not
how quickly a person replies. Service Notifications does not imply hosted
mailbox service.

Only list services that are actually offered and can receive incident updates.
The publicly indexed Delzory homepage shows a maintenance notice, and the
repository alone cannot confirm whether the portal, billing, hosted sites,
and support channels are live. Verify those before publishing this inventory.

Cloudflare Pages builds this Hugo site from the GitHub repository. The
production branch is `master`; pull requests receive preview deployments.

## Publishing an incident

Add a Markdown post under `content/issues/` using the cState frontmatter
fields `title`, `date`, `resolved`, `severity`, `affected`, and
`section: issue`. Use `notice` for maintenance, `disrupted` for degraded
service, and `down` for an outage. When the incident ends, set
`resolved: true` and enter the actual end time in `resolvedWhen`. Include
customer impact, affected regions where relevant, and the next update time
in the post.

cState reflects published incident files; this repository has no automated
service checks. Only describe a service as continuously monitored if an
independent check and update workflow is in place.
