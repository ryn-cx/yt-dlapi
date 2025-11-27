from typing import Any

from yt_dlapi.protocol import YTDLAPIProtocol
from yt_dlapi.video import models as model


class VideoMixin(YTDLAPIProtocol):
    def download_video(self, video_id: str) -> dict[str, Any]:
        url = f"https://www.youtube.com/watch?v={video_id}"
        return self._yt_dlp_request(url)

    def parse_video(self, data: dict[str, Any], *, update: bool = False) -> model.Video:
        if update:
            return self.parse_response(model.Video, data, "video")

        return model.Video.model_validate(data)

    def get_video(self, channel_name: str) -> model.Video:
        data = self.download_video(channel_name)

        return self.parse_video(data, update=True)
