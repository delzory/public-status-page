"""Check generated data, feeds and same-site navigation without crawling external sites."""
import argparse
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        key = "href" if tag in {"a", "link"} else "src" if tag in {"img", "script"} else None
        if key and attrs.get(key):
            self.targets.append(attrs[key])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    root = args.directory.resolve()
    for name in ("index.html", "index.json", "index.xml", "index.svg", "404.html"):
        if not (root / name).is_file():
            raise ValueError(f"Missing output: {name}")
    home = json.loads((root / "index.json").read_text())
    origin = urlparse(home["baseURL"])
    for path in root.rglob("*.json"):
        json.loads(path.read_text())
    for suffix in ("*.xml", "*.svg"):
        for path in root.rglob(suffix):
            ET.parse(path)
    errors = set()
    for path in root.rglob("*.html"):
        # Hugo taxonomy aliases contain redirects, not site navigation.
        html = path.read_text()
        links = Links()
        links.feed(html)
        relative = path.relative_to(root).as_posix()
        page_url = urljoin(home["baseURL"].rstrip("/") + "/", relative)
        for target in links.targets:
            url = urlparse(urljoin(page_url, target))
            if url.scheme not in {"http", "https"} or url.netloc != origin.netloc:
                continue
            candidate = (root / unquote(url.path).lstrip("/")).resolve()
            if not candidate.is_relative_to(root):
                errors.add(f"{relative}: path escapes output directory: {target}")
                continue
            if candidate.is_dir():
                candidate /= "index.html"
            if not candidate.is_file():
                errors.add(f"{relative}: missing local target {url.path}")
    if errors:
        raise ValueError("Broken site links:\n" + "\n".join(sorted(errors)))
    print("Generated JSON, RSS/SVG and internal navigation passed")


if __name__ == "__main__":
    main()
