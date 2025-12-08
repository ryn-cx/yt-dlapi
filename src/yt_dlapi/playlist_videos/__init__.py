from typing import Any

from yt_dlapi.playlist_videos import models
from yt_dlapi.protocol import YTDLAPIProtocol


class PlaylistVideosMixin(YTDLAPIProtocol):
    def download_playlist_videos(self, playlist_id: str) -> dict[str, Any]:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        # Need to get the episodes of the playlist so process must be False.
        return self._yt_dlp_request(url)

    def parse_playlist_videos(
        self,
        data: dict[str, Any],
        *,
        update: bool = True,
    ) -> models.PlaylistVideos:
        if update:
            return self.parse_response(models.PlaylistVideos, data, "playlist_videos")

        return models.PlaylistVideos.model_validate(data)

    def get_playlist_videos(self, playlist_id: str) -> models.PlaylistVideos:
        response = self.download_playlist_videos(playlist_id)
        return self.parse_playlist_videos(response)
