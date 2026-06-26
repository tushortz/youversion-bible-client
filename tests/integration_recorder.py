"""Capture live API request/response pairs during integration tests."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx

REDACT_HEADER_KEYS = frozenset(
    {"authorization", "cookie", "x-youversion-auth", "set-cookie"}
)
TEXT_PREVIEW_LIMIT = 20_000
_run_index = 0


def make_run_dir(base: Path | str = "results/integration") -> Path:
    """Create a timestamped directory for one integration test run."""
    global _run_index
    _run_index = 0
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = Path(base) / stamp
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _redact_headers(headers: dict[str, Any] | None) -> dict[str, Any]:
    if not headers:
        return {}
    redacted: dict[str, Any] = {}
    for key, value in headers.items():
        if key.lower() in REDACT_HEADER_KEYS:
            redacted[key] = "<redacted>"
        else:
            redacted[key] = value
    return redacted


def _redact_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
    safe = dict(kwargs)
    if "headers" in safe:
        safe["headers"] = _redact_headers(safe["headers"])
    if "auth" in safe:
        safe["auth"] = "<redacted>"
    if "json" in safe and isinstance(safe["json"], dict):
        body = dict(safe["json"])
        for key in ("password", "client_secret", "refresh_token", "access_token"):
            if key in body:
                body[key] = "<redacted>"
        safe["json"] = body
    if "data" in safe and isinstance(safe["data"], dict):
        body = dict(safe["data"])
        for key in ("password", "client_secret"):
            if key in body:
                body[key] = "<redacted>"
        safe["data"] = body
    return safe


def _slug_from_url(url: str) -> str:
    path = urlparse(url).path.strip("/")
    slug = re.sub(r"[^\w.-]+", "_", path) or "root"
    if slug.endswith(".json"):
        slug = slug[: -len(".json")]
    return slug[:120]


def _response_body(response: httpx.Response) -> Any:
    content_type = response.headers.get("content-type", "")
    if "json" in content_type:
        try:
            return response.json()
        except ValueError:
            pass
    text = response.text
    if len(text) > TEXT_PREVIEW_LIMIT:
        return {
            "_truncated": True,
            "length": len(text),
            "preview": text[:TEXT_PREVIEW_LIMIT],
        }
    return text


def _write_record(
    run_dir: Path,
    state: dict[str, Any],
    method: str,
    url: str,
    kwargs: dict[str, Any],
    response: httpx.Response,
) -> Path:
    global _run_index
    _run_index += 1
    idx = _run_index
    slug = _slug_from_url(url)
    filename = f"{idx:03d}_{method.lower()}_{slug}.json"
    path = run_dir / filename
    record = {
        "index": idx,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request": {
            "method": method.upper(),
            "url": url,
            "params": kwargs.get("params"),
            "json": kwargs.get("json"),
            "data": kwargs.get("data"),
            "headers": _redact_headers(kwargs.get("headers")),
        },
        "response": {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": _response_body(response),
        },
    }
    path.write_text(json.dumps(record, indent=2, default=str), encoding="utf-8")
    state["entries"].append(
        {
            "file": filename,
            "method": method.upper(),
            "url": url,
            "status_code": response.status_code,
        }
    )
    return path


def install_httpx_recorder(client: httpx.AsyncClient, run_dir: Path) -> dict[str, Any]:
    """Patch an httpx client so every GET/POST is saved under ``run_dir``."""
    state: dict[str, Any] = {"entries": []}
    original_get = client.get
    original_post = client.post

    async def recorded_get(url: str, **kwargs: Any) -> httpx.Response:
        response = await original_get(url, **kwargs)
        _write_record(run_dir, state, "GET", str(url), _redact_kwargs(kwargs), response)
        return response

    async def recorded_post(url: str, **kwargs: Any) -> httpx.Response:
        response = await original_post(url, **kwargs)
        _write_record(
            run_dir, state, "POST", str(url), _redact_kwargs(kwargs), response
        )
        return response

    client.get = recorded_get  # type: ignore[method-assign]
    client.post = recorded_post  # type: ignore[method-assign]
    return state


_recorder_states: list[dict[str, Any]] = []


def register_recorder_state(state: dict[str, Any]) -> None:
    """Track recorder state from async client fixtures."""
    _recorder_states.append(state)


def flush_manifest(run_dir: Path) -> Path | None:
    """Write manifest.json for all recorder states in this run."""
    if not _recorder_states:
        return None
    return write_manifest(run_dir, _recorder_states)


def write_manifest(run_dir: Path, states: list[dict[str, Any]]) -> Path:
    """Write a run-level manifest summarizing all recorded calls."""
    entries: list[dict[str, Any]] = []
    for state in states:
        entries.extend(state.get("entries", []))
    manifest = {
        "run_dir": str(run_dir),
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "total_calls": len(entries),
        "calls": entries,
    }
    path = run_dir / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path
