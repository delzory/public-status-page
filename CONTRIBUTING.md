# Contributing to Delzory Status

[← Repository overview](README.md)

Delzory maintains this repository internally. External pull requests,
translations, and feature submissions are not currently accepted. Public source
access does not grant permission to publish status updates or change the site.

## Report a problem

| Concern | Where to send it |
| --- | --- |
| Service outage or account issue | Your existing Delzory support channel |
| Incorrect status or a page defect | Your existing Delzory support channel; include the page URL |
| Suspected security vulnerability | [Private security reporting](SECURITY.md) |
| Harassment or other conduct concern | [contact@dev.delzory.com](mailto:contact@dev.delzory.com) |

GitHub Issues are disabled. Reporting a problem through this repository does not
open a support case or automatically publish an incident.

For non-security page defects, include the affected URL, approximate time and
time zone, browser/device, expected behavior, and what happened instead. Remove
personal information from screenshots and error messages.

## Maintainer workflow

1. Work on a branch and keep the pull request focused on a clear outcome.
2. For incident content, follow [Incident publishing](docs/incidents.md). For
   service or layout changes, follow [Site customization](docs/customization.md).
3. Run the applicable [production checks](docs/production-checks.md#local-checks)
   and inspect the Cloudflare Pages preview on desktop and mobile.
4. Describe customer impact, validation, and any remaining setup in the pull request.
5. Merge into `master` through the configured review and branch rules. Cloudflare
   Pages then builds the production deployment.

Keep credentials and customer data out of Git history, fixtures, and incident
posts. Review workflow permission changes and dependency updates carefully;
CI checks should not need production deployment credentials.

## Documentation and dependencies

Update the relevant guide when changing a command, component, publishing step, or
CI behavior. Keep actions pinned to commit SHAs, commit dependency lockfile
updates, and review Dependabot pull requests rather than accepting them blindly.
Preserve the upstream [MIT license](LICENSE.md) and theme attribution.

All participation is covered by the [Code of conduct](CODE_OF_CONDUCT.md).
