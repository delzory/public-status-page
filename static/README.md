# Public site assets

Hugo copies the contents of this directory directly into the published site.
Everything here is public; do not add credentials or internal documents.

- `logo.png` is the configured site logo.
- `_headers` contains Cloudflare Pages response header rules.
- `.well-known/security.txt` publishes the security contact; `security.txt` is its matching discovery copy.
- `img/` is available for public images referenced by site content.

To add custom favicons, use `favicon.ico`, `favicon-16x16.png`, and
`favicon-32x32.png`. Review changes using the production build and browser checks.
