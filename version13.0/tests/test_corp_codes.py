from pathlib import Path

import pytest

from gic_v13.opendart.corp_codes import CorpCodeResolver


def test_resolves_corp_code_by_stock_code_from_xml_fixture():
    resolver = CorpCodeResolver.from_xml(Path("tests/fixtures/opendart/corp_codes.xml"))

    company = resolver.resolve(stock_code="000001")

    assert company.corp_code == "00126380"
    assert company.corp_name == "DEFENSE_FIXTURE_CO"


def test_raises_on_ambiguous_or_missing_company_query():
    resolver = CorpCodeResolver.from_xml(Path("tests/fixtures/opendart/corp_codes.xml"))

    with pytest.raises(LookupError):
        resolver.resolve(corp_name="없는회사")
