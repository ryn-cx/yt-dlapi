from typing import Any

from yt_dlapi.protocol import YTDLAPIProtocol

from .models import PlaylistVideos


class PlaylistVideosMixin(YTDLAPIProtocol):
    def download_playlist_videos(self, playlist_id: str) -> dict[str, Any]:
        url = f"https://www.youtube.com/playlist?list={playlist_id}"
        # Need to get the episodes of the playlist so process must be False.
        return self._yt_dlp_request(url, process=True)

    def parse_playlist_videos(
        self,
        data: dict[str, Any],
        *,
        update: bool = False,
    ) -> PlaylistVideos:
        if update:
            return self._parse_response(PlaylistVideos, data, "playlist_videos")

        return PlaylistVideos.model_validate(data)

    def get_playlist_videos(self, channel_name: str) -> PlaylistVideos:
        data = self.download_playlist_videos(channel_name)

        return self.parse_playlist_videos(data, update=True)
