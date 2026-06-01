# GIC v13 에이전트 자동화 가이드 (스케줄 + 메일)

이 문서는 v13을 **수동 CLI 도구**에서 **스스로 도는 에이전트**로 바꾸는 방법이다.
모든 단계는 **무료**이며, 외부 인증값은 무료 OpenDART API Key와 Gmail 앱 비밀번호뿐이다.

```text
관심종목(watchlist.yaml)
   → 에이전트가 전 기업 일괄 실행 (OpenDART 수집 → 지표 → 초안 + QA)
   → 결과를 메일로 발송
   → 스케줄러가 매주 자동 반복
```

## 1. 에이전트 한 번 실행해보기 (로컬)

```powershell
cd version13.0
python -m pip install -e .

# 키 없이 fixture로 동작 확인
python -m gic_v13.cli agent run examples/watchlist.yaml `
  --fixture-dir tests/fixtures/opendart --output-dir outputs

# 실제 OpenDART로 실행
$env:OPENDART_API_KEY="여기에_본인_키"
python -m gic_v13.cli agent run examples/watchlist.yaml --output-dir outputs
```

`examples/watchlist.yaml`에 기업을 추가/삭제하면 관심종목이 바뀐다.

## 2. 메일 발송 켜기 (Gmail 무료)

### 2.1 Gmail 앱 비밀번호 발급

1. Google 계정 → 보안 → **2단계 인증**을 켠다.
2. 보안 → **앱 비밀번호** 에서 새 비밀번호(16자리)를 만든다.
3. 이 16자리를 `GIC_SMTP_PASSWORD`로 쓴다. (실제 로그인 비밀번호 아님)

### 2.2 환경변수 설정 후 실행

```powershell
$env:OPENDART_API_KEY="여기에_본인_OpenDART_키"
$env:GIC_SMTP_USER="보내는주소@gmail.com"
$env:GIC_SMTP_PASSWORD="앱비밀번호16자리"
$env:GIC_MAIL_TO="받는사람1@gmail.com,받는사람2@naver.com"

python -m gic_v13.cli agent run examples/watchlist.yaml --output-dir outputs --email
```

받는 사람에게 요약 본문 + 각 기업 `preview.html` + `qa_report.md`가 첨부되어 도착한다.
메일 설정이 비어 있으면 발송만 건너뛰고 산출물은 정상 생성된다(에이전트는 멈추지 않는다).

## 3. 자동 반복 — 방법 A: GitHub Actions (권장, 완전 무료)

공개 레포의 Actions는 무료이고, 내 PC가 꺼져 있어도 클라우드에서 돈다.

1. 레포 **Settings → Secrets and variables → Actions → New repository secret** 에서 등록:
   - `OPENDART_API_KEY` (필수)
   - `GIC_SMTP_USER`, `GIC_SMTP_PASSWORD`, `GIC_MAIL_TO` (메일 발송 시)
2. 워크플로 파일은 이미 포함돼 있다: [`.github/workflows/gic-agent.yml`](../../.github/workflows/gic-agent.yml)
3. 기본 스케줄: **매주 월요일 KST 오전 8시**(`cron: "0 23 * * 0"`, UTC 기준).
4. **Actions 탭 → GIC v13 Research Agent → Run workflow** 로 수동 실행도 가능.

> Secrets는 코드·로그에 노출되지 않는다. 키를 파일에 절대 적지 말 것.

## 4. 자동 반복 — 방법 B: Windows 작업 스케줄러 (내 PC)

GitHub Actions 대신 본인 PC에서 돌리고 싶을 때.

1. `run_agent.ps1` 같은 스크립트를 만든다:

   ```powershell
   $env:OPENDART_API_KEY="..."
   $env:GIC_SMTP_USER="...@gmail.com"
   $env:GIC_SMTP_PASSWORD="..."
   $env:GIC_MAIL_TO="..."
   cd "C:\경로\version13.0"
   python -m gic_v13.cli agent run examples/watchlist.yaml --output-dir outputs --email
   ```

2. **작업 스케줄러 → 기본 작업 만들기 → 매주 → 시작 프로그램**:
   - 프로그램: `powershell.exe`
   - 인수: `-ExecutionPolicy Bypass -File "C:\경로\run_agent.ps1"`

> 주의: 이 .ps1에는 키가 들어가므로 공유 폴더·Git에 올리지 말 것(`.gitignore`가 `*.ps1`은 막지 않으니 직접 관리).

## 5. QA 상태 읽기

메일 본문/콘솔의 상태 표시:

- `✅ PASS`: 자동 검사 통과.
- `⚠️ WARNING`: 산출물은 생성됐으나 사람 검토·추가 evidence 필요.
- `❌ FAIL`: 발표 자료로 쓰기 전 반드시 수정.
- `🚫 ERROR`: 해당 기업 실행 자체 실패(종목코드/공시 없음 등). 다른 기업은 계속 실행됨.

어떤 경우에도 `release_approved`는 사람 검토 전까지 `false`다.
