# API Key and Setup Guide

## 1. 필요한 것

- OpenDART API Key
- Python 3.11 이상 또는 v13 packaged app
- 인터넷 연결
- 로컬 브라우저

유료 AI 구독, OpenAI API Key, Anthropic API Key, Gemini API Key는 필요하지 않다.

## 2. API Key 입력 방식

권장 순서:

1. 실행 중 UI에서 직접 입력.
2. 로컬 환경변수 `OPENDART_API_KEY` 사용.
3. 개인 PC의 `.env` 사용.

금지:

- README, spec, prompt, report, HTML output에 key 저장.
- 단체 공유 폴더에 `.env` 업로드.
- screenshots에 key 노출.

## 3. Windows 환경변수 예시

```powershell
$env:OPENDART_API_KEY="여기에_개인_API_KEY"
python -m gic_v13 run examples/defense_company_request.yaml
```

이 설정은 현재 PowerShell 세션에만 적용된다.

## 4. 영구 설정을 권장하지 않는 이유

동아리 공용 PC나 공유 계정에서는 key가 남을 수 있다. v13은 세션 입력 또는 UI 입력을 기본으로 설계한다.

## 5. Key 오류 대응

- `010`: 등록되지 않은 key인지 확인.
- `011`: key가 중지되었는지 확인.
- `012`: IP 접근 제한 여부 확인.
- `020`: 요청 제한 초과. cache를 쓰고 다음 실행에서 재시도.
- `800`: OpenDART 점검. 나중에 재시도.

