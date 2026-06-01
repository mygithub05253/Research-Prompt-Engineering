# GIC 리서치 프롬프트 시스템 v10.0

> **버전**: v10.0 / 2026-05-09
> **One-liner**: 챗봇 복붙 100% 베이스 + 학회 양식 PPT/Excel 자동화 4트랙

---

## 빠른 시작

### 부원 (모든 챗봇)
1. **신규**: `prompts/GIC_사용설명서_v10.md` 정독 (8~15분)
2. **분석**: `prompts/GIC_기업리서치_v10.md` Step 0~8 챗봇 복붙 통과 (1시간)
3. **양식**: 챗봇에 "부록 C 형식 yaml 출력" 추가 요청
4. **PowerPoint**: 학회 드라이브에서 양식.pptx 다운 → yaml 변수를 텍스트로 매핑 (30~45분)
5. **발표** ✨

### 운영진 (Claude Code)
1. **Sprint 0**: slides-grab 플러그인 설치 + 세션 재시작
2. **Sprint 1**: 학회 드라이브에 v10.0 폴더 동기화
3. **Skill 호출**: `/gic-research 삼성전기` → 5분 만에 PPTX 자동 생성
4. **검증**: design-guide_v10 §11.7 호환성 점검 (자동)
5. **배포**: 결과물 학회 드라이브 업로드 → 부원 다운로드 → PowerPoint에서 자유 수정

---

## 폴더 구조

```
version10.0/
├── prompts/                             # 티어 1·2 (챗봇 복붙)
│   ├── GIC_기업리서치_v10.md             # 정식 9단계 + 부록 C
│   ├── GIC_위클리투자리포트_v10.md       # 위클리 + 부록 D
│   ├── GIC_산업TopPick_v10.md           # TopPick + 부록 E
│   └── GIC_사용설명서_v10.md             # 진입 가이드
│
├── design/
│   ├── GIC_design-guide_v10.md          # 디자인 시스템 (학회 톤 + PPTX 호환성)
│   ├── GIC_양식_ver2.pptx               # 학회 양식 원본
│   ├── GIC_양식_ver2.pdf
│   └── 양식_분석_결과.md / .json
│
├── templates/
│   ├── 기업리서치_9p.pptx                # 트랙 1
│   ├── Excel_5개년모델_v10.xlsx         # 트랙 2 (8 sheets)
│   ├── 위클리_4p.html                   # 트랙 3
│   └── 산업TopPick_8p.html
│
├── .claude/                             # Claude Code 운영진용
│   ├── CLAUDE.md
│   └── skills/
│       ├── gic-research/                # /gic-research [기업명]
│       ├── gic-excel/                   # /gic-excel
│       ├── gic-weekly/                  # /gic-weekly [기업명]
│       └── gic-toppick/                 # /gic-toppick [산업명]
│
├── data/
│   ├── samples/                         # yaml 샘플
│   └── output/                          # Skill 출력
│
└── docs/
    ├── GIC_v10.0_변경사항.md
    ├── GIC_v10.0_요약본.md (1페이지 마스터 인덱스)
    ├── 자동위클리_설계.md (v10.1+ 구현 예정)
    └── analyze_template.py
```

---

## 자동화 트랙

| # | Skill | 입력 | 출력 | 시간 (Skill / 수기) |
|---|---|---|---|---|
| 1 | `/gic-research` | 부록 C yaml | 학회 양식.pptx 9페이지 | 5분 / 30~45분 |
| 2 | `/gic-excel` | Step 6 5개년 표 | 8 sheets Excel | 3분 / 25~30분 |
| 3 | `/gic-weekly` | 부록 D yaml | 위클리 4p (PDF+PPTX) | 5분 / 30~45분 |
| 3 | `/gic-toppick` | 부록 E yaml | TopPick 8p (PDF+PPTX) | 5분 / 45~60분 |
| 4 | (가이드) | pykrx/korea-stock MCP | 데이터 자동 | 챗봇 직접 |
| 5 | (설계만) | 자동 위클리 cron | v10.1+ 구현 | - |

---

## 핵심 원칙

1. **마크다운 .md 파일만, 외부 의존 0** (v9.0)
2. **정식 9단계 + 블록 라이브러리 본질** (v9.0)
3. **외부 벤치마크 흡수, 본질 훼손 금지** (v9.0)
4. **한국 시장 환경 텍스트 가이드만** (v9.0)
5. **자동화는 챗봇 복붙의 부속 옵션** (v10)
6. **columns.md / rules.md = 학회 도메인 지식 외화** (v10)
7. **단계별 게이트 의무** (v10)
8. **챗봇 복붙 ≡ Skill 자동화 동등성** (v10, 핵심)

---

## 디자인 토큰 (학회 양식 ver2)

```css
--bg-light: #FFFFFF;
--bg-dark: #072A51;             /* Primary Navy */
--card-dark: #0D4889;           /* Secondary Navy */
--orange-primary: #E57728;      /* Accent */
--orange-accent: #E97132;       /* Check Point 알약 */
--text-primary-light: #1F1F1F;
--text-muted: #8A8A8A;
```

---

## 검증 통과 (Sprint 2·3)
- ✅ 학회 양식 ver2 분석 (9 슬라이드 좌표·4 컬러·3 폰트)
- ✅ 삼성전기 1차 빌드: 슬라이드 1 텍스트 11개 자동 매핑 + word_wrap 24건
- ✅ Excel 8 sheets 학회 표준 빌드
- ✅ 위클리 4p / TopPick 8p HTML 템플릿

---

## 다음 단계

| 대상 | 우선순위 |
|---|---|
| 학회 부원 | `prompts/GIC_사용설명서_v10.md` 정독 → 1개 종목 시도 |
| 운영진 | slides-grab 설치 + 1개 종목 풀 테스트 (챗봇 vs Skill 동등성 검증) |
| v10.1 개발 | 표 자동 채움 + Excel yaml 입력 + 자동 위클리 |

---

## 라이선스 / 저작권

본 시스템은 GIC(Gachon Investment Club) 학회 내부 학습·연구 목적으로 작성됨.
지적재산권은 가천대학교 금융투자동아리 GIC에 있음.

문의: GIC 4기 운영팀
