# GIC v10.0 — 1페이지 마스터 인덱스 (요약본)

> **목적**: v10.0 모든 자산을 한 페이지로 스캔. CLAUDE.md §7.1 규정대로 변경사항·요약본·전체명세 3종 세트 중 "요약본".
> **대상**: 신규 부원 / 기존 부원 마이그레이션 / 학회 외부 참고자.

---

## 한 줄 정의
> **GIC v10.0** = v9.0 챗봇 복붙 100% 베이스 + 학회 양식 PPT/Excel 자동화 4트랙 + slides-grab/anthropic-skills:pptx 통합.

## 폴더 한눈에
```
version10.0/
├── prompts/        4파일 (티어 1·2 — 모든 부원 복붙)
├── design/         디자인 가이드 + 학회 양식 ver2 + 분석 결과
├── templates/      자동화 출력 템플릿 (PPTX/Excel/HTML)
├── .claude/        Skill 4종 (티어 3) + CLAUDE.md
├── data/           샘플 + 출력
└── docs/           본 요약본 + 변경사항 + 자동위클리 설계
```

## 자동화 트랙 5종
| 트랙 | Skill / 자산 | 출력 | 상태 |
|---|---|---|---|
| 1 | `/gic-research` | 학회 양식.pptx 9페이지 | ✅ v0.1 (텍스트 박스 자동) |
| 2 | `/gic-excel --build-template` | 8 sheets Excel | ✅ 빈 양식 빌드 |
| 3 | `/gic-weekly`, `/gic-toppick` | slides-grab HTML→PDF/PNG/PPTX | ✅ Skill + HTML 템플릿 |
| 4 | pykrx-mcp / korea-stock-mcp 가이드 | 데이터 자동 수집 | 📖 가이드 |
| 5 | 자동 위클리 갱신 (cron) | 매주 월 05:00 자동 | 🗓️ 설계만, v10.1+ 구현 |

## 핵심 원칙 (8개)
1. 마크다운 .md 파일만, 외부 의존 0 (v9.0)
2. 정식 9단계 + 블록 라이브러리(A~J) 본질 (v9.0)
3. 외부 벤치마크 흡수, 본질 훼손 금지 (v9.0)
4. 한국 시장 환경 텍스트 가이드만 (v9.0)
5. **자동화는 챗봇 복붙(티어 1)의 부속 옵션** (v10 신규)
6. **columns.md / rules.md = 학회 도메인 지식의 외화** (v10 신규)
7. **단계별 게이트 의무** (v10 신규)
8. **챗봇 복붙 ≡ Skill 자동화 동등성** (v10 신규, 핵심)

## 학회 양식 토큰 (양식 ver2 정확 추출)
- Primary Navy `#072A51` / Secondary Navy `#0D4889`
- Accent Orange `#E57728` / Check Point Orange `#E97132`
- Light base `#FFFFFF`
- 슬라이드 19.05cm × 27.52cm (세로 보고서)
- Pretendard + fallback (Apple SD Gothic Neo → Malgun Gothic)

## 챗봇별 동등 워크플로 (시간 비교)
| 산출물 | Gemini | ChatGPT | Claude 챗봇 | Claude Code Skill |
|---|---|---|---|---|
| 9단계 분석 | 1h | 1h | 1h | 1h |
| 부록 yaml 출력 | 5min | 5min | 5min | 5min |
| 양식 매핑 | 30~45min | 30~45min | 30~45min | **5min** |
| Excel 5개년 | 30min | 15min | 30min | **3min** |
| **합계** | **2h 5min** | **1h 50min** | **2h 5min** | **1h 13min** |

## 검증 통과 항목 (Sprint 2·3)
- ✅ 학회 양식.pptx 분석 (9 슬라이드, 4 컬러, 3 폰트 추출)
- ✅ 트랙 1: 삼성전기.yaml → 학회 양식 9페이지 PPT 자동 생성 (텍스트 11개 박스 매핑 + word_wrap 후처리 24건)
- ✅ 트랙 2: 8 sheets Excel 학회 표준 빌드 (Balance Check 조건부 서식 포함)
- ✅ 트랙 3: 위클리 4페이지 + TopPick 8슬라이드 HTML 템플릿 (design-guide_v10 토큰 적용)

## 핵심 파일 빠른 참조
- 부원 시작점: [`prompts/GIC_사용설명서_v10.md`](../prompts/GIC_사용설명서_v10.md)
- 정식 9단계: [`prompts/GIC_기업리서치_v10.md`](../prompts/GIC_기업리서치_v10.md) (부록 C 9페이지 명세 포함)
- 위클리: [`prompts/GIC_위클리투자리포트_v10.md`](../prompts/GIC_위클리투자리포트_v10.md) (부록 D)
- TopPick: [`prompts/GIC_산업TopPick_v10.md`](../prompts/GIC_산업TopPick_v10.md) (부록 E)
- 디자인 시스템: [`design/GIC_design-guide_v10.md`](../design/GIC_design-guide_v10.md)
- 학회 양식 분석: [`design/양식_분석_결과.md`](../design/양식_분석_결과.md)
- 변경사항 상세: [`docs/GIC_v10.0_변경사항.md`](GIC_v10.0_변경사항.md)
- 자동위클리 설계: [`docs/자동위클리_설계.md`](자동위클리_설계.md)
- 운영진용: [`.claude/CLAUDE.md`](../.claude/CLAUDE.md)

## v10.0 → v10.1 로드맵
1. 트랙 1 v0.2: 표 행 + 이미지 자동 채움
2. 트랙 2 v0.2: yaml → Excel 자동 입력
3. 트랙 4: pykrx/korea-stock MCP Skill 통합
4. 트랙 5: 자동 위클리 cron + 발송 채널
5. 1분기 시범 운영 후 v10.2

---
GIC 4기 운영팀 / 2026-05-09
