"""관심종목(watchlist) 일괄 실행.

watchlist YAML 한 개에 여러 기업 요청(request)을 담아 두면,
에이전트가 순서대로 `run_pipeline`을 실행하고 각 결과의 QA 상태를 모아 반환한다.
한 기업이 실패해도 나머지는 계속 실행한다(에이전트는 멈추지 않는다).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from gic_v13.config import load_request
from gic_v13.pipeline import run_pipeline

REQUIRED_KEYS = ("run_id", "report_mode", "primary_entity")


@dataclass
class AgentRunResult:
    """watchlist 항목 1건의 실행 결과."""

    run_id: str
    entity: str
    qa_status: str  # "PASS" | "WARNING" | "FAIL" | "ERROR"
    run_dir: Path | None = None
    preview_path: Path | None = None
    qa_report_path: Path | None = None
    error: str | None = None
    warnings: list[str] = field(default_factory=list)
    fatal_errors: list[str] = field(default_factory=list)


def load_watchlist(path: str | Path) -> list[dict[str, Any]]:
    """watchlist YAML을 읽어 request 리스트로 반환한다.

    지원 형식:
    - `requests:` 키 아래에 request 객체 목록을 인라인으로 둔다.
    - 또는 최상위가 곧바로 request 객체 목록(list)인 경우.
    """
    with Path(path).open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if isinstance(data, list):
        requests = data
    elif isinstance(data, dict) and "requests" in data:
        requests = data["requests"] or []
    else:
        raise ValueError("watchlist는 'requests:' 목록 또는 request 객체 리스트여야 합니다.")

    if not requests:
        raise ValueError("watchlist에 실행할 request가 하나도 없습니다.")

    for index, request in enumerate(requests, start=1):
        missing = [key for key in REQUIRED_KEYS if not request.get(key)]
        if missing:
            raise ValueError(f"watchlist {index}번 request에 누락된 필드: {', '.join(missing)}")
    return requests


def _derive_qa_status(qa_report: dict[str, Any]) -> str:
    """qa_report.json dict에서 종합 상태(PASS/WARNING/FAIL)를 산출한다."""
    gates = qa_report.get("gates", {}) or {}
    gate_values = set(gates.values())
    if qa_report.get("fatal_errors") or "FAIL" in gate_values:
        return "FAIL"
    if qa_report.get("warnings") or "WARNING" in gate_values:
        return "WARNING"
    return "PASS"


def _read_qa_report(run_dir: Path) -> dict[str, Any]:
    qa_path = run_dir / "audit" / "qa_report.json"
    if not qa_path.exists():
        return {}
    return json.loads(qa_path.read_text(encoding="utf-8"))


def run_watchlist(
    watchlist_path: str | Path,
    output_root: str | Path,
    fixture_dir: str | Path | None = None,
    api_key: str | None = None,
) -> list[AgentRunResult]:
    """watchlist의 모든 기업을 순서대로 실행하고 결과 목록을 반환한다."""
    requests = load_watchlist(watchlist_path)
    results: list[AgentRunResult] = []

    for request in requests:
        entity = request.get("primary_entity", {}).get("corp_name") or request["run_id"]
        try:
            run_dir = run_pipeline(
                request=request,
                output_root=Path(output_root),
                fixture_dir=fixture_dir,
                api_key=api_key,
            )
            qa_report = _read_qa_report(run_dir)
            results.append(
                AgentRunResult(
                    run_id=request["run_id"],
                    entity=entity,
                    qa_status=_derive_qa_status(qa_report),
                    run_dir=run_dir,
                    preview_path=run_dir / "deliverables" / "preview.html",
                    qa_report_path=run_dir / "audit" / "qa_report.md",
                    warnings=list(qa_report.get("warnings", []) or []),
                    fatal_errors=list(qa_report.get("fatal_errors", []) or []),
                )
            )
        except Exception as exc:  # noqa: BLE001 - 한 건 실패가 전체를 멈추면 안 됨
            results.append(
                AgentRunResult(
                    run_id=request.get("run_id", "unknown"),
                    entity=entity,
                    qa_status="ERROR",
                    error=f"{type(exc).__name__}: {exc}",
                )
            )
    return results
