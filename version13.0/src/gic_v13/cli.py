from __future__ import annotations

import argparse
from pathlib import Path

from gic_v13.agent.batch import run_watchlist
from gic_v13.agent.mailer import send_report_email
from gic_v13.config import load_request
from gic_v13.pipeline import run_pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="gic-v13", description="GIC v13 local OpenDART automation CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run one GIC v13 report pipeline")
    run_parser.add_argument("request_file", help="Path to run request YAML")
    run_parser.add_argument("--output-dir", default="outputs", help="Output root directory")
    run_parser.add_argument("--fixture-dir", default=None, help="Offline OpenDART fixture directory")
    run_parser.add_argument("--api-key", default=None, help="OpenDART API key; prefer OPENDART_API_KEY")

    # 에이전트: 관심종목 일괄 실행 + (선택) 메일 발송
    agent_parser = subparsers.add_parser("agent", help="Run a watchlist and optionally email the drafts")
    agent_sub = agent_parser.add_subparsers(dest="agent_command", required=True)
    agent_run = agent_sub.add_parser("run", help="Run all companies in a watchlist YAML")
    agent_run.add_argument("watchlist_file", help="Path to watchlist YAML")
    agent_run.add_argument("--output-dir", default="outputs", help="Output root directory")
    agent_run.add_argument("--fixture-dir", default=None, help="Offline OpenDART fixture directory")
    agent_run.add_argument("--api-key", default=None, help="OpenDART API key; prefer OPENDART_API_KEY")
    agent_run.add_argument("--email", action="store_true", help="Send results via SMTP (env GIC_SMTP_* required)")

    args = parser.parse_args(argv)
    if args.command == "run":
        request = load_request(args.request_file)
        run_dir = run_pipeline(
            request=request,
            output_root=Path(args.output_dir),
            fixture_dir=args.fixture_dir,
            api_key=args.api_key,
        )
        print(f"GIC v13 run written to {run_dir}")
        return 0

    if args.command == "agent" and args.agent_command == "run":
        results = run_watchlist(
            watchlist_path=args.watchlist_file,
            output_root=Path(args.output_dir),
            fixture_dir=args.fixture_dir,
            api_key=args.api_key,
        )
        for result in results:
            print(f"[{result.qa_status}] {result.entity} -> {result.run_dir or result.error}")
        if args.email:
            sent = send_report_email(results)
            print("메일 발송 완료" if sent else "메일 설정(GIC_SMTP_*) 없음 → 발송 생략")
        failed = [r for r in results if r.qa_status == "ERROR"]
        return 1 if failed else 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
