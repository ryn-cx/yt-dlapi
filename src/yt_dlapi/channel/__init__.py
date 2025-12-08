from typing import Any, overload

from yt_dlapi.channel import models
from yt_dlapi.protocol import YTDLAPIProtocol


class ChannelMixin(YTDLAPIProtocol):
    @overload
    def _download_channel(self, *, channel_name: str) -> dict[str, Any]: ...
    @overload
    def _download_channel(self, *, channel_id: str) -> dict[str, Any]: ...
    def _download_channel(
        self,
        *,
        channel_name: str | None = None,
        channel_id: str | None = None,
    ) -> dict[str, Any]:
        if channel_name and channel_id:
            msg = "Only one of channel_name or channel_id should be provided."
            raise ValueError(msg)
        if channel_name:
            url = f"https://www.youtube.com/@{channel_name}"
            return self._yt_dlp_request(url)
        if channel_id:
            url = f"https://www.youtube.com/channel/{channel_id}"
            return self._yt_dlp_request(url)
        msg = "channel_name or channel_id must be provided."
        raise ValueError(msg)

    def parse_channel(
        self,
        data: dict[str, Any],
        *,
        update: bool = True,
    ) -> models.Channel:
        if update:
            return self.parse_response(models.Channel, data, "channel")

        return models.Channel.model_validate(data)

    @overload
    def get_channel(self, *, channel_name: str) -> models.Channel: ...
    @overload
    def get_channel(self, *, channel_id: str) -> models.Channel: ...
    def get_channel(
        self,
        *,
        channel_id: str | None = None,
        channel_name: str | None = None,
    ) -> models.Channel:
        if channel_name and channel_id:
            msg = "Only one of channel_name or channel_id should be provided."
            raise ValueError(msg)
        if channel_name:
            response = self._download_channel(channel_name=channel_name)
        elif channel_id:
            response = self._download_channel(channel_id=channel_id)
        else:
            msg = "channel_name or channel_id must be provided."
            raise ValueError(msg)

        return self.parse_channel(response)
