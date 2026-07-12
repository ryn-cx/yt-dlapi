# TODO: Validate
import json

import pytest
from yt_dlp.utils import DownloadError

from yt_dlapi import YTDLAPI

client = YTDLAPI()

VIDEO_ID = "jNQXAC9IVRw"
"""video id of me at the zoo."""
INVALID_VIDEO_ID = "12345678901"


class TestVideo:
    def test_get(self) -> None:
        endpoint = client.video
        model = endpoint.get(VIDEO_ID)
        assert model.id == VIDEO_ID
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_invalid_get(self) -> None:
        with pytest.raises(DownloadError):
            client.video.get(INVALID_VIDEO_ID)

    def test_single_resource_always_has_content(self) -> None:
        endpoint = client.video
        assert endpoint.has_content({}) is True

    def test_parse(self) -> None:
        endpoint = client.video
        for json_file in endpoint.json_files():
            endpoint.parse(json.loads(json_file.read_text()))
