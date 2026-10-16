# Delzory Status

Public customer-service status page built with [cState](https://github.com/cstate/cstate).
The configured components live in `config.yml`; incident posts live in `content/issues/`.

## Public status hierarchy

Three service headings are collapsed by default. Opening one shows its
capabilities and their individual status. Each heading summarizes the most
severe incident affecting any capability beneath it.

| Service | Capabilities shown on expansion |
| --- | --- |
| Website | Homepage, Documentation, Blog |
| Account | Sign-in, Portal, Billing, Notifications |
| Support | Requests, Urgent Assistance |

Keep the page focused on services customers can recognize. Describe affected
infrastructure (for example DNS, authentication, a processing queue, or a
regional cluster) in the incident details, and list each affected public
component by its exact configured name. For example, a billing outage should
not mark Sign-in or Portal as down if those still work. Requests and Urgent
Assistance describe the availability of contact channels, not how quickly a
person replies. Notifications does not imply hosted mailbox service.

Only list services that are actually offered and can receive incident updates.
The publicly indexed Delzory homepage shows a maintenance notice, and the
repository alone cannot confirm whether documentation, blog, portal, billing,
and support channels are live. Verify those before publishing this inventory.

Cloudflare Pages builds this Hugo site from the GitHub repository. The
production branch is `master`; pull requests receive preview deployments.

The incident history starts empty. The old 2025 maintenance posts were
removed, and future incidents will appear in a simple chronological list.

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
