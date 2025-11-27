from typing import Any

from yt_dlapi.playlist import models as model
from yt_dlapi.protocol import YTDLAPIProtocol


class PlaylistMixin(YTDLAPIProtocol):
    def download_playlist(self, playlist_id: str) -> dict[str, Any]:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        return self._yt_dlp_request(url)

    def parse_playlist(
        self,
        data: dict[str, Any],
        *,
        update: bool = False,
    ) -> model.Playlist:
        if update:
            return self.parse_response(model.Playlist, data, "playlist")

        return model.Playlist.model_validate(data)

    def get_playlist(self, channel_name: str) -> model.Playlist:
        data = self.download_playlist(channel_name)
        return self.parse_playlist(data, update=True)
