# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utils import assert_no_content_error, download_if_missing
from yt_dlapi import YTDLAPI

if TYPE_CHECKING:
    from yt_dlapi.channel_playlists import ChannelPlaylists

client = YTDLAPI()

CHANNEL_NAME = "jawed"
"""A channel name."""
CHANNEL_ID = "UC4QobU6STFB0P71PMvOGN5A"
"""channel_id of the jawed channel."""
TOPIC_ID = "UCo1DYcm1IZ9v3UPkpiAcgtg"
"""channel_id for the Tyler, the Creator - Topic channel."""
MINIMUM_ALBUM_COUNT = 2

# Each case is the download method to call and the identifier to pass it.
CASES = [
    ("download_by_name", CHANNEL_NAME),
    ("download_by_id", CHANNEL_ID),
]


@pytest.fixture(scope="session")
def endpoint() -> ChannelPlaylists:
    return client.channel_playlists


class TestChannelPlaylists:
    @pytest.mark.parametrize(("method", "identifier"), CASES)
    def test_download(
        self,
        endpoint: ChannelPlaylists,
        method: str,
        identifier: str,
    ) -> None:
        download = getattr(endpoint, method)
        download_if_missing(endpoint, identifier, lambda: download(identifier))


    def test_invalid(self, endpoint: ChannelPlaylists) -> None:
        assert_no_content_error(
            endpoint,
            "empty",
            lambda: endpoint._parse_or_raise({"entries": []}, type(endpoint).__name__),  # noqa: SLF001
        )
