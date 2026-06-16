#!/usr/bin/env python3
"""Generate the Black Metal theme family for Zed.

The upstream base16 "black-metal" family (by metalelf0) is a set of band-named
schemes that share one pitch-black palette and differ in exactly two slots:
``base0B`` (strings / additions) and ``base0A`` (types / modified). This script
mirrors that: it takes the two canonical base themes in ``src/base.json``
(an opaque variant and a frosted "Blurred" variant) and derives one of each per
band by swapping those two colors, reading them from the vendored base16 scheme
files in ``palettes/``.

The palettes are the upstream scheme files, vendored verbatim from
https://github.com/metalelf0/base16-black-metal-scheme.

Run it with ``just build`` (or ``python3 scripts/generate.py``). The output,
``themes/black-metal.json``, is the file Zed loads — do not edit it by hand.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PALETTES = ROOT / "palettes"
SRC = ROOT / "src" / "base.json"
OUT = ROOT / "themes" / "black-metal.json"

# The two scheme slots that vary between bands, as they appear in src/base.json.
BASE0B_GREEN = "#dd9999"   # strings, additions, links
BASE0A_YELLOW = "#a06666"  # types, enums, modified/warning

SCHEMA = "https://zed.dev/schema/themes/v0.2.0.json"
FAMILY = "Black Metal"
AUTHOR = "alvgaona"


def parse_scheme(path: Path) -> dict[str, str]:
    """Parse a base16 scheme YAML into a {'base0A': '#rrggbb', ...} map.

    Scheme files store colors as 6-digit hex without a leading '#'; this adds it.
    Kept dependency-free on purpose so the generator needs only the stdlib.
    """
    palette: dict[str, str] = {}
    for line in path.read_text().splitlines():
        match = re.match(r'\s*(base0[0-9A-F]):\s*"?([0-9a-fA-F]{6})"?', line)
        if match:
            palette[match.group(1)] = "#" + match.group(2).lower()
    return palette


def swap(node, mapping: dict[str, str]):
    """Recursively replace color substrings in every string in a JSON tree."""
    if isinstance(node, str):
        for old, new in mapping.items():
            node = node.replace(old, new)
        return node
    if isinstance(node, dict):
        return {key: swap(value, mapping) for key, value in node.items()}
    if isinstance(node, list):
        return [swap(value, mapping) for value in node]
    return node


def derive(base_theme: dict, name: str, mapping: dict[str, str]) -> dict:
    theme = copy.deepcopy(base_theme)
    theme["style"] = swap(theme["style"], mapping)
    theme["name"] = name
    return theme


def main() -> None:
    base = json.loads(SRC.read_text())
    opaque = next(t for t in base if not t["name"].endswith("Blurred"))
    blurred = next(t for t in base if t["name"].endswith("Blurred"))

    themes = [copy.deepcopy(opaque), copy.deepcopy(blurred)]

    # palettes/black-metal.yaml is the base scheme (already baked into src/base.json);
    # the band schemes are black-metal-<band>.yaml.
    for path in sorted(PALETTES.glob("black-metal-*.yaml")):
        slug = path.stem[len("black-metal-"):]
        palette = parse_scheme(path)
        mapping = {
            BASE0B_GREEN: palette["base0B"],
            BASE0A_YELLOW: palette["base0A"],
        }
        label = f"{FAMILY} ({slug.replace('-', ' ').title()})"
        themes.append(derive(opaque, label, mapping))
        themes.append(derive(blurred, f"{label} Blurred", mapping))

    family = {
        "$schema": SCHEMA,
        "name": FAMILY,
        "author": AUTHOR,
        "themes": themes,
    }
    OUT.write_text(json.dumps(family, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} with {len(themes)} themes")


if __name__ == "__main__":
    main()
