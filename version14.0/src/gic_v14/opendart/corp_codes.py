from __future__ import annotations

import zipfile
from pathlib import Path
from xml.etree import ElementTree

from gic_v14.domain import CompanyRecord


class CorpCodeResolver:
    def __init__(self, companies: list[CompanyRecord]) -> None:
        self.companies = companies

    @classmethod
    def from_xml(cls, path: str | Path) -> "CorpCodeResolver":
        root = ElementTree.fromstring(Path(path).read_text(encoding="utf-8"))
        companies: list[CompanyRecord] = []
        for node in root.findall("list"):
            companies.append(
                CompanyRecord(
                    corp_code=_node_text(node, "corp_code"),
                    corp_name=_node_text(node, "corp_name"),
                    stock_code=_node_text(node, "stock_code") or None,
                    modify_date=_node_text(node, "modify_date") or None,
                )
            )
        return cls(companies)

    @classmethod
    def from_zip(cls, path: str | Path) -> "CorpCodeResolver":
        with zipfile.ZipFile(path) as archive:
            xml_name = next(name for name in archive.namelist() if name.lower().endswith(".xml"))
            xml_text = archive.read(xml_name).decode("utf-8")
        root = ElementTree.fromstring(xml_text)
        companies = [
            CompanyRecord(
                corp_code=_node_text(node, "corp_code"),
                corp_name=_node_text(node, "corp_name"),
                stock_code=_node_text(node, "stock_code") or None,
                modify_date=_node_text(node, "modify_date") or None,
            )
            for node in root.findall("list")
        ]
        return cls(companies)

    def resolve(self, corp_name: str | None = None, stock_code: str | None = None, corp_code: str | None = None) -> CompanyRecord:
        if corp_code:
            matches = [company for company in self.companies if company.corp_code == corp_code]
        elif stock_code:
            matches = [company for company in self.companies if company.stock_code == stock_code]
        elif corp_name:
            matches = [company for company in self.companies if corp_name in company.corp_name]
        else:
            raise LookupError("corp_name, stock_code, or corp_code is required")
        if len(matches) != 1:
            raise LookupError(f"Expected one company match, found {len(matches)}")
        return matches[0]


def _node_text(node: ElementTree.Element, tag: str) -> str:
    child = node.find(tag)
    return (child.text or "").strip() if child is not None else ""
