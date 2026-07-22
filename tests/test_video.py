# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utils import download_and_save, parse_json

if TYPE_CHECKING:
    from yt_dlapi import YTDLAPI
    from yt_dlapi.video import Video

VIDEO_ID = "jNQXAC9IVRw"
"""video id of me at the zoo."""


@pytest.fixture(scope="session")
def endpoint(client: YTDLAPI) -> Video:
    return client.video


class TestVideo:
    def test_download(self, endpoint: Video) -> None:
        download_and_save(endpoint, VIDEO_ID, lambda: endpoint.download(VIDEO_ID))

    def test_parse(self, endpoint: Video) -> None:
        data = parse_json(endpoint, VIDEO_ID)
        assert data is not None
        # TODO: assert data.id == VIDEO_ID (needs live data)
