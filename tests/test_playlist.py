# TODO: Validate
import json

import pytest
from yt_dlp.utils import DownloadError

from yt_dlapi import YTDLAPI

client = YTDLAPI()

PLAYLIST_ID = "PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh"
"""playlist_id for Jawed's playlist."""
INVALID_PLAYLIST_ID = "PL12345678901234567890123456789012"


class TestPlaylist:
    def test_get(self) -> None:
        endpoint = client.playlist
        model = endpoint.get(PLAYLIST_ID)
        assert model.id == PLAYLIST_ID
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_invalid_get(self) -> None:
        with pytest.raises(DownloadError):
            client.playlist.get(INVALID_PLAYLIST_ID)

    def test_single_resource_always_has_content(self) -> None:
        endpoint = client.playlist
        assert endpoint.has_content({}) is True

    def test_parse(self) -> None:
        endpoint = client.playlist
        for json_file in endpoint.json_files():
            endpoint.parse(json.loads(json_file.read_text()))
