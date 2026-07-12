# TODO: Validate
import json

import pytest
from yt_dlp.utils import DownloadError

from yt_dlapi import YTDLAPI

client = YTDLAPI()

CHANNEL_NAME = "jawed"
"""A channel name."""
CHANNEL_ID = "UC4QobU6STFB0P71PMvOGN5A"
"""channel_id of the jawed channel."""
INVALID_CHANNEL_NAME = "channel"
INVALID_CHANNEL_ID = "UC1234567890123456789012"


class TestChannel:
    def test_get_by_name(self) -> None:
        endpoint = client.channel
        model = endpoint.get_by_name(CHANNEL_NAME)
        assert model.channel == CHANNEL_NAME
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_by_id(self) -> None:
        endpoint = client.channel
        model = endpoint.get_by_id(CHANNEL_ID)
        assert model.channel_id == CHANNEL_ID
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_invalid_get_by_name(self) -> None:
        with pytest.raises(DownloadError):
            client.channel.get_by_name(INVALID_CHANNEL_NAME)

    def test_invalid_get_by_id(self) -> None:
        with pytest.raises(DownloadError):
            client.channel.get_by_id(INVALID_CHANNEL_ID)

    def test_single_resource_always_has_content(self) -> None:
        endpoint = client.channel
        assert endpoint.has_content({}) is True

    def test_parse(self) -> None:
        endpoint = client.channel
        for json_file in endpoint.json_files():
            endpoint.parse(json.loads(json_file.read_text()))
