from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests


class OpenDartError(RuntimeError):
    pass


ENDPOINTS = {
    "company": "https://opendart.fss.or.kr/api/company.json",
    "list": "https://opendart.fss.or.kr/api/list.json",
    "fnlttSinglAcntAll": "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json",
    "fnlttSinglIndx": "https://opendart.fss.or.kr/api/fnlttSinglIndx.json",
    "document": "https://opendart.fss.or.kr/api/document.xml",
    "corpCode": "https://opendart.fss.or.kr/api/corpCode.xml",
}

FATAL_STATUSES = {"010", "011", "012", "020", "021", "100", "800", "900", "901"}


class OpenDartClient:
    def __init__(
        self,
        api_key: str,
        cache_dir: str | Path,
        session: Any | None = None,
        timeout: int = 20,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = session or requests.Session()
        self.timeout = timeout

    def get_json(self, endpoint: str, params: dict[str, Any], cache_name: str) -> dict[str, Any]:
        if endpoint not in ENDPOINTS:
            raise ValueError(f"Unsupported OpenDART endpoint: {endpoint}")
        request_params = dict(params)
        request_params["crtfc_key"] = self.api_key
        response = self.session.get(ENDPOINTS[endpoint], params=request_params, timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()
        status = str(payload.get("status", "000"))
        if status in FATAL_STATUSES:
            raise OpenDartError(f"OpenDART {endpoint} failed with status {status}: {payload.get('message', '')}")
        self._write_cache(cache_name, endpoint, params, payload)
        return payload

    def _write_cache(self, cache_name: str, endpoint: str, params: dict[str, Any], payload: dict[str, Any]) -> None:
        safe_params = {key: value for key, value in params.items() if key != "crtfc_key"}
        cached = {
            "endpoint": endpoint,
            "params": safe_params,
            "payload": payload,
        }
        (self.cache_dir / cache_name).write_text(
            json.dumps(cached, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
