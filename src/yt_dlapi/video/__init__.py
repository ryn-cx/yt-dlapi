from typing import Any

from yt_dlapi.protocol import YTDLAPIProtocol
from yt_dlapi.video import models


class VideoMixin(YTDLAPIProtocol):
    def download_video(self, video_id: str) -> dict[str, Any]:
        url = f"https://www.youtube.com/watch?v={video_id}"
        return self._yt_dlp_request(url)

    def parse_video(self, data: dict[str, Any], *, update: bool = True) -> models.Video:
        if update:
            return self.parse_response(models.Video, data, "video")

        return models.Video.model_validate(data)

    def get_video(self, video_id: str) -> models.Video:
        response = self.download_video(video_id)

        return self.parse_video(response)
