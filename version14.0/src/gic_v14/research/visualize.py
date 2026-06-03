"""지표 라이브러리 + 문헌 크롤 결과 → research/ HTML 시각화.

지속 발전 연구용. 자체완결 HTML(외부 에셋 없음) — 브라우저로 바로 열림.
"""

from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any

from gic_v14.research.indicators import INDICATOR_LIBRARY, SECTOR_KPIS, SOURCES
from gic_v14.research.literature import LiteratureResult

_CSS = """
body{margin:0;background:#eceef2;font-family:"Malgun Gothic","맑은 고딕","Apple SD Gothic Neo",sans-serif;color:#1c2430;}
.wrap{max-width:980px;margin:0 auto;padding:24px;}
h1{color:#fff;background:linear-gradient(120deg,#143E68,#205A93);padding:18px 22px;border-radius:6px;border-bottom:5px solid #E97132;font-size:22px;}
h2{color:#205A93;border-left:5px solid #205A93;padding-left:10px;margin-top:34px;}
.meta{color:#5b6577;font-size:12px;margin:6px 0 0;}
table{width:100%;border-collapse:collapse;font-size:12.5px;margin:10px 0;}
th,td{border:1px solid #d7dde7;padding:7px 8px;text-align:left;vertical-align:top;}
th{background:#e3edf8;color:#205A93;}
.cat{display:inline-block;background:#205A93;color:#fff;border-radius:3px;padding:1px 7px;font-size:11px;}
.src{font-size:11px;color:#7a8190;}
.bar-row{display:flex;align-items:center;gap:8px;margin:3px 0;font-size:12px;}
.bar-row .lab{width:230px;flex:0 0 230px;text-align:right;color:#333;}
.bar-row .bar{height:14px;background:#3A78B5;border-radius:2px;}
.bar-row .val{color:#205A93;font-weight:700;}
.note{background:#FFF4E0;border:1px solid #E97132;border-radius:4px;padding:8px 12px;font-size:12px;color:#8a5a12;}
li{font-size:12px;line-height:1.7;color:#444;}
.foot{margin-top:30px;color:#9aa3b2;font-size:11px;text-align:center;}
"""


def _indicator_table() -> str:
    rows = []
    for ind in INDICATOR_LIBRARY:
        auto = "🤖 자동" if ind["auto"] else "✍️ 사람/추가수집"
        srcs = ", ".join(ind["src"])
        rows.append(
            f"<tr><td><span class='cat'>{escape(ind['cat'])}</span></td>"
            f"<td><b>{escape(ind['ko'])}</b><br><span class='src'>{escape(ind['id'])}</span></td>"
            f"<td>{escape(ind['formula'])}</td><td>{escape(ind['why'])}</td>"
            f"<td>{auto}</td><td class='src'>{escape(srcs)}</td></tr>"
        )
    return (
        "<table><thead><tr><th>분류</th><th>지표</th><th>공식</th><th>왜 보는가</th>"
        "<th>수집</th><th>출처</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
    )


def _sector_kpi_section() -> str:
    blocks = []
    for sec, kpis in SECTOR_KPIS.items():
        items = "".join(f"<li><b>{escape(k['kpi'])}</b> — {escape(k['why'])}</li>" for k in kpis)
        blocks.append(f"<h3 style='color:#205A93'>{escape(sec)}</h3><ul>{items}</ul>")
    return "".join(blocks)


def _concept_bars(freq: list[tuple[str, int]]) -> str:
    if not freq:
        return "<div class='note'>문헌 개념 데이터 없음(오프라인). 지표 라이브러리는 내장 근거로 사용 가능.</div>"
    mx = max(c for _, c in freq) or 1
    rows = []
    for name, cnt in freq:
        w = int(cnt / mx * 480)
        rows.append(
            f"<div class='bar-row'><span class='lab'>{escape(name)}</span>"
            f"<span class='bar' style='width:{w}px'></span><span class='val'>{cnt}</span></div>"
        )
    return "".join(rows)


def _works_list(works: list[dict[str, Any]]) -> str:
    if not works:
        return "<li>(문헌 없음)</li>"
    out = []
    for w in works[:25]:
        y = w.get("year") or "?"
        cited = w.get("cited", 0)
        doi = w.get("doi") or ""
        link = f" <a href='{escape(doi)}'>{escape(doi)}</a>" if doi else ""
        out.append(f"<li>({y}, 피인용 {cited}) {escape(w['title'][:120])}{link}</li>")
    return "".join(out)


def _sources_list() -> str:
    return "".join(f"<li><b>{escape(k)}</b>: {escape(v)}</li>" for k, v in SOURCES.items())


def render_research_html(result: LiteratureResult, output_path: str | Path, title: str = "GIC 지표 연구") -> Path:
    now = datetime.now().strftime("%Y-%m-%d %H:%M KST")
    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>{escape(title)}</title><style>{_CSS}</style></head><body><div class="wrap">
<h1>📊 {escape(title)} — 기업분석 지표 근거 맵</h1>
<p class="meta">생성 {now} · 데이터: OpenAlex(무료 학술) + 내장 지표 라이브러리(KCI·DBpia·Damodaran) · {escape(result.note)}</p>

<h2>1. 분석해야 할 지표 라이브러리 (근거 포함)</h2>
<p class="meta">실제 학술·실무가 기업가치 분석에 쓰는 지표. 🤖=v14 자동 수집 / ✍️=사람·추가수집(프롬프트 팩 안내).</p>
{_indicator_table()}

<h2>2. 섹터별 KPI (비표준 — 사업보고서·IR)</h2>
{_sector_kpi_section()}

<h2>3. 문헌 개념 빈도 (OpenAlex 크롤 집계)</h2>
<p class="meta">검색 쿼리 {len(result.queries)}건에서 가장 자주 등장한 학술 개념 — '무엇을 분석하는가'의 실증.</p>
{_concept_bars(result.concept_freq)}

<h2>4. 참고 문헌 (피인용 상위)</h2>
<ul>{_works_list(result.works)}</ul>

<h2>5. 출처 정리</h2>
<ul>{_sources_list()}</ul>

<div class="foot">GIC v14 research · 무료 공개데이터 기반 · 본 자료는 학습·연구용입니다.</div>
</div></body></html>"""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out
