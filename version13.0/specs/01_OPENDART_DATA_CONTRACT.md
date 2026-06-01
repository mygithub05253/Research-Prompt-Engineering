# OpenDART Data Contract

## 1. 설계 목적

이 문서는 v13에서 OpenDART API를 어떻게 수집, 캐시, 정규화, 검증할지 정의한다. 목표는 부원이 OpenDART API Key만으로 재무 facts를 자동 수집하고, 출처 추적 가능한 리서치 산출물로 변환하는 것이다.

## 2. 인증키 처리

- API Key는 코드 저장소, 산출물, HTML, QA report에 저장하지 않는다.
- 실행 시 입력하거나 로컬 환경변수 `OPENDART_API_KEY`에서 읽는다.
- `.env` 파일을 지원하더라도 `.env.example`만 저장소에 둔다.
- HTML preview에는 key를 절대 출력하지 않는다.

## 3. 공식 API 범위

| 기능 | endpoint | v13 사용 목적 |
|---|---|---|
| 고유번호 | `/api/corpCode.xml` | corp_code, corp_name, stock_code cache |
| 공시검색 | `/api/list.json` | 사업보고서/분기보고서/반기보고서 접수번호 추적 |
| 기업개황 | `/api/company.json` | 기업명, 종목코드, 법인구분 metadata |
| 단일회사 전체 재무제표 | `/api/fnlttSinglAcntAll.json` | 재무제표 전체 계정 facts |
| 단일회사 주요 재무지표 | `/api/fnlttSinglIndx.json` | 수익성/안정성/성장성/활동성 지표 facts |
| 공시 원문 XML | `/api/document.xml` | 비정형 KPI 후보 추출용 선택 기능 |

## 4. 수집 순서

1. `corpCode.xml`을 다운로드하고 압축을 해제한다.
2. 기업명 또는 종목코드로 `corp_code`를 찾는다.
3. `list.json`으로 정기공시를 검색한다.
4. `fnlttSinglAcntAll.json`으로 재무제표 facts를 가져온다.
5. `fnlttSinglIndx.json`으로 주요 재무지표를 가져온다.
6. 필요한 경우 `document.xml`로 공시 원문을 받아 keyword 후보를 추출한다.
7. raw response를 `outputs/<run_id>/data/raw_opendart/`에 저장한다.
8. canonical schema로 normalize한다.

## 5. 요청 파라미터

### 공통

- `crtfc_key`: OpenDART API Key.
- `corp_code`: 공시대상회사 고유번호 8자리.

### `fnlttSinglAcntAll`

- `bsns_year`: 사업연도 4자리.
- `reprt_code`:
  - `11013`: 1분기보고서
  - `11012`: 반기보고서
  - `11014`: 3분기보고서
  - `11011`: 사업보고서
- `fs_div`:
  - `CFS`: 연결재무제표
  - `OFS`: 재무제표

### `fnlttSinglIndx`

- `idx_cl_code`:
  - `M210000`: 수익성지표
  - `M220000`: 안정성지표
  - `M230000`: 성장성지표
  - `M240000`: 활동성지표

## 6. 필수 저장 metadata

모든 OpenDART-origin fact는 아래를 보존한다.

- `api_endpoint`
- `corp_code`
- `corp_name`
- `stock_code`, if available
- `bsns_year`
- `reprt_code`
- `fs_div`, if applicable
- `rcept_no`, if available
- `retrieved_at`
- `source_url`
- `raw_payload_path`
- `status`
- `message`

## 7. 정규화 규칙

- `thstrm_amount`, `frmtrm_amount`, `bfefrmtrm_amount`를 기간별 fact로 분해한다.
- 분기/반기 손익계산서의 3개월 금액과 누적 금액을 구분한다.
- 금액 문자열의 쉼표, 공백, 괄호 음수, `-`를 처리한다.
- 통화 단위는 OpenDART `currency`와 source metadata를 함께 저장한다.
- `account_id`가 표준 계정이 아니면 계정명 기반 mapping confidence를 낮춘다.
- CFS/OFS를 한 표 안에서 섞지 않는다.

## 8. 오류 처리

| status | 처리 |
|---|---|
| `000` | 정상 수집 |
| `010`/`011` | key 오류로 run fail |
| `012` | IP 제한 또는 접근 제한으로 run fail |
| `013` | 조회 데이터 없음; fact unavailable |
| `014` | 파일 없음; retry 후 unavailable |
| `020` | 요청 제한 초과; backoff 및 cache 사용 |
| `021` | 조회 회사 수 초과; batch 분할 |
| `100` | 파라미터 검증 실패 |
| `800` | 시스템 점검; retry later |
| `900`/`901` | fatal 또는 key 재확인 |

## 9. 방산 KPI 추출 전략

OpenDART 재무 API는 방산 KPI를 표준 필드로 항상 제공하지 않는다. 따라서 v13은 아래 순서로 처리한다.

1. 정기보고서/사업보고서 원문 XML에서 keyword 후보를 찾는다.
2. 후보 텍스트 주변 문단과 표를 `evidence_candidate`로 저장한다.
3. 수치, 단위, 기간, source locator가 명확하면 `pending` fact로 승격한다.
4. 사람 확인 후 `verified`로 승격한다.
5. 자동 확인이 안 되면 `unavailable`로 둔다.

초기 DEFENSE keyword set:

- 수주잔고
- 수주
- 수출
- 계약
- 방산
- 납기
- 생산능력
- 현지화
- 승인
- 환율

## 10. 공식 문서 참조

- OpenDART 오픈API 소개: https://opendart.fss.or.kr/intro/main.do
- 고유번호: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018
- 공시검색: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001
- 단일회사 전체 재무제표: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019020
- 단일회사 주요 재무지표: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2022001

