"""v14 파이프라인 오프라인 테스트 (fixture, 네트워크 없음)."""

from __future__ import annotations

from pathlib import Path

from gic_v14.pipeline import run_pipeline
from gic_v14.render.report import build_sparkline, build_peer_bars

FIX = Path(__file__).parent / "fixtures"


def _request() -> dict:
    return {
        "run_id": "test_samsung",
        "report_mode": "COMPANY_REPORT",
        "sector_id": "SEMICONDUCTOR",
        "primary_entity": {"corp_name": "DEFENSE_FIXTURE_CO", "stock_code": "000001", "corp_code": None},
        "bsns_years": ["2024"],
        "reprt_codes": ["11011"],
        "fs_div": "CFS",
        "as_of_date": "2026-06-01",
        "report_meta": {"rating": "BUY", "target_price": 95000, "author": "GIC 4기 테스트"},
        "peers": {"manual": [{"corp_name": "SK하이닉스", "stock_code": "000660"}]},
    }


def test_pipeline_offline(tmp_path: Path) -> None:
    run_dir = run_pipeline(
        request=_request(),
        output_root=tmp_path / "output",
        fixture_dir=FIX / "opendart",
        market_fixture=FIX / "market_samsung.json",
        live_market=False,
    )
    report = run_dir / "deliverables" / "report.html"
    pack = run_dir / "deliverables" / "prompt_pack.md"
    assert report.exists() and pack.exists()
    html = report.read_text(encoding="utf-8")
    assert "GACHON INVESTMENT CLUB" in html
    assert "Check Point" in html
    assert "74,200" in html  # 시장 fixture 현재가가 표지에 반영
    # 에셋 동일 폴더 복사
    assert (run_dir / "deliverables" / "gic_logo.png").exists()
    # 프롬프트 팩: 단계 + 자동주입 데이터
    md = pack.read_text(encoding="utf-8")
    assert "Step 0" in md and "Step 8" in md
    assert "자동주입 데이터" in md
    assert "````" in md  # 4중 백틱


def test_sparkline_and_bars() -> None:
    spark = build_sparkline([{"date": "1", "close": 100}, {"date": "2", "close": 200}])
    assert spark["points"] and spark["hi"] == "200"
    bars = build_peer_bars([{"name": "A", "per": 10}, {"name": "B", "per": 20}])
    assert bars[1]["h"] == 1.0
