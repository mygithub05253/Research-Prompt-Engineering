"""GIC v14 파이프라인: 수집 → 조립 → 산출물 3종(report.html / prompt_pack.md / qa)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from gic_v14.config import get_api_key
from gic_v14.domain import FinancialFact, to_plain
from gic_v14.market.collect import collect_market, load_market_fixture, MarketSnapshot
from gic_v14.model.benchmark import append_peer_average
from gic_v14.model.financial_ratios import summary_row
from gic_v14.normalize.facts import normalize_single_account_all
from gic_v14.opendart.financials import collect_financial_payloads, resolve_company
from gic_v14.promptpack.build import build_prompt_pack
from gic_v14.render.report import render_report
from gic_v14.view import assemble_view

PKG_ROOT = Path(__file__).resolve().parent
# templates/assets 는 패키지 외부(version14.0/templates) — repo 레이아웃 기준 상대 탐색
def _find_dir(name: str) -> Path:
    for base in (PKG_ROOT.parent.parent, PKG_ROOT.parent.parent.parent):
        cand = base / name
        if cand.exists():
            return cand
    return PKG_ROOT.parent.parent / name


def run_pipeline(
    request: dict[str, Any],
    output_root: str | Path,
    fixture_dir: str | Path | None = None,
    market_fixture: str | Path | None = None,
    api_key: str | None = None,
    live_market: bool = True,
    template_dir: str | Path | None = None,
    assets_dir: str | Path | None = None,
) -> Path:
    run_dir = Path(output_root) / request["run_id"]
    raw_dir = run_dir / "data" / "raw_opendart"
    for folder in ["data", "deliverables", "audit"]:
        (run_dir / folder).mkdir(parents=True, exist_ok=True)

    template_dir = Path(template_dir) if template_dir else _find_dir("templates")
    assets_dir = Path(assets_dir) if assets_dir else (template_dir / "assets")

    # 1) OpenDART 재무 (대상기업)
    key = get_api_key(api_key, allow_missing=fixture_dir is not None)
    company, facts = _collect_entity_facts(
        request["primary_entity"], request, raw_dir, fixture_dir, key
    )

    # 2) 시장데이터
    stock_code = request["primary_entity"].get("stock_code") or ""
    if market_fixture:
        market = load_market_fixture(market_fixture)
    elif live_market and stock_code:
        market = collect_market(stock_code, request["as_of_date"])
    else:
        market = MarketSnapshot(stock_code=stock_code, as_of_date=request["as_of_date"], unavailable=["market_skipped"])

    # 3) 피어 벤치마킹 (각 피어 재무 수집 → OPM/ROE/ROA 계산)
    peers_cfg = (request.get("peers", {}) or {}).get("manual", []) or []
    rows = [summary_row(company.corp_name, facts, market)]
    for i, peer in enumerate(peers_cfg):
        p_code = peer.get("stock_code")
        p_name = peer.get("corp_name", p_code or "?")
        p_market = None
        try:
            if live_market and not market_fixture and p_code:
                p_market = collect_market(p_code, request["as_of_date"])
            _, p_facts = _collect_entity_facts(
                {"corp_name": p_name, "stock_code": p_code, "corp_code": peer.get("corp_code")},
                request, run_dir / "data" / f"raw_peer_{i}", fixture_dir, key,
            )
            rows.append(summary_row(p_name, p_facts, p_market))
        except Exception:
            rows.append({"name": p_name, "revenue": None, "opm": None, "roe": None,
                         "roa": None, "per": getattr(p_market, "per", None),
                         "pbr": getattr(p_market, "pbr", None), "ev_ebitda": None})
    peers = append_peer_average(rows)

    # 4) view 조립 + 산출물
    view = assemble_view(request, market, facts, peers=peers)
    report_path = render_report(view, run_dir / "deliverables" / "report.html", template_dir, assets_dir)
    (run_dir / "deliverables" / "prompt_pack.md").write_text(build_prompt_pack(view), encoding="utf-8")

    _write_json(run_dir / "data" / "market.json", market.to_plain())
    _write_json(run_dir / "data" / "normalized_facts.json", {"financial_fact": to_plain(facts)})
    _write_qa(run_dir / "audit" / "qa_report.md", view, market, facts)
    return run_dir


def _collect_entity_facts(entity, request, raw_dir, fixture_dir, key):
    """한 기업의 OpenDART 재무를 수집·정규화 → (CompanyRecord, facts)."""
    sub = dict(request)
    sub["primary_entity"] = entity
    Path(raw_dir).mkdir(parents=True, exist_ok=True)
    company = resolve_company(sub, raw_dir=raw_dir, fixture_dir=fixture_dir, api_key=key)
    payloads = collect_financial_payloads(sub, company, raw_dir=raw_dir, fixture_dir=fixture_dir, api_key=key)
    retrieved_at = f"{request.get('as_of_date')}T00:00:00+09:00"
    facts: list[FinancialFact] = []
    for payload in payloads:
        year = payload.get("list", [{}])[0].get("bsns_year", "unknown") if payload.get("list") else "unknown"
        facts.extend(
            normalize_single_account_all(
                payload, corp_name=company.corp_name, endpoint="fnlttSinglAcntAll",
                raw_payload_path=str(Path(raw_dir) / f"fnlttSinglAcntAll_{year}.json"), retrieved_at=retrieved_at,
            )
        )
    return company, facts


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_qa(path: Path, view: dict[str, Any], market: MarketSnapshot, facts: list[FinancialFact]) -> None:
    auto = [k for k, v in view["revision"].items() if v is not None]
    missing = [k for k, v in view["revision"].items() if v is None]
    lines = [
        "# QA Report (v14)", "",
        f"- 재무 facts 수집: {len(facts)}건",
        f"- 시장데이터 자동 수집 항목: {', '.join(auto) if auto else '없음'}",
        f"- 미수집(— 표기/사람 입력 필요): {', '.join(missing) if missing else '없음'}",
        f"- 시장데이터 unavailable: {', '.join(market.unavailable) if market.unavailable else '없음'}",
        "",
        "## 사람 몫 (release 전 필수)",
        "- report.html의 [작성 필요] 정성 칸을 prompt_pack.md로 작성",
        "- 목표주가/투자의견은 사람 판단 (자동 추정 안 함)",
        "",
        "release_approved: false",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
