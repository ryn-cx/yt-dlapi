# TODO: Validate
import json
from typing import Any

import pytest
from yt_dlp.utils import DownloadError

from yt_dlapi import YTDLAPI
from yt_dlapi.exceptions import NoContentError

client = YTDLAPI()

RELEASES_CHANNEL_NAME = "@kendricklamar"
"""channel name of a channel with a releases tab."""
INVALID_CHANNEL_NAME = "channel"
MINIMUM_RELEASE_COUNT = 2


class TestChannelReleases:
    def test_get_by_name(self) -> None:
        endpoint = client.channel_releases
        model = endpoint.get_by_name(RELEASES_CHANNEL_NAME)
        assert model.uploader_id == RELEASES_CHANNEL_NAME
        assert len(model.entries) >= MINIMUM_RELEASE_COUNT
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_invalid_get_by_name(self) -> None:
        with pytest.raises(DownloadError):
            client.channel_releases.get_by_name(INVALID_CHANNEL_NAME)

    def test_empty_entries_has_no_content(self) -> None:
        endpoint = client.channel_releases
        assert endpoint.has_content({"entries": []}) is False
        assert endpoint.has_content({}) is False
        assert endpoint.has_content({"entries": [{"id": "x"}]}) is True

    def test_empty_entries_raises_no_content_error(self) -> None:
        endpoint = client.channel_releases
        response: dict[str, Any] = {"entries": []}
        with pytest.raises(NoContentError) as error:
            endpoint._parse_or_raise(response)  # noqa: SLF001
        # The payload is still recoverable from the raised exception.
        assert error.value.response is response
        assert type(endpoint).__name__ in str(error.value)

    def test_parse(self) -> None:
        endpoint = client.channel_releases
        for json_file in endpoint.json_files():
            endpoint.parse(json.loads(json_file.read_text()))
