# GIC v13 Quickstart

이 문서는 구독형 AI 도구 없이 OpenDART API Key만으로 v13 CLI MVP를 실행하는 방법이다.

## 1. 설치 확인

```powershell
python --version
python -m pytest --version
```

Python 3.11 이상을 권장한다.

## 2. 의존성 설치

```powershell
python -m pip install -e .
```

필요 패키지:

- `requests`
- `PyYAML`
- `jinja2`
- `pytest`

## 3. 오프라인 데모 실행

OpenDART API Key 없이 fixture로 전체 파이프라인을 확인한다.

```powershell
python -m gic_v13.cli run tests/fixtures/request.yaml --fixture-dir tests/fixtures/opendart --output-dir outputs
```

생성 위치:

```text
outputs/fixture_cli_run/
```

열어볼 파일:

```text
outputs/fixture_cli_run/deliverables/preview.html
outputs/fixture_cli_run/audit/qa_report.md
```

## 4. 실제 OpenDART 실행

PowerShell 현재 세션에만 API Key를 넣는다.

```powershell
$env:OPENDART_API_KEY="여기에_본인_OpenDART_API_KEY"
python -m gic_v13.cli run examples/defense_company_request.yaml --output-dir outputs
```

주의:

- API Key는 HTML, JSON, Markdown 산출물에 저장되지 않는다.
- `examples/defense_company_request.yaml`에는 기업명 또는 종목코드를 입력해야 한다.
- OpenDART에 없는 DEFENSE KPI는 `unavailable` 또는 warning으로 남는다.

## 5. 테스트 실행

```powershell
python -m pytest tests -q
```

## 6. QA 결과 해석

- `PASS`: 자동 검사를 통과했다.
- `WARNING`: 산출물은 만들어졌지만 사람 검토 또는 추가 evidence가 필요하다.
- `FAIL`: 회의/발표 자료로 사용하기 전에 반드시 수정해야 한다.

기본적으로 `release_approved`는 `false`다. 사람이 검토하기 전까지 최종본으로 부르지 않는다.

