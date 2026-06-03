from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def load_request(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not data.get("run_id"):
        raise ValueError("run_request requires run_id")
    if not data.get("report_mode"):
        raise ValueError("run_request requires report_mode")
    if not data.get("primary_entity"):
        raise ValueError("run_request requires primary_entity")
    return data


def get_api_key(explicit_key: str | None = None, allow_missing: bool = False) -> str | None:
    key = explicit_key or os.environ.get("OPENDART_API_KEY")
    if key:
        return key.strip()
    if allow_missing:
        return None
    raise RuntimeError("OpenDART API key is required. Set OPENDART_API_KEY or pass it at runtime.")
