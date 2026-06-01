# GIC 리서치 프롬프트 시스템 v10.0 — Claude Code 프로젝트 컨벤션

> **프로젝트**: GIC(Gachon Investment Club) 4기 리서치 프롬프트 자동화 시스템
> **버전**: v10.0 / 2026-05-09
> **루트**: `C:\Users\kik32\내 드라이브\Obsidian Vault\Obsidian_School\가천대학교\GIC\4기\GIC 리서치 프롬프트 모델 생성 프로젝트\version10.0`

---

## 1. 프로젝트 개요

본 프로젝트는 GIC 학회 부원이 **AI 챗봇 1개만으로** 정식 기업 리서치 보고서·위클리·산업 Top Pick을 생성할 수 있도록 설계된 **마크다운 프롬프트 시스템**이다. v10.0은 그 위에 Claude Code Skill 자동화를 얹어 **양식 노가다를 5분으로 압축**한다.

### 핵심 원칙 (v9.0 §9.1 + v10 신규)

1. **마크다운 .md 파일만, 외부 의존 0** (배포 형태)
2. **정식 9단계 + 블록 라이브러리(A~J)가 본질**
3. **외부 벤치마크는 흡수하되 본질 훼손 금지**
4. **한국 시장 환경은 텍스트 가이드만, 코드 강제 금지** (비전공자 진입장벽 0)
5. **자동화는 챗봇 복붙(티어 1)의 부속 옵션** — v9.0 본문 한 줄도 축소하지 않음
6. **Skill의 columns.md / rules.md = 학회 도메인 지식의 외화** (자동화 PDF "기술보다 업무 설명")
7. **단계별 게이트 의무** — 자동화 결과를 검증 없이 발표하면 v7.0 실패 재현
8. **챗봇 복붙 ≡ Skill 자동화 동등성** — 양식 명세(부록 C·D·E)와 columns.md는 1:1 동일

---

## 2. 폴더 구조 (v10.0)

```
version10.0/
├── prompts/                    [티어 1·2 — 챗봇 복붙, 모든 부원]
│   ├── GIC_기업리서치_v10.md           # 정식 9단계 + 부록 C 슬라이드 명세
│   ├── GIC_위클리투자리포트_v10.md     # 위클리 + 부록 D
│   ├── GIC_산업TopPick_v10.md          # Top Pick + 부록 E
│   └── GIC_사용설명서_v10.md           # 진입 가이드 + 티어 1·2·3·4·5
├── design/
│   ├── GIC_design-guide_v10.md        # 디자인 시스템 (학회 톤 + PPTX 호환성)
│   ├── GIC_양식_ver2.pptx              # 학회 표준 양식 원본
│   ├── GIC_양식_ver2.pdf               # PDF 참고용
│   ├── 양식_분석_결과.md                # python-pptx 분석 결과
│   └── 양식_분석_결과.json
├── templates/                  [티어 3 — Skill 출력 템플릿]
│   ├── 기업리서치_9p.pptx              # 학회 양식 슬라이드 마스터 (트랙 1)
│   ├── 위클리_4p.html                  # design-guide_v10 기반 (트랙 3)
│   ├── 산업TopPick_8p.html
│   └── Excel_5개년모델_v10.xlsx        # 학회 표준 (트랙 2)
├── .claude/                    [Claude Code 전용]
│   ├── CLAUDE.md (본 파일)
│   └── skills/
│       ├── gic-research/       # /gic-research [기업명]
│       ├── gic-excel/          # /gic-excel [기업명]
│       ├── gic-weekly/         # /gic-weekly [기업명]
│       └── gic-toppick/        # /gic-toppick [산업명]
├── data/samples/               # 테스트용 입력 (삼성전기 yaml 등)
├── docs/
│   ├── analyze_template.py     # 양식 분석 스크립트 (일회성)
│   ├── GIC_v10.0_변경사항.md
│   ├── GIC_v10.0_요약본.md
│   └── 자동위클리_설계.md       # 트랙 5 (구현은 v10.1+)
└── README_v10.md
```

---

## 3. Skill 호출 컨벤션

### 3.1 Skill 4종 표준 인터페이스

모든 Skill은 다음 표준을 따른다:

```
/<skill-name> [필수인자] [--옵션=값]
```

| Skill | 사용 예 | 입력 (yaml) |
|---|---|---|
| `/gic-research` | `/gic-research 삼성전기 --code=009150` | 부록 C yaml (기업리서치 9페이지) |
| `/gic-excel` | `/gic-excel 삼성전기 --years=5` | Step 6 5개년 모델 마크다운 표 |
| `/gic-weekly` | `/gic-weekly 삼성전기 --week=2026-W19` | 부록 D yaml (위클리 4페이지) |
| `/gic-toppick` | `/gic-toppick 반도체 --pick=2` | 부록 E yaml (TopPick 8슬라이드) |

### 3.2 Skill 단계별 게이트 (원칙 7)

각 Skill은 다음 게이트를 거친다:

1. **Intake**: 부원이 yaml 입력 → Skill이 변수 누락·형식 오류 검증
2. **Map**: yaml → 학회 양식 슬라이드별 변수 매핑 (부원 승인 게이트)
3. **Render**: python-pptx로 PPTX 생성 또는 slides-grab으로 HTML 생성
4. **Export**: PDF/PNG/DOCX 부속 출력
5. **Verify**: design-guide §11.7 점검 표 (Bold 줄바꿈, white-space, line-height) 자동 체크 → ERROR면 부원에게 보고

### 3.3 Skill columns.md 작성 규칙 (원칙 6·8)

- **변수명은 부록 C/D/E yaml과 1:1 동일**
- 글자 수 룰 명시 (예: 메인_타이틀 ≤25자, 문단 설명 ≤200자)
- 자리표시자 형식 명시 (예: `[###,###원]`, `[YYYY.MM.DD]`)
- design-guide_v10 §3 토큰 변수 매핑 (예: --section-header, --orange-primary)

### 3.4 Skill rules.md 작성 규칙

- design-guide_v10 §11 PPTX 호환성 룰 그대로 차용
- white-space:nowrap 강제 셀렉터 명시
- word_wrap=False 후처리 의무
- Pretendard fallback 명시
- 학회 양식.pptx 컬러 hex 절대 임의 변경 금지

---

## 4. 코딩 컨벤션

### 4.1 Python (python-pptx, openpyxl)
- Python 3.12+
- 파일 인코딩 UTF-8
- 들여쓰기 4 spaces (Python 표준)
- 함수명 snake_case, 클래스명 PascalCase
- 주석은 한국어
- 모든 좌표·크기는 cm 단위 우선 (양식 분석 결과와 일치)

### 4.2 Markdown (.md)
- 들여쓰기 2 spaces
- 표는 정렬 명시 안 함 (가독성 우선)
- 4중 백틱 펜스 사용 (v9.0 코드 잘림 0건 룰)
- 한국어 본문, 변수명/함수명만 영어

### 4.3 yaml
- 들여쓰기 2 spaces
- 키 한국어 허용 (양식 변수와 1:1 매핑 위해)
- 자리표시자 `[대괄호]`로 통일

---

## 5. 자동화 도구·MCP 활용

### 5.1 활용 가능한 Skill (이미 설치됨)

| Skill | 본 프로젝트 활용 |
|---|---|
| `slides-grab` | 트랙 3 (위클리·TopPick) HTML→PDF/PNG 안정 출력 |
| `slides-grab-plan` | 슬라이드 outline 작성 (트랙 3) |
| `slides-grab-design` | HTML 슬라이드 생성 (트랙 3) |
| `slides-grab-export` | PDF/PNG 변환 (트랙 3) |
| `anthropic-skills:pptx` | PPTX 안정 출력 (트랙 1·3 보조) |
| `anthropic-skills:xlsx` | Excel 검증·수정 (트랙 2) |
| `anthropic-skills:pdf` | PDF 변환·검증 |
| `anthropic-skills:docx` | DOCX 부속 출력 (낮은 우선순위) |

### 5.2 활용 가능한 MCP

| MCP | 활용 |
|---|---|
| `pykrx-mcp` | 시세·시총·OHLCV·재무 자동 수집 |
| `korea-stock-mcp` | DART 공시·재무제표·기업 정보 |
| `tavily` / `exa` | 산업 리포트·뉴스 검색 |
| `firecrawl` | 사업보고서 PDF 크롤링 |

### 5.3 권장 워크플로

- **Step 0~1 (시총·경쟁사)**: pykrx-mcp + tavily
- **Step 2 (재무)**: korea-stock-mcp (DART)
- **Step 3 (산업)**: tavily/exa + firecrawl (산업 리포트 PDF)
- **Step 4 (기업)**: korea-stock-mcp (사업보고서) + firecrawl
- **Step 5 (포인트·리스크)**: 챗봇 추론 (출처: 누적 데이터)
- **Step 6 (밸류)**: pykrx-mcp + 자체 모델
- **Step 8 (양식)**: `/gic-research` Skill (트랙 1) 또는 `/gic-weekly`/`/gic-toppick` (트랙 3)

---

## 6. 안전 룰

### 6.1 절대 금지
- v9.0 4파일 본체 변형 (헤더·관련 문서 외 본문 수정 금지)
- 학회 양식.pptx 컬러 hex 임의 변경 (`#072A51` `#0D4889` `#E57728` `#E97132`)
- Skill 출력을 검증 없이 학회 드라이브에 자동 푸시
- 위클리 자동 갱신을 발송 채널까지 자동화 (v10.1+에서 인증·운영 검토 후)

### 6.2 변경 시 확인
- 양식 ver3 갱신 시 → §13 양식 갱신 체크리스트 (사용설명서 v10) 따름
- Skill columns.md 갱신 시 → 부록 C/D/E yaml 명세 동시 갱신 (1:1 동등성 유지)
- design-guide_v10 토큰 갱신 시 → templates/ 4종 재빌드

### 6.3 비전공자 부원 보호
- Skill 결과는 항상 .pptx + .pdf 페어 출력 (부원이 PowerPoint 없어도 PDF 확인 가능)
- 모든 .pptx는 PowerPoint 기본 폰트 fallback 명시 (Pretendard → Apple SD Gothic → Malgun)
- Skill 첫 줄에 "이 Skill 없이도 챗봇 복붙으로 동일 결과 가능" 명시

---

## 7. 빌드·테스트

### 7.1 1개 종목 풀 테스트 (Sprint 2 검증 단계)
```bash
# 1. 챗봇에서 yaml 출력 받기 (외부 작업)
# 2. Claude Code에서 Skill 호출
/gic-research 삼성전기

# 3. 결과물 검증
# - PPTX 시각: design/GIC_양식_ver2.pptx와 시각 일치 ≥90%
# - PDF: 모든 폰트 정상, 깨짐 0건
# - 부원 직접 매핑(경로 A) 결과와 비교 → ≥90% 일치
```

### 7.2 design-guide 호환성 자동 체크
```bash
python docs/scripts/verify_pptx_compat.py "[기업명]_GIC리서치_YYYYMMDD.pptx"
# 출력: §11.7 항목별 PASS/FAIL
```
(스크립트는 Sprint 2에서 작성)

---

## 8. 참고 문서

- `prompts/GIC_사용설명서_v10.md` — 부원용 진입 가이드
- `design/GIC_design-guide_v10.md` — 디자인 시스템 (Single Source of Truth)
- `design/양식_분석_결과.md` — 학회 양식 정확 좌표
- `docs/GIC_v10.0_변경사항.md` — v9.0 → v10.0 마이그레이션
- (외부) `AI도구/design-guide.md` — 원본 design system §11 PPTX 호환성 룰의 출처
- (외부) `AI도구/클로드코드업무자동화무료공유회.pdf` — Skill 패러다임 참고
