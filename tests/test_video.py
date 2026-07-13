# TODO: Validate
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from tests.utils import data_path, download_if_missing
from yt_dlapi import YTDLAPI

if TYPE_CHECKING:
    from yt_dlapi.video import Video

client = YTDLAPI()

VIDEO_ID = "jNQXAC9IVRw"
"""video id of me at the zoo."""


@pytest.fixture(scope="session")
def endpoint() -> Video:
    return client.video


class TestVideo:
    def test_download(self, endpoint: Video) -> None:
        download_if_missing(
            endpoint,
            VIDEO_ID,
            lambda: endpoint.download(VIDEO_ID),
        )

    def test_parse(self, endpoint: Video) -> None:
        json_file = data_path(endpoint, VIDEO_ID)
        data = endpoint.parse(json.loads(json_file.read_text()))
        assert data is not None
        # TODO: assert data.id == VIDEO_ID (needs live data)
