# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utils import download_and_save, parse_json

if TYPE_CHECKING:
    from yt_dlapi import YTDLAPI
    from yt_dlapi.playlist import Playlist

PLAYLIST_ID = "PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh"
"""playlist_id for Jawed's playlist."""


@pytest.fixture(scope="session")
def endpoint(client: YTDLAPI) -> Playlist:
    return client.playlist


class TestPlaylist:
    def test_download(self, endpoint: Playlist) -> None:
        download_and_save(endpoint, PLAYLIST_ID, lambda: endpoint.download(PLAYLIST_ID))

    def test_parse(self, endpoint: Playlist) -> None:
        data = parse_json(endpoint, PLAYLIST_ID)
        assert data is not None
        # TODO: assert data.id == PLAYLIST_ID (needs live data)
