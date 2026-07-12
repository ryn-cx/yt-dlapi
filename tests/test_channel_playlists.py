# TODO: Validate
import json
from typing import Any

import pytest
from yt_dlp.utils import DownloadError

from yt_dlapi import YTDLAPI
from yt_dlapi.exceptions import NoContentError

client = YTDLAPI()

CHANNEL_NAME = "jawed"
"""A channel name."""
CHANNEL_ID = "UC4QobU6STFB0P71PMvOGN5A"
"""channel_id of the jawed channel."""
TOPIC_ID = "UCo1DYcm1IZ9v3UPkpiAcgtg"
"""channel_id for the Tyler, the Creator - Topic channel."""
INVALID_CHANNEL_NAME = "channel"
INVALID_CHANNEL_ID = "UC1234567890123456789012"
MINIMUM_ALBUM_COUNT = 2


class TestChannelPlaylists:
    def test_get_by_name(self) -> None:
        endpoint = client.channel_playlists
        model = endpoint.get_by_name(CHANNEL_NAME)
        assert model.channel == CHANNEL_NAME
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_by_id(self) -> None:
        endpoint = client.channel_playlists
        model = endpoint.get_by_id(CHANNEL_ID)
        assert model.channel_id == CHANNEL_ID
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_invalid_get_by_name(self) -> None:
        with pytest.raises(DownloadError):
            client.channel_playlists.get_by_name(INVALID_CHANNEL_NAME)

    def test_invalid_get_by_id(self) -> None:
        with pytest.raises(DownloadError):
            client.channel_playlists.get_by_id(INVALID_CHANNEL_ID)

    def test_empty_entries_has_no_content(self) -> None:
        endpoint = client.channel_playlists
        assert endpoint.has_content({"entries": []}) is False
        assert endpoint.has_content({}) is False
        assert endpoint.has_content({"entries": [{"id": "x"}]}) is True

    def test_empty_entries_raises_no_content_error(self) -> None:
        endpoint = client.channel_playlists
        response: dict[str, Any] = {"entries": []}
        with pytest.raises(NoContentError) as error:
            endpoint._parse_or_raise(response)  # noqa: SLF001
        # The payload is still recoverable from the raised exception.
        assert error.value.response is response
        assert type(endpoint).__name__ in str(error.value)

    def test_parse(self) -> None:
        endpoint = client.channel_playlists
        for json_file in endpoint.json_files():
            endpoint.parse(json.loads(json_file.read_text()))

    def test_extract_albums(self) -> None:
        result = client.channel_playlists.get_albums_by_id(TOPIC_ID)
        assert len(result.albums) >= MINIMUM_ALBUM_COUNT
