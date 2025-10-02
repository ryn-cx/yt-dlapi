import json
from collections.abc import Iterator
from pathlib import Path

import pytest

from yt_dlapi import YTDLAPI
from yt_dlapi.update_files import Updater

# TODO: Having this hardcoded is kind of silly but it works.
client = YTDLAPI(cookie_file=Path(Path.home(), "yt-dlp.txt"))


class TestParsing:
    def get_test_files(self, endpoint: str) -> Iterator[Path]:
        """Get all JSON test files for a given endpoint."""
        updater = Updater(endpoint)
        dir_path = updater.input_folder()
        if not dir_path.exists():
            pytest.fail(f"{dir_path} not found")

        return dir_path.glob("*.json")

    def test_parse_channel(self) -> None:
        for json_file in self.get_test_files("channel"):
            file_content = json.loads(json_file.read_text())
            parsed = client.parse_channel(file_content)
            assert file_content == client.dump_response(parsed)

    def test_parse_playlist(self) -> None:
        for json_file in self.get_test_files("playlist"):
            file_content = json.loads(json_file.read_text())
            parsed = client.parse_playlist(file_content)
            assert file_content == client.dump_response(parsed)

    def test_parse_video(self) -> None:
        for json_file in self.get_test_files("video"):
            file_content = json.loads(json_file.read_text())
            parsed = client.parse_video(file_content)
            assert file_content == client.dump_response(parsed)

    def test_parse_channel_playlists(self) -> None:
        for json_file in self.get_test_files("channel_playlists"):
            file_content = json.loads(json_file.read_text())
            parsed = client.parse_channel_playlists(file_content)
            assert file_content == client.dump_response(parsed)

    def test_parse_playlist_videos(self) -> None:
        for json_file in self.get_test_files("playlist_videos"):
            file_content = json.loads(json_file.read_text())
            parsed = client.parse_playlist_videos(file_content)
            assert file_content == client.dump_response(parsed)


class TestGet:
    def test_get_channel_using_channel_name(self) -> None:
        client.get_channel(channel_name="jawed")

    def test_get_channel_using_channel_id(self) -> None:
        client.get_channel(channel_id="UC4QobU6STFB0P71PMvOGN5A")

    def test_get_playlist(self) -> None:
        client.get_playlist("PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh")

    def test_get_video(self) -> None:
        client.get_video("jNQXAC9IVRw")

    def test_get_age_restricted_video(self) -> None:
        client.get_video("l1ITP7m6R0Q")

    def test_channel_playlists_using_channel_name(self) -> None:
        client.get_channel_playlists(channel_name="jawed")

    def test_channel_playlists_using_channel_id(self) -> None:
        client.get_channel_playlists(channel_id="UC4QobU6STFB0P71PMvOGN5A")

    def test_get_playlist_videos_using_playlist_id(self) -> None:
        client.get_playlist_videos("PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh")

    def test_get_playlist_videos_using_channel_id(self) -> None:
        # Not really the channel id because it was modified to be a playlist id from the
        # channel id.
        client.get_playlist_videos("UU4QobU6STFB0P71PMvOGN5A")
