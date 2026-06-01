# GIC 리서치 프롬프트 시스템 — v9.0 → v10.0 변경사항

> **버전**: v10.0 / 2026-05-09
> **CLAUDE.md §7.1 규정**: 한 마일스톤 단위로 누적된 변경사항을 한 번에 정리
> **본 문서는 부원·학회 외부 참고자에게 v9.0 → v10.0 마이그레이션 가이드**

---

## 1. 한 줄 요약

> **v9.0의 단단한 챗봇 복붙 베이스(외부 의존 0)를 100% 보존하면서, 학회 양식 PPT/Excel 자동화를 그 위에 옵션으로 얹은 마일스톤.**

---

## 2. 핵심 변화 (Major)

### 2.1 폴더 구조 — `version9.0/` 보존, `version10.0/` 신규
- `version9.0/` 4파일 그대로 (수정 0)
- `version10.0/`에 자동화 자산 + 갱신된 prompts 추가

### 2.2 자동화 트랙 4종 + 자동위클리 설계
| 트랙 | Skill | 입력 | 출력 |
|---|---|---|---|
| 1 | `/gic-research` | 부록 C yaml | 학회 양식.pptx 9페이지 |
| 2 | `/gic-excel` | Step 6 5개년 표 | 8 sheets Excel (Balance Check) |
| 3 | `/gic-weekly`, `/gic-toppick` | 부록 D·E yaml | slides-grab HTML→PDF/PNG + PPTX |
| 4 | (가이드만) | 데이터 자동 수집 MCP | pykrx-mcp / korea-stock-mcp |
| 5 | (설계만) | 자동 위클리 갱신 (cron) | v10.1+ 구현 |

### 2.3 챗봇 복붙 ≡ Skill 자동화 동등성 (원칙 8, v10 신규)
- prompts/ 4파일에 **부록 C·D·E** (양식 슬라이드 명세) 추가
- Skill `columns.md` ≡ 부록 yaml 명세 1:1 동일
- Gemini·ChatGPT 부원도 챗봇 복붙으로 자동화에 근접한 결과 (시각 일치 ≥90%)

### 2.4 학회 양식 디자인 토큰 박제
- 양식 ver2 .pptx 분석 (`design/양식_분석_결과.md`):
  - Primary Navy `#072A51` / Secondary Navy `#0D4889`
  - Accent Orange `#E57728` / Check Point Orange `#E97132`
  - 슬라이드 크기 19.05cm × 27.52cm (세로 보고서형)
- `design/GIC_design-guide_v10.md`:
  - 학회 톤 + design-guide.md §11 PPTX 호환성 룰 흡수
  - §12 슬라이드별 정확 좌표 박제

### 2.5 slides-grab + anthropic-skills:pptx 통합
- slides-grab (오픈소스): HTML → PDF/PNG 안정 출력 (트랙 3)
- anthropic-skills:pptx: PPTX 안정 출력 (트랙 1·3 보조)
- 트랙 1 (학회 양식 9페이지)는 python-pptx 직접 빌드 (양식 보존 우선)

---

## 3. 새 파일 (v10.0 신규 생성)

### 3.1 prompts/ — v9.0 본문 100% 복사 + 부록 추가
- `GIC_기업리서치_v10.md` — 부록 C (9페이지 슬라이드 명세) 추가
- `GIC_위클리투자리포트_v10.md` — 부록 D (4페이지 명세) 추가
- `GIC_산업TopPick_v10.md` — 부록 E (8슬라이드 명세) 추가
- `GIC_사용설명서_v10.md` — §10 자동화 티어 3·4·5 + §11 챗봇별 동등 워크플로 + §12 v10 차이 추가

### 3.2 design/
- `GIC_design-guide_v10.md` — 디자인 시스템 (학회 톤 + PPTX 호환성)
- `GIC_양식_ver2.pptx` — 학회 표준 양식 원본 (Downloads에서 이동)
- `GIC_양식_ver2.pdf` — PDF 참고용
- `양식_분석_결과.md` / `.json` — python-pptx 분석 결과

### 3.3 templates/
- `기업리서치_9p.pptx` — 학회 양식 슬라이드 마스터 (트랙 1)
- `Excel_5개년모델_v10.xlsx` — 학회 표준 (8 sheets, Balance Check)
- `위클리_4p.html` — 위클리 베이스 HTML (트랙 3)
- `산업TopPick_8p.html` — TopPick 베이스 HTML (트랙 3)

### 3.4 .claude/skills/ — Skill 4종
- `gic-research/` — SKILL.md + columns.md + rules.md + stages/ 4파일 + scripts/render_research.py
- `gic-excel/` — SKILL.md + columns.md + rules.md + scripts/build_excel_template.py
- `gic-weekly/` — SKILL.md + columns.md + rules.md
- `gic-toppick/` — SKILL.md + columns.md + rules.md

### 3.5 .claude/CLAUDE.md
- v10.0 프로젝트 컨벤션
- 8가지 원칙 (v9.0 §9.1 4 + v10 신규 4)
- Skill 호출 컨벤션, 코딩 컨벤션, 안전 룰

### 3.6 docs/
- `analyze_template.py` — 양식 분석 스크립트 (일회성)
- `자동위클리_설계.md` — 트랙 5 (구현은 v10.1+)
- `GIC_v10.0_변경사항.md` — 본 문서
- `GIC_v10.0_요약본.md` — 1페이지 마스터 인덱스

### 3.7 data/
- `samples/삼성전기.yaml` — 부록 C yaml 샘플 (Skill 풀 테스트용)
- `output/삼성전기_GIC리서치_20260509/` — 1차 빌드 검증 결과

---

## 4. 수정된 파일 (v10.0)

**v9.0 → v10.0 마이그레이션 시 헤더만 갱신, 본문 변경 0**
- `version10.0/prompts/GIC_기업리서치_v10.md` — 헤더 + 부록 C 추가
- `version10.0/prompts/GIC_위클리투자리포트_v10.md` — 헤더 + 부록 D 추가
- `version10.0/prompts/GIC_산업TopPick_v10.md` — 헤더 + 부록 E 추가
- `version10.0/prompts/GIC_사용설명서_v10.md` — 헤더 + §10·11·12 부록 추가

**원칙 5 검증**: `version9.0/` 디렉토리 변경 0건. `diff version9.0/ version10.0/prompts/` = 헤더 + 부록 부분만 차이.

---

## 5. 신규 원칙 (v10.0)

### 5.1 원칙 5 — 자동화는 항상 챗봇 복붙(티어 1)의 부속 옵션
v9.0 본문 한 줄도 축소하지 않음. v9.0 4파일은 v10.0/prompts/에 100% 복사.

### 5.2 원칙 6 — Skill의 columns.md / rules.md = 학회 도메인 지식의 외화
자동화 PDF "기술보다 업무를 잘 설명하는 게 훨씬 더 중요" 흡수.

### 5.3 원칙 7 — 단계별 게이트 의무
자동화 PDF TIP 2 "Plan 모드부터" 적용. 각 Skill 단계 사이 부원 승인 게이트.

### 5.4 원칙 8 — 챗봇 복붙 ≡ Skill 자동화 동등성 [핵심]
부록 C/D/E yaml 명세와 Skill `columns.md`는 1:1 동일. 환경 격차(Gemini > ChatGPT > Claude 구독)를 흡수.

---

## 6. v10.0 검증 결과 (Sprint 2·3 빌드 테스트)

### 트랙 1 — 기업리서치 PPT 자동 생성
- 입력: `data/samples/삼성전기.yaml`
- 명령: `/gic-research` (`render_research.py` 호출)
- 결과: `data/output/삼성전기_GIC리서치_20260509.pptx` 생성 OK
- 검증:
  - 슬라이드 1 (표지): 종목명·종목코드·작성일·학회기수·투자의견·Check Point 슬로건·Point 1·2·3 모두 자동 매핑 ✅
  - 슬라이드 2~9: 우상단 기업명 라벨 자동 ✅
  - word_wrap=False 후처리: 24건 적용 ✅
  - 학회 양식 디자인 (네이비 헤더, 오렌지 Check Point, 폰트, 표 구조): 100% 보존 ✅

### 트랙 2 — Excel 양식 빌드
- 명령: `python build_excel_template.py`
- 결과: `templates/Excel_5개년모델_v10.xlsx` (8 sheets) 생성 OK
- 시트: Assumptions / IS / BS / CF / Valuation / Scenario / Sensitivity / Summary
- Balance Check 조건부 서식 (OK 초록 / ERROR 빨강) 적용 ✅

### 트랙 3 — 위클리·TopPick HTML 템플릿
- `templates/위클리_4p.html`: 다크 표지 1p + 라이트 본문 3p
- `templates/산업TopPick_8p.html`: 다크/라이트 교차 8슬라이드
- design-guide_v10 §3 토큰 적용 ✅
- §11 PPTX 호환성 룰 (line-height, white-space:nowrap) 적용 ✅

---

## 7. 알려진 한계 (v10.0)

1. **트랙 1 v0.1**: 텍스트 박스만 자동 매핑. 표(Revision/시총/주요주주/재무지표) 자동 채움은 v10.1+ 예정. 현재는 부원이 PowerPoint에서 직접 채움.
2. **트랙 1 PDF 변환**: LibreOffice 미설치 환경에서는 PDF 변환 SKIP. 부원이 PowerPoint에서 직접 PDF 저장 필요.
3. **트랙 2 yaml 자동 입력**: v10.0은 빈 양식만 빌드. yaml/마크다운 표 → Excel 자동 채움은 v10.1+.
4. **트랙 5 자동 위클리**: 설계만, 구현은 v10.1+.
5. **slides-grab PPTX**: experimental/unstable로 명시됨. PDF/PNG는 안정. PPTX는 anthropic-skills:pptx로 부속 출력.

---

## 8. v10.1 로드맵 (예정)

1. **트랙 1 v0.2**: 표 행 자동 채움 (Revision/시총·외국인/주요주주/재무지표 표) + 이미지 영역 PNG 삽입
2. **트랙 2 v0.2**: yaml/마크다운 → Excel 자동 입력 (`fill_excel_from_yaml.py`)
3. **트랙 4 통합**: pykrx-mcp / korea-stock-mcp Skill 통합
4. **트랙 5 구현**: 자동 위클리 cron + Slack/이메일 발송
5. **부원 검증**: 1분기 시범 운영 후 사용률·만족도 피드백 수집

---

## 9. 마이그레이션 가이드 (v9.0 → v10.0)

### 9.1 챗봇 복붙 부원 (모든 부원)
1. `version9.0/`에서 `version10.0/prompts/`로 이동
2. v10.0 4파일은 v9.0과 본문 동일 — 부록 C/D/E만 추가됨
3. 평소대로 9단계 챗봇 복붙 사용 가능
4. 발표 양식이 필요하면 마지막에 "부록 C 형식 yaml로 출력" 추가 요청 → PowerPoint 양식.pptx에 매핑

### 9.2 익숙한 부원 (Excel 사용)
1. `templates/Excel_5개년모델_v10.xlsx` 다운로드
2. Sheet 1 Assumptions (Bear/Base/Bull) 입력
3. Sheet 2~4 IS/BS/CF에 5개년 데이터 입력
4. Sheet 5 Valuation 자동 계산 확인
5. Sheet 8 Summary로 1페이지 결론 확인

### 9.3 운영진 (Claude Code Skill)
1. slides-grab 플러그인 설치 (Sprint 0)
2. 1개 종목 풀 테스트 (`/gic-research [기업명]`)
3. 결과물(.pptx/.xlsx) 학회 드라이브 배포
4. 부원에게 다운로드 안내

---

## 10. Compliance Notice

본 시스템은 GIC 학회 내부 학습 목적이며, 투자 권유가 아닙니다.
v9.0의 핵심 철학 *"AI 모델·웹앱·MCP가 사라져도 잘 쓴 .md 프롬프트는 영원하다"*는 v10.0에서도 그대로 유지됩니다.

---

문의·개선 제안은 GIC 4기 운영팀에.
