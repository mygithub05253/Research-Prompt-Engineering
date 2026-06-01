from __future__ import annotations

import argparse
from pathlib import Path

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
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
