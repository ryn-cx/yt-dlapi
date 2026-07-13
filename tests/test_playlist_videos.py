# TODO: Validate
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from tests.utils import assert_no_content_error, data_path, download_if_missing
from yt_dlapi import YTDLAPI

if TYPE_CHECKING:
    from yt_dlapi.playlist_videos import PlaylistVideos

client = YTDLAPI()

PLAYLIST_ID = "PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh"
"""playlist_id for Jawed's playlist."""
CHANNEL_UPLOADS_PLAYLIST_ID = "UU4QobU6STFB0P71PMvOGN5A"
"""playlist_id for uploads by jawed."""

PLAYLIST_IDS = [PLAYLIST_ID, CHANNEL_UPLOADS_PLAYLIST_ID]


@pytest.fixture(scope="session")
def endpoint() -> PlaylistVideos:
    return client.playlist_videos


class TestPlaylistVideos:
    @pytest.mark.parametrize("playlist_id", PLAYLIST_IDS)
    def test_download(self, endpoint: PlaylistVideos, playlist_id: str) -> None:
        download_if_missing(
            endpoint,
            playlist_id,
            lambda: endpoint.download(playlist_id),
        )

    @pytest.mark.parametrize("playlist_id", PLAYLIST_IDS)
    def test_parse(self, endpoint: PlaylistVideos, playlist_id: str) -> None:
        json_file = data_path(endpoint, playlist_id)
        data = endpoint.parse(json.loads(json_file.read_text()))
        assert data is not None
        # TODO: assert data.id == playlist_id (needs live data)

    def test_invalid(self, endpoint: PlaylistVideos) -> None:
        assert_no_content_error(
            endpoint,
            "empty",
            lambda: endpoint._parse_or_raise({"entries": []}, type(endpoint).__name__),  # noqa: SLF001
        )
