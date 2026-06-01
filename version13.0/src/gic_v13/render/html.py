from __future__ import annotations

from html import escape
from pathlib import Path

from gic_v13.domain import DerivedMetric, FinancialFact, QaReport, ReportPlan


def render_html(
    plan: ReportPlan,
    facts: list[FinancialFact],
    derived_metrics: list[DerivedMetric],
    qa_report: QaReport,
    output_path: str | Path,
) -> None:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fact_rows = "\n".join(
        f"<tr><td>{escape(fact.period)}</td><td>{escape(fact.metric_name)}</td><td>{fact.value}</td>"
        f"<td>{escape(fact.unit)}</td><td>{escape(fact.source_id)}</td></tr>"
        for fact in facts
    )
    metric_rows = "\n".join(
        f"<tr><td>{escape(metric.period)}</td><td>{escape(metric.metric_name)}</td><td>{metric.value}</td>"
        f"<td>{escape(metric.formula)}</td></tr>"
        for metric in derived_metrics
    )
    pages = "\n".join(_render_page(page) for page in plan.pages_or_slides)
    gates = "\n".join(
        f"<tr><td>{escape(gate)}</td><td>{escape(status)}</td></tr>"
        for gate, status in qa_report.gates.items()
    )
    warnings = "".join(f"<li>{escape(item)}</li>" for item in qa_report.warnings)
    html = f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>GIC v13 Report Preview - {escape(plan.entity)}</title>
  <style>
    :root {{
      --gic-navy: #172A46;
      --gic-orange: #F28C28;
      --gic-ink: #1E2430;
      --gic-line: #D8DEE8;
      --gic-bg: #F6F8FB;
    }}
    body {{
      margin: 0;
      background: var(--gic-bg);
      color: var(--gic-ink);
      font-family: "Malgun Gothic", "Apple SD Gothic Neo", Arial, sans-serif;
    }}
    header {{
      background: var(--gic-navy);
      color: white;
      padding: 20px 28px;
      border-bottom: 6px solid var(--gic-orange);
    }}
    .status {{
      display: inline-block;
      margin-top: 8px;
      padding: 4px 8px;
      background: var(--gic-orange);
      color: #111;
      font-weight: 700;
    }}
    main {{
      max-width: 980px;
      margin: 24px auto;
      padding: 0 18px;
    }}
    section.page {{
      background: white;
      border: 1px solid var(--gic-line);
      margin-bottom: 18px;
      padding: 22px;
    }}
    h1, h2, h3 {{ margin-top: 0; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0 20px;
      font-size: 13px;
    }}
    th, td {{
      border: 1px solid var(--gic-line);
      padding: 7px 8px;
      text-align: left;
    }}
    th {{
      background: #EDF2F7;
    }}
    .source-label {{
      font-size: 12px;
      color: #4A5568;
      margin-top: 4px;
    }}
    .qa-warning {{
      background: #FFF8EC;
      border-left: 4px solid var(--gic-orange);
      padding: 10px 12px;
    }}
  </style>
</head>
<body>
  <header data-qa-status="{escape(plan.draft_status)}">
    <h1>{escape(plan.entity)} GIC v13 HTML Preview</h1>
    <div>Mode: {escape(plan.mode)} | Orientation: {escape(plan.orientation)} | As of: {escape(plan.as_of_date)}</div>
    <div class="status">{escape(plan.draft_status)}</div>
  </header>
  <main>
    {pages}
    <section class="page">
      <h2>OpenDART Financial Facts</h2>
      <table><thead><tr><th>Period</th><th>Metric</th><th>Value</th><th>Unit</th><th>Source</th></tr></thead><tbody>{fact_rows}</tbody></table>
      <h2>Derived Metrics</h2>
      <table><thead><tr><th>Period</th><th>Metric</th><th>Value</th><th>Formula</th></tr></thead><tbody>{metric_rows}</tbody></table>
      <div class="source-label">Source: OpenDART normalized facts. API key is never written to this HTML.</div>
    </section>
    <section class="page">
      <h2>QA Gates</h2>
      <table><thead><tr><th>Gate</th><th>Status</th></tr></thead><tbody>{gates}</tbody></table>
      <div class="qa-warning"><strong>Warnings</strong><ul>{warnings}</ul></div>
    </section>
  </main>
</body>
</html>
"""
    output.write_text(html, encoding="utf-8")


def _render_page(page) -> str:
    charts = "".join(
        f"<div><strong>{escape(chart.chart_id)}</strong> ({escape(chart.chart_type)})"
        f"<div class=\"source-label\">{escape(chart.source_label)}</div></div>"
        for chart in page.charts
    )
    blocks = "".join(f"<p>{escape(block)}</p>" for block in page.narrative_blocks)
    notes = "".join(f"<li>{escape(note)}</li>" for note in page.visual_qa_notes)
    return f"""
    <section class="page" data-page-index="{page.index}" data-claim-ids="{escape(','.join(page.key_claim_ids))}">
      <h2>{page.index}. {escape(page.title)}</h2>
      <p><strong>Objective:</strong> {escape(page.objective)}</p>
      {blocks}
      {charts}
      <ul>{notes}</ul>
    </section>
    """
