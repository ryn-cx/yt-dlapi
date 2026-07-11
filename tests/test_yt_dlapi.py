# TODO: Validate
from __future__ import annotations

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
RELEASES_CHANNEL_NAME = "@kendricklamar"
"""channel name of a channel with a releases tab."""
PLAYLIST_ID = "PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh"
"""playlist_id for Jawed's playlist."""
CHANNEL_UPLOADS_PLAYLIST_ID = "UU4QobU6STFB0P71PMvOGN5A"
"""playlist_id for uploads by jawed."""
VIDEO_ID = "jNQXAC9IVRw"
"""video id of me at the zoo."""
TOPIC_ID = "UCo1DYcm1IZ9v3UPkpiAcgtg"
"""channel_id for the Tyler, the Creator - Topic channel."""
INVALID_CHANNEL_NAME = "channel"
INVALID_CHANNEL_ID = "UC1234567890123456789012"
INVALID_PLAYLIST_ID = "PL12345678901234567890123456789012"
INVALID_VIDEO_ID = "12345678901"
MINIMUM_RELEASE_COUNT = 2
MINIMUM_ALBUM_COUNT = 2


class TestGet:
    def test_get_channel_by_name(self) -> None:
        endpoint = client.channel
        model = endpoint.get_by_name(CHANNEL_NAME)
        assert model.channel == CHANNEL_NAME
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_channel_by_id(self) -> None:
        endpoint = client.channel
        model = endpoint.get_by_id(CHANNEL_ID)
        assert model.channel_id == CHANNEL_ID
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_channel_playlists_by_name(self) -> None:
        endpoint = client.channel_playlists
        model = endpoint.get_by_name(CHANNEL_NAME)
        assert model.channel == CHANNEL_NAME
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_channel_playlists_by_id(self) -> None:
        endpoint = client.channel_playlists
        model = endpoint.get_by_id(CHANNEL_ID)
        assert model.channel_id == CHANNEL_ID
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_channel_releases_by_name(self) -> None:
        endpoint = client.channel_releases
        model = endpoint.get_by_name(RELEASES_CHANNEL_NAME)
        assert model.uploader_id == RELEASES_CHANNEL_NAME
        assert len(model.entries) >= MINIMUM_RELEASE_COUNT
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_playlist(self) -> None:
        endpoint = client.playlist
        model = endpoint.get(PLAYLIST_ID)
        assert model.id == PLAYLIST_ID
        endpoint.save_new_json_file(endpoint.original_input(model))

    @pytest.mark.parametrize(
        "playlist_id",
        [PLAYLIST_ID, CHANNEL_UPLOADS_PLAYLIST_ID],
        ids=[f"{PLAYLIST_ID=}", f"{CHANNEL_UPLOADS_PLAYLIST_ID=}"],
    )
    def test_get_playlist_videos(self, playlist_id: str) -> None:
        endpoint = client.playlist_videos
        model = endpoint.get(playlist_id)
        assert model.id == playlist_id
        endpoint.save_new_json_file(endpoint.original_input(model))

    def test_get_video(self) -> None:
        endpoint = client.video
        model = endpoint.get(VIDEO_ID)
        assert model.id == VIDEO_ID
        endpoint.save_new_json_file(endpoint.original_input(model))


class TestInvalidGet:
    def test_invalid_get_channel_by_name(self) -> None:
        with pytest.raises(DownloadError):
            client.channel.get_by_name(INVALID_CHANNEL_NAME)

    def test_invalid_get_channel_by_id(self) -> None:
        with pytest.raises(DownloadError):
            client.channel.get_by_id(INVALID_CHANNEL_ID)

    def test_invalid_get_channel_playlists_by_name(self) -> None:
        with pytest.raises(DownloadError):
            client.channel_playlists.get_by_name(INVALID_CHANNEL_NAME)

    def test_invalid_get_channel_playlists_by_id(self) -> None:
        with pytest.raises(DownloadError):
            client.channel_playlists.get_by_id(INVALID_CHANNEL_ID)

    def test_invalid_get_channel_releases_by_name(self) -> None:
        with pytest.raises(DownloadError):
            client.channel_releases.get_by_name(INVALID_CHANNEL_NAME)

    def test_invalid_get_playlist(self) -> None:
        with pytest.raises(DownloadError):
            client.playlist.get(INVALID_PLAYLIST_ID)

    def test_invalid_get_playlist_videos(self) -> None:
        with pytest.raises(DownloadError):
            client.playlist_videos.get(INVALID_PLAYLIST_ID)

    def test_invalid_get_video(self) -> None:
        with pytest.raises(DownloadError):
            client.video.get(INVALID_VIDEO_ID)


# Endpoints whose response lists items under ``entries`` and which therefore have
# an empty-but-valid state (yt-dlp returns ``entries: []`` without raising).
LIST_ENDPOINT_NAMES = ["channel_playlists", "channel_releases", "playlist_videos"]
# Endpoints that represent a single resource and have no empty-but-valid state;
# an invalid target raises ``DownloadError`` instead.
SINGLE_ENDPOINT_NAMES = ["channel", "playlist", "video"]


class TestNoContent:
    """Cover the NoContentError layer without hitting the network.

    Invalid targets already raise ``DownloadError`` (see ``TestInvalidGet``); the
    NoContentError layer instead covers the empty-but-valid response, which is
    hard to pin to a stable real-world fixture, so it is exercised directly.
    """

    @pytest.mark.parametrize("endpoint_name", LIST_ENDPOINT_NAMES)
    def test_empty_entries_has_no_content(self, endpoint_name: str) -> None:
        endpoint = getattr(client, endpoint_name)
        assert endpoint.has_content({"entries": []}) is False
        assert endpoint.has_content({}) is False
        assert endpoint.has_content({"entries": [{"id": "x"}]}) is True

    @pytest.mark.parametrize("endpoint_name", SINGLE_ENDPOINT_NAMES)
    def test_single_resource_always_has_content(self, endpoint_name: str) -> None:
        endpoint = getattr(client, endpoint_name)
        assert endpoint.has_content({}) is True

    @pytest.mark.parametrize("endpoint_name", LIST_ENDPOINT_NAMES)
    def test_empty_entries_raises_no_content_error(self, endpoint_name: str) -> None:
        endpoint = getattr(client, endpoint_name)
        response: dict[str, Any] = {"entries": []}
        with pytest.raises(NoContentError) as error:
            endpoint._parse_or_raise(response)  # noqa: SLF001
        # The payload is still recoverable from the raised exception.
        assert error.value.response is response
        assert type(endpoint).__name__ in str(error.value)


class TestParse:
    @pytest.mark.parametrize(
        "endpoint_name",
        [
            "channel",
            "channel_playlists",
            "channel_releases",
            "playlist",
            "playlist_videos",
            "video",
        ],
    )
    def test_parse(self, endpoint_name: str) -> None:
        endpoint = getattr(client, endpoint_name)
        for json_file in endpoint.json_files():
            endpoint.parse(json.loads(json_file.read_text()))


class TestExtract:
    def test_extract_channel_playlists_albums(self) -> None:
        result = client.channel_playlists.get_albums_by_id(TOPIC_ID)
        assert len(result.albums) >= MINIMUM_ALBUM_COUNT
