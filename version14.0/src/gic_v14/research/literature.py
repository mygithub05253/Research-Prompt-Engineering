"""OpenAlex 학술 크롤러 (무료·API키 불필요, 표준 라이브러리만).

'어떤 지표를 실제 연구·기업이 분석하는가'를 문헌 개념 빈도로 확인한다.
네트워크 실패 시 빈 결과 + 사유를 반환(파이프라인은 죽지 않음).
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

OPENALEX = "https://api.openalex.org/works"
MAILTO = "gic.research@example.com"  # OpenAlex polite pool (개인정보 아님)

DEFAULT_QUERIES = [
    "equity valuation financial ratios firm value",
    "valuation multiples PER PBR EV/EBITDA",
    "ROIC EVA economic value added WACC",
    "DuPont analysis return on equity decomposition",
    "company fundamental analysis investment indicators Korea",
    "value investing low PER low PBR excess return",
]


@dataclass
class LiteratureResult:
    queries: list[str]
    works: list[dict[str, Any]] = field(default_factory=list)
    concept_freq: list[tuple[str, int]] = field(default_factory=list)
    note: str = ""

    def to_plain(self) -> dict[str, Any]:
        return {
            "queries": self.queries,
            "works": self.works,
            "concept_freq": self.concept_freq,
            "note": self.note,
        }


def _query_one(query: str, per_page: int = 10) -> list[dict[str, Any]]:
    url = OPENALEX + "?" + urllib.parse.urlencode(
        {
            "search": query,
            "per-page": per_page,
            "mailto": MAILTO,
            "sort": "cited_by_count:desc",
            "select": "title,publication_year,cited_by_count,concepts,doi",
        }
    )
    req = urllib.request.Request(url, headers={"User-Agent": "GIC-v14-research/1.0"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        data = json.load(resp)
    out = []
    for w in data.get("results", []):
        out.append(
            {
                "title": w.get("title") or "(제목 없음)",
                "year": w.get("publication_year"),
                "cited": w.get("cited_by_count", 0),
                "doi": w.get("doi"),
                "concepts": [c["display_name"] for c in (w.get("concepts") or [])[:6]],
            }
        )
    return out


def crawl(queries: list[str] | None = None, per_page: int = 10) -> LiteratureResult:
    queries = queries or DEFAULT_QUERIES
    works: list[dict[str, Any]] = []
    counter: Counter[str] = Counter()
    errors = 0
    for q in queries:
        try:
            results = _query_one(q, per_page=per_page)
            works.extend(results)
            for w in results:
                for c in w["concepts"]:
                    counter[c] += 1
        except Exception:
            errors += 1

    # 중복 제거(제목 기준), 인용수 정렬
    seen, dedup = set(), []
    for w in sorted(works, key=lambda x: x.get("cited", 0), reverse=True):
        key = (w["title"] or "").lower()[:80]
        if key in seen:
            continue
        seen.add(key)
        dedup.append(w)

    note = "OpenAlex 정상" if errors == 0 else f"일부 쿼리 실패({errors}/{len(queries)}) — 네트워크 확인"
    if not dedup:
        note = "문헌 수집 실패(네트워크 불가) — 지표 라이브러리는 내장 근거로 사용 가능"
    return LiteratureResult(
        queries=queries,
        works=dedup[:40],
        concept_freq=counter.most_common(20),
        note=note,
    )
