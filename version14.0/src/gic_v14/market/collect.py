"""KRX 시장데이터 수집기.

각 항목을 개별 try/except로 감싸 하나가 실패해도 나머지는 채운다.
값을 못 구하면 None으로 두고(=unavailable) QA가 표시한다. 추정하지 않는다.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


@dataclass
class MarketSnapshot:
    """양식 표지의 시장데이터 묶음. 단위는 필드명 주석 참고."""

    stock_code: str
    as_of_date: str
    current_price: float | None = None          # 현재주가(원)
    market_cap_eok: float | None = None          # 시가총액(억원)
    shares_outstanding_mn: float | None = None   # 발행주식수(백만주)
    high_52w: float | None = None                # 52주 최고가(원)
    low_52w: float | None = None                 # 52주 최저가(원)
    avg_trade_value_60d_eok: float | None = None # 일평균 거래액 60일(억원)
    foreign_ratio_pct: float | None = None       # 외국인 지분율(%)
    per: float | None = None
    pbr: float | None = None
    eps: float | None = None
    bps: float | None = None
    div_yield_pct: float | None = None           # 배당수익률 DY(%)
    price_series: list[dict[str, Any]] = field(default_factory=list)  # [{date, close}]
    unavailable: list[str] = field(default_factory=list)
    source: str = "KRX/pykrx"

    def to_plain(self) -> dict[str, Any]:
        return asdict(self)


def _ymd(d: str) -> str:
    return d.replace("-", "")


def collect_market(stock_code: str, as_of_date: str) -> MarketSnapshot:
    """pykrx로 시장데이터를 수집한다. pykrx 미설치/네트워크 실패 시 빈 스냅샷 반환."""
    snap = MarketSnapshot(stock_code=stock_code, as_of_date=as_of_date)
    try:
        from pykrx import stock  # type: ignore
    except Exception:
        snap.unavailable.append("pykrx_not_available")
        return snap

    end = _ymd(as_of_date)
    start_1y = _ymd((datetime.strptime(as_of_date, "%Y-%m-%d") - timedelta(days=365)).strftime("%Y-%m-%d"))
    start_60d = _ymd((datetime.strptime(as_of_date, "%Y-%m-%d") - timedelta(days=95)).strftime("%Y-%m-%d"))

    # 1년 OHLCV → 현재가/52주 최고저/주가 시계열
    try:
        ohlcv = stock.get_market_ohlcv(start_1y, end, stock_code)
        if ohlcv is not None and len(ohlcv) > 0:
            close = ohlcv["종가"]
            snap.current_price = float(close.iloc[-1])
            snap.high_52w = float(ohlcv["고가"].max())
            snap.low_52w = float(ohlcv["저가"].min())
            # 주가 시계열(월말 샘플링으로 가볍게)
            monthly = close.resample("ME").last().dropna() if hasattr(close, "resample") else close
            snap.price_series = [
                {"date": idx.strftime("%Y-%m"), "close": float(val)}
                for idx, val in monthly.items()
            ]
    except Exception:
        snap.unavailable.append("ohlcv")

    # 60일 거래대금 평균(억원)
    try:
        ohlcv60 = stock.get_market_ohlcv(start_60d, end, stock_code)
        if ohlcv60 is not None and "거래대금" in ohlcv60.columns and len(ohlcv60) > 0:
            snap.avg_trade_value_60d_eok = round(float(ohlcv60["거래대금"].tail(60).mean()) / 1e8, 1)
    except Exception:
        snap.unavailable.append("trade_value")

    # 펀더멘털: PER/PBR/EPS/BPS/DIV
    try:
        fund = stock.get_market_fundamental(end, end, stock_code)
        if fund is not None and len(fund) > 0:
            row = fund.iloc[-1]
            snap.per = _num(row.get("PER"))
            snap.pbr = _num(row.get("PBR"))
            snap.eps = _num(row.get("EPS"))
            snap.bps = _num(row.get("BPS"))
            snap.div_yield_pct = _num(row.get("DIV"))
    except Exception:
        snap.unavailable.append("fundamental")

    # 시가총액(억원) / 발행주식수(백만주)
    try:
        cap = stock.get_market_cap(end, end, stock_code)
        if cap is not None and len(cap) > 0:
            row = cap.iloc[-1]
            mc = _num(row.get("시가총액"))
            snap.market_cap_eok = round(mc / 1e8, 0) if mc else None
            sh = _num(row.get("상장주식수"))
            snap.shares_outstanding_mn = round(sh / 1e6, 0) if sh else None
    except Exception:
        snap.unavailable.append("market_cap")

    # 외국인 지분율(%)
    try:
        foreign = stock.get_exhaustion_rates_of_foreign_investment(end, stock_code)
        if foreign is not None and len(foreign) > 0 and "지분율" in foreign.columns:
            snap.foreign_ratio_pct = _num(foreign.iloc[-1].get("지분율"))
    except Exception:
        snap.unavailable.append("foreign_ratio")

    return snap


def _num(v: Any) -> float | None:
    try:
        if v is None:
            return None
        f = float(v)
        return None if f != f else f  # NaN 방어
    except (TypeError, ValueError):
        return None


def load_market_fixture(path: str | Path) -> MarketSnapshot:
    """오프라인 테스트용 시장데이터 fixture(JSON)를 MarketSnapshot으로."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return MarketSnapshot(**data)
