# TODO: Validate
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from tests.utils import assert_no_content_error, data_path, download_if_missing
from yt_dlapi import YTDLAPI

if TYPE_CHECKING:
    from yt_dlapi.channel_releases import ChannelReleases

client = YTDLAPI()

RELEASES_CHANNEL_NAME = "@kendricklamar"
"""channel name of a channel with a releases tab."""
MINIMUM_RELEASE_COUNT = 2


@pytest.fixture(scope="session")
def endpoint() -> ChannelReleases:
    return client.channel_releases


class TestChannelReleases:
    def test_download(self, endpoint: ChannelReleases) -> None:
        download_if_missing(
            endpoint,
            RELEASES_CHANNEL_NAME,
            lambda: endpoint.download_by_name(RELEASES_CHANNEL_NAME),
        )

    def test_parse(self, endpoint: ChannelReleases) -> None:
        json_file = data_path(endpoint, RELEASES_CHANNEL_NAME)
        data = endpoint.parse(json.loads(json_file.read_text()))
        assert data is not None
        # TODO: assert data.uploader_id == RELEASES_CHANNEL_NAME (needs live data)
        # TODO: assert len(data.entries) >= MINIMUM_RELEASE_COUNT (needs live data)

    def test_invalid(self, endpoint: ChannelReleases) -> None:
        assert_no_content_error(
            endpoint,
            "empty",
            lambda: endpoint._parse_or_raise({"entries": []}, type(endpoint).__name__),  # noqa: SLF001
        )
