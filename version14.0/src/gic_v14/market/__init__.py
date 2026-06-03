"""시장(KRX) 데이터 수집 — pykrx 우선, FinanceDataReader 옵션.

OpenDART에 없는 주가·시가총액·거래량·PER/PBR/배당·외국인지분율을 무료로 가져온다.
키·결제 불필요. 네트워크 실패 시 graceful degradation(해당 칸 unavailable).
"""
