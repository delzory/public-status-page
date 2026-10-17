#!/usr/bin/env bash
set -euo pipefail
# Only Linux x86_64 is used by this project's standard GitHub-hosted runners.
[[ "$(uname -s)/$(uname -m)" == "Linux/x86_64" ]] || { echo 'Linux x86_64 required'; exit 1; }
root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$root/.tools"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
download() {
  local repository="$1" version="$2" archive="$3" checksums="$4" binary="$5"
  local base="https://github.com/$repository/releases/download/v$version"
  curl --fail --silent --show-error --location --retry 3 "$base/$archive" -o "$tmp/$archive"
  curl --fail --silent --show-error --location --retry 3 "$base/$checksums" -o "$tmp/checksums.txt"
  (cd "$tmp"; awk -v file="$archive" '$2 == file { print }' checksums.txt > selected.sha256
    test -s selected.sha256; sha256sum --check selected.sha256)
  tar --no-same-owner -xzf "$tmp/$archive" -C "$root/.tools" "$binary"
}
version="$(tr -d '\r\n' < "$root/.hugo-version")"
[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo 'Invalid Hugo version'; exit 1; }
download gohugoio/hugo "$version" "hugo_extended_${version}_linux-amd64.tar.gz" "hugo_${version}_checksums.txt" hugo
download rhysd/actionlint 1.7.12 actionlint_1.7.12_linux_amd64.tar.gz actionlint_1.7.12_checksums.txt actionlint
download gitleaks/gitleaks 8.30.1 gitleaks_8.30.1_linux_x64.tar.gz gitleaks_8.30.1_checksums.txt gitleaks
if [[ -n "${GITHUB_PATH:-}" ]]; then printf '%s\n' "$root/.tools" >> "$GITHUB_PATH"; fi
