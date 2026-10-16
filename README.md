# Delzory Status

Public customer-service status page built with [cState](https://github.com/cstate/cstate).
The configured components live in `config.yml`; incident posts live in `content/issues/`.

## Public components

| Component | Report problems with |
| --- | --- |
| Website & Docs | Public website, documentation, and announcements |
| Customer Portal & Billing | Sign-in, service management, invoices, and payments |
| Hosted Websites | Customer websites and custom domains |
| Support | General and urgent support channels |
| Email & Notifications | Transactional email, alerts, and notifications |

Keep the page focused on services customers can recognize. Describe affected
infrastructure (for example DNS, authentication, a processing queue, or a
regional cluster) in the incident details, and list each affected public
component by its exact configured name.

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
