"""Validate cState configuration and incident front matter before publishing."""
import argparse
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import yaml


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"Duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_yaml(text):
    value = yaml.load(text, Loader=UniqueLoader)
    if not isinstance(value, dict):
        raise ValueError("Expected a YAML object")
    return value


def named_entries(entries, label):
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{label} must be a nonempty list")
    names = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str) or not entry["name"].strip():
            raise ValueError(f"Every {label} entry needs a name")
        names.append(entry["name"])
    if len(names) != len(set(names)):
        raise ValueError(f"Duplicate names in {label}")
    return set(names)


def validate_config(config):
    base = urlparse(config.get("baseURL", ""))
    if base.scheme != "https" or not base.hostname:
        raise ValueError("Production baseURL must be an absolute HTTPS URL")
    params = config.get("params", {})
    categories = named_entries(params.get("categories"), "categories")
    systems = named_entries(params.get("systems"), "systems")
    for system in params["systems"]:
        if system.get("category") not in categories:
            raise ValueError(f"Unknown category for {system['name']}: {system.get('category')}")
    for category in params["categories"]:
        for flag in ("closed", "untitled"):
            if flag in category and not isinstance(category[flag], bool):
                raise ValueError(f"Category {category['name']}: {flag} must be boolean")
    return systems


def timestamp(value):
    if isinstance(value, datetime):
        result = value
    elif isinstance(value, date):
        result = datetime.combine(value, datetime.min.time())
    elif isinstance(value, str):
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    else:
        raise ValueError("Missing or invalid incident date")
    # Existing cState content uses unqualified UTC dates. Prefer explicit offsets for new posts.
    return result.replace(tzinfo=timezone.utc) if result.tzinfo is None else result


def validate_incident(incident, systems):
    if incident.get("section") != "issue":
        raise ValueError("Incident section must be 'issue'")
    if not isinstance(incident.get("title"), str) or not incident["title"].strip():
        raise ValueError("Incident needs a title")
    started = timestamp(incident.get("date"))
    for flag in ("resolved", "informational", "draft", "pin"):
        if flag in incident and not isinstance(incident[flag], bool):
            raise ValueError(f"{flag} must be boolean")
    if "resolved" not in incident:
        raise ValueError("Set resolved explicitly to true or false")
    affected = incident.get("affected", [])
    if not isinstance(affected, list) or any(not isinstance(name, str) for name in affected):
        raise ValueError("affected must be a list of service names")
    if set(affected) - systems:
        raise ValueError(f"Unknown affected services: {sorted(set(affected) - systems)}")
    if not incident.get("informational", False):
        if incident.get("severity") not in {"notice", "disrupted", "down"}:
            raise ValueError("severity must be notice, disrupted, or down")
        if not affected:
            raise ValueError("A service incident needs at least one affected service")
    if incident.get("resolvedWhen") and timestamp(incident["resolvedWhen"]) < started:
        raise ValueError("resolvedWhen cannot precede the incident start")


def frontmatter(path):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("Expected YAML front matter delimited by ---")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("Unterminated front matter") from error
    return load_yaml("\n".join(lines[1:end]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    systems = validate_config(load_yaml((args.root / "config.yml").read_text()))
    paths = sorted((args.root / "content/issues").rglob("*.md"))
    for path in paths:
        if path.name == "_index.md":
            continue
        try:
            validate_incident(frontmatter(path), systems)
        except (ValueError, yaml.YAMLError) as error:
            raise ValueError(f"{path}: {error}") from error
    print(f"Validated {len(systems)} services and {len(paths)} incident files")


if __name__ == "__main__":
    main()
