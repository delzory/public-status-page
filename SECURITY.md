# Security policy

Report suspected vulnerabilities privately to
[security@delzory.com](mailto:security@delzory.com).

Do not put credentials, customer information, exploit details, or security reports
in public pull requests, comments, or incident posts.

## Scope

This policy covers the source in this repository and the public status page at
**status.delzory.com**. Include the affected URL, file, or commit so maintainers
can identify the issue. For an upstream Hugo or cState issue, identify the
upstream component as well; avoid disclosing an unpatched vulnerability publicly.

The current production deployment and changes proposed for the next deployment
are the maintained versions. Historical commits, forks, and third-party
deployments are not maintained release branches.

## What to include

- A concise description of the vulnerability and its potential impact.
- The affected URL, file, dependency version, or commit.
- Minimal reproduction steps using accounts and data you control.
- Sanitized evidence and a way to contact you privately.

Remove passwords, tokens, personal information, and unrelated customer data from
reports. If you encounter exposed credentials or private data, stop testing and
report where you found them without copying more than necessary.

## Coordinate disclosure

Allow maintainers to investigate and coordinate a fix before publishing technical
details. Keep testing limited to the minimum needed to demonstrate the issue;
this policy does not authorize disruptive testing or access to other people's
accounts or data.

No response deadline or payment is promised by this document. General support
requests and routine status-page corrections belong in your existing Delzory
support channel.

## Security checks in this repository

The pull request workflow checks for exposed credentials, known vulnerable
dependencies, invalid status content, and build or browser regressions. GitHub's
CodeQL setup analyzes GitHub Actions workflows; OpenSSF Scorecard reports on
repository practices. These checks have defined limits and do not certify that
the site is vulnerability-free. See [Production checks](docs/production-checks.md)
for coverage and the settings needed to enforce checks before merging.

## Published contact file

The site publishes its security contact at `/.well-known/security.txt`, with a
matching `/security.txt` copy for discoverability. Source files are in `static/`.
Maintainers must verify the contact details and renew the expiration date before
**April 16, 2027**. No encryption key is advertised; do not send secrets by email.
