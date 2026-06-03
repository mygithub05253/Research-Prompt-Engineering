"""ReportView → prompt_pack.md.

핵심 산출물. 자동 수집한 실제 수치/공식을 단계별 프롬프트에 미리 주입해,
부원이 ChatGPT/Claude/Gemini/Antigravity에 '그대로 복붙'하면 정성 서술을 완성하도록 한다.
v9 규칙 계승: 4중 백틱 펜스(잘림 0), [대괄호] 채우기, AI별 분기, 10블록 라이브러리.
"""

from __future__ import annotations

from typing import Any

from gic_v14.research.indicators import recommended_indicator_lines

FENCE = "````"  # 4중 백틱: 내부 ```mermaid 등이 들어가도 안 잘림


def _digest(view: dict[str, Any]) -> str:
    """자동주입 데이터 다이제스트(프롬프트가 인용할 실제 수치)."""
    rows = view.get("fin_rows", [])
    lines = []
    for r in rows:
        rev = "—" if r["revenue"] is None else f"{r['revenue']:,.0f}"
        op = "—" if r["op"] is None else f"{r['op']:,.0f}"
        opm = ""
        if r["revenue"] and r["op"]:
            opm = f", 영업이익률 {r['op']/r['revenue']*100:.1f}%"
        lines.append(f"- {r['year']}: 매출 {rev}십억, 영업이익 {op}십억{opm}")
    # CAGR
    nums = [r["revenue"] for r in rows if r["revenue"]]
    if len(nums) >= 2 and nums[0]:
        cagr = ((nums[-1] / nums[0]) ** (1 / (len(nums) - 1)) - 1) * 100
        lines.append(f"- 매출 CAGR(기간 평균): {cagr:.1f}%")
    rev_box = view.get("revision", {})
    mk = []
    if rev_box.get("current_price"):
        mk.append(f"현재가 {rev_box['current_price']:,.0f}원")
    if rev_box.get("market_cap_eok"):
        mk.append(f"시총 {rev_box['market_cap_eok']:,.0f}억원")
    if rev_box.get("foreign_pct"):
        mk.append(f"외국인 {rev_box['foreign_pct']:.1f}%")
    fr = view.get("fin_rows", [])
    if fr:
        last = fr[-1]
        if last.get("per"):
            mk.append(f"PER {last['per']:.1f}배")
        if last.get("pbr"):
            mk.append(f"PBR {last['pbr']:.1f}배")
        if last.get("dy"):
            mk.append(f"배당수익률 {last['dy']:.1f}%")
    if mk:
        lines.append("- 시장지표: " + ", ".join(mk))
    peers = view.get("peers", [])
    if peers:
        ptxt = "; ".join(
            f"{p['name']}(PER {p.get('per','—')}, ROE {p.get('roe','—')})" for p in peers
        )
        lines.append(f"- 피어: {ptxt}")
    return "\n".join(lines) if lines else "- (자동 수집 데이터 없음 — 수동 입력 필요)"


def _step(no: str, title: str, fills: str, output: str) -> str:
    return f"""## Step {no} — {title}

{FENCE}
{fills.strip()}

[출력]
{output.strip()}
{FENCE}
"""


def build_prompt_pack(view: dict[str, Any]) -> str:
    meta = view["meta"]
    entity = meta["entity"]
    code = meta["code"]
    digest = _digest(view)
    indicator_block = "\n".join(recommended_indicator_lines(view.get("sector_id")))

    header = f"""# GIC 리서치 프롬프트 팩 — {entity} ({code})

> 생성: GIC v14 자동 파이프라인 · 기준일 {meta['as_of']}
> **이 프롬프트는 그대로 복사해서 ChatGPT · Claude · Gemini · Antigravity 등 어떤 AI 챗봇에 붙여넣어도 동작합니다.**
> API 키·코드 불필요. `[대괄호]`만 본인 분석에 맞게 채우세요.

## 사용 방법

1. 아래 각 Step의 **4중 백틱(```` ```` ````) 펜스 안 텍스트만** 복사 (펜스 줄은 제외).
2. AI 챗봇에 붙여넣고, `[대괄호]`를 채운다.
3. Step 0 → 1 → ... → 8 순서로 진행. 앞 단계 답을 다음 단계에 이어붙인다.
4. 결과 문장을 `report.html`의 `[작성 필요]` 칸에 옮긴다.

## 자동주입 데이터 (이 수치를 근거로 쓰세요)

```
{digest}
```

## 분석해야 할 지표 (학술·실무 근거 — 이 지표들을 우선 분석하세요)

이 목록은 국내 KCI/DBpia 실증연구와 Damodaran·McKinsey 프레임워크에서 도출했습니다.
(상세 근거·문헌은 `research/` 폴더의 지표연구 HTML 참조)

```
{indicator_block}
```

## 10블록 라이브러리 (전 단계 공통 적용)

A 용어번역기 · B Sanity Check · C 핵심비유 · D Mermaid 다이어그램 · E 검증태그
F Red Team(공매도 관점) · G Evidence Card(근거 3건+출처+신뢰도) · H 유사사례 인과추론
I 5개년 Forward 모델링 · **J Anti-Hallucination**(추측 금지·Missing Data 표기·출처/시점 의무)

---
"""

    steps = []
    steps.append(_step(
        "0", "초기 설정 / Anti-Hallucination",
        f"""당신은 가천대학교 투자동아리 GIC의 기업 리서치 애널리스트입니다.
분석 대상: {entity} ({code}) · 섹터: [섹터] · 기준일: {meta['as_of']} · 독자수준: [초급/중급]
[블록 J] 모든 수치는 공개자료(OpenDART·KRX)에서만 인용, 모르는 값은 "Data unavailable"로 표기,
각 수치 옆 (출처, 시점) 의무, 추측 금지. 위 '자동주입 데이터'를 1차 근거로 사용.""",
        "1) 기업 1줄 요약 2) 섹터 핵심키워드 3~5개 3) 집중 재무지표 4) 데이터 체크리스트",
    ))
    steps.append(_step(
        "1", "산업분석 (양식 p.산업분석)",
        f"""{entity}가 속한 산업을 분석하라. 자동주입된 매출/CAGR을 산업 수급·가격 사이클과 연결하라.
[블록 C 비유] [블록 D Mermaid 밸류체인] 포함.""",
        "제목문장 2개 + 각 문단설명(3~5문장). 시장규모·성장률·경쟁구도는 [출처] 표기.",
    ))
    steps.append(_step(
        "2", "기업분석 (양식 p.기업분석)",
        f"""{entity}의 사업부 구조·경쟁력·지배구조를 분석하라. 자동주입 영업이익률 추이를 사업부 믹스로 설명하라.""",
        "제목문장 2개 + 문단설명. 사업부별 매출비중 표 + 지배구조 Mermaid.",
    ))
    steps.append(_step(
        "3", "투자포인트 (Point 1·2·3)",
        f"""{entity} 매수논리 3개. 각 포인트는 [블록 G Evidence Card]로 근거 3건+출처+신뢰도, [블록 I]로 5개년 영향.""",
        "Point 1·2·3 각 제목 + 3~5문장 + Evidence Card.",
    ))
    steps.append(_step(
        "4", "투자리스크 (Red Team)",
        f"""[블록 F] 공매도 애널리스트 페르소나로 {entity} 투자논리를 공격하라. 하방 시나리오·민감도 포함.""",
        "Risk 1·2 각 제목 + 메커니즘 + 정량 민감도(가능 시).",
    ))
    steps.append(_step(
        "5", "밸류에이션 / 목표주가",
        f"""자동주입 멀티플(PER/PBR/배당)과 피어 비교를 사용해 {entity} 적정가치를 산출하라.
방법: PER·PBR·EV/EBITDA·DCF 중 2개 이상 교차검증. 공식과 가정을 모두 표기.""",
        "목표주가 범위 + 산출근거(공식·가정) + 현재가 대비 상승여력 + 피어 대비 할인/할증.",
    ))
    steps.append(_step(
        "6", "교차검증 / 결론",
        f"""Step 1~5의 충돌을 점검하고(Sanity Check), {entity} 투자의견(BUY/HOLD/SELL)과 한 줄 논거를 확정하라.""",
        "투자의견 + 1줄 논거 + 핵심 가정이 틀릴 경우의 falsifier 3개.",
    ))
    steps.append(_step(
        "8", "표지 Check Point 3줄 요약",
        f"""위 분석을 {entity} 표지의 Point 1·2·3 (각 1~2문장)으로 압축하라. 투자자가 30초에 이해하도록.""",
        "Point 1 / Point 2 / Point 3 — 각 1~2문장.",
    ))

    return header + "\n".join(steps) + "\n---\n> 본 팩은 GIC v14가 자동 생성했습니다. 작성 결과는 사람 검토 후 사용하세요.\n"
