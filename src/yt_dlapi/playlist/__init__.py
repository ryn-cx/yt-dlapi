from typing import Any

from yt_dlapi.protocol import YTDLAPIProtocol

from .models import Playlist


class PlaylistMixin(YTDLAPIProtocol):
    def download_playlist(self, playlist_id: str) -> dict[str, Any]:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        return self._yt_dlp_request(url)

    def parse_playlist(self, data: dict[str, Any], *, update: bool = False) -> Playlist:
        if update:
            return self.parse_response(Playlist, data, "playlist")

        return Playlist.model_validate(data)

    def get_playlist(self, channel_name: str) -> Playlist:
        data = self.download_playlist(channel_name)
        return self.parse_playlist(data, update=True)
