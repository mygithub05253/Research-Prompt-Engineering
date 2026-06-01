from pathlib import Path

import pytest

from gic_v13.opendart.client import OpenDartClient, OpenDartError


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, payload):
        self.payload = payload
        self.last_params = None

    def get(self, url, params, timeout):
        self.last_params = params
        return FakeResponse(self.payload)


def test_client_adds_key_to_request_but_redacts_it_from_cached_payload(tmp_path):
    session = FakeSession({"status": "000", "message": "정상", "list": []})
    client = OpenDartClient(api_key="SECRET_KEY", cache_dir=tmp_path, session=session)

    payload = client.get_json("fnlttSinglAcntAll", {"corp_code": "00126380"}, cache_name="sample.json")

    assert payload["status"] == "000"
    assert session.last_params["crtfc_key"] == "SECRET_KEY"
    cached = Path(tmp_path / "sample.json").read_text(encoding="utf-8")
    assert "SECRET_KEY" not in cached
    assert "crtfc_key" not in cached


def test_client_raises_for_key_error_status(tmp_path):
    session = FakeSession({"status": "010", "message": "등록되지 않은 인증키입니다."})
    client = OpenDartClient(api_key="BAD_KEY", cache_dir=tmp_path, session=session)

    with pytest.raises(OpenDartError):
        client.get_json("company", {"corp_code": "00126380"}, cache_name="company.json")
