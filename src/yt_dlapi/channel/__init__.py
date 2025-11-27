from typing import Any, overload

from yt_dlapi.channel import models as model
from yt_dlapi.protocol import YTDLAPIProtocol


class ChannelMixin(YTDLAPIProtocol):
    def parse_channel(
        self,
        data: dict[str, Any],
        *,
        update: bool = False,
    ) -> model.Channel:
        if update:
            return self.parse_response(model.Channel, data, "channel")

        return model.Channel.model_validate(data)

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

    @overload
    def get_channel(self, *, channel_name: str) -> model.Channel: ...
    @overload
    def get_channel(self, *, channel_id: str) -> model.Channel: ...
    def get_channel(
        self,
        *,
        channel_id: str | None = None,
        channel_name: str | None = None,
    ) -> model.Channel:
        if channel_name and channel_id:
            msg = "Only one of channel_name or channel_id should be provided."
            raise ValueError(msg)
        if channel_name:
            data = self._download_channel(channel_name=channel_name)
        elif channel_id:
            data = self._download_channel(channel_id=channel_id)
        else:
            msg = "channel_name or channel_id must be provided."
            raise ValueError(msg)

        return self.parse_channel(data, update=True)
