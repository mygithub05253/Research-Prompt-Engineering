from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests

from gic_v13.domain import CompanyRecord
from gic_v13.opendart.client import ENDPOINTS, OpenDartClient
from gic_v13.opendart.corp_codes import CorpCodeResolver


def resolve_company(
    request: dict[str, Any],
    raw_dir: str | Path,
    fixture_dir: str | Path | None = None,
    api_key: str | None = None,
) -> CompanyRecord:
    entity = request["primary_entity"]
    if entity.get("corp_code") and entity.get("corp_name"):
        return CompanyRecord(
            corp_code=entity["corp_code"],
            corp_name=entity["corp_name"],
            stock_code=entity.get("stock_code"),
        )
    if fixture_dir:
        resolver = CorpCodeResolver.from_xml(Path(fixture_dir) / "corp_codes.xml")
    else:
        if not api_key:
            raise RuntimeError("OpenDART API key is required for live corp code lookup.")
        zip_path = download_corp_code_zip(api_key, Path(raw_dir))
        resolver = CorpCodeResolver.from_zip(zip_path)
    return resolver.resolve(
        corp_name=entity.get("corp_name") or None,
        stock_code=entity.get("stock_code") or None,
        corp_code=entity.get("corp_code") or None,
    )


def collect_financial_payloads(
    request: dict[str, Any],
    company: CompanyRecord,
    raw_dir: str | Path,
    fixture_dir: str | Path | None = None,
    api_key: str | None = None,
) -> list[dict[str, Any]]:
    raw_path = Path(raw_dir)
    raw_path.mkdir(parents=True, exist_ok=True)
    payloads: list[dict[str, Any]] = []
    for year in request.get("bsns_years", []):
        for reprt_code in request.get("reprt_codes", ["11011"]):
            if fixture_dir:
                payload = json.loads((Path(fixture_dir) / f"fnlttSinglAcntAll_{year}.json").read_text(encoding="utf-8"))
                (raw_path / f"fnlttSinglAcntAll_{year}.json").write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
            else:
                if not api_key:
                    raise RuntimeError("OpenDART API key is required for live financial collection.")
                client = OpenDartClient(api_key=api_key, cache_dir=raw_path)
                payload = client.get_json(
                    "fnlttSinglAcntAll",
                    {
                        "corp_code": company.corp_code,
                        "bsns_year": year,
                        "reprt_code": reprt_code,
                        "fs_div": request.get("fs_div", "CFS"),
                    },
                    cache_name=f"fnlttSinglAcntAll_{year}_{reprt_code}_{request.get('fs_div', 'CFS')}.json",
                )
            payloads.append(payload)
    return payloads


def download_corp_code_zip(api_key: str, raw_dir: Path) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    response = requests.get(ENDPOINTS["corpCode"], params={"crtfc_key": api_key}, timeout=30)
    response.raise_for_status()
    zip_path = raw_dir / "corpCode.zip"
    zip_path.write_bytes(response.content)
    return zip_path
