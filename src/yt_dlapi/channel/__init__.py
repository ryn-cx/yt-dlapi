from typing import Any, overload

from yt_dlapi.protocol import YTDLAPIProtocol

from .models import Model


class Channel(YTDLAPIProtocol):
    def parse_channel(self, data: dict[str, Any], *, update: bool = False) -> Model:
        if update:
            return self._parse_response(Model, data, "channel")

        return Model.model_validate(data)

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
            return self._yt_dlp_request(f"https://www.youtube.com/{channel_name}")
        if channel_id:
            return self._yt_dlp_request(f"https://www.youtube.com/channel/{channel_id}")
        msg = "channel_name or channel_id must be provided."
        raise ValueError(msg)

    @overload
    def get_channel(self, *, channel_name: str) -> Model: ...
    @overload
    def get_channel(self, *, channel_id: str) -> Model: ...
    def get_channel(
        self,
        *,
        channel_id: str | None = None,
        channel_name: str | None = None,
    ) -> Model:
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

        return self.parse_channel(data)
