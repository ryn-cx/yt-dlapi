# TODO: Validate
"""Tests for the yt_dlapi library."""

import json

import pytest
from yt_dlp.utils import DownloadError

from yt_dlapi import YTDLAPI

client = YTDLAPI()

MINIMUM_ALBUM_COUNT = 2
MINIMUM_RELEASE_COUNT = 2


class TestGet:
    """Test live get requests across every endpoint.

    Every test fetches and validates a real response, then saves it back into the
    model's ``_files/`` corpus so real responses feed future model rebuilds.
    """

    def test_get_channel_by_name(self) -> None:
        """Download, parse, and save a channel by name."""
        model = client.channel.get_by_name("jawed")
        client.channel.save_new_json_file(client.channel.dump(model))

    def test_get_channel_by_id(self) -> None:
        """Download, parse, and save a channel by ID."""
        model = client.channel.get_by_id("UC4QobU6STFB0P71PMvOGN5A")
        client.channel.save_new_json_file(client.channel.dump(model))

    def test_get_channel_playlists_by_name(self) -> None:
        """Download, parse, and save channel playlists by channel name."""
        model = client.channel_playlists.get_by_name("jawed")
        client.channel_playlists.save_new_json_file(
            client.channel_playlists.dump(model),
        )

    def test_get_channel_playlists_by_id(self) -> None:
        """Download, parse, and save channel playlists by channel ID."""
        model = client.channel_playlists.get_by_id("UC4QobU6STFB0P71PMvOGN5A")
        client.channel_playlists.save_new_json_file(
            client.channel_playlists.dump(model),
        )

    def test_get_channel_releases_by_name(self) -> None:
        """Download, parse, and save channel releases by channel name."""
        model = client.channel_releases.get_by_name("@kendricklamar")
        client.channel_releases.save_new_json_file(
            client.channel_releases.dump(model),
        )
        assert len(model.entries) >= MINIMUM_RELEASE_COUNT

    def test_get_playlist(self) -> None:
        """Download, parse, and save a playlist."""
        model = client.playlist.get("PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh")
        client.playlist.save_new_json_file(client.playlist.dump(model))

    def test_get_playlist_videos(self) -> None:
        """Download, parse, and save playlist videos by playlist ID."""
        model = client.playlist_videos.get("PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh")
        client.playlist_videos.save_new_json_file(client.playlist_videos.dump(model))

    def test_get_playlist_videos_by_channel_playlist_id(self) -> None:
        """Download, parse, and save playlist videos by a channel-derived ID."""
        model = client.playlist_videos.get("UU4QobU6STFB0P71PMvOGN5A")
        client.playlist_videos.save_new_json_file(client.playlist_videos.dump(model))

    def test_get_video(self) -> None:
        """Download, parse, and save a video."""
        model = client.video.get("jNQXAC9IVRw")
        client.video.save_new_json_file(client.video.dump(model))


class TestInvalidGet:
    """Test get requests for missing or invalid resources raise DownloadError."""

    def test_invalid_get_channel_by_name(self) -> None:
        """Raise DownloadError when channel name does not exist."""
        with pytest.raises(DownloadError):
            client.channel.get_by_name("channel")

    def test_invalid_get_channel_by_id(self) -> None:
        """Raise DownloadError when channel ID does not exist."""
        with pytest.raises(DownloadError):
            client.channel.get_by_id("UC1234567890123456789012")

    def test_invalid_get_channel_playlists_by_name(self) -> None:
        """Raise DownloadError when channel name does not exist."""
        with pytest.raises(DownloadError):
            client.channel_playlists.get_by_name("channel")

    def test_invalid_get_channel_playlists_by_id(self) -> None:
        """Raise DownloadError when channel ID does not exist."""
        with pytest.raises(DownloadError):
            client.channel_playlists.get_by_id("UC1234567890123456789012")

    def test_invalid_get_playlist(self) -> None:
        """Raise DownloadError when playlist ID does not exist."""
        with pytest.raises(DownloadError):
            client.playlist.get("PL12345678901234567890123456789012")

    def test_invalid_get_playlist_videos(self) -> None:
        """Raise DownloadError when playlist ID does not exist."""
        with pytest.raises(DownloadError):
            client.playlist_videos.get("PL12345678901234567890123456789012")

    def test_invalid_get_video(self) -> None:
        """Raise DownloadError when video ID does not exist."""
        with pytest.raises(DownloadError):
            client.video.get("12345678901")


class TestParse:
    """Test parsing every saved file for each endpoint."""

    def test_parse_channel(self) -> None:
        """Parse all saved channel JSON files."""
        for json_file in client.channel.json_files():
            client.channel.parse(json.loads(json_file.read_text()))

    def test_parse_channel_playlists(self) -> None:
        """Parse all saved channel playlists JSON files."""
        for json_file in client.channel_playlists.json_files():
            client.channel_playlists.parse(json.loads(json_file.read_text()))

    def test_parse_channel_releases(self) -> None:
        """Parse all saved channel releases JSON files."""
        for json_file in client.channel_releases.json_files():
            client.channel_releases.parse(json.loads(json_file.read_text()))

    def test_parse_playlist(self) -> None:
        """Parse all saved playlist JSON files."""
        for json_file in client.playlist.json_files():
            client.playlist.parse(json.loads(json_file.read_text()))

    def test_parse_playlist_videos(self) -> None:
        """Parse all saved playlist videos JSON files."""
        for json_file in client.playlist_videos.json_files():
            client.playlist_videos.parse(json.loads(json_file.read_text()))

    def test_parse_video(self) -> None:
        """Parse all saved video JSON files."""
        for json_file in client.video.json_files():
            client.video.parse(json.loads(json_file.read_text()))


class TestExtract:
    """Test extracting typed entries from responses."""

    def test_extract_channel_playlists_albums(self) -> None:
        """Scrape and extract a Topic channel's album playlists."""
        result = client.channel_playlists.get_albums_by_id(
            "UCo1DYcm1IZ9v3UPkpiAcgtg",
        )
        assert len(result.albums) >= MINIMUM_ALBUM_COUNT
