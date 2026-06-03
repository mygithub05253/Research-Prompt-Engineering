"""지표 라이브러리의 '자동' 항목을 OpenDART facts로 실제 계산.

OPM/NPM/GPM/ROE/ROA/부채비율/FCF/CAPEX강도/순부채 + 성장성(매출CAGR·순이익증가율).
값이 없으면 None(추정 안 함). 단위: 비율은 % 또는 배, 금액은 KRW.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from gic_v14.domain import FinancialFact


def _by_period(facts: list[FinancialFact]) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = defaultdict(dict)
    for f in facts:
        if f.value is not None:
            out[f.period][f.metric_name] = float(f.value)
    return out


def _div(a: float | None, b: float | None) -> float | None:
    if a is None or b in (None, 0):
        return None
    return a / b


def compute_period_ratios(facts: list[FinancialFact]) -> dict[str, dict[str, float | None]]:
    """기간별 재무비율(%, 배, KRW)."""
    bp = _by_period(facts)
    result: dict[str, dict[str, float | None]] = {}
    for period, m in bp.items():
        rev, op, ni = m.get("revenue"), m.get("operating_income"), m.get("net_income")
        eq, asset, cogs = m.get("total_equity"), m.get("total_assets"), m.get("cogs")
        ocf, capex = m.get("operating_cash_flow"), m.get("capex")
        debt, cash = m.get("total_debt"), m.get("cash")
        gp = m.get("gross_profit")
        if gp is None and rev is not None and cogs is not None:
            gp = rev - cogs
        result[period] = {
            "opm": _pct(_div(op, rev)),
            "npm": _pct(_div(ni, rev)),
            "gpm": _pct(_div(gp, rev)),
            "roe": _pct(_div(ni, eq)),
            "roa": _pct(_div(ni, asset)),
            "debt_ratio": _pct(_div(debt, eq)),
            "fcf": (ocf - capex) if (ocf is not None and capex is not None) else None,
            "capex_intensity": _pct(_div(capex, rev)),
            "net_debt": (debt - cash) if (debt is not None and cash is not None) else None,
            "revenue": rev,
            "operating_income": op,
            "net_income": ni,
        }
    return result


def _pct(v: float | None) -> float | None:
    return None if v is None else round(v * 100, 1)


def growth(facts: list[FinancialFact]) -> dict[str, float | None]:
    """매출 CAGR, 순이익 증가율(최신 YoY)."""
    bp = _by_period(facts)
    periods = sorted(bp.keys())
    rev = [bp[p].get("revenue") for p in periods if bp[p].get("revenue") is not None]
    ni = [bp[p].get("net_income") for p in periods if bp[p].get("net_income") is not None]
    out: dict[str, float | None] = {"revenue_cagr": None, "ni_yoy": None}
    if len(rev) >= 2 and rev[0] and rev[0] > 0:
        out["revenue_cagr"] = round(((rev[-1] / rev[0]) ** (1 / (len(rev) - 1)) - 1) * 100, 1)
    if len(ni) >= 2 and ni[-2]:
        out["ni_yoy"] = round((ni[-1] / ni[-2] - 1) * 100, 1)
    return out


def summary_row(name: str, facts: list[FinancialFact], market: Any = None) -> dict[str, Any]:
    """피어 비교표 한 행: 매출(십억)·OPM·ROE·ROA + 시장 PER/PBR."""
    r = latest_ratios(facts)
    rev = r.get("revenue")
    return {
        "name": name,
        "revenue": round(rev / 1e9, 0) if rev else None,
        "opm": r.get("opm"),
        "roe": r.get("roe"),
        "roa": r.get("roa"),
        "per": getattr(market, "per", None) if market else None,
        "pbr": getattr(market, "pbr", None) if market else None,
        "ev_ebitda": None,
    }


def latest_ratios(facts: list[FinancialFact]) -> dict[str, Any]:
    """최신 기간 비율 + 성장성을 한 dict로(피어 비교/요약용)."""
    pr = compute_period_ratios(facts)
    if not pr:
        return {**{k: None for k in ("opm", "npm", "roe", "roa", "debt_ratio")}, **growth(facts)}
    last = sorted(pr.keys())[-1]
    flat = dict(pr[last])
    flat.update(growth(facts))
    flat["period"] = last
    return flat
