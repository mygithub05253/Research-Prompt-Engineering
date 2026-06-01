---
name: gic-weekly
description: GIC 위클리 투자리포트 4페이지 자동 생성. slides-grab으로 HTML→PDF/PNG 안정 출력 + anthropic-skills:pptx로 PPTX 부속. 부록 D yaml과 1:1 매핑. 챗봇 복붙 부원도 yaml을 PowerPoint에 직접 매핑하면 동등 결과.
trigger: /gic-weekly [기업명] [--week=YYYY-WW]
---

# /gic-weekly — 위클리 투자리포트 자동 생성 Skill

## 사용법
```
/gic-weekly 삼성전기 --week=2026-W19
[그 다음 부록 D yaml 붙여넣기]
```

## 입력 (yaml)
부록 D 명세 (`prompts/GIC_위클리투자리포트_v10.md`).
4슬라이드 변수: 표지 / 이번주 새 정보 / 멀티플·목표주가 / 모니터링.

## 처리 (slides-grab 4단계 파이프라인 활용)
```
1. /slides-grab-plan
   → templates/위클리_4p.html 베이스 + yaml 데이터 → outline 생성
2. /slides-grab-design
   → slide-01~04.html 생성 (GIC_design-guide_v10 토큰 적용)
3. /slides-grab-export
   → PDF + PNG 출력 (안정)
4. anthropic-skills:pptx
   → PPTX 부속 출력 (선택)
```

## 출력
```
data/output/[기업명]_GIC위클리_YYYYMMDD/
├── slide-01.html ~ slide-04.html
├── [기업명]_GIC위클리_YYYYMMDD.pdf
├── [기업명]_GIC위클리_YYYYMMDD-1.png ~ -4.png
└── [기업명]_GIC위클리_YYYYMMDD.pptx (선택)
```

## 의존
- `templates/위클리_4p.html` — 4페이지 베이스 HTML (design-guide_v10 토큰)
- `../../../design/GIC_design-guide_v10.md` — 디자인 가이드
- slides-grab 플러그인 (Sprint 0에서 설치)
- anthropic-skills:pptx (PPTX 부속)

## 챗봇 복붙 동등성
1. 부원이 챗봇에서 부록 D yaml 받음
2. PowerPoint 새 파일 생성 (16:9 또는 4:3)
3. 4슬라이드를 design-guide_v10 §3 토큰으로 직접 빌드 (네이비 #072A51, 오렌지 #E57728)
4. yaml 변수를 텍스트로 입력 (15분)

총 30~45분. Skill 사용 시 5분.
