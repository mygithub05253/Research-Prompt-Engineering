from pathlib import Path

from gic_v13.cli import main


def test_cli_fixture_run_writes_audit_data_narrative_and_html_outputs(tmp_path):
    output_dir = tmp_path / "outputs"

    exit_code = main(
        [
            "run",
            "tests/fixtures/request.yaml",
            "--fixture-dir",
            "tests/fixtures/opendart",
            "--output-dir",
            str(output_dir),
        ]
    )

    run_dir = output_dir / "fixture_cli_run"
    assert exit_code == 0
    assert (run_dir / "audit/source_register.md").exists()
    assert (run_dir / "audit/evidence_matrix.csv").exists()
    assert (run_dir / "audit/calculation_checks.md").exists()
    assert (run_dir / "audit/qa_report.md").exists()
    assert (run_dir / "data/normalized_facts.json").exists()
    assert (run_dir / "data/derived_metrics.json").exists()
    assert (run_dir / "data/sector_kpi_checklist.json").exists()
    assert (run_dir / "data/driver_map.json").exists()
    assert (run_dir / "narrative/report_plan.json").exists()
    assert (run_dir / "narrative/research_thesis.md").exists()
    html = (run_dir / "deliverables/preview.html").read_text(encoding="utf-8")
    qa_report = (run_dir / "audit/qa_report.md").read_text(encoding="utf-8")
    assert "DRAFT - QA NOT APPROVED" in html
    assert "DEFENSE_FIXTURE_CO" in html
    assert "OpenDART" in html
    assert "crtfc_key" not in html
    assert "DEFENSE KPI unavailable" in qa_report
    warnings_section = qa_report.split("## Warnings", 1)[1].split("release_approved", 1)[0]
    assert "- DEFENSE KPI unavailable" in warnings_section
    assert "- None" not in warnings_section
