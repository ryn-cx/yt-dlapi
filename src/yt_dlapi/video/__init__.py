from typing import Any

from yt_dlapi.protocol import YTDLAPIProtocol

from .models import Model


class Video(YTDLAPIProtocol):
    def download_video(self, video_id: str) -> dict[str, Any]:
        url = f"https://www.youtube.com/watch?v={video_id}"
        return self.yt_dlp_request(url=url)

    def parse_video(self, data: dict[str, Any]) -> Model:
        return self.parse_response(Model, data, "video")

    def get_video(self, channel_name: str) -> Model:
        data = self.download_video(channel_name)

        return self.parse_video(data)
