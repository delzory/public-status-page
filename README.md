# Delzory Status

**Service availability, maintenance notices, and incident updates for Delzory.**

[View status](https://status.delzory.com) · [About this page](docs/about.md) · [Report a vulnerability](SECURITY.md)

This repository contains the source for Delzory's public status page. It is built
with [Hugo](https://gohugo.io/) and [cState](https://github.com/cstate/cstate), with
production hosting and pull request previews on Cloudflare Pages.

## What the page covers

Customers can expand three service groups to see individual components and open
their incident history. Each group reflects its most severe active incident.

| Service group | Components |
| --- | --- |
| Website | Homepage, Documentation, Blog |
| Account | Sign-in, Portal, Billing, Notifications |
| Support | Requests, Urgent Assistance |

Status is based on published incident updates. This repository does not perform
live availability monitoring; a successful site build does not mean every
Delzory service is healthy. [How to read the status page →](docs/about.md)

## Working on the site

| Task | Guide |
| --- | --- |
| Publish or resolve an incident | [Incident publishing](docs/incidents.md) |
| Run checks and prepare a release | [Production checks](docs/production-checks.md) |
| Change components, branding, or layouts | [Site customization](docs/customization.md) |
| Contribute as a maintainer | [Contribution guide](CONTRIBUTING.md) |
| Report a security concern privately | [Security policy](SECURITY.md) |
| Participate in repository discussions | [Code of conduct](CODE_OF_CONDUCT.md) |

### Preview locally

Install Git and the Hugo version recorded in [`.hugo-version`](.hugo-version), then:

```sh
git clone --recurse-submodules https://github.com/delzory/public-status-page.git
cd public-status-page
hugo server --disableFastRender
```

Open the local address printed by Hugo. For an existing clone, run
`git submodule update --init --recursive` before starting. The full CI toolchain
and validation commands are in [Production checks](docs/production-checks.md).

### Publish through a pull request

1. Create a branch and make the content or code change.
2. Run the relevant local checks and open a pull request into `master`.
3. Review the automated results and Cloudflare Pages preview.
4. Merge only after the required reviews and checks pass.

Cloudflare Pages uses `master` for production. Workflow files define the checks;
GitHub rulesets must separately require them before merging. The remaining
administration setup is documented in [Production checks](docs/production-checks.md#settings-required-before-production).

## Repository map

| Path | Purpose |
| --- | --- |
| `config.yml` | Site metadata, service groups, and component descriptions |
| `content/issues/` | Published incident and maintenance posts |
| `content/affected/` | Component detail pages, including those without incidents |
| `layouts/` and `i18n/` | Delzory's theme overrides and interface wording |
| `static/` | Assets and public security contact files copied into the site |
| `themes/cstate/` | Pinned upstream theme submodule |
| `.github/`, `scripts/`, and `tests/` | CI workflows, dependency updates, and validation |

## Before launch

Confirm that every listed component is offered and its contact channel works.
The initial incident history is intentionally empty and does not establish
historical uptime. Verify the production settings in the release guide and the
security and general contact mailboxes before publishing.

## License and credits

The project includes cState under the [MIT License](LICENSE.md). Preserve the
upstream license and attribution when changing or redistributing the source.
