# Production checks

`Site checks` runs for every pull request, merge group, and push to `master`.
It can also be started manually. Jobs use standard Ubuntu runners and read-only
repository permissions. The workflow does not publish or have deployment credentials.

## Checks

- **Build and test status page**: workflow linting with actionlint; a redacted
  Gitleaks scan of Git history; YAML/service/incident validation; an isolated
  incident-rendering regression test; a production Hugo build; JSON, RSS/SVG and
  internal-link validation; a high/critical npm dependency audit; Chromium interaction
  tests at desktop and mobile sizes.
- **Dependency review**: fails on newly introduced high/critical known vulnerable
  dependencies, including development dependencies. Uses the PR or merge-group
  base/head commits. It complements the weekly Dependabot update PRs for Actions,
  the cState submodule, npm and Python. It does not scan arbitrary remote CDN scripts
  or prove the theme has no vulnerabilities.
- **CodeQL**: retain GitHub's working default setup. Its current language is GitHub
  Actions; this is workflow security analysis, not a Hugo-template audit.
- **OpenSSF Scorecard**: retained as an advisory on the default branch. It is not a
  per-PR functional test. Its results are public and its artifact expires in 5 days.

The redundant advanced CodeQL file, both OSV workflows, and automatic stale
issue/PR closure are removed. CodeQL's default setup is configured in GitHub,
not in the deleted `codeql.yml` file.

## Settings required before production

Repository files cannot enable these GitHub/Cloudflare settings:

1. In the default-branch ruleset, require the successful checks **Build and test
   status page**, **Dependency review**, and **Cloudflare Pages** (select the actual
   check names after their first runs). Retain the required CodeQL scanning tool
   and its high/critical threshold. Require branches to be up to date before merging.
2. Remove **Require code quality results** until a useful Code Quality check is
   configured and producing results. This is separate from working CodeQL security
   scanning. Keep the PR requirement, signed commits, linear history, and blocks
   on force pushes/deletion. Retain squash merging if using linear history.
3. For this small project, remove **Require merge queue**. If a queue is retained,
   validate all required providers on `merge_group` before requiring their results;
   do not assume Cloudflare's PR preview runs on merge-group commits. The new site
   and dependency workflows support merge groups, but provider settings still matter.
4. In Cloudflare Pages, use `master` as the production branch. Set `HUGO_VERSION`
   to the value in `.hugo-version` for production and preview (currently `0.147.7`).
   Use `hugo --environment production --gc --minify` and output directory `public`;
   keep any existing preview base-URL override. CI has tested this Hugo version,
   but cannot read or change your Cloudflare dashboard configuration.
5. Verify GitHub secret scanning and push protection are enabled. Gitleaks provides
   an additional required-job scan; it is not a replacement for push protection.

Do not give deployment credentials to pull-request tests. Keep production
deployments restricted to the protected production branch. When adding another
maintainer, require an independent approval and review changes to workflows and tests.

## Local checks

On Linux x86_64, with Git, curl, tar, Python 3.12 and Node 24:

```sh
git submodule update --init --recursive
python3 -m pip install -r requirements-ci.txt
npm ci --ignore-scripts
npx playwright install --with-deps chromium --only-shell
bash scripts/install-ci-tools.sh
.tools/actionlint
.tools/gitleaks git --redact --no-banner
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/validate_status.py
.tools/hugo --environment production --gc --minify
python3 scripts/check_rendered_site.py public
npm test
```

The install script verifies release checksums for pinned Hugo, actionlint and
Gitleaks binaries. Actions are pinned to commit SHAs; npm uses its committed lockfile.
Review and merge Dependabot updates to keep these dependencies maintained.

When adding a service, add its category/system to `config.yml` and create the
corresponding `content/affected/<slug>/_index.md`. Explicit term pages keep service
details available before the first incident; missing targets fail the link check.
For new incident dates, prefer ISO timestamps with an explicit UTC offset.

## Costs and limits

Standard GitHub-hosted runner compute is free for public repositories. Larger
runners and paid third-party services are separate. Artifact and cache storage
have their own allowances. This workflow does not upload browser videos, traces,
or screenshots; Scorecard retains its small report for five days. Cloudflare
Pages build/deployment limits are separate from GitHub Actions.
