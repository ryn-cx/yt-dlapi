# TODO: Validate
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from tests.utils import data_path, download_if_missing
from yt_dlapi import YTDLAPI

if TYPE_CHECKING:
    from yt_dlapi.playlist import Playlist

client = YTDLAPI()

PLAYLIST_ID = "PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh"
"""playlist_id for Jawed's playlist."""


@pytest.fixture(scope="session")
def endpoint() -> Playlist:
    return client.playlist


class TestPlaylist:
    def test_download(self, endpoint: Playlist) -> None:
        download_if_missing(
            endpoint,
            PLAYLIST_ID,
            lambda: endpoint.download(PLAYLIST_ID),
        )

    def test_parse(self, endpoint: Playlist) -> None:
        json_file = data_path(endpoint, PLAYLIST_ID)
        data = endpoint.parse(json.loads(json_file.read_text()))
        assert data is not None
        # TODO: assert data.id == PLAYLIST_ID (needs live data)
