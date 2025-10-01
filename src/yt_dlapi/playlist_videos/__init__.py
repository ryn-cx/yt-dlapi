from typing import Any

from yt_dlapi.protocol import YTDLAPIProtocol

from .models import Model


class PlaylistVideos(YTDLAPIProtocol):
    def download_playlist_videos(self, playlist_id: str) -> dict[str, Any]:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        # Need to get the episodes of the playlist so process must be False.
        return self._yt_dlp_request(url, process=True)

    def parse_playlist_videos(
        self,
        data: dict[str, Any],
        *,
        update: bool = False,
    ) -> Model:
        if update:
            return self._parse_response(Model, data, "playlist_videos")

        return Model.model_validate(data)

    def get_playlist_videos(self, channel_name: str) -> Model:
        data = self.download_playlist_videos(channel_name)

        return self.parse_playlist_videos(data)
