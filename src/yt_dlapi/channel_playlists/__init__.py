from typing import Any, overload

from yt_dlapi.channel_playlists import models as model
from yt_dlapi.protocol import YTDLAPIProtocol


class ChannelPlaylistsMixin(YTDLAPIProtocol):
    def parse_channel_playlists(
        self,
        data: dict[str, Any],
        *,
        update: bool = False,
    ) -> model.ChannelPlaylists:
        if update:
            return self.parse_response(
                model.ChannelPlaylists,
                data,
                "channel_playlists",
            )

        return model.ChannelPlaylists.model_validate(data)

    @overload
    def download_channel_playlists(self, *, channel_name: str) -> dict[str, Any]: ...
    @overload
    def download_channel_playlists(self, *, channel_id: str) -> dict[str, Any]: ...
    def download_channel_playlists(
        self,
        *,
        channel_name: str | None = None,
        channel_id: str | None = None,
    ) -> dict[str, Any]:
        if channel_name and channel_id:
            msg = "Only one of channel_name or channel_id should be provided."
            raise ValueError(msg)
        if channel_name:
            url = f"https://www.youtube.com/{channel_name}/playlists"
            return self._yt_dlp_request(url)
        if channel_id:
            url = f"https://www.youtube.com/channel/{channel_id}/playlists"
            return self._yt_dlp_request(url)
        msg = "channel_name or channel_id must be provided."
        raise ValueError(msg)

    @overload
    def get_channel_playlists(self, *, channel_name: str) -> model.ChannelPlaylists: ...
    @overload
    def get_channel_playlists(self, *, channel_id: str) -> model.ChannelPlaylists: ...
    def get_channel_playlists(
        self,
        *,
        channel_id: str | None = None,
        channel_name: str | None = None,
    ) -> model.ChannelPlaylists:
        if channel_name and channel_id:
            msg = "Only one of channel_name or channel_id should be provided."
            raise ValueError(msg)
        if channel_name:
            data = self.download_channel_playlists(channel_name=channel_name)
        elif channel_id:
            data = self.download_channel_playlists(channel_id=channel_id)
        else:
            msg = "channel_name or channel_id must be provided."
            raise ValueError(msg)

        return self.parse_channel_playlists(data, update=True)
