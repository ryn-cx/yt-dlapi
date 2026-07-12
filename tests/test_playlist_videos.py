# TODO: Validate
import json
from typing import Any

import pytest
from yt_dlp.utils import DownloadError

from yt_dlapi import YTDLAPI
from yt_dlapi.exceptions import NoContentError

client = YTDLAPI()

PLAYLIST_ID = "PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh"
"""playlist_id for Jawed's playlist."""
CHANNEL_UPLOADS_PLAYLIST_ID = "UU4QobU6STFB0P71PMvOGN5A"
"""playlist_id for uploads by jawed."""
INVALID_PLAYLIST_ID = "PL12345678901234567890123456789012"


class TestPlaylistVideos:
    @pytest.mark.parametrize(
        "playlist_id",
        [PLAYLIST_ID, CHANNEL_UPLOADS_PLAYLIST_ID],
        ids=[f"{PLAYLIST_ID=}", f"{CHANNEL_UPLOADS_PLAYLIST_ID=}"],
    )
    def test_get(self, playlist_id: str) -> None:
        endpoint = client.playlist_videos
        model = endpoint.get(playlist_id)
        assert model.id == playlist_id
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_invalid_get(self) -> None:
        with pytest.raises(DownloadError):
            client.playlist_videos.get(INVALID_PLAYLIST_ID)

    def test_empty_entries_has_no_content(self) -> None:
        endpoint = client.playlist_videos
        assert endpoint.has_content({"entries": []}) is False
        assert endpoint.has_content({}) is False
        assert endpoint.has_content({"entries": [{"id": "x"}]}) is True

    def test_empty_entries_raises_no_content_error(self) -> None:
        endpoint = client.playlist_videos
        response: dict[str, Any] = {"entries": []}
        with pytest.raises(NoContentError) as error:
            endpoint._parse_or_raise(response)  # noqa: SLF001
        # The payload is still recoverable from the raised exception.
        assert error.value.response is response
        assert type(endpoint).__name__ in str(error.value)

    def test_parse(self) -> None:
        endpoint = client.playlist_videos
        for json_file in endpoint.json_files():
            endpoint.parse(json.loads(json_file.read_text()))
