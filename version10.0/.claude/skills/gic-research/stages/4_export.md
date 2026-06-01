# Stage 4 — Export (PDF + 호환성 점검)

## 입력
Stage 3 출력 PPTX

## 처리

### 4.1 PDF 변환
LibreOffice headless:
```bash
soffice --headless --convert-to pdf --outdir [output_dir] [pptx]
```
LibreOffice 미설치 시 SKIP + WARNING.

### 4.2 호환성 점검 (design-guide_v10 §11.7 + rules.md §7)
`scripts/verify_pptx.py` 호출:
- Bold 줄바꿈 점검
- white-space 단어 끊김 점검
- line-height 점검
- padding-bottom 점검
- 폰트 누락 점검

### 4.3 verify_report.txt 출력
```
[GIC 리서치 PPTX 호환성 점검]
✅ Bold 줄바꿈: PASS (0건)
⚠️ white-space: 슬라이드 1 "Check Point" word_wrap=True 잔존 → 자동 fix
✅ line-height: PASS
✅ padding-bottom: PASS (모든 텍스트 박스 슬라이드 하단 36pt 이내 진입 0건)
✅ 폰트 누락: PASS (Pretendard 정상 매핑)

총 결과: PASS (1건 자동 fix)
```

## 출력
```
data/output/[기업명]_GIC리서치_YYYYMMDD/
├── [기업명]_GIC리서치_YYYYMMDD.pptx
├── [기업명]_GIC리서치_YYYYMMDD.pdf
├── render_log.txt
└── verify_report.txt
```

## 부원 보고
```
✅ /gic-research 완료
- PPTX: data/output/[기업명]_GIC리서치_YYYYMMDD/[기업명]_GIC리서치_YYYYMMDD.pptx
- PDF: 동일 폴더 .pdf
- 점검: PASS

다음 단계:
1. PowerPoint에서 PPTX 열기
2. 슬라이드별로 차트/이미지 영역에 실제 PNG 삽입
3. 자유롭게 텍스트 추가/수정/삭제
4. 발표
```
