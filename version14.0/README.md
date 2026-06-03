# GIC v14 — 기업/산업 리서치 자동화 + 프롬프트 팩

OpenDART(재무·공시)와 KRX(주가·멀티플) **무료 공개데이터**로 GIC 공식 양식 리포트를
자동 생성하고, 정성 분석은 **데이터가 미리 주입된 프롬프트**로 사람이 완성하는 하이브리드 시스템.

> **처음이면 [시작하기.md](시작하기.md) 부터 보세요. (5분)**

## 무엇을 만들어 주나

`input/`에 종목코드 하나 넣고 실행하면 `output/<run_id>/`에:

- **`deliverables/report.html`** — GIC 양식 그대로(표지·산업·기업·투자포인트·리스크·밸류에이션 7p). 주가차트·재무표·피어비교가 자동으로 채워짐. 정성 칸은 `[작성 필요]`.
- **`deliverables/prompt_pack.md`** — v9 계보의 단계별(Step 0~8) 프롬프트. **수집한 실제 수치가 미리 박혀** 있어, ChatGPT/Claude/Gemini/Antigravity에 복붙하면 정성 서술이 완성됨.
- **`audit/qa_report.md`** — 무엇이 자동 수집됐고 무엇이 사람 몫인지.

## 왜 이렇게 (설계 철학)

리서치는 ① **하드 데이터**(주가·재무·멀티플·피어)와 ② **정성 해석**(산업·투자논리)으로 나뉜다.
v14는 ①을 무료로 정확히 자동화하고, ②는 억지로 자동화하지 않는다 — 대신 ①을 인용한 **프롬프트**로 사람을 돕는다.

- 유료 LLM/데이터 의존 **0원**. 외부 인증값은 **무료 OpenDART 키 하나**. (시장데이터 pykrx는 키도 불필요)
- 못 구한 값은 **추정하지 않고** `—`(미수집)로 두고 QA가 표시.
- 프롬프트가 최종 산출물에 **항상 남는다** — AI 구독이 없거나 코드를 못 다루는 부원도 사용 가능.

## 리포트 3종

| 종류 | 양식 | 비고 |
|---|---|---|
| 기업 리서치 | 세로 양식(현재 구현) | |
| 산업 리서치 | **기업과 동일 세로 양식** | + 가로 PPT는 후속 |
| 산업 Top Pick | 자유 양식 | 후속 |

## 폴더 구조 (부원은 `input/`만 만지면 됨)

```text
version14.0/
├─ 시작하기.md            ← 제일 먼저
├─ README.md
├─ input/                 ← ✏️ 여기만 수정 (company_request.yaml)
├─ output/                ← 📦 결과 자동 생성
├─ templates/             ← 양식 HTML 템플릿 + assets(로고·배경)
├─ prompts/               ← 프롬프트 원본
├─ src/gic_v14/           ← ⚙️ 코드 (안 만져도 됨)
│   ├─ opendart/  market/  model/  normalize/  render/  promptpack/
│   ├─ view.py  pipeline.py  cli.py
├─ docs/                  ← 설계서(DESIGN_v14.md)
└─ tests/
```

## 실행 요약

```powershell
python -m pip install -e .
$env:OPENDART_API_KEY="본인_키"
python -m gic_v14.cli run input\company_request.yaml --output-dir output
```

옵션:
- `--no-live-market` : pykrx 실시간 끄기
- `--market-fixture <json>` / `--fixture-dir <dir>` : 오프라인(키 없이) 테스트

## 지표 근거 + 연구 시각화 (research/)

프롬프트가 "어떤 지표를 분석해야 하는지"를 **학술·실무 근거**로 안내합니다.

- **근거**: 국내 KCI/DBpia 실증연구(Ohlson 모형, AHP 18변수, 저PER·저PBR 효과, PBR 결정요인) + 국제(Damodaran 멀티플, ROIC/EVA/WACC, DuPont). 출처는 `src/gic_v14/research/indicators.py`에 인용.
- **지표 라이브러리**: PER·PBR·EV/EBITDA·PCR·PSR / OPM·NPM·GPM·ROE·ROA·ROIC·EVA / 매출CAGR·순이익·EPS성장 / 회전율(자산·재고·매출채권) / 부채비율·유동비율·순부채 / FCF·CAPEX강도 / 배당수익률·배당성향 + **섹터 KPI**(예: 반도체 DRAM/NAND ASP·Bit Growth·HBM 믹스·가동률·재고일수).
- **문헌 크롤 + 시각화** (무료, OpenAlex, 키 불필요):

```powershell
python -m gic_v14.cli research --output-dir research          # 라이브 크롤
python -m gic_v14.cli research --offline                       # 내장 근거만
```

→ `research/<날짜>_지표연구.html` 에 지표 맵·문헌 개념 빈도·참고문헌·출처를 시각화(브라우저로 열기). 연구가 쌓이면 이 폴더에 누적됩니다.

## 데이터 출처 매핑

| 양식 항목 | 출처 |
|---|---|
| 매출·영업이익·순이익, 사업부문 | OpenDART |
| 현재가·52주·거래액·시총·발행주식·PER/PBR/배당·외국인 | KRX (pykrx) |
| 주요주주 | OpenDART (후속 연결) |
| 목표주가·투자의견·정성서술 | 사람 (prompt_pack) |
| 피어 비교 | OpenDART + pykrx |

## 테스트

```powershell
python -m pytest tests -q
```

## 보안

- OpenDART 키는 **환경변수/세션 입력만**. 코드·결과물·Git에 저장 금지.
- 자동 스케줄/메일은 v13의 [에이전트 가이드](../version13.0/docs/AGENT_AUTOMATION_GUIDE.md)와 동일 방식(GitHub Secrets).

## 한계 / 후속

- 영업이익률·ROE·EV/EBITDA 등 피어 비율은 현재 PER/PBR 위주 → 피어 OpenDART 재무 연결(v14.1).
- 주요주주(최대주주현황 API), 사업부문 매출 자동 파싱, 산업 가로 PPT, Top Pick 자유 양식은 후속.
- 일부 KRX 엔드포인트는 간헐적으로 막힐 수 있음 → 해당 값은 `—`로 표기(추정 안 함).
