# gic-research rules.md — 처리·전처리·예외 룰

> Skill 실행 시 따라야 할 규칙 모음. design-guide_v10 §11 PPTX 호환성 룰 + 학회 양식 보존 룰.

---

## 1. 학회 양식 보존 (절대 룰)

| 룰 | 사유 |
|---|---|
| 컬러 hex 변경 금지: `#072A51` `#0D4889` `#E57728` `#E97132` | 학회 정체성, 부원 발표 신뢰도 |
| 슬라이드 마스터 변경 금지 | 양식 ver3 갱신 시에만 변경 (운영진 승인) |
| 폰트 패밀리는 기존 양식 유지 | `+mj-ea` `+mn-ea` `프리젠테이션 4 Regular` |
| 슬라이드 크기 19.05cm × 27.52cm 유지 | 보고서 양식 표준 |

---

## 2. 폰트 fallback (Pretendard 누락 시)

```
Pretendard Black → Apple SD Gothic Neo Heavy → Malgun Gothic Bold → sans-serif
Pretendard ExtraBold → Apple SD Gothic Neo Bold → Malgun Gothic Bold
Pretendard → Apple SD Gothic Neo → Malgun Gothic
```

python-pptx 적용 방법:
```python
from pptx.util import Pt
from pptx.dml.color import RGBColor

run.font.name = 'Pretendard'  # 1순위
# python-pptx는 multi-font fallback 직접 지원 X → 슬라이드 마스터 themeFontScheme로 처리
```

---

## 3. 텍스트 처리

### 3.1 글자 수 룰 (자동 검증)
- 위반 시 WARNING + `--auto-truncate` 옵션 제공
- ≤25자 룰: 25자 초과 시 22자 + "…"로 절단 (사용자 승인 후)
- ≤200자 룰: 200자 초과 시 197자 + "…"로 절단

### 3.2 줄바꿈 (line-height)
- Display/Headline: 1.2~1.3
- Body: 1.5~1.6
- 표 셀 짧은 라벨: 1.2~1.3

### 3.3 white-space: nowrap (필수)
다음 클래스/요소는 항상 nowrap:
- 섹션 헤더 ("산업분석", "기업분석" 등)
- BUY/HOLD/SELL 박스
- Check Point 알약
- 표 헤더 행 (≤30자 셀)

python-pptx 적용:
```python
text_frame.word_wrap = False  # 짧은 라벨 한정
```

### 3.4 word_wrap=False 후처리 (필수, design-guide_v10 §11.9)
PPTX 출력 직후 모든 슬라이드 순회하며:
```python
for slide in prs.slides:
    for shape in slide.shapes:
        if not shape.has_text_frame: continue
        tf = shape.text_frame
        if len(tf.text.strip()) <= 30 and len(tf.paragraphs) == 1:
            tf.word_wrap = False
```

---

## 4. 표 처리

### 4.1 표 헤더와 본문 분리 (design-guide_v10 §11.6)
- 헤더 행: 배경 `#072A51` 흰 글자 Bold 11pt
- 본문 행: 배경 흰색 검정 글자 Regular 11pt
- 강조 컬럼 헤더: 글자 `#E57728`
- 행 구분: hairline `#EAEAEA` 1pt

### 4.2 표 행 부족 처리
- 학회 양식 표는 행 수 고정 (예: 시총·외국인 표 = 7행)
- yaml에 행 부족 시 → 빈 행을 "-"로 채움
- 행 초과 시 → ERROR (표 확장 불가, 양식 보존 우선)

### 4.3 셀 패딩
- 6pt × 10pt (양식 ver2 표준)

---

## 5. 이미지 처리

### 5.1 이미지 영역 비어있을 때
- yaml에 `파일경로` 누락 → 영역에 placeholder 텍스트 "[차트/이미지 영역]" 표시
- 부원이 PowerPoint에서 직접 삽입 가능

### 5.2 이미지 크기 자동 맞춤
- 양식 영역 좌표 (W × H) 그대로 적용 → aspect ratio 유지하며 fit
- 이미지가 더 클 경우 contain 모드 (양 옆 공백)
- 이미지가 더 작을 경우 cover 모드는 사용 안 함 (왜곡 방지)

### 5.3 자료 출처 표기 의무
- 모든 차트/이미지 하단에 "자료: [출처]" Pretendard 8pt `#8A8A8A`
- yaml에 `출처` 누락 시 ERROR

---

## 6. PDF 변환 (LibreOffice headless)

### 6.1 변환 명령
```bash
soffice --headless --convert-to pdf --outdir [output_dir] [input.pptx]
```

### 6.2 LibreOffice 미설치 시
- Skill 출력에 PDF 미생성 + WARNING
- 부원이 PowerPoint에서 직접 PDF 저장 (Files → Save As → PDF)

---

## 7. 호환성 점검 (design-guide_v10 §11.7)

PPTX 출력 후 자동 점검 + verify_report.txt 출력:

| 항목 | 체크 방법 | FAIL 시 처리 |
|---|---|---|
| Bold 줄바꿈 | 모든 텍스트 박스의 줄 수 vs 예상 줄 수 | WARNING + 부원에 폰트 0.5pt 줄임 제안 |
| white-space 단어 끊김 | 짧은 라벨 (≤30자) word_wrap 상태 | 자동 word_wrap=False 적용 |
| line-height | 모든 paragraph line_spacing | 1.2~1.3 또는 1.5~1.6 외 값 WARNING |
| padding-bottom | 텍스트 박스 bottom < slide_height - 36pt 체크 | 슬라이드 하단 침범 시 WARNING |
| 폰트 누락 | Pretendard 사용 도형 fallback 매핑 확인 | PASS |

---

## 8. 단계별 게이트 (원칙 7)

각 stage 종료 시 부원 승인 의무:
1. **Intake 완료**: yaml 검증 결과 보고 + 부원 "다음" 입력 대기
2. **Map 완료**: 슬라이드별 매핑 미리보기 (텍스트 요약) + 부원 승인
3. **Render 완료**: 자동 진행 (긴 작업)
4. **Export 완료**: 최종 결과물 보고 + verify_report.txt 함께

→ 부원이 단계 중 "수정" 요청 시 해당 stage로 롤백.

---

## 9. 에러 처리

### 9.1 yaml 파싱 실패
- 부원에게 yaml 형식 가이드 + 첫 에러 라인 표시
- 부록 C 명세 링크 제공

### 9.2 templates/기업리서치_9p.pptx 누락
- ERROR 즉시 중단
- 부원에게 `templates/` 빌드 안내

### 9.3 학회 양식 ver2 폰트 미설치
- WARNING + fallback 폰트 자동 적용
- 부원 PC에 Pretendard 설치 안내 (https://github.com/orioncactus/pretendard)

---

## 10. 챗봇 복붙 동등성 보장 (원칙 8)

이 Skill 결과물(PPTX) vs 부원이 부록 C yaml을 PowerPoint에 직접 매핑한 결과물 비교:
- 텍스트 위치 일치 ≥95%
- 컬러 일치 100%
- 표 데이터 일치 100%
- 이미지 위치/크기 일치 ≥95%
- **차이 발생 시 부록 C yaml 명세 우선 갱신** (Skill columns.md는 명세 따름)
