"""문헌 근거 지표 라이브러리.

각 지표에 '왜 보는지(근거)'와 '출처'를 붙여, 프롬프트 팩과 리포트가
'실제 기업·학술이 분석하는 지표'를 정확히 따르도록 한다.
출처는 아래 SOURCES 참조(국내 KCI/DBpia + 국제 Damodaran/CFA/Morgan Stanley).
"""

from __future__ import annotations

from typing import Any

SOURCES: dict[str, str] = {
    "KCI_OHLSON": "재무비율에 의한 기업가치평가와 투자 (KCI ART001238342) — Ohlson Model; 매출총이익률·영업자산회전율·재무레버리지·매출이 기업가치에 유의(1% 수준).",
    "DBPIA_AHP18": "구승환·신택현·율다세브(2015), AHP·로짓회귀 기업가치 분석 (DBpia NODE07214616) — 18개 변수(PER·PBR·PCR·EV/EBITDA·ROE·순이익증가율·매출성장률·부채비율·유동비율·재고/매출채권회전율·영업이익률·매출액순이익률·ROA·EPS성장률·배당수익률 등) 사용 시 정확도 91.98%.",
    "KCI_LOWPER": "주가배수 평가모형과 저PER·저PBR 효과 실증연구 (KCI ART000895822).",
    "KCI_VALUE": "가치주와 장기투자성과의 관련성 (KCI ART001473219) — E/P·S/P 가치투자전략의 초과수익.",
    "IKSA_PBR": "코리아 디스카운트·PBR 결정요인 연구 (iksa) — PBR/PER·ROE·ROA·CAPEX·배당성향.",
    "DAMODARAN": "Aswath Damodaran, Valuation (NYU Stern) — 멀티플은 분자·분모의 청구권 일치(equity↔equity, firm↔firm); EV/EBITDA·EV/Sales·PER.",
    "MCKINSEY_ROIC": "Morgan Stanley / McKinsey — 경제적이익 EVA=(ROIC−WACC)×투하자본; ROIC=NOPAT마진×투하자본회전율.",
    "DUPONT": "DuPont 분해 — ROE = 순이익률 × 총자산회전율 × 재무레버리지.",
}

# category: 수익성/성장성/안정성/활동성/멀티플/현금흐름/주주환원/가치창출
INDICATOR_LIBRARY: list[dict[str, Any]] = [
    # ── 밸류에이션 멀티플 ──
    {"id": "PER", "ko": "주가수익비율(PER)", "cat": "멀티플", "formula": "주가 / EPS", "auto": True,
     "why": "이익 대비 가격. 저PER 효과 실증. 동종 비교의 출발점.", "src": ["KCI_LOWPER", "DAMODARAN"]},
    {"id": "PBR", "ko": "주가순자산비율(PBR)", "cat": "멀티플", "formula": "주가 / BPS", "auto": True,
     "why": "장부가 대비 가격. 코리아 디스카운트·저PBR 효과 핵심 변수.", "src": ["IKSA_PBR", "KCI_LOWPER"]},
    {"id": "EV_EBITDA", "ko": "EV/EBITDA", "cat": "멀티플", "formula": "(시총+순부채) / EBITDA", "auto": False,
     "why": "자본구조·감가상각 차이에 둔감한 firm-level 멀티플. 비교 신뢰도 높음.", "src": ["DAMODARAN", "DBPIA_AHP18"]},
    {"id": "PCR", "ko": "주가현금흐름비율(PCR)", "cat": "멀티플", "formula": "주가 / 주당영업현금흐름", "auto": False,
     "why": "이익 조정 영향이 적은 현금흐름 기준 가격. AHP 18변수 포함.", "src": ["DBPIA_AHP18"]},
    {"id": "PSR_SP", "ko": "주가매출비율(PSR)/S·P", "cat": "멀티플", "formula": "시총 / 매출", "auto": False,
     "why": "적자·초기기업 평가. S/P 가치전략 초과수익 보고.", "src": ["KCI_VALUE", "DAMODARAN"]},
    # ── 수익성 ──
    {"id": "OPM", "ko": "영업이익률", "cat": "수익성", "formula": "영업이익 / 매출", "auto": True,
     "why": "본업 수익성. AHP 18변수·Ohlson 유의.", "src": ["DBPIA_AHP18", "KCI_OHLSON"]},
    {"id": "NPM", "ko": "매출액순이익률", "cat": "수익성", "formula": "순이익 / 매출", "auto": True,
     "why": "최종 마진. DuPont 첫 항.", "src": ["DBPIA_AHP18", "DUPONT"]},
    {"id": "GPM", "ko": "매출총이익률", "cat": "수익성", "formula": "매출총이익 / 매출", "auto": False,
     "why": "원가 경쟁력. Ohlson 모형에서 기업가치에 유의.", "src": ["KCI_OHLSON"]},
    {"id": "ROE", "ko": "자기자본이익률(ROE)", "cat": "수익성", "formula": "순이익 / 자기자본", "auto": False,
     "why": "주주자본 수익성. DuPont 분해로 마진·회전율·레버리지 원천 추적.", "src": ["DUPONT", "DBPIA_AHP18", "IKSA_PBR"]},
    {"id": "ROA", "ko": "총자본순이익률(ROA)", "cat": "수익성", "formula": "순이익 / 총자산", "auto": False,
     "why": "자산 효율. PBR 결정요인.", "src": ["DBPIA_AHP18", "IKSA_PBR"]},
    {"id": "ROIC", "ko": "투하자본이익률(ROIC)", "cat": "가치창출", "formula": "NOPAT / 투하자본", "auto": False,
     "why": "ROIC>WACC일 때만 가치창출(EVA>0). 밸류에이션의 핵심 동인.", "src": ["MCKINSEY_ROIC"]},
    {"id": "EVA", "ko": "경제적부가가치(EVA)", "cat": "가치창출", "formula": "(ROIC − WACC) × 투하자본", "auto": False,
     "why": "자본비용 초과 이익. 진짜 가치창출 여부.", "src": ["MCKINSEY_ROIC"]},
    # ── 성장성 ──
    {"id": "REV_CAGR", "ko": "매출성장률/CAGR", "cat": "성장성", "formula": "(말기/초기)^(1/n) − 1", "auto": True,
     "why": "외형 성장. AHP 18변수.", "src": ["DBPIA_AHP18"]},
    {"id": "NI_GROWTH", "ko": "순이익증가율", "cat": "성장성", "formula": "당기순이익 YoY", "auto": True,
     "why": "이익 성장. AHP 18변수.", "src": ["DBPIA_AHP18"]},
    {"id": "EPS_GROWTH", "ko": "EPS 성장률", "cat": "성장성", "formula": "EPS YoY", "auto": False,
     "why": "주당이익 성장. PEG의 분모.", "src": ["DBPIA_AHP18"]},
    # ── 활동성(회전율) ──
    {"id": "ATO", "ko": "총자산/영업자산회전율", "cat": "활동성", "formula": "매출 / 자산", "auto": False,
     "why": "자산 효율. Ohlson 모형 유의·DuPont 둘째 항.", "src": ["KCI_OHLSON", "DUPONT"]},
    {"id": "INV_TO", "ko": "재고자산회전율", "cat": "활동성", "formula": "매출원가 / 평균재고", "auto": False,
     "why": "재고 효율(반도체 사이클 민감). AHP 18변수.", "src": ["DBPIA_AHP18"]},
    {"id": "AR_TO", "ko": "매출채권회전율", "cat": "활동성", "formula": "매출 / 평균매출채권", "auto": False,
     "why": "운전자본 회수. AHP 18변수.", "src": ["DBPIA_AHP18"]},
    # ── 안정성/레버리지 ──
    {"id": "DEBT_RATIO", "ko": "부채비율", "cat": "안정성", "formula": "부채 / 자기자본", "auto": False,
     "why": "재무 안정성·레버리지. Ohlson FLEV 유의·AHP 18변수.", "src": ["KCI_OHLSON", "DBPIA_AHP18"]},
    {"id": "CURRENT", "ko": "유동비율", "cat": "안정성", "formula": "유동자산 / 유동부채", "auto": False,
     "why": "단기 지급능력. AHP 18변수.", "src": ["DBPIA_AHP18"]},
    {"id": "NET_DEBT", "ko": "순부채", "cat": "안정성", "formula": "총차입금 − 현금성자산", "auto": True,
     "why": "실질 차입. EV 산출·재무여력.", "src": ["DAMODARAN"]},
    # ── 현금흐름 ──
    {"id": "FCF", "ko": "잉여현금흐름(FCF)", "cat": "현금흐름", "formula": "영업현금흐름 − CAPEX", "auto": True,
     "why": "실제 창출 현금. DCF·주주환원 여력의 원천.", "src": ["DAMODARAN", "MCKINSEY_ROIC"]},
    {"id": "CAPEX_INT", "ko": "CAPEX 강도", "cat": "현금흐름", "formula": "CAPEX / 매출", "auto": True,
     "why": "자본집약도(반도체 핵심). PBR 결정요인.", "src": ["IKSA_PBR"]},
    # ── 주주환원 ──
    {"id": "DY", "ko": "배당수익률(DY)", "cat": "주주환원", "formula": "주당배당 / 주가", "auto": True,
     "why": "현금 수익률. AHP 18변수·코리아디스카운트 논의.", "src": ["DBPIA_AHP18", "IKSA_PBR"]},
    {"id": "PAYOUT", "ko": "배당성향", "cat": "주주환원", "formula": "배당 / 순이익", "auto": False,
     "why": "이익 환원 정도. PBR 결정요인.", "src": ["IKSA_PBR"]},
]

# 섹터별 추가 KPI(비표준, 사업보고서/IR에서 수집·서술) — 실무 분석 관점
SECTOR_KPIS: dict[str, list[dict[str, str]]] = {
    "SEMICONDUCTOR": [
        {"kpi": "DRAM/NAND ASP", "why": "메모리 가격 사이클의 핵심 동인(매출·마진 직결)."},
        {"kpi": "Bit Growth(출하 증가율)", "why": "수량 성장. ASP와 함께 메모리 매출 분해."},
        {"kpi": "HBM 매출비중", "why": "AI 메모리 고부가 믹스. 마진 레버리지."},
        {"kpi": "가동률·수율(파운드리)", "why": "비메모리 수익성·턴어라운드 신호."},
        {"kpi": "재고일수(DIO)", "why": "다운사이클 진입·탈출 선행지표."},
        {"kpi": "CAPEX/매출", "why": "공급 증설 강도 → 향후 수급."},
    ],
    "GENERIC": [
        {"kpi": "시장점유율", "why": "경쟁 지위."},
        {"kpi": "전방 수요 동인", "why": "매출 성장의 근본 원인."},
        {"kpi": "원가 구조", "why": "마진 방어력."},
    ],
}


def indicators_for_sector(sector_id: str | None) -> dict[str, Any]:
    """섹터에 맞는 표준 지표 + 섹터 KPI 묶음 반환."""
    sec = (sector_id or "GENERIC").upper()
    return {
        "standard": INDICATOR_LIBRARY,
        "sector_kpis": SECTOR_KPIS.get(sec, SECTOR_KPIS["GENERIC"]),
        "sector_id": sec,
    }


def recommended_indicator_lines(sector_id: str | None) -> list[str]:
    """프롬프트 팩에 주입할 '분석해야 할 지표' 라인."""
    lines = []
    for ind in INDICATOR_LIBRARY:
        srcs = ", ".join(ind["src"])
        lines.append(f"- [{ind['cat']}] {ind['ko']} = {ind['formula']} · 이유: {ind['why']} (근거: {srcs})")
    for kpi in SECTOR_KPIS.get((sector_id or "GENERIC").upper(), SECTOR_KPIS["GENERIC"]):
        lines.append(f"- [섹터KPI] {kpi['kpi']} · {kpi['why']}")
    return lines
