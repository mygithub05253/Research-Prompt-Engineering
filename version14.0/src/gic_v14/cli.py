from __future__ import annotations

import argparse
from pathlib import Path

from gic_v14.config import load_request
from gic_v14.pipeline import run_pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="gic-v14", description="GIC v14 기업/산업 리서치 자동화")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="요청 1건 실행 → report.html + prompt_pack.md")
    run.add_argument("request_file", help="input/company_request.yaml 경로")
    run.add_argument("--output-dir", default="output", help="산출물 루트")
    run.add_argument("--fixture-dir", default=None, help="오프라인 OpenDART fixture 폴더")
    run.add_argument("--market-fixture", default=None, help="오프라인 시장데이터 JSON")
    run.add_argument("--no-live-market", action="store_true", help="pykrx 실시간 수집 끄기")
    run.add_argument("--api-key", default=None, help="OpenDART 키(권장: 환경변수 OPENDART_API_KEY)")

    res = sub.add_parser("research", help="학술 문헌 크롤 → research/ 지표연구 HTML 시각화")
    res.add_argument("--output-dir", default="research", help="research 산출 폴더")
    res.add_argument("--offline", action="store_true", help="크롤 없이 내장 지표 라이브러리만 시각화")
    res.add_argument("--per-page", type=int, default=10, help="쿼리당 문헌 수")

    args = parser.parse_args(argv)
    if args.command == "research":
        from datetime import datetime
        from gic_v14.research.literature import crawl, LiteratureResult
        from gic_v14.research.visualize import render_research_html
        result = LiteratureResult(queries=[], note="offline(내장 근거)") if args.offline else crawl(per_page=args.per_page)
        out = Path(args.output_dir) / f"{datetime.now():%Y%m%d}_지표연구.html"
        path = render_research_html(result, out)
        print(f"research 시각화 생성 → {path}")
        print(f"  문헌 {len(result.works)}건 · 개념 {len(result.concept_freq)}종 · {result.note}")
        return 0

    if args.command == "run":
        request = load_request(args.request_file)
        run_dir = run_pipeline(
            request=request,
            output_root=Path(args.output_dir),
            fixture_dir=args.fixture_dir,
            market_fixture=args.market_fixture,
            api_key=args.api_key,
            live_market=not args.no_live_market,
        )
        print(f"완료 → {run_dir}")
        print(f"  - {run_dir / 'deliverables' / 'report.html'}")
        print(f"  - {run_dir / 'deliverables' / 'prompt_pack.md'}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
