from typing import Any

from yt_dlapi.protocol import YTDLAPIProtocol

from .models import Model


class Playlist(YTDLAPIProtocol):
    def download_playlist(self, playlist_id: str) -> dict[str, Any]:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        return self.yt_dlp_request(url=url)

    def parse_playlist(self, data: dict[str, Any]) -> Model:
        return self.parse_response(Model, data, "playlist")

    def get_playlist(self, channel_name: str) -> Model:
        data = self.download_playlist(channel_name)

        return self.parse_playlist(data)
