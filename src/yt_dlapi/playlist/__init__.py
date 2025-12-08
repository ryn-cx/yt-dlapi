from typing import Any

from yt_dlapi.playlist import models
from yt_dlapi.protocol import YTDLAPIProtocol


class PlaylistMixin(YTDLAPIProtocol):
    def download_playlist(self, playlist_id: str) -> dict[str, Any]:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        return self._yt_dlp_request(url)

    def parse_playlist(
        self,
        data: dict[str, Any],
        *,
        update: bool = True,
    ) -> models.Playlist:
        if update:
            return self.parse_response(models.Playlist, data, "playlist")

        return models.Playlist.model_validate(data)

    def get_playlist(self, playlist_id: str) -> models.Playlist:
        response = self.download_playlist(playlist_id)
        return self.parse_playlist(response)
