"""수집 데이터 → 렌더용 ReportView(dict) 조립.

OpenDART 재무 facts + 시장 스냅샷 + 피어를 양식 칸에 매핑한다.
정성 섹션은 '힌트'만 채우고 본문은 [작성 필요]로 둔다(프롬프트 팩에서 작성).
"""

from __future__ import annotations

from typing import Any

from gic_v14.domain import FinancialFact
from gic_v14.market.collect import MarketSnapshot
from gic_v14.model.financial_ratios import compute_period_ratios

WON_PER_BILLION = 1e9  # 원 → 십억원

COMPLIANCE = [
    "본 문서는 가천대학교 금융투자 동아리 GIC의 학생들이 학습 및 연구 목적으로 작성한 리포트입니다.",
    "본 문서는 증권, 금융 상품, 기타 투자 자산에 대한 매수·매도·보유를 권유하기 위한 목적으로 제작되지 않았습니다.",
    "본 보고서에 포함된 모든 정보는 작성 시점의 공개 자료(OpenDART·KRX)를 바탕으로 하며 그 정확성·완전성을 보증하지 않습니다.",
    "모든 투자 결정은 투자자 본인의 판단과 책임하에 이루어져야 합니다.",
    "본 보고서에 대한 지적재산권은 가천대학교 금융투자동아리 GIC에 있으며 법적 책임소재의 증빙자료로 사용될 수 없습니다.",
]

CONTENTS = [
    {"title": "산업분석", "sub": "산업 사이클 · 수급 구조 · 경쟁 환경"},
    {"title": "기업분석", "sub": "사업부 구조 · 경쟁력 · 지배구조"},
    {"title": "투자포인트", "sub": "Point 1 · 2 · 3"},
    {"title": "투자리스크", "sub": "하방 시나리오 · 민감도 (Red Team)"},
    {"title": "밸류에이션", "sub": "피어 비교 · 목표주가 산출"},
]

# 섹터별 기본 정성 힌트(프롬프트 팩과 공유). 미정의 섹터는 GENERIC.
SECTOR_PROFILES: dict[str, dict[str, Any]] = {
    "SEMICONDUCTOR": {
        "industry": [
            {"h4": "메모리 사이클 위치", "hint": "DRAM/NAND 수급과 가격 사이클의 현재 국면을 서술. (자동주입: 매출 YoY·CAGR)"},
            {"h4": "AI 수요 구조", "hint": "HBM 등 AI 메모리 수요와 일반 메모리 수요의 분기, 가격 탄력성."},
        ],
        "company": [
            {"h4": "사업부 포트폴리오", "hint": "사업부문별 매출·이익 비중과 핵심 경쟁력. (자동주입: 사업보고서 부문 매출)"},
            {"h4": "원가·해자 구조", "hint": "수직계열화·캐펙스·R&D 강도가 만드는 진입장벽."},
        ],
        "points": [
            {"h4": "메모리 믹스 고도화", "hint": "고부가 제품 비중 확대 → 영업이익률 회복 논리."},
            {"h4": "파운드리/비메모리", "hint": "가동률·수율·수주잔고 개선 시나리오."},
            {"h4": "주주환원", "hint": "순현금·배당·자사주 정책이 밸류에이션 하단 지지."},
        ],
        "risks": [
            {"h4": "메모리 가격 변동", "hint": "다운사이클 시 ASP·재고 부담 (Red Team)."},
            {"h4": "환율·지정학", "hint": "수출 비중·미중 규제 민감도."},
        ],
    },
    "GENERIC": {
        "industry": [
            {"h4": "산업 구조", "hint": "시장 규모·성장률·경쟁 구도를 서술. (자동주입: 매출 YoY·CAGR)"},
            {"h4": "수요 동인", "hint": "핵심 수요 드라이버와 가격 결정 구조."},
        ],
        "company": [
            {"h4": "사업 구조", "hint": "사업부문별 매출·이익 비중과 경쟁력. (자동주입: 부문 매출)"},
            {"h4": "경쟁 우위", "hint": "원가·브랜드·기술이 만드는 해자."},
        ],
        "points": [
            {"h4": "성장 동력", "hint": "핵심 성장 논리 1."},
            {"h4": "수익성 개선", "hint": "마진 개선 논리."},
            {"h4": "자본 배분", "hint": "현금흐름·배당·투자 정책."},
        ],
        "risks": [
            {"h4": "수요 둔화", "hint": "전방 수요 약화 시나리오 (Red Team)."},
            {"h4": "외부 변수", "hint": "환율·규제·원자재 민감도."},
        ],
    },
}


def _profile(sector_id: str | None) -> dict[str, Any]:
    return SECTOR_PROFILES.get((sector_id or "").upper(), SECTOR_PROFILES["GENERIC"])


def _won_to_billion(v: float | int | None) -> float | None:
    return None if v is None else round(float(v) / WON_PER_BILLION, 0)


def _build_fin_rows(facts: list[FinancialFact], market: MarketSnapshot) -> list[dict[str, Any]]:
    """연도별 매출/영업이익/순이익(십억) + 최신연도 멀티플."""
    by_period: dict[str, dict[str, Any]] = {}
    for f in facts:
        slot = by_period.setdefault(f.period, {})
        if f.metric_name == "revenue":
            slot["revenue"] = _won_to_billion(f.value)
        elif f.metric_name == "operating_income":
            slot["op"] = _won_to_billion(f.value)
        elif f.metric_name == "net_income":
            slot["np"] = _won_to_billion(f.value)
    ratios = compute_period_ratios(facts)  # period -> {roe, ...} (% 단위)
    rows = []
    periods = sorted(by_period.keys())  # FY2022, FY2023, ...
    for i, period in enumerate(periods):
        year = period.replace("FY", "")
        is_last = i == len(periods) - 1
        rows.append(
            {
                "year": f"{year}A",
                "revenue": by_period[period].get("revenue"),
                "op": by_period[period].get("op"),
                "np": by_period[period].get("np"),
                "per": market.per if is_last else None,       # 멀티플은 최신연도 시장값
                "roe": ratios.get(period, {}).get("roe"),     # ROE는 재무로 연도별 계산
                "pbr": market.pbr if is_last else None,
                "ev_ebitda": None,                            # EBITDA 분해 필요 — 후속
                "dy": market.div_yield_pct if is_last else None,
            }
        )
    return rows


def assemble_view(
    request: dict[str, Any],
    market: MarketSnapshot,
    facts: list[FinancialFact],
    peers: list[dict[str, Any]] | None = None,
    holders: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    entity = request["primary_entity"]["corp_name"]
    code = request["primary_entity"].get("stock_code") or ""
    meta_cfg = request.get("report_meta", {}) or {}
    profile = _profile(request.get("sector_id"))

    rating_label = (meta_cfg.get("rating") or "N/A").upper()
    label_ko = {"BUY": "매수", "HOLD": "중립", "SELL": "매도"}.get(rating_label, "검토중")
    target = meta_cfg.get("target_price")
    upside = None
    if target and market.current_price:
        upside = f"{(target / market.current_price - 1) * 100:+.0f}%"

    view: dict[str, Any] = {
        "draft_status": "DRAFT — QA 미승인",
        "sector_id": request.get("sector_id"),
        "meta": {
            "entity": entity,
            "code": code,
            "slogan": meta_cfg.get("slogan", "GIC여 긱스럽게 도전하라"),
            "author": meta_cfg.get("author", "GIC 4기"),
            "as_of": request.get("as_of_date", ""),
        },
        "rating": {
            "label": rating_label,
            "label_ko": label_ko,
            "target_price": target,
            "upside": upside,
        },
        "revision": {
            "current_price": market.current_price,
            "market_cap_eok": market.market_cap_eok,
            "shares_mn": market.shares_outstanding_mn,
            "float_pct": None,  # 유동주식비율: OpenDART/별도 — 미수집 시 —
            "high_52w": market.high_52w,
            "low_52w": market.low_52w,
            "avg_trade_eok": market.avg_trade_value_60d_eok,
            "foreign_pct": market.foreign_ratio_pct,
        },
        "holders": holders or [],
        "price_series": market.price_series,
        "check_points": [
            {"hint": profile["points"][0]["hint"]},
            {"hint": profile["points"][1]["hint"] if len(profile["points"]) > 1 else ""},
            {"hint": profile["points"][2]["hint"] if len(profile["points"]) > 2 else ""},
        ],
        "fin_rows": _build_fin_rows(facts, market),
        "contents": CONTENTS,
        "sections": {
            "industry": profile["industry"],
            "company": profile["company"],
            "points": profile["points"],
            "risks": profile["risks"],
        },
        "peers": peers or [],
        "compliance": COMPLIANCE,
    }
    return view
