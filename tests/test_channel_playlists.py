# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utils import assert_error, download_and_save, parse_json
from yt_dlapi.exceptions import NoContentError

if TYPE_CHECKING:
    from yt_dlapi import YTDLAPI
    from yt_dlapi.channel_playlists import ChannelPlaylists

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
def endpoint(client: YTDLAPI) -> ChannelPlaylists:
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
        download_and_save(endpoint, identifier, lambda: download(identifier))

    @pytest.mark.parametrize("identifier", IDENTIFIERS)
    def test_parse(self, endpoint: ChannelPlaylists, identifier: str) -> None:
        data = parse_json(endpoint, identifier)
        assert data is not None
        # TODO: assert expected value (needs live data)

    def test_invalid(self, endpoint: ChannelPlaylists) -> None:
        assert_error(
            endpoint,
            "empty",
            lambda: endpoint._parse_or_raise({"entries": []}, "empty"),  # noqa: SLF001
            NoContentError,
        )


def test_log_id(endpoint: ChannelPlaylists) -> None:
    assert (
        endpoint.get_log_id(channel_name=CHANNEL_NAME)
        == f"ChannelPlaylists channel_name={CHANNEL_NAME!r}"
    )
    assert (
        endpoint.get_log_id(channel_id=CHANNEL_ID)
        == f"ChannelPlaylists channel_id={CHANNEL_ID!r}"
    )
