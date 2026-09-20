#!/usr/bin/env python3
"""Render bucket/causari.json from the latest causari GitHub release.

Reads SHA256SUMS.txt, prefers the causari-<tag>-<target>.zip archive (holds
causari.exe and re.exe), falls back to re-<tag>-<target>.zip. Standard
library only.

    python3 scripts/render.py            # latest release
    python3 scripts/render.py v0.2.0     # a specific tag
"""
import json
import sys
import urllib.request

REPO = "croviatrust/causari"
TARGET = "x86_64-pc-windows-msvc"


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "causari-scoop-bucket"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main() -> int:
    tag = sys.argv[1] if len(sys.argv) > 1 else json.loads(get(f"https://api.github.com/repos/{REPO}/releases/latest"))["tag_name"]
    version = tag.lstrip("v")
    base = f"https://github.com/{REPO}/releases/download/{tag}"
    sums = {}
    for line in get(f"{base}/SHA256SUMS.txt").decode().splitlines():
        parts = line.split()
        if len(parts) == 2:
            sums[parts[1].lstrip("*")] = parts[0]
    name = sha = None
    for candidate in (f"causari-{tag}-{TARGET}.zip", f"re-{tag}-{TARGET}.zip"):
        if candidate in sums:
            name, sha = candidate, sums[candidate]
            break
    if not name:
        raise SystemExit(f"no Windows archive in SHA256SUMS.txt of {tag}")
    both = name.startswith("causari-")
    manifest = {
        "version": version,
        "description": "AI-written code has no author. It has causes. Causari proves them.",
        "homepage": "https://causari.dev",
        "license": "Apache-2.0",
        "url": f"{base}/{name}",
        "hash": sha,
        "bin": ["causari.exe", "re.exe"] if both else [["re.exe", "re"], ["re.exe", "causari"]],
        "checkver": {"github": f"https://github.com/{REPO}"},
        "autoupdate": {
            "url": f"https://github.com/{REPO}/releases/download/v$version/causari-v$version-{TARGET}.zip",
            "hash": {"url": "$baseurl/SHA256SUMS.txt"},
        },
        "notes": ["Run `re audit` in any git repository. A count, not a grade: https://causari.dev/method"],
    }
    with open("bucket/causari.json", "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    print(f"bucket/causari.json rendered for {tag} ({'causari+re' if both else 're + shim'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
