"""피어(경쟁사) 벤치마킹 — 비교 행 모음에 '피어 평균'을 덧붙인다.

각 피어의 재무비율(OPM/ROE/ROA)은 pipeline이 financial_ratios.summary_row로 계산해 전달한다.
"""

from __future__ import annotations

from typing import Any


def append_peer_average(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """rows[0]=대상기업, rows[1:]=피어. 피어 평균 행을 추가해 반환."""
    if len(rows) <= 1:
        return rows
    peers = rows[1:]

    def _avg(key: str) -> float | None:
        vals = [r[key] for r in peers if isinstance(r.get(key), (int, float))]
        return round(sum(vals) / len(vals), 1) if vals else None

    avg = {
        "name": "피어 평균",
        "revenue": None,
        "opm": _avg("opm"),
        "per": _avg("per"),
        "roe": _avg("roe"),
        "roa": _avg("roa"),
        "pbr": _avg("pbr"),
        "ev_ebitda": _avg("ev_ebitda"),
    }
    return rows + [avg]
