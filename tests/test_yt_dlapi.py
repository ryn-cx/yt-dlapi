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
            client.parse_channel(file_content)

    def test_parse_playlist(self) -> None:
        for json_file in self.get_test_files("playlist"):
            file_content = json.loads(json_file.read_text())
            client.parse_playlist(file_content)

    def test_parse_video(self) -> None:
        for json_file in self.get_test_files("video"):
            file_content = json.loads(json_file.read_text())
            client.parse_video(file_content)


class TestGet:
    def test_get_channel(self) -> None:
        client.get_channel("jawed")

    def test_get_playlist(self) -> None:
        client.get_playlist("PLuhl9TnQPDCnWIhy_KSbtFwXVQnNvgfSh")

    def test_get_video(self) -> None:
        client.get_video("jNQXAC9IVRw")

    def test_get_age_restricted_video(self) -> None:
        client.get_video("l1ITP7m6R0Q")
