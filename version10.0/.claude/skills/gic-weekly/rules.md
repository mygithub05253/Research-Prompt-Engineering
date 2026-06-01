# gic-weekly rules.md — 위클리 빌드·검증 룰

## 1. 디자인 (GIC_design-guide_v10 §3 적용)
- 슬라이드 1 (표지): 다크 베이스 `#072A51`, 머스타드 강조 X (오렌지 사용)
- 슬라이드 2~4 (본문): 라이트 베이스 `#FFFFFF`, 네이비 섹션 헤더
- 폰트: Pretendard + fallback (Apple SD Gothic Neo → Malgun Gothic)
- 시그니처: 짧은 오렌지 언더라인 1~2개 (슬라이드당)

## 2. PPTX 호환성 (§11 적용)
- line-height 1.2~1.3 (제목), 1.5~1.6 (본문)
- white-space: nowrap (짧은 라벨)
- word_wrap=False 후처리

## 3. slides-grab 활용
- design-guide.md = `../../../design/GIC_design-guide_v10.md`
- 슬라이드 outline 작성 시 yaml 변수 자동 매핑
- HTML 슬라이드는 `templates/위클리_4p.html` 기반 변형

## 4. 안정성 우선
- PDF/PNG 출력 안정 (slides-grab 표준)
- PPTX는 anthropic-skills:pptx로 부속 출력 (선택)
- 부원 PPTX 미세 수정은 PowerPoint에서 자유

## 5. 위클리 핵심 룰
- 직전 vs 이번주 변동을 표로 가시화 (D.2 컨센서스 변화 표 의무)
- 변경 사유 1줄 ≤60자 — 표지 핵심
- 4페이지 강제 채울 필요 없음 (정보 변동 없으면 1줄로 마무리 가능)
