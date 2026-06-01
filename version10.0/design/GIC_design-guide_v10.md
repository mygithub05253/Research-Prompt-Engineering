# GIC Design Guide v10.0

> 본 문서는 **Single Source Of Truth**입니다. v10.0의 모든 자동화(트랙 1·2·3) 산출물은 이 가이드의 토큰·시그니처·규칙을 그대로 따릅니다.
> 사용법: 새 슬라이드/리포트 작업 시 → "이 GIC_design-guide_v10.md 참고해서 OO 작성해줘"
>
> **출처**: `design/GIC_양식_ver2.pptx` 분석 결과(`양식_분석_결과.md` / `.json`) + `AI도구/design-guide.md`(원본 design system) §11 PPTX 호환성 룰 흡수

---

## 0. 사용 안내

- **§1~10**: GIC 디자인 시스템 — AI에 이 파일 던져주면 어디서든 학회 톤으로 산출물 생성
- **§11**: HTML→PPTX 변환 호환성 (slides-grab + html2pptx 전제, python-pptx 직접 빌드에도 적용)
- **§12**: GIC 양식 ver2 슬라이드별 좌표·변수 매핑 — 자동화 PDF의 "columns.md" 역할

---

## 1. Visual Thesis

> **단단한 네이비와 따뜻한 오렌지의 대비** — 학회의 신뢰성과 분석의 명확성이 만나는 GIC 정체성.

학회 양식(라이트 베이스)을 기본으로 하되, 위클리·TopPick·결론 임팩트 슬라이드에는 **다크 네이비 베이스**를 허용해 발표 페이스를 만든다.

---

## 2. System Declaration

- **두 톤 교차 사용** — 라이트 베이스가 80% (정식 기업리서치 9페이지 모두 라이트), 다크 베이스는 위클리·TopPick·결론에서 페이스 메이커로 20%
- **포인트 컬러는 오렌지 1색**(`#E57728`). 슬라이드당 3회 이하
- **헤더 패턴은 GIC 양식 공통** — `섹션 헤더 박스(네이비) → 표 → 그림/차트` (산업분석·기업분석·투자포인트·투자리스크·밸류에이션 모두)
- **타이포는 Pretendard 1종**. 코드만 monospace. fallback: Apple SD Gothic Neo → Malgun Gothic
- **표 헤더는 네이비**, 강조 컬럼은 오렌지

---

## 3. Design Tokens (학회 양식.pptx에서 정확 추출)

### 3.1 Background
| Role | Hex | 사용처 |
|---|---|---|
| **Light base** | `#FFFFFF` | 정식 기업리서치 9페이지 전체 |
| Dark base | `#072A51` | 위클리·TopPick 표지·결론 (선택) |

### 3.2 Surface
| Role | Hex | 사용처 |
|---|---|---|
| Light card | `#FFFFFF` | 라이트 슬라이드 카드 |
| Dark card | `#0D4889` | 다크 슬라이드 카드(보조 네이비) |
| Section header bar | `#072A51` | 산업분석·기업분석 등 섹션 헤더 둥근 사각형 |
| Hairline | `#E2E2E2` | 표 행 구분 |

### 3.3 Text
| Role | Hex | 사용처 |
|---|---|---|
| Primary on light | `#1F1F1F` | 본문 |
| Secondary on light | `#5A5A5A` | 보조 설명 |
| Primary on dark | `#FFFFFF` | 다크 위 본문 |
| Heading on light | `#072A51` | 라이트 슬라이드 큰 제목 (BUY, CONTENTS 등) |
| Muted | `#8A8A8A` | 캡션·푸터·자료 출처 |

### 3.4 Accent (1색만 — 슬라이드당 3회 이하)
| Role | Hex | 사용처 |
|---|---|---|
| **Primary Orange** | `#E57728` | ① Check Point 알약 ② 표 강조 컬럼 ③ Point 1·2·3 번호 ④ 짧은 직선 언더라인 |
| Accent Orange | `#E97132` | Check Point 둥근 사각형 (양식 ver2 그대로) |

### 3.5 Border
| Role | Hex |
|---|---|
| Subtle on light | `#E2E2E2` |
| Hairline | `#EAEAEA` |

---

## 4. Typography Roles

| Role | Font | Size | Weight | 사용처 |
|---|---|---|---|---|
| Display | Pretendard Black | 36–44pt | 900 | 표지 빅타이틀 (종목명) |
| Headline | Pretendard ExtraBold | 24–32pt | 800 | 슬라이드 메인 제목 (CONTENTS, BUY) |
| Subhead | Pretendard Bold | 14–16pt | 700 | 부제, Point 1·2·3 라벨 |
| Body | Pretendard | 11–12pt | 400 | 본문(문단 설명 글) |
| Body Strong | Pretendard Bold | 11–12pt | 700 | 본문 강조 |
| Caption | Pretendard | 9–10pt | 500 | 자료 출처, 푸터 |
| Code | JetBrains Mono / Courier | 10–12pt | 500 | 명령어, ASCII tree |

**금기**: 9pt 미만 텍스트 절대 금지. 표지 종목명은 36pt 이상.

### 4.1 PPTX 호환성 폰트 fallback (필수)
```css
.title {
  font-family: 'Pretendard Black', 'Pretendard ExtraBold', 'Pretendard',
               'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
  font-weight: 900;
}
```
이유: 부원 PC에 Pretendard 없으면 Apple SD Gothic Neo (Mac) → Malgun Gothic (Windows 기본).

---

## 5. Layout Patterns (재사용 시스템)

### 5.1 학회 양식 공통 헤더 (산업분석·기업분석·투자포인트·투자리스크·밸류에이션 5섹션)
```
[섹션 헤더 둥근 사각형 #072A51 흰 글자] L1.27cm T2.13cm W16.32cm H0.81cm
```
- 둥근 모서리 4pt
- 폰트: Pretendard Bold 14pt, 흰색
- 텍스트: "산업분석" / "기업분석" / "투자포인트" / "투자리스크" / "밸류에이션"

### 5.2 우상단 기업명 라벨
- TextBox L13.84cm T1.01cm W3.75cm H0.60cm
- 텍스트: `[기업명](종목코드)` (예: 삼성전기(009150))
- 폰트: Pretendard 9pt, secondary

### 5.3 Check Point 알약 (표지)
- 둥근 사각형: 배경 `#E97132`, 텍스트 `#FFFFFF`, "Check Point"
- L7.26cm T5.27cm W3.40cm H0.68cm
- 우측에 직선(오렌지) 언더라인 W7.45cm

### 5.4 BUY 박스 (표지 좌상단)
- TextBox " BUY(매수)" L0.07cm T5.00cm W6.56cm H1.97cm
- 폰트: Pretendard Black 36pt, `#072A51`

### 5.5 Point 1·2·3 (표지 우측)
- TextBox L7.15cm T6.37 / 10.86 / 15.36cm W11.02cm H0.77cm
- 폰트: Subhead Bold 14pt, `#072A51`
- 형식: `Point 1.` `Point 2.` `Point 3.`

### 5.6 표 시스템 (Revision·주요주주·재무지표)
- 헤더 행: 배경 `#072A51`, 글자 `#FFFFFF`, Pretendard Bold 10pt
- 강조 컬럼 헤더: 글자 `#E57728`
- 행 구분: hairline `#EAEAEA`
- 셀 패딩: 6pt × 10pt

### 5.7 자료 출처 (모든 차트·이미지 하단)
- TextBox: `자료: [출처명]`, Pretendard 8pt, `#8A8A8A`
- 양식 ver2 모든 차트·이미지에 의무

---

## 6. Signature Elements (GIC 톤의 시그니처 4가지)

1. **네이비 섹션 헤더 둥근 사각형** (W16.32cm × H0.81cm) — 모든 본문 슬라이드 공통
2. **오렌지 짧은 직선 언더라인** (W7.45cm × 1pt) — 표지 Check Point, 헤더 강조
3. **오렌지 Check Point 알약** (W3.40cm × H0.68cm) — 표지 한정
4. **표 헤더 네이비 + 오렌지 강조 컬럼** — 모든 표 공통

→ 한 슬라이드에 시그니처 4개 모두 출현 금지. 1~2개로 한정.

---

## 7. Avoid (절대 금지 — AI slop 회피 + PPTX 변환 호환성)

- ❌ 오렌지 외 포인트 컬러 (블루/레드/그린/머스타드) — Avoid
- ❌ 그라데이션 배경 (단색만)
- ❌ 라이트 슬라이드에 다크 카드, 다크 슬라이드에 흰색 카드 (톤 충돌)
- ❌ 이모지 아이콘 — 문자 화살표 `→ ↓ ●` 만 OK
- ❌ Inter / Roboto / Arial / 시스템 영문 폰트 (Pretendard 고정)
- ❌ **둥근 카드(border-radius ≥ 8pt) 위의 좌측 오렌지 띠** — PPTX 변환 시 침범
- ❌ **제목에 font-family 없이 font-weight: 900 만 적용** — PPTX 출력에서 얇게 나옴
- ❌ **빈 `<span>` 도형으로 점/아이콘 표현** — html2pptx 누락
- ❌ **`<code>` 안에 텍스트만 두기** (감싸는 `<p>` 없이) — PPTX 텍스트 컨테이너로 인식 안 됨
- ❌ **inline 요소(`<span>`, `<b>`, `<strong>`)에 margin** — PPTX 호환 X
- ❌ 9pt 미만 본문, 8pt 미만 캡션
- ❌ 드롭 섀도우 / 카드 그라데이션 / 3D 효과
- ❌ 한 슬라이드에 시그니처 4종 모두 출현
- ❌ 학회 양식.pptx의 컬러 값 임의 변경 — `#072A51` `#0D4889` `#E57728` `#E97132` 그대로

---

## 8. Slide Type Library (콘텐츠별 패턴 매칭)

| 콘텐츠 성격 | 톤 | 패턴 | 시그니처 |
|---|---|---|---|
| 정식 기업리서치 표지 | Light | BUY 박스 + Revision 표 + 주가차트 + Check Point 3개 | 알약 + 짧은 언더라인 |
| CONTENTS 목차 | Light | 5섹션 목차 표 | 양식 그대로 |
| 산업·기업·포인트·리스크 본문 | Light | 네이비 섹션 헤더 + 표 2개(상·하) + 차트/이미지 | 섹션 헤더 |
| 밸류에이션 | Light | 재무지표 표 + 차트 4개 | 표 헤더 네이비 |
| 위클리 표지 | Dark | Display + 핵심 메시지 + 투자의견 변동 | 표지 |
| 위클리 본문 | Light | 직전 → 이번 주 비교 표 | 표 헤더 |
| TopPick 산업 진단 | Dark | 산업 사이클 비유 + 시장 규모 | 다크 베이스 |
| TopPick 스크리닝 | Light | 5~10개 후보 표 | 표 |
| TopPick 정식 압축 | Light | 6-Lens 점수 + Risk-Reward | 표 |
| Compliance Notice | Light | 표 + 작은 글씨 | - |

---

## 9. 자동화 트랙별 디자인 적용 (v10 신규)

### 트랙 1: 정식 기업리서치 PPT (`/gic-research`)
- 학회 양식.pptx 슬라이드 마스터 그대로 사용 — python-pptx로 텍스트 박스만 채움
- §3 토큰 자동 적용 (마스터에 박제됨)
- 9페이지 변수 매핑은 **§12 + columns.md** 참조

### 트랙 2: Excel 5개년 모델 (`/gic-excel`)
- 컬러 코딩: 입력 셀 배경 `#FFE9D6` (오렌지 10%), 수식 셀 배경 `#FFFFFF`, 참조 셀 배경 `#E8EFFF` (네이비 10%)
- 헤더 배경 `#072A51` 흰 글자
- Balance Check OK = 녹색 / ERROR = 빨강 (조건부 서식)

### 트랙 3: 위클리·TopPick HTML→PPTX (`/gic-weekly`, `/gic-toppick`)
- 본 가이드 §3·§5·§7 전체 적용
- slides-grab의 design-guide.md로 본 파일 사용
- §11 PPTX 호환성 룰 의무 (line-height 1.2~1.3, white-space:nowrap, word_wrap=False 후처리)

---

## 10. 새 작업 시작 명령 (만능 프롬프트)

```
이 GIC_design-guide_v10.md 참고해서 [기업/산업/주제]에 대해 [기업리서치/위클리/TopPick] 만들어줘.
청중은 GIC 학회원, 분량 [N]페이지, 톤은 가이드대로.
양식.pptx 토큰을 그대로 적용. 시그니처 1~2개만.
```

---

## 11. PPTX 편집 가능 변환 호환성 체크리스트

(원본 `AI도구/design-guide.md` §11 그대로 흡수 — slides-grab + html2pptx 또는 python-pptx 직접 빌드 모두 적용)

### 11.1 HTML 구조 규칙
1. 모든 텍스트는 `<p>` / `<h1>~<h6>` / `<ul>` / `<ol>` 안에 — `<div>` 직접 자식으로 텍스트 두지 않기
2. `<p>` / `<h*>` / `<ul>` / `<ol>` 에는 **background · border · box-shadow 금지** — 박스 디자인은 부모 `<div>` 에
3. `<span>` / `<b>` / `<strong>` / `<i>` / `<em>` / `<u>` 에 **margin 금지** — 인라인 간격은 부모의 `flex gap` 으로
4. `<code>` 만으로 텍스트 감싸지 말 것 — `<p><span class="code">…</span></p>` 형태로

### 11.2 시각 요소 규칙
1. **점·도형 표현은 텍스트 캐릭터로** — `●●●●●`(켜짐) `○`(꺼짐). 빈 `<span>` 도형 금지
2. **CSS 그라데이션 금지** — 단색만
3. **둥근 카드(radius ≥ 8pt)에 좌측 오렌지 띠 금지** — 직사각형 코드/CTA 박스에서만
4. **본문 padding-bottom ≥ 36pt** — 텍스트 박스가 슬라이드 하단 0.5인치 이내로 가지 않아야 함

### 11.3 폰트 규칙
1. **제목은 font-family 에 굵은 패밀리 명시** — `font-family: 'Pretendard Black', 'Pretendard ExtraBold', 'Pretendard', 'Malgun Gothic'` 식
2. **font-weight 는 보조** — 패밀리 이름이 우선
3. **letter-spacing 은 -0.025em ~ +0.12em 범위**

### 11.4 줄간격 (line-height)
| 텍스트 종류 | 권장 line-height |
|---|---|
| Display / Headline | **1.2~1.3** |
| Subhead | 1.25~1.35 |
| Body | 1.5~1.6 |
| 표/카드 안 짧은 라벨 | 1.2~1.3 |

### 11.5 짧은 라벨 `white-space: nowrap` 강제
한 단어 라벨(`BUY`, `Check Point`, `산업분석` 같은)에 의무.
```css
.section-header, .check-point, .point-label, .col-name {
  white-space: nowrap;
}
```

### 11.6 표(table)의 head row와 body row 분리
```css
.row:not(.head) .col p { color: #1F1F1F; font-size: 11pt; }
.row.head .col p { color: #FFFFFF; font-size: 11pt; font-weight: 700; background: #072A51; }
```
`.table` 에 `flex: 1` 금지.

### 11.7 Bold 줄바꿈 점검 (변환 후 필수)
PPTX 변환 후 반드시 한 번 열어서 확인. Bold 텍스트 폭 초과로 의도치 않은 줄바꿈 발생 가능.

| 현상 | 처방 |
|---|---|
| 카드 안 본문이 한 줄 더 늘어남 | 본문 짧게 / 카드 padding 줄이기 / 폰트 0.5pt 줄이기 |
| 표 셀 안 텍스트 줄바꿈 | flex 비율 조정 또는 셀 글자수 줄이기 |
| 제목 두 줄로 깨짐 | 명시적 `<br>` + `white-space: nowrap` |
| 한 단어 글자 단위 끊김 | `white-space: nowrap` (§11.5) |
| 제목·부제 겹침 | line-height 1.2~1.3 통일 (§11.4) |

### 11.8 변환 파이프라인 3단계 + 검증
```
HTML 작성 (line-height 1.2~1.3 + 한 단어 라벨 nowrap)
   ↓
preprocess.py        ← 구조 호환 보정
   ↓
html2pptx            ← 텍스트박스/도형/이미지 생성
   ↓
postprocess.py       ← word_wrap 정책 (짧은 라벨 → False)
   ↓
PPTX 열기 → §11.7 점검
```

### 11.9 word_wrap 후처리 (필수)
HTML `white-space: nowrap`은 html2pptx에서 무시됨. python-pptx로 강제.
```python
from pptx import Presentation
prs = Presentation('deck.pptx')
for slide in prs.slides:
    for shape in slide.shapes:
        if not shape.has_text_frame: continue
        tf = shape.text_frame
        if len(tf.text.strip()) <= 30 and len(tf.paragraphs) == 1:
            tf.word_wrap = False
prs.save('deck.pptx')
```
임계값: 30자, 1 paragraph.

---

## 12. GIC 양식 ver2 슬라이드별 좌표 매핑 (자동화 columns.md 베이스)

> 본 섹션은 `analyze_template.py`로 추출한 정확한 좌표를 박제. python-pptx 또는 html2pptx 빌드 시 그대로 사용.

**슬라이드 크기**: 19.05cm × 27.52cm (7.5″ × 10.83″, 세로 보고서형)

### 12.1 슬라이드 1 — 표지
| 변수 | 위치(cm) | 크기(cm) | 비고 |
|---|---|---|---|
| 종목명 | L4.59 T0.85 | W9.88 H1.45 | Display 36pt+ `[기업명] ([종목코드])` |
| 부제 | L4.59 T2.35 | W9.88 H0.94 | "GIC여 긱스럽게 도전하라" 고정 |
| 작성일 | L0.19 T3.51 | W5.63 H0.68 | `[YYYY.MM.DD]` |
| 학회기수 | L13.06 T3.42 | W5.63 H0.68 | `GIC [N]기 [작성자]` |
| BUY 박스 | L0.07 T5.00 | W6.56 H1.97 | `BUY/HOLD/SELL` Display 네이비 |
| Revision 표 | L1.35 T7.07 | W3.91 H1.78 | 목표주가/상승여력/현재가 3행 |
| 시총·외국인 표 | L0.52 T9.30 | W5.57 H4.53 | 시총·발행주식·유동주식·52주 고저·일평균거래액·외국인지분율 6행 |
| 주요주주 표 | L0.52 T14.07 | W5.57 H1.82 | 주요주주(%) 헤더 |
| 주요주주 표(상세) | L0.52 T16.50 | W5.57 H4.56 | 주주별 % 데이터 |
| 주가 차트 | L0.52 T17.30 | W5.60 H3.82 | 차트 이미지 |
| Check Point 알약 | L7.26 T5.27 | W3.40 H0.68 | "Check Point" 오렌지 |
| Check Point 부제 | L10.65 T5.22 | W7.62 H0.68 | `[≤30자 슬로건]` |
| 오렌지 직선 | L10.57 T5.93 | W7.45 H0 | 언더라인 |
| Point 1 | L7.15 T6.37 | W11.02 H0.77 | `Point 1. [내용 ≤200자]` |
| Point 2 | L7.15 T10.86 | W11.02 H0.77 | `Point 2. [내용 ≤200자]` |
| Point 3 | L7.15 T15.36 | W11.02 H0.77 | `Point 3. [내용 ≤200자]` |
| 재무지표 표 | L0.83 T21.64 | W17.38 H4.90 | 12월결산·매출액·영업이익·지배순이익·PER·ROE·PBR·EV/EBITDA·DY |

### 12.2 슬라이드 2 — CONTENTS
| 변수 | 위치(cm) | 크기(cm) | 비고 |
|---|---|---|---|
| 우상단 기업명 | L13.84 T1.01 | W3.75 H0.60 | `[기업명]([종목코드])` |
| CONTENTS 제목 | L8.82 T3.92 | W7.51 H1.62 | 고정 |
| 5섹션 목차 표 | L1.98 T6.10 | W14.30 H13.41 | 산업분석·기업분석·투자포인트·투자리스크·밸류에이션 |

### 12.3 슬라이드 3 — 산업분석
| 변수 | 위치(cm) | 크기(cm) | 비고 |
|---|---|---|---|
| 우상단 기업명 | L13.84 T1.01 | W3.75 H0.60 | 동일 |
| 섹션 헤더 | L1.27 T2.13 | W16.32 H0.81 | "산업분석" 네이비 박스 |
| 첫 문단 표 | L1.27 T3.48 | W16.32 H5.81 | 제목 문장(≤25자) + 문단 설명 글(≤200자) |
| 둘째 문단 표 | L1.27 T9.81 | W16.32 H5.81 | 제목 문장 + 문단 설명 글 |
| 그림(우) | L9.96 T19.29 | W6.90 H4.60 | 산업 이미지 |
| 차트(좌) | L1.61 T19.29 | W7.64 H4.60 | 산업 차트 |
| 자료 출처 | 차트 하단 | - | "자료: [출처]" |

### 12.4 슬라이드 4 — 기업분석
| 변수 | 위치(cm) | 크기(cm) | 비고 |
|---|---|---|---|
| 섹션 헤더 | L1.27 T2.13 | W16.32 H0.81 | "기업분석" |
| 첫 문단 표 | L1.27 T3.48 | W16.32 H5.81 | 제목 + 문단 |
| 둘째 문단 표 | L1.27 T9.81 | W16.32 H5.81 | 제목 + 문단 |
| 다이어그램(좌) | L1.26 T16.66 | W7.98 H5.81 | 사업구조/지배구조 |
| 다이어그램(우상) | L10.31 T15.01 | W6.41 H4.47 | BM 다이어그램 |
| 그림(우하) | L10.31 T19.77 | W6.41 H4.28 | 제품 이미지 |

### 12.5 슬라이드 5·6 — 투자포인트
| 변수 | 위치(cm) | 크기(cm) | 비고 |
|---|---|---|---|
| 섹션 헤더 | L1.27 T2.13 | W16.32 H0.81 | "투자포인트" |
| Point 1 표 | L1.27 T3.48 | W16.32 H5.81 | `Point 1. [제목]` + 문단 |
| Point 2 표 | L1.27 T9.81 | W16.32 H5.81 | `Point 2. [제목]` + 문단 |
| Point 3 표 | L1.27 T16.15 | W16.32 H5.81 | `Point 3. [제목]` + 문단 |

→ 슬라이드 5·6은 동일 레이아웃. Point 1·2·3 분량에 따라 1페이지 또는 2페이지 사용.

### 12.6 슬라이드 7 — 투자리스크
| 변수 | 위치(cm) | 크기(cm) | 비고 |
|---|---|---|---|
| 섹션 헤더 | L1.27 T2.13 | W16.32 H0.81 | "투자리스크" |
| Risk 1 표 | L1.27 T3.48 | W16.32 H5.81 | `Risk 1. [제목]` + 문단 |
| Risk 1 이미지 영역 | L1.27 T8.57 | W15.98 H6.51 | 차트/표 |
| Risk 2 표 | L1.27 T16.16 | W16.32 H5.81 | `Risk 2. [제목]` + 문단 |

### 12.7 슬라이드 8 — 밸류에이션 (1)
| 변수 | 위치(cm) | 크기(cm) | 비고 |
|---|---|---|---|
| 섹션 헤더 | L1.27 T2.13 | W16.32 H0.81 | "밸류에이션" |
| 재무지표 표 | L1.32 T5.02 | W15.93 H5.65 | 5개년 IS+ratio 표 |
| 차트 1 (좌상) | L1.27 T14.17 | W7.87 H4.29 | 매출/영업이익 추이 |
| 차트 2 (우상) | L10.20 T14.17 | W7.87 H4.29 | ROE/ROIC 추이 |
| 차트 3 (좌하) | L1.32 T20.40 | W8.26 H4.61 | 멀티플 비교 |
| 차트 4 (우하) | L9.82 T20.55 | W8.26 H4.84 | 시나리오 또는 매출 구성 |

### 12.8 슬라이드 9 — 밸류에이션 (2) + Compliance
| 변수 | 위치(cm) | 크기(cm) | 비고 |
|---|---|---|---|
| 섹션 헤더 | L1.27 T2.13 | W16.32 H0.81 | "밸류에이션" |
| 재무지표 표 (요약) | L1.32 T5.02 | W15.93 H5.65 | 결론 표 |
| Compliance Notice 표 | L1.32 T22.49 | W16.28 H3.58 | 고정 텍스트(학회 표준) |

---

## 부록 A: CSS 토큰 빠른 복사용

```css
:root {
  /* GIC v10.0 Brand Tokens */
  --bg-light: #FFFFFF;
  --bg-dark: #072A51;
  --card-light: #FFFFFF;
  --card-dark: #0D4889;

  --section-header: #072A51;
  --hairline: #E2E2E2;

  --text-primary-light: #1F1F1F;
  --text-secondary-light: #5A5A5A;
  --text-primary-dark: #FFFFFF;
  --text-heading-light: #072A51;
  --text-muted: #8A8A8A;

  --orange-primary: #E57728;
  --orange-accent: #E97132;

  --border-light: #E2E2E2;
}
```

## 부록 B: 가이드 사용 원칙

- **유연 = 토큰은 고정, 레이아웃은 콘텐츠에 맞춰 변형**. §8 매핑은 권장 — 콘텐츠가 더 잘 맞는 다른 패턴이 있으면 그걸 쓴다.
- **avoid가 가장 강력**. AI는 "쓸 색"보다 "안 쓸 색"으로 더 잘 통제됨.
- **시그니처는 한 슬라이드 안에서 1~2개만**. 모든 시그니처를 다 쓰면 시각적 노이즈.
- **§12 좌표는 정식 기업리서치 9페이지 한정**. 위클리·TopPick은 §3·§5 토큰만 따르고 레이아웃은 자유 설계.
- **컬러 hex 임의 변경 금지** — 학회 양식.pptx에서 정확 추출한 값. 양식 ver3 갱신 시 재추출.
