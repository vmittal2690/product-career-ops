from __future__ import annotations

import re
import shutil
from pathlib import Path

from .config import ROOT

PRIVATE_PATHS = {
    "private",
    "output",
    "outputs",
    "backups",
    "tmp",
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "public-export",
}

SECRET_PATTERNS = [
    re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    re.compile(r"\+?1?[-.\s(]*\d{3}[-.\s)]*\d{3}[-.\s]*\d{4}"),
    re.compile(r"/Users/[^/\s]+"),
    re.compile(r"(api[_-]?key|secret|token|password)\s*[:=]\s*[^\s]+", re.I),
]


def export_public(destination: Path) -> Path:
    destination = destination.resolve()
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for source in ROOT.rglob("*"):
        if destination == source.resolve() or destination in source.resolve().parents:
            continue
        relative = source.relative_to(ROOT)
        if any(part in PRIVATE_PATHS for part in relative.parts):
            continue
        if any(part.endswith(".egg-info") for part in relative.parts):
            continue
        if source.is_dir():
            (destination / relative).mkdir(parents=True, exist_ok=True)
        else:
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

    fixture = destination / "examples" / "synthetic-profile.yml"
    fixture.parent.mkdir(parents=True, exist_ok=True)
    fixture.write_text(
        "candidate:\n  full_name: Example Product Leader\n"
        "target_roles:\n  - Head of Product\n",
        encoding="utf-8",
    )
    public_readme = destination / "docs" / "PUBLIC_README.md"
    if public_readme.exists():
        shutil.copy2(public_readme, destination / "README.md")
    findings = scan_private(destination)
    if findings:
        shutil.rmtree(destination)
        raise ValueError("Public export blocked by privacy scan:\n" + "\n".join(findings[:20]))
    return destination


def scan_private(root: Path) -> list[str]:
    findings = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() in {".png", ".jpg", ".pdf", ".xlsx"}:
            continue
        relative = path.relative_to(root)
        if relative.as_posix() == "pco/privacy.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            match = pattern.search(text)
            if match:
                findings.append(f"{path.relative_to(root)}: {match.group(0)[:80]}")
    return findings
