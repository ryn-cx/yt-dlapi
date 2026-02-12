"""Tests for the yt_dlapi library."""

import json

from yt_dlapi import YTDLAPI

client = YTDLAPI()


class TestParsing:
    """Tests for parsing saved JSON files into Pydantic models."""

    def test_parse_channel(self) -> None:
        """Parse all saved channel JSON files."""
        for json_file in client.channel.json_files_folder.glob("*.json"):
            file_content = json.loads(json_file.read_text())
            client.channel.parse(file_content)

    def test_parse_playlist(self) -> None:
        """Parse all saved playlist JSON files."""
        for json_file in client.playlist.json_files_folder.glob("*.json"):
            file_content = json.loads(json_file.read_text())
            client.playlist.parse(file_content)

    def test_parse_video(self) -> None:
        """Parse all saved video JSON files."""
        for json_file in client.video.json_files_folder.glob("*.json"):
            file_content = json.loads(json_file.read_text())
            client.video.parse(file_content)

    def test_parse_channel_playlists(self) -> None:
        """Parse all saved channel playlists JSON files."""
        for json_file in client.channel_playlists.json_files_folder.glob("*.json"):
            file_content = json.loads(json_file.read_text())
            client.channel_playlists.parse(file_content)

    def test_parse_playlist_videos(self) -> None:
        """Parse all saved playlist videos JSON files."""
        for json_file in client.playlist_videos.json_files_folder.glob("*.json"):
            file_content = json.loads(json_file.read_text())
            client.playlist_videos.parse(file_content)


class TestGet:
    """Tests for downloading and parsing live data from YouTube."""

    def test_get_channel_using_channel_name(self) -> None:
        """Download and parse a channel by name."""
        client.channel.get_by_name("jawed")

    def test_get_channel_using_channel_id(self) -> None:
        """Download and parse a channel by ID."""
        client.channel.get_by_id("UC4QobU6STFB0P71PMvOGN5A")

    def test_get_playlist(self) -> None:
        """Download and parse a playlist."""
        client.playlist.get("PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh")

    def test_get_video(self) -> None:
        """Download and parse a video."""
        client.video.get("jNQXAC9IVRw")

    def test_channel_playlists_using_channel_name(self) -> None:
        """Download and parse channel playlists by channel name."""
        client.channel_playlists.get_by_name("jawed")

    def test_channel_playlists_using_channel_id(self) -> None:
        """Download and parse channel playlists by channel ID."""
        client.channel_playlists.get_by_id("UC4QobU6STFB0P71PMvOGN5A")

    def test_get_playlist_videos_using_playlist_id(self) -> None:
        """Download and parse playlist videos by playlist ID."""
        client.playlist_videos.get("PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh")

    def test_get_playlist_videos_using_channel_id(self) -> None:
        """Download and parse playlist videos using a channel-derived playlist ID."""
        # Not really the channel id because it was modified to be a playlist id from the
        # channel id.
        client.playlist_videos.get("UU4QobU6STFB0P71PMvOGN5A")
