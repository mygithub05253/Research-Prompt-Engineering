"""ReportView(dict) → GIC 양식 HTML.

승인된 샘플(output/샘플_삼성전자_리포트.html)을 Jinja2 템플릿(templates/report.html.j2)으로
변환한 것을 렌더한다. 이미지는 HTML과 같은 폴더에 복사(파일명 참조) — 메일/이동에도 안 깨짐.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

ASSET_FILES = ("cover_bg.png", "gic_logo.png")


def build_sparkline(series: list[dict[str, Any]], width: int = 320, height: int = 120) -> dict[str, Any]:
    """주가 시계열 → SVG polyline points + y축 라벨."""
    closes = [float(p["close"]) for p in series if p.get("close") is not None] or [0.0]
    lo, hi = min(closes), max(closes)
    span = (hi - lo) or 1.0
    x0, x1, y0, y1 = 34, width - 4, 10, height - 16
    n = len(closes)
    pts = []
    for i, c in enumerate(closes):
        x = x0 + (x1 - x0) * (i / (n - 1 if n > 1 else 1))
        y = y1 - (y1 - y0) * ((c - lo) / span)
        pts.append(f"{x:.0f},{y:.0f}")
    return {
        "points": " ".join(pts),
        "hi": f"{hi:,.0f}",
        "mid": f"{(hi + lo) / 2:,.0f}",
        "lo": f"{lo:,.0f}",
    }


def build_peer_bars(peers: list[dict[str, Any]], key: str = "per") -> list[dict[str, Any]]:
    """피어 비교용 막대 데이터(0~1 정규화 높이)."""
    vals = [(p.get("name", ""), p.get(key)) for p in peers]
    nums = [v for _, v in vals if isinstance(v, (int, float))]
    mx = max(nums) if nums else 1.0
    bars = []
    for name, v in vals:
        h = (float(v) / mx) if isinstance(v, (int, float)) and mx else 0.0
        bars.append({"name": name, "value": v, "h": round(h, 3)})
    return bars


def _make_env(template_dir: str | Path) -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    def fmt_int(v: Any) -> str:
        return "—" if v is None else f"{float(v):,.0f}"

    def fmt_ratio(v: Any) -> str:
        return "—" if v is None else f"{float(v):.1f}"

    def fmt_pct(v: Any) -> str:
        return "—" if v is None else f"{float(v):.1f}%"

    env.filters["won"] = fmt_int
    env.filters["ratio"] = fmt_ratio
    env.filters["pct"] = fmt_pct
    return env


def render_report(
    view: dict[str, Any],
    output_path: str | Path,
    template_dir: str | Path,
    assets_src: str | Path,
    template_name: str = "report.html.j2",
) -> Path:
    env = _make_env(template_dir)
    # 차트 사전계산
    view = dict(view)
    view["spark"] = build_sparkline(view.get("price_series", []))
    view["peer_bars"] = build_peer_bars(view.get("peers", []), key="per")

    html = env.get_template(template_name).render(**view)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

    # 에셋을 HTML과 같은 폴더로 복사
    for name in ASSET_FILES:
        src = Path(assets_src) / name
        if src.exists():
            shutil.copy(src, out.parent / name)
    return out
