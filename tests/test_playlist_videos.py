# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utils import assert_error, download_and_save, parse_json
from yt_dlapi.exceptions import NoContentError

if TYPE_CHECKING:
    from yt_dlapi import YTDLAPI
    from yt_dlapi.playlist_videos import PlaylistVideos

PLAYLIST_ID = "PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh"
"""playlist_id for Jawed's playlist."""
CHANNEL_UPLOADS_PLAYLIST_ID = "UU4QobU6STFB0P71PMvOGN5A"
"""playlist_id for uploads by jawed."""

PLAYLIST_IDS = [PLAYLIST_ID, CHANNEL_UPLOADS_PLAYLIST_ID]


@pytest.fixture(scope="session")
def endpoint(client: YTDLAPI) -> PlaylistVideos:
    return client.playlist_videos


class TestPlaylistVideos:
    @pytest.mark.parametrize("playlist_id", PLAYLIST_IDS)
    def test_download(self, endpoint: PlaylistVideos, playlist_id: str) -> None:
        download_and_save(
            endpoint,
            playlist_id,
            lambda: endpoint.download(playlist_id),
        )

    @pytest.mark.parametrize("playlist_id", PLAYLIST_IDS)
    def test_parse(self, endpoint: PlaylistVideos, playlist_id: str) -> None:
        data = parse_json(endpoint, playlist_id)
        assert data is not None
        # TODO: assert data.id == playlist_id (needs live data)

    def test_invalid(self, endpoint: PlaylistVideos) -> None:
        assert_error(
            endpoint,
            "empty",
            lambda: endpoint._parse_or_raise({"entries": []}, "empty"),  # noqa: SLF001
            NoContentError,
        )


def test_log_id(endpoint: PlaylistVideos) -> None:
    expected = f"PlaylistVideos playlist_id={PLAYLIST_ID!r}"
    assert endpoint.get_log_id(PLAYLIST_ID) == expected
