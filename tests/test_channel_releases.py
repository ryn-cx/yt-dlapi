# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utils import assert_error, download_and_save, parse_json
from yt_dlapi.exceptions import NoContentError

if TYPE_CHECKING:
    from yt_dlapi import YTDLAPI
    from yt_dlapi.channel_releases import ChannelReleases

RELEASES_CHANNEL_NAME = "@kendricklamar"
"""channel name of a channel with a releases tab."""


@pytest.fixture(scope="session")
def endpoint(client: YTDLAPI) -> ChannelReleases:
    return client.channel_releases


class TestChannelReleases:
    def test_download(self, endpoint: ChannelReleases) -> None:
        download_and_save(
            endpoint,
            RELEASES_CHANNEL_NAME,
            lambda: endpoint.download_by_name(RELEASES_CHANNEL_NAME),
        )

    def test_parse(self, endpoint: ChannelReleases) -> None:
        data = parse_json(endpoint, RELEASES_CHANNEL_NAME)
        assert data is not None
        # TODO: assert data.uploader_id == RELEASES_CHANNEL_NAME (needs live data)

    def test_invalid(self, endpoint: ChannelReleases) -> None:
        assert_error(
            endpoint,
            "empty",
            lambda: endpoint._parse_or_raise({"entries": []}, "empty"),  # noqa: SLF001
            NoContentError,
        )


def test_log_id(endpoint: ChannelReleases) -> None:
    assert (
        endpoint.get_log_id(channel_name=RELEASES_CHANNEL_NAME)
        == f"ChannelReleases channel_name={RELEASES_CHANNEL_NAME!r}"
    )
