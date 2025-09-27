from typing import Any

from yt_dlapi.protocol import YTDLAPIProtocol

from .models import Model


class Channel(YTDLAPIProtocol):
    def download_channel(self, channel_name: str) -> dict[str, Any]:
        url = f"https://www.youtube.com/{channel_name}"
        return self.yt_dlp_request(url=url)

    def parse_channel(self, data: dict[str, Any]) -> Model:
        return self.parse_response(Model, data, "channel")

    def get_channel(self, channel_name: str) -> Model:
        data = self.download_channel(channel_name)

        return self.parse_channel(data)
