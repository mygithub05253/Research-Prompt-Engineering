# HTML Rendering and QA Contract

## 1. 목적

v13의 기본 제출 가능 산출물은 `preview.html`이다. HTML은 로컬 브라우저에서 열 수 있어야 하며, 유료 앱이나 구독형 AI 도구가 필요 없어야 한다.

## 2. 렌더링 원칙

- HTML은 static file로 생성한다.
- 외부 CDN 의존을 사용하지 않는다.
- 한글 폰트 fallback을 포함한다.
- 차트는 첫 MVP에서 SVG 또는 CSS/HTML table로 렌더링한다.
- source label은 모든 표/차트 하단에 표시한다.
- QA 실패 시 상단에 `DRAFT - QA NOT APPROVED` 배너를 표시한다.
- HTML 안에 OpenDART API Key를 포함하지 않는다.

## 3. 디자인 원칙

- GIC navy/orange visual identity를 계승한다.
- 공식 GIC 양식은 디자인 기준이며 콘텐츠 고정 템플릿이 아니다.
- `COMPANY_REPORT`와 `INDUSTRY_REPORT`는 portrait ratio preview.
- `INDUSTRY_TOP_PICK`은 landscape 16:9 preview.
- 카드 남발을 피하고 리서치 보고서에 맞는 표·차트·문단 구조를 우선한다.

## 4. HTML 구조

```html
<html>
  <head>
    <title>GIC v13 Report Preview</title>
  </head>
  <body>
    <header data-qa-status="DRAFT"></header>
    <main>
      <section class="page"></section>
    </main>
    <footer></footer>
  </body>
</html>
```

각 page/slide block은 아래 data attributes를 가진다.

- `data-mode`
- `data-orientation`
- `data-page-index`
- `data-claim-ids`
- `data-source-ids`
- `data-qa-overflow-risk`

## 5. QA lint gates

| Gate | 자동 검사 |
|---|---|
| G1 Evidence | 핵심 claim에 fact/source/driver/falsifier link가 있는지 |
| G2 Calculation | OPM, YoY, FCF, net debt 계산 검증 |
| G3 Scenario | actual, company guidance, analyst estimate, assumption 분리 |
| G4 Research Quality | mechanism과 financial impact 필드 존재 |
| G5 Mode & Design | mode와 orientation 일치 |
| G6 Render Integrity | source label, title, unit, period, non-empty chart/table |

## 6. Release rule

v13 MVP에서 `release_approved`는 아래 조건에서만 true다.

- G1-G6 중 FAIL이 없음.
- 핵심 수치의 source가 traceable.
- HTML preview에 DRAFT 배너가 제거되어도 되는 상태.
- 사람이 final review를 수행했다는 `human_reviewed: true`가 기록됨.

PDF/PPTX는 v13 MVP에서 release target이 아니므로, 생성하더라도 `exported draft`로 표시한다.

