from typing import Any

from yt_dlapi.protocol import YTDLAPIProtocol

from .models import Model


class Playlist(YTDLAPIProtocol):
    def download_playlist(self, playlist_id: str) -> dict[str, Any]:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        return self._yt_dlp_request(url=url)

    def parse_playlist(self, data: dict[str, Any], *, update: bool = False) -> Model:
        if update:
            return self._parse_response(Model, data, "playlist")

        return Model.model_validate(data)

    def get_playlist(self, channel_name: str) -> Model:
        data = self.download_playlist(channel_name)

        return self.parse_playlist(data)
