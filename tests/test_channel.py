# TODO: Validate
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from tests.utils import data_path, download_if_missing
from yt_dlapi import YTDLAPI

if TYPE_CHECKING:
    from yt_dlapi.channel import Channel

client = YTDLAPI()

CHANNEL_NAME = "jawed"
"""A channel name."""
CHANNEL_ID = "UC4QobU6STFB0P71PMvOGN5A"
"""channel_id of the jawed channel."""

# Each case is the download method to call and the identifier to pass it.
CASES = [
    ("download_by_name", CHANNEL_NAME),
    ("download_by_id", CHANNEL_ID),
]
IDENTIFIERS = [identifier for _, identifier in CASES]


@pytest.fixture(scope="session")
def endpoint() -> Channel:
    return client.channel


class TestChannel:
    @pytest.mark.parametrize(("method", "identifier"), CASES)
    def test_download(self, endpoint: Channel, method: str, identifier: str) -> None:
        download = getattr(endpoint, method)
        download_if_missing(endpoint, identifier, lambda: download(identifier))

    @pytest.mark.parametrize("identifier", IDENTIFIERS)
    def test_parse(self, endpoint: Channel, identifier: str) -> None:
        data = endpoint.parse(json.loads(data_path(endpoint, identifier).read_text()))
        assert data is not None
        # TODO: assert expected value (needs live data)
