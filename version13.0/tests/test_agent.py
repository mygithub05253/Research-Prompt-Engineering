"""에이전트 레이어 테스트 (오프라인 fixture 사용, 실제 메일 발송 없음)."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from gic_v13.agent.batch import AgentRunResult, load_watchlist, run_watchlist
from gic_v13.agent.mailer import SmtpConfig, build_message, build_summary, send_report_email

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "opendart"


def _write_watchlist(tmp_path: Path) -> Path:
    content = textwrap.dedent(
        """
        requests:
          - run_id: "agent_run_a"
            report_mode: "COMPANY_REPORT"
            sector_id: "DEFENSE"
            primary_entity:
              corp_name: "DEFENSE_FIXTURE_CO"
              stock_code: "000001"
              corp_code: null
            bsns_years: ["2024"]
            reprt_codes: ["11011"]
            fs_div: "CFS"
            as_of_date: "2026-05-31"
            language: "ko-KR"
            output_formats: ["html"]
          - run_id: "agent_run_b"
            report_mode: "COMPANY_REPORT"
            sector_id: "DEFENSE"
            primary_entity:
              corp_name: "한화에어로스페이스"
              stock_code: "012450"
              corp_code: null
            bsns_years: ["2024"]
            reprt_codes: ["11011"]
            fs_div: "CFS"
            as_of_date: "2026-05-31"
            language: "ko-KR"
            output_formats: ["html"]
        """
    ).strip()
    path = tmp_path / "watchlist.yaml"
    path.write_text(content, encoding="utf-8")
    return path


def test_load_watchlist_requires_requests(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("foo: bar\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_watchlist(bad)


def test_run_watchlist_offline(tmp_path: Path) -> None:
    watchlist = _write_watchlist(tmp_path)
    results = run_watchlist(
        watchlist_path=watchlist,
        output_root=tmp_path / "outputs",
        fixture_dir=FIXTURE_DIR,
    )
    assert len(results) == 2
    for result in results:
        assert result.qa_status in {"PASS", "WARNING", "FAIL"}
        assert result.preview_path is not None and result.preview_path.exists()
        assert result.qa_report_path is not None and result.qa_report_path.exists()


def test_build_summary_and_message() -> None:
    results = [
        AgentRunResult(run_id="r1", entity="기업A", qa_status="WARNING", warnings=["KPI 없음"]),
        AgentRunResult(run_id="r2", entity="기업B", qa_status="ERROR", error="boom"),
    ]
    summary = build_summary(results)
    assert "기업A" in summary and "기업B" in summary
    assert "KPI 없음" in summary and "boom" in summary

    config = SmtpConfig(host="smtp.test", port=465, user="a@test.com", password="x", recipients=["b@test.com"])
    message = build_message(results, config)
    assert message["To"] == "b@test.com"
    assert "리서치 초안" in message["Subject"]


def test_send_report_email_skips_without_config(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in ("GIC_SMTP_USER", "GIC_SMTP_PASSWORD", "GIC_MAIL_TO"):
        monkeypatch.delenv(var, raising=False)
    sent = send_report_email([AgentRunResult(run_id="r", entity="e", qa_status="PASS")])
    assert sent is False
