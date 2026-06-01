---
name: gic-toppick
description: GIC 산업 Top Pick 5~8 슬라이드 자동 생성. 산업 진단 + 스크리닝 표 + Top Pick 1~2개 정식 압축 분석 + Risk-Reward 매트릭스. slides-grab + anthropic-skills:pptx. 부록 E yaml과 1:1 매핑.
trigger: /gic-toppick [산업명] [--pick=1|2]
---

# /gic-toppick — 산업 Top Pick 자동 생성 Skill

## 사용법
```
/gic-toppick 반도체 --pick=2
[그 다음 부록 E yaml 붙여넣기]
```

## 입력 (yaml)
부록 E 명세 (`prompts/GIC_산업TopPick_v10.md`).
8슬라이드: 표지 / 산업 진단 / 스크리닝 / Top Pick #1 / Top Pick #2 / Risk-Reward / 모니터링 / Disclaimer.

## 처리 (slides-grab 4단계)
```
1. /slides-grab-plan
2. /slides-grab-design (templates/산업TopPick_8p.html 기반)
3. /slides-grab-export (PDF + PNG)
4. anthropic-skills:pptx (선택)
```

## 출력
```
data/output/[산업명]_TopPick_YYYYMMDD/
├── slide-01.html ~ slide-08.html
├── [산업명]_TopPick_YYYYMMDD.pdf
├── [산업명]_TopPick_YYYYMMDD-1.png ~ -8.png
└── [산업명]_TopPick_YYYYMMDD.pptx (선택)
```

## 의존
- `templates/산업TopPick_8p.html`
- `../../../design/GIC_design-guide_v10.md`
- slides-grab + anthropic-skills:pptx

## 챗봇 복붙 동등성
부원이 부록 E yaml을 받아 PowerPoint에서 8슬라이드 직접 빌드 가능 (45~60분). Skill 사용 시 5분.

## Top Pick 1개 vs 2개
- `--pick=1`: 슬라이드 5(Top Pick #2) 생략, 7슬라이드 출력
- `--pick=2`: 8슬라이드 (기본)
