from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass, asdict
from typing import Iterable

import yaml

from .config import SOURCES_PATH


@dataclass
class DiscoveredRole:
    company: str
    role: str
    url: str
    location: str = ""
    source: str = ""


def _fetch_json(url: str) -> object:
    req = urllib.request.Request(url, headers={"User-Agent": "product-career-ops/0.1"})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def _greenhouse(source: dict) -> list[DiscoveredRole]:
    data = _fetch_json(source["api_url"])
    return [
        DiscoveredRole(
            source="Greenhouse",
            company=source["company"],
            role=job.get("title", ""),
            url=job.get("absolute_url", ""),
            location=(job.get("location") or {}).get("name", ""),
        )
        for job in data.get("jobs", [])
        if job.get("title") and job.get("absolute_url")
    ]


def _lever(source: dict) -> list[DiscoveredRole]:
    data = _fetch_json(source["api_url"])
    return [
        DiscoveredRole(
            source="Lever",
            company=source["company"],
            role=job.get("text", ""),
            url=job.get("hostedUrl", ""),
            location=(job.get("categories") or {}).get("location", ""),
        )
        for job in data
        if job.get("text") and job.get("hostedUrl")
    ]


def _ashby(source: dict) -> list[DiscoveredRole]:
    data = _fetch_json(source["api_url"])
    jobs = data.get("jobs", data if isinstance(data, list) else [])
    return [
        DiscoveredRole(
            source="Ashby",
            company=source["company"],
            role=job.get("title", ""),
            url=job.get("jobUrl", job.get("url", "")),
            location=job.get("location", ""),
        )
        for job in jobs
        if job.get("title") and (job.get("jobUrl") or job.get("url"))
    ]


def _matches(role: DiscoveredRole, positive: list[str], negative: list[str]) -> bool:
    text = f"{role.role} {role.location}".lower()
    return any(word.lower() in text for word in positive) and not any(
        word.lower() in text for word in negative
    )


def scan() -> list[dict]:
    if not SOURCES_PATH.exists():
        return []
    config = yaml.safe_load(SOURCES_PATH.read_text(encoding="utf-8")) or {}
    positive = config.get("filters", {}).get("positive_titles", [])
    negative = config.get("filters", {}).get("negative_titles", [])
    discovered: list[DiscoveredRole] = []
    for source in config.get("sources", []):
        if not source.get("enabled", True):
            continue
        provider = source.get("provider", "").lower()
        try:
            if provider == "greenhouse":
                discovered.extend(_greenhouse(source))
            elif provider == "lever":
                discovered.extend(_lever(source))
            elif provider == "ashby":
                discovered.extend(_ashby(source))
        except Exception as exc:
            discovered.append(DiscoveredRole(
                company=source.get("company", ""),
                role=f"SCAN ERROR: {exc}",
                url=source.get("api_url", ""),
                source=provider,
            ))
    dedup = {}
    for role in discovered:
        key = role.url.lower().rstrip("/") or f"{role.company}|{role.role}".lower()
        if role.role.startswith("SCAN ERROR") or _matches(role, positive, negative):
            dedup[key] = role
    return [asdict(item) for item in dedup.values()]

